"""Horizontal AI news poster: clear regional panels (not a crowded vertical stack)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "2026-09-04_ai_claude_code_limits" / "assets"
# 横版大图 16:9，适合桌面/长图；封面可再裁或作头图
W, H = 1920, 1080

BG = "#0B1220"
PANEL = "#152033"
PANEL2 = "#1B2740"
LINE = "#334155"
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


def panel(draw: ImageDraw.ImageDraw, xy, fill=PANEL, outline=LINE, r=20) -> None:
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=2)


def main() -> None:
    """
    横向四区：
    ① 事件说明  ② 宣传口径(+25%)  ③ 体感口径(-17%)  ④ 行动建议
    顶栏一条标题，底栏一条免责。
    """
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 8), fill=BLUE)

    # top bar
    draw.text((48, 36), "AI 资讯", font=font(28, True), fill=BLUE_SOFT)
    draw.text((180, 32), "Claude Code 周限额：同一公告，两种读法", font=font(42, True), fill=TEXT)
    draw.text((1680, 40), "2026.09", font=font(28, True), fill=MUTED)

    # four equal columns with gaps
    margin, gap, top, bottom = 40, 24, 110, H - 70
    usable = W - margin * 2 - gap * 3
    col_w = usable // 4
    cols = []
    x = margin
    for _ in range(4):
        cols.append((x, top, x + col_w, bottom - 10))
        x += col_w + gap

    # ① 事件
    panel(draw, cols[0], fill=PANEL2)
    x0, y0, x1, y1 = cols[0]
    draw.text((x0 + 28, y0 + 28), "① 事件", font=font(28, True), fill=BLUE_SOFT)
    draw.text((x0 + 28, y0 + 90), "发生了什么", font=font(36, True), fill=TEXT)
    lines = [
        "临时促销 +50%",
        "用到 9/13",
        "",
        "9/14 起改为",
        "永久 +25%",
        "（相对原始基线）",
        "",
        "官方后来澄清：",
        "相对今天约少 17%",
    ]
    yy = y0 + 170
    for line in lines:
        draw.text((x0 + 28, yy), line, font=font(28), fill=TEXT if line else MUTED)
        yy += 48

    # ② 宣传口径
    panel(draw, cols[1], fill="#123528", outline="#1F6B4A")
    x0, y0, x1, y1 = cols[1]
    draw.text((x0 + 28, y0 + 28), "② 宣传口径", font=font(28, True), fill=GREEN)
    draw.text((x0 + 28, y0 + 100), "涨 25%", font=font(96, True), fill=GREEN)
    draw.text((x0 + 28, y0 + 240), "相对：原始基线", font=font(32, True), fill="#A7F3D0")
    draw.text((x0 + 28, y0 + 320), "好听的分母", font=font(28), fill=MUTED)
    for i, t in enumerate(["官方常用这个说法", "相对「过去标准」是涨", "不等于手头额度变多"]):
        draw.text((x0 + 28, y0 + 400 + i * 56), f"· {t}", font=font(28), fill=TEXT)

    # ③ 体感口径
    panel(draw, cols[2], fill="#3A1D24", outline="#7A3340")
    x0, y0, x1, y1 = cols[2]
    draw.text((x0 + 28, y0 + 28), "③ 体感口径", font=font(28, True), fill=RED)
    draw.text((x0 + 28, y0 + 100), "少约 17%", font=font(88, True), fill=RED)
    draw.text((x0 + 28, y0 + 240), "相对：今天额度", font=font(32, True), fill="#FECACA")
    draw.text((x0 + 28, y0 + 320), "正在用的分母", font=font(28), fill=MUTED)
    for i, t in enumerate(["临时 150 → 永久 125", "相对今天是下降", "重度用户体感最明显"]):
        draw.text((x0 + 28, y0 + 400 + i * 56), f"· {t}", font=font(28), fill=TEXT)

    # ④ 行动
    panel(draw, cols[3], fill=PANEL)
    x0, y0, x1, y1 = cols[3]
    draw.text((x0 + 28, y0 + 28), "④ 你可以做什么", font=font(28, True), fill=AMBER)
    draw.text((x0 + 28, y0 + 90), "行动区", font=font(36, True), fill=TEXT)
    actions = [
        ("查", "先看本周剩余用量"),
        ("排", "重任务尽量赶 9/13 前"),
        ("备", "准备第二工具链路"),
        ("问", "读公告先问「相对谁」"),
    ]
    yy = y0 + 180
    for tag, text in actions:
        panel(draw, (x0 + 24, yy, x1 - 24, yy + 100), fill=PANEL2, r=14)
        draw.text((x0 + 44, yy + 18), tag, font=font(32, True), fill=AMBER)
        draw.text((x0 + 44, yy + 56), text, font=font(28), fill=TEXT)
        yy += 120

    # bottom formula strip + disclaimer
    draw.rectangle((0, H - 64, W, H), fill="#070B14")
    draw.text(
        (48, H - 46),
        "换算：基线 100  →  临时 150  →  永久后 125      |      9月14日起生效 · 以官方最终公告为准 · 本地草稿未发布",
        font=font(26),
        fill=MUTED,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    landscape = OUT_DIR / "cover_landscape.jpg"
    img.save(landscape, format="JPEG", quality=94)
    # also keep as primary cover.jpg for this run (horizontal)
    img.save(OUT_DIR / "cover.jpg", format="JPEG", quality=94)
    print(f"wrote {landscape}")


if __name__ == "__main__":
    main()
