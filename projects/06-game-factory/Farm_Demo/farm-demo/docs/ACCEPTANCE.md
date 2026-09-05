# ACCEPTANCE — Farm_Demo

| 项 | 结果 | 证据 |
|----|------|------|
| 主场景可运行 | PASS | get_errors=0，runtime `/root/Main` |
| 俯视移动 | PASS | pos 416→1034（后加边界钳制） |
| 地图五区 | PASS | `assets/qa/screenshot_farm_demo.png` 河/草/田/屋/树 |
| 种地环 | PASS | MCP `hoe→plant→water×2→harvest=radish` |
| 背包 | PASS | Tab 开关（打开时仍可再按 Tab 关闭） |
| 5 NPC | PASS | world 生成 5 居民不同配色 |
| 对话关闭 | PASS | 打开同帧忽略关闭，避免立刻重开 |
| 动物喂食 | PASS | 鸡×3 牛×1 羊×2 + feed |
| 钓鱼 | PASS | 河边 InteractZone mode=fish |
| 抠图 QA | PASS | `assets/qa/checker_*`（品红键，保留绿色） |
| 无昼夜/存档/经济 | PASS | 未实现 |

## 禁止偷懒核对

- [x] 非 ColorRect 冒充美术
- [x] 棋盘格 QA
- [x] Player/World/HUD/Inventory/Dialogue 分离
- [x] 种地环完整
- [x] MCP 截图 + runtime
- [x] 无假昼夜/存档/商店
- [x] NPC 五套配色
- [x] 背包与对话独立层
