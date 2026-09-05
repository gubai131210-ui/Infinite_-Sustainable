"""Cutout pipeline: chroma-green key + checkerboard QA (fast path).

Optional: set USE_REMBG=1 to also run rembg (downloads large models).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets" / "raw"
OUT = ROOT / "assets" / "processed"
QA = ROOT / "assets" / "qa"

JOBS = [
    ("bg_far_dusk_mountains.png", "bg_far.png", False),
    ("bg_mid_cabin_yard.png", "bg_mid.png", True),
    ("fg_props_trees_fence.png", "fg_props.png", True),
    ("player_traveler_side.png", "player.png", True),
]


def chroma_key(img: Image.Image, threshold: int = 55) -> Image.Image:
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if g > 85 and g >= r + threshold and g >= b + threshold:
                pixels[x, y] = (0, 0, 0, 0)
            elif a < 32:
                pixels[x, y] = (0, 0, 0, 0)
            elif a < 200:
                # hard-ish edge for game composite (reduce halo)
                pixels[x, y] = (r, g, b, 255 if a >= 128 else 0)
    return rgba


def checkerboard(size: tuple[int, int], cell: int = 16) -> Image.Image:
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

    session = new_session("u2net")
    rgb = Image.new("RGB", img.size, (0, 255, 0))
    rgb.paste(img.convert("RGB"), mask=img.split()[-1])
    return remove(rgb, session=session).convert("RGBA")


def process_one(src_name: str, dst_name: str, use_chroma: bool) -> None:
    src = RAW / src_name
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert("RGBA")

    if dst_name == "bg_far.png":
        out = img
    else:
        out = chroma_key(img) if use_chroma else img
        out = maybe_rembg(out)
        if use_chroma:
            out = chroma_key(out, threshold=50)

    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    out_path = OUT / dst_name
    out.save(out_path)

    board = checkerboard(out.size)
    board.alpha_composite(out)
    qa_path = QA / f"checker_{dst_name}"
    board.convert("RGB").save(qa_path, quality=92)
    # crude QA: count non-near-green opaque pixels ratio
    print(f"OK {src_name} -> {out_path.name} qa={qa_path.name} size={out.size}")


def main() -> int:
    for job in JOBS:
        process_one(*job)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
