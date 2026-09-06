"""Generate lake-echo master tileset atlas (16x16 cells)."""
from __future__ import annotations

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "tiles"
QA = ROOT / "assets" / "qa"
TS = 16

# Atlas layout 8 cols x 4 rows
# 0 grass 1 dirt 2 path 3 plaza 4 water 5 cliff 6 hill 7 stairs
# 8 farmland 9 rail 10 sand 11 bridge 12-15 water edges later

COLORS = {
    0: (74, 148, 64),      # grass
    1: (148, 108, 70),     # dirt
    2: (186, 166, 118),    # path
    3: (156, 150, 142),    # plaza
    4: (58, 124, 186),     # water
    5: (118, 104, 86),     # cliff
    6: (112, 126, 86),     # hill
    7: (140, 128, 108),    # stairs
    8: (134, 100, 64),     # farmland
    9: (60, 60, 70),       # rail
    10: (210, 190, 140),   # sand
    11: (120, 90, 55),     # bridge wood
    12: (90, 160, 80),     # grass light
    13: (40, 90, 150),     # deep water
    14: (170, 70, 60),     # barn red marker
    15: (220, 220, 230),   # station stone
}


def cell(c: tuple[int, int, int], detail: bool = True) -> Image.Image:
    img = Image.new("RGBA", (TS, TS), (*c, 255))
    if detail:
        px = img.load()
        for i, (x, y) in enumerate([(2, 3), (7, 5), (12, 2), (4, 10), (9, 12)]):
            shade = tuple(max(0, min(255, v + (-8 if i % 2 else 8))) for v in c)
            px[x, y] = (*shade, 255)
    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    cols, rows = 8, 2
    atlas = Image.new("RGBA", (cols * TS, rows * TS), (0, 0, 0, 0))
    for i in range(16):
        c = COLORS[i]
        tile = cell(c, detail=i not in (9,))
        if i == 3:  # plaza grid lines
            for x in range(TS):
                tile.putpixel((x, 0), (130, 124, 116, 255))
                tile.putpixel((x, 8), (130, 124, 116, 255))
            for y in range(TS):
                tile.putpixel((0, y), (130, 124, 116, 255))
                tile.putpixel((8, y), (130, 124, 116, 255))
        if i == 7:  # stairs
            for y in (3, 7, 11):
                for x in range(1, 15):
                    tile.putpixel((x, y), (168, 156, 136, 255))
        if i == 9:  # rail ties
            for x in range(TS):
                tile.putpixel((x, 6), (40, 40, 45, 255))
                tile.putpixel((x, 9), (40, 40, 45, 255))
            for x in (2, 7, 12):
                for y in range(TS):
                    tile.putpixel((x, y), (90, 70, 40, 255))
        r, cidx = divmod(i, cols)
        atlas.paste(tile, (cidx * TS, r * TS))
    path = OUT / "tileset_master.png"
    atlas.save(path)
    # checker
    board = Image.new("RGBA", atlas.size)
    for y in range(atlas.height):
        for x in range(atlas.width):
            board.putpixel((x, y), (220, 220, 220, 255) if ((x // 8) + (y // 8)) % 2 == 0 else (160, 160, 160, 255))
    board.alpha_composite(atlas)
    board.convert("RGB").save(QA / "checker_tileset_master.png", quality=92)
    print("OK", path, atlas.size)


if __name__ == "__main__":
    main()
