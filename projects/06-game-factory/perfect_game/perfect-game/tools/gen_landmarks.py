"""High-detail landmark props — shaded pixel art for Oakhaven town + lake."""
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


def _shade_rect(d, box, base, dark, light) -> None:
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=base)
    d.rectangle([x0, y0, x0 + 1, y1], fill=light)
    d.rectangle([x0, y0, x1, y0 + 1], fill=light)
    d.rectangle([x1 - 1, y0, x1, y1], fill=dark)
    d.rectangle([x0, y1 - 1, x1, y1], fill=dark)


def barn(w=120, h=100) -> Image.Image:
    """Stardew-like red barn — plank walls, loft door, stone footing, dual doors."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Grounding shadow
    d.ellipse([10, h - 8, w - 10, h - 1], fill=(40, 40, 50, 55))
    # Stone footing
    d.rectangle([6, h - 14, w - 6, h - 5], fill=(118, 112, 104, 255))
    for x in range(8, w - 8, 8):
        d.rectangle([x, h - 12, x + 6, h - 6], fill=(138, 132, 122, 255))
        d.line([(x + 6, h - 12), (x + 6, h - 6)], fill=(90, 85, 78, 255))
    # Wall body with left light / right dark
    wall = (168, 52, 44, 255)
    wall_d = (120, 32, 28, 255)
    wall_l = (200, 85, 72, 255)
    _shade_rect(d, (8, 28, w - 8, h - 12), wall, wall_d, wall_l)
    # Vertical planks
    for x in range(12, w - 12, 5):
        d.line([(x, 30), (x, h - 14)], fill=(140, 40, 36, 140), width=1)
        if x % 10 == 2:
            d.line([(x + 1, 32), (x + 1, h - 16)], fill=(210, 100, 88, 70), width=1)
    # Cross beams
    d.rectangle([8, 40, w - 8, 43], fill=(90, 48, 38, 255))
    d.rectangle([8, 62, w - 8, 65], fill=(90, 48, 38, 255))
    # Gable roof (brown shingles)
    mid = w // 2
    d.polygon([(4, 30), (mid, 2), (w - 4, 30)], fill=(78, 52, 34, 255))
    d.polygon([(12, 30), (mid, 8), (w - 12, 30)], fill=(102, 72, 46, 255))
    d.line([(4, 30), (mid, 2)], fill=(45, 30, 20, 255))
    d.line([(w - 4, 30), (mid, 2)], fill=(45, 30, 20, 255))
    for i, y in enumerate(range(8, 28, 3)):
        inset = 8 + i * 5
        d.line([(inset, y), (w - inset, y)], fill=(60, 40, 28, 150))
    # White fascia board
    d.rectangle([8, 28, w - 8, 32], fill=(235, 228, 215, 255))
    d.line([(8, 32), (w - 8, 32)], fill=(180, 170, 155, 255))
    # Loft round window
    d.ellipse([mid - 10, 10, mid + 10, 26], fill=(48, 36, 28, 255), outline=(30, 22, 16, 255))
    d.ellipse([mid - 7, 13, mid + 7, 23], fill=(160, 195, 220, 255))
    d.line([(mid, 13), (mid, 23)], fill=(55, 40, 30, 255))
    d.line([(mid - 7, 18), (mid + 7, 18)], fill=(55, 40, 30, 255))
    # Main double doors
    door_l, door_r = mid - 16, mid + 16
    d.rectangle([door_l, 48, door_r, h - 12], fill=(62, 38, 26, 255), outline=(38, 22, 14, 255))
    d.line([(mid, 48), (mid, h - 12)], fill=(95, 62, 42, 255))
    for y in range(52, h - 16, 4):
        d.line([(door_l + 2, y), (mid - 2, y)], fill=(78, 48, 32, 180))
        d.line([(mid + 2, y), (door_r - 2, y)], fill=(78, 48, 32, 180))
    d.ellipse([mid + 8, 66, mid + 12, 70], fill=(190, 160, 70, 255))
    d.ellipse([mid - 12, 66, mid - 8, 70], fill=(190, 160, 70, 255))
    # Side windows with shutters
    for ox in (14, w - 30):
        d.rectangle([ox - 2, 46, ox + 16, 60], fill=(70, 45, 35, 255))
        d.rectangle([ox, 48, ox + 14, 58], fill=(170, 205, 230, 255), outline=(55, 40, 30, 255))
        d.line([(ox + 7, 48), (ox + 7, 58)], fill=(55, 40, 30, 255))
        d.line([(ox, 53), (ox + 14, 53)], fill=(55, 40, 30, 255))
        # shutters
        d.rectangle([ox - 5, 48, ox - 1, 58], fill=(90, 110, 70, 255))
        d.rectangle([ox + 15, 48, ox + 19, 58], fill=(90, 110, 70, 255))
    return img


def silo() -> Image.Image:
    """Cylindrical metal/wood silo with dome cap — not a flat red pillar."""
    w, h = 48, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([6, h - 10, w - 6, h - 2], fill=(40, 40, 50, 50))
    # Dome cap
    d.ellipse([4, 2, w - 4, 28], fill=(175, 58, 48, 255), outline=(110, 35, 30, 255))
    d.ellipse([10, 6, w - 10, 22], fill=(220, 95, 78, 255))
    d.ellipse([16, 10, w - 16, 18], fill=(240, 140, 120, 180))
    # Cylinder with horizontal bands + left highlight
    for y in range(18, h - 12):
        t = (y - 18) / float(h - 30)
        shade = int(155 + 40 * (1.0 - t))
        d.rectangle([8, y, w - 8, y + 1], fill=(shade, 48, 42, 255))
        d.rectangle([8, y, 14, y + 1], fill=(min(255, shade + 45), 85, 72, 255))
        d.rectangle([w - 14, y, w - 8, y + 1], fill=(max(0, shade - 35), 30, 28, 255))
    for y in (28, 42, 56, 70):
        d.rectangle([9, y, w - 9, y + 2], fill=(130, 40, 36, 255))
        d.rectangle([9, y, 15, y + 2], fill=(190, 80, 70, 200))
    # Access hatch
    d.rectangle([w // 2 - 6, 22, w // 2 + 6, 32], fill=(85, 90, 100, 255), outline=(45, 48, 52, 255))
    d.rectangle([w // 2 - 3, 24, w // 2 + 3, 30], fill=(55, 58, 65, 255))
    # Base ring
    d.rectangle([6, h - 14, w - 6, h - 8], fill=(85, 75, 65, 255))
    d.rectangle([10, h - 12, w - 10, h - 9], fill=(110, 100, 88, 255))
    return img


def townhouse(
    roof=(140, 70, 55),
    wall=(220, 205, 175),
    accent=(70, 50, 35),
    shutter=None,
    dormer: bool = True,
    width: int = 88,
    height: int = 80,
) -> Image.Image:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([8, height - 8, width - 8, height - 2], fill=(40, 50, 30, 60))
    d.rectangle([4, height - 16, width - 4, height - 6], fill=(118, 112, 104, 255))
    for x in range(6, width - 6, 7):
        d.rectangle([x, height - 14, x + 5, height - 8], fill=(138, 132, 122, 255))
        d.line([(x + 5, height - 14), (x + 5, height - 8)], fill=(90, 85, 78, 255))
    _shade_rect(
        d,
        (6, 26, width - 6, height - 14),
        (*wall, 255),
        (max(0, wall[0] - 40), max(0, wall[1] - 40), max(0, wall[2] - 40), 255),
        (min(255, wall[0] + 20), min(255, wall[1] + 20), min(255, wall[2] + 15), 255),
    )
    for y in range(30, height - 16, 5):
        d.line([(8, y), (width - 8, y)], fill=(wall[0] - 15, wall[1] - 15, wall[2] - 12, 90))
    timber = (*accent, 255)
    d.rectangle([6, 26, width - 6, 30], fill=timber)
    d.rectangle([6, 44, width - 6, 47], fill=timber)
    d.rectangle([width // 2 - 2, 26, width // 2 + 2, height - 14], fill=timber)
    d.rectangle([6, 26, 10, height - 14], fill=timber)
    d.rectangle([width - 10, 26, width - 6, height - 14], fill=timber)
    mid = width // 2
    roof_hi = (min(255, roof[0] + 30), min(255, roof[1] + 22), min(255, roof[2] + 18))
    d.polygon([(2, 28), (mid, 2), (width - 2, 28)], fill=(*roof, 255))
    d.polygon([(10, 28), (mid, 8), (width - 10, 28)], fill=(*roof_hi, 255))
    d.line([(2, 28), (mid, 2)], fill=(50, 35, 25, 255))
    d.line([(width - 2, 28), (mid, 2)], fill=(50, 35, 25, 255))
    for i, y in enumerate(range(10, 26, 4)):
        inset = 6 + i * 4
        d.line([(inset, y), (width - inset, y)], fill=(roof[0] - 25, roof[1] - 20, roof[2] - 15, 160))
    cx = width - 22
    d.rectangle([cx, 6, cx + 10, 26], fill=(120, 110, 100, 255))
    d.rectangle([cx - 1, 4, cx + 11, 8], fill=(95, 88, 80, 255))
    d.rectangle([cx + 2, 8, cx + 5, 12], fill=(70, 70, 75, 255))
    if dormer:
        dw = mid - 8
        d.polygon([(dw, 14), (dw + 8, 8), (dw + 16, 14)], fill=(*roof_hi, 255))
        d.rectangle([dw + 3, 14, dw + 13, 22], fill=(150, 190, 220, 255), outline=(60, 45, 35, 255))
        d.line([(dw + 8, 14), (dw + 8, 22)], fill=(60, 45, 35, 255))
    door_x = mid - 7
    d.rectangle([door_x - 2, height - 30, door_x + 16, height - 14], fill=(90, 70, 50, 255))
    d.rectangle([door_x, height - 28, door_x + 14, height - 14], fill=(72, 45, 28, 255))
    d.rectangle([door_x + 2, height - 26, door_x + 12, height - 20], fill=(95, 60, 40, 255))
    d.ellipse([door_x + 10, height - 22, door_x + 13, height - 19], fill=(210, 175, 70, 255))
    d.rectangle([door_x - 3, height - 14, door_x + 17, height - 12], fill=(100, 95, 88, 255))
    for ox in (14, width - 28):
        if shutter:
            d.rectangle([ox - 4, 32, ox, 44], fill=(*shutter, 255))
            d.rectangle([ox + 14, 32, ox + 18, 44], fill=(*shutter, 255))
        d.rectangle([ox, 32, ox + 14, 44], fill=(135, 185, 225, 255), outline=(55, 40, 30, 255))
        d.line([(ox + 7, 32), (ox + 7, 44)], fill=(55, 40, 30, 255))
        d.line([(ox, 38), (ox + 14, 38)], fill=(55, 40, 30, 255))
        d.rectangle([ox - 1, 44, ox + 15, 46], fill=(90, 70, 50, 255))
        d.rectangle([ox + 1, 33, ox + 4, 36], fill=(220, 235, 250, 180))
    ox = 14
    d.rectangle([ox, 50, ox + 14, 58], fill=(125, 175, 210, 255), outline=(55, 40, 30, 255))
    d.line([(ox + 7, 50), (ox + 7, 58)], fill=(55, 40, 30, 255))
    d.rectangle([12, 44, 30, 48], fill=(90, 120, 55, 255))
    for fx in (14, 18, 22, 26):
        d.point((fx, 45), fill=(220, 70, 90, 255) if fx % 8 == 0 else (240, 220, 80, 255))
    return img


def stall(awning=(220, 50, 50), goods: bool = True) -> Image.Image:
    img = Image.new("RGBA", (64, 52), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 46, 60, 52], fill=(40, 50, 30, 50))
    _shade_rect(d, (4, 24, 60, 46), (135, 98, 62, 255), (90, 60, 35, 255), (170, 130, 90, 255))
    for x in range(8, 56, 5):
        d.line([(x, 26), (x, 44)], fill=(110, 80, 50, 100))
    for x in (6, 56):
        d.rectangle([x, 14, x + 3, 46], fill=(95, 68, 42, 255))
        d.rectangle([x, 14, x + 3, 16], fill=(150, 120, 80, 255))
    for x in range(2, 62, 5):
        col = (*awning, 255) if ((x // 5) % 2) == 0 else (248, 248, 250, 255)
        d.polygon([(x, 4), (x + 5, 4), (x + 4, 22), (x + 1, 22)], fill=col)
    for x in range(4, 60, 6):
        d.ellipse([x, 20, x + 5, 26], fill=(*awning, 255) if ((x // 6) % 2) == 0 else (248, 248, 250, 255))
    d.rectangle([2, 4, 62, 6], fill=(80, 55, 35, 255))
    if goods:
        d.rectangle([8, 28, 22, 38], fill=(200, 65, 50, 255), outline=(120, 40, 30, 255))
        d.ellipse([10, 26, 14, 30], fill=(230, 80, 60, 255))
        d.ellipse([14, 25, 18, 29], fill=(240, 90, 70, 255))
        d.rectangle([24, 28, 38, 38], fill=(235, 200, 70, 255), outline=(160, 130, 40, 255))
        d.ellipse([26, 26, 32, 32], fill=(250, 220, 90, 255))
        d.rectangle([40, 28, 52, 36], fill=(80, 150, 85, 255), outline=(40, 90, 45, 255))
        d.rectangle([42, 26, 50, 28], fill=(100, 170, 90, 255))
        d.rectangle([26, 8, 38, 16], fill=(90, 60, 40, 255))
        d.rectangle([28, 10, 36, 14], fill=(220, 200, 160, 255))
    return img


def train() -> Image.Image:
    img = Image.new("RGBA", (140, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 44, 140, 48], fill=(70, 70, 75, 180))
    _shade_rect(d, (4, 16, 48, 40), (36, 36, 42, 255), (18, 18, 22, 255), (70, 70, 80, 255))
    d.rectangle([10, 8, 28, 16], fill=(50, 50, 58, 255))
    d.rectangle([12, 10, 20, 15], fill=(160, 190, 220, 255))
    d.rectangle([30, 4, 38, 16], fill=(45, 45, 50, 255))
    d.ellipse([32, 0, 44, 10], fill=(210, 210, 215, 160))
    d.ellipse([38, 0, 50, 12], fill=(190, 190, 195, 120))
    d.polygon([(4, 36), (0, 44), (12, 40)], fill=(90, 90, 100, 255))
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
    w, h = 64, 144
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon(
        [(4, h - 8), (60, h - 8), (54, h - 22), (48, h - 18), (36, h - 26), (22, h - 20), (10, h - 24)],
        fill=(95, 90, 82, 255),
    )
    d.polygon([(8, h - 10), (56, h - 10), (50, h - 18), (14, h - 18)], fill=(120, 115, 105, 255))
    for rx, ry in ((12, h - 16), (28, h - 20), (44, h - 14), (18, h - 12)):
        d.ellipse([rx, ry, rx + 10, ry + 6], fill=(80, 78, 72, 255))
    for gx in (16, 30, 42):
        d.rectangle([gx, h - 24, gx + 2, h - 20], fill=(70, 120, 55, 255))
    bands = list(range(28, 118, 9))
    for i, y in enumerate(bands):
        t = (118 - y) / 100.0
        inset = int(3 + t * 6)
        red = i % 2 == 0
        base = (210, 42, 42, 255) if red else (250, 250, 252, 255)
        dark = (150, 28, 28, 255) if red else (190, 190, 198, 255)
        light = (245, 110, 100, 255) if red else (255, 255, 255, 255)
        _shade_rect(d, (8 + inset, y, w - 8 - inset, y + 9), base, dark, light)
        d.point((10 + inset, y + 4), fill=dark)
        d.point((w - 12 - inset, y + 4), fill=dark)
        if (not red) and 40 < y < 100:
            cx = w // 2
            d.rectangle([cx - 4, y + 2, cx + 4, y + 7], fill=(35, 45, 65, 255), outline=(25, 30, 40, 255))
            d.rectangle([cx - 3, y + 3, cx - 1, y + 5], fill=(180, 200, 220, 120))
    d.rectangle([w // 2 - 6, 108, w // 2 + 6, 118], fill=(55, 40, 30, 255), outline=(30, 22, 18, 255))
    d.ellipse([w // 2 + 2, 112, w // 2 + 4, 114], fill=(200, 170, 60, 255))
    d.rectangle([10, 26, 54, 30], fill=(200, 200, 210, 255), outline=(120, 120, 130, 255))
    for x in range(12, 54, 4):
        d.rectangle([x, 24, x + 1, 30], fill=(160, 160, 170, 255))
    d.rectangle([16, 12, 48, 26], fill=(255, 220, 90, 255), outline=(180, 140, 40, 255))
    for wx in (20, 28, 36):
        d.rectangle([wx, 14, wx + 5, 24], fill=(255, 250, 200, 255))
        d.rectangle([wx + 1, 15, wx + 3, 18], fill=(255, 255, 240, 200))
    d.polygon([(16, 12), (32, 2), (48, 12)], fill=(200, 45, 45, 255))
    d.polygon([(20, 12), (32, 5), (44, 12)], fill=(230, 70, 70, 255))
    d.rectangle([30, 0, 34, 4], fill=(180, 40, 40, 255))
    d.ellipse([29, 0, 35, 3], fill=(255, 220, 80, 255))
    for a, dy in ((40, 8), (60, 14), (80, 20)):
        d.polygon([(32, 18), (w - 2, 18 + dy), (w - 2, 22 + dy)], fill=(255, 240, 150, a))
    return img


def statue() -> Image.Image:
    img = Image.new("RGBA", (40, 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    _shade_rect(d, (2, 44, 38, 58), (105, 105, 112, 255), (70, 70, 78, 255), (150, 150, 158, 255))
    d.rectangle([6, 40, 34, 44], fill=(130, 130, 138, 255))
    d.rectangle([12, 48, 28, 54], fill=(160, 140, 80, 255))
    _shade_rect(d, (14, 18, 26, 40), (155, 155, 165, 255), (110, 110, 120, 255), (190, 190, 200, 255))
    d.ellipse([12, 6, 28, 20], fill=(160, 160, 170, 255))
    d.rectangle([10, 22, 14, 34], fill=(145, 145, 155, 255))
    d.rectangle([26, 22, 30, 34], fill=(145, 145, 155, 255))
    d.rectangle([14, 8, 17, 12], fill=(200, 200, 210, 255))
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
        d.rectangle(
            [x, 14, x + 5, 28],
            fill=(100, 72, 42, 255) if (x // 7) % 2 == 0 else (130, 95, 55, 255),
        )
    d.rectangle([0, 2, 5, 28], fill=(85, 60, 35, 255))
    d.rectangle([67, 2, 72, 28], fill=(85, 60, 35, 255))
    d.rectangle([0, 2, 72, 6], fill=(145, 110, 70, 255))
    d.rectangle([0, 6, 72, 8], fill=(90, 65, 40, 255))
    return img


def boat() -> Image.Image:
    img = Image.new("RGBA", (56, 28), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 20, 52, 28], fill=(60, 120, 170, 80))
    d.polygon([(2, 16), (50, 16), (44, 24), (8, 24)], fill=(95, 60, 35, 255))
    d.polygon([(6, 16), (48, 16), (42, 20), (10, 20)], fill=(135, 95, 55, 255))
    d.rectangle([24, 2, 26, 16], fill=(70, 55, 35, 255))
    d.polygon([(26, 2), (48, 12), (26, 14)], fill=(250, 250, 255, 255))
    d.line([(26, 2), (26, 14)], fill=(180, 180, 195, 255))
    d.rectangle([12, 12, 20, 16], fill=(70, 100, 140, 255))
    return img


def waterfall() -> Image.Image:
    img = Image.new("RGBA", (64, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 64, 22], fill=(105, 95, 80, 255))
    for x in range(0, 64, 5):
        d.rectangle(
            [x, 2, x + 3, 20],
            fill=(125, 115, 95, 255) if (x // 5) % 2 == 0 else (90, 82, 70, 255),
        )
    d.rectangle([4, 18, 60, 24], fill=(70, 65, 55, 255))
    for x, a in ((12, 200), (18, 160), (24, 220), (30, 180), (36, 210), (42, 150), (48, 190)):
        d.rectangle([x, 22, x + 3, 68], fill=(150, 210, 245, a))
        d.rectangle([x + 1, 26, x + 2, 64], fill=(220, 240, 255, min(255, a + 40)))
    d.ellipse([10, 64, 54, 78], fill=(70, 145, 210, 230))
    d.ellipse([18, 66, 46, 74], fill=(160, 220, 255, 180))
    return img


def ruins() -> Image.Image:
    img = Image.new("RGBA", (96, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    moss = (70, 110, 70, 255)
    stone = (130, 125, 115, 255)
    dark = (90, 85, 78, 255)
    _shade_rect(d, (8, 18, 28, 60), stone, dark, (160, 155, 145, 255))
    _shade_rect(d, (68, 18, 88, 60), stone, dark, (160, 155, 145, 255))
    d.arc([8, 4, 88, 48], 180, 360, fill=stone, width=10)
    d.arc([14, 10, 82, 44], 180, 360, fill=dark, width=4)
    for x, y, ww, hh in ((4, 52, 20, 10), (30, 54, 16, 8), (50, 50, 22, 12), (74, 54, 18, 8)):
        d.rectangle([x, y, x + ww, y + hh], fill=dark)
        d.rectangle([x + 2, y + 2, x + ww - 2, y + 4], fill=moss)
    for ox, oy in ((10, 24), (14, 40), (72, 28), (78, 44), (40, 16)):
        d.ellipse([ox, oy, ox + 8, oy + 5], fill=moss)
    return img


def planter() -> Image.Image:
    img = Image.new("RGBA", (32, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    _shade_rect(d, (2, 12, 30, 22), (130, 95, 60, 255), (90, 60, 35, 255), (170, 130, 90, 255))
    d.rectangle([4, 8, 28, 14], fill=(70, 110, 50, 255))
    cols = [(220, 60, 80), (250, 230, 90), (240, 240, 250), (230, 80, 120), (255, 180, 60)]
    for i, x in enumerate(range(6, 28, 4)):
        c = cols[i % len(cols)]
        d.ellipse([x, 4, x + 5, 10], fill=(*c, 255))
        d.rectangle([x + 1, 9, x + 3, 12], fill=(50, 100, 40, 255))
    return img


def flowerbed() -> Image.Image:
    img = Image.new("RGBA", (48, 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 8, 48, 20], fill=(55, 100, 45, 255))
    d.ellipse([4, 6, 44, 16], fill=(70, 120, 55, 255))
    for i, x in enumerate(range(4, 44, 5)):
        c = [(230, 50, 70), (250, 250, 250), (240, 210, 60), (220, 80, 160)][i % 4]
        d.ellipse([x, 2 + ((i % 2) * 2), x + 6, 10 + ((i % 2) * 2)], fill=(*c, 255))
    return img


def pier() -> Image.Image:
    img = Image.new("RGBA", (80, 28), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 20, 80, 28], fill=(70, 140, 200, 60))
    for x in range(0, 80, 8):
        _shade_rect(d, (x, 10, x + 7, 22), (120, 85, 50, 255), (80, 55, 30, 255), (150, 110, 70, 255))
    d.rectangle([0, 8, 80, 12], fill=(145, 105, 65, 255))
    for x in (4, 28, 52, 72):
        d.rectangle([x, 12, x + 3, 26], fill=(85, 60, 35, 255))
    d.rectangle([70, 2, 74, 14], fill=(90, 65, 40, 255))
    d.ellipse([68, 0, 76, 6], fill=(120, 90, 55, 255))
    return img


def rocks() -> Image.Image:
    img = Image.new("RGBA", (40, 28), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([2, 10, 22, 26], fill=(110, 105, 95, 255))
    d.ellipse([14, 6, 38, 24], fill=(130, 125, 115, 255))
    d.ellipse([8, 14, 28, 28], fill=(95, 90, 82, 255))
    d.rectangle([10, 12, 14, 16], fill=(160, 155, 145, 255))
    return img



def shop() -> Image.Image:
    w, h = 96, 72
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([6, h - 6, w - 6, h - 1], fill=(40, 50, 30, 55))
    d.rectangle([4, h - 14, w - 4, h - 6], fill=(110, 105, 98, 255))
    _shade_rect(d, (6, 22, w - 6, h - 14), (235, 220, 195, 255), (180, 160, 130, 255), (250, 240, 220, 255))
    for x in range(6, w - 6, 6):
        col = (40, 140, 70, 255) if (x // 6) % 2 == 0 else (245, 245, 245, 255)
        d.polygon([(x, 14), (x + 6, 14), (x + 5, 24), (x + 1, 24)], fill=col)
    d.rectangle([6, 12, w - 6, 15], fill=(30, 100, 50, 255))
    d.rectangle([12, 28, 58, 52], fill=(150, 195, 230, 255), outline=(60, 45, 30, 255))
    d.line([(35, 28), (35, 52)], fill=(60, 45, 30, 255))
    d.line([(12, 40), (58, 40)], fill=(60, 45, 30, 255))
    d.rectangle([64, 34, 82, h - 14], fill=(90, 55, 35, 255), outline=(50, 30, 20, 255))
    d.ellipse([76, 46, 79, 49], fill=(210, 175, 70, 255))
    d.rectangle([38, 6, 58, 18], fill=(180, 60, 50, 255), outline=(100, 30, 25, 255))
    d.rectangle([42, 9, 54, 15], fill=(245, 230, 180, 255))
    return img


def cafe() -> Image.Image:
    w, h = 96, 72
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([6, h - 6, w - 6, h - 1], fill=(40, 50, 30, 55))
    d.rectangle([4, h - 14, w - 4, h - 6], fill=(110, 105, 98, 255))
    _shade_rect(d, (6, 20, w - 6, h - 14), (245, 235, 220, 255), (190, 170, 145, 255), (255, 250, 240, 255))
    d.polygon([(2, 24), (48, 4), (94, 24)], fill=(120, 70, 45, 255))
    d.polygon([(12, 24), (48, 10), (84, 24)], fill=(150, 95, 60, 255))
    for x in range(10, 70, 5):
        col = (200, 80, 60, 255) if (x // 5) % 2 == 0 else (250, 230, 200, 255)
        d.polygon([(x, 26), (x + 5, 26), (x + 4, 34), (x + 1, 34)], fill=col)
    d.ellipse([14, 36, 36, 56], fill=(150, 195, 230, 255), outline=(70, 50, 35, 255))
    d.rectangle([44, 36, 60, h - 14], fill=(100, 60, 40, 255), outline=(50, 30, 20, 255))
    d.ellipse([68, 48, 86, 58], fill=(140, 100, 60, 255))
    d.rectangle([70, 28, 88, 40], fill=(90, 55, 35, 255))
    return img

def main() -> None:
    save(barn(), "prop_barn.png")
    save(barn(112, 92), "prop_barn2.png")
    save(silo(), "prop_silo.png")
    save(townhouse((110, 70, 50), (235, 220, 195), shutter=(70, 110, 70)), "prop_farmhouse.png")
    save(
        townhouse((65, 100, 150), (238, 228, 210), shutter=(50, 80, 140), accent=(60, 55, 80)),
        "prop_townhouse_blue.png",
    )
    save(townhouse((105, 68, 48), (218, 198, 168), shutter=(120, 70, 45)), "prop_townhouse_brown.png")
    save(townhouse((55, 120, 70), (230, 215, 190), shutter=(40, 90, 50)), "prop_townhouse_green.png")
    save(stall((210, 45, 45)), "prop_stall.png")
    save(stall((45, 85, 200)), "prop_stall_blue.png")
    save(stall((220, 140, 40)), "prop_stall_yellow.png")
    save(train(), "prop_train.png")
    save(lighthouse(), "prop_lighthouse.png")
    save(statue(), "prop_statue.png")
    save(fence(), "prop_fence.png")
    save(bridge(), "prop_bridge.png")
    save(boat(), "prop_boat.png")
    save(waterfall(), "prop_waterfall.png")
    save(ruins(), "prop_ruins.png")
    save(planter(), "prop_planter.png")
    save(flowerbed(), "prop_flowerbed.png")
    save(pier(), "prop_pier.png")
    save(rocks(), "prop_rocks.png")
    save(shop(), "prop_shop.png")
    save(cafe(), "prop_cafe.png")


if __name__ == "__main__":
    main()
