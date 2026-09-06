"""P11 — Clearer 4-stage crop sprites (Visual Bible, nearest 16px)."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "assets" / "processed"

CROPS = {
    "radish": {"leaf": (70, 150, 70), "body": (230, 90, 90), "tip": (200, 60, 60)},
    "greens": {"leaf": (60, 160, 80), "body": (90, 180, 90), "tip": (50, 120, 50)},
    "wheat": {"leaf": (180, 170, 70), "body": (220, 190, 80), "tip": (240, 210, 100)},
    "tomato": {"leaf": (50, 140, 60), "body": (220, 50, 50), "tip": (180, 30, 30)},
    "pumpkin": {"leaf": (60, 130, 50), "body": (230, 140, 40), "tip": (200, 100, 30)},
}


def stage(crop: str, s: int) -> Image.Image:
    c = CROPS[crop]
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # soil mound always
    d.ellipse([5, 12, 10, 15], fill=(110, 80, 50, 220))
    if s == 0:
        d.point((8, 11), fill=c["leaf"] + (255,))
        d.point((7, 12), fill=(90, 70, 40, 255))
        return img
    # stem
    h = 2 + s * 2
    d.rectangle([7, 12 - h, 8, 12], fill=(50, 110, 50, 255))
    if s == 1:
        d.ellipse([5, 8, 10, 12], fill=c["leaf"] + (255,))
        return img
    if s == 2:
        d.ellipse([4, 5, 11, 11], fill=c["leaf"] + (255,))
        d.ellipse([6, 7, 9, 10], fill=c["body"] + (200,))
        return img
    # ripe
    d.ellipse([3, 3, 12, 11], fill=c["leaf"] + (255,))
    d.ellipse([5, 5, 10, 11], fill=c["body"] + (255,))
    d.point((7, 6), fill=(255, 255, 220, 255))
    d.ellipse([6, 4, 9, 6], fill=c["tip"] + (255,))
    return img


def main() -> None:
    for name in CROPS:
        for s in range(4):
            p = OUT / f"crop_{name}_{s}.png"
            stage(name, s).save(p)
            print("OK", p.name)
    print("P11 crops done")


if __name__ == "__main__":
    main()
