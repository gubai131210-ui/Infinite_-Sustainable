# 06 — AI Game Factory（Godot）

**状态：探针工程已建；团队走 v2 Playbook**  
**优先级：占位 → 可用 PB-Game-Visual 开工**

## 目标

升级为 AI 游戏开发流水线：Game Design → World → Quest → NPC → Item → Pixel Prompt → Sprite → Cleaner → Sheet → Godot Import → Code → Test。

不是“生成一张猫走路图”，而是可重复的资产与代码流水线。

## 当前探针

- 工程根：`visual_capability_probe/cursor-demo/`
- Playbook：[`docs/playbooks/PB-Game-Visual.md`](../../docs/playbooks/PB-Game-Visual.md)
- 角色：Game / Asset / Builder / Verifier（见 Agent Team v2）

## 关联

- Knowledge: `knowledge/godot/`（待沉淀）
- Agent ops: `knowledge/agent-ops/`
- Skill 占位: image-generation

## 开工前必问

1. 这次要做到什么深度？（骨架 / MVP / 可发布）
2. 是否对接已有 Godot 工程路径？
3. 是否允许写真实代码 / 接 MCP / 生图 / 发内容？目标引擎版本？

## 禁止偷懒

- 禁止只生成散图不接入 Godot
- 禁止无 Verifier 截图/runtime 证据的“做完了”
- 禁止把所有关卡/UI/系统堆在一个场景文件应付
- 禁止伪造未实现的 Quest/NPC 全流水线
