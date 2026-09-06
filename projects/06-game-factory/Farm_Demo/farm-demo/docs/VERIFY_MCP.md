# VERIFY_MCP — Farm_Demo Round3

Godot 打开 `farm-demo` 且 MCP Connected 到本工程。

## 环

1. `get_godot_status` → path 含 `Farm_Demo/farm-demo`
2. `run_scene({ scene: "res://scenes/main.tscn", wait_for_runtime: true })`
3. `get_errors` → 0
4. `call_method(/root/Main/World/FarmField, world_size)` → `(1536, 1024)`
5. 四向：`move_*` press → wait 300 → 查 `animation` 含方向；release
6. `GameBus.enter_house(Vector2)` → root 出现 `HouseInterior`；截图
7. `GameBus.exit_house()` → 回到 `Main`；玩家在门外附近
8. `Player.set("global_position", Vector2(480,800))` → y>640（扩图）
9. 截图存 `assets/qa/golden_r3/`
10. `stop_scene`

## 最近一次 MCP 复验（2026-09-06）

| 断言 | 结果 |
|------|------|
| get_errors | 0 |
| world_size | (1536, 1024) |
| Camera2D.zoom | (2, 2) |
| move_right | anim=`walk_right` · facing=(1,0) · x↑ |
| move_left | anim=`walk_left` · facing=(-1,0) · x↓ |
| move_up | anim=`walk_up` · facing=(0,-1) · y↓ (400→359) |
| move_down | anim=`walk_down` · facing=(0,1) · y↑ (359→557) |
| enter_house | `/root/HouseInterior` + Bed/Chest/Exit |
| bed | ToastLabel=`休息了一会儿，精神满满。` |
| chest | `_do_interact` OK（共享 `chest_claimed`） |
| exit | `/root/Main` · pos≈(560,360) |
| pasture | y≈796.9 > 640 · golden `03_south_pasture.png` |

## 本机

- F5；WASD 看四向；走到农舍门 E 进屋；床 E；门口离开
- 南下牧场 / 东进林地
