# prompts/ — 提示词库索引（Agent Team v2）

完整版提示词在此；Cursor 薄适配见 `.cursor/agents/`（禁止再全文复制）。

团队总览：[docs/agent-team-v2.md](../docs/agent-team-v2.md)  
路由：[docs/routing-table.md](../docs/routing-table.md)  
交接：[docs/handoff-v2.md](../docs/handoff-v2.md)

## 层次结构

| 层级 | 目录 | 角色 |
|------|------|------|
| L0 | [00-core](00-core/) | Core Operating Rules |
| L1 | [01-orchestration](01-orchestration/) | **Conductor**（orchestrator 为别名） |
| L2 | [02-execution](02-execution/) | Scout / Researcher / Planner / **Builder** / **Verifier** / **Critic** |
| L3 | [03-knowledge](03-knowledge/) | Teacher / Memory / Reflection |
| L4 | [04-domain](04-domain/) | Content / Industrial / Experiment / **Game** / **Asset** |

## 调用关系（v2）

```text
                         CONDUCTOR
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
        SCOUT           RESEARCHER           PLANNER
          │                  │                  │
          └────────────┬─────┴────────┬─────────┘
                       ▼              ▼
                    BUILDER  (+ GAME / ASSET / CONTENT / INDUSTRIAL)
                       │
                       ▼
                   VERIFIER ──证据──▶ CRITIC
                       │
                       ▼
                    MEMORY / REFLECTION / TEACHER
```

## 典型 Playbook

| 场景 | Playbook |
|------|----------|
| Godot 画面探针 | [PB-Game-Visual](../docs/playbooks/PB-Game-Visual.md) |
| 内容工厂 | [PB-Content](../docs/playbooks/PB-Content.md) |
| 工控 | [PB-Industrial](../docs/playbooks/PB-Industrial.md) |
| 学习 | [PB-Learn](../docs/playbooks/PB-Learn.md) |
| 改 OS/提示词 | [PB-OS-Change](../docs/playbooks/PB-OS-Change.md) |

## 兼容别名

| 旧名 | 新名 |
|------|------|
| Orchestrator | Conductor |
| Coder | Builder |
| Reviewer | Critic + Verifier |

所有角色遵守：[00-core/agent-core-operating-rules.md](00-core/agent-core-operating-rules.md)
