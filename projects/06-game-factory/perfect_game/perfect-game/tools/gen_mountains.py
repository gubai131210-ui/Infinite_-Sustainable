"""Generate distant mountain / hill ridge sprites for Oakhaven north skyline."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "assets" / "processed"


def mountain_ridge(w: int = 128, h: int = 48) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Far cool ridge
    peaks = [(0, h), (18, 22), (36, 28), (54, 12), (78, 24), (98, 10), (118, 26), (w - 1, h)]
    d.polygon(peaks, fill=(72, 98, 118, 255))
    # Mid warmer ridge
    mid = [(0, h), (12, 34), (30, 26), (48, 32), (70, 18), (92, 30), (110, 22), (w - 1, h)]
    d.polygon(mid, fill=(86, 120, 92, 255))
    # Near dark green foothills
    near = [(0, h), (10, 40), (28, 36), (50, 38), (74, 32), (100, 38), (120, 36), (w - 1, h)]
    d.polygon(near, fill=(58, 96, 62, 255))
    # Soft snow caps
    for x0, y0 in [(54, 12), (98, 10), (70, 18)]:
        d.polygon([(x0 - 6, y0 + 8), (x0, y0), (x0 + 6, y0 + 8)], fill=(230, 235, 240, 200))
    return img


def hill_chunk(w: int = 64, h: int = 32) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(0, h), (8, 18), (22, 10), (40, 16), (56, 8), (w - 1, h)], fill=(70, 110, 74, 255))
    d.polygon([(0, h), (14, 24), (34, 20), (52, 24), (w - 1, h)], fill=(50, 88, 56, 255))
    return img


def main() -> None:
    mountain_ridge().save(OUT / "prop_mountains.png")
    hill_chunk().save(OUT / "prop_hills.png")
    print("OK prop_mountains.png prop_hills.png")


if __name__ == "__main__":
    main()
