#!/usr/bin/env python3
"""P148 — deepen residential + Miller farmhouse facades (stone, shutters, porch, flowers)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"


def _shade_rect(d, box, base, dark, light) -> None:
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=base)
    d.rectangle([x0, y0, x0 + 2, y1], fill=light)
    d.rectangle([x0, y0, x1, y0 + 2], fill=light)
    d.rectangle([x1 - 2, y0, x1, y1], fill=dark)
    d.rectangle([x0, y1 - 2, x1, y1], fill=dark)


def _stone(d, x0, y0, x1, y1) -> None:
    d.rectangle([x0, y0, x1, y1], fill=(112, 106, 98, 255))
    for x in range(x0 + 2, x1 - 2, 8):
        for y in range(y0 + 1, y1 - 1, 4):
            lit = ((x // 8) + (y // 4)) % 2 == 0
            c = (138, 132, 122, 255) if lit else (95, 90, 82, 255)
            d.rectangle([x, y, min(x + 6, x1 - 2), min(y + 2, y1 - 1)], fill=c)


def _window(d, wx, wy, ww, wh, shutter=None, flowers=True) -> None:
    d.rectangle([wx - 2, wy - 2, wx + ww + 2, wy + wh + 2], fill=(70, 50, 34, 255))
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=(155, 200, 235, 255))
    d.line([(wx + ww // 2, wy), (wx + ww // 2, wy + wh)], fill=(90, 70, 50, 255))
    d.line([(wx, wy + wh // 2), (wx + ww, wy + wh // 2)], fill=(90, 70, 50, 255))
    d.line([(wx + 1, wy + 1), (wx + 5, wy + 1)], fill=(240, 250, 255, 200))
    if shutter:
        d.rectangle([wx - 6, wy, wx - 2, wy + wh], fill=(*shutter, 255))
        d.rectangle([wx + ww + 2, wy, wx + ww + 6, wy + wh], fill=(*shutter, 255))
        d.line([(wx - 4, wy + 1), (wx - 4, wy + wh - 1)], fill=(40, 40, 40, 100))
        d.line([(wx + ww + 4, wy + 1), (wx + ww + 4, wy + wh - 1)], fill=(40, 40, 40, 100))
    if flowers:
        d.rectangle([wx - 1, wy + wh + 1, wx + ww + 1, wy + wh + 6], fill=(90, 58, 36, 255))
        for fx in range(wx + 1, wx + ww - 1, 4):
            d.ellipse([fx, wy + wh - 1, fx + 3, wy + wh + 4], fill=(210, 70, 90, 255) if (fx // 4) % 2 else (240, 200, 70, 255))
            d.ellipse([fx + 1, wy + wh - 2, fx + 2, wy + wh + 1], fill=(50, 130, 55, 255))


def house(name: str, wall, roof, accent, shutter) -> None:
    w, h = 96, 104
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([10, h - 12, w - 10, h - 2], fill=(28, 36, 24, 75))
    mid = w // 2
    roof_d = tuple(max(0, c - 35) for c in roof[:3]) + (255,)
    roof_l = tuple(min(255, c + 28) for c in roof[:3]) + (255,)
    d.polygon([(4, 32), (mid, 4), (w - 4, 32)], fill=(*roof, 255))
    d.polygon([(4, 32), (w - 4, 32), (w - 12, 42), (12, 42)], fill=roof_d)
    for yy in range(10, 32, 3):
        inset = 8 + (yy - 10)
        d.line([(inset, yy), (w - inset, yy)], fill=tuple(max(0, c - 20) for c in roof[:3]) + (150,))
    # Chimney + smoke puff
    d.rectangle([w - 28, 8, w - 18, 34], fill=(118, 110, 102, 255))
    d.rectangle([w - 30, 6, w - 16, 10], fill=(95, 88, 80, 255))
    d.ellipse([w - 27, 1, w - 19, 9], fill=(220, 220, 230, 140))
    # Fascia
    d.rectangle([10, 40, w - 10, 46], fill=(235, 225, 210, 255))
    wall_d = (max(0, wall[0] - 40), max(0, wall[1] - 40), max(0, wall[2] - 40), 255)
    wall_l = (min(255, wall[0] + 18), min(255, wall[1] + 18), min(255, wall[2] + 12), 255)
    _shade_rect(d, (12, 44, w - 12, h - 18), (*wall, 255), wall_d, wall_l)
    # Timber
    d.rectangle([12, 44, w - 12, 48], fill=(*accent, 255))
    d.rectangle([12, 68, w - 12, 71], fill=(*accent, 255))
    d.rectangle([mid - 2, 44, mid + 2, h - 18], fill=(*accent, 255))
    d.rectangle([12, 44, 16, h - 18], fill=(*accent, 255))
    d.rectangle([w - 16, 44, w - 12, h - 18], fill=(*accent, 255))
    # Plank lines
    for bx in range(20, w - 20, 6):
        d.line([(bx, 48), (bx, h - 20)], fill=(max(0, wall[0] - 18), max(0, wall[1] - 18), max(0, wall[2] - 14), 120))
    _window(d, 20, 52, 16, 12, shutter, True)
    _window(d, w - 36, 52, 16, 12, shutter, True)
    # Door + porch
    dx0, dx1 = mid - 9, mid + 9
    d.rectangle([dx0 - 2, h - 44, dx1 + 2, h - 18], fill=(55, 38, 24, 255))
    d.rectangle([dx0, h - 42, dx1, h - 20], fill=(*accent, 255) if accent[0] > 80 else (100, 65, 42, 255))
    d.rectangle([dx0 + 2, h - 40, mid - 1, h - 30], fill=(78, 48, 28, 255))
    d.rectangle([mid + 1, h - 40, dx1 - 2, h - 30], fill=(78, 48, 28, 255))
    d.ellipse([dx1 - 5, h - 34, dx1 - 2, h - 31], fill=(220, 185, 90, 255))
    _stone(d, 10, h - 18, w - 10, h - 6)
    d.rectangle([dx0 - 4, h - 12, dx1 + 4, h - 6], fill=(128, 96, 58, 255))
    d.line([(dx0 - 4, h - 9), (dx1 + 4, h - 9)], fill=(100, 72, 42, 255))
    # Side planter
    d.rectangle([14, h - 28, 28, h - 20], fill=(55, 110, 48, 255))
    for fx in range(16, 27, 3):
        d.point((fx, h - 30), fill=(240, 90, 110, 255))
    img.save(PROC / name)
    print("OK", name, img.size)


def farmhouse_dark() -> None:
    """Miller farmhouse — larger timber cottage with porch depth."""
    w, h = 120, 112
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([12, h - 12, w - 12, h - 2], fill=(28, 36, 24, 80))
    mid = w // 2
    roof = (78, 58, 42, 255)
    roof_d = (55, 40, 28, 255)
    d.polygon([(6, 36), (mid, 4), (w - 6, 36)], fill=roof)
    d.polygon([(6, 36), (w - 6, 36), (w - 14, 48), (14, 48)], fill=roof_d)
    for yy in range(10, 36, 3):
        inset = 10 + (yy - 10)
        d.line([(inset, yy), (w - inset, yy)], fill=(45, 32, 22, 160))
    # Loft window
    d.rectangle([mid - 7, 14, mid + 7, 26], fill=(70, 50, 34, 255))
    d.rectangle([mid - 5, 16, mid + 5, 24], fill=(155, 200, 235, 255))
    d.line([(mid, 16), (mid, 24)], fill=(70, 50, 34, 255))
    d.rectangle([w - 34, 8, w - 22, 40], fill=(118, 110, 102, 255))
    d.rectangle([w - 36, 6, w - 20, 10], fill=(95, 88, 80, 255))
    d.ellipse([w - 33, 1, w - 23, 10], fill=(220, 220, 230, 140))
    d.rectangle([12, 46, w - 12, 52], fill=(235, 225, 210, 255))
    wall = (232, 218, 195, 255)
    _shade_rect(d, (14, 50, w - 14, h - 20), wall, (190, 170, 145, 255), (248, 238, 220, 255))
    timber = (85, 58, 38, 255)
    d.rectangle([14, 50, w - 14, 54], fill=timber)
    d.rectangle([14, 74, w - 14, 78], fill=timber)
    d.rectangle([mid - 2, 50, mid + 2, h - 20], fill=timber)
    d.rectangle([14, 50, 18, h - 20], fill=timber)
    d.rectangle([w - 18, 50, w - 14, h - 20], fill=timber)
    for bx in range(22, w - 22, 5):
        d.line([(bx, 54), (bx, h - 22)], fill=(200, 185, 160, 100))
    shut = (55, 105, 60)
    _window(d, 22, 58, 18, 14, shut, True)
    _window(d, w - 42, 58, 18, 14, shut, True)
    _window(d, 22, 82, 16, 12, None, False)
    # Door right of center (cozy farmhouse asymmetry)
    dx0, dx1 = mid + 4, mid + 22
    d.rectangle([dx0 - 2, h - 48, dx1 + 2, h - 20], fill=(55, 38, 24, 255))
    d.rectangle([dx0, h - 46, dx1, h - 22], fill=(98, 62, 38, 255))
    d.rectangle([dx0 + 2, h - 44, mid + 12, h - 34], fill=(78, 48, 28, 255))
    d.rectangle([mid + 14, h - 44, dx1 - 2, h - 34], fill=(78, 48, 28, 255))
    d.ellipse([dx1 - 5, h - 36, dx1 - 2, h - 33], fill=(220, 185, 90, 255))
    _stone(d, 12, h - 20, w - 12, h - 6)
    d.rectangle([dx0 - 6, h - 14, dx1 + 6, h - 6], fill=(128, 96, 58, 255))
    d.line([(dx0 - 6, h - 10), (dx1 + 6, h - 10)], fill=(100, 72, 42, 255))
    # Laundry line / porch rail hint
    d.line([(20, h - 26), (48, h - 26)], fill=(160, 140, 110, 200))
    for lx in (24, 32, 40):
        d.rectangle([lx, h - 34, lx + 3, h - 26], fill=(240, 240, 248, 200))
    img.save(PROC / "prop_farmhouse_darkroof.png")
    print("OK prop_farmhouse_darkroof", img.size)
    # Also refresh generic farmhouse used at lake/terrace
    house("prop_farmhouse.png", (235, 220, 195), (110, 70, 50), (70, 50, 35), (70, 110, 70))


def main() -> None:
    house("prop_house_redroof.png", (222, 200, 172), (168, 68, 52), (115, 55, 38), (70, 110, 70))
    house("prop_house_slateroof.png", (198, 204, 210), (70, 88, 112), (55, 65, 85), (50, 80, 120))
    house("prop_house_thatch.png", (218, 198, 158), (145, 122, 68), (100, 78, 42), (120, 95, 50))
    house("prop_house_greenroof.png", (200, 208, 180), (62, 118, 78), (50, 88, 58), (40, 90, 50))
    farmhouse_dark()


if __name__ == "__main__":
    main()
