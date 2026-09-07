#!/usr/bin/env python3
"""P139 — hero storefronts with Stardew-like depth (stone footing, goods windows, layered awning)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"


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
        "I": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
        "'": ["00100", "00100", "00000", "00000", "00000", "00000", "00000"],
    }
    for ch in text:
        rows = font.get(ch, font[" "])
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "1" and 0 <= x + c < img.width and 0 <= y + r < img.height:
                    img.putpixel((x + c, y + r), color)
        x += 6


def _shade_rect(d: ImageDraw.ImageDraw, box, base, dark, light) -> None:
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=base)
    d.rectangle([x0, y0, x0 + 2, y1], fill=light)
    d.rectangle([x0, y0, x1, y0 + 2], fill=light)
    d.rectangle([x1 - 2, y0, x1, y1], fill=dark)
    d.rectangle([x0, y1 - 2, x1, y1], fill=dark)


def _stone_footing(d: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int) -> None:
    d.rectangle([x0, y0, x1, y1], fill=(112, 106, 98, 255))
    for x in range(x0 + 2, x1 - 2, 9):
        for y in range(y0 + 1, y1 - 1, 5):
            lit = (x // 9 + y // 5) % 2 == 0
            c = (138, 132, 122, 255) if lit else (95, 90, 82, 255)
            d.rectangle([x, y, min(x + 7, x1 - 2), min(y + 3, y1 - 1)], fill=c)
            d.line([(min(x + 7, x1 - 2), y), (min(x + 7, x1 - 2), min(y + 3, y1 - 1))], fill=(70, 66, 60, 255))


def _awning(d: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, a, b) -> None:
    # Shadow under awning
    d.rectangle([x0 + 2, y1 - 2, x1 - 2, y1 + 6], fill=(40, 30, 20, 70))
    stripe = 11
    i = 0
    x = x0
    while x < x1:
        c = a if i % 2 == 0 else b
        x2 = min(x + stripe, x1)
        d.rectangle([x, y0, x2, y1], fill=c)
        # scallop
        d.pieslice([x, y1 - 4, x2, y1 + 10], 0, 180, fill=c)
        # highlight edge
        d.line([(x + 1, y0 + 1), (x + 1, y1 - 2)], fill=tuple(min(255, v + 35) for v in c[:3]) + (180,))
        x = x2
        i += 1
    # top rail
    d.rectangle([x0 - 1, y0 - 3, x1 + 1, y0 + 1], fill=(70, 48, 32, 255))


def _goods_window(d: ImageDraw.ImageDraw, wx: int, wy: int, ww: int, wh: int, goods) -> None:
    # Frame + recess
    d.rectangle([wx - 2, wy - 2, wx + ww + 2, wy + wh + 2], fill=(70, 50, 34, 255))
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(55, 70, 85, 255))
    # Interior shelf goods
    for i, g in enumerate(goods):
        gx = wx + 3 + (i % 3) * 7
        gy = wy + wh - 8 - (i // 3) * 8
        d.ellipse([gx, gy, gx + 5, gy + 5], fill=g)
    # Glass tint + muntins
    for yy in range(wy, wy + wh):
        for xx in range(wx, wx + ww):
            if (xx + yy) % 7 == 0:
                continue
    d.rectangle([wx, wy, wx + ww, wy + wh], outline=(190, 220, 240, 120))
    mx = wx + ww // 2
    my = wy + wh // 2
    d.line([(mx, wy), (mx, wy + wh)], fill=(90, 70, 50, 200))
    d.line([(wx, my), (wx + ww, my)], fill=(90, 70, 50, 200))
    # Specular
    d.line([(wx + 2, wy + 2), (wx + 8, wy + 2)], fill=(240, 250, 255, 200))
    # Flower box
    d.rectangle([wx - 1, wy + wh + 1, wx + ww + 1, wy + wh + 7], fill=(90, 58, 36, 255))
    for fx in range(wx + 2, wx + ww - 2, 5):
        d.ellipse([fx, wy + wh - 1, fx + 4, wy + wh + 4], fill=(200, 70, 90, 255) if (fx // 5) % 2 else (230, 190, 60, 255))
        d.ellipse([fx + 1, wy + wh - 3, fx + 3, wy + wh], fill=(50, 130, 55, 255))


def facade(
    name: str,
    roof,
    awn_a,
    awn_b,
    sign_bg,
    wall,
    wall_d,
    wall_l,
    label: str,
    goods,
) -> None:
    w, h = 192, 168
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Grounding shadow
    d.ellipse([14, h - 16, w - 14, h - 2], fill=(28, 36, 24, 80))
    # Side wall depth slab (right)
    d.polygon([(w - 22, 48), (w - 8, 56), (w - 8, h - 18), (w - 22, h - 24)], fill=wall_d)
    # Roof
    mid = w // 2
    d.polygon([(4, 44), (mid, 4), (w - 18, 44)], fill=roof)
    roof_d = tuple(max(0, c - 38) for c in roof[:3]) + (255,)
    d.polygon([(4, 44), (w - 18, 44), (w - 26, 56), (12, 56)], fill=roof_d)
    for yy in range(12, 44, 3):
        inset = 10 + (yy - 12)
        d.line([(inset, yy), (w - 18 - inset // 2, yy)], fill=tuple(max(0, c - 20) for c in roof[:3]) + (160,))
    # Chimney
    d.rectangle([w - 48, 10, w - 34, 46], fill=(118, 110, 102, 255))
    d.rectangle([w - 50, 8, w - 32, 14], fill=(95, 90, 82, 255))
    d.ellipse([w - 46, 2, w - 36, 12], fill=(220, 220, 230, 140))
    # Fascia
    d.rectangle([10, 52, w - 24, 58], fill=(235, 225, 210, 255))
    d.line([(10, 58), (w - 24, 58)], fill=(170, 155, 135, 255))
    # Wall body
    _shade_rect(d, (12, 56, w - 24, h - 22), wall, wall_d, wall_l)
    # Timber beams
    d.rectangle([12, 70, w - 24, 74], fill=(95, 68, 42, 255))
    d.rectangle([12, 108, w - 24, 112], fill=(95, 68, 42, 255))
    for bx in (28, mid, w - 40):
        d.rectangle([bx - 1, 56, bx + 1, h - 22], fill=(105, 75, 48, 200))
    # Awning
    _awning(d, 16, 58, w - 28, 78, awn_a, awn_b)
    # Sign board with hanging chains
    tw = len(label) * 6 + 14
    sx = max(20, (w - 24 - tw) // 2 + 6)
    d.line([(sx + 4, 78), (sx + 4, 86)], fill=(70, 50, 30, 255))
    d.line([(sx + tw - 4, 78), (sx + tw - 4, 86)], fill=(70, 50, 30, 255))
    d.rectangle([sx - 6, 84, sx + tw + 6, 108], fill=(72, 48, 30, 255))
    d.rectangle([sx - 4, 86, sx + tw + 4, 106], fill=sign_bg)
    d.rectangle([sx - 3, 87, sx + tw + 3, 105], outline=(140, 100, 50, 255))
    blit_text(img, sx, 91, label, (42, 28, 16, 255))
    # Display windows with goods
    _goods_window(d, 22, 114, 28, 22, goods[:4])
    _goods_window(d, w - 62, 114, 28, 22, goods[2:])
    # Door with panels + porch step
    dx0, dx1 = mid - 12, mid + 12
    d.rectangle([dx0 - 2, h - 56, dx1 + 2, h - 22], fill=(55, 38, 24, 255))
    d.rectangle([dx0, h - 54, dx1, h - 24], fill=(98, 62, 38, 255))
    d.rectangle([dx0 + 2, h - 52, mid - 1, h - 40], fill=(78, 48, 28, 255))
    d.rectangle([mid + 1, h - 52, dx1 - 2, h - 40], fill=(78, 48, 28, 255))
    d.rectangle([dx0 + 2, h - 38, mid - 1, h - 26], fill=(78, 48, 28, 255))
    d.rectangle([mid + 1, h - 38, dx1 - 2, h - 26], fill=(78, 48, 28, 255))
    d.ellipse([dx1 - 6, h - 40, dx1 - 3, h - 37], fill=(220, 185, 90, 255))
    # Stone footing + wood porch step
    _stone_footing(d, 10, h - 22, w - 20, h - 8)
    d.rectangle([dx0 - 6, h - 14, dx1 + 6, h - 8], fill=(128, 96, 58, 255))
    d.line([(dx0 - 6, h - 11), (dx1 + 6, h - 11)], fill=(100, 72, 42, 255))
    img.save(PROC / name)
    print("OK", name, label, img.size)


def bakery() -> None:
    w, h = 160, 148
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([12, h - 14, w - 12, h - 2], fill=(28, 36, 24, 80))
    roof = (150, 62, 48, 255)
    roof_d = (110, 42, 32, 255)
    mid = w // 2
    d.polygon([(6, 40), (mid, 4), (w - 6, 40)], fill=roof)
    d.polygon([(6, 40), (w - 6, 40), (w - 14, 52), (14, 52)], fill=roof_d)
    for yy in range(12, 40, 3):
        inset = 8 + (yy - 12)
        d.line([(inset, yy), (w - inset, yy)], fill=(90, 35, 28, 160))
    d.rectangle([w - 36, 10, w - 24, 42], fill=(118, 110, 102, 255))
    wall = (232, 214, 188, 255)
    _shade_rect(d, (12, 50, w - 12, h - 20), wall, (200, 180, 155, 255), (248, 236, 215, 255))
    d.rectangle([12, 64, w - 12, 68], fill=(95, 68, 42, 255))
    _awning(d, 16, 52, w - 16, 70, (210, 60, 55, 255), (245, 245, 245, 255))
    tw = len("BAKERY") * 6 + 14
    sx = (w - tw) // 2
    d.rectangle([sx - 6, 76, sx + tw + 6, 100], fill=(72, 48, 30, 255))
    d.rectangle([sx - 4, 78, sx + tw + 4, 98], fill=(245, 220, 150, 255))
    blit_text(img, sx, 83, "BAKERY", (70, 40, 20, 255))
    # Big display + loaves
    d.rectangle([18, 106, 70, 128], fill=(70, 50, 34, 255))
    d.rectangle([20, 108, 68, 126], fill=(60, 75, 90, 255))
    for lx, ly in ((24, 118), (34, 116), (44, 119), (54, 117)):
        d.ellipse([lx, ly, lx + 10, ly + 6], fill=(190, 140, 80, 255))
        d.ellipse([lx + 1, ly - 1, lx + 9, ly + 3], fill=(220, 175, 110, 255))
    d.line([(44, 108), (44, 126)], fill=(90, 70, 50, 200))
    d.line([(20, 117), (68, 117)], fill=(90, 70, 50, 200))
    d.rectangle([18, 128, 70, 134], fill=(90, 58, 36, 255))
    for fx in range(22, 66, 6):
        d.ellipse([fx, 126, fx + 4, 132], fill=(220, 80, 90, 255))
    # Door
    d.rectangle([mid - 10, h - 52, mid + 10, h - 20], fill=(100, 65, 42, 255))
    d.ellipse([mid + 4, h - 38, mid + 7, h - 35], fill=(220, 185, 90, 255))
    # Oven chimney smoke hint on wall
    d.rectangle([w - 48, 108, w - 28, 128], fill=(90, 55, 40, 255))
    d.rectangle([w - 46, 110, w - 30, 118], fill=(40, 30, 25, 255))
    _stone_footing(d, 10, h - 20, w - 10, h - 6)
    d.rectangle([mid - 14, h - 12, mid + 14, h - 6], fill=(128, 96, 58, 255))
    img.save(PROC / "prop_bakery.png")
    print("OK prop_bakery", img.size)


def main() -> None:
    produce = [
        (210, 55, 50, 255),
        (240, 180, 50, 255),
        (70, 150, 60, 255),
        (230, 100, 40, 255),
        (180, 60, 90, 255),
        (250, 220, 80, 255),
    ]
    cafe_goods = [
        (120, 75, 45, 255),
        (240, 230, 210, 255),
        (90, 55, 35, 255),
        (200, 160, 100, 255),
        (160, 100, 60, 255),
        (230, 200, 160, 255),
    ]
    facade(
        "prop_shop_awning.png",
        (148, 58, 46, 255),
        (200, 55, 50, 255),
        (245, 245, 245, 255),
        (245, 220, 140, 255),
        (218, 198, 168, 255),
        (175, 155, 125, 255),
        (240, 225, 200, 255),
        "GENERAL STORE",
        produce,
    )
    facade(
        "prop_cafe_awning.png",
        (38, 110, 116, 255),
        (45, 145, 150, 255),
        (240, 248, 248, 255),
        (200, 235, 230, 255),
        (210, 200, 178, 255),
        (170, 160, 140, 255),
        (235, 228, 210, 255),
        "OAKHAVEN CAFE",
        cafe_goods,
    )
    bakery()


if __name__ == "__main__":
    main()
