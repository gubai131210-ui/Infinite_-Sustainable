## TASK HANDOFF v2

### Meta
- handoff_id: 2026-09-06-builder-lake-echo-w0
- playbook: PB-Game-Visual
- from_agent: Builder
- to_agent: Verifier
- parallel_group: lake-echo-w0

### Objective
Wave0 Foundation：lake-echo 工程可运行，TileMap 六区底图，MCP 就绪。

### Completed
- 创建 `projects/06-game-factory/Farm_Demo/lake-echo/`
- `tileset_master.png` + runtime TileSet
- 六区底图绘制 + 标签 + 水/崖碰撞
- Player WASD + Camera zoom=2 + HUD
- Autoload + godot_mcp 已拷贝

### Acceptance
- [ ] Godot 打开 lake-echo 且 MCP Connected 到该路径
- [ ] run_scene main → get_errors=0
- [ ] world_size=(3072,2048)
- [ ] 截图存 assets/qa/golden_r5/00_wave0_overview.png

### Do-Not
- 禁止继续用 farm-demo Sprite 铺地
- 禁止宣称六区地标已完成（仅底图）
- 禁止跳过 MCP 换工程路径

### Suggested Next Agent
Verifier → 然后 Wave1 Z1_FARM Asset‖Builder
