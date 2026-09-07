# Visual QA — Oakhaven

> Godot 改图后：**运行 → 截图 → 打分 → 再改**。  
> 禁止无截图宣称「不割裂」。

## 三档缩放

| 档 | 问 |
|----|----|
| Zoomed Out | 区域可读？大地标明显？像世界还是像瓦片网格？ |
| Gameplay Zoom | 路合理？建筑接地？过渡自然？变化够吗？ |
| Close Zoom | 瓦片重复？接缝硬？边不自然？装饰过随机？ |

## 打分卡（0–10）

```text
Tile Repetition:
Terrain Coherence:
Visual Variety:
Composition:
Building Integration:
Road Naturalness:
Decoration Density:
Palette Consistency:
World Cohesion:
```

## 反模式处置

若结果读作 `tile + tile + building + tile`：

1. **STOP** — 不要再加小装饰  
2. 回到 Macro / Region / Transition / Roads / Clusters  

若「太空」：不要均匀提高随机装饰密度；改善地形形状、区域结构、路径、簇、地标、中尺度构图。

## 证据槽

- golden：`assets/qa/golden/*.png`  
- Critic：`VISUAL_CRITIC_OVERVIEW.md`  
- itch 主图判定：World Cohesion 与 Composition 未达「商店页可直接当主图」前保持 **否**
