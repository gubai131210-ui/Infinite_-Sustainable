"""High-detail landmark props — shaded pixel art, not flat color blocks."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "processed"
QA = ROOT / "assets" / "qa"


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


def _px(d: ImageDraw.ImageDraw, xy, c) -> None:
    d.point(xy, fill=c)


def _shade_rect(d, box, base, dark, light) -> None:
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=base)
    d.rectangle([x0, y0, x0 + 1, y1], fill=light)
    d.rectangle([x0, y0, x1, y0 + 1], fill=light)
    d.rectangle([x1 - 1, y0, x1, y1], fill=dark)
    d.rectangle([x0, y1 - 1, x1, y1], fill=dark)


def barn(w=112, h=88) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # foundation
    d.rectangle([8, h - 10, w - 8, h - 4], fill=(90, 80, 70, 255))
    # body with board lines
    _shade_rect(d, (10, 30, w - 10, h - 8), (168, 52, 44, 255), (110, 30, 28, 255), (200, 80, 70, 255))
    for x in range(14, w - 14, 6):
        d.line([(x, 34), (x, h - 10)], fill=(140, 40, 36, 180), width=1)
    # gambrel-ish roof
    d.polygon([(8, 32), (w // 2, 4), (w - 8, 32)], fill=(78, 58, 40, 255))
    d.polygon([(14, 32), (w // 2, 10), (w - 14, 32)], fill=(102, 78, 52, 255))
    d.line([(8, 32), (w // 2, 4)], fill=(50, 36, 24, 255))
    d.line([(w - 8, 32), (w // 2, 4)], fill=(50, 36, 24, 255))
    # white trim + loft
    d.rectangle([12, 34, w - 12, 38], fill=(235, 228, 215, 255))
    d.ellipse([w // 2 - 9, 14, w // 2 + 9, 28], fill=(55, 40, 32, 255), outline=(30, 22, 18, 255))
    d.line([(w // 2, 14), (w // 2, 28)], fill=(200, 190, 175, 255))
    # big door + hardware
    d.rectangle([w // 2 - 14, 46, w // 2 + 14, h - 8], fill=(62, 38, 26, 255), outline=(40, 24, 16, 255))
    d.line([(w // 2, 46), (w // 2, h - 8)], fill=(90, 60, 40, 255))
    d.ellipse([w // 2 + 6, 58, w // 2 + 10, 62], fill=(180, 150, 60, 255))
    # side windows
    for ox in (18, w - 34):
        d.rectangle([ox, 44, ox + 14, 56], fill=(170, 205, 230, 255), outline=(60, 45, 35, 255))
        d.line([(ox + 7, 44), (ox + 7, 56)], fill=(60, 45, 35, 255))
        d.line([(ox, 50), (ox + 14, 50)], fill=(60, 45, 35, 255))
    return img


def silo() -> Image.Image:
    img = Image.new("RGBA", (40, 88), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 0, 36, 20], fill=(200, 70, 58, 255), outline=(120, 40, 36, 255))
    d.ellipse([8, 4, 32, 16], fill=(230, 110, 90, 255))
    _shade_rect(d, (6, 12, 34, 80), (175, 55, 48, 255), (120, 35, 32, 255), (210, 90, 80, 255))
    for y in (24, 36, 48, 60, 72):
        d.rectangle([8, y, 32, y + 2], fill=(140, 42, 38, 255))
        d.rectangle([8, y, 14, y + 2], fill=(200, 90, 80, 180))
    d.rectangle([16, 18, 24, 24], fill=(90, 95, 105, 255), outline=(50, 50, 55, 255))
    d.rectangle([10, 80, 30, 86], fill=(80, 70, 60, 255))
    return img


def townhouse(roof=(140, 70, 55), wall=(220, 205, 175)) -> Image.Image:
    img = Image.new("RGBA", (80, 72), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # stone base
    d.rectangle([4, 56, 76, 68], fill=(120, 115, 108, 255))
    for x in range(6, 74, 8):
        d.rectangle([x, 58, x + 5, 66], fill=(140, 135, 125, 255))
    _shade_rect(d, (6, 22, 74, 58), (*wall, 255), (160, 145, 120, 255), (245, 235, 215, 255))
    # timber frame
    d.rectangle([6, 22, 74, 26], fill=(70, 50, 35, 255))
    d.rectangle([6, 38, 74, 41], fill=(70, 50, 35, 255))
    d.rectangle([38, 22, 42, 58], fill=(70, 50, 35, 255))
    # roof
    d.polygon([(2, 24), (40, 2), (78, 24)], fill=(*roof, 255))
    d.polygon([(10, 24), (40, 8), (70, 24)], fill=(min(255, roof[0] + 25), min(255, roof[1] + 20), min(255, roof[2] + 15), 255))
    # chimney + smoke hint
    d.rectangle([56, 6, 66, 22], fill=(110, 100, 95, 255))
    d.rectangle([54, 4, 68, 8], fill=(90, 85, 80, 255))
    # door + windows
    d.rectangle([34, 40, 46, 58], fill=(70, 45, 30, 255), outline=(40, 25, 18, 255))
    d.ellipse([42, 48, 45, 51], fill=(200, 170, 70, 255))
    for ox in (12, 54):
        d.rectangle([ox, 28, ox + 12, 38], fill=(140, 185, 220, 255), outline=(60, 45, 35, 255))
        d.line([(ox + 6, 28), (ox + 6, 38)], fill=(60, 45, 35, 255))
        d.line([(ox, 33), (ox + 12, 33)], fill=(60, 45, 35, 255))
        d.rectangle([ox - 1, 38, ox + 13, 40], fill=(90, 70, 50, 255))  # sill
    return img


def stall(awning=(220, 50, 50)) -> Image.Image:
    img = Image.new("RGBA", (52, 44), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([2, 20, 50, 40], fill=(130, 95, 60, 255), outline=(80, 55, 35, 255))
    for x in range(4, 48, 4):
        d.line([(x, 22), (x, 38)], fill=(110, 80, 50, 120))
    for x in range(2, 50, 6):
        col = (*awning, 255) if ((x // 6) % 2) == 0 else (245, 245, 245, 255)
        d.polygon([(x, 4), (x + 6, 4), (x + 5, 20), (x + 1, 20)], fill=col)
    d.rectangle([6, 24, 18, 32], fill=(200, 70, 55, 255))
    d.rectangle([22, 24, 34, 32], fill=(240, 210, 90, 255))
    d.rectangle([38, 24, 46, 30], fill=(90, 160, 90, 255))
    d.rectangle([4, 16, 6, 40], fill=(90, 65, 40, 255))
    d.rectangle([46, 16, 48, 40], fill=(90, 65, 40, 255))
    return img


def train() -> Image.Image:
    img = Image.new("RGBA", (140, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # rails shadow
    d.rectangle([0, 44, 140, 48], fill=(70, 70, 75, 180))
    # engine
    _shade_rect(d, (4, 16, 48, 40), (36, 36, 42, 255), (18, 18, 22, 255), (70, 70, 80, 255))
    d.rectangle([10, 8, 28, 16], fill=(50, 50, 58, 255))  # cabin
    d.rectangle([12, 10, 20, 15], fill=(160, 190, 220, 255))
    d.rectangle([30, 4, 38, 16], fill=(45, 45, 50, 255))  # stack
    d.ellipse([32, 0, 44, 10], fill=(210, 210, 215, 160))
    d.ellipse([38, 0, 50, 12], fill=(190, 190, 195, 120))
    # cowcatcher
    d.polygon([(4, 36), (0, 44), (12, 40)], fill=(90, 90, 100, 255))
    # cars
    for i, ox in enumerate((50, 90)):
        col = (145, 78, 52, 255) if i == 0 else (120, 95, 70, 255)
        _shade_rect(d, (ox, 18, ox + 38, 40), col, (80, 50, 35, 255), (180, 120, 90, 255))
        for wx in (ox + 6, ox + 18, ox + 28):
            d.rectangle([wx, 22, wx + 8, 30], fill=(170, 200, 225, 255), outline=(50, 40, 30, 255))
    for cx in (12, 28, 58, 78, 100, 120):
        d.ellipse([cx, 36, cx + 12, 48], fill=(25, 25, 28, 255))
        d.ellipse([cx + 3, 39, cx + 9, 45], fill=(90, 90, 95, 255))
    return img


def lighthouse() -> Image.Image:
    img = Image.new("RGBA", (56, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # rocky base
    d.polygon([(8, 118), (48, 118), (44, 108), (12, 108)], fill=(110, 105, 95, 255))
    d.rectangle([10, 108, 46, 118], fill=(95, 90, 82, 255))
    # tapered tower with stripe bands + highlight
    for i, y in enumerate(range(24, 108, 10)):
        t = (108 - y) / 90.0
        inset = int(4 + t * 4)
        col = (220, 48, 48, 255) if i % 2 == 0 else (245, 245, 248, 255)
        dark = (160, 30, 30, 255) if i % 2 == 0 else (200, 200, 205, 255)
        light = (250, 120, 110, 255) if i % 2 == 0 else (255, 255, 255, 255)
        _shade_rect(d, (10 + inset, y, 46 - inset, y + 10), col, dark, light)
        # window every other band
        if i % 2 == 1 and 40 < y < 90:
            cx = 28
            d.rectangle([cx - 3, y + 2, cx + 3, y + 8], fill=(40, 50, 70, 255))
    # lantern room
    d.rectangle([14, 14, 42, 26], fill=(255, 235, 120, 255), outline=(180, 140, 40, 255))
    d.rectangle([18, 16, 22, 24], fill=(255, 255, 220, 255))
    d.rectangle([34, 16, 38, 24], fill=(255, 255, 220, 255))
    d.polygon([(14, 14), (28, 2), (42, 14)], fill=(190, 45, 45, 255))
    d.rectangle([26, 16, 30, 24], fill=(255, 250, 180, 255))
    return img


def statue() -> Image.Image:
    img = Image.new("RGBA", (36, 52), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([2, 40, 34, 50], fill=(100, 100, 108, 255))
    d.rectangle([6, 36, 30, 40], fill=(130, 130, 138, 255))
    d.rectangle([12, 18, 24, 36], fill=(150, 150, 160, 255))
    d.ellipse([10, 6, 26, 20], fill=(155, 155, 165, 255))
    d.rectangle([8, 22, 12, 34], fill=(140, 140, 150, 255))  # arm
    d.rectangle([24, 22, 28, 34], fill=(140, 140, 150, 255))
    d.rectangle([14, 8, 16, 12], fill=(180, 180, 190, 255))  # highlight
    return img


def fence() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 5, 16, 7], fill=(140, 105, 65, 255))
    d.rectangle([0, 10, 16, 12], fill=(125, 90, 55, 255))
    for x in (2, 12):
        d.rectangle([x, 2, x + 2, 14], fill=(100, 70, 40, 255))
        d.point((x, 2), fill=(160, 130, 90, 255))
    return img


def bridge() -> Image.Image:
    img = Image.new("RGBA", (72, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 14, 72, 28], fill=(115, 82, 48, 255))
    for x in range(0, 72, 7):
        d.rectangle([x, 14, x + 5, 28], fill=(100, 72, 42, 255) if (x // 7) % 2 == 0 else (130, 95, 55, 255))
    d.rectangle([0, 2, 5, 28], fill=(85, 60, 35, 255))
    d.rectangle([67, 2, 72, 28], fill=(85, 60, 35, 255))
    d.rectangle([0, 2, 72, 6], fill=(145, 110, 70, 255))
    d.rectangle([0, 6, 72, 8], fill=(90, 65, 40, 255))
    return img


def boat() -> Image.Image:
    img = Image.new("RGBA", (48, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(2, 14), (42, 14), (36, 22), (8, 22)], fill=(100, 65, 38, 255))
    d.polygon([(4, 14), (40, 14), (34, 18), (10, 18)], fill=(130, 90, 55, 255))
    d.rectangle([22, 2, 24, 14], fill=(70, 55, 35, 255))
    d.polygon([(24, 2), (40, 10), (24, 12)], fill=(245, 245, 250, 255))
    d.line([(24, 2), (24, 12)], fill=(180, 180, 190, 255))
    return img


def waterfall() -> Image.Image:
    img = Image.new("RGBA", (64, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # cliff face
    d.rectangle([0, 0, 64, 22], fill=(105, 95, 80, 255))
    for x in range(0, 64, 5):
        d.rectangle([x, 2, x + 3, 20], fill=(125, 115, 95, 255) if (x // 5) % 2 == 0 else (90, 82, 70, 255))
    d.rectangle([4, 18, 60, 24], fill=(70, 65, 55, 255))
    # falling water strands
    for x, a in ((12, 200), (18, 160), (24, 220), (30, 180), (36, 210), (42, 150), (48, 190)):
        d.rectangle([x, 22, x + 3, 68], fill=(150, 210, 245, a))
        d.rectangle([x + 1, 26, x + 2, 64], fill=(220, 240, 255, min(255, a + 40)))
    # splash pool
    d.ellipse([10, 64, 54, 78], fill=(70, 145, 210, 230))
    d.ellipse([18, 66, 46, 74], fill=(160, 220, 255, 180))
    return img


def ruins() -> Image.Image:
    """Mossy stone arch + crumbled wall — forest ruins between waterfall and station."""
    img = Image.new("RGBA", (96, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    moss = (70, 110, 70, 255)
    stone = (130, 125, 115, 255)
    dark = (90, 85, 78, 255)
    # left pillar
    _shade_rect(d, (8, 18, 28, 60), stone, dark, (160, 155, 145, 255))
    # right pillar
    _shade_rect(d, (68, 18, 88, 60), stone, dark, (160, 155, 145, 255))
    # arch top
    d.arc([8, 4, 88, 48], 180, 360, fill=stone, width=10)
    d.arc([14, 10, 82, 44], 180, 360, fill=dark, width=4)
    # rubble base
    for x, y, w, h in ((4, 52, 20, 10), (30, 54, 16, 8), (50, 50, 22, 12), (74, 54, 18, 8)):
        d.rectangle([x, y, x + w, y + h], fill=dark)
        d.rectangle([x + 2, y + 2, x + w - 2, y + 4], fill=moss)
    # moss patches
    for ox, oy in ((10, 24), (14, 40), (72, 28), (78, 44), (40, 16)):
        d.ellipse([ox, oy, ox + 8, oy + 5], fill=moss)
    return img


def main() -> None:
    save(barn(), "prop_barn.png")
    save(barn(100, 80), "prop_barn2.png")
    save(silo(), "prop_silo.png")
    save(townhouse((110, 70, 50), (235, 220, 195)), "prop_farmhouse.png")
    save(townhouse((70, 95, 140), (235, 225, 210)), "prop_townhouse_blue.png")
    save(townhouse((95, 65, 48), (215, 195, 165)), "prop_townhouse_brown.png")
    save(stall((220, 50, 50)), "prop_stall.png")
    save(stall((50, 90, 200)), "prop_stall_blue.png")
    save(train(), "prop_train.png")
    save(lighthouse(), "prop_lighthouse.png")
    save(statue(), "prop_statue.png")
    save(fence(), "prop_fence.png")
    save(bridge(), "prop_bridge.png")
    save(boat(), "prop_boat.png")
    save(waterfall(), "prop_waterfall.png")
    save(ruins(), "prop_ruins.png")


if __name__ == "__main__":
    main()
