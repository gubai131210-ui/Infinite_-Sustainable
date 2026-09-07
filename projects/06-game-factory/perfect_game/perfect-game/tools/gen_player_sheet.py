"""Generate Oakhaven player sheet — clear walk legs + tool actions (Stardew-like).

Layout (48px cells):
  Rows 0-3: walk down / left / right / up — 6 frames each (idle + stride)
  Rows 4-7: hoe down / left / right / up — 4 frames
  Rows 8-11: water down / left / right / up — 4 frames
  Rows 12-15: plant/seed down / left / right / up — 4 frames

Walk cycle (Stardew wiki pattern): contact → lift L → contact → lift R
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "processed" / "player.png"
QA = ROOT / "assets" / "qa" / "player_sheet_preview.png"
CELL = 48
COLS = 6
ROWS = 16  # 4 walk + 4 hoe + 4 water + 4 plant

# palette — blue-shirt boy (LOCKED)
SKIN = (240, 198, 160, 255)
SKIN_S = (210, 160, 120, 255)
HAIR = (92, 58, 36, 255)
SHIRT = (70, 140, 220, 255)
SHIRT_S = (50, 110, 180, 255)
PANTS = (90, 70, 50, 255)
PANTS_S = (70, 52, 38, 255)
SHOE = (50, 40, 35, 255)
OUTLINE = (30, 24, 20, 255)
HOE = (160, 160, 170, 255)
HOE_H = (130, 90, 50, 255)
CAN = (90, 140, 200, 255)
SEED = (220, 180, 80, 255)


def blank() -> Image.Image:
    return Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))


def px(img: Image.Image, x: int, y: int, c) -> None:
    if 0 <= x < CELL and 0 <= y < CELL:
        img.putpixel((x, y), c)


def rect(img, x0, y0, x1, y1, c) -> None:
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(img, x, y, c)


def oval(img, cx, cy, rx, ry, c) -> None:
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx) / max(rx, 1)) ** 2 + ((y - cy) / max(ry, 1)) ** 2 <= 1.0:
                px(img, x, y, c)


def draw_shadow(img) -> None:
    oval(img, 24, 44, 9, 3, (20, 20, 30, 70))


def draw_head(img, cx: int, cy: int, facing: str) -> None:
    oval(img, cx, cy, 7, 7, OUTLINE)
    oval(img, cx, cy, 6, 6, SKIN)
    # hair
    if facing == "up":
        oval(img, cx, cy - 2, 7, 5, HAIR)
        rect(img, cx - 6, cy - 1, cx + 6, cy + 2, HAIR)
    else:
        oval(img, cx, cy - 3, 7, 4, HAIR)
        rect(img, cx - 6, cy - 5, cx + 6, cy - 1, HAIR)
        if facing == "down":
            px(img, cx - 3, cy - 1, HAIR)
            px(img, cx + 3, cy - 1, HAIR)
    # eyes
    if facing == "down":
        px(img, cx - 2, cy, OUTLINE)
        px(img, cx + 2, cy, OUTLINE)
    elif facing == "left":
        px(img, cx - 3, cy, OUTLINE)
    elif facing == "right":
        px(img, cx + 3, cy, OUTLINE)


def draw_torso(img, cx: int, cy: int, facing: str, lean: int = 0) -> None:
    tx = cx + lean
    rect(img, tx - 6, cy, tx + 6, cy + 10, OUTLINE)
    rect(img, tx - 5, cy + 1, tx + 5, cy + 9, SHIRT)
    rect(img, tx - 5, cy + 8, tx + 5, cy + 9, SHIRT_S)
    if facing in ("left", "right"):
        # sleeve hint
        sx = tx - 6 if facing == "left" else tx + 6
        rect(img, sx - 1, cy + 2, sx + 1, cy + 7, SHIRT)


def draw_legs(img, cx: int, cy: int, facing: str, phase: int) -> None:
    """phase 0..5 — exaggerated stride so legs clearly move."""
    # Stardew-like: 0/3 plant, 1/4 lift-left, 2/5 lift-right-ish
    plant = phase % 3 == 0
    left_fwd = phase in (1, 4)
    right_fwd = phase in (2, 5)

    def leg(ox: int, oy: int, shoe_ox: int = 0) -> None:
        rect(img, cx + ox - 2, cy + oy, cx + ox + 1, cy + oy + 8, OUTLINE)
        rect(img, cx + ox - 1, cy + oy + 1, cx + ox, cy + oy + 7, PANTS)
        rect(img, cx + ox - 2 + shoe_ox, cy + oy + 8, cx + ox + 1 + shoe_ox, cy + oy + 10, SHOE)

    if facing in ("down", "up"):
        # both legs visible; stride shifts feet
        if plant:
            leg(-3, 0, 0)
            leg(3, 0, 0)
        elif left_fwd:
            leg(-4, -2, -1)  # lifted / forward
            leg(3, 1, 1)  # planted back
        else:
            leg(-3, 1, -1)
            leg(4, -2, 1)
    elif facing == "left":
        # side profile — alternate front/back leg
        if plant:
            leg(-1, 0, -1)
            leg(2, 0, 1)
        elif left_fwd:
            leg(-4, -2, -2)
            leg(2, 1, 1)
        else:
            leg(0, 1, 0)
            leg(-3, -2, -2)
    else:  # right
        if plant:
            leg(-2, 0, -1)
            leg(1, 0, 1)
        elif left_fwd:
            leg(4, -2, 2)
            leg(-2, 1, -1)
        else:
            leg(0, 1, 0)
            leg(3, -2, 2)


def draw_arms_walk(img, cx: int, cy: int, facing: str, phase: int) -> None:
    swing = 1 if phase % 2 else -1
    if facing == "down":
        rect(img, cx - 8, cy + 2 + swing, cx - 6, cy + 8, SKIN)
        rect(img, cx + 6, cy + 2 - swing, cx + 8, cy + 8, SKIN)
    elif facing == "up":
        rect(img, cx - 8, cy + 2 - swing, cx - 6, cy + 7, SKIN)
        rect(img, cx + 6, cy + 2 + swing, cx + 8, cy + 7, SKIN)
    elif facing == "left":
        rect(img, cx - 9, cy + 3 + swing, cx - 7, cy + 9, SKIN)
    else:
        rect(img, cx + 7, cy + 3 + swing, cx + 9, cy + 9, SKIN)


def walk_frame(facing: str, phase: int) -> Image.Image:
    img = blank()
    draw_shadow(img)
    bob = -1 if phase % 2 else 0
    head_y = 12 + bob
    torso_y = 18 + bob
    leg_y = 28 + bob
    draw_legs(img, 24, leg_y, facing, phase)
    draw_torso(img, 24, torso_y, facing)
    draw_arms_walk(img, 24, torso_y, facing, phase)
    draw_head(img, 24, head_y, facing)
    return img


def tool_frame(facing: str, kind: str, phase: int) -> Image.Image:
    """phase 0..3 for hoe/water/plant."""
    img = blank()
    draw_shadow(img)
    lean = 0
    if kind == "hoe":
        lean = [0, -1, -2, 1][phase] if facing == "left" else [0, 1, 2, -1][phase]
        if facing in ("down", "up"):
            lean = 0
    elif kind == "water":
        lean = 1 if facing == "right" else (-1 if facing == "left" else 0)
    head_y = 12
    torso_y = 18
    leg_y = 28
    # planted stance
    draw_legs(img, 24, leg_y, facing, 0 if phase < 2 else 1)
    draw_torso(img, 24, torso_y, facing, lean)
    draw_head(img, 24 + lean // 2, head_y, facing)

    # tool graphic
    if kind == "hoe":
        if facing == "down":
            # raise → strike
            hy = 8 + phase * 4
            rect(img, 28, hy, 30, hy + 10, HOE_H)
            rect(img, 26, hy + 10, 34, hy + 12, HOE)
        elif facing == "up":
            hy = 6 + phase * 3
            rect(img, 18, hy, 20, hy + 10, HOE_H)
            rect(img, 14, hy + 10, 22, hy + 12, HOE)
        elif facing == "left":
            hx = 8 + (3 - phase) * 3
            rect(img, hx, 16, hx + 10, 18, HOE_H)
            rect(img, hx - 2, 14, hx, 22, HOE)
        else:
            hx = 30 + phase * 2
            rect(img, hx, 16, hx + 10, 18, HOE_H)
            rect(img, hx + 10, 14, hx + 12, 22, HOE)
    elif kind == "water":
        if facing == "down":
            rect(img, 30, 20, 36, 26, CAN)
            if phase >= 2:
                for i in range(4):
                    px(img, 32 + (i % 2), 30 + i, (120, 180, 240, 200))
        elif facing == "up":
            rect(img, 12, 18, 18, 24, CAN)
            if phase >= 2:
                for i in range(3):
                    px(img, 14, 14 - i, (120, 180, 240, 200))
        elif facing == "left":
            rect(img, 8, 20, 14, 26, CAN)
            if phase >= 2:
                for i in range(4):
                    px(img, 6 - i, 24, (120, 180, 240, 200))
        else:
            rect(img, 34, 20, 40, 26, CAN)
            if phase >= 2:
                for i in range(4):
                    px(img, 42 + i, 24, (120, 180, 240, 200))
    else:  # plant / seed toss
        if facing == "down":
            rect(img, 28, 22 - phase, 31, 26 - phase, SKIN)
            if phase >= 1:
                px(img, 30, 28 + phase, SEED)
                px(img, 32, 30 + phase, SEED)
        elif facing == "up":
            rect(img, 17, 20 - phase, 20, 24 - phase, SKIN)
            if phase >= 1:
                px(img, 18, 16 - phase, SEED)
        elif facing == "left":
            rect(img, 10 - phase, 22, 14 - phase, 25, SKIN)
            if phase >= 1:
                px(img, 8 - phase, 26, SEED)
        else:
            rect(img, 34 + phase, 22, 38 + phase, 25, SKIN)
            if phase >= 1:
                px(img, 40 + phase, 26, SEED)
    return img


def main() -> None:
    sheet = Image.new("RGBA", (COLS * CELL, ROWS * CELL), (0, 0, 0, 0))
    dirs = ["down", "left", "right", "up"]
    # walk rows 0-3
    for di, d in enumerate(dirs):
        for fi in range(6):
            fr = walk_frame(d, fi)
            sheet.paste(fr, (fi * CELL, di * CELL), fr)
    # hoe 4-7
    for di, d in enumerate(dirs):
        for fi in range(4):
            fr = tool_frame(d, "hoe", fi)
            sheet.paste(fr, (fi * CELL, (4 + di) * CELL), fr)
    # water 8-11
    for di, d in enumerate(dirs):
        for fi in range(4):
            fr = tool_frame(d, "water", fi)
            sheet.paste(fr, (fi * CELL, (8 + di) * CELL), fr)
    # plant 12-15
    for di, d in enumerate(dirs):
        for fi in range(4):
            fr = tool_frame(d, "plant", fi)
            sheet.paste(fr, (fi * CELL, (12 + di) * CELL), fr)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT)
    # checker preview
    prev = Image.new("RGBA", sheet.size, (40, 40, 48, 255))
    prev.alpha_composite(sheet)
    QA.parent.mkdir(parents=True, exist_ok=True)
    prev.convert("RGB").save(QA, quality=92)
    print("OK", OUT, sheet.size)


if __name__ == "__main__":
    main()
