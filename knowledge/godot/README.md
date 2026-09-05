# Godot — visual probe notes

## 2026-09-05

- **事实：** Cursor 生图 + 绿幕色键可快速入库；rembg 默认 bria 模型约 1GB，本机下载过慢不宜阻塞探针。
- **事实：** CharacterBody2D 会走出 StaticBody2D 平台边缘坠落；探针地面需远宽于可走范围。
- **规律：** Verifier 必须同时看 `position.x` 变化与 `y`/`velocity.y` 稳定，避免“移动了但已掉出世界”的假阳性。
- **规律：** 写实精灵导入用 Linear + Fix Alpha Border；棋盘格预览先于入库。
