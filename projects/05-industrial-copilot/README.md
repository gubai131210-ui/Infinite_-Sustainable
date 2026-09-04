# 05 — Industrial Engineering AI Copilot

**状态：未开工**  
**优先级：占位（行业长期资产）**

## 目标

把 PLC / Modbus TCP / C# / 三次元 / Keyence / 测量算法 / Hair Pin 等经验变成可复用的工业工程 Copilot：分层排查、测量数据分析、故障报告。

## 关联

- Agent: `prompts/04-domain/industrial.md`
- Skill 占位: `.cursor/skills/modbus-tcp-troubleshooting/`
- Knowledge: `knowledge/industrial/`

## 开工前必问

1. 这次要做到什么深度？（骨架 / MVP / 可发布）
2. 是否对接已有资产？（真实 CSV、PLC 日志、测量程序等）
3. 是否允许写真实代码 / 接 MCP / 生图 / 发内容？是否允许接触产线敏感数据？

## 禁止偷懒

- 禁止只给理论不给排查顺序与验证
- 禁止混淆 Measurement / Calculation / Specification
- 禁止未隔离对比就下根因结论
