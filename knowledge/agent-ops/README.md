# Agent Ops Knowledge

运营多 Agent 团队的可复用规律（非流水账）。

## 2026-09-05 — v1→v2

- **事实：** v1 仅有提示词角色名，无路由/Playbook/证据槽；Godot 写实链路缺 Asset+Verifier。
- **规律：** 语义角色与 Cursor Task 载体分离；游戏类验收必须截图或 runtime，文档类可用 diff。
- **规律：** `.cursor/agents` 必须薄适配，完整逻辑只活在 `prompts/`。
- **反模式：** 主对话自称全团队却无 handoff、无证据。
- **资产：** Godot/写实抠图用 D 盘 rembg（`knowledge/godot/rembg-d-drive.md`），禁止默认写入 C: 用户缓存。

## 指针

- `docs/agent-team-v2.md`
- `docs/routing-table.md`
- `docs/handoff-v2.md`
- `docs/playbooks/`
