"""P73–P76: taller skyline, organic cliff/fall, readable signs, plaza fringe helpers."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"
WORLD_W = 192 * 16  # 3072
SKY_H = 200


def _draw_text(d: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: tuple) -> None:
    """Tiny pixel-ish label; fall back to default bitmap font."""
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    d.text(xy, text, fill=fill, font=font)


def seamless_skyline() -> None:
    w, h = WORLD_W, SKY_H
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Tall bright sky
    for y in range(0, 95):
        t = y / 94.0
        r = int(155 + 30 * t)
        g = int(200 + 28 * t)
        b = 248
        d.line([(0, y), (w - 1, y)], fill=(r, g, b, 255))

    clouds = [
        (30, 12, 90, 26),
        (160, 6, 110, 28),
        (310, 18, 80, 22),
        (450, 8, 100, 26),
        (620, 14, 88, 24),
        (780, 5, 120, 30),
        (980, 12, 92, 22),
        (1160, 7, 108, 28),
        (1380, 16, 86, 20),
        (1560, 6, 114, 28),
        (1780, 10, 96, 24),
        (2000, 14, 80, 20),
        (2180, 5, 130, 30),
        (2440, 12, 90, 22),
        (2680, 8, 110, 26),
        (2900, 15, 78, 18),
    ]
    for cx, cy, cw, ch in clouds:
        d.ellipse((cx, cy, cx + cw, cy + ch), fill=(255, 255, 255, 235))
        d.ellipse((cx + 14, cy - 6, cx + cw - 8, cy + ch - 6), fill=(252, 253, 255, 250))
        d.ellipse((cx + cw // 3, cy + 4, cx + cw // 3 + 32, cy + 16), fill=(245, 248, 255, 200))

    def bowl_depth(x: int) -> float:
        """0 = full hills, 1 = deep bowl. Soft edges (no hard seam)."""
        # waterfall bowl ~ tiles 16–36 → px 256–576
        wf = _smooth_window(x, 240, 592, 48)
        # ruins ~ tiles 64–108 → px 1024–1728
        ru = _smooth_window(x, 1000, 1760, 56) * 0.55
        return max(wf, ru)

    peak_y = []
    for x in range(w):
        y = 78 + int(
            12 * math.sin(x * 0.0075)
            + 8 * math.sin(x * 0.018 + 0.7)
            + 4 * math.sin(x * 0.038)
        )
        bd = bowl_depth(x)
        y = int(y + bd * 28)
        peak_y.append(y)

    for x, ytop in enumerate(peak_y):
        for y in range(ytop, min(h, ytop + 34)):
            depth = y - ytop
            rr = 110 + depth * 2
            gg = 138 + depth * 2
            bb = 178 + depth
            a = 255 if depth < 26 else max(0, 255 - (depth - 26) * 30)
            if a > 0:
                img.putpixel((x, y), (min(170, rr), min(190, gg), min(220, bb), a))
        if ytop < h - 1:
            img.putpixel((x, ytop), (88, 112, 150, 255))

    hill_y = []
    for x in range(w):
        y = 110 + int(
            10 * math.sin(x * 0.01 + 0.4)
            + 6 * math.sin(x * 0.025)
            + 3 * math.sin(x * 0.05 + 1.1)
        )
        bd = bowl_depth(x)
        y = int(y + bd * 55)
        hill_y.append(min(h - 3, y))

    for x, ytop in enumerate(hill_y):
        for y in range(ytop, h):
            depth = y - ytop
            shade = (x // 13 + y // 4) % 3
            rr = 44 + shade * 8 + depth
            gg = 105 + shade * 11 + depth // 2
            bb = 50 + shade * 4
            img.putpixel((x, y), (min(86, rr), min(155, gg), min(86, bb), 255))
        img.putpixel((x, ytop), (28, 70, 38, 255))

    # Sparse pines outside deep bowls
    x = 28
    placed = 0
    while x < w - 28:
        if bowl_depth(x) > 0.45:
            x += 36
            continue
        if (x * 13 + placed * 29) % 5 == 0:
            x += 20
            continue
        y0 = hill_y[x] - 18 - (placed % 3) * 2
        d.polygon([(x, y0 + 20), (x + 7, y0), (x + 14, y0 + 20)], fill=(24, 62, 36, 240))
        d.polygon([(x + 3, y0 + 15), (x + 7, y0 + 2), (x + 11, y0 + 15)], fill=(32, 76, 44, 245))
        d.rectangle((x + 6, y0 + 19, x + 8, y0 + 24), fill=(66, 44, 28, 255))
        placed += 1
        x += 28 + (placed % 4) * 5

    img.save(PROC / "prop_skyline_wide.png")
    print("OK prop_skyline_wide", w, h)


def _smooth_window(x: int, a: int, b: int, feather: int) -> float:
    if a <= x <= b:
        return 1.0
    if a - feather <= x < a:
        t = (x - (a - feather)) / float(feather)
        return t * t * (3 - 2 * t)
    if b < x <= b + feather:
        t = ((b + feather) - x) / float(feather)
        return t * t * (3 - 2 * t)
    return 0.0


def organic_cliff() -> None:
    """Irregular rock face — not brick stack."""
    w, h = 48, 64
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            # jagged silhouette
            edge = 6 + int(4 * math.sin(y * 0.22 + x * 0.05) + 3 * math.sin(y * 0.11))
            if x < edge or x > w - edge - 1:
                continue
            depth = y / float(h)
            n = ((x * 17 + y * 31) ^ (x * y)) & 7
            rr = 95 + int(depth * 35) + n
            gg = 90 + int(depth * 25) + n // 2
            bb = 82 + int(depth * 18)
            # moss flecks
            if n == 1 and y > 20:
                rr, gg, bb = 55, 95, 50
            img.putpixel((x, y), (min(150, rr), min(130, gg), min(120, bb), 255))
    # darker lip
    d = ImageDraw.Draw(img)
    for x in range(8, w - 8):
        yy = 4 + (x % 5)
        img.putpixel((x, yy), (70, 68, 62, 255))
    img.save(PROC / "prop_cliff.png")
    print("OK prop_cliff", w, h)


def organic_waterfall() -> None:
    w, h = 64, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # cliff bowl behind
    for y in range(0, 28):
        for x in range(8, w - 8):
            n = (x + y * 3) % 5
            img.putpixel((x, y), (90 + n * 4, 88 + n * 3, 80 + n * 2, 255))
    # falls strands
    for i, x0 in enumerate(range(14, 50, 5)):
        wob = int(2 * math.sin(i * 1.3))
        d.rectangle((x0 + wob, 18, x0 + 4 + wob, h - 12), fill=(170, 210, 245, 220))
        d.rectangle((x0 + 1 + wob, 20, x0 + 3 + wob, h - 14), fill=(210, 235, 255, 240))
    # mist base
    d.ellipse((10, h - 28, w - 10, h - 4), fill=(230, 240, 255, 160))
    d.ellipse((18, h - 22, w - 18, h - 8), fill=(245, 250, 255, 190))
    # foam
    for fx, fy in [(20, h - 18), (28, h - 16), (36, h - 19), (44, h - 17)]:
        d.ellipse((fx, fy, fx + 6, fy + 4), fill=(255, 255, 255, 230))
    img.save(PROC / "prop_waterfall.png")
    print("OK prop_waterfall", w, h)


def hero_facade(name: str, roof: tuple, awn_a: tuple, awn_b: tuple, sign_bg: tuple, wall: tuple, label: str) -> None:
    w, h = 140, 128
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(4, 34), (70, 2), (136, 34)], fill=roof)
    shade = tuple(max(0, c - 38) for c in roof[:3]) + (255,)
    d.polygon([(4, 34), (136, 34), (126, 46), (14, 46)], fill=shade)
    for yy in range(10, 34, 3):
        d.line([(22, yy), (118, yy)], fill=shade, width=1)
    d.rectangle((108, 10, 124, 36), fill=(110, 100, 94, 255))
    d.ellipse((110, 0, 126, 12), fill=(230, 230, 235, 150))
    d.rectangle((8, h - 20, w - 8, h - 4), fill=(128, 122, 114, 255))
    d.rectangle((12, 46, w - 12, h - 20), fill=wall)
    frame = (70, 50, 34, 255)
    d.rectangle((12, 46, w - 12, h - 20), outline=frame, width=2)
    for bx in range(18, w - 18, 7):
        d.line([(bx, 48), (bx, h - 22)], fill=(max(0, wall[0] - 20), max(0, wall[1] - 20), max(0, wall[2] - 20), 255))
    for i, x0 in enumerate(range(16, 122, 12)):
        c = awn_a if i % 2 == 0 else awn_b
        d.rectangle((x0, 48, x0 + 11, 66), fill=c)
        d.pieslice((x0, 62, x0 + 11, 76), 0, 180, fill=c)
    # Readable sign
    d.rectangle((40, 70, 100, 92), fill=(85, 58, 36, 255))
    d.rectangle((42, 72, 98, 90), fill=sign_bg)
    _draw_text(d, (48, 76), label, (40, 30, 20, 255))
    for wx in (18, 100):
        d.rectangle((wx - 2, 74, wx + 22, 96), fill=(68, 52, 38, 255))
        d.rectangle((wx, 76, wx + 20, 94), fill=(155, 200, 235, 255))
        d.line([(wx + 10, 76), (wx + 10, 94)], fill=(105, 145, 170, 255))
        d.rectangle((wx - 1, 94, wx + 21, 102), fill=(90, 65, 42, 255))
        d.ellipse((wx + 2, 92, wx + 18, 100), fill=(50, 110, 45, 255))
    d.rectangle((62, h - 48, 78, h - 20), fill=(98, 62, 40, 255))
    d.rectangle((72, h - 38, 74, h - 36), fill=(220, 190, 100, 255))
    img.save(PROC / name)
    print("OK", name, label)


def bakery() -> None:
    w, h = 120, 110
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    roof = (150, 62, 48, 255)
    d.polygon([(6, 30), (60, 4), (114, 30)], fill=roof)
    d.polygon([(6, 30), (114, 30), (106, 40), (14, 40)], fill=(110, 42, 32, 255))
    d.rectangle((10, 40, w - 10, h - 6), fill=(228, 210, 185, 255))
    d.rectangle((10, 40, w - 10, h - 6), outline=(72, 52, 36, 255), width=2)
    d.rectangle((8, h - 14, w - 8, h - 4), fill=(125, 118, 110, 255))
    for i, x0 in enumerate(range(14, 104, 10)):
        c = (210, 60, 55, 255) if i % 2 == 0 else (245, 245, 245, 255)
        d.rectangle((x0, 42, x0 + 9, 56), fill=c)
        d.pieslice((x0, 52, x0 + 9, 64), 0, 180, fill=c)
    d.rectangle((28, 60, 92, 78), fill=(90, 65, 42, 255))
    d.rectangle((30, 62, 90, 76), fill=(245, 220, 150, 255))
    _draw_text(d, (38, 64), "BAKERY", (70, 40, 20, 255))
    for wx in (16, 88):
        d.rectangle((wx, 64, wx + 16, 82), fill=(160, 205, 235, 255))
    d.rectangle((52, h - 36, 68, h - 14), fill=(100, 65, 42, 255))
    img.save(PROC / "prop_bakery.png")
    print("OK prop_bakery")


def main() -> None:
    seamless_skyline()
    organic_cliff()
    organic_waterfall()
    hero_facade(
        "prop_shop_awning.png",
        (148, 58, 46, 255),
        (200, 55, 50, 255),
        (245, 245, 245, 255),
        (245, 220, 140, 255),
        (218, 198, 168, 255),
        "SHOP",
    )
    hero_facade(
        "prop_cafe_awning.png",
        (38, 110, 116, 255),
        (45, 145, 150, 255),
        (240, 248, 248, 255),
        (200, 235, 230, 255),
        (210, 200, 178, 255),
        "CAFE",
    )
    bakery()
    print("P73-P76 assets done")


if __name__ == "__main__":
    main()
