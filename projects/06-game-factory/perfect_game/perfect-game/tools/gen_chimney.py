"""Small chimney silhouette for townhouse roof variety."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "assets" / "processed"


def main() -> None:
    img = Image.new("RGBA", (16, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((5, 6, 11, 22), fill=(110, 100, 95, 255))
    d.rectangle((4, 4, 12, 8), fill=(90, 82, 78, 255))
    d.rectangle((6, 8, 10, 12), fill=(40, 36, 34, 255))
    # smoke puff hint
    d.ellipse((6, 0, 12, 5), fill=(200, 200, 205, 120))
    path = OUT / "prop_chimney.png"
    img.save(path)
    print("OK", path)


if __name__ == "__main__":
    main()
