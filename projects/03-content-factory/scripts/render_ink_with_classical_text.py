"""Overlay classical Chinese (古文) on ink painting with Kai font."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\孤白赟悫\.cursor\projects\d-Infinite-Sustainable\assets\painting-jiangzhou-guying.png")
OUT_DIR = ROOT / "outputs" / "2026-09-04_culture_shanshui_jiangzhou" / "assets"

# Prefer 楷体 for classical text
KAI = Path(r"C:\Windows\Fonts\simkai.ttf")
FALLBACK = Path(r"C:\Windows\Fonts\STKAITI.TTF")
FANG = Path(r"C:\Windows\Fonts\simfang.ttf")


def pick_font(size: int) -> ImageFont.FreeTypeFont:
    for p in (KAI, FALLBACK, FANG):
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", size=size, index=0)


def draw_vertical_text(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, font, fill, gap: int) -> None:
    cy = y
    for ch in text:
        draw.text((x, cy), ch, font=font, fill=fill)
        cy += gap


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = Image.open(SRC).convert("RGB")
    # normalize to 1080x1440-ish
    base = base.resize((1080, 1440), Image.Resampling.LANCZOS)
    img = base.copy()
    draw = ImageDraw.Draw(img)

    # classical lines (江雪 / 意境短句，竖排)
    title_font = pick_font(54)
    body_font = pick_font(42)
    seal_font = pick_font(28)

    # soft panel for readability (left upper, not covering boat)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((48, 80, 220, 720), radius=8, fill=(243, 230, 200, 210))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 竖题
    draw_vertical_text(draw, "孤舟一葉", 90, 120, title_font, "#1F1A14", 62)
    draw_vertical_text(draw, "煙水蒼茫", 155, 120, body_font, "#3A3228", 52)

    # 小字出处感
    draw.text((70, 760), "煙波之意", font=seal_font, fill="#5C5346")
    draw.text((70, 800), "非某一名畫翻製", font=seal_font, fill="#5C5346")

    cover = OUT_DIR / "cover.jpg"
    wall = OUT_DIR / "wallpaper.jpg"
    # wallpaper: cleaner, less text — only short classical seal line
    wall_img = base.copy()
    wd = ImageDraw.Draw(wall_img)
    wfont = pick_font(40)
    # vertical short phrase bottom-left
    draw_vertical_text(wd, "獨釣寒江", 70, 980, wfont, "#2B2B2B", 48)
    wd.text((70, 1200), "（意境·非原作）", font=seal_font, fill="#6B7280")

    img.save(cover, format="JPEG", quality=93)
    wall_img.save(wall, format="JPEG", quality=93)
    # also copy plain base as wallpaper_plain
    base.save(OUT_DIR / "wallpaper_plain.jpg", format="JPEG", quality=93)
    print(f"wrote {cover}")
    print(f"wrote {wall}")


if __name__ == "__main__":
    main()
