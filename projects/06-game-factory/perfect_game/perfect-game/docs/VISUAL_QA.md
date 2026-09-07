# Visual QA — Oakhaven

> Godot 改图后：**运行 → 截图 → 打分 → 再改**。  
> 禁止无截图宣称「不割裂」。

## 三档缩放

| 档 | 问 |
|----|----|
| Zoomed Out | 区域可读？大地标明显？像世界还是像瓦片网格？ |
| Gameplay Zoom | 路合理？建筑接地？过渡自然？变化够吗？ |
| Close Zoom | 瓦片重复？接缝硬？边不自然？装饰过随机？ |

## 打分卡（0–10）· P166 · 2026-09-07

证据：`00_overview`（decor 树簇可见）+ `GOLDEN_CAPTURE_DONE` + `smoke/21_plant_anim`

```text
Tile Repetition:        6
Terrain Coherence:      7
Visual Variety:         7
Composition:            7
Building Integration:   7
Road Naturalness:       7
Decoration Density:     7
Palette Consistency:    7
World Cohesion:         7
```

### 本轮相对 P165

| 项 | 变化 |
|----|------|
| 验证 | deferred decor 后 golden 重抓；中谷/房环树簇入画 |
| 动画 | plant freeze → `smoke/21_plant_anim.png` |
| 接缝 | 镇区草/土硬边仍在（未本轮改瓦） |

## 证据槽

- Critic：`VISUAL_CRITIC_OVERVIEW.md`  
- itch 主图：**否**（密度略好，接缝仍割裂；需试玩签字 + itch URL）
