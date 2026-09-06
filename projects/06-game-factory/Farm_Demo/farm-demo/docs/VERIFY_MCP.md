# VERIFY_MCP — Farm_Demo Round4

Godot 打开 `farm-demo` 且 MCP Connected 到本工程。

## 环

1. `get_godot_status` → path 含 `Farm_Demo/farm-demo`
2. `run_scene({ scene: "res://scenes/main.tscn", wait_for_runtime: true })`
3. `get_errors` → 0
4. `call_method(/root/Main/World/FarmField, world_size)` → `(1536, 1024)`
5. 四向：warp 开阔地 → `move_*` press → wait → 查 `facing` + `animation` + **截图脸朝向** → release
6. 河岸 / 村口 / 总览截图 → `assets/qa/golden_r4/`
7. `GameBus.enter_house` → HouseInterior；床 `_do_interact`；出门
8. `stop_scene`

## 最近一次 MCP 复验（2026-09-06 R4）

| 断言 | 结果 |
|------|------|
| get_errors | 0 |
| world_size | (1536, 1024) |
| move_left | facing=(-1,0) · walk_left · golden `04_facing_left.png` |
| move_right | facing=(1,0) · walk_right · golden `05_facing_right.png` |
| move_up | facing=(0,-1) · walk_up · y↓ · golden `06_facing_up.png` |
| move_down | facing=(0,1) · walk_down · y↑ |
| 河岸 | `02_river_shore.png` |
| 村口 | `03_village_plaza.png` |
| 进屋 | `/root/HouseInterior` · `07_house_interior.png` |

## 本机

- F5；确认 A 朝左脸、D 朝右脸（粉边应明显减轻）
- 走上北阶 / 东进广场 / 南下牧场
- 农舍 E 进屋 · 床 E · 门口离开
