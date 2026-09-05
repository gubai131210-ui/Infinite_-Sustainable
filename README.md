# Infinite Sustainable — Personal AI OS

15 天 Cursor 无限 Token 旗舰仓库：把你训练成「会设计 AI 工作流的人」，并留下可迁移的 Rules / Skills / Agents / 知识库 / 项目骨架。

来源计划：[ChatGPT 对话](https://chatgpt.com/share/6a9a1272-a0d0-83ea-9d45-8c0d44a73194)  
远程：[gubai131210-ui/Infinite_-Sustainable](https://github.com/gubai131210-ui/Infinite_-Sustainable.git)

## 当前状态

**骨架已就绪，业务项目均未开工。** 你指定从哪个 `projects/0X-*` 开始后，Agent 会先问三问再执行。

## 仓库地图

```text
prompts/          完整提示词库（分层 L0–L4）
.cursor/          Cursor Rules / Agents / Skills 占位
knowledge/        主题知识库
memories/         偏好 / 教训 / 决策
docs/             概览、15天计划、交接模板
automation/       自动化占位
projects/
  01-agent-lab           优先级1
  02-personal-ai-os      优先级2
  03-content-factory     优先级3
  04-public-product      优先级4
  05-industrial-copilot  占位
  06-game-factory        占位
  07-social-agent        占位
```

## 提示词层次

见 [prompts/README.md](prompts/README.md) 与 **[docs/agent-team-v2.md](docs/agent-team-v2.md)**。

| 层 | 内容 |
|----|------|
| L0 | Core Operating Rules |
| L1 | Conductor（原 Orchestrator） |
| L2 | Scout / Researcher / Planner / Builder / Verifier / Critic |
| L3 | Teacher / Memory / Reflection |
| L4 | Content / Industrial / Experiment / Game / Asset |

## 文档

- [docs/00-overview.md](docs/00-overview.md) — 价值层级与四大系统
- [docs/15-day-bootcamp.md](docs/15-day-bootcamp.md) — Day1–15 检查清单
- [docs/agent-team-v2.md](docs/agent-team-v2.md) — 多 Agent 团队 v2
- [docs/routing-table.md](docs/routing-table.md) — 路由 × Cursor Task
- [docs/playbooks/](docs/playbooks/) — Playbook（Game / Content / Industrial / Learn / OS）
- [docs/handoff-v2.md](docs/handoff-v2.md) — 交接协议 v2
- [docs/handoff-template.md](docs/handoff-template.md) — 短交接（兼容）

## 如何开工

1. 告诉 Agent：从 `projects/01-agent-lab`（或其它）开工；复杂任务走 Conductor + Playbook
2. 回答三问：深度 / 已有资产 / 是否允许代码·MCP·生图·发布
3. 本地自行打开目录检查（中文路径，避免危险批量命令）

## 禁止偷懒（仓库级）

- 禁止未确认就写业务实现
- 禁止把多个 Agent 糊成单文件；`.cursor/agents` 必须薄适配
- 禁止 Skills 假实现
- 禁止改完不推 GitHub、不复查
- 禁止无 Verifier 证据就宣称游戏/运行时「完成」
