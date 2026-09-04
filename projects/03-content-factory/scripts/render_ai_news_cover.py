"""Render AI news cover per prompt_library/ai_news_data_card.md layout contract."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "2026-09-04_ai_claude_code_limits" / "assets" / "cover.jpg"
OUT_V = ROOT / "outputs" / "2026-09-04_ai_claude_code_limits" / "assets" / "cover_data_card.jpg"

W, H = 1080, 1440
BG = "#0B1220"
CARD = "#152033"
CARD2 = "#1B2740"
LINE = "#2A3B55"
BLUE = "#3B82F6"
BLUE_SOFT = "#93C5FD"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
GREEN = "#34D399"
RED = "#F87171"
AMBER = "#FBBF24"

FONT_REG = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size=size, index=0)


def card(draw: ImageDraw.ImageDraw, xy, fill=CARD, outline=LINE, r=16) -> None:
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=2)


def main() -> None:
    """
    Layout contract (ai_news_data_card.md):
    top bar ~6%, title ~10%, hook ~5%,
    core number ~32%, 3 rows ~22%, formula ~8%, actions ~14%, footer ~5%
    """
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 12, H), fill=BLUE)

    # top bar
    card(draw, (36, 28, 300, 78), fill=CARD2)
    draw.text((52, 40), "AI资讯·额度口径", font=font(26, True), fill=BLUE_SOFT)
    draw.text((820, 40), "2026.09", font=font(26, True), fill=TEXT)

    # title + hook
    draw.text((36, 100), "Claude Code 周限额", font=font(48, True), fill=TEXT)
    draw.text((36, 168), "别只看「涨 25%」这半句", font=font(34, True), fill=AMBER)

    # CORE NUMBER ZONE (~32% height) — Apiyi data-card pattern
    core = (36, 230, W - 36, 230 + int(H * 0.30))
    card(draw, core, fill="#121C2E", outline=BLUE)
    draw.text((60, 250), "体感主数字（相对今天）", font=font(26), fill=MUTED)
    draw.text((60, 300), "少约 17%", font=font(110, True), fill=RED)
    draw.text((60, 440), "对照宣传口径", font=font(26), fill=MUTED)
    draw.text((60, 485), "涨 25%", font=font(64, True), fill=GREEN)
    draw.text((320, 510), "相对原始基线", font=font(28), fill="#A7F3D0")
    draw.text((620, 250), "读法", font=font(26, True), fill=BLUE_SOFT)
    for i, line in enumerate(
        [
            "同一公告两种分母",
            "基线↑ ≠ 今天额度↑",
            "先问：相对谁？",
            "再查自己 /usage",
        ]
    ):
        draw.text((620, 300 + i * 48), f"• {line}", font=font(26), fill=TEXT)

    # 3 supplementary rows
    y = core[3] + 24
    rows = [
        ("临时促销", "+50%", "用到 9/13", AMBER),
        ("永久调整", "+25%", "相对基线", GREEN),
        ("体感变化", "-17%", "相对今天", RED),
    ]
    for label, val, note, color in rows:
        card(draw, (36, y, W - 36, y + 78), fill=CARD)
        draw.text((56, y + 22), label, font=font(28), fill=MUTED)
        draw.text((320, y + 16), val, font=font(40, True), fill=color)
        draw.text((560, y + 24), note, font=font(28), fill=TEXT)
        y += 90

    # formula strip
    card(draw, (36, y, W - 36, y + 88), fill=CARD2)
    draw.text((56, y + 12), "换算一眼看懂", font=font(24), fill=BLUE_SOFT)
    draw.text((56, y + 44), "基线 100   →   临时 150   →   永久后 125", font=font(32, True), fill=TEXT)
    y += 108

    # actions
    card(draw, (36, y, W - 36, H - 90), fill=CARD)
    draw.text((56, y + 16), "看完马上做", font=font(28, True), fill=AMBER)
    actions = [
        "打开用量面板 / 命令行查本周剩余",
        "重任务尽量排在临时额度结束前",
        "准备备用链路，避免单厂商卡死",
    ]
    ay = y + 60
    for a in actions:
        card(draw, (56, ay, W - 56, ay + 48), fill=CARD2, r=12)
        draw.text((76, ay + 10), a, font=font(26), fill=TEXT)
        ay += 56

    draw.text((36, H - 70), "9月14日起生效 · 以官方最终公告为准 · 本地草稿", font=font(24), fill=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="JPEG", quality=94)
    img.save(OUT_V, format="JPEG", quality=94)
    print(f"wrote {OUT}")
    print(f"wrote {OUT_V}")


if __name__ == "__main__":
    main()
