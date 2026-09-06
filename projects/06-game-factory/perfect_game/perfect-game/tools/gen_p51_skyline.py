"""P51–P52: taller sky, big clouds, hero shop/cafe facades."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"


def sky_band() -> None:
    w, h = 192, 72
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(88 + 50 * t)
        g = int(150 + 35 * t)
        b = int(235 - 8 * t)
        a = 255 if y < h - 10 else max(160, 255 - (y - (h - 10)) * 12)
        d.line([(0, y), (w - 1, y)], fill=(r, g, b, a))
    # Soft distant peaks inside sky (haze)
    for i, x0 in enumerate(range(4, w - 30, 34)):
        peak = 38 + (i % 4) * 6
        d.polygon([(x0, h - 1), (x0 + 14, peak), (x0 + 30, h - 1)], fill=(95, 130, 155, 50))
    img.save(PROC / "prop_sky_band.png")
    print("OK sky", w, h)


def cloud(name: str, w: int, h: int) -> None:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((2, h // 3, w // 2 + 4, h - 1), fill=(248, 250, 255, 245))
    d.ellipse((w // 5, 2, w * 3 // 4, h - 3), fill=(255, 255, 255, 250))
    d.ellipse((w // 2 - 2, h // 4, w - 2, h - 1), fill=(245, 248, 255, 240))
    d.ellipse((w // 3, 4, w // 2 + 8, h // 2), fill=(255, 255, 255, 255))
    img.save(PROC / name)
    print("OK", name)


def hero_shop(name: str, roof: tuple, awning_a: tuple, awning_b: tuple, sign: str) -> None:
    """Distinct storefront with porch, sign, and deep awning."""
    w, h = 96, 88
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Roof
    d.polygon([(2, 22), (48, 2), (94, 22)], fill=roof)
    shade = tuple(max(0, c - 30) for c in roof[:3]) + (255,)
    d.polygon([(2, 22), (94, 22), (88, 30), (8, 30)], fill=shade)
    for yy in range(8, 22, 3):
        d.line([(14, yy), (82, yy)], fill=shade, width=1)
    # Chimney
    d.rectangle((70, 8, 80, 26), fill=(100, 92, 88, 255))
    d.ellipse((72, 2, 82, 10), fill=(230, 230, 235, 150))
    # Body
    d.rectangle((10, 30, 86, h - 6), fill=(220, 205, 180, 255))
    d.rectangle((10, 30, 86, h - 6), outline=(80, 60, 45, 255), width=2)
    # Awning scallops
    for i, x0 in enumerate(range(14, 82, 9)):
        c = awning_a if i % 2 == 0 else awning_b
        d.rectangle((x0, 32, x0 + 8, 46), fill=c)
        d.pieslice((x0, 42, x0 + 8, 54), 0, 180, fill=c)
    # Sign
    d.rectangle((28, 48, 68, 58), fill=(90, 70, 45, 255))
    d.rectangle((30, 50, 66, 56), fill=(240, 220, 160, 255))
    # Windows
    for wx in (16, 70):
        d.rectangle((wx, 52, wx + 14, 64), fill=(160, 200, 230, 255))
        d.line([(wx + 7, 52), (wx + 7, 64)], fill=(100, 130, 150, 255))
    # Door
    d.rectangle((42, h - 28, 54, h - 6), fill=(110, 75, 50, 255))
    d.rectangle((50, h - 20, 52, h - 18), fill=(220, 190, 100, 255))
    # Porch step + planter
    d.rectangle((36, h - 8, 60, h - 4), fill=(95, 90, 85, 255))
    d.rectangle((14, h - 12, 26, h - 6), fill=(70, 120, 55, 255))
    d.rectangle((70, h - 12, 82, h - 6), fill=(70, 120, 55, 255))
    img.save(PROC / name)
    print("OK", name, sign)


def house(name: str, wall: tuple, roof: tuple, accent: tuple) -> None:
    w, h = 76, 84
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(4, 24), (w // 2, 2), (w - 4, 24)], fill=roof)
    shade = tuple(max(0, c - 26) for c in roof[:3]) + (255,)
    d.polygon([(4, 24), (w - 4, 24), (w - 10, 32), (10, 32)], fill=shade)
    for yy in range(8, 24, 3):
        d.line([(12, yy), (w - 12, yy)], fill=shade, width=1)
    d.rectangle((w // 2 + 12, 8, w // 2 + 20, 28), fill=(105, 95, 90, 255))
    d.ellipse((w // 2 + 13, 1, w // 2 + 22, 9), fill=(230, 230, 235, 150))
    d.rectangle((10, 32, w - 10, h - 4), fill=wall)
    frame = (68, 52, 38, 255)
    d.rectangle((10, 32, w - 10, h - 4), outline=frame, width=2)
    d.line([(w // 2, 32), (w // 2, h - 4)], fill=frame, width=2)
    d.line([(10, 48), (w - 10, 48)], fill=frame, width=1)
    win = (185, 215, 235, 255)
    for wx in (16, w - 28):
        d.rectangle((wx - 2, 38, wx + 14, 50), fill=(90, 70, 50, 255))
        d.rectangle((wx, 40, wx + 12, 48), fill=win)
    d.rectangle((w // 2 - 7, h - 24, w // 2 + 7, h - 4), fill=accent)
    d.rectangle((14, 50, 30, 54), fill=(70, 120, 60, 255))
    img.save(PROC / name)
    print("OK", name)


def main() -> None:
    sky_band()
    cloud("prop_cloud_0.png", 96, 36)
    cloud("prop_cloud_1.png", 112, 40)
    cloud("prop_cloud_2.png", 80, 32)
    house("prop_house_redroof.png", (222, 200, 172, 255), (168, 68, 52, 255), (115, 55, 38, 255))
    house("prop_house_slateroof.png", (198, 204, 210, 255), (70, 88, 112, 255), (55, 65, 85, 255))
    house("prop_house_thatch.png", (218, 198, 158, 255), (145, 122, 68, 255), (100, 78, 42, 255))
    house("prop_house_greenroof.png", (200, 208, 180, 255), (62, 118, 78, 255), (50, 88, 58, 255))
    hero_shop("prop_shop_awning.png", (148, 58, 46, 255), (200, 55, 50, 255), (245, 245, 245, 255), "杂货")
    hero_shop("prop_cafe_awning.png", (38, 110, 116, 255), (45, 145, 150, 255), (240, 248, 248, 255), "咖啡")
    print("P51-P52 assets done")


if __name__ == "__main__":
    main()
