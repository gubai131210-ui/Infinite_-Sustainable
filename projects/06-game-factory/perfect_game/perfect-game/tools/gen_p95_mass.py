"""P95–P97: mass pine canopy, deeper fall bowl, readable pines, hero facades."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"
WORLD_W = 192 * 16


def _font():
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def pine_canopy() -> None:
    """Hand-mass style canopy: overlapping dark blobs + soft underside, not hatched triangles."""
    w, h = WORLD_W, 112
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def in_wf(x: int) -> bool:
        return 288 <= x <= 520

    # Far cool band (lighter)
    for x in range(0, w, 18):
        if in_wf(x):
            continue
        cx = x + 20
        cy = 28 + (x // 40) % 8
        d.ellipse((cx - 36, cy - 18, cx + 40, cy + 22), fill=(40, 85, 52, 200))
        d.ellipse((cx - 20, cy - 28, cx + 24, cy + 8), fill=(48, 98, 58, 210))

    # Mid dark mass
    for x in range(0, w, 14):
        if in_wf(x):
            continue
        cx = x + 10
        cy = 48 + (x // 30) % 10
        d.ellipse((cx - 42, cy - 16, cx + 46, cy + 28), fill=(22, 58, 34, 235))
        d.ellipse((cx - 28, cy - 30, cx + 30, cy + 10), fill=(28, 68, 40, 240))
        # soft underside shadow
        d.ellipse((cx - 30, cy + 10, cx + 32, cy + 26), fill=(12, 32, 20, 120))

    # Near jagged dark tips (readable pine points on mass)
    for x in range(4, w - 4, 11):
        if in_wf(x):
            continue
        base = h - 6
        tip = base - (34 + (x * 7) % 18)
        half = 8 + (x % 5)
        d.polygon([(x, tip), (x - half, base), (x + half, base)], fill=(18, 48, 28, 250))
        d.polygon(
            [(x, tip + 8), (x - half + 2, base - 4), (x + half - 2, base - 4)],
            fill=(30, 72, 42, 245),
        )

    # Extra dark clumps near waterfall edges (amphitheater flanks)
    for cx in (250, 560):
        d.ellipse((cx - 50, 40, cx + 50, 100), fill=(16, 44, 26, 245))
        d.ellipse((cx - 30, 20, cx + 34, 70), fill=(24, 60, 36, 250))

    img.save(PROC / "prop_pine_canopy.png")
    print("OK prop_pine_canopy", w, h)


def pine_variants() -> None:
    specs = [
        ("tree_pine_b.png", (26, 70, 40), 0.0),
        ("tree_pine_c.png", (34, 78, 44), 0.15),
    ]
    for name, base, lean in specs:
        tw, th = 48, 64
        img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx = int(24 + lean * 8)
        layers = [(6, 44, 14), (14, 34, 11), (22, 24, 8), (28, 16, 6)]
        for top, hh, half in layers:
            c = (base[0], base[1], base[2], 250)
            d.polygon([(cx, top), (cx - half, top + hh), (cx + half, top + hh)], fill=c)
            # highlight edge
            d.line([(cx, top), (cx + half - 1, top + hh - 2)], fill=(base[0] + 30, base[1] + 35, base[2] + 20, 200))
        d.rectangle((cx - 2, 52, cx + 2, 62), fill=(72, 48, 30, 255))
        img.save(PROC / name)
        print("OK", name, tw, th)


def waterfall_bowl() -> None:
    w, h = 144, 160
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Cliff shelves (3 terraces)
    for shelf_y, shelf_h, inset in [(0, 36, 8), (28, 28, 14), (48, 24, 20)]:
        for y in range(shelf_y, shelf_y + shelf_h):
            for x in range(inset, w - inset):
                dx = x - w // 2
                if abs(dx) > (w // 2 - inset - (y - shelf_y) // 3):
                    continue
                n = (x * 13 + y * 17) & 7
                rr = 70 + n * 3 + (y - shelf_y)
                gg = 68 + n * 2
                bb = 62 + n
                if n == 2:
                    rr, gg, bb = 45, 82, 42
                img.putpixel((x, y), (min(125, rr), min(110, gg), min(100, bb), 255))
    # Sky notch
    for y in range(0, 20):
        for x in range(52, 92):
            img.putpixel((x, y), (0, 0, 0, 0))
    # Falls
    for i, x0 in enumerate(range(50, 94, 5)):
        wob = int(2 * math.sin(i * 0.8))
        d.rectangle((x0 + wob, 36, x0 + 6 + wob, h - 48), fill=(145, 195, 235, 210))
        d.rectangle((x0 + 2 + wob, 38, x0 + 5 + wob, h - 50), fill=(200, 228, 255, 235))
    # Pool
    for y in range(h - 52, h - 10):
        for x in range(40, 104):
            dx, dy = x - 72, y - (h - 32)
            if dx * dx * 0.75 + dy * dy * 1.5 < 520:
                depth = abs(dy)
                img.putpixel((x, y), (60 + depth, 145 + depth // 2, 185 + depth // 3, 255))
    # Foam + mist
    d.ellipse((36, h - 56, w - 36, h - 16), fill=(230, 240, 255, 130))
    for fx, fy in [(48, h - 40), (60, h - 36), (72, h - 38), (84, h - 36), (68, h - 28)]:
        d.ellipse((fx, fy, fx + 12, fy + 7), fill=(255, 255, 255, 230))
    for rx in (42, 56, 72, 88, 98):
        d.ellipse((rx, h - 26, rx + 14, h - 14), fill=(92, 86, 78, 255))
    img.save(PROC / "prop_waterfall_bowl.png")
    print("OK prop_waterfall_bowl", w, h)


def facade(name: str, roof: tuple, awn_a: tuple, awn_b: tuple, sign_bg: tuple, wall: tuple, label: str) -> None:
    w, h = 152, 136
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(4, 36), (76, 2), (148, 36)], fill=roof)
    shade = tuple(max(0, c - 40) for c in roof[:3]) + (255,)
    d.polygon([(4, 36), (148, 36), (138, 48), (14, 48)], fill=shade)
    for yy in range(10, 36, 3):
        d.line([(24, yy), (128, yy)], fill=shade, width=1)
    d.rectangle((118, 10, 136, 38), fill=(110, 100, 94, 255))
    d.ellipse((120, 0, 138, 14), fill=(230, 230, 235, 150))
    d.rectangle((8, h - 22, w - 8, h - 4), fill=(128, 122, 114, 255))
    d.rectangle((12, 48, w - 12, h - 22), fill=wall)
    d.rectangle((12, 48, w - 12, h - 22), outline=(70, 50, 34, 255), width=2)
    for bx in range(18, w - 18, 7):
        d.line([(bx, 50), (bx, h - 24)], fill=(max(0, wall[0] - 22), max(0, wall[1] - 22), max(0, wall[2] - 22), 255))
    for i, x0 in enumerate(range(16, 132, 12)):
        c = awn_a if i % 2 == 0 else awn_b
        d.rectangle((x0, 50, x0 + 11, 70), fill=c)
        d.pieslice((x0, 66, x0 + 11, 80), 0, 180, fill=c)
    # Big readable sign
    d.rectangle((36, 74, 116, 100), fill=(80, 55, 34, 255))
    d.rectangle((40, 78, 112, 96), fill=sign_bg)
    d.text((48, 82), label, fill=(35, 25, 18, 255), font=_font())
    for wx in (16, 112):
        d.rectangle((wx, 78, wx + 24, 102), fill=(155, 200, 235, 255))
        d.line([(wx + 12, 78), (wx + 12, 102)], fill=(100, 145, 170, 255))
        d.rectangle((wx - 1, 102, wx + 25, 110), fill=(55, 115, 48, 255))
    d.rectangle((68, h - 52, 84, h - 22), fill=(95, 60, 40, 255))
    d.rectangle((78, h - 42, 80, h - 40), fill=(220, 190, 100, 255))
    img.save(PROC / name)
    print("OK", name, label)


def bakery() -> None:
    w, h = 128, 118
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(6, 32), (64, 2), (122, 32)], fill=(150, 62, 48, 255))
    d.polygon([(6, 32), (122, 32), (114, 42), (14, 42)], fill=(110, 42, 32, 255))
    d.rectangle((10, 42, w - 10, h - 6), fill=(228, 210, 185, 255))
    d.rectangle((10, 42, w - 10, h - 6), outline=(72, 52, 36, 255), width=2)
    d.rectangle((8, h - 16, w - 8, h - 4), fill=(125, 118, 110, 255))
    for i, x0 in enumerate(range(14, 110, 10)):
        c = (210, 60, 55, 255) if i % 2 == 0 else (245, 245, 245, 255)
        d.rectangle((x0, 44, x0 + 9, 58), fill=c)
        d.pieslice((x0, 54, x0 + 9, 66), 0, 180, fill=c)
    d.rectangle((24, 62, 104, 86), fill=(85, 58, 36, 255))
    d.rectangle((28, 66, 100, 82), fill=(245, 220, 150, 255))
    d.text((36, 68), "BAKERY", fill=(70, 40, 20, 255), font=_font())
    d.rectangle((54, h - 40, 74, h - 16), fill=(100, 65, 42, 255))
    img.save(PROC / "prop_bakery.png")
    print("OK prop_bakery")


def main() -> None:
    pine_canopy()
    pine_variants()
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
    print("P95-P97 assets done")


if __name__ == "__main__":
    main()
