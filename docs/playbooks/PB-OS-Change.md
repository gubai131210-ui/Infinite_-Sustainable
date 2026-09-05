# PB-OS-Change

**用途：** 修改本仓库 prompts / rules / agents / 团队协议。  
**证据强度：** 文档级（diff + Critic）

## 链

```text
Conductor → Planner → Builder → Critic → Memory?
```

## 验收（默认）

- [ ] `prompts/` 完整版与 `.cursor/agents` 薄适配一致（指针有效）
- [ ] 路由表 / Playbook / handoff 若受影响则已更新
- [ ] 无伪造「已实现」的 Skill 逻辑

## 禁止偷懒

- 禁止只改一处索引不改角色正文
- 禁止 `.cursor/agents` 再次全文复制 prompts
- 禁止新增角色无「不做」边界
