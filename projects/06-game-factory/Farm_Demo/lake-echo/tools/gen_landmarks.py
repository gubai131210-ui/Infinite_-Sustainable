"""Procedural landmark sprites for Wave1+ (identifiable silhouettes)."""
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


def barn() -> Image.Image:
    img = Image.new("RGBA", (96, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([8, 28, 88, 76], fill=(170, 55, 48, 255))
    d.polygon([(8, 28), (48, 8), (88, 28)], fill=(90, 70, 55, 255))
    d.rectangle([40, 44, 56, 76], fill=(60, 40, 30, 255))
    d.rectangle([16, 36, 28, 48], fill=(200, 210, 230, 255))
    d.rectangle([68, 36, 80, 48], fill=(200, 210, 230, 255))
    return img


def silo() -> Image.Image:
    img = Image.new("RGBA", (32, 72), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([4, 4, 28, 20], fill=(190, 60, 50, 255))
    d.rectangle([6, 12, 26, 68], fill=(175, 50, 45, 255))
    d.rectangle([10, 20, 22, 24], fill=(120, 120, 130, 255))
    return img


def farmhouse() -> Image.Image:
    img = Image.new("RGBA", (64, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([6, 22, 58, 54], fill=(210, 190, 150, 255))
    d.polygon([(6, 22), (32, 4), (58, 22)], fill=(140, 70, 55, 255))
    d.rectangle([26, 34, 38, 54], fill=(80, 50, 35, 255))
    d.rectangle([12, 28, 20, 36], fill=(160, 200, 230, 255))
    d.rectangle([44, 28, 52, 36], fill=(160, 200, 230, 255))
    d.rectangle([48, 10, 56, 22], fill=(120, 110, 100, 255))  # chimney
    return img


def stall() -> Image.Image:
    img = Image.new("RGBA", (40, 36), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([4, 16, 36, 34], fill=(150, 110, 70, 255))
    for x in range(4, 36, 4):
        col = (220, 60, 60, 255) if (x // 4) % 2 == 0 else (240, 240, 240, 255)
        d.rectangle([x, 6, x + 4, 18], fill=col)
    return img


def train() -> Image.Image:
    img = Image.new("RGBA", (96, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([8, 12, 40, 32], fill=(30, 30, 35, 255))
    d.rectangle([40, 14, 88, 30], fill=(120, 70, 50, 255))
    d.ellipse([12, 26, 24, 38], fill=(20, 20, 20, 255))
    d.ellipse([28, 26, 40, 38], fill=(20, 20, 20, 255))
    d.rectangle([16, 4, 28, 12], fill=(50, 50, 55, 255))  # stack
    return img


def lighthouse() -> Image.Image:
    img = Image.new("RGBA", (40, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(20, 88, 10):
        col = (220, 50, 50, 255) if ((y // 10) % 2) == 0 else (240, 240, 240, 255)
        d.rectangle([12, y, 28, y + 10], fill=col)
    d.rectangle([10, 12, 30, 22], fill=(240, 220, 80, 255))
    d.polygon([(10, 12), (20, 2), (30, 12)], fill=(180, 50, 50, 255))
    d.rectangle([8, 88, 32, 94], fill=(100, 90, 80, 255))
    return img


def statue() -> Image.Image:
    img = Image.new("RGBA", (24, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([4, 28, 20, 38], fill=(120, 120, 125, 255))
    d.rectangle([8, 12, 16, 28], fill=(150, 150, 155, 255))
    d.ellipse([7, 4, 17, 14], fill=(150, 150, 155, 255))
    return img


def fence_h() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 6, 16, 8], fill=(130, 95, 55, 255))
    d.rectangle([0, 11, 16, 13], fill=(130, 95, 55, 255))
    d.rectangle([2, 4, 4, 14], fill=(100, 70, 40, 255))
    d.rectangle([12, 4, 14, 14], fill=(100, 70, 40, 255))
    return img


def bridge_prop() -> Image.Image:
    img = Image.new("RGBA", (48, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 10, 48, 20], fill=(110, 80, 50, 255))
    d.rectangle([0, 4, 4, 20], fill=(90, 65, 40, 255))
    d.rectangle([44, 4, 48, 20], fill=(90, 65, 40, 255))
    return img


def main() -> None:
    save(barn(), "prop_barn.png")
    save(silo(), "prop_silo.png")
    save(farmhouse(), "prop_farmhouse.png")
    save(stall(), "prop_stall.png")
    save(train(), "prop_train.png")
    save(lighthouse(), "prop_lighthouse.png")
    save(statue(), "prop_statue.png")
    save(fence_h(), "prop_fence.png")
    save(bridge_prop(), "prop_bridge.png")


if __name__ == "__main__":
    main()
