"""Cutout pipeline for Farm_Demo — magenta key (+ optional rembg) + QA.

Prefer tools/gen_pixel_assets.py which already keys + writes processed/qa.
This script re-processes assets/raw/* for any AI-imported sprites.
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets" / "raw"
OUT = ROOT / "assets" / "processed"
QA = ROOT / "assets" / "qa"
REMBG_HOME = ROOT / "tools" / "rembg_models"

os.environ.setdefault("U2NET_HOME", str(REMBG_HOME))
os.environ.setdefault("REMBG_HOME", str(REMBG_HOME))
os.environ.setdefault("XDG_DATA_HOME", str(REMBG_HOME))

from PIL import Image

# Re-key all raw sprites (magenta backdrop). Tiles/trees use green pixels — do NOT green-key.
JOBS = sorted(p.name for p in RAW.glob("*.png"))


def chroma_magenta(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if r > 200 and b > 200 and g < 80:
                px[x, y] = (0, 0, 0, 0)
            elif r > 180 and b > 180 and g < r - 40 and g < b - 40:
                px[x, y] = (0, 0, 0, 0)
    return rgba


def scrub(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if a == 0:
                px[x, y] = (0, 0, 0, 0)
            elif r > 180 and b > 180 and g < 100:
                gray = int(0.3 * r + 0.4 * g + 0.3 * b)
                px[x, y] = (gray, gray, gray, a)
    return rgba


def checkerboard(size: tuple[int, int], cell: int = 8) -> Image.Image:
    w, h = size
    board = Image.new("RGBA", (w, h))
    px = board.load()
    c1, c2 = (220, 220, 220, 255), (160, 160, 160, 255)
    for y in range(h):
        for x in range(w):
            px[x, y] = c1 if (x // cell + y // cell) % 2 == 0 else c2
    return board


def maybe_rembg(img: Image.Image) -> Image.Image:
    if os.environ.get("USE_REMBG") != "1":
        return img
    from rembg import remove, new_session

    model = os.environ.get("REMBG_MODEL", "u2net")
    session = new_session(model)
    rgb = Image.new("RGB", img.size, (255, 0, 255))
    rgb.paste(img.convert("RGB"), mask=img.split()[-1])
    return remove(rgb, session=session).convert("RGBA")


def process_one(name: str) -> None:
    src = RAW / name
    img = Image.open(src).convert("RGBA")
    out = scrub(chroma_magenta(maybe_rembg(chroma_magenta(img))))
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    out.save(OUT / name)
    board = checkerboard(out.size)
    board.alpha_composite(out)
    board.convert("RGB").save(QA / f"checker_{name}", quality=92)
    print(f"OK {name} -> {out.size}")


def main() -> int:
    if not JOBS:
        print("No raw PNGs")
        return 1
    for name in JOBS:
        process_one(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
