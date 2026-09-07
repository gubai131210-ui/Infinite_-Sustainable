#!/usr/bin/env python3
"""P151 — station hall + steam train + pine canopy station window; refresh waterfall bowl."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"
WORLD_W = 192 * 16
rng = random.Random(151)


def blit_text(img: Image.Image, x: int, y: int, text: str, color) -> None:
    font = {
        "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
        "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
        "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
        "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
        "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
        "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
        "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
        "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
        "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
        "I": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
        " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    }
    for ch in text:
        rows = font.get(ch, font[" "])
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "1" and 0 <= x + c < img.width and 0 <= y + r < img.height:
                    img.putpixel((x + c, y + r), color)
        x += 6


def pine_canopy() -> None:
    """North pine mass — waterfall + station windows kept open."""
    w, h = WORLD_W, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def in_wf(x: int) -> bool:
        return 260 <= x <= 540

    def in_station(x: int) -> bool:
        # Station hall/platform band (tile ~136–178 → ~2176–2848)
        return 2100 <= x <= 2920

    for x in range(0, w, 22):
        if in_wf(x) or in_station(x):
            continue
        cx, cy = x + 18, 22 + (x // 55) % 6
        d.ellipse((cx - 44, cy - 16, cx + 48, cy + 20), fill=(55, 95, 72, 160))
        d.ellipse((cx - 28, cy - 26, cx + 30, cy + 6), fill=(62, 108, 80, 170))
    for x in range(0, w, 16):
        if in_wf(x) or in_station(x):
            continue
        cx = x + 12 + (x % 7)
        cy = 42 + (x // 28) % 12
        d.ellipse((cx - 48, cy - 18, cx + 52, cy + 30), fill=(28, 72, 42, 220))
        d.ellipse((cx - 32, cy - 34, cx + 34, cy + 8), fill=(36, 88, 52, 230))
    for x in range(0, w, 12):
        if in_wf(x) or in_station(x):
            continue
        cx = x + 8
        cy = 58 + (x * 3) % 14
        d.ellipse((cx - 40, cy - 14, cx + 44, cy + 32), fill=(16, 48, 28, 245))
        d.ellipse((cx - 22, cy - 28, cx + 26, cy + 6), fill=(22, 58, 34, 250))
    for x in range(6, w - 6, 9):
        if in_wf(x) or in_station(x):
            continue
        base = h - 4
        tip = base - (38 + (x * 11) % 22)
        half = 7 + (x % 6)
        d.polygon([(x, tip), (x - half, base), (x + half, base)], fill=(12, 40, 22, 255))
    # Soft flanks beside station (not over roof)
    for cx in (2050, 2980):
        d.ellipse((cx - 40, 40, cx + 40, 110), fill=(14, 42, 24, 220))
    img.save(PROC / "prop_pine_canopy.png")
    print("OK prop_pine_canopy", w, h)


def notch_skyline_waterfall() -> None:
    """Punch amphitheater corridor so skyline no longer blankets the falls."""
    path = PROC / "prop_skyline_wide.png"
    if not path.exists():
        print("SKIP skyline notch — missing", path.name)
        return
    img = Image.open(path).convert("RGBA")
    px = img.load()
    # Match pine waterfall window (~tiles 16–33 → px 256–528)
    x0, x1 = 250, 560
    for x in range(x0, x1):
        for y in range(img.height):
            r, g, b, a = px[x, y]
            # Soft edge: keep distant ridge tips, clear mid/lower mass
            edge = min(x - x0, x1 - 1 - x)
            fade = 1.0 if edge > 18 else edge / 18.0
            # Keep a little mountain tip above (top 18%)
            keep_top = 1.0 if y < int(img.height * 0.18) else 0.0
            clear = fade * (1.0 - keep_top * 0.55)
            na = int(a * (1.0 - 0.92 * clear))
            px[x, y] = (r, g, b, na)
    img.save(path)
    print("OK skyline waterfall notch", x0, x1)


def waterfall_bowl() -> None:
    """Larger amphitheater falls — cliff strata + multi-stream + foam bowl (scale≈1)."""
    w, h = 220, 280
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    mid = w // 2
    for y in range(0, h - 48):
        for x in range(w):
            flare = 22 + y // 6
            # Amphitheater outer cliff walls
            wall = x < 34 or x > w - 34
            throat = abs(x - mid) < flare + 8
            shelf_band = any(abs(y - sy) < 5 for sy in (36, 72, 110, 148))
            if y < 28 and 70 < x < 150:
                continue  # sky notch at crest
            if not wall and not throat and not shelf_band and abs(x - mid) > flare + 36:
                continue
            n = (x * 17 + y * 13) & 15
            rr = 58 + n * 2 + y // 10
            gg = 56 + n + y // 12
            bb = 52 + n // 2
            if n % 5 == 0:
                rr, gg, bb = 42, 72, 40
            if n % 7 == 0:
                rr, gg, bb = 92, 84, 72
            if wall:
                rr, gg, bb = rr - 14, gg - 12, bb - 10
            img.putpixel((x, y), (max(18, min(135, rr)), max(18, min(125, gg)), max(16, min(115, bb)), 255))
    for shelf_y in (36, 72, 110, 148):
        for x in range(28, w - 28):
            if abs(x - mid) > 68 - (shelf_y - 36) // 5:
                continue
            for dy in range(5):
                y = shelf_y + dy
                moss = dy < 2
                c = (48 + dy * 5, 78 + dy * 2, 44, 255) if moss else (78, 70, 58, 255)
                img.putpixel((x, y), c)
    # Multi-stream white water
    for i, x0 in enumerate(range(78, 148, 5)):
        wob = int(4 * math.sin(i * 0.65))
        top = 24 + (i % 4)
        bot = h - 72
        d.rectangle((x0 + wob, top, x0 + 6 + wob, bot), fill=(145, 195, 235, 210))
        d.rectangle((x0 + 1 + wob, top + 3, x0 + 5 + wob, bot - 3), fill=(215, 238, 255, 235))
        if i % 2 == 0:
            d.line([(x0 + 3 + wob, top), (x0 + 3 + wob, bot)], fill=(245, 252, 255, 210))
    # Tier pools
    for pool_y, rw, rh in ((118, 42, 14), (158, 50, 16)):
        d.ellipse([mid - rw, pool_y, mid + rw, pool_y + rh], fill=(160, 205, 240, 200))
        d.ellipse([mid - rw + 6, pool_y + 3, mid + rw - 6, pool_y + rh - 2], fill=(190, 225, 255, 160))
    # Base foam bowl
    for y in range(h - 70, h - 10):
        for x in range(40, w - 40):
            dx = (x - mid) / 62.0
            dy = (y - (h - 40)) / 26.0
            if dx * dx + dy * dy > 1.0:
                continue
            foam = 205 + ((x * 3 + y * 5) % 45)
            a = 230 if dy < 0.25 else 175
            img.putpixel((x, y), (min(255, foam), min(255, foam + 12), 255, a))
    for _ in range(55):
        x = rng.randint(60, w - 60)
        y = rng.randint(50, h - 80)
        d.ellipse((x - 1, y - 1, x + 2, y + 2), fill=(225, 242, 255, 150))
    foam_band = img.crop((36, h - 72, w - 36, h - 8)).filter(ImageFilter.GaussianBlur(0.7))
    img.paste(foam_band, (36, h - 72), foam_band)
    img.save(PROC / "prop_waterfall_bowl.png")
    print("OK prop_waterfall_bowl", w, h)


def station() -> None:
    w, h = 220, 120
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([16, h - 14, w - 16, h - 2], fill=(30, 40, 28, 70))
    # Platform
    d.rectangle([4, h - 28, w - 4, h - 8], fill=(148, 142, 134, 255))
    for x in range(8, w - 8, 10):
        d.line([(x, h - 26), (x, h - 10)], fill=(120, 114, 106, 255))
    d.rectangle([4, h - 12, w - 4, h - 8], fill=(110, 104, 96, 255))
    # Main hall
    d.rectangle([28, 36, 170, h - 28], fill=(210, 190, 160, 255))
    d.rectangle([28, 36, 170, h - 28], outline=(80, 60, 40, 255), width=2)
    for bx in range(34, 166, 6):
        d.line([(bx, 40), (bx, h - 32)], fill=(185, 165, 135, 140))
    # Roof
    d.polygon([(22, 40), (99, 6), (176, 40)], fill=(55, 78, 118, 255))
    d.polygon([(22, 40), (176, 40), (168, 50), (30, 50)], fill=(38, 58, 90, 255))
    for yy in range(12, 40, 3):
        inset = 12 + (yy - 12)
        d.line([(inset + 10, yy), (w - inset - 40, yy)], fill=(30, 48, 78, 160))
    # Clock
    d.ellipse([90, 14, 108, 32], fill=(240, 240, 245, 255), outline=(40, 40, 50, 255))
    d.line([(99, 23), (99, 16)], fill=(30, 30, 40, 255))
    d.line([(99, 23), (105, 23)], fill=(30, 30, 40, 255))
    d.rectangle([150, 10, 162, 40], fill=(118, 110, 102, 255))
    # Sign
    d.rectangle([70, 52, 128, 68], fill=(72, 48, 30, 255))
    d.rectangle([72, 54, 126, 66], fill=(245, 220, 150, 255))
    blit_text(img, 78, 56, "STATION", (50, 35, 20, 255))
    # Windows + door
    for wx in (40, 58, 140):
        d.rectangle([wx, 72, wx + 16, 88], fill=(70, 50, 34, 255))
        d.rectangle([wx + 2, 74, wx + 14, 86], fill=(155, 200, 235, 255))
        d.line([(wx + 8, 74), (wx + 8, 86)], fill=(70, 50, 34, 255))
    d.rectangle([92, 70, 116, h - 28], fill=(90, 55, 35, 255))
    d.rectangle([94, 72, 102, h - 30], fill=(70, 42, 26, 255))
    d.rectangle([106, 72, 114, h - 30], fill=(70, 42, 26, 255))
    d.ellipse([110, 90, 113, 93], fill=(220, 185, 90, 255))
    # Posts + canopy
    for px in (36, 70, 110, 150):
        d.rectangle([px, 50, px + 4, h - 28], fill=(95, 68, 42, 255))
    d.rectangle([30, 50, 166, 56], fill=(70, 50, 35, 255))
    # Side annex
    d.rectangle([168, 48, 210, h - 28], fill=(200, 182, 155, 255), outline=(80, 60, 40, 255))
    d.polygon([(166, 52), (189, 28), (212, 52)], fill=(55, 78, 118, 255))
    d.rectangle([178, 70, 192, 86], fill=(155, 200, 235, 255), outline=(70, 50, 34, 255))
    d.rectangle([196, 78, 206, h - 28], fill=(90, 55, 35, 255))
    # Bench + luggage cart
    d.rectangle([42, h - 40, 62, h - 34], fill=(110, 80, 50, 255))
    d.rectangle([44, h - 46, 46, h - 34], fill=(90, 65, 40, 255))
    d.rectangle([58, h - 46, 60, h - 34], fill=(90, 65, 40, 255))
    d.rectangle([148, h - 42, 164, h - 34], fill=(130, 130, 138, 255))
    d.ellipse([150, h - 34, 156, h - 28], fill=(60, 60, 68, 255))
    d.ellipse([158, h - 34, 164, h - 28], fill=(60, 60, 68, 255))
    img.save(PROC / "prop_station.png")
    print("OK prop_station", img.size)


def train() -> None:
    w, h = 160, 56
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Track
    d.rectangle([0, h - 10, w, h - 6], fill=(70, 70, 78, 255))
    d.rectangle([0, h - 8, w, h - 7], fill=(110, 110, 120, 255))
    for x in range(4, w, 12):
        d.rectangle([x, h - 12, x + 2, h - 4], fill=(90, 70, 45, 255))
    # Locomotive
    d.rectangle([8, 18, 52, h - 14], fill=(55, 58, 65, 255))
    d.rectangle([10, 8, 34, 22], fill=(45, 48, 55, 255))
    d.rectangle([14, 10, 24, 18], fill=(150, 200, 230, 255))
    d.rectangle([28, 2, 36, 14], fill=(40, 42, 48, 255))
    d.ellipse([24, 0, 40, 10], fill=(180, 180, 188, 160))
    d.ellipse([30, -2, 44, 8], fill=(200, 200, 210, 120))
    d.polygon([(4, h - 14), (12, h - 14), (8, h - 22)], fill=(140, 140, 150, 255))
    for wx in (14, 30):
        d.ellipse([wx, h - 18, wx + 12, h - 6], fill=(35, 35, 40, 255))
        d.ellipse([wx + 3, h - 15, wx + 9, h - 9], fill=(90, 90, 100, 255))
    # Cars
    for i, (x0, col) in enumerate([(56, (168, 72, 48, 255)), (100, (150, 120, 85, 255))]):
        d.rectangle([x0, 16, x0 + 40, h - 14], fill=col, outline=(60, 40, 28, 255))
        d.rectangle([x0, 14, x0 + 40, 18], fill=(70, 50, 35, 255))
        for wx in range(x0 + 6, x0 + 36, 10):
            d.rectangle([wx, 22, wx + 7, 32], fill=(155, 200, 235, 255), outline=(50, 40, 30, 255))
        for wx in (x0 + 6, x0 + 24):
            d.ellipse([wx, h - 18, wx + 12, h - 6], fill=(35, 35, 40, 255))
            d.ellipse([wx + 3, h - 15, wx + 9, h - 9], fill=(90, 90, 100, 255))
    img.save(PROC / "prop_train.png")
    print("OK prop_train", img.size)


def main() -> None:
    pine_canopy()
    notch_skyline_waterfall()
    waterfall_bowl()
    station()
    train()


if __name__ == "__main__":
    main()
