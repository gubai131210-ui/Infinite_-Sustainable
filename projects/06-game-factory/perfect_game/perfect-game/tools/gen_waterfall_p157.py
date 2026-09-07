#!/usr/bin/env python3
"""P157 — Stardew-leaning multi-tier waterfall bowl (organic cliffs, foam, mist)."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"
rng = random.Random(157)


def _noise(x: int, y: int) -> float:
    return ((x * 73856093) ^ (y * 19349663) ^ 83492791) % 1000 / 1000.0


def waterfall_bowl() -> None:
    w, h = 256, 320
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    mid = w // 2

    rock_dark = (58, 52, 48, 255)
    rock_mid = (78, 70, 62, 255)
    rock_lit = (102, 92, 80, 255)
    moss = (48, 86, 52, 255)
    moss2 = (62, 108, 64, 255)

    # Fill amphitheater throat with water blue first (no black void between streams)
    for y in range(12, h - 60):
        flare = 26 + int(y * 0.11) + int(3 * math.sin(y * 0.08))
        for x in range(mid - flare - 6, mid + flare + 7):
            dx = abs(x - mid) / float(flare + 6)
            if dx > 1.0:
                continue
            shimmer = int(14 * math.sin(x * 0.55 + y * 0.4))
            depth = int(20 * dx)
            px[x, y] = (
                max(40, 70 + shimmer - depth),
                max(80, 130 + shimmer // 2 - depth // 2),
                max(140, 200 + shimmer // 3),
                255,
            )

    # Amphitheater cliff walls — ONLY outside water throat
    for y in range(8, h - 56):
        flare = 28 + int(y * 0.12) + int(4 * math.sin(y * 0.09))
        left_inner = mid - flare - 8
        right_inner = mid + flare + 8
        left_outer = left_inner - 44 - int(5 * math.sin(y * 0.07 + 0.4))
        right_outer = right_inner + 44 + int(5 * math.sin(y * 0.07 + 1.1))
        for x in range(w):
            in_left = left_outer <= x <= left_inner
            in_right = right_inner <= x <= right_outer
            if not (in_left or in_right):
                continue
            n = _noise(x, y * 3)
            band = (y // 7) % 3
            if n < 0.18:
                c = moss if (x + y) % 5 else moss2
            elif band == 0:
                c = rock_dark
            elif band == 1:
                c = rock_mid
            else:
                c = rock_lit
            # darken toward water lip
            if abs(x - left_inner) <= 3 or abs(x - right_inner) <= 3:
                c = (max(20, c[0] - 18), max(20, c[1] - 16), max(18, c[2] - 14), 255)
            if n > 0.88:
                c = (min(140, c[0] + 22), min(130, c[1] + 18), min(110, c[2] + 14), 255)
            px[x, y] = c

    # Tier shelves with pools
    shelves = [(70, 38, 10), (120, 48, 12), (170, 56, 14)]
    d = ImageDraw.Draw(img)
    for sy, rw, rh in shelves:
        # rock lip
        d.ellipse([mid - rw - 6, sy - 4, mid + rw + 6, sy + 6], fill=(70, 64, 56, 255))
        for x in range(mid - rw - 4, mid + rw + 5):
            for y in range(sy - 2, sy + 5):
                if 0 <= x < w and 0 <= y < h and _noise(x, y) > 0.35:
                    px[x, y] = moss if _noise(x + 3, y) < 0.4 else rock_mid
        # pool water
        for y in range(sy, sy + rh):
            for x in range(mid - rw, mid + rw + 1):
                dx = (x - mid) / float(rw)
                dy = (y - sy) / float(max(rh, 1))
                if dx * dx + (dy - 0.35) ** 2 > 1.05:
                    continue
                shimmer = int(18 * math.sin(x * 0.7 + y * 0.9))
                px[x, y] = (
                    95 + shimmer,
                    155 + shimmer // 2,
                    210 + shimmer // 3,
                    230,
                )

    # Cascading streams (irregular widths, not solid stripes)
    streams = []
    x = mid - 34
    while x < mid + 36:
        streams.append(x)
        x += 5 + rng.randint(0, 4)
    for i, sx in enumerate(streams):
        wob_amp = 2.2 + (i % 3) * 0.4
        width = 2 + (i % 3)
        top = 28 + (i % 5)
        for y in range(top, h - 68):
            # skip through shelf pools (already drawn)
            wob = int(wob_amp * math.sin(y * 0.11 + i * 0.7))
            for dx in range(-width, width + 1):
                xx = sx + wob + dx
                if not (0 <= xx < w):
                    continue
                # brighter core
                t = abs(dx) / float(width + 1)
                if t < 0.35:
                    c = (210, 235, 255, 235)
                elif t < 0.7:
                    c = (150, 200, 240, 210)
                else:
                    c = (110, 170, 220, 160)
                # foam flecks
                if _noise(xx, y) > 0.92:
                    c = (240, 250, 255, 220)
                # don't obliterate cliff completely outside throat
                if abs(xx - mid) > 52 and _noise(xx + 1, y) < 0.4:
                    continue
                px[xx, y] = c

    # Base foam bowl
    for y in range(h - 72, h - 8):
        for x in range(36, w - 36):
            dx = (x - mid) / 78.0
            dy = (y - (h - 40)) / 30.0
            if dx * dx + dy * dy > 1.0:
                continue
            foam = 200 + int(40 * _noise(x, y))
            a = 240 if dy < 0.2 else 170
            # mix water blue under foam
            if dy > 0.45 and _noise(x + 2, y) < 0.45:
                px[x, y] = (120, 180, 230, 200)
            else:
                px[x, y] = (min(255, foam), min(255, foam + 8), 255, a)

    # Mist dots
    for _ in range(90):
        x = rng.randint(mid - 50, mid + 50)
        y = rng.randint(50, h - 80)
        r = rng.randint(1, 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(220, 240, 255, rng.randint(90, 160)))

    # Soft blur on foam only
    foam_band = img.crop((30, h - 78, w - 30, h - 6)).filter(ImageFilter.GaussianBlur(0.8))
    img.paste(foam_band, (30, h - 78), foam_band)

    # Kill any leftover opaque black (safety)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and r < 8 and g < 8 and b < 8:
                px[x, y] = (0, 0, 0, 0)

    out = PROC / "prop_waterfall_bowl.png"
    img.save(out)
    print("OK prop_waterfall_bowl", img.size)


if __name__ == "__main__":
    waterfall_bowl()
