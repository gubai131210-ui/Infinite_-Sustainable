"""P41–P43: sky clouds + hand-drawn roof facades (not recolor)."""
from __future__ import annotations

from pathlib import Path
import random

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"
rng = random.Random(33)


def px(img: Image.Image, x: int, y: int, c: tuple) -> None:
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), c)


def cloud(name: str, w: int = 48, h: int = 20) -> None:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    blobs = [(8, 8, 22, 18), (16, 4, 34, 16), (28, 8, 44, 18)]
    for b in blobs:
        d.ellipse(b, fill=(245, 248, 255, 200))
    path = PROC / name
    img.save(path)
    print("OK", path.name)


def house(name: str, wall: tuple, roof: tuple, w: int = 64, h: int = 72, accent: tuple | None = None) -> None:
    """Simple but distinct timber house with clear roof silhouette."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Roof triangle / trapezoid
    peak = (w // 2, 4)
    d.polygon([(6, 28), peak, (w - 6, 28)], fill=roof)
    d.polygon([(4, 28), (w - 4, 28), (w - 8, 36), (8, 36)], fill=tuple(max(0, c - 20) for c in roof[:3]) + (255,))
    # Chimney
    d.rectangle((w // 2 + 10, 10, w // 2 + 16, 28), fill=(110, 100, 95, 255))
    d.rectangle((w // 2 + 9, 8, w // 2 + 17, 12), fill=(90, 82, 78, 255))
    # Walls
    d.rectangle((10, 36, w - 10, h - 4), fill=wall)
    # Timber frame
    frame = (70, 55, 40, 255)
    d.rectangle((10, 36, w - 10, h - 4), outline=frame, width=2)
    d.line([(w // 2, 36), (w // 2, h - 4)], fill=frame, width=2)
    d.line([(10, 52), (w - 10, 52)], fill=frame, width=1)
    # Door
    door = accent or (90, 70, 50, 255)
    d.rectangle((w // 2 - 6, h - 22, w // 2 + 6, h - 4), fill=door)
    # Windows
    win = (180, 210, 230, 255)
    d.rectangle((16, 42, 26, 50), fill=win)
    d.rectangle((w - 26, 42, w - 16, 50), fill=win)
    d.line([(21, 42), (21, 50)], fill=(120, 140, 160, 255))
    d.line([(w - 21, 42), (w - 21, 50)], fill=(120, 140, 160, 255))
    # Foundation
    d.rectangle((8, h - 6, w - 8, h - 2), fill=(100, 95, 90, 255))
    path = PROC / name
    img.save(path)
    print("OK", path.name)


def shop_facade(name: str, roof: tuple, awning: tuple) -> None:
    w, h = 80, 68
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(4, 22), (40, 4), (76, 22)], fill=roof)
    d.rectangle((8, 22, 72, h - 4), fill=(210, 195, 170, 255))
    d.rectangle((8, 22, 72, h - 4), outline=(90, 70, 50, 255), width=2)
    # Awning stripes
    for i, x0 in enumerate(range(12, 68, 8)):
        c = awning if i % 2 == 0 else (245, 245, 245, 255)
        d.rectangle((x0, 28, x0 + 7, 36), fill=c)
    d.rectangle((30, h - 24, 50, h - 4), fill=(100, 70, 45, 255))
    d.rectangle((14, 40, 26, 50), fill=(170, 210, 230, 255))
    d.rectangle((54, 40, 66, 50), fill=(170, 210, 230, 255))
    img.save(PROC / name)
    print("OK", name)


def main() -> None:
    cloud("prop_cloud_0.png", 48, 18)
    cloud("prop_cloud_1.png", 56, 20)
    cloud("prop_cloud_2.png", 40, 16)
    house("prop_house_redroof.png", (220, 200, 175, 255), (168, 72, 58, 255), accent=(120, 60, 40, 255))
    house("prop_house_slateroof.png", (200, 205, 210, 255), (75, 90, 115, 255), accent=(60, 70, 90, 255))
    house("prop_house_thatch.png", (215, 195, 160, 255), (140, 120, 70, 255), accent=(100, 80, 45, 255))
    house("prop_house_greenroof.png", (205, 210, 185, 255), (70, 120, 80, 255), accent=(55, 90, 60, 255))
    shop_facade("prop_shop_awning.png", (150, 65, 50, 255), (200, 60, 55, 255))
    shop_facade("prop_cafe_awning.png", (45, 115, 120, 255), (50, 140, 145, 255))
    # Soft sky strip for overview north edge
    sky = Image.new("RGBA", (128, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(sky)
    for y in range(32):
        t = y / 31.0
        r = int(160 + 40 * t)
        g = int(195 + 25 * t)
        b = int(235 - 10 * t)
        d.line([(0, y), (127, y)], fill=(r, g, b, 90))
    sky.save(PROC / "prop_sky_band.png")
    print("OK prop_sky_band.png")
    print("P41-P43 assets done")


if __name__ == "__main__":
    main()
