#!/usr/bin/env python3
"""P161 — break rigid horizontal canopy bands; irregular pine + meadow lobes."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"
WORLD_W = 192 * 16
rng = random.Random(161)


def _clear_rect(img: Image.Image, x0: int, x1: int, soft: int = 24) -> None:
    px = img.load()
    h = img.height
    for x in range(max(0, x0 - soft), min(img.width, x1 + soft)):
        edge = min(abs(x - x0), abs(x - x1), soft)
        fade = 1.0 if x0 <= x <= x1 else edge / float(soft)
        for y in range(h):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, int(a * (1.0 - 0.97 * fade)))


def pine_canopy() -> None:
    """Cluster masses with corridor gaps — not a continuous stripe wall."""
    w, h = WORLD_W, 140
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def blocked(x: int) -> bool:
        if 250 <= x <= 560:  # waterfall
            return True
        if 2080 <= x <= 2940:  # station
            return True
        if 980 <= x <= 1180:  # ruins approach corridor
            return True
        return False

    # Seed irregular cluster centers (lobes), skip corridors
    centers: list[tuple[int, int, int]] = []
    x = 40
    while x < w - 40:
        if blocked(x):
            x += 80
            continue
        gap = 70 + rng.randint(0, 110)
        cy = 28 + rng.randint(0, 36)
        rad = 55 + rng.randint(0, 45)
        centers.append((x, cy, rad))
        x += gap

    for cx, cy, rad in centers:
        for _ in range(5):
            ox = rng.randint(-rad // 2, rad // 2)
            oy = rng.randint(-18, 22)
            rx = rad // 2 + rng.randint(-8, 18)
            ry = 18 + rng.randint(0, 16)
            col = (28 + rng.randint(0, 20), 70 + rng.randint(0, 30), 40 + rng.randint(0, 20), 180 + rng.randint(0, 50))
            d.ellipse((cx + ox - rx, cy + oy - ry, cx + ox + rx, cy + oy + ry), fill=col)
        # Darker near crowns
        d.ellipse((cx - rad // 3, cy - 10, cx + rad // 3, cy + 28), fill=(14, 42, 24, 240))
        # Pine tip scallops along lobe bottom
        base = min(h - 4, cy + 48 + rng.randint(0, 20))
        for tx in range(cx - rad + 8, cx + rad - 8, 10):
            tip = base - (30 + (tx * 11) % 24)
            half = 6 + (tx % 5)
            d.polygon([(tx, tip), (tx - half, base), (tx + half, base)], fill=(10, 36, 20, 255))

    # Soft secondary haze above (not a solid bar)
    for cx, cy, rad in centers[::2]:
        d.ellipse((cx - rad, cy - 28, cx + rad, cy + 8), fill=(55, 95, 72, 90))

    _clear_rect(img, 250, 560, 28)
    _clear_rect(img, 2080, 2940, 32)
    _clear_rect(img, 980, 1180, 20)
    img.save(PROC / "prop_pine_canopy.png")
    print("OK prop_pine_canopy", w, h, "clusters", len(centers))


def meadow_canopy() -> None:
    """Lobed deciduous mass — plaza + path corridors open; scalloped south edge."""
    w, h = WORLD_W, 110
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def blocked(x: int) -> bool:
        if 1080 <= x <= 1880:  # plaza
            return True
        if 280 <= x <= 520:  # river corridor
            return True
        return False

    centers: list[tuple[int, int, int]] = []
    x = 60
    while x < w - 60:
        if blocked(x):
            x += 90
            continue
        gap = 90 + rng.randint(0, 130)
        cy = 36 + rng.randint(0, 28)
        rad = 60 + rng.randint(0, 50)
        centers.append((x, cy, rad))
        x += gap

    for cx, cy, rad in centers:
        cool = (70, 120, 78, 130)
        mid = (42, 98, 54, 200)
        near = (24, 70, 38, 235)
        d.ellipse((cx - rad, cy - 20, cx + rad, cy + 26), fill=cool)
        d.ellipse((cx - rad // 2 - 10, cy - 8, cx + rad // 2 + 10, cy + 36), fill=mid)
        d.ellipse((cx - rad // 3, cy + 6, cx + rad // 3, cy + 44), fill=near)
        for _ in range(6):
            sx = cx + rng.randint(-rad // 2, rad // 2)
            sy = cy + rng.randint(-6, 30)
            d.ellipse((sx - 16, sy - 10, sx + 18, sy + 14), fill=(36, 92, 48, 180))
            d.ellipse((sx - 6, sy - 14, sx + 8, sy - 2), fill=(90, 150, 70, 100))

    _clear_rect(img, 1080, 1880, 36)
    _clear_rect(img, 280, 520, 22)
    # Soft farm→town path window (approx tiles 48–90 → px 768–1440) mid band only
    px = img.load()
    for x in range(760, 1500):
        for y in range(70, h):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, int(a * 0.35))
    img.save(PROC / "prop_meadow_canopy.png")
    print("OK prop_meadow_canopy", w, h, "clusters", len(centers))


if __name__ == "__main__":
    pine_canopy()
    meadow_canopy()
