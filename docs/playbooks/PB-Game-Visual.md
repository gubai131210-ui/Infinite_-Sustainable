# PB-Game-Visual

**用途：** 2D 画面能力验证（分层、嵌入、移动）；不实现玩法。  
**证据强度：** 高（截图 + runtime）

## 链

```text
Conductor → Scout(MCP/工程) → Game(场景规格)
         → Asset(生图/抠图/棋盘格) → Builder(场景/脚本)
         → Verifier(run/screenshot/position) → Critic → Memory?
```

## 输入

- Godot 工程根路径
- Grill 锁定规格（题材、视口、资产清单）
- tools_allowed 含 code + mcp + image

## 验收（默认）

- [ ] 主场景可运行，无致命错误
- [ ] ≥3 层视差或明确 z 分层，角色可被前景遮挡
- [ ] Player 为独立场景 instance
- [ ] 左右移动 + 重力/地面；runtime position 变化有证据
- [ ] HUD 或等价物证明 UI 层与世界层分离（若规格要求）
- [ ] 抠图素材通过棋盘格检查后再导入

## 禁止偷懒

- 禁止无截图宣称画面 OK
- 禁止 Player/World/HUD 堆成无结构单场景
- 禁止跳过 Asset 棋盘格验收
- 禁止用纯 ColorRect 冒充写实分层（规格要求写实时）
- 禁止未启用 MCP 时假装完成 Verifier 截图项（应降级为用户本机证据）
