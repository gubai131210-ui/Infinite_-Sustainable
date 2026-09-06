"""Nested cliff-bowl waterfall — reads as fall into river, not floating cylinder."""
from __future__ import annotations

from pathlib import Path
import random

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "processed"
rng = random.Random(11)


def main() -> None:
    w, h = 72, 88
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Cliff ledge top
    d.rectangle((6, 0, 66, 14), fill=(92, 82, 68, 255))
    d.rectangle((8, 2, 64, 8), fill=(78, 128, 58, 255))
    # Side rock jaws
    d.polygon([(4, 10), (18, 12), (16, 50), (2, 48)], fill=(86, 76, 62, 255))
    d.polygon([(54, 12), (68, 10), (70, 48), (56, 50)], fill=(86, 76, 62, 255))
    # Main fall (taper toward pool)
    for y in range(12, 68):
        t = (y - 12) / 56.0
        half = int(10 + t * 6)
        cx = 36
        col = (70 + int(t * 20), 150 + int(t * 10), 210, 235)
        d.rectangle((cx - half, y, cx + half, y + 1), fill=col)
        if y % 3 == 0:
            d.line((cx - half + 2, y, cx + half - 2, y), fill=(200, 230, 250, 180))
    # Foam lip
    d.ellipse((20, 10, 52, 20), fill=(235, 245, 255, 230))
    # Pool splash
    d.ellipse((14, 64, 58, 84), fill=(80, 150, 205, 210))
    for _ in range(24):
        x = rng.randint(18, 54)
        y = rng.randint(66, 82)
        d.point((x, y), fill=(230, 245, 255, 255))
    path = OUT / "prop_waterfall.png"
    img.save(path)
    print("OK", path, img.size)


if __name__ == "__main__":
    main()
