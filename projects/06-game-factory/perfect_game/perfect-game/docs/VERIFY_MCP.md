# VERIFY_MCP — Oakhaven

1. 打开本工程，主场景 `res://scenes/main.tscn`
2. MCP Connected 后 `run_scene` + 分区 `take_screenshot`
3. 或 CLI：`godot --path . -- --capture_golden`
4. 截图落入 `assets/qa/golden/`
5. 对照 `docs/ref/oakhaven_overview.jpg` 六区相对位置

MCP `:6506` 不可用时，降级为本机 F5 + 用户截图，不得伪造。
