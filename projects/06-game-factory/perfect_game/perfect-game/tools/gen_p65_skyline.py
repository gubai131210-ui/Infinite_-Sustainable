"""P65–P67: ref-aligned skyline (sky→blue peaks→green hills), richer facades, path edge props."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"


def skyline() -> None:
    """Match overview ref: tall pale sky, fluffy clouds, soft blue peaks, green hills.
    Grey rock is only a thin cliff lip — not the main silhouette.
    Waterfall (x~60-110) and ruins (x~175-230) windows keep sky open.
    """
    w, h = 384, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Tall pale-blue sky (ref: light strip above map)
    for y in range(0, 48):
        t = y / 47.0
        r = int(140 + 40 * t)
        g = int(185 + 35 * t)
        b = int(235 + 15 * t)
        d.line([(0, y), (w - 1, y)], fill=(r, g, b, 250))

    # Fluffy white clouds (soft blobs, not hard rings)
    for cx, cy, cw, ch in [
        (18, 8, 54, 18),
        (90, 4, 62, 20),
        (168, 10, 50, 16),
        (240, 6, 58, 18),
        (310, 9, 48, 16),
        (130, 14, 36, 12),
    ]:
        d.ellipse((cx, cy, cx + cw, cy + ch), fill=(255, 255, 255, 235))
        d.ellipse((cx + 10, cy - 4, cx + cw - 4, cy + ch - 4), fill=(252, 253, 255, 245))
        d.ellipse((cx + cw // 3, cy + 2, cx + cw // 3 + 22, cy + 12), fill=(248, 250, 255, 220))

    # Soft blue distant peaks (behind green hills)
    peak_y = []
    for x in range(w):
        y = 38 + int(
            10 * math.sin(x * 0.022)
            + 6 * math.sin(x * 0.055 + 1.2)
            + 3 * math.sin(x * 0.11)
        )
        # Open windows for waterfall / ruins
        if 55 <= x <= 115 or 170 <= x <= 235:
            y = 52 + int(2 * math.sin(x * 0.1))
        peak_y.append(y)

    for x, ytop in enumerate(peak_y):
        for y in range(ytop, min(h, ytop + 28)):
            depth = y - ytop
            # Cool blue-grey mountain (ref distant peaks)
            rr = 120 + depth * 2
            gg = 145 + depth * 2
            bb = 185 + depth
            a = 255 if depth < 22 else max(0, 255 - (depth - 22) * 40)
            if a > 0:
                img.putpixel((x, y), (min(180, rr), min(200, gg), min(230, bb), a))
        if ytop < h - 1:
            img.putpixel((x, ytop), (95, 120, 160, 255))

    # Green rolling hills (main near silhouette — ref look)
    hill_y = []
    for x in range(w):
        y = 58 + int(
            8 * math.sin(x * 0.031 + 0.4)
            + 5 * math.sin(x * 0.07)
            + 3 * math.sin(x * 0.14 + 1.5)
        )
        if 55 <= x <= 115:
            y = 72 + int(2 * math.sin(x * 0.15))  # waterfall bowl
        elif 170 <= x <= 235:
            y = 70 + int(2 * math.sin(x * 0.12))  # ruins plateau gap
        hill_y.append(y)

    for x, ytop in enumerate(hill_y):
        for y in range(ytop, h):
            depth = y - ytop
            # Lush green with slight shade bands
            shade = (x // 7 + y // 3) % 3
            rr = 48 + shade * 8 + depth
            gg = 110 + shade * 10 + depth // 2
            bb = 55 + shade * 4
            img.putpixel((x, y), (min(90, rr), min(160, gg), min(90, bb), 255))
        # Darker crown lip
        img.putpixel((x, ytop), (32, 78, 42, 255))
        if ytop + 1 < h:
            img.putpixel((x, ytop + 1), (40, 95, 50, 255))

    # Thin brown cliff lip only at hill base (not grey wall)
    for x, ytop in enumerate(hill_y):
        for dy in range(0, 4):
            yy = min(h - 1, ytop + 14 + dy + (x % 3))
            if yy > ytop + 8:
                img.putpixel((x, yy), (105, 88, 70, 230))

    # Sparse pine crowns on high green (never solid wall; skip windows)
    for i, x0 in enumerate(range(10, w - 12, 28)):
        if 55 <= x0 <= 115 or 170 <= x0 <= 235:
            continue
        if i % 4 == 2:
            continue
        y0 = hill_y[x0] - 14 - (i % 3) * 2
        d.polygon(
            [(x0, y0 + 16), (x0 + 5, y0), (x0 + 10, y0 + 16)],
            fill=(28, 68, 40, 240),
        )
        d.polygon(
            [(x0 + 2, y0 + 12), (x0 + 5, y0 + 2), (x0 + 8, y0 + 12)],
            fill=(36, 82, 48, 245),
        )
        d.rectangle((x0 + 4, y0 + 15, x0 + 6, y0 + 20), fill=(70, 48, 32, 255))

    img.save(PROC / "prop_ridge_organic.png")
    print("OK prop_ridge_organic", w, h)


def path_edge_props() -> None:
    """Tuft + pebble variants for organic path edges."""
    # Dense grass tuft
    img = Image.new("RGBA", (16, 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((1, 5, 8, 11), fill=(62, 125, 48, 255))
    d.ellipse((5, 4, 13, 11), fill=(52, 112, 42, 255))
    d.ellipse((7, 6, 14, 11), fill=(70, 135, 55, 255))
    for fx, fy, c in [(3, 3, (230, 80, 90)), (8, 2, (245, 205, 70)), (11, 4, (210, 70, 150)), (6, 3, (255, 255, 255))]:
        d.point((fx, fy), fill=c + (255,))
    img.save(PROC / "prop_path_tuft.png")
    print("OK prop_path_tuft")

    # Pebble scatter for dirt fringe
    peb = Image.new("RGBA", (12, 8), (0, 0, 0, 0))
    pd = ImageDraw.Draw(peb)
    for ox, oy, c in [(1, 3, (150, 130, 100)), (4, 2, (120, 110, 95)), (7, 4, (165, 145, 115)), (9, 2, (130, 120, 100))]:
        pd.ellipse((ox, oy, ox + 3, oy + 2), fill=c + (255,))
    peb.save(PROC / "prop_path_pebble.png")
    print("OK prop_path_pebble")


def storefront(name: str, roof: tuple, awn_a: tuple, awn_b: tuple, sign_fill: tuple, wall: tuple) -> None:
    """Deeper hand-drawn-ish facade: stone base, timber siding, flower boxes, porch."""
    w, h = 112, 104
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Roof gable + eave depth + shingle lines
    d.polygon([(2, 28), (56, 2), (110, 28)], fill=roof)
    shade = tuple(max(0, c - 36) for c in roof[:3]) + (255,)
    d.polygon([(2, 28), (110, 28), (102, 38), (10, 38)], fill=shade)
    for yy in range(10, 28, 3):
        d.line([(18, yy), (94, yy)], fill=shade, width=1)
    # Chimney
    d.rectangle((84, 8, 98, 30), fill=(108, 98, 92, 255))
    d.rectangle((82, 6, 100, 10), fill=(90, 82, 78, 255))
    d.ellipse((86, 0, 100, 10), fill=(230, 230, 235, 150))

    # Stone foundation
    d.rectangle((8, h - 18, w - 8, h - 4), fill=(130, 125, 118, 255))
    for sx in range(10, w - 10, 8):
        d.line([(sx, h - 18), (sx, h - 4)], fill=(100, 95, 88, 255))

    # Timber wall with vertical boards
    d.rectangle((10, 38, w - 10, h - 18), fill=wall)
    frame = (72, 52, 36, 255)
    d.rectangle((10, 38, w - 10, h - 18), outline=frame, width=2)
    for bx in range(14, w - 14, 6):
        d.line([(bx, 40), (bx, h - 20)], fill=(max(0, wall[0] - 18), max(0, wall[1] - 18), max(0, wall[2] - 18), 255))
    d.line([(w // 2, 38), (w // 2, h - 18)], fill=frame, width=2)
    d.line([(10, 56), (w - 10, 56)], fill=frame, width=1)

    # Deep scalloped awning
    for i, x0 in enumerate(range(14, 98, 10)):
        c = awn_a if i % 2 == 0 else awn_b
        d.rectangle((x0, 40, x0 + 9, 56), fill=c)
        d.pieslice((x0, 52, x0 + 9, 64), 0, 180, fill=c)
    d.line([(14, 40), (98, 40)], fill=(50, 40, 30, 255), width=2)

    # Hanging sign
    d.rectangle((44, 58, 68, 72), fill=(88, 62, 40, 255))
    d.rectangle((46, 60, 66, 70), fill=sign_fill)
    d.line([(56, 56), (56, 58)], fill=(60, 45, 30, 255))

    # Display windows with panes + sill flower boxes
    for wx in (16, 78):
        d.rectangle((wx - 2, 60, wx + 18, 78), fill=(70, 55, 40, 255))
        d.rectangle((wx, 62, wx + 16, 76), fill=(160, 205, 235, 255))
        d.line([(wx + 8, 62), (wx + 8, 76)], fill=(110, 150, 175, 255))
        d.line([(wx, 69), (wx + 16, 69)], fill=(110, 150, 175, 255))
        # Flower box
        d.rectangle((wx - 1, 76, wx + 17, 82), fill=(95, 70, 45, 255))
        d.ellipse((wx + 2, 74, wx + 8, 80), fill=(55, 120, 50, 255))
        d.ellipse((wx + 8, 73, wx + 15, 80), fill=(50, 110, 45, 255))
        for fx in (wx + 3, wx + 7, wx + 12):
            d.point((fx, 73), fill=(235, 70, 90, 255))

    # Door + porch step
    d.rectangle((50, h - 40, 62, h - 18), fill=(100, 65, 42, 255))
    d.rectangle((58, h - 32, 60, h - 30), fill=(220, 190, 100, 255))
    d.rectangle((44, h - 18, 68, h - 12), fill=(115, 100, 85, 255))

    # Side planters
    for px in (12, w - 28):
        d.rectangle((px, h - 28, px + 14, h - 18), fill=(60, 110, 48, 255))
        for fx in range(px + 2, px + 13, 3):
            d.point((fx, h - 30), fill=(240, 90, 110, 255))

    img.save(PROC / name)
    print("OK", name)


def house(name: str, wall: tuple, roof: tuple, accent: tuple) -> None:
    w, h = 84, 92
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(4, 28), (w // 2, 2), (w - 4, 28)], fill=roof)
    shade = tuple(max(0, c - 30) for c in roof[:3]) + (255,)
    d.polygon([(4, 28), (w - 4, 28), (w - 10, 36), (10, 36)], fill=shade)
    for yy in range(8, 28, 3):
        d.line([(12, yy), (w - 12, yy)], fill=shade, width=1)
    d.rectangle((w // 2 + 12, 8, w // 2 + 22, 30), fill=(108, 98, 92, 255))
    d.ellipse((w // 2 + 13, 1, w // 2 + 24, 10), fill=(230, 230, 235, 155))
    # Stone base
    d.rectangle((10, h - 12, w - 10, h - 4), fill=(128, 122, 115, 255))
    d.rectangle((10, 36, w - 10, h - 12), fill=wall)
    frame = (68, 52, 38, 255)
    d.rectangle((10, 36, w - 10, h - 12), outline=frame, width=2)
    for bx in range(14, w - 14, 5):
        d.line([(bx, 38), (bx, h - 14)], fill=(max(0, wall[0] - 14), max(0, wall[1] - 14), max(0, wall[2] - 14), 255))
    d.line([(w // 2, 36), (w // 2, h - 12)], fill=frame, width=2)
    for wx in (16, w - 30):
        d.rectangle((wx - 2, 42, wx + 14, 54), fill=(90, 70, 50, 255))
        d.rectangle((wx, 44, wx + 12, 52), fill=(185, 215, 235, 255))
        d.rectangle((wx - 1, 54, wx + 13, 58), fill=(70, 115, 55, 255))
    d.rectangle((w // 2 - 7, h - 30, w // 2 + 7, h - 12), fill=accent)
    img.save(PROC / name)
    print("OK", name)


def main() -> None:
    skyline()
    path_edge_props()
    house("prop_house_redroof.png", (222, 200, 172, 255), (168, 68, 52, 255), (115, 55, 38, 255))
    house("prop_house_slateroof.png", (198, 204, 210, 255), (70, 88, 112, 255), (55, 65, 85, 255))
    house("prop_house_thatch.png", (218, 198, 158, 255), (145, 122, 68, 255), (100, 78, 42, 255))
    house("prop_house_greenroof.png", (200, 208, 180, 255), (62, 118, 78, 255), (50, 88, 58, 255))
    storefront(
        "prop_shop_awning.png",
        (148, 58, 46, 255),
        (200, 55, 50, 255),
        (245, 245, 245, 255),
        (245, 220, 140, 255),
        (218, 198, 168, 255),
    )
    storefront(
        "prop_cafe_awning.png",
        (38, 110, 116, 255),
        (45, 145, 150, 255),
        (240, 248, 248, 255),
        (200, 235, 230, 255),
        (210, 200, 178, 255),
    )
    print("P65-P67 assets done")


if __name__ == "__main__":
    main()
