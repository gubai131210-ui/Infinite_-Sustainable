#!/usr/bin/env python3
"""P109–P111 — ref-aligned canopy / waterfall / storefront depth (oil-pixel feel)."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"
WORLD_W = 192 * 16
rng = random.Random(109)


def blit_text(img: Image.Image, x: int, y: int, text: str, color) -> None:
    font = {
        "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
        "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
        "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
        "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
        "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
        "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
        "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
        "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
        "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
        "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
        "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
        "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
        "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
        "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
        "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
        "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
        " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
        "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    }
    for ch in text:
        rows = font.get(ch, font[" "])
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "1" and 0 <= x + c < img.width and 0 <= y + r < img.height:
                    img.putpixel((x + c, y + r), color)
        x += 6


def pine_canopy() -> None:
    """Layered oil-pixel forest mass — cool far / warm near, soft underside."""
    w, h = WORLD_W, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def in_wf(x: int) -> bool:
        return 260 <= x <= 540

    # Far cool haze band
    for x in range(0, w, 22):
        if in_wf(x):
            continue
        cx, cy = x + 18, 22 + (x // 55) % 6
        d.ellipse((cx - 44, cy - 16, cx + 48, cy + 20), fill=(55, 95, 72, 160))
        d.ellipse((cx - 28, cy - 26, cx + 30, cy + 6), fill=(62, 108, 80, 170))

    # Mid olive mass
    for x in range(0, w, 16):
        if in_wf(x):
            continue
        cx = x + 12 + (x % 7)
        cy = 42 + (x // 28) % 12
        d.ellipse((cx - 48, cy - 18, cx + 52, cy + 30), fill=(28, 72, 42, 220))
        d.ellipse((cx - 32, cy - 34, cx + 34, cy + 8), fill=(36, 88, 52, 230))
        d.ellipse((cx - 26, cy + 12, cx + 28, cy + 28), fill=(14, 38, 24, 110))

    # Near dark clumps with moss highlights
    for x in range(0, w, 12):
        if in_wf(x):
            continue
        cx = x + 8
        cy = 58 + (x * 3) % 14
        d.ellipse((cx - 40, cy - 14, cx + 44, cy + 32), fill=(16, 48, 28, 245))
        d.ellipse((cx - 22, cy - 28, cx + 26, cy + 6), fill=(22, 58, 34, 250))
        # moss speckles
        for _ in range(5):
            sx = cx + rng.randint(-20, 20)
            sy = cy + rng.randint(-10, 16)
            d.ellipse((sx - 2, sy - 2, sx + 3, sy + 2), fill=(48, 110, 55, 180))

    # Jagged near tips
    for x in range(6, w - 6, 9):
        if in_wf(x):
            continue
        base = h - 4
        tip = base - (38 + (x * 11) % 22)
        half = 7 + (x % 6)
        d.polygon([(x, tip), (x - half, base), (x + half, base)], fill=(12, 40, 22, 255))
        d.polygon(
            [(x, tip + 6), (x - half + 2, base - 3), (x + half - 2, base - 3)],
            fill=(32, 78, 44, 240),
        )

    # Amphitheater flanks denser
    for cx in (230, 560):
        d.ellipse((cx - 58, 36, cx + 58, 110), fill=(10, 36, 22, 250))
        d.ellipse((cx - 36, 16, cx + 40, 72), fill=(20, 54, 32, 255))
        for i in range(8):
            px = cx - 30 + i * 8
            tip = 48 + (i % 3) * 4
            d.polygon([(px, tip), (px - 6, 100), (px + 6, 100)], fill=(14, 42, 24, 255))

    img.save(PROC / "prop_pine_canopy.png")
    print("OK prop_pine_canopy", w, h)


def waterfall_bowl() -> None:
    """Taller amphitheater falls — cliff strata + multi-stream + foam bowl."""
    w, h = 176, 200
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Cliff rock body
    for y in range(0, h - 40):
        for x in range(w):
            # Amphitheater U-shape
            mid = w // 2
            flare = 18 + y // 5
            if abs(x - mid) > (w // 2 - 6 - max(0, 40 - y) // 2) and y < 50:
                continue
            if abs(x - mid) > flare + 40 and y > 50:
                # outer cliff walls only near sides
                if not (x < 28 or x > w - 28):
                    continue
            # sky notch for falls source
            if y < 22 and 58 < x < 118:
                continue
            n = (x * 17 + y * 13) & 15
            rr = 62 + n * 2 + y // 8
            gg = 60 + n + y // 10
            bb = 56 + n // 2
            if n % 5 == 0:
                rr, gg, bb = 48, 78, 42  # moss
            if n % 7 == 0:
                rr, gg, bb = 88, 82, 74  # lit rock
            # darken edges
            if x < 22 or x > w - 22:
                rr, gg, bb = rr - 18, gg - 16, bb - 14
            img.putpixel((x, y), (max(20, min(130, rr)), max(20, min(120, gg)), max(18, min(110, bb)), 255))

    # Terrace shelves
    for shelf_y in (28, 52, 78, 104):
        for x in range(24, w - 24):
            if abs(x - w // 2) > 55 - (shelf_y - 28) // 4:
                continue
            for dy in range(4):
                y = shelf_y + dy
                if 0 <= y < h:
                    c = (55 + dy * 4, 72 + dy, 48, 255) if dy < 2 else (70, 66, 58, 255)
                    img.putpixel((x, y), c)

    # Multi-stream falls
    for i, x0 in enumerate(range(62, 118, 4)):
        wob = int(3 * math.sin(i * 0.7))
        top = 20 + (i % 3)
        bot = h - 56
        d.rectangle((x0 + wob, top, x0 + 5 + wob, bot), fill=(150, 200, 240, 200))
        d.rectangle((x0 + 1 + wob, top + 2, x0 + 4 + wob, bot - 2), fill=(210, 235, 255, 230))
        # bright core
        if i % 2 == 0:
            d.line([(x0 + 2 + wob, top), (x0 + 2 + wob, bot)], fill=(240, 250, 255, 200))

    # Foam pool
    for y in range(h - 58, h - 8):
        for x in range(36, w - 36):
            dx = (x - w // 2) / 50.0
            dy = (y - (h - 34)) / 22.0
            if dx * dx + dy * dy > 1.0:
                continue
            foam = 200 + ((x * 3 + y * 5) % 40)
            a = 220 if dy < 0.3 else 180
            img.putpixel((x, y), (min(255, foam), min(255, foam + 10), 255, a))

    # Side spray
    for _ in range(40):
        x = rng.randint(48, w - 48)
        y = rng.randint(40, h - 60)
        d.ellipse((x - 1, y - 1, x + 2, y + 2), fill=(220, 240, 255, 140))

    # Soft blur on foam only — keep cliffs crisp
    foam_band = img.crop((30, h - 60, w - 30, h - 6)).filter(ImageFilter.GaussianBlur(0.6))
    img.paste(foam_band, (30, h - 60), foam_band)

    img.save(PROC / "prop_waterfall_bowl.png")
    print("OK prop_waterfall_bowl", w, h)


def facade(name, roof, awn_a, awn_b, sign_bg, wall, label) -> None:
    w, h = 176, 152
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Soft ground shadow
    d.ellipse((18, h - 18, w - 18, h - 2), fill=(30, 40, 28, 70))
    d.polygon([(6, 40), (88, 2), (170, 40)], fill=roof)
    shade = tuple(max(0, c - 40) for c in roof[:3]) + (255,)
    d.polygon([(6, 40), (170, 40), (160, 52), (16, 52)], fill=shade)
    for yy in range(14, 40, 3):
        d.line([(30, yy), (146, yy)], fill=shade)
    d.rectangle([(140, 12), (158, 42)], fill=(108, 98, 92, 255))
    d.ellipse([(142, 2), (160, 16)], fill=(230, 230, 235, 150))
    d.rectangle([(10, h - 22), (w - 10, h - 4)], fill=(128, 122, 114, 255))
    d.rectangle([(14, 52), (w - 14, h - 22)], fill=wall)
    d.rectangle([(14, 52), (w - 14, h - 22)], outline=(70, 50, 34, 255), width=2)
    # Right-side depth shade
    for yy in range(54, h - 24):
        for xx in range(w - 28, w - 14):
            img.putpixel((xx, yy), tuple(max(0, c - 28) for c in wall[:3]) + (255,))
    for bx in range(20, w - 20, 7):
        d.line(
            [(bx, 54), (bx, h - 24)],
            fill=(max(0, wall[0] - 22), max(0, wall[1] - 22), max(0, wall[2] - 22), 255),
        )
    for i, x0 in enumerate(range(18, 154, 12)):
        c = awn_a if i % 2 == 0 else awn_b
        d.rectangle([(x0, 54), (x0 + 11, 72)], fill=c)
        d.pieslice([(x0, 68), (x0 + 11, 82)], 0, 180, fill=c)
    tw = len(label) * 6 + 10
    sx = max(18, (w - tw) // 2)
    d.rectangle([(sx - 6, 78), (sx + tw + 6, 100)], fill=(80, 55, 34, 255))
    d.rectangle([(sx - 4, 80), (sx + tw + 4, 98)], fill=sign_bg)
    blit_text(img, sx, 84, label, (40, 28, 18, 255))
    for wx in (18, w - 44):
        d.rectangle([(wx, 104), (wx + 24, 122)], fill=(155, 200, 235, 255))
        d.line([(wx + 12, 104), (wx + 12, 122)], fill=(100, 145, 170, 255))
        d.rectangle([(wx - 1, 122), (wx + 25, 128)], fill=(55, 115, 48, 255))
    d.rectangle([(w // 2 - 8, h - 48), (w // 2 + 8, h - 22)], fill=(95, 60, 40, 255))
    d.rectangle([(w // 2 + 2, h - 40), (w // 2 + 4, h - 38)], fill=(220, 190, 100, 255))
    img.save(PROC / name)
    print("OK", name, label)


def bakery() -> None:
    w, h = 148, 132
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((16, h - 16, w - 16, h - 2), fill=(30, 40, 28, 70))
    d.polygon([(8, 36), (74, 2), (140, 36)], fill=(150, 62, 48, 255))
    d.polygon([(8, 36), (140, 36), (132, 46), (16, 46)], fill=(110, 42, 32, 255))
    d.rectangle([(12, 46), (w - 12, h - 6)], fill=(228, 210, 185, 255))
    d.rectangle([(12, 46), (w - 12, h - 6)], outline=(72, 52, 36, 255), width=2)
    for yy in range(48, h - 8):
        for xx in range(w - 26, w - 12):
            img.putpixel((xx, yy), (200, 185, 160, 255))
    d.rectangle([(10, h - 16), (w - 10, h - 4)], fill=(125, 118, 110, 255))
    for i, x0 in enumerate(range(16, 128, 10)):
        c = (210, 60, 55, 255) if i % 2 == 0 else (245, 245, 245, 255)
        d.rectangle([(x0, 48), (x0 + 9, 62)], fill=c)
        d.pieslice([(x0, 58), (x0 + 9, 70)], 0, 180, fill=c)
    d.rectangle([(34, 72), (114, 98)], fill=(85, 58, 36, 255))
    d.rectangle([(38, 76), (110, 94)], fill=(245, 220, 150, 255))
    blit_text(img, 52, 80, "BAKERY", (70, 40, 20, 255))
    d.rectangle([(64, h - 40), (84, h - 16)], fill=(100, 65, 42, 255))
    img.save(PROC / "prop_bakery.png")
    print("OK bakery")


if __name__ == "__main__":
    pine_canopy()
    waterfall_bowl()
    facade(
        "prop_shop_awning.png",
        (148, 58, 46, 255),
        (200, 55, 50, 255),
        (245, 245, 245, 255),
        (245, 220, 140, 255),
        (218, 198, 168, 255),
        "GENERAL STORE",
    )
    facade(
        "prop_cafe_awning.png",
        (38, 110, 116, 255),
        (45, 145, 150, 255),
        (240, 248, 248, 255),
        (200, 235, 230, 255),
        (210, 200, 178, 255),
        "OAKHAVEN CAFE",
    )
    bakery()
