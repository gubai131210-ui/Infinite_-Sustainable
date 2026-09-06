# Perfect Game — 纸片沙盘（Paper Isle）

**状态：可玩 MVP**  
**工程：** `perfect-game/`（Godot 4.6）  
**品类：** 纸片/插画风俯视沙盘（与 Farm_Demo 差异化）

## Grill 锁定摘要

详见 [`perfect-game/docs/SPEC.md`](perfect-game/docs/SPEC.md)

- 深度：可玩 MVP
- 硬约束：**无缝地形 tileset** + rembg/色键抠图道具拼接
- 画风：纸片/插画（利于抠图）
- 玩法：在沙盘岛上走动，收集纸星
- 允许：代码 / MCP / 生图抠图 / 推 GitHub

## 本机操作

1. 用 Godot 4.6 打开 `perfect-game/project.godot`
2. 可选：启用 Godot MCP 后按 `docs/VERIFY_MCP.md` 验收
3. F5 运行

| 键 | 作用 |
|----|------|
| WASD / 方向键 | 移动 |
| 1 / 2 | 手持灯笼 / 花丛 |
| E / 空格 | 摆放 / 和纸狐打招呼 |
| 靠近纸星 | 自动拾取 |

### 玩法循环

1. 捡齐 5 颗漂浮纸星  
2. 小屋旁出现光圈 → 站上去按 E 摆件（攒温馨值）  
3. 纸狐出现并跟随 → 靠近按 E 打招呼 → 通关后可继续漫步  

## 美术管线

```powershell
cd "d:\Infinite_ Sustainable\projects\06-game-factory\perfect_game\perfect-game"
python tools\import_and_build_assets.py
# 可选 rembg（模型在 visual_capability_probe D 盘约定路径）：
# $env:USE_REMBG="1"; python tools\import_and_build_assets.py
```

## 开工前必问（已答）

1. 深度：可玩 MVP  
2. 无缝地形：必须  
3. 题材：纸片沙盘  
4. 画风：纸片/插画  
5. 允许：代码 / MCP / 生图 / GitHub  
6. 与 Farm：差异化新品类  

## 禁止偷懒

- 禁止用纯色 ColorRect 冒充纸片地形
- 禁止跳过 `assets/qa/seam_*` 拼缝验收图
- 禁止道具不抠图直接带底图进场景
- 禁止 Player / World / HUD 堆成无结构单场景
- 禁止无截图/无 seam 指标宣称「无缝完成」
- 禁止复刻 Farm 种地环应付新品类
