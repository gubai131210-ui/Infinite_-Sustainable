# Skill: Game Pixel Art Prompts（Farm / Godot）

**状态：可用**  
**用途：** 为 2D 游戏生成可入库的像素精灵（单帧 / 序列帧），禁止“几个色块冒充像素画”。

## 证据来源（网研摘要）

- 序列帧要写死：**帧数、单帧尺寸、横向 strip / 网格布局、透明或纯色底**
- Walk 循环最佳路径往往是 **静帧锚点 → I2V 原地踏步 → 抽关键帧 → 抠图 → 脚底对齐**（见 chongdashu / H3 Game Sprites）
- 本仓当前可用：**Cursor GenerateImage 静帧/条带** + Python 品红抠图 + nearest 降采样；无视频时用「4–8 帧横向 strip」提示词兜底

## 6 槽公式（游戏向）

```text
1. SUBJECT     角色/道具身份 + 服装配色 + 面向（front / 3/4 top-down）
2. STYLE       16-bit SNES / Stardew-like pixel art, limited palette 16–32 colors,
               crisp 1px outlines, no anti-alias smear
3. LIGHTING    flat game lighting, soft cel shade max 2 tones
4. COMPOSITION isolated subject, centered, full body, feet visible;
               OR horizontal sprite sheet N frames equal cells
5. MOOD        cozy farm / rustic village（按题材）
6. TECHNICAL   exact px size, solid MAGENTA #FF00FF **or** hot-pink #ED067A background,
               orthographic top-down, NO photoreal, NO blur, NO text
```

色键入库时必须同时抠：标准品红 + AI 常用玫红 `(r>190, g<80, b≈100–170)`。

## 负向词（必加）

```text
photorealistic, 3d render, blurry, soft focus, gradient mesh, watercolor,
vector flat icon, emoji, chibi giant head only, watermark, logo, UI text,
green screen spill, different scale per frame, cropped feet, modern UI chrome
```

## 比例契约（本 Demo）

| 资产 | 逻辑高度 | 说明 |
|------|----------|------|
| 玩家 / NPC | 48px | 序列帧单元格 48×48 |
| 鸡 | 16–20px | ≈ 人高 1/3 |
| 羊 | 24–28px | 略矮于人 |
| 牛 | 28–32px 宽 40+ | 体长大于人，身高略矮 |
| 树 | 64–96px | 明显高于人 |
| 地砖 | 16×16 | 可拼 tileset |

## 提示词模板

### A. 单角色静帧（锚点）

```text
SUBJECT: young farmer, blue shirt, brown pants, straw hat, holding nothing, front-facing full body
STYLE: 16-bit pixel art game sprite, Stardew Valley inspired, crisp pixels, limited palette
LIGHTING: flat game lighting, two-tone shade
COMPOSITION: centered full body, feet on ground plane, isolated
MOOD: cozy farm
TECHNICAL: orthographic slight top-down, solid magenta background #FF00FF,
exact readable silhouette, no anti-alias, no text
NEGATIVE: photorealistic, blurry, 3d, soft brush, watermark, UI
```

### B. 行走序列帧（横向 strip）

```text
SUBJECT: same young farmer walking in place, front view
STYLE: 16-bit pixel art sprite sheet
COMPOSITION: horizontal strip of EXACTLY 6 equal frames, each frame same size,
character aligned to bottom of each cell (foot-anchored), identical scale
TECHNICAL: magenta #FF00FF background, no gaps of different sizes,
treadmill walk cycle (does not travel across the image), loopable
NEGATIVE: camera pan, perspective change, frame size mismatch, blur
```

### C. 动物（强制写相对尺寸）

```text
SUBJECT: small farm chicken, tiny body, red comb
TECHNICAL: pixel art, height about one-third of a human farmer sprite,
solid magenta background, front 3/4 view, 4-frame horizontal idle bob strip
NEGATIVE: chicken as tall as human, giant chicken, chibi humanoid
```

## 入库流水线

1. 生成 → `assets/raw/`
2. 品红抠图 + fringe scrub → `assets/processed/`
3. nearest 缩放到比例契约
4. 棋盘格 QA → `assets/qa/checker_*`
5. Godot `TEXTURE_FILTER_NEAREST` + AnimatedSprite2D（走 8–10 FPS）

## 禁止偷懒

- 禁止用 8×8 色块冒充成品像素角色
- 禁止鸡/鸭与人同画布同高度
- 禁止无脚底对齐的序列帧直接进游戏
- 禁止跳过 QA 棋盘格
