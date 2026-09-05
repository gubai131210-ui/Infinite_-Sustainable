"""Cutout pipeline: chroma key (+ optional rembg) + checkerboard QA + fringe scrub.

Models live on D: under tools/rembg_models/ (NOT user profile / C:).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets" / "raw"
OUT = ROOT / "assets" / "processed"
QA = ROOT / "assets" / "qa"
REMBG_HOME = ROOT / "tools" / "rembg_models"

# Force rembg/pooch off C: before importing rembg
os.environ.setdefault("U2NET_HOME", str(REMBG_HOME))
os.environ.setdefault("REMBG_HOME", str(REMBG_HOME))
# Some builds also honor XDG_DATA_HOME for ~/.rembg layout
os.environ.setdefault("XDG_DATA_HOME", str(REMBG_HOME))

from PIL import Image

JOBS = [
    ("bg_far_dusk_mountains.png", "bg_far.png", False),
    ("bg_mid_cabin_yard.png", "bg_mid.png", True),
    ("fg_props_trees_fence.png", "fg_props.png", True),
    ("player_traveler_side.png", "player.png", True),
]


def chroma_key(img: Image.Image, threshold: int = 45) -> Image.Image:
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # strong green-screen key
            if g > 70 and g >= r + threshold and g >= b + threshold:
                pixels[x, y] = (0, 0, 0, 0)
            elif g > 140 and r < 120 and b < 120 and g > r and g > b:
                pixels[x, y] = (0, 0, 0, 0)
            elif a < 40:
                pixels[x, y] = (0, 0, 0, 0)
            elif a < 210:
                pixels[x, y] = (r, g, b, 255 if a >= 140 else 0)
    return rgba


def scrub_fringe(img: Image.Image) -> Image.Image:
    """Zero RGB on transparent pixels; pull green fringe toward neighbor opaque."""
    rgba = img.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    # pass 1: clear RGB where transparent
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                px[x, y] = (0, 0, 0, 0)
            elif a > 0 and g > r + 25 and g > b + 25 and g > 100:
                # desaturate leftover green fringe
                gray = int(0.3 * r + 0.4 * g + 0.3 * b)
                px[x, y] = (gray, gray, min(gray, b), a)
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

    model = os.environ.get("REMBG_MODEL", "u2net")
    session = new_session(model)
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
            out = chroma_key(out, threshold=40)
        out = scrub_fringe(out)

    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    out_path = OUT / dst_name
    out.save(out_path)

    board = checkerboard(out.size)
    board.alpha_composite(out)
    qa_path = QA / f"checker_{dst_name}"
    board.convert("RGB").save(qa_path, quality=92)
    print(f"OK {src_name} -> {out_path.name} qa={qa_path.name} size={out.size}")


def main() -> int:
    print(f"USE_REMBG={os.environ.get('USE_REMBG', '0')} model={os.environ.get('REMBG_MODEL', 'u2net')}")
    for job in JOBS:
        process_one(*job)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
