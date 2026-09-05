"""文人小品：在水墨底图上竖排曲词句眼（楷体）。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "ink-songhua-niangjiu-base.png"
OUT = ROOT / "outputs" / "2026-09-05_culture_songhua_niangjiu" / "assets"

KAI = Path(r"C:\Windows\Fonts\simkai.ttf")
FALLBACK = Path(r"C:\Windows\Fonts\STKAITI.TTF")


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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    base = Image.open(SRC).convert("RGB").resize((1080, 1440), Image.Resampling.LANCZOS)

    # cover: poem as part of painting
    cover = base.copy()
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # soft paper strip for inscription (文人题跋感，不做成现代卡片)
    od.rectangle((40, 60, 200, 980), fill=(247, 240, 224, 165))
    cover = Image.alpha_composite(cover.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(cover)

    vertical(draw, "松花釀酒", 70, 100, kai(52), "#1C1710", 60)
    vertical(draw, "春水煎茶", 135, 100, kai(52), "#1C1710", 60)
    draw.text((55, 1020), "人月圓·山中書事", font=kai(26), fill="#5C5346")
    draw.text((55, 1060), "張可久句眼·意境非翻製", font=kai(24), fill="#7A7266")

    # wallpaper: lighter inscription
    wall = base.copy()
    wd = ImageDraw.Draw(wall)
    vertical(wd, "松花釀酒", 60, 120, kai(46), "#2A241C", 54)
    vertical(wd, "春水煎茶", 120, 120, kai(46), "#2A241C", 54)

    plain = base.copy()
    cover.save(OUT / "cover.jpg", format="JPEG", quality=93)
    wall.save(OUT / "wallpaper.jpg", format="JPEG", quality=93)
    plain.save(OUT / "wallpaper_plain.jpg", format="JPEG", quality=93)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
