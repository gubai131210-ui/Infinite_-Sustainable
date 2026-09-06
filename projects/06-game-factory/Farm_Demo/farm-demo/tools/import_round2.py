"""Round-2 import: player 4-dir walk, NPC walk strips, transition tileset."""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

# reuse helpers from import_ai_sprites
import import_ai_sprites as base

SRC = base.SRC
RAW = base.RAW
OUT = base.OUT
H_HUMAN = base.H_HUMAN
TILE = base.TILE
chroma = base.chroma
crop_op = base.crop_op
save = base.save
fit_cell = base.fit_cell
sheet_from_frames = base.sheet_from_frames
split_grid = base.split_grid
opaque_bbox = base.opaque_bbox


def split_grid_clean(img: Image.Image, cols: int, rows: int) -> list[list[Image.Image]]:
    """Equal grid split without treadmill foot-trim (for characters / tiles)."""
    img = crop_op(img)
    cw = max(1, img.width // cols)
    rh = max(1, img.height // rows)
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            x0, y0 = c * cw, r * rh
            x1 = img.width if c == cols - 1 else (c + 1) * cw
            y1 = img.height if r == rows - 1 else (r + 1) * rh
            cell = img.crop((x0, y0, x1, y1))
            cb = opaque_bbox(cell)
            if cb:
                cell = cell.crop(cb)
            row.append(cell)
        grid.append(row)
    return grid


def import_player_4dir() -> None:
    print("player 4dir")
    path = SRC / "farm_player_4dir_walk.png"
    src = chroma(Image.open(path))
    # AI layout: row0 down, row1 right, row2 left, row3 up — 4x6
    grid = split_grid_clean(src, 6, 4)
    # Atlas rows: down, left, right, up
    order = [0, 2, 1, 3]
    atlas = Image.new("RGBA", (H_HUMAN * 6, H_HUMAN * 4), (0, 0, 0, 0))
    for out_r, src_r in enumerate(order):
        frames = grid[src_r] if src_r < len(grid) else []
        for c, fr in enumerate(frames[:6]):
            cell = fit_cell(fr, H_HUMAN, 46, 40)
            atlas.alpha_composite(cell, (c * H_HUMAN, out_r * H_HUMAN))
    save(atlas, "player.png")
    RAW.mkdir(parents=True, exist_ok=True)
    Image.open(path).convert("RGBA").save(RAW / "farm_player_4dir_walk.png", "PNG")


def import_npc_walks() -> None:
    print("npc walks")
    path = SRC / "farm_npc_walk_strips.png"
    src = chroma(Image.open(path))
    grid = split_grid_clean(src, 6, 5)
    names = ["npc_ahe", "npc_xiaoman", "npc_qingyu", "npc_linshen", "npc_zhou"]
    for i, name in enumerate(names):
        frames = grid[i] if i < len(grid) else []
        if not frames:
            print(f"  WARN {name}")
            continue
        save(sheet_from_frames(frames[:6], H_HUMAN, 46, 40), f"{name}.png")
    Image.open(path).convert("RGBA").save(RAW / "farm_npc_walk_strips.png", "PNG")


def import_tileset() -> None:
    print("tileset")
    path = SRC / "farm_tileset_transitions.png"
    src = chroma(Image.open(path))
    # Use 8x8 grid of square tiles (description says 8 cols; rows ~8)
    box = opaque_bbox(src)
    if not box:
        print("  FAIL empty")
        return
    full = src.crop(box)
    cols, rows = 8, 8
    cw = full.width // cols
    rh = full.height // rows
    cells: list[list[Image.Image]] = []
    for r in range(rows):
        row = []
        for c in range(cols):
            x0, y0 = c * cw, r * rh
            x1 = full.width if c == cols - 1 else (c + 1) * cw
            y1 = full.height if r == rows - 1 else (r + 1) * rh
            cell = crop_op(full.crop((x0, y0, x1, y1)))
            cell = cell.resize((TILE, TILE), Image.Resampling.NEAREST)
            row.append(cell)
        cells.append(row)

    # Row0 bases (from description)
    bases = {
        "tile_grass": (0, 0),
        "tile_dirt": (0, 1),
        "tile_tilled": (0, 2),
        "tile_watered": (0, 3),
        "tile_water": (0, 4),
        "tile_path": (0, 5),
        "tile_hill": (0, 6),
        "tile_farmland": (0, 7),
    }
    for name, (r, c) in bases.items():
        if r < len(cells) and c < len(cells[r]):
            save(cells[r][c], f"{name}.png")

    # Save full atlas for transition lookups: 8x8 of 16px = 128x128
    atlas = Image.new("RGBA", (TILE * cols, TILE * rows), (0, 0, 0, 0))
    for r in range(rows):
        for c in range(cols):
            atlas.paste(cells[r][c], (c * TILE, r * TILE))
    save(atlas, "tile_atlas.png")

    # Named transition tiles (approx positions from description)
    # grass-dirt edges often row1-2; water-grass row3
    trans = {
        "tile_gd_n": (1, 0),
        "tile_gd_e": (1, 4),
        "tile_gd_s": (2, 0),
        "tile_gd_w": (1, 5),
        "tile_gw_n": (3, 0),
        "tile_gw_e": (3, 4),
        "tile_gw_s": (3, 1),
        "tile_gw_w": (3, 5),
        "tile_gw_ne": (3, 2),
        "tile_gw_nw": (3, 3),
        "tile_gw_se": (3, 6),
        "tile_gw_sw": (3, 7),
    }
    for name, (r, c) in trans.items():
        if r < len(cells) and c < len(cells[r]):
            save(cells[r][c], f"{name}.png")

    Image.open(path).convert("RGBA").save(RAW / "farm_tileset_transitions.png", "PNG")


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    import_player_4dir()
    import_npc_walks()
    import_tileset()
    print("round2 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
