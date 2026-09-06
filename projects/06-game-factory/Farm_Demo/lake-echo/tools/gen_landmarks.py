"""High-detail landmark props for Lake Echo zones."""
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
            board.putpixel((x, y), (220, 220, 220, 255) if ((x // 8) + (y // 8)) % 2 == 0 else (160, 160, 160, 255))
    board.alpha_composite(img)
    board.convert("RGB").save(QA / f"checker_{name}", quality=92)
    print("OK", name, img.size)


def barn(w=112, h=88) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([10, 32, w - 10, h - 6], fill=(168, 48, 42, 255), outline=(90, 30, 28, 255))
    d.polygon([(10, 32), (w // 2, 6), (w - 10, 32)], fill=(92, 68, 48, 255))
    # white trim
    d.rectangle([14, 36, w - 14, 40], fill=(230, 220, 210, 255))
    d.rectangle([w // 2 - 10, 48, w // 2 + 10, h - 6], fill=(70, 42, 28, 255))
    d.rectangle([18, 44, 34, 56], fill=(200, 220, 240, 255))
    d.rectangle([w - 34, 44, w - 18, 56], fill=(200, 220, 240, 255))
    # loft window
    d.ellipse([w // 2 - 8, 18, w // 2 + 8, 30], fill=(40, 30, 25, 255))
    return img


def silo() -> Image.Image:
    img = Image.new("RGBA", (36, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 2, 32, 18], fill=(190, 55, 48, 255))
    d.rectangle([6, 10, 30, 74], fill=(175, 48, 42, 255), outline=(100, 30, 28, 255))
    for y in (22, 36, 50, 64):
        d.rectangle([8, y, 28, y + 2], fill=(140, 40, 36, 255))
    d.rectangle([14, 16, 22, 20], fill=(130, 130, 140, 255))
    return img


def townhouse(roof=(140, 70, 55), wall=(220, 205, 175)) -> Image.Image:
    img = Image.new("RGBA", (72, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([6, 24, 66, 60], fill=(*wall, 255), outline=(90, 70, 50, 255))
    d.polygon([(6, 24), (36, 4), (66, 24)], fill=(*roof, 255))
    d.rectangle([30, 38, 42, 60], fill=(80, 50, 35, 255))
    d.rectangle([12, 30, 22, 40], fill=(150, 195, 230, 255))
    d.rectangle([50, 30, 60, 40], fill=(150, 195, 230, 255))
    d.rectangle([52, 8, 60, 22], fill=(120, 110, 100, 255))
    # timber beam
    d.rectangle([6, 24, 66, 27], fill=(70, 50, 35, 255))
    return img


def stall(awning=(220, 50, 50)) -> Image.Image:
    img = Image.new("RGBA", (48, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([4, 18, 44, 38], fill=(150, 110, 70, 255))
    for x in range(4, 44, 5):
        col = (*awning, 255) if ((x // 5) % 2) == 0 else (245, 245, 245, 255)
        d.rectangle([x, 4, x + 5, 20], fill=col)
    d.rectangle([8, 22, 18, 28], fill=(200, 80, 60, 255))
    d.rectangle([22, 22, 32, 28], fill=(240, 220, 100, 255))
    return img


def train() -> Image.Image:
    img = Image.new("RGBA", (120, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([6, 14, 44, 36], fill=(28, 28, 32, 255))
    d.rectangle([44, 16, 112, 34], fill=(130, 70, 48, 255))
    d.rectangle([48, 18, 60, 28], fill=(180, 200, 220, 255))
    d.rectangle([70, 18, 82, 28], fill=(180, 200, 220, 255))
    d.rectangle([92, 18, 104, 28], fill=(180, 200, 220, 255))
    d.ellipse([10, 30, 24, 44], fill=(20, 20, 20, 255))
    d.ellipse([28, 30, 42, 44], fill=(20, 20, 20, 255))
    d.rectangle([16, 2, 30, 14], fill=(45, 45, 50, 255))
    # smoke puffs
    d.ellipse([18, 0, 28, 8], fill=(220, 220, 220, 180))
    d.ellipse([26, 0, 36, 10], fill=(200, 200, 200, 140))
    return img


def lighthouse() -> Image.Image:
    img = Image.new("RGBA", (48, 112), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([8, 100, 40, 110], fill=(100, 90, 80, 255))
    y = 20
    while y < 100:
        col = (220, 45, 45, 255) if ((y // 10) % 2) == 0 else (245, 245, 245, 255)
        d.rectangle([14, y, 34, y + 10], fill=col)
        y += 10
    d.rectangle([12, 12, 36, 22], fill=(255, 230, 90, 255))
    d.polygon([(12, 12), (24, 2), (36, 12)], fill=(190, 40, 40, 255))
    d.rectangle([22, 14, 26, 20], fill=(255, 255, 200, 255))
    return img


def statue() -> Image.Image:
    img = Image.new("RGBA", (32, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([4, 36, 28, 46], fill=(110, 110, 118, 255))
    d.rectangle([8, 32, 24, 36], fill=(130, 130, 138, 255))
    d.rectangle([12, 14, 20, 32], fill=(150, 150, 158, 255))
    d.ellipse([10, 4, 22, 16], fill=(150, 150, 158, 255))
    return img


def fence() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 5, 16, 7], fill=(130, 95, 55, 255))
    d.rectangle([0, 10, 16, 12], fill=(130, 95, 55, 255))
    d.rectangle([2, 3, 4, 14], fill=(100, 70, 40, 255))
    d.rectangle([12, 3, 14, 14], fill=(100, 70, 40, 255))
    return img


def bridge() -> Image.Image:
    img = Image.new("RGBA", (64, 28), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 12, 64, 24], fill=(120, 88, 52, 255))
    for x in range(0, 64, 8):
        d.rectangle([x, 12, x + 6, 24], fill=(105, 75, 45, 255))
    d.rectangle([0, 2, 4, 24], fill=(90, 65, 40, 255))
    d.rectangle([60, 2, 64, 24], fill=(90, 65, 40, 255))
    d.rectangle([0, 2, 64, 5], fill=(140, 105, 65, 255))
    return img


def boat() -> Image.Image:
    img = Image.new("RGBA", (40, 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(2, 12), (36, 12), (30, 18), (8, 18)], fill=(110, 70, 40, 255))
    d.rectangle([18, 2, 20, 12], fill=(80, 60, 40, 255))
    d.polygon([(20, 2), (32, 8), (20, 10)], fill=(240, 240, 245, 255))
    return img


def waterfall() -> Image.Image:
    img = Image.new("RGBA", (48, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 48, 16], fill=(118, 102, 84, 255))
    for x in range(8, 40, 4):
        d.rectangle([x, 14, x + 2, 58], fill=(140, 200, 240, 200))
    d.ellipse([10, 52, 38, 62], fill=(70, 140, 200, 220))
    return img


def main() -> None:
    save(barn(), "prop_barn.png")
    save(barn(100, 80), "prop_barn2.png")
    save(silo(), "prop_silo.png")
    save(townhouse(), "prop_farmhouse.png")
    save(townhouse((70, 90, 130), (235, 225, 210)), "prop_townhouse_blue.png")
    save(townhouse((90, 60, 50), (210, 190, 160)), "prop_townhouse_brown.png")
    save(stall((220, 50, 50)), "prop_stall.png")
    save(stall((50, 90, 200)), "prop_stall_blue.png")
    save(train(), "prop_train.png")
    save(lighthouse(), "prop_lighthouse.png")
    save(statue(), "prop_statue.png")
    save(fence(), "prop_fence.png")
    save(bridge(), "prop_bridge.png")
    save(boat(), "prop_boat.png")
    save(waterfall(), "prop_waterfall.png")


if __name__ == "__main__":
    main()
