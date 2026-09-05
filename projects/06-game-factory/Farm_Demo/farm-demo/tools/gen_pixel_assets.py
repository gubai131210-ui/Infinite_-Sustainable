"""Generate Farm_Demo pixel sprites (green-screen raw + alpha processed + QA)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets" / "raw"
OUT = ROOT / "assets" / "processed"
QA = ROOT / "assets" / "qa"
GREEN = (255, 0, 255, 255)  # magenta key — do NOT use green (crops/trees need green)


def new_img(w: int, h: int, fill=GREEN) -> Image.Image:
    return Image.new("RGBA", (w, h), fill)


def put(img: Image.Image, pixels: list[tuple[int, int, tuple]]) -> None:
    px = img.load()
    for x, y, c in pixels:
        if 0 <= x < img.width and 0 <= y < img.height:
            px[x, y] = c


def fill_rect(img: Image.Image, x0, y0, x1, y1, c) -> None:
    px = img.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            if 0 <= x < img.width and 0 <= y < img.height:
                px[x, y] = c


def circle(img: Image.Image, cx, cy, r, c) -> None:
    px = img.load()
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                if 0 <= x < img.width and 0 <= y < img.height:
                    px[x, y] = c


def checkerboard(size: tuple[int, int], cell: int = 8) -> Image.Image:
    w, h = size
    board = Image.new("RGBA", (w, h))
    px = board.load()
    c1, c2 = (220, 220, 220, 255), (160, 160, 160, 255)
    for y in range(h):
        for x in range(w):
            px[x, y] = c1 if (x // cell + y // cell) % 2 == 0 else c2
    return board


def chroma_to_alpha(img: Image.Image, threshold: int = 40) -> Image.Image:
    """Key out magenta / hot-pink backdrop only (preserve foliage greens)."""
    rgba = img.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            # pure-ish magenta key
            if r > 200 and b > 200 and g < 80:
                px[x, y] = (0, 0, 0, 0)
            elif r > 180 and b > 180 and g < r - 40 and g < b - 40:
                px[x, y] = (0, 0, 0, 0)
    return rgba


def scrub(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if a == 0:
                px[x, y] = (0, 0, 0, 0)
            elif r > 180 and b > 180 and g < 100:
                # desaturate leftover magenta fringe
                gray = int(0.3 * r + 0.4 * g + 0.3 * b)
                px[x, y] = (gray, gray, gray, a)
    return rgba


def save_pair(name: str, green_img: Image.Image) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    green_img.save(RAW / name)
    cut = scrub(chroma_to_alpha(green_img))
    cut.save(OUT / name)
    board = checkerboard(cut.size)
    board.alpha_composite(cut)
    board.convert("RGB").save(QA / f"checker_{name}", quality=92)
    print(f"OK {name} {cut.size}")


def tile_grass() -> Image.Image:
    img = new_img(16, 16)
    base = (76, 145, 62, 255)
    fill_rect(img, 0, 0, 16, 16, base)
    for x, y in [(2, 3), (7, 5), (12, 2), (4, 10), (9, 12), (14, 9), (1, 14)]:
        fill_rect(img, x, y, x + 1, y + 2, (98, 168, 72, 255))
    for x, y in [(5, 1), (11, 8), (3, 7)]:
        img.putpixel((x, y), (58, 120, 48, 255))
    return img


def tile_dirt() -> Image.Image:
    img = new_img(16, 16)
    fill_rect(img, 0, 0, 16, 16, (145, 106, 68, 255))
    for x, y in [(3, 4), (10, 7), (6, 12), (13, 2)]:
        img.putpixel((x, y), (120, 88, 55, 255))
    return img


def tile_tilled() -> Image.Image:
    img = new_img(16, 16)
    fill_rect(img, 0, 0, 16, 16, (120, 84, 52, 255))
    for y in (3, 7, 11):
        fill_rect(img, 1, y, 15, y + 1, (98, 68, 40, 255))
    return img


def tile_watered() -> Image.Image:
    img = new_img(16, 16)
    fill_rect(img, 0, 0, 16, 16, (92, 68, 48, 255))
    for y in (3, 7, 11):
        fill_rect(img, 1, y, 15, y + 1, (70, 52, 36, 255))
    for x, y in [(3, 4), (8, 6), (12, 9), (5, 11), (10, 13)]:
        img.putpixel((x, y), (90, 140, 190, 255))
    return img

def tile_water() -> Image.Image:
    img = new_img(16, 16)
    fill_rect(img, 0, 0, 16, 16, (64, 130, 190, 255))
    for x, y in [(2, 4), (8, 3), (12, 8), (5, 11), (14, 13)]:
        img.putpixel((x, y), (120, 180, 220, 255))
    for x, y in [(4, 7), (10, 12)]:
        img.putpixel((x, y), (40, 90, 150, 255))
    return img


def tile_path() -> Image.Image:
    img = new_img(16, 16)
    fill_rect(img, 0, 0, 16, 16, (180, 160, 110, 255))
    for x, y in [(2, 2), (9, 5), (5, 10), (13, 12), (7, 1)]:
        img.putpixel((x, y), (150, 130, 90, 255))
    return img


def tile_hill() -> Image.Image:
    img = new_img(16, 16)
    fill_rect(img, 0, 0, 16, 16, (120, 130, 90, 255))
    fill_rect(img, 0, 0, 16, 6, (150, 155, 120, 255))
    for x in range(0, 16, 3):
        img.putpixel((x, 8), (90, 100, 70, 255))
    return img


def tile_farmland() -> Image.Image:
    """Soft soil ready for farming zone marker."""
    img = new_img(16, 16)
    fill_rect(img, 0, 0, 16, 16, (132, 98, 62, 255))
    for x, y in [(1, 1), (8, 4), (14, 9), (4, 13)]:
        img.putpixel((x, y), (110, 80, 50, 255))
    return img


def make_character(name: str, skin, hair, shirt, pants, accent=None) -> Image.Image:
    """32x32 top-down-ish character facing down, green bg. 4-frame sheet horizontally."""
    sheet = new_img(128, 32)
    accent = accent or shirt
    for fi in range(4):
        ox = fi * 32
        bob = (0, 1, 0, -1)[fi]
        # shadow
        fill_rect(sheet, ox + 10, 28, ox + 22, 30, (0, 0, 0, 60))
        # legs
        fill_rect(sheet, ox + 11, 22 + bob, ox + 15, 28 + bob, pants)
        fill_rect(sheet, ox + 17, 22 + bob, ox + 21, 28 + bob, pants)
        # body
        fill_rect(sheet, ox + 10, 14 + bob, ox + 22, 23 + bob, shirt)
        fill_rect(sheet, ox + 12, 16 + bob, ox + 14, 18 + bob, accent)
        # head
        fill_rect(sheet, ox + 11, 6 + bob, ox + 21, 15 + bob, skin)
        # hair
        fill_rect(sheet, ox + 11, 5 + bob, ox + 21, 9 + bob, hair)
        # eyes
        sheet.putpixel((ox + 13, 10 + bob), (30, 30, 30, 255))
        sheet.putpixel((ox + 18, 10 + bob), (30, 30, 30, 255))
        # walk arm swing
        if fi % 2 == 0:
            fill_rect(sheet, ox + 8, 16 + bob, ox + 10, 21 + bob, skin)
            fill_rect(sheet, ox + 22, 16 + bob, ox + 24, 21 + bob, skin)
        else:
            fill_rect(sheet, ox + 8, 15 + bob, ox + 10, 20 + bob, skin)
            fill_rect(sheet, ox + 22, 17 + bob, ox + 24, 22 + bob, skin)
    save_pair(f"{name}.png", sheet)
    return sheet


def make_animal(name: str, body, accent, ear=None) -> None:
    sheet = new_img(64, 32)
    ear = ear or body
    for fi in range(2):
        ox = fi * 32
        bob = fi
        fill_rect(sheet, ox + 8, 26 + bob, ox + 24, 29 + bob, (0, 0, 0, 50))
        # body
        fill_rect(sheet, ox + 8, 14 + bob, ox + 24, 26 + bob, body)
        # head
        fill_rect(sheet, ox + 18, 8 + bob, ox + 28, 18 + bob, body)
        fill_rect(sheet, ox + 20, 10 + bob, ox + 22, 12 + bob, (20, 20, 20, 255))
        fill_rect(sheet, ox + 25, 10 + bob, ox + 27, 12 + bob, (20, 20, 20, 255))
        # ears / crest
        fill_rect(sheet, ox + 18, 5 + bob, ox + 21, 9 + bob, ear)
        fill_rect(sheet, ox + 25, 5 + bob, ox + 28, 9 + bob, ear)
        # feet
        fill_rect(sheet, ox + 10, 25 + bob, ox + 13, 29 + bob, accent)
        fill_rect(sheet, ox + 19, 25 + bob, ox + 22, 29 + bob, accent)
        if name == "chicken":
            fill_rect(sheet, ox + 27, 12 + bob, ox + 30, 14 + bob, (230, 120, 40, 255))
            fill_rect(sheet, ox + 21, 4 + bob, ox + 25, 7 + bob, (220, 50, 50, 255))
    save_pair(f"{name}.png", sheet)


def make_tree(variant: int) -> None:
    img = new_img(48, 64)
    # trunk
    fill_rect(img, 20, 36, 28, 60, (110, 75, 45, 255))
    fill_rect(img, 22, 40, 26, 58, (90, 60, 35, 255))
    # canopy
    greens = [(40, 120, 55, 255), (50, 140, 65, 255), (30, 100, 45, 255)]
    g = greens[variant % 3]
    circle(img, 24, 28, 16, g)
    circle(img, 16, 30, 10, greens[(variant + 1) % 3])
    circle(img, 32, 30, 10, greens[(variant + 2) % 3])
    circle(img, 24, 18, 12, greens[(variant + 1) % 3])
    save_pair(f"tree_{variant}.png", img)


def make_flower(variant: int) -> None:
    img = new_img(16, 16)
    stem = (50, 120, 50, 255)
    fill_rect(img, 7, 8, 9, 15, stem)
    colors = [
        (230, 80, 120, 255),
        (240, 200, 60, 255),
        (180, 100, 220, 255),
        (255, 140, 80, 255),
    ]
    c = colors[variant % 4]
    circle(img, 8, 6, 3, c)
    img.putpixel((8, 6), (255, 240, 120, 255))
    save_pair(f"flower_{variant}.png", img)


def make_bush() -> None:
    img = new_img(32, 24)
    circle(img, 16, 14, 10, (45, 110, 50, 255))
    circle(img, 10, 14, 7, (55, 130, 60, 255))
    circle(img, 22, 14, 7, (40, 100, 45, 255))
    for x, y in [(12, 10), (18, 12), (15, 8)]:
        img.putpixel((x, y), (200, 60, 70, 255))
    save_pair("bush.png", img)


def make_crop_stages(crop_id: str, ripe_color) -> None:
    # stage0 seed mark, 1 sprout, 2 growing, 3 ripe
    for stage in range(4):
        img = new_img(16, 16)
        if stage == 0:
            img.putpixel((8, 12), (80, 60, 40, 255))
            img.putpixel((7, 11), (90, 70, 45, 255))
        elif stage == 1:
            fill_rect(img, 7, 10, 9, 14, (60, 140, 50, 255))
            img.putpixel((8, 9), (80, 160, 60, 255))
        elif stage == 2:
            fill_rect(img, 7, 6, 9, 14, (50, 130, 45, 255))
            fill_rect(img, 5, 8, 7, 10, (60, 140, 55, 255))
            fill_rect(img, 9, 8, 11, 10, (60, 140, 55, 255))
        else:
            fill_rect(img, 7, 8, 9, 14, (50, 120, 40, 255))
            circle(img, 8, 6, 4, ripe_color)
            if crop_id == "wheat":
                fill_rect(img, 6, 4, 10, 12, (210, 180, 70, 255))
                for y in range(4, 12, 2):
                    img.putpixel((5, y), (190, 160, 50, 255))
                    img.putpixel((10, y), (190, 160, 50, 255))
            elif crop_id == "pumpkin":
                circle(img, 8, 9, 5, ripe_color)
                fill_rect(img, 7, 4, 9, 7, (50, 120, 40, 255))
        save_pair(f"crop_{crop_id}_{stage}.png", img)


def make_house() -> None:
    img = new_img(64, 64)
    fill_rect(img, 8, 28, 56, 58, (160, 110, 70, 255))
    # roof
    for i in range(28):
        fill_rect(img, 8 + i // 2, 28 - i, 56 - i // 2, 29 - i, (140, 60, 50, 255))
    fill_rect(img, 26, 40, 38, 58, (80, 50, 30, 255))
    fill_rect(img, 14, 36, 22, 44, (180, 210, 230, 255))
    fill_rect(img, 42, 36, 50, 44, (180, 210, 230, 255))
    save_pair("house.png", img)


def make_chest() -> None:
    img = new_img(24, 20)
    fill_rect(img, 2, 6, 22, 18, (150, 100, 50, 255))
    fill_rect(img, 2, 4, 22, 10, (170, 120, 60, 255))
    fill_rect(img, 10, 9, 14, 13, (200, 170, 40, 255))
    save_pair("chest.png", img)


def make_item_icon(name: str, color) -> None:
    img = new_img(16, 16)
    if name.startswith("seed_"):
        circle(img, 8, 8, 4, color)
        img.putpixel((8, 8), (40, 30, 20, 255))
    elif name == "feed":
        fill_rect(img, 3, 5, 13, 12, (200, 170, 90, 255))
        fill_rect(img, 5, 3, 11, 5, (180, 140, 70, 255))
    elif name == "fish":
        fill_rect(img, 3, 6, 12, 11, (90, 140, 200, 255))
        img.putpixel((12, 8), (70, 110, 170, 255))
        img.putpixel((5, 8), (20, 20, 40, 255))
    elif name == "wood":
        fill_rect(img, 4, 3, 12, 13, (130, 90, 50, 255))
        fill_rect(img, 6, 5, 10, 11, (150, 110, 70, 255))
    else:
        # harvested crop icon
        circle(img, 8, 8, 5, color)
    save_pair(f"item_{name}.png", img)


def make_tool_icon(name: str) -> None:
    img = new_img(16, 16)
    if name == "hoe":
        fill_rect(img, 7, 2, 9, 12, (120, 80, 40, 255))
        fill_rect(img, 4, 11, 12, 14, (140, 140, 150, 255))
    elif name == "can":
        fill_rect(img, 5, 5, 12, 13, (70, 130, 200, 255))
        fill_rect(img, 11, 3, 14, 7, (70, 130, 200, 255))
        fill_rect(img, 6, 2, 10, 5, (90, 90, 100, 255))
    elif name == "axe":
        fill_rect(img, 7, 4, 9, 14, (120, 80, 40, 255))
        fill_rect(img, 3, 3, 12, 7, (160, 160, 170, 255))
    elif name == "rod":
        fill_rect(img, 8, 1, 10, 14, (140, 100, 50, 255))
        fill_rect(img, 10, 2, 14, 3, (200, 200, 210, 255))
    save_pair(f"tool_{name}.png", img)


def main() -> int:
    for fn, gen in [
        ("tile_grass.png", tile_grass),
        ("tile_dirt.png", tile_dirt),
        ("tile_tilled.png", tile_tilled),
        ("tile_watered.png", tile_watered),
        ("tile_water.png", tile_water),
        ("tile_path.png", tile_path),
        ("tile_hill.png", tile_hill),
        ("tile_farmland.png", tile_farmland),
    ]:
        save_pair(fn, gen())

    make_character("player", (240, 200, 160, 255), (60, 40, 30, 255), (70, 120, 200, 255), (50, 60, 90, 255), (255, 220, 80, 255))
    make_character("npc_ahe", (230, 190, 150, 255), (90, 70, 40, 255), (140, 100, 60, 255), (70, 55, 40, 255), (200, 160, 80, 255))
    make_character("npc_xiaoman", (245, 210, 175, 255), (200, 120, 60, 255), (220, 120, 150, 255), (90, 70, 110, 255))
    make_character("npc_qingyu", (235, 195, 160, 255), (40, 50, 70, 255), (50, 110, 150, 255), (40, 50, 70, 255), (180, 210, 230, 255))
    make_character("npc_linshen", (240, 200, 170, 255), (80, 50, 40, 255), (100, 160, 90, 255), (80, 60, 50, 255), (230, 100, 130, 255))
    make_character("npc_zhou", (220, 180, 145, 255), (50, 50, 55, 255), (120, 120, 130, 255), (60, 60, 70, 255), (180, 100, 60, 255))

    make_animal("chicken", (240, 230, 210, 255), (200, 160, 80, 255), (230, 80, 70, 255))
    make_animal("cow", (210, 210, 215, 255), (80, 70, 60, 255), (200, 200, 205, 255))
    make_animal("sheep", (235, 235, 230, 255), (90, 80, 70, 255), (245, 245, 240, 255))

    for i in range(3):
        make_tree(i)
    for i in range(4):
        make_flower(i)
    make_bush()
    make_house()
    make_chest()

    crops = {
        "radish": (240, 240, 245, 255),
        "greens": (80, 170, 70, 255),
        "wheat": (220, 190, 70, 255),
        "tomato": (220, 60, 50, 255),
        "pumpkin": (230, 140, 40, 255),
    }
    for cid, col in crops.items():
        make_crop_stages(cid, col)
        make_item_icon(f"seed_{cid}", col)
        make_item_icon(cid, col)

    make_item_icon("feed", (200, 170, 90, 255))
    make_item_icon("fish", (90, 140, 200, 255))
    make_item_icon("wood", (130, 90, 50, 255))

    for t in ("hoe", "can", "axe", "rod"):
        make_tool_icon(t)

    print("All assets generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
