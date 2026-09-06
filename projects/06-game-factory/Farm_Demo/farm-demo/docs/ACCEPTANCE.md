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
| 抠图 QA | PASS | `assets/qa/checker_*`；玫红+品红双键 |
| AI 像素替换 | PASS | `tools/import_ai_sprites.py` + `screenshot_ai_art.png` |
| 动物相对缩放 | PASS | 鸡20 / 羊28 / 牛36 / 人48 单元格 |
| 四向走路 | PASS | `idle_right` runtime；player atlas 288×192 |
| NPC 真走路条 | PASS | 5 条 6 帧 side walk + flip_h |
| 过渡地砖 | PASS | gw/gd 边角接入 `_display_tex` |
| Round2 截图 | PASS | `assets/qa/screenshot_round2.png` |
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
