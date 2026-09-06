# VERIFY_MCP — Paper Isle

## 前置

1. Godot 4.6 打开本工程，插件 Connected  
2. MCP server 监听正常（若 `ECONNREFUSED :6506`，先重启 Cursor / MCP）

## 步骤

1. `get_godot_status` → connected  
2. `run_scene` main（`wait_for_runtime=true`）  
3. `take_screenshot` → `assets/qa/golden/01_overview.png`  
4. `send_input` WASD 若干帧 → 再截 `02_moved.png`  
5. `get_errors` → 无致命  
6. 对照 `assets/qa/seam_*_3x3.png` 与 `seam_report.json`

## 降级（MCP 不可用）

用户本机 F5 + 自行把截图放入 `assets/qa/golden/`，Agent 不得谎称已 runtime 验收。
