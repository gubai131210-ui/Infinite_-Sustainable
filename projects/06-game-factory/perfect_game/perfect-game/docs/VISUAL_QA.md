# Visual QA — Oakhaven

> Godot 改图后：**运行 → 截图 → 打分 → 再改**。  
> 禁止无截图宣称「不割裂」。

## 三档缩放

| 档 | 问 |
|----|----|
| Zoomed Out | 区域可读？大地标明显？像世界还是像瓦片网格？ |
| Gameplay Zoom | 路合理？建筑接地？过渡自然？变化够吗？ |
| Close Zoom | 瓦片重复？接缝硬？边不自然？装饰过随机？ |

## 打分卡（0–10）· P162 · 2026-09-07

证据：`00_overview` / `03_town` / `06_lake` + `GOLDEN_CAPTURE_DONE` · 0 script errors

```text
Tile Repetition:        5
Terrain Coherence:      6
Visual Variety:         6
Composition:            7
Building Integration:   7
Road Naturalness:       7
Decoration Density:     5
Palette Consistency:    7
World Cohesion:         6
```

### 本轮相对 P161

| 项 | 变化 |
|----|------|
| 路/田 | dirt-stitch 不再吃 PATH → 减少棋盘噪点 |
| 湖岸 | 陆地 fringe 禁 WE（仅沙/草/dirt）；WE 留在水层 |
| 镇区 | +6 民宅 + 院落 footing；广场 oval 略放大 |

## 证据槽

- Critic：`VISUAL_CRITIC_OVERVIEW.md`  
- itch 主图：**否**（World Cohesion 6；缺试玩签字 + itch URL）
