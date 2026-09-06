"""P36–P38 spectacle assets: nested cliff waterfall + roof facade variants."""
from __future__ import annotations

from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "assets" / "processed"
rng = random.Random(21)


def gen_waterfall() -> None:
    """Wide cliff-cascade like overview reference (not a thin cylinder)."""
    w, h = 96, 112
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Cliff mass behind
    d.rectangle((8, 0, 88, 28), fill=(78, 70, 58, 255))
    for y in range(0, 28):
        for x in range(8, 88):
            if ((x + y * 3) % 5) == 0:
                img.putpixel((x, y), (95, 86, 72, 255))
    # Grass lip
    d.rectangle((10, 0, 86, 8), fill=(70, 120, 55, 255))
    d.rectangle((14, 4, 82, 10), fill=(86, 130, 58, 255))
    # Side rock jaws
    d.polygon([(4, 8), (22, 12), (18, 70), (2, 66)], fill=(88, 78, 64, 255))
    d.polygon([(74, 12), (92, 8), (94, 66), (78, 70)], fill=(88, 78, 64, 255))
    # Three cascade ribbons tapering into pool
    ribbons = [(28, 38), (40, 52), (54, 40)]
    for cx0, cx1 in ribbons:
        for y in range(10, 78):
            t = (y - 10) / 68.0
            half = int(4 + t * 5)
            cx = int((cx0 + cx1) / 2 + (cx1 - cx0) * 0.15 * (1 - t))
            for x in range(cx - half, cx + half + 1):
                if 0 <= x < w:
                    shade = 70 + int(t * 35) + rng.randint(-8, 8)
                    img.putpixel((x, y), (max(40, shade), 140 + int(t * 20), 210, 240))
            if y % 2 == 0:
                hx = cx + rng.randint(-half, half)
                if 0 <= hx < w:
                    img.putpixel((hx, y), (210, 235, 250, 220))
    # Foam crest
    d.ellipse((22, 8, 74, 20), fill=(235, 245, 255, 230))
    for _ in range(30):
        img.putpixel((rng.randint(24, 72), rng.randint(8, 18)), (255, 255, 255, 255))
    # Plunge pool
    d.ellipse((18, 72, 78, 100), fill=(55, 120, 185, 230))
    d.ellipse((26, 78, 70, 96), fill=(90, 160, 215, 200))
    for _ in range(40):
        img.putpixel((rng.randint(22, 74), rng.randint(74, 98)), (220, 240, 255, 255))
    # Moss on rocks
    for x, y in [(10, 40), (12, 48), (82, 42), (84, 50), (16, 60)]:
        d.ellipse((x, y, x + 6, y + 4), fill=(60, 110, 50, 200))
    path = PROC / "prop_waterfall.png"
    img.save(path)
    print("OK", path.name, img.size)


def _recolor_roof(img: Image.Image, roof_rgb: tuple[int, int, int], top_frac: float = 0.42) -> Image.Image:
    out = img.copy().convert("RGBA")
    px = out.load()
    w, h = out.size
    y_cut = int(h * top_frac)
    for y in range(y_cut):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 20:
                continue
            # skip near-green foliage / windows blues lightly — prefer brownish roof pixels
            if g > r + 25 and g > b + 15:
                continue
            # blend toward target roof
            nr = int(r * 0.35 + roof_rgb[0] * 0.65)
            ng = int(g * 0.35 + roof_rgb[1] * 0.65)
            nb = int(b * 0.35 + roof_rgb[2] * 0.65)
            px[x, y] = (nr, ng, nb, a)
    return out


def gen_roofs() -> None:
    specs = [
        ("prop_townhouse_brown.png", "prop_townhouse_redroof.png", (150, 70, 55)),
        ("prop_townhouse_blue.png", "prop_townhouse_slateroof.png", (70, 85, 110)),
        ("prop_townhouse_green.png", "prop_townhouse_thatch.png", (120, 105, 60)),
        ("prop_shop.png", "prop_shop_redroof.png", (160, 75, 50)),
        ("prop_cafe.png", "prop_cafe_tealroof.png", (50, 110, 115)),
        ("prop_farmhouse.png", "prop_farmhouse_darkroof.png", (90, 70, 55)),
    ]
    for src_name, dst_name, color in specs:
        src = PROC / src_name
        if not src.exists():
            print("SKIP missing", src_name)
            continue
        img = Image.open(src)
        out = _recolor_roof(img, color)
        # slight contrast so roofs read at overview zoom
        out = ImageEnhance.Contrast(out).enhance(1.08)
        dst = PROC / dst_name
        out.save(dst)
        print("OK", dst.name)


def main() -> None:
    gen_waterfall()
    gen_roofs()
    print("P36-P38 assets done")


if __name__ == "__main__":
    main()
