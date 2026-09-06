# Perfect Game — 橡木湾 Oakhaven

**状态：编辑器可玩竖切 Demo（六区/种地/对话/进出建筑）**  
**工程：** `perfect-game/`（Godot 4.6）

## Grill 锁定

- 参考图：`perfect-game/docs/ref/oakhaven_overview.jpg`
- 六区拓扑相对位置一比一；中文木牌
- 种地 / 对话 / ≥6 进出建筑 / ≥12 可交互 NPC
- 像素风；itch 级 Windows 试玩

详见 [`perfect-game/docs/SPEC.md`](perfect-game/docs/SPEC.md) · [`GOAL_OAKHAVEN.md`](perfect-game/docs/GOAL_OAKHAVEN.md)

## 本机操作

1. Godot 4.6 打开 `perfect-game/project.godot`
2. 确认主场景 `res://scenes/main.tscn`
3. F5 运行

| 键 | 作用 |
|----|------|
| WASD | 移动 |
| 1–4 | 锄 / 壶 / 斧 / 竿 |
| 空格 | 使用工具 |
| E | 交互（对话/进门/摸动物） |
| Tab / I | 背包 |

## 资产重建（可选）

```powershell
cd "d:\Infinite_ Sustainable\projects\06-game-factory\perfect_game\perfect-game"
python tools\gen_tileset_master.py
```

## 导出

见 [`docs/PLAYTEST.md`](perfect-game/docs/PLAYTEST.md) 与 `export_presets.cfg`。

## 禁止偷懒

- 禁止单张大图冒充可走世界
- 禁止跳过六区对照就宣称一比一
- 禁止 NPC 无对话
- 禁止未经验证宣称可发布
