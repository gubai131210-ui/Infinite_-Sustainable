# Farm_Demo — 类星露谷可玩 Demo

**状态：可玩 Demo（无剧情）**  
**工程：** `farm-demo/`（Godot 4.6）

## Grill 锁定摘要

详见 [`docs/SPEC.md`](farm-demo/docs/SPEC.md)

- 俯视；种地环 + 背包；中等连续地图；五区 + 钓鱼
- 5 作物 / 5 NPC / 鸡牛羊；中文 UI
- 像素：程序绘制绿幕 → 色键抠图 → `assets/qa` 棋盘格

## 本机操作

1. 用 Godot 4.6 打开 `farm-demo/project.godot`
2. 确认插件 Godot MCP Connected（若要让 Agent 验收）
3. F5 运行

| 键 | 作用 |
|----|------|
| WASD | 移动 |
| 空格 | 使用当前工具 |
| 1–4 | 锄 / 壶 / 斧 / 竿 |
| E | 交互（对话/喂食/箱/钓/播种收割） |
| Tab / I | 背包 |

种地：走到耕地 → `1`+空格锄地 → Tab 选种子 → E 播种 → `2`+空格浇水（多次至成熟）→ E 收获。

## 美术管线

```powershell
cd "d:\Infinite_ Sustainable\projects\06-game-factory\Farm_Demo\farm-demo"
python tools\gen_pixel_assets.py
# 可选 rembg：
# $env:USE_REMBG=1; python tools\cutout_pipeline.py
```

## 验收

- [`farm-demo/docs/VERIFY_MCP.md`](farm-demo/docs/VERIFY_MCP.md)
- [`farm-demo/docs/ACCEPTANCE.md`](farm-demo/docs/ACCEPTANCE.md)

## 开工前必问（已答）

1. 深度：可玩 Demo  
2. 对接：新建 Farm_Demo + 复用探针管线  
3. 允许：代码 / MCP / 生图抠图 / 推 GitHub  
