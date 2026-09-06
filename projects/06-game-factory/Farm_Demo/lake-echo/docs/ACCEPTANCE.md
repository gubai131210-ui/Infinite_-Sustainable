# ACCEPTANCE — Lake Echo R5

| Wave | 项 | 结果 | 证据 |
|------|----|------|------|
| 0 | 工程存在 TileMapLayer | PASS | `scenes/world.tscn` Ground/Water |
| 0 | 192×128 / world_size | PASS | `world.gd` W=192 H=128；CLI 运行无致命错 |
| 0 | 六区底图+标签 | PASS | `world.gd` ZONES + ZoneMarkers |
| 0 | 玩家 WASD + zoom=2 | PASS | `player.gd` / `main.gd` |
| 0 | Godot CLI 启动 | PASS | coding-solo run_project；仅 GDScript 警告 |
| 1 | 农场地标（谷仓/筒仓/农舍） | PASS | `prop_barn/silo/farmhouse` + landmarks.gd |
| 1 | Z1 锄地播种 | PASS | `farm_plots.gd` |
| 3–6 | 广场摊位/火车/灯塔剪影 | PARTIAL | landmarks 已放；密度与美术待深化 |
| 7 | golden_r5 全包 | PENDING | 待 MCP Connected 到 lake-echo |
