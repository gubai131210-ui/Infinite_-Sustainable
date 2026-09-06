"""Round4: fix player facing atlas + regenerate clean tiles (no pink fringe)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "processed"
QA = ROOT / "assets" / "qa"
CELL = 48
TILE = 16


def checker(img: Image.Image) -> Image.Image:
    board = Image.new("RGBA", img.size)
    px = board.load()
    for y in range(img.height):
        for x in range(img.width):
            px[x, y] = (220, 220, 220, 255) if ((x // 8) + (y // 8)) % 2 == 0 else (160, 160, 160, 255)
    board.alpha_composite(img)
    return board.convert("RGB")


def save(img: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    img.save(OUT / name)
    checker(img).save(QA / f"checker_{name}", quality=92)
    print(f"OK {name} {img.size}")


def scrub_fringe(img: Image.Image) -> Image.Image:
    """Remove hot-pink / magenta fringe pixels (opaque or semi)."""
    rgba = img.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 8:
                px[x, y] = (0, 0, 0, 0)
                continue
            # classic magenta / hot pink keys (including opaque outline on black)
            if r >= 160 and g <= 100 and b >= 100 and r > g + 50:
                px[x, y] = (0, 0, 0, 0)
                continue
            if r >= 180 and b >= 160 and g <= 140 and r + b > g * 2.2:
                px[x, y] = (0, 0, 0, 0)
                continue
            if r >= 190 and g <= 80 and b <= 180 and r > g + 80:
                px[x, y] = (0, 0, 0, 0)
                continue
            if r >= 200 and b >= 200 and g < 160:
                px[x, y] = (0, 0, 0, 0)
                continue
            if r > 160 and g < 130 and b > 140 and a < 250 and abs(r - b) < 40:
                px[x, y] = (0, 0, 0, 0)
    return rgba


def fix_player_atlas() -> None:
    """Ensure rows are down, left, right, up.

    Visual check: row1 was facing right, row2 facing left — swap them.
    """
    path = OUT / "player.png"
    im = Image.open(path).convert("RGBA")
    assert im.size == (CELL * 6, CELL * 4), im.size
    rows = [im.crop((0, r * CELL, CELL * 6, (r + 1) * CELL)) for r in range(4)]
    print("SWAPPING left/right rows (visual: row1 faced right, row2 faced left)")
    rows[1], rows[2] = rows[2], rows[1]
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    for r, row in enumerate(rows):
        out.alpha_composite(scrub_fringe(row), (0, r * CELL))
    save(out, "player.png")
    # verify
    for r, name in enumerate(["down", "left", "right", "up"]):
        cell = out.crop((0, r * CELL, CELL, (r + 1) * CELL))
        cell.resize((CELL * 4, CELL * 4), Image.Resampling.NEAREST).save(
            QA / f"player_row_{r}_{name}.png"
        )


def px(img: Image.Image, x: int, y: int, c: tuple) -> None:
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), c)


def fill(img: Image.Image, x0, y0, x1, y1, c) -> None:
    for y in range(y0, y1):
        for x in range(x0, x1):
            px(img, x, y, c)


def tile_grass() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    base = (74, 148, 64, 255)
    fill(img, 0, 0, 16, 16, base)
    for x, y in [(2, 3), (7, 5), (12, 2), (4, 10), (9, 12), (14, 9), (1, 14), (11, 6)]:
        fill(img, x, y, x + 1, y + 2, (96, 170, 78, 255))
    for x, y in [(5, 1), (11, 8), (3, 7), (8, 14)]:
        px(img, x, y, (52, 118, 46, 255))
    return img


def tile_dirt() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (148, 108, 70, 255))
    for x, y in [(3, 4), (10, 7), (6, 12), (13, 2), (1, 9)]:
        px(img, x, y, (122, 90, 56, 255))
    return img


def tile_path() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (186, 166, 118, 255))
    for x, y in [(2, 2), (9, 5), (5, 10), (13, 12), (7, 1), (4, 14)]:
        px(img, x, y, (158, 138, 96, 255))
    return img


def tile_plaza() -> Image.Image:
    """Stone plaza for village square."""
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (156, 150, 142, 255))
    fill(img, 0, 0, 16, 1, (130, 124, 116, 255))
    fill(img, 0, 8, 16, 9, (130, 124, 116, 255))
    fill(img, 0, 0, 1, 16, (130, 124, 116, 255))
    fill(img, 8, 0, 9, 16, (130, 124, 116, 255))
    for x, y in [(3, 3), (11, 5), (5, 12), (12, 11)]:
        px(img, x, y, (172, 166, 158, 255))
    return img


def tile_water() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (58, 124, 186, 255))
    for x, y in [(2, 4), (8, 3), (12, 8), (5, 11), (14, 13)]:
        px(img, x, y, (118, 178, 220, 255))
    for x, y in [(4, 7), (10, 12)]:
        px(img, x, y, (36, 86, 148, 255))
    return img


def tile_hill() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (112, 126, 86, 255))
    fill(img, 0, 0, 16, 5, (138, 148, 112, 255))
    for x in range(0, 16, 3):
        px(img, x, 7, (86, 98, 66, 255))
    return img


def tile_cliff() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (118, 104, 86, 255))
    fill(img, 0, 0, 16, 4, (148, 136, 118, 255))
    for y in (6, 10, 14):
        fill(img, 1, y, 15, y + 1, (96, 84, 68, 255))
    for x in (3, 8, 12):
        px(img, x, 8, (168, 156, 138, 255))
    return img


def tile_stairs() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (140, 128, 108, 255))
    for y in (3, 7, 11):
        fill(img, 1, y, 15, y + 2, (118, 106, 88, 255))
        fill(img, 1, y, 15, y + 1, (168, 156, 136, 255))
    return img


def tile_farmland() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (134, 100, 64, 255))
    for x, y in [(1, 1), (8, 4), (14, 9), (4, 13)]:
        px(img, x, y, (112, 82, 52, 255))
    return img


def tile_tilled() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (122, 86, 54, 255))
    for y in (3, 7, 11):
        fill(img, 1, y, 15, y + 1, (98, 70, 42, 255))
    return img


def tile_watered() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fill(img, 0, 0, 16, 16, (94, 70, 50, 255))
    for y in (3, 7, 11):
        fill(img, 1, y, 15, y + 1, (72, 54, 38, 255))
    for x, y in [(3, 4), (8, 6), (12, 9), (5, 11)]:
        px(img, x, y, (92, 142, 192, 255))
    return img


def _grass_water_edge(kind: str) -> Image.Image:
    """kind: n/e/s/w/ne/nw/se/sw — grass body with water bite."""
    g = tile_grass()
    wcol = (58, 124, 186, 255)
    wlight = (118, 178, 220, 255)
    img = g.copy()
    # water region
    for y in range(TILE):
        for x in range(TILE):
            in_w = False
            if kind == "n" and y < 7:
                in_w = True
            elif kind == "s" and y > 8:
                in_w = True
            elif kind == "e" and x > 8:
                in_w = True
            elif kind == "w" and x < 7:
                in_w = True
            elif kind == "ne" and (y < 7 and x > 8):
                in_w = True
            elif kind == "nw" and (y < 7 and x < 7):
                in_w = True
            elif kind == "se" and (y > 8 and x > 8):
                in_w = True
            elif kind == "sw" and (y > 8 and x < 7):
                in_w = True
            if in_w:
                img.putpixel((x, y), wcol if (x + y) % 5 else wlight)
    # soft shore line (tan)
    shore = (168, 140, 96, 255)
    for y in range(TILE):
        for x in range(TILE):
            if img.getpixel((x, y))[:3] == wcol[:3] or img.getpixel((x, y))[:3] == wlight[:3]:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < TILE and 0 <= ny < TILE:
                        c = img.getpixel((nx, ny))
                        if c[1] > 120 and c[0] < 120:  # grass-ish
                            img.putpixel((nx, ny), shore)
    return img


def _grass_dirt_edge(kind: str) -> Image.Image:
    g = tile_grass()
    dcol = (148, 108, 70, 255)
    img = g.copy()
    for y in range(TILE):
        for x in range(TILE):
            in_d = False
            if kind == "n" and y < 5:
                in_d = True
            elif kind == "s" and y > 10:
                in_d = True
            elif kind == "e" and x > 10:
                in_d = True
            elif kind == "w" and x < 5:
                in_d = True
            if in_d:
                img.putpixel((x, y), dcol)
    return img


def gen_all_tiles() -> None:
    mapping = {
        "tile_grass.png": tile_grass(),
        "tile_dirt.png": tile_dirt(),
        "tile_path.png": tile_path(),
        "tile_plaza.png": tile_plaza(),
        "tile_water.png": tile_water(),
        "tile_hill.png": tile_hill(),
        "tile_cliff.png": tile_cliff(),
        "tile_stairs.png": tile_stairs(),
        "tile_farmland.png": tile_farmland(),
        "tile_tilled.png": tile_tilled(),
        "tile_watered.png": tile_watered(),
    }
    for name, img in mapping.items():
        save(img, name)
    for k in ("n", "e", "s", "w", "ne", "nw", "se", "sw"):
        save(_grass_water_edge(k), f"tile_gw_{k}.png")
    for k in ("n", "e", "s", "w"):
        save(_grass_dirt_edge(k), f"tile_gd_{k}.png")


def scrub_existing_props() -> None:
    for name in ("house.png", "tree_0.png", "tree_1.png", "tree_2.png", "bush.png", "chest.png"):
        p = OUT / name
        if not p.exists():
            continue
        save(scrub_fringe(Image.open(p)), name)


if __name__ == "__main__":
    fix_player_atlas()
    gen_all_tiles()
    scrub_existing_props()
    print("R4 asset pass done")
