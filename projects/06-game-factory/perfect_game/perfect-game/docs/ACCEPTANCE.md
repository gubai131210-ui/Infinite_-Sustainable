# ACCEPTANCE — Oakhaven

| 项 | 结果 | 证据 |
|----|------|------|
| Paper Isle 已清除 | PASS | 无 fox/star/GameState 玩法 |
| 参考图入库 | PASS | `docs/ref/oakhaven_overview.jpg` |
| TileMap 192×128 六区 | PASS | `world.gd` ZONES + paint |
| 中文木牌 | PASS | decor 米勒农庄/橡木河/火车站/回声湖 |
| 种地环 | PASS | `farm_plots.gd` + Player 工具 |
| ≥6 进出建筑 | PASS | GameBus.INTERIORS 六键 |
| ≥12 NPC 对话 | PASS | decor roster npc_01..12 |
| 动物交互 | PASS | dialogue zones |
| golden 六区截图 | 待跑 | `--capture_golden` / 本机 F5 |
| Critic | 待跑 | 子 agent |
| Windows 导出说明 | PASS | `docs/PLAYTEST.md` |

## 禁止偷懒核对

- [x] 非单张背景世界
- [x] Player/World/HUD/Inventory/Dialogue 分场景
- [x] 未复用纸片资产作主视觉
- [ ] golden 对照参考图（用户/CLI 补）
