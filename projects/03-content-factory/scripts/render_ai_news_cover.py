"""Render denser AI news Xiaohongshu cover — keep palette, fix hollow layout."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "2026-09-04_ai_claude_code_limits" / "assets" / "cover.jpg"

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


def round_card(draw: ImageDraw.ImageDraw, xy, fill=CARD, outline=LINE, radius=18) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=2)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # left accent + top bar
    draw.rectangle((0, 0, 14, H), fill=BLUE)
    draw.rectangle((0, 0, W, 6), fill=BLUE)

    # header row: badge + date
    round_card(draw, (40, 36, 290, 92), fill=CARD2)
    draw.text((58, 50), "AI 资讯", font=font(28, True), fill=BLUE_SOFT)
    draw.text((320, 50), "额度口径拆解", font=font(28), fill=MUTED)
    draw.text((760, 50), "2026.09", font=font(28, True), fill=TEXT)

    # compact title block
    draw.text((40, 118), "Claude Code 周限额", font=font(52, True), fill=TEXT)
    draw.text((40, 185), "别只看“涨 25%”这半句", font=font(44, True), fill=AMBER)

    # two-column comparison — fills the hollow middle
    left = (40, 260, 520, 520)
    right = (560, 260, 1040, 520)
    round_card(draw, left, fill="#123528", outline="#1F6B4A")
    round_card(draw, right, fill="#3A1D24", outline="#7A3340")
    draw.text((64, 285), "好听的说法", font=font(28), fill=GREEN)
    draw.text((64, 340), "涨 25%", font=font(72, True), fill=GREEN)
    draw.text((64, 430), "相对：原始基线", font=font(30), fill="#A7F3D0")
    draw.text((64, 470), "官方宣传常用这个分母", font=font(26), fill=MUTED)

    draw.text((584, 285), "体感的说法", font=font(28), fill=RED)
    draw.text((584, 340), "少约 17%", font=font(72, True), fill=RED)
    draw.text((584, 430), "相对：今天额度", font=font(30), fill="#FECACA")
    draw.text((584, 470), "临时+50%结束后的落差", font=font(26), fill=MUTED)

    # formula strip
    round_card(draw, (40, 548, 1040, 690), fill=CARD)
    draw.text((64, 568), "换算一眼看懂", font=font(28, True), fill=BLUE_SOFT)
    # three pills
    pills = [
        (64, "基线", "100", MUTED),
        (360, "临时促销", "150", AMBER),
        (700, "永久后", "125", GREEN),
    ]
    for x, label, val, color in pills:
        round_card(draw, (x, 610, x + 250, 670), fill=CARD2)
        draw.text((x + 18, 622), f"{label} {val}", font=font(30, True), fill=color)
    draw.text((320, 622), "→", font=font(30, True), fill=MUTED)
    draw.text((660, 622), "→", font=font(30, True), fill=MUTED)

    # timeline dense rows
    round_card(draw, (40, 714, 1040, 980), fill=CARD)
    draw.text((64, 734), "时间线 / 关键变化", font=font(28, True), fill=TEXT)
    rows = [
        ("现在～9/13", "临时 +50% 仍有效", "先用手头额度"),
        ("9/14 起", "改永久 +25%（相对基线）", "相对今天约 -17%"),
        ("消耗提醒", "长上下文 / 重模型更吃额度", "别换算成固定条数"),
    ]
    y = 790
    for a, b, c in rows:
        draw.rectangle((64, y, 1016, y + 1), fill=LINE)
        draw.text((64, y + 14), a, font=font(26, True), fill=BLUE_SOFT)
        draw.text((300, y + 14), b, font=font(26), fill=TEXT)
        draw.text((760, y + 14), c, font=font(24), fill=MUTED)
        y += 58

    # action checklist — removes empty bottom
    round_card(draw, (40, 1004, 1040, 1288), fill=CARD)
    draw.text((64, 1024), "看完你可以马上做", font=font(28, True), fill=AMBER)
    actions = [
        "1. 打开用量面板 / 命令行查本周剩余",
        "2. 重任务先排在 9/13 前（若仍享临时额度）",
        "3. 准备备用链路：Cursor / Codex / 其它模型",
        "4. 别被单边标题带节奏，先问「相对谁」",
    ]
    y = 1078
    for line in actions:
        round_card(draw, (64, y, 1016, y + 44), fill=CARD2, radius=12)
        draw.text((84, y + 8), line, font=font(26), fill=TEXT)
        y += 52

    draw.text((40, 1320), "9月14日起按新口径生效", font=font(30, True), fill=TEXT)
    draw.text((40, 1370), "以官方最终公告为准 · 本地草稿未发布", font=font(24), fill=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="JPEG", quality=93)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
