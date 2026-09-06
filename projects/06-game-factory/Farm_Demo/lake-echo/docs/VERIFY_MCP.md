# VERIFY_MCP — Lake Echo R5

## Wave0

1. Godot 打开 `Farm_Demo/lake-echo/`（非 farm-demo）
2. MCP Connected 到该路径
3. `run_scene(res://scenes/main.tscn, wait_for_runtime=true)`
4. `get_errors` → 0
5. `call_method(/root/Main/World, world_size)` → `(3072, 2048)`
6. 截图 `assets/qa/golden_r5/00_wave0_overview.png`
7. `stop_scene`

## 本机

F5；出生农场；向东/北看到区标签。
