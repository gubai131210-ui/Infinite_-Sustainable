"""Rich master tileset — varied grass/path/water/cliff for video-like density."""
from __future__ import annotations

from pathlib import Path
import math
import random

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "tiles"
QA = ROOT / "assets" / "qa"
TS = 16
rng = random.Random(42)


def save(img: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    img.save(OUT / name)
    board = Image.new("RGBA", img.size)
    for y in range(img.height):
        for x in range(img.width):
            board.putpixel(
                (x, y),
                (220, 220, 220, 255) if ((x // 8) + (y // 8)) % 2 == 0 else (160, 160, 160, 255),
            )
    board.alpha_composite(img)
    board.convert("RGB").save(QA / f"checker_{name}", quality=92)
    print("OK", name, img.size)


def px(img, x, y, c):
    if 0 <= x < TS and 0 <= y < TS:
        img.putpixel((x, y), c)


def fill(img, c):
    ImageDraw.Draw(img).rectangle([0, 0, TS - 1, TS - 1], fill=c)


def grass(variant: int = 0) -> Image.Image:
    """Oil-meadow grass — near-identical bases so overview zoom never reads as a checkerboard."""
    # Very close hues; variation comes from soft blobs, not tile-to-tile base jumps
    bases = [(76, 148, 64), (78, 150, 66), (74, 146, 62), (77, 149, 65)]
    b = bases[variant % 4]
    img = Image.new("RGBA", (TS, TS), (*b, 255))
    # Large soft blobs (same family across variants)
    for _ in range(6):
        cx, cy = rng.randrange(TS), rng.randrange(TS)
        rad = rng.randrange(4, 8)
        tint = (
            max(0, min(255, b[0] + rng.randrange(-10, 12))),
            max(0, min(255, b[1] + rng.randrange(-8, 14))),
            max(0, min(255, b[2] + rng.randrange(-6, 10))),
            255,
        )
        for yy in range(TS):
            for xx in range(TS):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= rad * rad and rng.random() > 0.2:
                    px(img, xx, yy, tint)
    # Fine low-contrast dither
    for _ in range(22):
        x, y = rng.randrange(TS), rng.randrange(TS)
        bright = (min(255, b[0] + 8), min(255, b[1] + 10), min(255, b[2] + 6), 255)
        dark = (max(0, b[0] - 8), max(0, b[1] - 9), max(0, b[2] - 6), 255)
        px(img, x, y, bright if rng.random() > 0.5 else dark)
    # Sparse blades only (flowers rarer — avoid pepper grid at zoom-out)
    for _ in range(3):
        x, y = rng.randrange(1, 14), rng.randrange(2, 14)
        px(img, x, y, (58, 124, 48, 255))
        px(img, x, y - 1, (98, 168, 82, 255))
    if variant == 0 and rng.random() > 0.7:
        fx, fy = rng.randrange(2, 14), rng.randrange(2, 14)
        px(img, fx, fy, (220, 96, 124, 255) if rng.random() > 0.5 else (236, 214, 96, 255))
    return img


def path() -> Image.Image:
    """Organic dirt path — mottled, no hard brick borders."""
    img = Image.new("RGBA", (TS, TS), (176, 148, 98, 255))
    for _ in range(48):
        x, y = rng.randrange(TS), rng.randrange(TS)
        choice = rng.randrange(4)
        if choice == 0:
            px(img, x, y, (150, 122, 78, 255))
        elif choice == 1:
            px(img, x, y, (195, 168, 118, 255))
        elif choice == 2:
            px(img, x, y, (138, 110, 70, 255))
        else:
            px(img, x, y, (168, 140, 92, 255))
    # Soft pebble nubs (not full edge lines)
    for _ in range(4):
        x, y = rng.randrange(2, 14), rng.randrange(2, 14)
        px(img, x, y, (120, 100, 70, 255))
        px(img, x + 1, y, (130, 108, 76, 255))
    return img


def plaza() -> Image.Image:
    """Worn cobble plaza — irregular stones, no 8px brick grid."""
    img = Image.new("RGBA", (TS, TS), (152, 146, 138, 255))
    # Irregular cobble patches instead of crosshair grid
    for _ in range(10):
        cx, cy = rng.randrange(1, 14), rng.randrange(1, 14)
        w = rng.randrange(2, 5)
        h = rng.randrange(2, 4)
        shade = (
            140 + rng.randrange(0, 30),
            134 + rng.randrange(0, 28),
            126 + rng.randrange(0, 26),
            255,
        )
        for yy in range(cy, min(TS, cy + h)):
            for xx in range(cx, min(TS, cx + w)):
                if rng.random() > 0.15:
                    px(img, xx, yy, shade)
    for _ in range(8):
        x, y = rng.randrange(TS), rng.randrange(TS)
        px(img, x, y, (118, 112, 104, 255) if rng.random() > 0.5 else (170, 164, 156, 255))
    return img


def dirt() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (148, 108, 68, 255))
    for _ in range(36):
        x, y = rng.randrange(TS), rng.randrange(TS)
        px(img, x, y, (128, 92, 55, 255) if rng.random() > 0.5 else (165, 122, 80, 255))
    for _ in range(6):
        x, y = rng.randrange(1, 14), rng.randrange(1, 14)
        px(img, x, y, (110, 82, 50, 255))
    return img


def water(deep: bool = False) -> Image.Image:
    base = (36, 92, 168, 255) if deep else (52, 124, 198, 255)
    foam = (150, 210, 240, 255)
    dark = (28, 70, 130, 255)
    img = Image.new("RGBA", (TS, TS), base)
    for y in range(TS):
        for x in range(TS):
            wave = math.sin((x + y * 0.6) * 0.9)
            if wave > 0.55:
                px(img, x, y, foam if not deep else (90, 150, 210, 255))
            elif wave < -0.65 and deep:
                px(img, x, y, dark)
    for y in (2, 6, 10, 14):
        for x in range(1, 15, 4):
            xx = (x + y // 2) % 15
            px(img, xx, y, foam)
    return img


def cliff() -> Image.Image:
    # Dark rock face — must read as elevation vs brown farm dirt
    img = Image.new("RGBA", (TS, TS), (72, 62, 52, 255))
    # grass/dirt lip on top edge
    for x in range(TS):
        px(img, x, 0, (86, 130, 58, 255))
        px(img, x, 1, (100, 88, 70, 255))
        px(img, x, 2, (88, 78, 64, 255))
    # vertical rock strata
    for x in (2, 5, 8, 11, 14):
        for y in range(3, TS):
            px(img, x, y, (55, 48, 40, 255) if (x + y) % 2 == 0 else (90, 78, 64, 255))
    # horizontal cracks
    for y in (6, 10, 14):
        for x in range(TS):
            px(img, x, y, (48, 42, 36, 255))
    # highlight stones
    for x, y in ((3, 8), (9, 12), (12, 5), (6, 13)):
        px(img, x, y, (140, 128, 110, 255))
    return img


def hill() -> Image.Image:
    img = grass(2)
    for y in range(0, 6):
        for x in range(TS):
            g = img.getpixel((x, y))
            px(img, x, y, (min(255, g[0] + 20), min(255, g[1] + 15), g[2], 255))
    return img


def stairs() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (140, 128, 108, 255))
    for y in (2, 6, 10, 14):
        for x in range(1, 15):
            px(img, x, y, (170, 158, 138, 255))
            px(img, x, y + 1, (110, 98, 80, 255))
    return img


def farmland() -> Image.Image:
    img = dirt()
    for y in (4, 8, 12):
        for x in range(1, 15):
            px(img, x, y, (110, 80, 48, 255))
    return img


def rail() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (72, 78, 70, 255))
    for x in range(TS):
        px(img, x, 5, (50, 50, 55, 255))
        px(img, x, 10, (50, 50, 55, 255))
    for x in (2, 7, 12):
        for y in range(TS):
            px(img, x, y, (100, 75, 45, 255))
    return img


def sand() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (214, 196, 148, 255))
    for _ in range(14):
        px(img, rng.randrange(TS), rng.randrange(TS), (190, 170, 120, 255))
    return img


