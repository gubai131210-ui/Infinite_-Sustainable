"""Rich master tileset — varied grass/path/water/cliff for video-like density."""
from __future__ import annotations

from pathlib import Path
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
    bases = [(70, 140, 58), (78, 152, 64), (62, 128, 52), (84, 158, 70)]
    b = bases[variant % 4]
    img = Image.new("RGBA", (TS, TS), (*b, 255))
    # mottled patches (break flat fill / stripe look)
    for _ in range(40):
        x, y = rng.randrange(TS), rng.randrange(TS)
        bright = (min(255, b[0] + 28), min(255, b[1] + 34), min(255, b[2] + 22), 255)
        dark = (max(0, b[0] - 24), max(0, b[1] - 28), max(0, b[2] - 18), 255)
        mid = (b[0] + 8, b[1] + 10, b[2] + 4, 255)
        px(img, x, y, [dark, bright, mid][rng.randrange(3)])
    for _ in range(6):
        x, y = rng.randrange(1, 14), rng.randrange(2, 14)
        px(img, x, y, (48, 110, 40, 255))
        px(img, x, y - 1, (96, 170, 78, 255))
        if rng.random() > 0.5:
            px(img, x + 1, y, (55, 120, 45, 255))
    # occasional flower speck
    if variant % 2 == 0 and rng.random() > 0.55:
        fx, fy = rng.randrange(2, 14), rng.randrange(2, 14)
        px(img, fx, fy, (220, 90, 120, 255) if rng.random() > 0.5 else (240, 220, 90, 255))
    return img


def dirt() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (148, 108, 68, 255))
    for _ in range(22):
        x, y = rng.randrange(TS), rng.randrange(TS)
        px(img, x, y, (128, 92, 55, 255) if rng.random() > 0.5 else (165, 122, 80, 255))
    return img


def path() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (188, 168, 118, 255))
    for _ in range(16):
        x, y = rng.randrange(TS), rng.randrange(TS)
        px(img, x, y, (160, 140, 95, 255))
    # soft edge darken
    for i in range(TS):
        px(img, i, 0, (150, 130, 90, 255))
        px(img, 0, i, (150, 130, 90, 255))
    return img


def plaza() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (158, 152, 144, 255))
    for x in range(TS):
        px(img, x, 0, (120, 114, 106, 255))
        px(img, x, 8, (120, 114, 106, 255))
    for y in range(TS):
        px(img, 0, y, (120, 114, 106, 255))
        px(img, 8, y, (120, 114, 106, 255))
    px(img, 3, 3, (175, 170, 162, 255))
    px(img, 11, 11, (140, 134, 126, 255))
    return img


def water(deep: bool = False) -> Image.Image:
    base = (42, 96, 168, 255) if deep else (58, 128, 192, 255)
    light = (110, 180, 230, 255)
    img = Image.new("RGBA", (TS, TS), base)
    for y in (3, 7, 11):
        for x in range(2, 14, 3):
            px(img, x + (y % 2), y, light)
    if deep:
        for _ in range(6):
            px(img, rng.randrange(TS), rng.randrange(TS), (30, 70, 130, 255))
    return img


def cliff() -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (118, 102, 84, 255))
    fill_top = (148, 138, 118, 255)
    for y in range(0, 5):
        for x in range(TS):
            px(img, x, y, fill_top)
    for y in (6, 10, 14):
        for x in range(1, 15):
            px(img, x, y, (96, 82, 66, 255))
    for x in (3, 8, 12):
        px(img, x, 8, (168, 156, 138, 255))
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
    """Grass tile with water bite on one side."""
    img = grass(0)
    w = (58, 128, 192, 255)
    shore = (170, 145, 100, 255)
    for y in range(TS):
        for x in range(TS):
            hit = False
            if side == "n" and y < 6:
                hit = True
            elif side == "s" and y > 9:
                hit = True
            elif side == "e" and x > 9:
                hit = True
            elif side == "w" and x < 6:
                hit = True
            if hit:
                px(img, x, y, w)
    # shore fringe
    for y in range(TS):
        for x in range(TS):
            if img.getpixel((x, y))[:3] == w[:3]:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < TS and 0 <= ny < TS:
                        c = img.getpixel((nx, ny))
                        if c[1] > 100 and c[0] < 120:
                            px(img, nx, ny, shore)
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
    # extend atlas to 8x4 = 32 for extra edges
    extra = [
        water_edge("n"),
        water_edge("s"),
        grass(2),
        grass(3),
        path(),
        dirt(),
        cliff(),
        plaza(),
        water(False),
        sand(),
        farmland(),
        bridge(),
        rail(),
        hill(),
        stairs(),
        grass(0),
    ]
    tiles.extend(extra)
    cols, rows = 8, 4
    atlas = Image.new("RGBA", (cols * TS, rows * TS), (0, 0, 0, 0))
    for i, t in enumerate(tiles[:32]):
        r, c = divmod(i, cols)
        # wait: divmod(i, cols) gives (quot, rem) = (row if row-major by cols...)
        # i=0 -> 0,0; i=8 -> 1,0
        row, col = divmod(i, cols)
        atlas.paste(t, (col * TS, row * TS))
    save(atlas, "tileset_master.png")


if __name__ == "__main__":
    main()
