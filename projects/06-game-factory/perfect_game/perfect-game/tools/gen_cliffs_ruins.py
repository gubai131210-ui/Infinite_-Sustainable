"""Taller cliff faces + denser ruin arch variants for overview north edge."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "assets" / "processed"


def cliff_face(w: int = 48, h: int = 64) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # layered rock bands
    bands = [
        ((48, 62, 78), 0),
        ((62, 78, 92), 10),
        ((78, 92, 108), 22),
        ((55, 70, 85), 36),
        ((70, 88, 100), 48),
    ]
    for color, y0 in bands:
        d.rectangle([4, y0, w - 5, min(h - 1, y0 + 18)], fill=color + (255,))
        d.line([(6, y0 + 4), (w - 8, y0 + 6)], fill=(30, 40, 50, 180))
        d.line([(8, y0 + 12), (w - 10, y0 + 10)], fill=(100, 120, 130, 120))
    # grass cap
    d.polygon([(2, 8), (w // 2, 0), (w - 3, 8), (w - 4, 14), (4, 14)], fill=(70, 120, 70, 255))
    return img


def ruin_arch(w: int = 48, h: int = 40) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    stone = (120, 118, 110, 255)
    dark = (80, 78, 72, 255)
    d.rectangle([4, 10, 12, h - 2], fill=stone)
    d.rectangle([w - 13, 10, w - 5, h - 2], fill=stone)
    d.rectangle([4, 6, w - 5, 14], fill=stone)
    # arch hole
    d.ellipse([14, 12, w - 15, h - 4], fill=(0, 0, 0, 0))
    # redraw pillars over ellipse bottom
    d.rectangle([4, 22, 12, h - 2], fill=stone)
    d.rectangle([w - 13, 22, w - 5, h - 2], fill=stone)
    d.rectangle([6, 8, 10, 20], fill=dark)
    d.rectangle([w - 11, 8, w - 7, 20], fill=dark)
    # moss
    d.ellipse([8, 4, 18, 12], fill=(70, 120, 60, 200))
    d.ellipse([w - 20, 5, w - 8, 13], fill=(60, 110, 55, 180))
    return img


def mountain_tall(w: int = 160, h: int = 72) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(0, h), (20, 40), (45, 18), (70, 28), (95, 8), (120, 22), (145, 14), (w - 1, h)], fill=(70, 95, 120, 255))
    d.polygon([(0, h), (15, 48), (40, 32), (68, 40), (100, 24), (130, 36), (w - 1, h)], fill=(78, 115, 88, 255))
    d.polygon([(0, h), (25, 55), (55, 48), (90, 52), (125, 46), (w - 1, h)], fill=(55, 95, 60, 255))
    for x0, y0 in [(95, 8), (45, 18), (145, 14)]:
        d.polygon([(x0 - 8, y0 + 10), (x0, y0), (x0 + 8, y0 + 10)], fill=(235, 240, 245, 210))
    return img


def main() -> None:
    cliff_face().save(OUT / "prop_cliff.png")
    ruin_arch().save(OUT / "prop_ruin_arch.png")
    mountain_tall().save(OUT / "prop_mountains.png")
    print("OK cliff, ruin_arch, mountains refreshed")


if __name__ == "__main__":
    main()
