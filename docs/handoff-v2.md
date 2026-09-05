# TASK HANDOFF v2

Agent 之间禁止扔无结构自然语言。本模板是默认交接协议。

短任务仍可用 [handoff-template.md](handoff-template.md)；凡跨 2 个以上 Agent、或需要验收证据的，必须用 v2。

```markdown
## TASK HANDOFF v2

### Meta
- handoff_id: <yyyy-mm-dd-slug>
- playbook: <PB-* | none>
- from_agent: <role>
- to_agent: <role>
- parallel_group: <optional id | none>

### Objective
要完成什么（一句话 + 可检查完成态）

### Context
背景、用户约束、已锁定决策（Grill 结果摘要）

### Inputs
- paths: []
- prior_handoff_ids: []
- tools_allowed: [code | mcp | image | publish | shell]

### Completed
已经做了什么（条目化）

### Evidence
| 类型 | 路径或摘要 | 结果 |
|------|------------|------|
| screenshot / log / test / diff / runtime | … | pass/fail/n/a |

（无证据时写 `Evidence: none — reason: …`，接收方默认视为未完成。）

### Acceptance
- [ ] 验收项 1
- [ ] 验收项 2

### Open Questions
还缺什么（阻塞项标 BLOCKER）

### Risks
风险与缓解

### Suggested Next Agent
下一角色 + 为何

### Required Output
下一 Agent 必须产出的工件（文件路径或结构化块）

### Do-Not
本任务禁止偷懒清单（至少 3 条）

### Related Files
路径列表
```

## 规则

1. **Evidence 空 = 未完成**（除非 Playbook 规定文档类可仅用 diff）。
2. Conductor 汇总时只向用户报告：结论 / 关键证据 / 风险 / 下一步。
3. 并行扇出时填写同一 `parallel_group`；汇合前 Conductor 检查冲突。
4. Memory 只接收「规律」类 handoff，不接收流水账。
