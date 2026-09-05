"""AI 早报风格：浅底橙标题，概览 2x2 + 深挖双卡；输出 16:9 与 3:4 竖裁。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "2026-09-05_ai_morning_report" / "assets"

W, H = 1920, 1080  # 16:9
CREAM = "#F7F3EB"
CARD = "#FFFFFF"
TITLE = "#C45C26"
TEXT = "#2B2B2B"
MUTED = "#6B7280"
LINE = "#E7DFD3"
ACCENT = "#D4543C"
TAB_BG = "#EFE8DC"
GREEN = "#3F6F5A"
BLUE = "#3B6EA5"

FONT_REG = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size=size, index=0)


def rounded(draw: ImageDraw.ImageDraw, xy, fill=CARD, outline=LINE, r=18) -> None:
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=2)


def pill(draw: ImageDraw.ImageDraw, xy, text: str, fill="#F3E8E2") -> None:
    rounded(draw, xy, fill=fill, outline=fill, r=10)
    x0, y0, x1, y1 = xy
    draw.text((x0 + 10, y0 + 6), text, font=font(22), fill=TEXT)


def draw_tabs(draw: ImageDraw.ImageDraw, active: str) -> None:
    tabs = ["Intro", "要闻", "开发生态", "模型发布", "产品应用", "技术与洞察", "行业动态", "前瞻与传闻"]
    x = 48
    y = 28
    for t in tabs:
        tw = 28 + len(t) * 18
        bg = ACCENT if t == active else TAB_BG
        fg = "#FFFFFF" if t == active else MUTED
        rounded(draw, (x, y, x + tw, y + 44), fill=bg, outline=bg, r=12)
        draw.text((x + 14, y + 8), t, font=font(22, True), fill=fg)
        x += tw + 12


def crop_vertical(img: Image.Image, out: Path) -> None:
    """Center-crop 16:9 -> 3:4."""
    w, h = img.size
    target_ratio = 3 / 4
    new_w = int(h * target_ratio)
    left = max(0, (w - new_w) // 2)
    cropped = img.crop((left, 0, left + new_w, h)).resize((1080, 1440), Image.Resampling.LANCZOS)
    cropped.save(out, format="JPEG", quality=93)


def render_overview() -> Path:
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_tabs(draw, "要闻")
    draw.text((48, 100), "2026-09-05 资讯概览", font=font(56, True), fill=TITLE)

    cards = [
        ("要闻", ACCENT, ["Claude Code 周限额口径再引争议", "相对基线 +25%，相对今天约 -17%", "官方澄清：促销结束后落差明显"]),
        ("开发生态", "#C47A26", ["多工具切换成开发者自救策略", "Cursor / Codex 备用链路讨论升温", "用量面板自查成为早报固定动作"]),
        ("模型发布", BLUE, ["各家额度与重置政策同周对比", "订阅口径 ≠ API 计费口径", "长上下文任务更吃配额"]),
        ("产品应用", GREEN, ["早报卡片模板可复用到小红书长图", "单条深挖页：标题 + 左右双卡", "关键词沉底栏，正文不堆标签"]),
    ]
    positions = [(48, 200), (984, 200), (48, 560), (984, 560)]
    for (title, color, lines), (x, y) in zip(cards, positions):
        rounded(draw, (x, y, x + 888, y + 320))
        draw.ellipse((x + 28, y + 28, x + 58, y + 58), fill=color)
        draw.text((x + 76, y + 28), title, font=font(32, True), fill=TITLE)
        yy = y + 100
        for line in lines:
            draw.text((x + 36, yy), f"· {line}", font=font(28), fill=TEXT)
            yy += 52

    # keyword ticker
    rounded(draw, (48, 980, W - 48, 1048), fill="#EFE8DC", outline="#EFE8DC")
    draw.text(
        (70, 998),
        "关键词  Claude Code   额度口径   Cursor   Codex   订阅重置   早报模板   双卡深挖",
        font=font(24),
        fill=MUTED,
    )
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "overview_16x9.jpg"
    img.save(path, format="JPEG", quality=93)
    crop_vertical(img, OUT / "overview_3x4.jpg")
    return path


def render_deep_dive() -> Path:
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_tabs(draw, "要闻")
    draw.text(
        (48, 100),
        "Claude Code 周限额：涨 25%？相对今天少约 17%",
        font=font(44, True),
        fill=TITLE,
    )

    # left card
    rounded(draw, (48, 220, 936, 820))
    draw.ellipse((80, 260, 120, 300), fill=GREEN)
    draw.text((140, 258), "宣传口径", font=font(34, True), fill=TITLE)
    draw.text((80, 340), "涨 25%", font=font(92, True), fill=GREEN)
    draw.text((80, 460), "相对：原始基线", font=font(32, True), fill=TEXT)
    for i, t in enumerate(["官方常用这个分母", "相对「过去标准」是上涨", "不等于手头额度变多"]):
        draw.text((80, 540 + i * 56), f"· {t}", font=font(28), fill=TEXT)
    pill(draw, (80, 740, 220, 780), "基线")
    pill(draw, (240, 740, 420, 780), "+25% 永久")

    # right card
    rounded(draw, (984, 220, 1872, 820))
    draw.ellipse((1016, 260, 1056, 300), fill=ACCENT)
    draw.text((1076, 258), "体感口径", font=font(34, True), fill=TITLE)
    draw.text((1016, 340), "少约 17%", font=font(84, True), fill=ACCENT)
    draw.text((1016, 460), "相对：今天正在用的额度", font=font(32, True), fill=TEXT)
    for i, t in enumerate(["临时 150 → 永久 125", "相对今天是下降", "重度用户体感最明显"]):
        draw.text((1016, 540 + i * 56), f"· {t}", font=font(28), fill=TEXT)
    pill(draw, (1016, 740, 1180, 780), "今天")
    pill(draw, (1200, 740, 1400, 780), "约 -17%")

    rounded(draw, (48, 860, W - 48, 960), fill="#2B2B2B", outline="#2B2B2B")
    draw.text(
        (70, 890),
        "换算：基线 100  →  临时 150  →  永久后 125　　｜　　9月14日起生效 · 以官方最终公告为准",
        font=font(28),
        fill="#F7F3EB",
    )
    rounded(draw, (48, 980, W - 48, 1048), fill="#EFE8DC", outline="#EFE8DC")
    draw.text(
        (70, 998),
        "关键词  Claude Code   周限额   banked 口径对比   相对谁   /usage",
        font=font(24),
        fill=MUTED,
    )

    path = OUT / "deepdive_16x9.jpg"
    img.save(path, format="JPEG", quality=93)
    crop_vertical(img, OUT / "deepdive_3x4.jpg")
    return path


def main() -> None:
    o = render_overview()
    d = render_deep_dive()
    print(f"overview -> {o}")
    print(f"deepdive -> {d}")
    print(f"also wrote 3x4 crops in {OUT}")


if __name__ == "__main__":
    main()
