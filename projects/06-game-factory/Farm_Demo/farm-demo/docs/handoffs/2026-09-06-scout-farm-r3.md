# Scout — Farm_Demo R3

**handoff_id:** 2026-09-06-scout-farm-r3  
**from:** Scout → Game/Builder

## Findings

| 项 | 现状 |
|----|------|
| MCP | Connected `Farm_Demo/farm-demo` |
| 地图 | `farm_field.gd` W=56 H=40 |
| 房屋 | `world.gd` 仅 Sprite，无进屋 |
| 方向 | player 四向 atlas 288×192；idle_up 已 MCP 验证 |
| 相机 | zoom=(2,2) 已是整数 |
| 粉边抽样 | player/tree/house/chicken/npc/gw 热粉=0 |
| 过渡砖 | 存在；gd_n 有 1 红像素；截图曾见河岸竖线伪影 |

## Risks
- 过渡砖映射错误会加重「乱」
- 进屋换场景需处理 MCP runtime 重连

## Next
Game 规格 → Asset 室内素材 → Builder 扩图+进屋
