"""P69–P71: seamless full-width north skyline + hero town facades."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"

# Match world.gd: W=192 tiles * 16px
WORLD_W = 192 * 16  # 3072
SKY_H = 144


def seamless_skyline() -> None:
    """One continuous strip: sky → blue peaks → green hills.
    Waterfall bowl at world tile x≈24 (px≈384); ruins gap tiles≈68–100.
    """
    w, h = WORLD_W, SKY_H
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Tall bright sky (must read against grey viewport clear color)
    for y in range(0, 68):
        t = y / 67.0
        r = int(150 + 35 * t)
        g = int(195 + 30 * t)
        b = int(245)
        d.line([(0, y), (w - 1, y)], fill=(r, g, b, 255))

    # Soft fluffy clouds (no hard vertical repeat)
    clouds = [
        (40, 8, 70, 20),
        (180, 4, 90, 22),
        (320, 10, 64, 18),
        (480, 6, 88, 20),
        (660, 12, 72, 18),
        (820, 5, 96, 22),
        (1000, 9, 70, 18),
        (1180, 4, 100, 24),
        (1400, 11, 76, 18),
        (1580, 7, 92, 20),
        (1780, 5, 84, 22),
        (1980, 10, 68, 16),
        (2180, 6, 110, 24),
        (2420, 9, 80, 18),
        (2680, 4, 96, 22),
        (2900, 12, 70, 16),
    ]
    for cx, cy, cw, ch in clouds:
        d.ellipse((cx, cy, cx + cw, cy + ch), fill=(255, 255, 255, 230))
        d.ellipse((cx + 12, cy - 5, cx + cw - 6, cy + ch - 5), fill=(252, 253, 255, 245))
        d.ellipse((cx + cw // 3, cy + 3, cx + cw // 3 + 28, cy + 14), fill=(248, 250, 255, 210))

    # World-space windows (tile → px)
    # waterfall bowl ~ tiles 16–36 → px 256–576
    # ruins plateau ~ tiles 64–108 → px 1024–1728
    def in_waterfall(x: int) -> bool:
        return 256 <= x <= 576

    def in_ruins(x: int) -> bool:
        return 1024 <= x <= 1728

    peak_y = []
    for x in range(w):
        y = 56 + int(
            11 * math.sin(x * 0.008)
            + 7 * math.sin(x * 0.019 + 0.9)
            + 4 * math.sin(x * 0.041 + 0.3)
        )
        if in_waterfall(x) or in_ruins(x):
            y = 78 + int(2 * math.sin(x * 0.05))
        peak_y.append(y)

    for x, ytop in enumerate(peak_y):
        for y in range(ytop, min(h, ytop + 30)):
            depth = y - ytop
            rr = 115 + depth * 2
            gg = 140 + depth * 2
            bb = 180 + depth
            a = 255 if depth < 24 else max(0, 255 - (depth - 24) * 35)
            if a > 0:
                img.putpixel((x, y), (min(175, rr), min(195, gg), min(225, bb), a))
        if ytop < h - 1:
            img.putpixel((x, ytop), (90, 115, 155, 255))

    hill_y = []
    for x in range(w):
        y = 82 + int(
            9 * math.sin(x * 0.011 + 0.5)
            + 6 * math.sin(x * 0.027)
            + 3 * math.sin(x * 0.055 + 1.2)
        )
        if in_waterfall(x):
            y = 118 + int(3 * math.sin(x * 0.08))
        elif in_ruins(x):
            y = 102 + int(2 * math.sin(x * 0.06))
        hill_y.append(min(h - 4, y))

    for x, ytop in enumerate(hill_y):
        for y in range(ytop, h):
            depth = y - ytop
            shade = (x // 11 + y // 4) % 3
            rr = 46 + shade * 8 + depth
            gg = 108 + shade * 10 + depth // 2
            bb = 52 + shade * 4
            img.putpixel((x, y), (min(88, rr), min(158, gg), min(88, bb), 255))
        img.putpixel((x, ytop), (30, 74, 40, 255))
        if ytop + 1 < h:
            img.putpixel((x, ytop + 1), (38, 90, 48, 255))

    # Thin cliff lip only outside bowls
    for x, ytop in enumerate(hill_y):
        if in_waterfall(x):
            continue
        for dy in range(0, 3):
            yy = min(h - 1, ytop + 12 + dy + (x % 3))
            if yy > ytop + 6:
                img.putpixel((x, yy), (100, 85, 68, 220))

    # Sparse pines on green (skip bowls) — irregular spacing
    rng_x = list(range(24, w - 24, 1))
    placed = 0
    x = 30
    while x < w - 30:
        if in_waterfall(x) or in_ruins(x):
            x += 40
            continue
        if (x * 17 + placed * 31) % 7 == 0:
            x += 18
            continue
        y0 = hill_y[x] - 16 - (placed % 3) * 2
        d.polygon([(x, y0 + 18), (x + 6, y0), (x + 12, y0 + 18)], fill=(26, 64, 38, 240))
        d.polygon([(x + 2, y0 + 14), (x + 6, y0 + 2), (x + 10, y0 + 14)], fill=(34, 78, 46, 245))
        d.rectangle((x + 5, y0 + 17, x + 7, y0 + 22), fill=(68, 46, 30, 255))
        placed += 1
        x += 26 + (placed % 5) * 4

    out = PROC / "prop_skyline_wide.png"
    img.save(out)
    print("OK", out.name, w, h)


def hero_facade(name: str, roof: tuple, awn_a: tuple, awn_b: tuple, sign: tuple, wall: tuple) -> None:
    """Larger overview-readable storefront (overview silhouette)."""
    w, h = 140, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.polygon([(4, 34), (70, 2), (136, 34)], fill=roof)
    shade = tuple(max(0, c - 38) for c in roof[:3]) + (255,)
    d.polygon([(4, 34), (136, 34), (126, 46), (14, 46)], fill=shade)
    for yy in range(10, 34, 3):
        d.line([(22, yy), (118, yy)], fill=shade, width=1)
    d.rectangle((108, 10, 124, 36), fill=(110, 100, 94, 255))
    d.rectangle((106, 8, 126, 12), fill=(90, 82, 78, 255))
    d.ellipse((110, 0, 126, 12), fill=(230, 230, 235, 150))

    # Stone base
    d.rectangle((8, h - 20, w - 8, h - 4), fill=(128, 122, 114, 255))
    for sx in range(12, w - 12, 10):
        d.line([(sx, h - 20), (sx, h - 4)], fill=(98, 92, 85, 255))

    d.rectangle((12, 46, w - 12, h - 20), fill=wall)
    frame = (70, 50, 34, 255)
    d.rectangle((12, 46, w - 12, h - 20), outline=frame, width=2)
    for bx in range(18, w - 18, 7):
        d.line(
            [(bx, 48), (bx, h - 22)],
            fill=(max(0, wall[0] - 20), max(0, wall[1] - 20), max(0, wall[2] - 20), 255),
        )
    d.line([(w // 2, 46), (w // 2, h - 20)], fill=frame, width=2)

    # Deep awning
    for i, x0 in enumerate(range(16, 122, 12)):
        c = awn_a if i % 2 == 0 else awn_b
        d.rectangle((x0, 48, x0 + 11, 66), fill=c)
        d.pieslice((x0, 62, x0 + 11, 76), 0, 180, fill=c)
    d.line([(16, 48), (122, 48)], fill=(45, 35, 25, 255), width=2)

    # Big hanging sign (readable at overview)
    d.rectangle((48, 70, 92, 88), fill=(85, 58, 36, 255))
    d.rectangle((50, 72, 90, 86), fill=sign)
    d.line([(70, 66), (70, 70)], fill=(55, 40, 28, 255), width=2)

    for wx in (18, 100):
        d.rectangle((wx - 2, 72, wx + 22, 94), fill=(68, 52, 38, 255))
        d.rectangle((wx, 74, wx + 20, 92), fill=(155, 200, 235, 255))
        d.line([(wx + 10, 74), (wx + 10, 92)], fill=(105, 145, 170, 255))
        d.line([(wx, 83), (wx + 20, 83)], fill=(105, 145, 170, 255))
        d.rectangle((wx - 1, 92, wx + 21, 100), fill=(90, 65, 42, 255))
        d.ellipse((wx + 2, 90, wx + 10, 98), fill=(52, 115, 48, 255))
        d.ellipse((wx + 10, 89, wx + 18, 98), fill=(48, 105, 44, 255))
        for fx in (wx + 4, wx + 9, wx + 15):
            d.point((fx, 89), fill=(235, 70, 95, 255))

    d.rectangle((62, h - 48, 78, h - 20), fill=(98, 62, 40, 255))
    d.rectangle((72, h - 38, 74, h - 36), fill=(220, 190, 100, 255))
    d.rectangle((54, h - 20, 86, h - 12), fill=(112, 98, 82, 255))

    for px in (14, w - 32):
        d.rectangle((px, h - 34, px + 16, h - 20), fill=(58, 108, 46, 255))
        for fx in range(px + 2, px + 15, 3):
            d.point((fx, h - 36), fill=(240, 85, 105, 255))

    img.save(PROC / name)
    print("OK", name, w, h)


def bakery_block() -> None:
    """South-plaza bakery massing (ref has labeled bakery)."""
    w, h = 120, 110
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    roof = (150, 62, 48, 255)
    d.polygon([(6, 30), (60, 4), (114, 30)], fill=roof)
    shade = (110, 42, 32, 255)
    d.polygon([(6, 30), (114, 30), (106, 40), (14, 40)], fill=shade)
    d.rectangle((10, 40, w - 10, h - 6), fill=(228, 210, 185, 255))
    d.rectangle((10, 40, w - 10, h - 6), outline=(72, 52, 36, 255), width=2)
    d.rectangle((8, h - 14, w - 8, h - 4), fill=(125, 118, 110, 255))
    # Striped porch awning
    for i, x0 in enumerate(range(14, 104, 10)):
        c = (210, 60, 55, 255) if i % 2 == 0 else (245, 245, 245, 255)
        d.rectangle((x0, 42, x0 + 9, 56), fill=c)
        d.pieslice((x0, 52, x0 + 9, 64), 0, 180, fill=c)
    d.rectangle((34, 60, 86, 74), fill=(90, 65, 42, 255))
    d.rectangle((36, 62, 84, 72), fill=(245, 220, 150, 255))
    for wx in (16, 88):
        d.rectangle((wx, 62, wx + 16, 80), fill=(160, 205, 235, 255))
    d.rectangle((52, h - 36, 68, h - 14), fill=(100, 65, 42, 255))
    img.save(PROC / "prop_bakery.png")
    print("OK prop_bakery", w, h)


def main() -> None:
    seamless_skyline()
    hero_facade(
        "prop_shop_awning.png",
        (148, 58, 46, 255),
        (200, 55, 50, 255),
        (245, 245, 245, 255),
        (245, 220, 140, 255),
        (218, 198, 168, 255),
    )
    hero_facade(
        "prop_cafe_awning.png",
        (38, 110, 116, 255),
        (45, 145, 150, 255),
        (240, 248, 248, 255),
        (200, 235, 230, 255),
        (210, 200, 178, 255),
    )
    bakery_block()
    print("P69-P71 assets done")


if __name__ == "__main__":
    main()
