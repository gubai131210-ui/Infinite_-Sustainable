# VERIFY_MCP — Game MVP（cursor_demo）

在 Godot 已打开本工程且 MCP Connected 时，Agent / 人工可按此环验收。

## 最小环

1. `run_scene({ scene: "res://scenes/main.tscn", wait_for_runtime: true })`
2. `get_errors` → 应为 0
3. `query_runtime_node(/root/Main/Player, [global_position])` 记下起点
4. `send_input` `move_right` pressed → `wait(400)` → release  
   断言：`x` 增大，`y` 大致稳定，`velocity.y≈0`
5. 走到门区 / 山路区：HUD 出现「按 E …」  
   - 本机：按 E  
   - MCP：`call_method try_interact` → `ToastLabel.text` 非空（或 `show_toast` 直调）
6. `take_screenshot` 存证
7. `stop_scene`

## 注意

- MCP 的 `InputEventAction` 可能粘滞；开局 `player._ready` 会 release 移动键
- 验收交互优先用 `try_interact`，本机用手按 E

## 本机手测

- F5；A/D 移动；靠近门/山路看提示；E 交互
- 看前景树是否仍有明显绿边（rembg 未就绪时以色键+scrub 为准）
