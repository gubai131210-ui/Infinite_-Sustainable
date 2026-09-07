#!/usr/bin/env python3
"""P145 — mid-valley oil-pixel deciduous canopy strips (overview mass without 1k sprites)."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"
WORLD_W = 192 * 16
rng = random.Random(145)


def meadow_canopy() -> None:
    """Soft layered leaf masses for mid-map — cool far / warm near, plaza cutout."""
    w, h = WORLD_W, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def in_plaza(x: int) -> bool:
        # Town plaza / storefront band (tile ~70–114 → px 1120–1824)
        return 1080 <= x <= 1880

    # Far cool haze blobs
    for x in range(0, w, 28):
        if in_plaza(x):
            continue
        cx = x + 14
        cy = 18 + (x // 60) % 8
        d.ellipse((cx - 50, cy - 14, cx + 54, cy + 22), fill=(70, 120, 78, 140))
        d.ellipse((cx - 32, cy - 24, cx + 34, cy + 8), fill=(78, 130, 86, 150))

    # Mid olive masses
    for x in range(0, w, 18):
        if in_plaza(x):
            continue
        cx = x + 10 + (x % 5)
        cy = 36 + (x // 40) % 10
        d.ellipse((cx - 46, cy - 16, cx + 50, cy + 28), fill=(40, 95, 52, 210))
        d.ellipse((cx - 30, cy - 30, cx + 32, cy + 6), fill=(48, 108, 60, 220))
        d.ellipse((cx - 24, cy + 10, cx + 26, cy + 24), fill=(22, 55, 30, 100))

    # Near dark clumps + moss highlights
    for x in range(0, w, 14):
        if in_plaza(x):
            continue
        cx = x + 8
        cy = 52 + (x * 3) % 12
        d.ellipse((cx - 38, cy - 12, cx + 42, cy + 30), fill=(24, 68, 36, 240))
        d.ellipse((cx - 20, cy - 26, cx + 24, cy + 4), fill=(32, 80, 44, 245))
        for _ in range(4):
            sx = cx + rng.randint(-18, 18)
            sy = cy + rng.randint(-8, 14)
            d.ellipse((sx - 2, sy - 2, sx + 3, sy + 2), fill=(70, 140, 70, 170))

    # Soft rounded crowns (not pine spikes)
    for x in range(10, w - 10, 16):
        if in_plaza(x):
            continue
        base = h - 6
        cy = base - (22 + (x * 7) % 16)
        half = 14 + (x % 8)
        d.ellipse((x - half, cy - 12, x + half, base), fill=(18, 58, 28, 250))
        d.ellipse((x - half + 4, cy - 18, x + half - 4, cy + 4), fill=(36, 92, 48, 235))
        # warm lit rim
        d.ellipse((x - 6, cy - 16, x + 8, cy - 4), fill=(90, 150, 70, 120))

    # Thin river corridor gap (west) so water reads
    for x in range(280, 520):
        for y in range(h):
            img.putpixel((x, y), (0, 0, 0, 0))

    img.save(PROC / "prop_meadow_canopy.png")
    print("OK prop_meadow_canopy", w, h)


if __name__ == "__main__":
    meadow_canopy()
