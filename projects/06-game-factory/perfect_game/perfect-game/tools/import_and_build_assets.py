"""Import AI plates → seamless tiles + cutout props for Paper Isle."""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets" / "raw"
PROC = ROOT / "assets" / "processed"
TILES = ROOT / "assets" / "tiles"
QA = ROOT / "assets" / "qa"
TS = 64

# Cursor session generated assets (absolute).
CURSOR_ASSETS = Path(r"C:\Users\孤白赟悫\.cursor\projects\d-Infinite-Sustainable\assets")

# rembg models: D-drive probe convention
PROBE_REMBG = Path(
    r"d:\Infinite_ Sustainable\projects\06-game-factory\visual_capability_probe\cursor-demo\tools\rembg_models"
)
os.environ.setdefault("U2NET_HOME", str(PROBE_REMBG))
os.environ.setdefault("REMBG_HOME", str(PROBE_REMBG))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seamless import make_seamless, extract_tile, seam_score, stitch_grid  # noqa: E402

PROP_MAP = {
    "paper-prop-player.png": "player.png",
    "paper-prop-tree.png": "tree.png",
    "paper-prop-cottage.png": "cottage.png",
    "paper-prop-star.png": "star.png",
    "paper-prop-flowers.png": "flowers.png",
}

TEX_MAP = {
    "paper-tex-grass.png": "src_grass.png",
    "paper-tex-path.png": "src_path.png",
    "paper-tex-water.png": "src_water.png",
}

# Target logical sizes after cutout (max side).
PROP_MAX = {
    "player.png": 64,
    "tree.png": 120,
    "cottage.png": 140,
    "star.png": 40,
    "flowers.png": 56,
}


def ensure_dirs() -> None:
    for p in (RAW, PROC, TILES, QA):
        p.mkdir(parents=True, exist_ok=True)


def copy_sources() -> None:
    if not CURSOR_ASSETS.is_dir():
        print("WARN: cursor assets missing:", CURSOR_ASSETS)
        return
    for src_name, dst_name in {**PROP_MAP, **TEX_MAP}.items():
        src = CURSOR_ASSETS / src_name
        if src.is_file():
            shutil.copy2(src, RAW / dst_name)
            print("copy", src_name, "->", dst_name)
        else:
            print("MISS", src)


