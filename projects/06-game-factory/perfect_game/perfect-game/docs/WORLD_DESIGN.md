# World Design — Oakhaven（世界驱动流程）

> 强制流程来自 [ChatGPT 分享](https://chatgpt.com/share/6a9e585e-6e10-83ea-98fc-30457ff86eac)：  
> **不要从 Tile 开始。**

## 禁止的工作流（Asset-driven）

```text
找素材 → 切 Tile → TileMap → 铺满 → 放建筑 → 补草 → 完成
```

## 强制工作流（World-driven）

```text
世界观
  → 地图大布局（Macro）
  → 区域划分
  → 道路 / 水系
  → 建筑群
  → Terrain
  → Decoration
  → Tile
  → Godot 实现
  → 截图 Visual QA
  → 返工（优先改构图，禁止只堆碎屑）
```

## 分阶段闸门（每步可验收）

| Step | 产出 | 检查 |
|------|------|------|
| 1 Macro Layout | 区域块/主道路/水系/地标草图 | 远景可读 |
| 2 Macro Review | Critic / Art Director 签字 | 不像棋盘 |
| 3 Terrain Layout | 有机边界 + 过渡带 | 无大矩形自然区 |
| 4 Terrain Review | 岸线/土草接缝 | vs stitch 参考 |
| 5 Building clusters | 院落/入口/邻接 | 建筑不漂浮 |
| 6 Roads | 曲线/分叉/磨损边 | 连接有意义地点 |
| 7 Vegetation | 密度梯度 + 簇 | 非均匀噪声 |
| 8 Decoration | 中尺度道具簇 | 服务构图 |
| 9 Godot | layers 分离实现 | 见 MAP_RULES |
| 10 Screenshot QA | `VISUAL_QA.md` 打分 | World Cohesion≥目标 |
| 11 Rework | 按 QA 优先序返工 | 禁止只加小装饰 |

## 区域开工模板（写完再动代码）

```text
REGION:
PURPOSE:
PRIMARY LANDMARK:
TERRAIN:
ROAD STRUCTURE:
VEGETATION DENSITY:
BUILDING DENSITY:
PALETTE:
TRANSITION AREAS:
DECORATION:
EMPTY SPACE:
PLAYER FLOW:
```

## 与现有六区

Z1 米勒农庄 · Z2 橡木河/瀑布 · Z3 镇广场 · Z4 火车站 · Z5 梯田 · Z6 回声湖  

每个新区/重做区必须先填上表，再改 `world.gd` / landmarks / decor。