def bridge() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (128, 96, 58, 255))
    for y in (3, 8, 13):
        for x in range(TS):
            px(img, x, y, (100, 72, 42, 255))
    for x in (1, 14):
        for y in range(TS):
            px(img, x, y, (90, 65, 40, 255))
    return img


def water_edge(side: str) -> Image.Image:
    """Jagged grass↔sand↔water shore — Stardew-like soft bank (not a hard tile cut)."""
    img = grass(2).copy()
    wcols = [(52, 124, 198, 255), (58, 132, 208, 255), (44, 110, 180, 255)]
    shore = [(196, 172, 118, 255), (178, 152, 100, 255), (210, 188, 132, 255), (168, 145, 96, 255)]
    foam = (170, 220, 245, 255)
    for y in range(TS):
        for x in range(TS):
            jag = ((x * 7) ^ (y * 11) ^ (x * y * 3)) % 7
            wave = int(2.4 * math.sin(x * 0.95 + y * 0.45 + (0.0 if side in ("n", "s") else 1.2)))
            # water depth band (deeper toward water side)
            if side == "n":
                depth = (5 + wave - jag // 3) - y
            elif side == "s":
                depth = y - (10 + wave + jag // 3)
            elif side == "e":
                depth = x - (10 + wave + jag // 3)
            else:  # w
                depth = (5 + wave - jag // 3) - x
            if depth >= 3:
                px(img, x, y, wcols[(x + y) % 3])
                if (x + y * 3) % 11 == 0:
                    px(img, x, y, foam)
            elif depth >= 0:
                px(img, x, y, shore[(x * 3 + y) % 4])
            elif depth >= -2 and rng.random() > 0.45:
                # sand speckles into grass
                px(img, x, y, shore[(x + y) % 4])
    # grass blade overhang onto sand/water lip
    for _ in range(16):
        if side == "n":
            x, y = rng.randrange(1, 15), rng.randrange(4, 11)
        elif side == "s":
            x, y = rng.randrange(1, 15), rng.randrange(5, 12)
        elif side == "e":
            x, y = rng.randrange(5, 12), rng.randrange(1, 15)
        else:
            x, y = rng.randrange(4, 11), rng.randrange(1, 15)
        c = img.getpixel((x, y))
        if c[2] > 150 or c[0] > 160:  # water or sand
            blade = (48 + rng.randrange(0, 30), 110 + rng.randrange(0, 40), 40 + rng.randrange(0, 20), 255)
            px(img, x, y, blade)
    return img


def grass_dirt(side: str) -> Image.Image:
    """Strong irregular grass↔dirt seam — grass tufts overhang dirt (Stardew stitch)."""
    img = grass(2).copy()
    dcols = [(148, 108, 68, 255), (128, 92, 55, 255), (165, 122, 80, 255), (138, 100, 62, 255)]
    for y in range(TS):
        for x in range(TS):
            # multi-frequency jagged boundary
            jag = ((x * 5) ^ (y * 9) ^ (x * y)) % 7
            wave = int(2.2 * math.sin(x * 0.9 + y * 0.4))
            hit = False
            if side == "n":
                hit = y > (6 + wave - jag // 3)
            elif side == "s":
                hit = y < (9 + wave + jag // 3)
            elif side == "e":
                hit = x < (9 + wave + jag // 3)
            elif side == "w":
                hit = x > (6 + wave - jag // 3)
            elif side == "ne":
                hit = y > (7 + wave) and x < (9 - wave)
            elif side == "nw":
                hit = y > (7 + wave) and x > (6 + wave)
            elif side == "se":
                hit = y < (9 - wave) and x < (9 - wave)
            elif side == "sw":
                hit = y < (9 - wave) and x > (6 + wave)
            if hit:
                px(img, x, y, dcols[(x + y) % 4])
    # dense grass blade overhang onto dirt side
    for _ in range(18):
        if side in ("n", "ne", "nw"):
            x, y = rng.randrange(1, 15), rng.randrange(7, 15)
        elif side in ("s", "se", "sw"):
            x, y = rng.randrange(1, 15), rng.randrange(1, 9)
        elif side == "e":
            x, y = rng.randrange(1, 9), rng.randrange(1, 15)
        else:
            x, y = rng.randrange(7, 15), rng.randrange(1, 15)
        blade = (48 + rng.randrange(0, 30), 110 + rng.randrange(0, 40), 40 + rng.randrange(0, 20), 255)
        tip = (90 + rng.randrange(0, 40), 160 + rng.randrange(0, 40), 70 + rng.randrange(0, 20), 255)
        px(img, x, y, blade)
        px(img, x, max(0, y - 1), tip)
        if rng.random() > 0.5:
            px(img, min(15, x + 1), y, blade)
    return img


def main() -> None:
    tiles = [
        grass(0),
        dirt(),
        path(),
        plaza(),
        water(False),
        cliff(),
        hill(),
        stairs(),
        farmland(),
        rail(),
        sand(),
        bridge(),
        grass(1),
        water(True),
        water_edge("e"),
        water_edge("w"),
    ]
    extra = [
        water_edge("n"),
        water_edge("s"),
        grass(2),
        grass(3),
        path(),
        dirt(),
        grass_dirt("n"),
        plaza(),
        grass_dirt("s"),
        sand(),
        farmland(),
        bridge(),
        grass_dirt("e"),
        grass_dirt("w"),
        grass_dirt("ne"),
        grass_dirt("nw"),
    ]
    # Replace duplicate sand/farmland slots (25–26) with SE/SW corners
    extra[9] = grass_dirt("se")   # was sand dup @ atlas 25
    extra[10] = grass_dirt("sw")  # was farmland dup @ atlas 26
    tiles.extend(extra)
    cols, rows = 8, 4
    atlas = Image.new("RGBA", (cols * TS, rows * TS), (0, 0, 0, 0))
    for i, t in enumerate(tiles[:32]):
        row, col = divmod(i, cols)
        atlas.paste(t, (col * TS, row * TS))
    save(atlas, "tileset_master.png")


if __name__ == "__main__":
    main()
