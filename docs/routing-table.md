# 路由表 — Agent Team v2 × Cursor Task

**原则（T3=A）：** 本仓库角色 = 语义职责；Cursor Task `subagent_type` = 执行载体。先定语义角色，再选载体。

## 任务类型 → 语义角色

| 用户意图信号 | 首选角色 | 常用后续 |
|--------------|----------|----------|
| 「在哪」「结构怎样」「找文件」 | Scout | Builder / Planner |
| 「查资料」「为什么」「对比方案」 | Researcher | Planner / Critic |
| 「做个方案」「拆任务」「grill」 | Planner | Conductor |
| 「实现」「改代码」「搭场景」 | Builder | Verifier |
| 「生图」「抠图」「导入素材」 | Asset | Builder / Verifier |
| 「游戏设计」「关卡/流水线」 | Game | Asset / Builder |
| 「跑一下」「截图验」「有没有挂」 | Verifier | Critic |
| 「审查」「有没有偷懒」「安全吗」 | Critic | Builder（返工） |
| 「写成小红书/内容」 | Content | Critic |
| 「PLC/Modbus/工控」 | Industrial | Researcher / Builder |
| 「教我」「对照实验」 | Teacher / Experiment | Memory |
| 「记下来」「规律」 | Memory | — |
| 「复盘」 | Reflection | Memory / Conductor |
| 多步 / 跨项目 / 含验收 | Conductor | 按 Playbook |

## 语义角色 → Cursor Task 载体

| 语义角色 | 推荐 `subagent_type` | 备注 |
|----------|----------------------|------|
| Scout | `explore` | thoroughness 按范围选 |
| Builder（纯命令） | `shell` | git/测试/脚本 |
| Critic（缺陷向） | `bugbot` 或外部 code-review skill | 用户显式要求时 |
| Critic（安全向） | `security-review` | 用户显式要求时 |
| Conductor / 综合 | `generalPurpose` | 或主对话亲自编排 |
| Verifier（Godot） | 主对话 + MCP；必要时 `generalPurpose` | 截图/runtime |
| Asset / Game / Content | 主对话或 `generalPurpose` | 需 MCP/生图时留在能用工具的会话 |

## Playbook 快选

| 场景 | Playbook |
|------|----------|
| Godot 画面/分层/移动探针 | PB-Game-Visual |
| Oakhaven 世界驱动地图（防拼接割裂） | PB-Oakhaven-World |
| 内容工厂图文 | PB-Content |
| 工控/PLC | PB-Industrial |
| 学习新技术 | PB-Learn |
| 改 prompts/rules/团队本身 | PB-OS-Change |

## 反模式

- 主对话声称「我是全部 Agent」却不写 handoff、不出证据
- 用 `explore` 代替 Researcher 做外网事实（explore 偏代码库）
- Verifier 与 Critic 互相替代：无证据的「我觉得没问题」不算 Verifier
- 为炫技并行 5 个无关 Agent（违反 Core：最小可靠方案）
