"""Pattern education cover: symbolism + usage + object photo collage header."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "2026-09-04_culture_pattern_yunwen_objects" / "assets"
ASSETS = Path(r"C:\Users\孤白赟悫\.cursor\projects\d-Infinite-Sustainable\assets")

W, H = 1080, 1440
INDIGO = "#1F2A44"
CREAM = "#F3E6C8"
CINNABAR = "#B54A3C"
GOLD = "#C2A15A"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"

KAI = Path(r"C:\Windows\Fonts\simkai.ttf")
MSYH = Path(r"C:\Windows\Fonts\msyh.ttc")
MSYHBD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def font(size: int, kai: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont:
    if kai and KAI.exists():
        return ImageFont.truetype(str(KAI), size=size)
    path = MSYHBD if bold and MSYHBD.exists() else MSYH
    return ImageFont.truetype(str(path), size=size, index=0)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # save object photos
    robe = Image.open(ASSETS / "pattern-on-silk-robe.png").convert("RGB").resize((1000, 560), Image.Resampling.LANCZOS)
    box = Image.open(ASSETS / "pattern-on-lacquer-box.png").convert("RGB").resize((480, 640), Image.Resampling.LANCZOS)
    robe.save(OUT_DIR / "object_silk_robe.jpg", format="JPEG", quality=92)
    box.save(OUT_DIR / "object_lacquer_box.jpg", format="JPEG", quality=92)

    # wallpaper = robe (life object with pattern)
    robe_full = Image.open(ASSETS / "pattern-on-silk-robe.png").convert("RGB")
    robe_full = robe_full.resize((1080, 1440), Image.Resampling.LANCZOS)
    robe_full.save(OUT_DIR / "wallpaper.jpg", format="JPEG", quality=92)

    # cover: object strip + education cards
    img = Image.new("RGB", (W, H), INDIGO)
    draw = ImageDraw.Draw(img)
    img.paste(robe.resize((1000, 420), Image.Resampling.LANCZOS), (40, 40))
    # small box inset
    small = box.resize((280, 360), Image.Resampling.LANCZOS)
    img.paste(small, (760, 80))

    draw.rounded_rectangle((40, 490, W - 40, H - 40), radius=18, fill="#121A2B", outline=GOLD, width=2)
    draw.text((70, 520), "传统文化 · 只讲纹饰", font=font(28), fill=GOLD)
    draw.text((70, 570), "卷雲紋", font=font(64, kai=True, bold=True), fill=CREAM)
    draw.text((70, 650), "置於衣上 · 見於器上", font=font(34, kai=True), fill=CINNABAR)

    cards = [
        ("作用", "以連續雲氣節奏填滿平面，連接邊飾與中心紋，使器物/织物不顯空疏。"),
        ("象徵", "雲行雨施、流動不息；傳統裡常借雲氣喻祥瑞、升騰與接天。"),
        ("常用", "服飾織繡、漆器边飾、建築彩畫、陶瓷肩部與口沿附近。"),
        ("本篇圖", "上圖：雲紋織於袍服；右上：回紋邊+雲角於漆盒——皆生活可用物。"),
    ]
    y = 720
    for title, body in cards:
        draw.rounded_rectangle((70, y, W - 70, y + 130), radius=12, fill="#1B2740")
        draw.text((90, y + 16), title, font=font(30, bold=True), fill=GOLD)
        # wrap-ish simple
        draw.text((90, y + 58), body[:22], font=font(24), fill=TEXT)
        if len(body) > 22:
            draw.text((90, y + 92), body[22:44], font=font(24), fill=TEXT)
        y += 145

    draw.text((70, H - 70), "本地草稿未發布 · 非某一文物翻製", font=font(22), fill=MUTED)
    cover = OUT_DIR / "cover.jpg"
    img.save(cover, format="JPEG", quality=93)
    print(f"wrote {cover}")
    print(f"wrote objects + wallpaper in {OUT_DIR}")


if __name__ == "__main__":
    main()
