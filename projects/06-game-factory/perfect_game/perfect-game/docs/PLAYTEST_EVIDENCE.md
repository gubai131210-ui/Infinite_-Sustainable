# Oakhaven 试玩 / 导出证据

> 竖切证据 ≠ Goal complete。本文件只记录当前可核验事实。  
> **关闭 Goal 硬门槛：** 下方「用户签字」表全部勾选 + itch 页面 URL。

## 导出产物（本机）

| 项 | 值 |
|----|----|
| 路径 | `build/Oakhaven.exe` |
| 大小 | ≈ **103.8 MB** |
| 时间戳 | 2026-09-07 |
| 引擎 | Godot **4.6.1 mono** |

用户需在中文路径本机 **双击 exe 或编辑器 F5** 做最终冒烟（Agent 不代替该步宣称“可玩可发布”）。

## MCP 冒烟（Agent · 2026-09-07）

| 步骤 | 结果 |
|------|------|
| `run_scene` | 0 script error |
| 杂货店进门 → 买种子礼包 | 金 **120→90**；`seed_radish` count≥3；截图 `smoke/11_shop_interior.png` |
| 咖啡馆进门 → 热可可 | 金 **90→80**；截图 `smoke/12_cafe_interior.png` |
| 面包房进门 → 南瓜派 | 金 **80→65**；标题「橡木面包房」；截图 `smoke/13_bakery_interior.png` |
| 瀑布构图 | 截图 `smoke/14_waterfall.png` |
| 镇店招 | 截图 `smoke/15_storefronts.png` |
| Golden 全套 | `GOLDEN_CAPTURE_DONE`（含 `07` zoom 1.55） |
| 农庄锄→种→浇→睡→熟→收 | cell(16,78) radish **stage 0→3** · harvest=`radish` · `smoke/16_farm_growth.png` |
| Tween 修复 | crop/tree sway 绑定节点，避免 sleep 刷新时 infinite loop |
| 走路帧 | `walk_down` frame **5** · `smoke/17_walk_anim.png` |
| 锄地帧（freeze） | `hoe_down` frame **2** · `smoke/18_hoe_anim.png` |
| 浇水帧（freeze） | `water_down` frame **2** · `smoke/19_water_anim.png` |
| 畜栏 | 鸡/牛/羊 spawn + `pen_min`/`pen_max` clamp 南围栏内 |
| Golden 重抓 | P126 `GOLDEN_CAPTURE_DONE`（含 blob fringe） |
| 院子 blob / 门廊 | P127–P129：农舍 apron blob + bridge 木台 + 碎屑；区标默认隐藏；golden 再抓 |
| Overview 对齐 | P130–P132：畜栏泥土 + 湖南田 + 路径 soften；farm/lake 相机重取景 |
| 立面 + y-sort | P133–P135：barn/silo 重绘；Player→Entities；树/NPC 同层排序 |
| 镇店招 | P139–P141：店招加深 + 广场密度 |
| Overview 密度 | P142–P144：软草 + 加密；取景含四区标 |
| 树冠 + NPC | P145–P147：meadow canopy 条带；NPC 脚影/步幅；smoke/20_npc_life |

> Agent MCP 冒烟 **不能替代** 用户签字。中文路径本机手感 / 输入 / 音频需你确认。

## Golden

`assets/qa/golden/`：`00_overview` … `10_shop_door`  
对照：`docs/ref/oakhaven_overview.jpg`

## itch

- 文案：[`ITCH_PAGE_DRAFT_CN.md`](ITCH_PAGE_DRAFT_CN.md)
- 导出：[`EXPORT_AND_PLAYTEST.md`](EXPORT_AND_PLAYTEST.md)
- **尚未**完成：正式 itch 上传 URL（待用户发布）

## 用户签字试玩清单（请本机勾选后回贴）

请 F5 或运行 `build/Oakhaven.exe`，逐项勾选：

- [ ] 农庄：锄地 → 播种 → 浇水 → 床睡觉 → 作物有生长
- [ ] **走路腿会交替摆动**（非原地滑行）；锄/浇/播有专用挥动帧
- [ ] 镇中心：看见 **GENERAL STORE / OAKHAVEN CAFE / BAKERY** 招牌
- [ ] 杂货店：E 进门 → 买种子礼包 / 卖作物 → E 离开
- [ ] 咖啡馆：E 进门 → 花 10 金点可可 → 精力增加
- [ ] 面包房：E 进门 → 花 15 金买派 → 离开
- [ ] 瀑布：走到西北瀑布，能看到崖壁落水 + 听瀑交互
- [ ] 灯塔 / 火车站：可接近并进入内景
- [ ] NPC（林婶/豆豆）在店面附近走动，可对话
- [ ] 雨天或过夜后存档仍在（金币/地块）
- [ ] 无崩溃、无黑屏、无进店卡死

签字：________　　日期：________　　itch URL（可选）：________

## 仍缺（Goal 关闭前）

1. 上表用户签字  
2. itch 页面实际上线证据  
3. Critic「商店页主图」仍为否（视觉可继续打磨，但不替代签字）
