#!/usr/bin/env python3
"""P99 — bitmap-font storefront signs; windows below sign band (no letter clip)."""
from pathlib import Path
from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"

FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
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
}


def blit_text(img: Image.Image, x: int, y: int, text: str, color) -> None:
    for ch in text:
        rows = FONT.get(ch, FONT[" "])
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "1" and 0 <= x + c < img.width and 0 <= y + r < img.height:
                    img.putpixel((x + c, y + r), color)
        x += 6


def facade(name, roof, awn_a, awn_b, sign_bg, wall, label):
    w, h = 176, 148
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
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


def bakery():
    w, h = 140, 124
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(8, 36), (70, 2), (132, 36)], fill=(150, 62, 48, 255))
    d.polygon([(8, 36), (132, 36), (124, 46), (16, 46)], fill=(110, 42, 32, 255))
    d.rectangle([(12, 46), (w - 12, h - 6)], fill=(228, 210, 185, 255))
    d.rectangle([(12, 46), (w - 12, h - 6)], outline=(72, 52, 36, 255), width=2)
    d.rectangle([(10, h - 16), (w - 10, h - 4)], fill=(125, 118, 110, 255))
    for i, x0 in enumerate(range(16, 120, 10)):
        c = (210, 60, 55, 255) if i % 2 == 0 else (245, 245, 245, 255)
        d.rectangle([(x0, 48), (x0 + 9, 62)], fill=c)
        d.pieslice([(x0, 58), (x0 + 9, 70)], 0, 180, fill=c)
    d.rectangle([(34, 70), (106, 96)], fill=(85, 58, 36, 255))
    d.rectangle([(38, 74), (102, 92)], fill=(245, 220, 150, 255))
    blit_text(img, 46, 78, "BAKERY", (70, 40, 20, 255))
    d.rectangle([(60, h - 40), (80, h - 16)], fill=(100, 65, 42, 255))
    img.save(PROC / "prop_bakery.png")
    print("OK bakery")


if __name__ == "__main__":
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
