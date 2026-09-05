# Godot Knowledge

可复用规律与工具约定。探针工程：`projects/06-game-factory/visual_capability_probe/cursor-demo/`

## 下次开发优先读

| 主题 | 文档 |
|------|------|
| **rembg 抠图（D 盘，已就绪）** | [rembg-d-drive.md](rembg-d-drive.md) |
| 画面探针验收 | [ACCEPTANCE.md](../../projects/06-game-factory/visual_capability_probe/cursor-demo/docs/ACCEPTANCE.md) |
| MCP 验证环 | [VERIFY_MCP.md](../../projects/06-game-factory/visual_capability_probe/cursor-demo/docs/VERIFY_MCP.md) |
| Playbook | [PB-Game-Visual.md](../../docs/playbooks/PB-Game-Visual.md) |

## 规律摘要（2026-09-05）

- Cursor 生图 + 绿幕可快速出素材；高质量抠图用 **D 盘 u2net**（见上表），勿用 C 盘、勿默认 bria 1GB。
- CharacterBody2D 会走出平台坠落；地面碰撞要宽于可走范围，或 clamp `min_x/max_x`。
- MCP 改 `.gd` 后 Area2D 可能仍跑旧脚本 → 重新 `attach_script` 或重开场景。
- Verifier：同时看 `position.x` 变化与 `y` / `velocity.y` 稳定。
- 写实精灵：Linear + Fix Alpha Border；棋盘格预览先于入库。
- HUD toast：`show_toast(text, seconds)` 且 seconds 设下限（防 MCP 传 0）。
