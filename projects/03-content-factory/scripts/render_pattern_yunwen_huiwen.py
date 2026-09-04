"""Pure traditional pattern composition wallpaper (NO landscape painting)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "2026-09-04_culture_pattern_yunwen_huiwen" / "assets"
W, H = 1080, 1440

# traditional palette: indigo ground + cinnabar/gold accents on paper cream cards
INDIGO = "#1F2A44"
CREAM = "#F3E6C8"
CINNABAR = "#B54A3C"
GOLD = "#C2A15A"
INK = "#2B2B2B"
MUTED = "#6B7280"

FONT_REG = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size=size, index=0)


def draw_huiwen(draw: ImageDraw.ImageDraw, box, step=28, color=GOLD, width=3) -> None:
    """Meander / key-fret border (回纹) — geometric only."""
    x0, y0, x1, y1 = box
    # outer rect
    draw.rectangle(box, outline=color, width=width)
    # stepped meander along top
    x = x0 + step
    y = y0 + step
    path = []
    while x < x1 - step:
        path.extend([(x, y), (x, y + step // 2), (x + step // 2, y + step // 2), (x + step // 2, y)])
        x += step
    if len(path) >= 2:
        draw.line(path, fill=color, width=2)
    # bottom mirror
    x = x0 + step
    y = y1 - step
    path = []
    while x < x1 - step:
        path.extend([(x, y), (x, y - step // 2), (x + step // 2, y - step // 2), (x + step // 2, y)])
        x += step
    if len(path) >= 2:
        draw.line(path, fill=color, width=2)


def draw_yunwen(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float, color=CINNABAR) -> None:
    """Simplified rolling cloud scroll (卷云纹) using arcs — ornamental only."""
    r = int(36 * scale)
    # S-like double spiral suggestion
    bbox1 = [cx - r, cy - r // 2, cx, cy + r // 2]
    bbox2 = [cx, cy - r // 2, cx + r, cy + r // 2]
    draw.arc(bbox1, 200, 20, fill=color, width=4)
    draw.arc(bbox2, 20, 200, fill=color, width=4)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy], 180, 0, fill=color, width=3)
    # small finishing curl
    draw.ellipse([cx + r - 6, cy - 6, cx + r + 6, cy + 6], outline=color, width=2)


def tile_yunwen(draw: ImageDraw.ImageDraw, area, gap=72) -> None:
    x0, y0, x1, y1 = area
    row = 0
    y = y0 + 24
    while y < y1 - 24:
        x = x0 + 28 + (row % 2) * (gap // 2)
        while x < x1 - 24:
            # denser dual-layer: cinnabar main + gold offset echo
            draw_yunwen(draw, x, y, scale=0.85 + 0.12 * math.sin((row + x) / 40), color=CINNABAR)
            draw_yunwen(draw, x + 18, y + 14, scale=0.55, color=GOLD)
            x += gap
        y += int(gap * 0.72)
        row += 1


def render_wallpaper() -> Path:
    """Full-bleed pattern-only wallpaper: 回纹边框 + 卷云纹铺满。"""
    img = Image.new("RGB", (W, H), INDIGO)
    draw = ImageDraw.Draw(img)
    margin = 36
    # cream panel
    panel = (margin, margin, W - margin, H - margin)
    draw.rounded_rectangle(panel, radius=20, fill=CREAM)
    # triple huiwen border for denser craft feel
    draw_huiwen(draw, (margin + 10, margin + 10, W - margin - 10, H - margin - 10), step=24, color=GOLD, width=3)
    draw_huiwen(draw, (margin + 28, margin + 28, W - margin - 28, H - margin - 28), step=22, color=CINNABAR, width=2)
    draw_huiwen(draw, (margin + 46, margin + 46, W - margin - 46, H - margin - 46), step=20, color=GOLD, width=2)
    # dense cloud scroll field
    tile_yunwen(draw, (margin + 60, margin + 60, W - margin - 60, H - margin - 60), gap=78)
    # corner seals (ornament, not landscape)
    for cx, cy in [(100, 100), (W - 100, 100), (100, H - 100), (W - 100, H - 100)]:
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=GOLD, width=2)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=CINNABAR)

    out = OUT_DIR / "wallpaper.jpg"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.save(out, format="JPEG", quality=93)
    return out


def render_cover() -> Path:
    """Cover: dense pattern field + typography explaining 纹饰组合（仍不含山水）。"""
    img = Image.new("RGB", (W, H), INDIGO)
    draw = ImageDraw.Draw(img)

    # upper pattern band — denser fill
    band = Image.new("RGB", (W - 80, 560), CREAM)
    bdraw = ImageDraw.Draw(band)
    draw_huiwen(bdraw, (10, 10, W - 90, 550), step=22, color=GOLD, width=3)
    draw_huiwen(bdraw, (28, 28, W - 108, 532), step=20, color=CINNABAR, width=2)
    tile_yunwen(bdraw, (44, 44, W - 124, 516), gap=70)
    img.paste(band, (40, 40))
    # text card — tighter under denser band
    draw.rounded_rectangle((40, 640, W - 40, H - 40), radius=22, fill="#121A2B", outline=GOLD, width=2)
    draw.text((70, 670), "传统文化 · 只讲纹饰", font=font(28), fill=GOLD)
    draw.text((70, 720), "卷云纹 × 回纹", font=font(54, True), fill=CREAM)
    draw.text((70, 790), "今天不讲山水画 · 只做纹饰组合", font=font(30, True), fill=CINNABAR)
    lines = [
        "组合：回纹=边框节奏；卷云纹=内部铺陈",
        "出处：器物边饰 / 织物 / 建筑彩画母题",
        "边界：禁止混入水墨山水/名画场景",
        "下篇候选：如意云、缠枝莲、藻井纹（仍单开）",
    ]
    y = 850
    for line in lines:
        draw.rounded_rectangle((70, y, W - 70, y + 64), radius=12, fill="#1B2740")
        draw.text((90, y + 16), line, font=font(26), fill=CREAM)
        y += 74

    draw.text((70, H - 90), "本地草稿未发布", font=font(24), fill=MUTED)

    out = OUT_DIR / "cover.jpg"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.save(out, format="JPEG", quality=93)
    return out


def main() -> None:
    w = render_wallpaper()
    c = render_cover()
    print(f"wallpaper -> {w}")
    print(f"cover -> {c}")


if __name__ == "__main__":
    main()
