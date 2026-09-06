# VERIFY_MCP — Lake Echo R5

## 首选（MCP Connected 到 lake-echo）

1. 打开 `Farm_Demo/lake-echo/`（关掉 farm-demo）
2. MCP Connected 确认 path 含 `lake-echo`
3. `run_scene(main.tscn, wait_for_runtime=true)` → `get_errors=0`
4. `call_method(/root/Main/World, world_size)` → `(3072, 2048)`
5. warp 六区截图 → `assets/qa/golden_r5/`
6. `GameBus.enter_house` → HouseInterior

## CLI 后备（已用）

```text
Godot_v4.6.1 ... --path lake-echo res://scenes/main.tscn -- --capture_golden
```

产出：`assets/qa/golden_r5/00_overview.png` … `06_lake.png` + `GOLDEN_CAPTURE_DONE`
