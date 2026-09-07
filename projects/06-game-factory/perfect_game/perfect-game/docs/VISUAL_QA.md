# Visual QA — Oakhaven

> Godot 改图后：**运行 → 截图 → 打分 → 再改**。  
> 禁止无截图宣称「不割裂」。

## 三档缩放

| 档 | 问 |
|----|----|
| Zoomed Out | 区域可读？大地标明显？像世界还是像瓦片网格？ |
| Gameplay Zoom | 路合理？建筑接地？过渡自然？变化够吗？ |
| Close Zoom | 瓦片重复？接缝硬？边不自然？装饰过随机？ |

## 打分卡（0–10）· P160 · 2026-09-07

证据：`assets/qa/golden/00_overview.png` + `06_lake.png` + `GOLDEN_CAPTURE_DONE`

```text
Tile Repetition:        5
Terrain Coherence:      6
Visual Variety:         6
Composition:            6
Building Integration:   6
Road Naturalness:       6
Decoration Density:     5
Palette Consistency:    7
World Cohesion:         5
```

### 本轮相对 P159

| 项 | 变化 |
|----|------|
| 路网 | 2–3 格实心脊 + 中谷 dirt ridge；overview 可读性↑，仍不及参考图连续 fringe |
| 中谷 | dirt meadows + 脊旁树簇密度梯度；死绿减少，仍偏空 |
| 湖形 | 多频 wobble，减弱正圆；近景岸线仍偏硬 |
| 树冠带 | meadow canopy 错位叠层减水平带感；北松冠仍偏条 |

### 反模式处置

若结果仍读作 `tile + tile + building + tile`：

1. **STOP** — 不要再加小装饰  
2. 回到 Macro / Region / Transition / Roads / Clusters  

若「太空」：不要均匀提高随机装饰密度；改善地形形状、区域结构、路径、簇、地标、中尺度构图。

## 证据槽

- golden：`assets/qa/golden/*.png`  
- Critic：`VISUAL_CRITIC_OVERVIEW.md`  
- itch 主图判定：World Cohesion / Composition 未达「商店页可直接当主图」→ **否**
