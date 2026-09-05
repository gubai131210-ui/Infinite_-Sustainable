"""纹饰词典卡：仅 名/作用/象征/常用（器物非必须）。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "2026-09-05_pattern_dict_yunwen" / "assets"

W, H = 1080, 1440
CREAM = "#F7F3EB"
INK = "#1C1710"
MUTED = "#6B5E4E"
LINE = "#D9CDB8"
CINNABAR = "#A6533E"
GOLD = "#B08A4A"

KAI = Path(r"C:\Windows\Fonts\simkai.ttf")
MSYH = Path(r"C:\Windows\Fonts\msyh.ttc")
MSYHBD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def f(size: int, kai: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont:
    if kai and KAI.exists():
        return ImageFont.truetype(str(KAI), size=size)
    path = MSYHBD if bold and MSYHBD.exists() else MSYH
    return ImageFont.truetype(str(path), size=size, index=0)


def wrap(draw, text: str, font, max_w: int) -> list[str]:
    lines, cur = [], ""
    for ch in text:
        trial = cur + ch
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle((48, 48, W - 48, H - 48), outline=LINE, width=3)
    draw.rectangle((60, 60, W - 60, H - 60), outline=GOLD, width=1)

    draw.text((90, 100), "紋樣詞典", font=f(28), fill=GOLD)
    draw.text((90, 160), "卷雲紋", font=f(72, kai=True), fill=INK)
    draw.text((90, 260), "Yunwen · rolling cloud scroll", font=f(24), fill=MUTED)

    entries = [
        ("作用", "以連續雲氣節奏鋪陳平面，銜接邊飾與中心紋樣，使器物或織物不顯空疏。"),
        ("象徵", "雲行雨施、流動不息；傳統語境中常借雲氣喻祥瑞、升騰與接天。"),
        ("常用", "服飾織繡、漆器邊飾、建築彩畫、陶瓷肩部與口沿附近。"),
    ]
    y = 340
    for title, body in entries:
        draw.rectangle((90, y, W - 90, y + 220), outline=LINE, width=2)
        draw.text((110, y + 24), title, font=f(34, bold=True), fill=CINNABAR)
        by = y + 80
        for line in wrap(draw, body, f(28), W - 220):
            draw.text((110, by), line, font=f(28), fill=INK)
            by += 40
        y += 250

    draw.text((90, H - 110), "词典卡 · 器物图非必须 · 本地草稿", font=f(22), fill=MUTED)
    path = OUT / "dict_card_3x4.jpg"
    img.save(path, format="JPEG", quality=93)
    # also 16:9 crop-style wide dict for series consistency
    wide = Image.new("RGB", (1920, 1080), CREAM)
    wd = ImageDraw.Draw(wide)
    wd.rectangle((60, 60, 1860, 1020), outline=LINE, width=3)
    wd.text((100, 100), "紋樣詞典 · 卷雲紋", font=f(56, kai=True), fill=INK)
    x = 100
    for title, body in entries:
        wd.rectangle((x, 240, x + 540, 900), outline=LINE, width=2)
        wd.text((x + 30, 280), title, font=f(40, bold=True), fill=CINNABAR)
        by = 380
        for line in wrap(wd, body, f(30), 470):
            wd.text((x + 30, by), line, font=f(30), fill=INK)
            by += 44
        x += 580
    wide.save(OUT / "dict_card_16x9.jpg", format="JPEG", quality=93)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
