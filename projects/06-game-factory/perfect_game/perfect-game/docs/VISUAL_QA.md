# Visual QA — Oakhaven

> Godot 改图后：**运行 → 截图 → 打分 → 再改**。  
> 禁止无截图宣称「不割裂」。

## 三档缩放

| 档 | 问 |
|----|----|
| Zoomed Out | 区域可读？大地标明显？像世界还是像瓦片网格？ |
| Gameplay Zoom | 路合理？建筑接地？过渡自然？变化够吗？ |
| Close Zoom | 瓦片重复？接缝硬？边不自然？装饰过随机？ |

## 打分卡（0–10）· P161 · 2026-09-07

证据：`assets/qa/golden/00_overview.png` + `06_lake.png` + `GOLDEN_CAPTURE_DONE`

```text
Tile Repetition:        5
Terrain Coherence:      6
Visual Variety:         6
Composition:            6
Building Integration:   6
Road Naturalness:       7
Decoration Density:     5
Palette Consistency:    7
World Cohesion:         6
```

### 本轮相对 P160

| 项 | 变化 |
|----|------|
| 树冠 | pine/meadow 改为 lobe 簇 + 走廊开窗；叠层错位 — 条带感↓ |
| 路缘 | GD fringe 含 dirt + spit shoulders — Road Naturalness ↑ |
| 湖岸 | 外圈沙/草 dither，少硬 WE 环 — 近景仍偏硬 |

### 反模式处置

若结果仍读作 `tile + tile + building + tile`：

1. **STOP** — 不要再加小装饰  
2. 回到 Macro / Region / Transition / Roads / Clusters  

## 证据槽

- golden：`assets/qa/golden/*.png`  
- Critic：`VISUAL_CRITIC_OVERVIEW.md`  
- itch 主图：**否**（World Cohesion 6 / 距参考海报仍差；缺试玩签字 + itch URL）
