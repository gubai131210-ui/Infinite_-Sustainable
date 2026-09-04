# 提示词库索引（Prompt Hierarchy）

来源：[ChatGPT 半月成长对话](https://chatgpt.com/share/6a9a1272-a0d0-83ea-9d45-8c0d44a73194)

本目录是**完整版**提示词。Cursor 可执行精简版见 `.cursor/rules/` 与 `.cursor/agents/`。

## 层次结构

| 层级 | 目录 | 角色 |
|------|------|------|
| L0 母规则 | [00-core](00-core/) | Agent Core Operating Rules |
| L1 总管 | [01-orchestration](01-orchestration/) | Orchestrator |
| L2 执行链 | [02-execution](02-execution/) | Researcher / Planner / Coder / Reviewer |
| L3 知识循环 | [03-knowledge](03-knowledge/) | Teacher / Memory / Reflection |
| L4 领域 | [04-domain](04-domain/) | Content / Industrial / Experiment |
| 协议 | [../docs/handoff-template.md](../docs/handoff-template.md) | TASK HANDOFF |

## 调用关系

```text
                  ┌───────────────────┐
                  │   ORCHESTRATOR    │
                  └─────────┬─────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
 RESEARCHER              PLANNER              TEACHER
       │                    │                    │
       └──────────────┬─────┴────────────┬───────┘
                      ▼                  ▼
                    CODER            INDUSTRIAL
                      │                  │
                      └────────┬─────────┘
                               ▼
                           REVIEWER
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
             CONTENT       EXPERIMENT       MEMORY
                 │             │             │
                 └─────────────┴─────────────┘
                               ▼
                         REFLECTION
```

所有角色默认遵守：[00-core/agent-core-operating-rules.md](00-core/agent-core-operating-rules.md)

## 典型工作流

### 工业 / PLC

Orchestrator → Industrial → Researcher → Coder → Reviewer → Memory

### 自媒体内容

Orchestrator → Researcher → Content → (image-generation skill) → Reviewer

### 学习新技术

Teacher → Experiment → Coder → Reviewer → Memory

### 日复盘

Reflection → Memory（如有长期规律）→ Orchestrator（如需调整计划）

## 文件清单

- [00-core/agent-core-operating-rules.md](00-core/agent-core-operating-rules.md)
- [01-orchestration/orchestrator.md](01-orchestration/orchestrator.md)
- [02-execution/researcher.md](02-execution/researcher.md)
- [02-execution/planner.md](02-execution/planner.md)
- [02-execution/coder.md](02-execution/coder.md)
- [02-execution/reviewer.md](02-execution/reviewer.md)
- [03-knowledge/teacher.md](03-knowledge/teacher.md)
- [03-knowledge/memory.md](03-knowledge/memory.md)
- [03-knowledge/reflection.md](03-knowledge/reflection.md)
- [04-domain/content.md](04-domain/content.md)
- [04-domain/industrial.md](04-domain/industrial.md)
- [04-domain/experiment.md](04-domain/experiment.md)
