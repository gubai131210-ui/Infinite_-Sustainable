"""Import AI sheets with geometric slicing (magenta key + equal cells / rows)."""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\孤白赟悫\.cursor\projects\d-Infinite-Sustainable\assets")
RAW = ROOT / "assets" / "raw"
OUT = ROOT / "assets" / "processed"
QA = ROOT / "assets" / "qa"

H_HUMAN = 48
TILE = 16


def chroma(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            # classic magenta
            if r >= 180 and b >= 160 and g <= 140 and r + b > g * 2.2:
                px[x, y] = (0, 0, 0, 0)
                continue
            if r >= 200 and b >= 200 and g < 160:
                px[x, y] = (0, 0, 0, 0)
                continue
            # AI hot-pink / rose key (high R, low G, mid-low B) e.g. (237,6,122)
            if r >= 190 and g <= 80 and b <= 180 and r > b + 40 and r > g + 80:
                px[x, y] = (0, 0, 0, 0)
                continue
            if r >= 210 and g <= 40 and 80 <= b <= 170:
                px[x, y] = (0, 0, 0, 0)
                continue
    return rgba


def opaque_bbox(img: Image.Image, pad: int = 2):
    a = img.split()[-1]
    b = a.getbbox()
    if not b:
        return None
    l, t, r, bot = b
    return (
        max(0, l - pad),
        max(0, t - pad),
        min(img.width, r + pad),
        min(img.height, bot + pad),
    )


def crop_op(img: Image.Image) -> Image.Image:
    b = opaque_bbox(img)
    return img.crop(b) if b else img


def save(img: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    img.save(OUT / name)
    board = Image.new("RGBA", img.size)
    px = board.load()
    for y in range(img.height):
        for x in range(img.width):
            px[x, y] = (220, 220, 220, 255) if ((x // 8) + (y // 8)) % 2 == 0 else (160, 160, 160, 255)
    board.alpha_composite(img)
    board.convert("RGB").save(QA / f"checker_{name}", quality=92)
    print(f"  OK {name} {img.size}")


def fit_cell(fr: Image.Image, cell: int, target_h: int | None = None, max_w: int | None = None) -> Image.Image:
    fr = crop_op(fr)
    th = target_h or (cell - 2)
    if fr.height < 1:
        return Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
    scale = th / fr.height
    w = max(1, int(round(fr.width * scale)))
    if max_w and w > max_w:
        w = max_w
        th = max(1, int(round(fr.height * (w / fr.width))))
    fr = fr.resize((w, th), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
    canvas.alpha_composite(fr, ((cell - w) // 2, cell - th))
    return canvas


def sheet_from_frames(frames: list[Image.Image], cell: int, target_h: int, max_w: int) -> Image.Image:
    cells = [fit_cell(f, cell, target_h, max_w) for f in frames]
    out = Image.new("RGBA", (cell * len(cells), cell), (0, 0, 0, 0))
    for i, c in enumerate(cells):
        out.alpha_composite(c, (i * cell, 0))
    return out


def split_strip(img: Image.Image, n: int) -> list[Image.Image]:
    img = crop_op(img)
    cw = max(1, img.width // n)
    return [img.crop((i * cw, 0, img.width if i == n - 1 else (i + 1) * cw, img.height)) for i in range(n)]


def split_grid(img: Image.Image, cols: int, rows: int) -> list[list[Image.Image]]:
    img = crop_op(img)
    cw = max(1, img.width // cols)
    rh = max(1, img.height // rows)
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            x0, y0 = c * cw, r * rh
            x1 = img.width if c == cols - 1 else (c + 1) * cw
            y1 = img.height if r == rows - 1 else (r + 1) * rh
            cell = img.crop((x0, y0, x1, y1))
            # drop treadmill platform: keep upper ~85% if bottom is dark bar
            cb = opaque_bbox(cell)
            if cb:
                cell = cell.crop(cb)
                # trim bottom 12% (wheels/platform)
                trim = max(1, int(cell.height * 0.12))
                if cell.height > trim + 4:
                    cell = cell.crop((0, 0, cell.width, cell.height - trim))
            row.append(cell)
        grid.append(row)
    return grid


def synth_bob(base: Image.Image, n: int = 6) -> list[Image.Image]:
    frames = []
    for i in range(n):
        dy = (0, 1, 0, -1, 0, 1)[i % 6]
        c = Image.new("RGBA", (base.width, base.height + 2), (0, 0, 0, 0))
        c.alpha_composite(base, (0, 1 + dy))
        frames.append(c)
    return frames


def import_player() -> None:
    print("player")
    src = chroma(Image.open(SRC / "farm_player_walk_sheet.png"))
    frames = split_strip(src, 6)
    save(sheet_from_frames(frames, H_HUMAN, 46, 40), "player.png")
    shutil.copy2(SRC / "farm_player_walk_sheet.png", RAW / "farm_player_walk_sheet.png")


def import_npcs() -> None:
    print("npcs")
    src = chroma(Image.open(SRC / "farm_npcs_lineup.png"))
    frames = split_strip(src, 5)
    names = ["npc_ahe", "npc_xiaoman", "npc_qingyu", "npc_linshen", "npc_zhou"]
    for name, fr in zip(names, frames):
        bob = synth_bob(crop_op(fr), 6)
        save(sheet_from_frames(bob, H_HUMAN, 46, 40), f"{name}.png")
    shutil.copy2(SRC / "farm_npcs_lineup.png", RAW / "farm_npcs_lineup.png")


def import_animals() -> None:
    print("animals")
    path = SRC / "farm_animals_walk_cycles.png"
    src = chroma(Image.open(path))
    grid = split_grid(src, 6, 3)
    specs = [
        ("chicken", 20, 12, 14),   # cell, target_h, max_w — ~1/4 human
        ("sheep", 28, 20, 26),
        ("cow", 36, 24, 40),
    ]
    for row_i, (name, cell, th, mw) in enumerate(specs):
        frames = grid[row_i] if row_i < len(grid) else []
        if not frames:
            print(f"  WARN empty {name}")
            continue
        save(sheet_from_frames(frames, cell, th, mw), f"{name}.png")
    shutil.copy2(path, RAW / "farm_animals_walk_cycles.png")


def import_world() -> None:
    print("world")
    src = chroma(Image.open(SRC / "farm_world_props.png"))
    # Layout: row0 tiles(6), row1 rock+trees+house, row2 props
    box = opaque_bbox(src)
    if not box:
        print("  FAIL empty")
        return
    full = src.crop(box)
    # Split into 3 vertical bands by height thirds
    h = full.height
    bands = [
        full.crop((0, 0, full.width, h // 3)),
        full.crop((0, h // 3, full.width, 2 * h // 3)),
        full.crop((0, 2 * h // 3, full.width, h)),
    ]
    # tiles
    tile_names = ["tile_grass", "tile_dirt", "tile_tilled", "tile_watered", "tile_water", "tile_path"]
    tiles = split_strip(bands[0], 6)
    for name, t in zip(tile_names, tiles):
        t = crop_op(t).resize((TILE, TILE), Image.Resampling.NEAREST)
        save(t, f"{name}.png")
    # mid band: rock, tree, tree, house — 4 parts
    mid = split_strip(bands[1], 4)
    if mid:
        save(crop_op(mid[0]).resize((TILE, TILE), Image.Resampling.NEAREST), "tile_hill.png")
        save(crop_op(mid[0]).resize((TILE, TILE), Image.Resampling.NEAREST), "tile_farmland.png")
    for i, idx in enumerate([1, 2, 1]):
        if idx < len(mid):
            tr = crop_op(mid[idx])
            th = 80
            scale = th / max(1, tr.height)
            tw = max(1, int(tr.width * scale))
            save(tr.resize((tw, th), Image.Resampling.NEAREST), f"tree_{i}.png")
    if len(mid) >= 4:
        house = crop_op(mid[3])
        hh = 64
        scale = hh / max(1, house.height)
        hw = max(1, int(house.width * scale))
        save(house.resize((hw, hh), Image.Resampling.NEAREST), "house.png")
    # bottom props
    bot = split_strip(bands[2], 6)
    if bot:
        save(fit_cell(bot[0], 24, 18, 22), "chest.png")
    for i in range(4):
        if i + 1 < len(bot):
            save(crop_op(bot[i + 1]).resize((16, 16), Image.Resampling.NEAREST), f"flower_{i}.png")
    if len(bot) >= 6:
        bush = crop_op(bot[5])
        bh = 28
        scale = bh / max(1, bush.height)
        bw = max(1, int(bush.width * scale))
        save(bush.resize((bw, bh), Image.Resampling.NEAREST), "bush.png")
    shutil.copy2(SRC / "farm_world_props.png", RAW / "farm_world_props.png")


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    import_player()
    import_npcs()
    import_animals()
    import_world()
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
