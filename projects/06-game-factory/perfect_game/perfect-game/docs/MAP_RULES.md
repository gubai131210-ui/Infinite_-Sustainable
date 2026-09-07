# Map Rules — Oakhaven（Godot 实现分层）

实现时分离职责（禁止巨型单脚本一把梭）：

| 层 | 负责 |
|----|------|
| World Layout | 区域、主地形、道路、水系、建筑位点 |
| Terrain Rendering | 过渡、autotile/接缝、边角变体 |
| Decoration | 树/石/花/草/道具簇 |
| Gameplay Objects | NPC、交互、作物、进出建筑 |

工程映射（现有）：

- Layout / terrain：`scripts/world.gd`  
- Landmarks：`scripts/landmarks.gd`  
- Decor / NPC：`scripts/decor.gd`  
- 玩法实体：`farm_plots.gd` / `player.gd` / interiors  

## 道路

少用完美矩形；偏好曲线、宽窄变化、分叉、磨损边、草侵入；必须连接有意义地点。

## 水体

不规则岸线 + 过渡 + 岸边植被/石/芦苇；避免矩形天然池塘。

## 留白

不要填满每一格。留白用于分区、强调地标、呼吸感、引导移动。
