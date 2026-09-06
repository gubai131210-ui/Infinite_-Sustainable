"""P56: organic north ridge strip (sky gaps, uneven pines silhouettes)."""
from __future__ import annotations

from pathlib import Path
import math

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"


def ridge() -> None:
    w, h = 320, 64
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Sky wash behind ridge
    for y in range(0, 28):
        t = y / 27.0
        d.line([(0, y), (w - 1, y)], fill=(100 + int(40 * t), 160 + int(30 * t), 230, 220))
    # Organic ridge top via sine sum
    pts = []
    for x in range(w):
        y = 28 + int(10 * math.sin(x * 0.04) + 6 * math.sin(x * 0.11 + 1.2) + 4 * math.sin(x * 0.23))
        # Gaps (waterfall-ish windows)
        if 55 <= x <= 95 or 170 <= x <= 210:
            y = 48 + int(3 * math.sin(x * 0.2))
        pts.append((x, y))
    # Fill ridge body
    for x, ytop in pts:
        for y in range(ytop, h):
            shade = 70 + (y - ytop) * 2
            green = 90 + (y % 5)
            img.putpixel((x, y), (55, min(140, green + shade // 3), 70, 255))
    # Sparse pine silhouettes on ridge
    for i, x0 in enumerate(range(8, w - 8, 28)):
        if 55 <= x0 <= 95 or 170 <= x0 <= 210:
            continue
        y0 = pts[x0][1] - 10 - (i % 3) * 2
        d.polygon([(x0, y0 + 14), (x0 + 4, y0), (x0 + 8, y0 + 14)], fill=(30, 70, 40, 255))
        d.rectangle((x0 + 3, y0 + 12, x0 + 5, y0 + 18), fill=(60, 40, 25, 255))
    # Soft clouds above
    for cx, cy in [(30, 8), (120, 6), (200, 10), (270, 7)]:
        d.ellipse((cx, cy, cx + 36, cy + 14), fill=(250, 252, 255, 230))
        d.ellipse((cx + 10, cy - 4, cx + 40, cy + 10), fill=(255, 255, 255, 240))
    img.save(PROC / "prop_ridge_organic.png")
    print("OK prop_ridge_organic.png", w, h)


def main() -> None:
    ridge()


if __name__ == "__main__":
    main()
