"""文人小品：彩色浅绛 + 黑白水墨 两套曲词壁纸（楷体竖排句眼）。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "2026-09-05_culture_songhua_niangjiu" / "assets"

INK_BASE = ROOT / "assets" / "ink-songhua-niangjiu-base.png"
COLOR_BASE = ROOT / "assets" / "ink-songhua-niangjiu-color-base.png"

KAI = Path(r"C:\Windows\Fonts\simkai.ttf")
FALLBACK = Path(r"C:\Windows\Fonts\STKAITI.TTF")

SIZE = (1080, 1440)


def kai(size: int) -> ImageFont.FreeTypeFont:
    for p in (KAI, FALLBACK):
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", size=size, index=0)


def vertical(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, font, fill, gap: int) -> None:
    cy = y
    for ch in text:
        if ch in "，、。":
            draw.text((x + 8, cy - 8), ch, font=font, fill=fill)
            cy += gap // 2
        else:
            draw.text((x, cy), ch, font=font, fill=fill)
            cy += gap


def load_base(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"missing base: {path}")
    return Image.open(path).convert("RGB").resize(SIZE, Image.Resampling.LANCZOS)


def render_set(base: Image.Image, prefix: str, ink: bool) -> None:
    """prefix: color_ | ink_ ; ink=True uses darker inscription strip."""
    strip = (247, 240, 224, 165) if not ink else (240, 236, 228, 150)
    title = "#1C1710"
    meta1 = "#5C5346"
    meta2 = "#7A7266"
    wall_ink = "#2A241C"

    cover = base.copy()
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((40, 60, 200, 980), fill=strip)
    cover = Image.alpha_composite(cover.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(cover)
    vertical(draw, "松花釀酒", 70, 100, kai(52), title, 60)
    vertical(draw, "春水煎茶", 135, 100, kai(52), title, 60)
    draw.text((55, 1020), "人月圓·山中書事", font=kai(26), fill=meta1)
    draw.text((55, 1060), "張可久句眼·意境非翻製", font=kai(24), fill=meta2)

    wall = base.copy()
    wd = ImageDraw.Draw(wall)
    vertical(wd, "松花釀酒", 60, 120, kai(46), wall_ink, 54)
    vertical(wd, "春水煎茶", 120, 120, kai(46), wall_ink, 54)

    plain = base.copy()

    cover.save(OUT / f"{prefix}cover.jpg", format="JPEG", quality=93)
    wall.save(OUT / f"{prefix}wallpaper.jpg", format="JPEG", quality=93)
    plain.save(OUT / f"{prefix}wallpaper_plain.jpg", format="JPEG", quality=93)

    # keep short aliases for the ink set (backward compatible)
    if ink:
        cover.save(OUT / "cover.jpg", format="JPEG", quality=93)
        wall.save(OUT / "wallpaper.jpg", format="JPEG", quality=93)
        plain.save(OUT / "wallpaper_plain.jpg", format="JPEG", quality=93)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    render_set(load_base(COLOR_BASE), "color_", ink=False)
    render_set(load_base(INK_BASE), "ink_", ink=True)
    print(f"wrote color_ + ink_ sets -> {OUT}")


if __name__ == "__main__":
    main()
