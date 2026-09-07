# Agent Team v2 — 可编排 + 可验收

**状态：已落地骨架（提示词 + 协议 + Playbook）**  
**决策锁定：** T1=C · T2=A · T3=A · T4=A · T5=C（2026-09-05）

## 问题

v1 有 11 个角色名，但缺：强制路由、证据闭环、领域 Playbook、与 Cursor Task 的映射。表现为主对话一人包办；Godot/写实资产链路无人专责。

## 编制（L0–L4）

| 层 | 角色 | 文件（完整版） | Cursor 薄适配 |
|----|------|----------------|---------------|
| L0 | Core | `prompts/00-core/agent-core-operating-rules.md` | `.cursor/rules/00-agent-core.mdc` |
| L1 | Conductor | `prompts/01-orchestration/conductor.md` | `.cursor/agents/conductor.md` |
| L2 | Scout | `prompts/02-execution/scout.md` | `.cursor/agents/scout.md` |
| L2 | Researcher | `prompts/02-execution/researcher.md` | `.cursor/agents/researcher.md` |
| L2 | Planner | `prompts/02-execution/planner.md` | `.cursor/agents/planner.md` |
| L2 | Builder | `prompts/02-execution/builder.md` | `.cursor/agents/builder.md` |
| L2 | Verifier | `prompts/02-execution/verifier.md` | `.cursor/agents/verifier.md` |
| L2 | Critic | `prompts/02-execution/critic.md` | `.cursor/agents/critic.md` |
| L3 | Teacher / Memory / Reflection | `prompts/03-knowledge/*` | `.cursor/agents/*` |
| L4 | Content / Industrial / Experiment | `prompts/04-domain/*` | `.cursor/agents/*` |
| L4 | Game | `prompts/04-domain/game.md` | `.cursor/agents/game.md` |
| L4 | Asset | `prompts/04-domain/asset.md` | `.cursor/agents/asset.md` |

兼容别名：`orchestrator` → Conductor；`coder` → Builder；`reviewer` → Critic（审查）+ Verifier（证据）。

## 强制闭环

```text
Conductor → Scout/Researcher → Planner → Builder(+Asset/Game)
         → Verifier（证据）→ Critic（规范/需求）→ Memory（仅规律）
```

琐碎单文件修改可跳过 Scout/Researcher；**不可**跳过「有验收标准的任务」的 Verifier（证据强度见 T5）。

## 证据强度（T5=C）

| Playbook 类型 | Verifier 最低证据 |
|---------------|-------------------|
| 游戏 / 运行时画面 | 截图或 runtime 属性 + 无致命错误 |
| 代码逻辑 | 测试输出或可复现命令日志 |
| 文档 / 提示词 / OS 变更 | diff 摘要 + Critic 通过即可 |

## Cursor Task 映射（T3=A）

见 [routing-table.md](routing-table.md)。语义层用本团队角色；执行层可派 Cursor Task（explore/shell/bugbot/security-review 等），禁止两套职责互相打架。

## Playbook

| ID | 路径 |
|----|------|
| PB-Game-Visual | [playbooks/PB-Game-Visual.md](playbooks/PB-Game-Visual.md) |
| PB-Oakhaven-World | [playbooks/PB-Oakhaven-World.md](playbooks/PB-Oakhaven-World.md) |
| PB-Content | [playbooks/PB-Content.md](playbooks/PB-Content.md) |
| PB-Industrial | [playbooks/PB-Industrial.md](playbooks/PB-Industrial.md) |
| PB-Learn | [playbooks/PB-Learn.md](playbooks/PB-Learn.md) |
| PB-OS-Change | [playbooks/PB-OS-Change.md](playbooks/PB-OS-Change.md) |

## 交接

复杂任务使用 [handoff-v2.md](handoff-v2.md)。旧版 [handoff-template.md](handoff-template.md) 仅兼容短交接。

## 知识沉淀

可复用运营规律写入 `knowledge/agent-ops/`。

## 禁止偷懒

- 禁止只改 README 不写路由表与 handoff-v2
- 禁止新增角色无「不做」边界
- 禁止 Verifier 无证据槽位就报完成
- 禁止 Game/Asset 写成空喊流水线而无输入输出契约
- 禁止与 Cursor Task 类型重名却职责冲突
- 禁止把 `.cursor/agents` 再做成全文复制（必须薄适配 + 指针）
