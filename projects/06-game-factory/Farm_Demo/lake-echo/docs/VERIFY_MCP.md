# VERIFY_MCP — Lake Echo R5

## 首选（MCP Connected 到 lake-echo）

1. 打开 `Farm_Demo/lake-echo/`（关掉 farm-demo）
2. MCP Connected 确认 path 含 `lake-echo`
3. `run_scene(main.tscn, wait_for_runtime=true)` → `get_errors=0`（允许 int 以外无 ERROR）
4. `call_method(/root/Main/World, world_size)` → `(3072, 2048)`
5. warp 六区截图 → `assets/qa/golden_r5/`
6. `GameBus.enter_house` → HouseInterior

**当前阻塞：** `user-godot-tomyud1` 常仍 Connected 到 `farm-demo/`。需人工关闭 farm-demo 编辑器后只开 lake-echo。

## CLI 后备（已用 · 权威本轮证据）

```text
Godot_v4.6.1-stable_mono_win64.exe --path lake-echo --import
Godot_v4.6.1-stable_mono_win64.exe --path lake-echo res://scenes/main.tscn -- --capture_golden
```

| 检查 | 结果 | 证据 |
|------|------|------|
| 启动无 SCRIPT ERROR | PASS（本轮 capture 无 Parse） | CLI stdout |
| golden 七张 | PASS | `assets/qa/golden_r5/00–06.png` |
| `GOLDEN_CAPTURE_DONE` | PASS | CLI |
| coding-solo run_project | PARTIAL | 曾有 missing landmark 竞态（import 前）；import 后 CLI OK |
| tomyud1 path=lake-echo | FAIL 待用户 | `get_godot_status` → farm-demo |

## 对照参考

- 总览 vs `docs/ref/frame_01.png`：拓扑可辨；密度/风格仍未达 Critic PASS 线
