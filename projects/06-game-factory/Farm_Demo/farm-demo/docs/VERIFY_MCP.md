# VERIFY_MCP — Farm_Demo

Godot 打开 `farm-demo` 且 MCP Connected 后执行。

## 最小环

1. `run_scene({ scene: "res://scenes/main.tscn", wait_for_runtime: true })`
2. `get_errors` → 应为 0
3. `query_runtime_node(/root/Main/Player, [global_position])` 记起点
4. `send_input` `move_right` pressed → `wait(400)` → release；断言 x 增大
5. `send_input` `move_down` 同理；断言 y 增大
6. 走到耕地附近：`tool_1` + `use_tool` 锄地；换 `tool_2` 浇水（需先 E 播种）
7. 靠近 NPC：`call_method try_interact` 或本机 E → 对话层出现
8. `take_screenshot` 存证
9. `stop_scene`

## 本机手测

- 河流不可走；山丘不可走
- 树/花/动物/5 居民可见且可辨
- 背包 Tab；箱子 E 领种子；河边 4+E 钓鱼
- 完整：锄→播→浇→熟→收

## 注意

- 请勿在 `cursor-demo` 工程上跑本清单
- MCP 粘滞键：Player `_ready` 会 release 移动键
