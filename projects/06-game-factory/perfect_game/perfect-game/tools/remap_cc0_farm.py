"""P05 — Remap CC0 inspiration into Oakhaven-consistent wet soil + denser crop stages.

Does NOT paste Kenney side-view tiles into the top-down world (style clash).
Uses Visual Bible palette; optionally samples Kenney tile colors as accent hints.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "processed"
CC0_TILES = ROOT / "assets" / "cc0" / "kenney_pixelplatformer_farm" / "raw" / "Tiles"
QA = ROOT / "assets" / "qa"

# Visual Bible-ish palette
SOIL = (139, 107, 74, 255)
SOIL_DARK = (90, 70, 48, 255)
WET = (55, 90, 130, 200)
GRASS_HINT = (95, 168, 106, 255)


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
    board.convert("RGB").save(QA / f"checker_{name}", quality=90)
    print("OK", name, img.size)


def wet_soil_tile() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=SOIL_DARK)
    for y in range(0, 16, 2):
        for x in range(0, 16, 2):
            if (x + y) % 4 == 0:
                d.point((x, y), fill=WET)
    d.rectangle([1, 1, 14, 14], outline=(40, 70, 100, 180))
    return img


def enhance_crop_stage(crop: str, stage: int) -> None:
    path = OUT / f"crop_{crop}_{stage}.png"
    if not path.exists():
        return
    img = Image.open(path).convert("RGBA")
    # Add subtle stem sway shadow / highlight for readability
    d = ImageDraw.Draw(img)
    w, h = img.size
    if stage >= 1:
        d.rectangle([w // 2 - 1, h - 4, w // 2, h - 1], fill=(60, 100, 50, 200))
    if stage >= 2:
        d.ellipse([w // 2 - 3, 2, w // 2 + 3, 8], outline=(255, 255, 200, 120))
    if stage >= 3:
        # ripe sparkle
        d.point((w // 2 + 2, 4), fill=(255, 240, 120, 220))
        d.point((w // 2 - 2, 6), fill=(255, 255, 255, 180))
    save(img, f"crop_{crop}_{stage}.png")


def catalog_kenney_sample() -> None:
    """Copy a few Kenney tiles into cc0/catalog for designers (not runtime)."""
    cat = ROOT / "assets" / "cc0" / "catalog"
    cat.mkdir(parents=True, exist_ok=True)
    if not CC0_TILES.exists():
        print("no kenney tiles")
        return
    # Sample every 10th tile as reference sheet cells
    picks = sorted(CC0_TILES.glob("tile_*.png"))[::10][:12]
    for p in picks:
        img = Image.open(p).convert("RGBA")
        # Nearest scale toward 16 if needed
        if img.size != (16, 16):
            img = img.resize((16, 16), Image.NEAREST)
        img.save(cat / p.name)
    print("catalog", len(picks), "->", cat)


def main() -> None:
    save(wet_soil_tile(), "tile_wet_soil.png")
    for crop in ("radish", "greens", "wheat", "tomato", "pumpkin"):
        for stage in range(4):
            enhance_crop_stage(crop, stage)
    catalog_kenney_sample()
    print("P05 remap done")


if __name__ == "__main__":
    main()
