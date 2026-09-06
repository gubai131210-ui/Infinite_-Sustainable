"""P46–P48: tall opaque sky, big clouds, denser house facades."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

PROC = Path(__file__).resolve().parents[1] / "assets" / "processed"


def sky_band() -> None:
    """Tall opaque sky strip that survives overview zoom 0.38."""
    w, h = 160, 56
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        # Deep azure → soft horizon haze
        r = int(110 + 70 * t)
        g = int(170 + 45 * t)
        b = int(230 - 15 * t)
        a = 255 if y < h - 8 else int(255 - (y - (h - 8)) * 20)
        d.line([(0, y), (w - 1, y)], fill=(r, g, b, max(180, a)))
    # Soft distant ridge silhouettes inside sky (read as mountains behind pines)
    for i, x0 in enumerate(range(8, w - 20, 28)):
        peak = 34 + (i % 3) * 4
        d.polygon(
            [(x0, h - 2), (x0 + 10, peak), (x0 + 22, h - 2)],
            fill=(90, 130, 150, 70),
        )
    img.save(PROC / "prop_sky_band.png")
    print("OK prop_sky_band.png", w, h)


def cloud(name: str, w: int, h: int, seed_off: int = 0) -> None:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Layered opaque puffs so overview still reads white
    blobs = [
        (4 + seed_off % 3, h // 2 - 2, w // 2 + 4, h - 2),
        (w // 4, 2, w * 3 // 4, h - 4),
        (w // 2 - 4, h // 3, w - 4, h - 2),
    ]
    for b in blobs:
        d.ellipse(b, fill=(250, 252, 255, 240))
    # Highlight rim
    d.ellipse((w // 4 + 2, 4, w // 2, h // 2), fill=(255, 255, 255, 255))
    img.save(PROC / name)
    print("OK", name, w, h)


def house(name: str, wall: tuple, roof: tuple, accent: tuple, timber: bool = True) -> None:
    """Denser facade: shingles, shutters, planter, chimney smoke stub."""
    w, h = 72, 80
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Roof mass
    peak = (w // 2, 2)
    d.polygon([(4, 26), peak, (w - 4, 26)], fill=roof)
    shade = tuple(max(0, c - 28) for c in roof[:3]) + (255,)
    d.polygon([(4, 26), (w - 4, 26), (w - 10, 34), (10, 34)], fill=shade)
    # Shingle lines
    for yy in range(10, 26, 3):
        d.line([(12 + (yy % 2), yy), (w - 12 - (yy % 2), yy)], fill=shade, width=1)
    # Chimney + puff
    d.rectangle((w // 2 + 12, 8, w // 2 + 20, 28), fill=(105, 95, 90, 255))
    d.rectangle((w // 2 + 11, 6, w // 2 + 21, 10), fill=(80, 75, 70, 255))
    d.ellipse((w // 2 + 14, 1, w // 2 + 22, 8), fill=(230, 230, 235, 160))
    # Walls
    d.rectangle((10, 34, w - 10, h - 4), fill=wall)
    if timber:
        frame = (68, 52, 38, 255)
        d.rectangle((10, 34, w - 10, h - 4), outline=frame, width=2)
        d.line([(w // 2, 34), (w // 2, h - 4)], fill=frame, width=2)
        d.line([(10, 50), (w - 10, 50)], fill=frame, width=1)
    # Windows + shutters
    win = (185, 215, 235, 255)
    for wx in (16, w - 28):
        d.rectangle((wx - 2, 40, wx + 14, 52), fill=(90, 70, 50, 255))
        d.rectangle((wx, 42, wx + 12, 50), fill=win)
        d.line([(wx + 6, 42), (wx + 6, 50)], fill=(120, 145, 165, 255))
    # Door + stoop
    d.rectangle((w // 2 - 7, h - 24, w // 2 + 7, h - 4), fill=accent)
    d.rectangle((w // 2 - 3, h - 16, w // 2 - 1, h - 14), fill=(220, 200, 120, 255))
    d.rectangle((w // 2 - 10, h - 6, w // 2 + 10, h - 3), fill=(95, 90, 85, 255))
    # Window box flowers
    d.rectangle((14, 52, 30, 56), fill=(70, 120, 60, 255))
    for fx in (16, 20, 24):
        d.point((fx, 51), fill=(220, 80, 90, 255))
    img.save(PROC / name)
    print("OK", name)


def shop(name: str, roof: tuple, awning_a: tuple, awning_b: tuple) -> None:
    w, h = 88, 76
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(2, 20), (44, 2), (86, 20)], fill=roof)
    d.rectangle((8, 20, 80, h - 4), fill=(215, 200, 175, 255))
    d.rectangle((8, 20, 80, h - 4), outline=(85, 65, 45, 255), width=2)
    # Deep awning with scallops
    for i, x0 in enumerate(range(12, 76, 8)):
        c = awning_a if i % 2 == 0 else awning_b
        d.rectangle((x0, 24, x0 + 7, 38), fill=c)
        d.pieslice((x0, 34, x0 + 7, 44), 0, 180, fill=c)
    d.rectangle((34, h - 26, 54, h - 4), fill=(95, 70, 45, 255))
    d.rectangle((14, 44, 28, 56), fill=(170, 210, 230, 255))
    d.rectangle((60, 44, 74, 56), fill=(170, 210, 230, 255))
    # Sign board
    d.rectangle((30, 40, 58, 48), fill=(120, 90, 50, 255))
    img.save(PROC / name)
    print("OK", name)


def main() -> None:
    sky_band()
    cloud("prop_cloud_0.png", 72, 28, 0)
    cloud("prop_cloud_1.png", 88, 32, 1)
    cloud("prop_cloud_2.png", 64, 26, 2)
    house("prop_house_redroof.png", (222, 200, 172, 255), (168, 68, 52, 255), (115, 55, 38, 255))
    house("prop_house_slateroof.png", (198, 204, 210, 255), (70, 88, 112, 255), (55, 65, 85, 255))
    house("prop_house_thatch.png", (218, 198, 158, 255), (145, 122, 68, 255), (100, 78, 42, 255))
    house("prop_house_greenroof.png", (200, 208, 180, 255), (62, 118, 78, 255), (50, 88, 58, 255))
    shop("prop_shop_awning.png", (148, 60, 48, 255), (200, 55, 50, 255), (245, 245, 245, 255))
    shop("prop_cafe_awning.png", (40, 112, 118, 255), (45, 145, 150, 255), (240, 248, 248, 255))
    print("P46-P48 assets done")


if __name__ == "__main__":
    main()
