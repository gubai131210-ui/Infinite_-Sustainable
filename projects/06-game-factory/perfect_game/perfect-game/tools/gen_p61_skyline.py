"""P61–P63: continuous rocky skyline, path fringe flowers, richer storefronts."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"


def skyline() -> None:
    """One continuous rocky ridge with tall sky + clouds; waterfall windows."""
    w, h = 384, 80
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Tall sky
    for y in range(0, 42):
        t = y / 41.0
        d.line([(0, y), (w - 1, y)], fill=(90 + int(50 * t), 150 + int(40 * t), 235, 245))
    # Clouds
    for cx, cy, cw in [(24, 10, 48), (100, 6, 56), (180, 12, 44), (250, 8, 52), (320, 11, 46)]:
        d.ellipse((cx, cy, cx + cw, cy + 16), fill=(250, 252, 255, 240))
        d.ellipse((cx + 14, cy - 4, cx + cw + 8, cy + 12), fill=(255, 255, 255, 250))
    # Ridge top
    tops = []
    for x in range(w):
        y = 40 + int(7 * math.sin(x * 0.028) + 5 * math.sin(x * 0.07 + 0.8) + 3 * math.sin(x * 0.15))
        # Soft gaps (waterfall / ruins windows) — lower rock, more sky
        if 60 <= x <= 110 or 175 <= x <= 230:
            y = 58 + int(2 * math.sin(x * 0.12))
        tops.append(y)
    for x, ytop in enumerate(tops):
        for y in range(ytop, h):
            depth = y - ytop
            # Grey-brown rock, not green canopy
            r = 95 + depth * 2 + (x % 3)
            g = 92 + depth + (y % 2)
            b = 82 + depth // 2
            img.putpixel((x, y), (min(150, r), min(130, g), min(115, b), 255))
        # Darker cliff lip
        if ytop < h - 1:
            img.putpixel((x, ytop), (70, 68, 62, 255))
    # Sparse pines only on high peaks
    for i, x0 in enumerate(range(16, w - 16, 40)):
        if 60 <= x0 <= 110 or 175 <= x0 <= 230:
            continue
        y0 = tops[x0] - 10 - (i % 2) * 2
        d.polygon([(x0, y0 + 12), (x0 + 4, y0), (x0 + 8, y0 + 12)], fill=(32, 72, 42, 235))
        d.rectangle((x0 + 3, y0 + 11, x0 + 5, y0 + 17), fill=(65, 42, 28, 255))
    img.save(PROC / "prop_ridge_organic.png")
    print("OK prop_ridge_organic", w, h)


def path_fringe(name: str) -> None:
    """Tiny grass tuft / flower cluster for path edges."""
    img = Image.new("RGBA", (16, 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((2, 6, 7, 11), fill=(70, 130, 55, 255))
    d.ellipse((6, 5, 12, 11), fill=(60, 120, 50, 255))
    d.point((4, 4), fill=(220, 90, 100, 255))
    d.point((9, 3), fill=(240, 200, 80, 255))
    d.point((11, 5), fill=(200, 80, 160, 255))
    img.save(PROC / name)
    print("OK", name)


def storefront(name: str, roof: tuple, awn_a: tuple, awn_b: tuple) -> None:
    w, h = 104, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Roof with eave depth
    d.polygon([(2, 24), (52, 2), (102, 24)], fill=roof)
    shade = tuple(max(0, c - 32) for c in roof[:3]) + (255,)
    d.polygon([(2, 24), (102, 24), (96, 34), (8, 34)], fill=shade)
    for yy in range(8, 24, 3):
        d.line([(16, yy), (88, yy)], fill=shade, width=1)
    # Chimney + smoke
    d.rectangle((78, 8, 90, 28), fill=(100, 90, 85, 255))
    d.ellipse((80, 1, 92, 10), fill=(230, 230, 235, 160))
    # Walls timber
    d.rectangle((10, 34, 94, h - 6), fill=(218, 200, 172, 255))
    d.rectangle((10, 34, 94, h - 6), outline=(75, 55, 40, 255), width=2)
    d.line([(52, 34), (52, h - 6)], fill=(75, 55, 40, 255), width=2)
    d.line([(10, 52), (94, 52)], fill=(75, 55, 40, 255), width=1)
    # Deep scalloped awning
    for i, x0 in enumerate(range(14, 90, 10)):
        c = awn_a if i % 2 == 0 else awn_b
        d.rectangle((x0, 36, x0 + 9, 52), fill=c)
        d.pieslice((x0, 48, x0 + 9, 60), 0, 180, fill=c)
    # Sign
    d.rectangle((32, 54, 72, 66), fill=(95, 70, 45, 255))
    d.rectangle((34, 56, 70, 64), fill=(235, 215, 150, 255))
    # Display windows
    for wx in (16, 76):
        d.rectangle((wx, 58, wx + 16, 74), fill=(155, 200, 230, 255))
        d.line([(wx + 8, 58), (wx + 8, 74)], fill=(100, 140, 160, 255))
        d.line([(wx, 66), (wx + 16, 66)], fill=(100, 140, 160, 255))
    # Door + porch
    d.rectangle((46, h - 30, 58, h - 6), fill=(105, 70, 48, 255))
    d.rectangle((54, h - 22, 56, h - 20), fill=(220, 190, 100, 255))
    d.rectangle((38, h - 8, 66, h - 4), fill=(90, 85, 80, 255))
    # Planters
    d.rectangle((14, h - 14, 28, h - 6), fill=(65, 115, 50, 255))
    d.rectangle((76, h - 14, 90, h - 6), fill=(65, 115, 50, 255))
    for fx in (16, 20, 24, 78, 82, 86):
        d.point((fx, h - 15), fill=(230, 70, 90, 255))
    img.save(PROC / name)
    print("OK", name)


def house(name: str, wall: tuple, roof: tuple, accent: tuple) -> None:
    w, h = 80, 88
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(4, 26), (w // 2, 2), (w - 4, 26)], fill=roof)
    shade = tuple(max(0, c - 28) for c in roof[:3]) + (255,)
    d.polygon([(4, 26), (w - 4, 26), (w - 10, 34), (10, 34)], fill=shade)
    for yy in range(8, 26, 3):
        d.line([(12, yy), (w - 12, yy)], fill=shade, width=1)
    d.rectangle((w // 2 + 12, 8, w // 2 + 22, 28), fill=(105, 95, 90, 255))
    d.ellipse((w // 2 + 13, 1, w // 2 + 24, 10), fill=(230, 230, 235, 155))
    d.rectangle((10, 34, w - 10, h - 4), fill=wall)
    frame = (68, 52, 38, 255)
    d.rectangle((10, 34, w - 10, h - 4), outline=frame, width=2)
    d.line([(w // 2, 34), (w // 2, h - 4)], fill=frame, width=2)
    d.line([(10, 50), (w - 10, 50)], fill=frame, width=1)
    for wx in (16, w - 30):
        d.rectangle((wx - 2, 40, wx + 14, 52), fill=(90, 70, 50, 255))
        d.rectangle((wx, 42, wx + 12, 50), fill=(185, 215, 235, 255))
    d.rectangle((w // 2 - 7, h - 26, w // 2 + 7, h - 4), fill=accent)
    d.rectangle((14, 52, 30, 56), fill=(70, 120, 60, 255))
    img.save(PROC / name)
    print("OK", name)


def main() -> None:
    skyline()
    path_fringe("prop_path_tuft.png")
    house("prop_house_redroof.png", (222, 200, 172, 255), (168, 68, 52, 255), (115, 55, 38, 255))
    house("prop_house_slateroof.png", (198, 204, 210, 255), (70, 88, 112, 255), (55, 65, 85, 255))
    house("prop_house_thatch.png", (218, 198, 158, 255), (145, 122, 68, 255), (100, 78, 42, 255))
    house("prop_house_greenroof.png", (200, 208, 180, 255), (62, 118, 78, 255), (50, 88, 58, 255))
    storefront("prop_shop_awning.png", (148, 58, 46, 255), (200, 55, 50, 255), (245, 245, 245, 255))
    storefront("prop_cafe_awning.png", (38, 110, 116, 255), (45, 145, 150, 255), (240, 248, 248, 255))
    print("P61-P63 assets done")


if __name__ == "__main__":
    main()
