"""Render AI news Xiaohongshu cover with real Chinese typography."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "2026-09-04_ai_claude_code_limits" / "assets" / "cover.jpg"

W, H = 1080, 1440
FONT_REG = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size=size, index=0)


def main() -> None:
    img = Image.new("RGB", (W, H), "#101820")
    draw = ImageDraw.Draw(img)

    # accent bar
    draw.rectangle((0, 0, 16, H), fill="#3B82F6")
    draw.rectangle((0, 0, W, 8), fill="#3B82F6")

    # top label
    draw.text((64, 72), "AI 资讯 · 额度口径", font=font(36), fill="#93C5FD")

    # headline
    draw.text((64, 150), "Claude Code", font=font(64, bold=True), fill="#F8FAFC")
    draw.text((64, 240), "额度到底怎么算？", font=font(72, bold=True), fill="#FFFFFF")

    # highlight box
    box = (64, 380, W - 64, 780)
    draw.rounded_rectangle(box, radius=28, fill="#1E293B", outline="#334155", width=2)
    draw.text((96, 420), "你会同时看到两种说法", font=font(40, bold=True), fill="#FBBF24")
    draw.text((96, 500), "涨 25%", font=font(88, bold=True), fill="#34D399")
    draw.text((420, 540), "相对原始基线", font=font(36), fill="#94A3B8")
    draw.text((96, 620), "少约 17%", font=font(88, bold=True), fill="#F87171")
    draw.text((460, 660), "相对今天正在用的额度", font=font(36), fill="#94A3B8")

    # detail rows
    rows = [
        ("临时促销", "+50%", "用到 9/13"),
        ("永久调整", "+25%", "相对基线"),
        ("体感变化", "-17%", "相对今天"),
    ]
    y = 860
    for label, value, note in rows:
        draw.rounded_rectangle((64, y, W - 64, y + 110), radius=20, fill="#0F172A", outline="#1E293B", width=2)
        draw.text((96, y + 30), label, font=font(34), fill="#94A3B8")
        draw.text((360, y + 22), value, font=font(48, bold=True), fill="#F8FAFC")
        draw.text((620, y + 34), note, font=font(32), fill="#CBD5E1")
        y += 130

    draw.text((64, H - 120), "9月14日起生效", font=font(36, bold=True), fill="#E2E8F0")
    draw.text((64, H - 70), "数字以官方最终公告为准 · 本地草稿未发布", font=font(28), fill="#64748B")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="JPEG", quality=92)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