def chroma_magenta(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            # hot magenta / pink screen
            if r > 190 and b > 160 and g < 110:
                px[x, y] = (0, 0, 0, 0)
            elif r > 200 and b > 200 and g < 90:
                px[x, y] = (0, 0, 0, 0)
            elif r > 180 and g < 90 and 90 < b < 200 and r - g > 80:
                # AI hot-pink #ED067A-ish
                px[x, y] = (0, 0, 0, 0)
    return rgba


def trim_alpha(img: Image.Image, pad: int = 2) -> Image.Image:
    rgba = img.convert("RGBA")
    bbox = rgba.getbbox()
    if not bbox:
        return rgba
    l, t, r, b = bbox
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(rgba.width, r + pad)
    b = min(rgba.height, b + pad)
    return rgba.crop((l, t, r, b))


def resize_max(img: Image.Image, max_side: int) -> Image.Image:
    w, h = img.size
    m = max(w, h)
    if m <= max_side:
        return img
    scale = max_side / float(m)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    return img.resize((nw, nh), Image.Resampling.LANCZOS)


def maybe_rembg(img: Image.Image) -> Image.Image:
    if os.environ.get("USE_REMBG") != "1":
        return img
    from rembg import remove, new_session

    model = os.environ.get("REMBG_MODEL", "u2net")
    session = new_session(model)
    rgb = Image.new("RGB", img.size, (255, 0, 255))
    rgb.paste(img.convert("RGB"), mask=img.split()[-1] if img.mode == "RGBA" else None)
    return remove(rgb, session=session).convert("RGBA")


def checkerboard(size: tuple[int, int], cell: int = 8) -> Image.Image:
    w, h = size
    board = Image.new("RGBA", (w, h))
    px = board.load()
    c1, c2 = (220, 220, 220, 255), (160, 160, 160, 255)
    for y in range(h):
        for x in range(w):
            px[x, y] = c1 if ((x // cell) + (y // cell)) % 2 == 0 else c2
    return board


def process_props() -> None:
    for raw_name in PROP_MAP.values():
        src = RAW / raw_name
        if not src.is_file():
            print("skip prop missing", raw_name)
            continue
        img = Image.open(src).convert("RGBA")
        out = chroma_magenta(maybe_rembg(chroma_magenta(img)))
        out = trim_alpha(out)
        out = resize_max(out, PROP_MAX.get(raw_name, 64))
        out.save(PROC / raw_name)
        board = checkerboard(out.size)
        board.alpha_composite(out)
        board.convert("RGB").save(QA / f"checker_{raw_name}", quality=92)
        print("prop", raw_name, out.size)


def blend_edge(a: Image.Image, b: Image.Image, side: str) -> Image.Image:
    """Soft transition tile: a dominates interior, b bleeds from side."""
    a = a.convert("RGB").resize((TS, TS))
    b = b.convert("RGB").resize((TS, TS))
    aa = __import__("numpy").asarray(a, dtype=float)
    bb = __import__("numpy").asarray(b, dtype=float)
    import numpy as np

    yy, xx = np.mgrid[0:TS, 0:TS]
    if side == "n":
        t = np.clip(1.0 - yy / (TS * 0.55), 0, 1)
    elif side == "s":
        t = np.clip((yy - TS * 0.45) / (TS * 0.55), 0, 1)
    elif side == "w":
        t = np.clip(1.0 - xx / (TS * 0.55), 0, 1)
    elif side == "e":
        t = np.clip((xx - TS * 0.45) / (TS * 0.55), 0, 1)
    else:
        t = np.zeros((TS, TS))
    t = t[..., None]
    mix = aa * (1 - t) + bb * t
    return Image.fromarray(np.clip(mix, 0, 255).astype("uint8"))


def build_tiles() -> None:
    import numpy as np

    bases: dict[str, Image.Image] = {}
    for key, raw in (("grass", "src_grass.png"), ("path", "src_path.png"), ("water", "src_water.png")):
        src = RAW / raw
        if not src.is_file():
            # procedural fallback papercraft flat
            colors = {"grass": (140, 186, 120), "path": (210, 186, 140), "water": (120, 176, 210)}
            img = Image.new("RGB", (256, 256), colors[key])
            dr = ImageDraw.Draw(img)
            for i in range(0, 256, 8):
                shade = tuple(max(0, c - 12) for c in colors[key])
                dr.line([(i, 0), (i, 255)], fill=shade)
            src_img = img
        else:
            src_img = Image.open(src)

        # Iterate seamless until under threshold or max tries
        tile = extract_tile(src_img, 128)
        best = None
        best_score = 999.0
        cur = tile
        for _ in range(6):
            cur = make_seamless(cur, feather=max(10, cur.size[0] // 6))
            sc = seam_score(cur)
            if sc < best_score:
                best_score = sc
                best = cur.copy()
            if sc <= 12.0:
                break
        assert best is not None
        tile64 = best.resize((TS, TS), Image.Resampling.LANCZOS)
        # Final micro-heal if still high
        if seam_score(tile64) > 12.0:
            tile64 = make_seamless(tile64, feather=12).resize((TS, TS), Image.Resampling.LANCZOS)
        bases[key] = tile64
        tile64.save(TILES / f"tile_{key}.png")
        print(f"tile_{key} seam={seam_score(tile64):.3f}")

    # Transition tiles grass↔water / grass↔path
    for side in ("n", "s", "e", "w"):
        gw = blend_edge(bases["grass"], bases["water"], side)
        gw = make_seamless(gw, feather=6).resize((TS, TS), Image.Resampling.LANCZOS)
        # Don't force full wrap seam on transition tiles — they are edge pieces.
        gw.save(TILES / f"tile_gw_{side}.png")
        gp = blend_edge(bases["grass"], bases["path"], side)
        gp.save(TILES / f"tile_gp_{side}.png")

    # Atlas strip for Godot: grass, path, water, gw_n/s/e/w
    names = [
        "tile_grass.png",
        "tile_path.png",
        "tile_water.png",
        "tile_gw_n.png",
        "tile_gw_s.png",
        "tile_gw_e.png",
        "tile_gw_w.png",
        "tile_gp_n.png",
        "tile_gp_s.png",
        "tile_gp_e.png",
        "tile_gp_w.png",
    ]
    atlas = Image.new("RGBA", (TS * len(names), TS))
    for i, name in enumerate(names):
        atlas.paste(Image.open(TILES / name).convert("RGBA"), (i * TS, 0))
    atlas.save(TILES / "atlas_terrain.png")
    print("atlas", atlas.size)

    # Meta for GDScript
    meta = {
        "tile_size": TS,
        "names": [n.replace("tile_", "").replace(".png", "") for n in names],
    }
    import json

    (TILES / "atlas_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def write_seam_report() -> int:
    # Only score pure wrap tiles
    import json

    report = {"threshold": 12.0, "tiles": {}}
    ok_all = True
    for name in ("tile_grass.png", "tile_path.png", "tile_water.png"):
        path = TILES / name
        img = Image.open(path)
        sc = seam_score(img)
        ok = sc <= 12.0
        ok_all = ok_all and ok
        stitch_grid(img, 3).save(QA / f"seam_{path.stem}_3x3.png")
        report["tiles"][name] = {"seam_score": round(sc, 3), "pass": ok}
        print(("PASS" if ok else "FAIL"), name, sc)
    report["all_pass"] = ok_all
    (QA / "seam_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0 if ok_all else 2


def main() -> int:
    ensure_dirs()
    copy_sources()
    process_props()
    build_tiles()
    return write_seam_report()


if __name__ == "__main__":
    raise SystemExit(main())
