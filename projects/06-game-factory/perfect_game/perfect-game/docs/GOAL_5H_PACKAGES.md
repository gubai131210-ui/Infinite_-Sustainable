# 5 小时+ 可执行工作包 — Oakhaven 接近完整星露谷

> **用途：** `/goal` 长跑会话的燃料。Agent **不得**因「已有竖切」提前 `UpdateGoal complete`。  
> **锁定：** `LOCKED_DECISIONS.md`（长期对齐 · 全做 · CC0 允许 · 轻松日常 · 蓝衣少年）  
> **估时：** 每包约 25–40 分钟（含 Scout→Build→Verifier→Critic）；合计 **≥5 小时**。可跨多日多会话。

## 规则

1. 一次只开 **1 个**工作包（或同 Wave 内 2 个强相关包）。  
2. 每包结束必须：代码/素材 diff + Godot 冒烟证据 + Critic 一句 + 勾选本表。  
3. 包未完成不得跳到发布包装。  
4. 有 BLOCKER 先问用户。  
5. **禁止偷懒：** 只改文档勾选、无 runtime、无风格 QA、堆 UI 单页、浮点货币。

---

## Pack 清单（按序）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P01 | 30m | 日夜 TimeClock + CanvasModulate + HUD 时钟 | F5 见昼夜变色与时钟走动 |
| P02 | 30m | 作物湿土/摇摆/隔日生长 + 水体闪烁 | 浇水变湿、过夜长一阶、水层动 |
| P03 | 30m | 整数金币 + 卖出/买种子 + 存档 user:// | 进出建筑后金币/地块仍在 |
| P04 | 35m | 主线轻松日常任务线（≥7 步）+ 区域触发 | HUD 提示随进度变 |
| P05 | 40m | CC0 图集下载管线 + attribution + 湿土/作物补图 remap | `assets/cc0/` + ASSET_ATTRIBUTION |
| P06 | 40m | 12 NPC 轻松日常人设卡 + 昼夜台词差 | `content/characters/*.md` + 代码读表 |
| P07 | 40m | NPC 简易日程（早农庄/午镇/晚回家） | 不同时段位置变化截图 |
| P08 | 35m | 精力系统 + 工具耗能 + 睡觉恢复 | 耗尽提示；睡回满 |
| P09 | 40m | 钓鱼小玩法 + 斧砍木 + 动物产出（蛋/毛） | 各至少一次成功反馈 |
| P10 | 40m | 室内差异化（店柜/咖啡馆桌/站厅椅）新场景页 | 6 室内观感不同 |
| P11 | 40m | 动画素材升档： cropl 4 阶更清晰、水瓦动画帧 | Visual Bible QA |
| P12 | 35m | 音效占位（脚步/浇水/开箱/卖出） | 有 AudioStreamPlayer 触发 |
| P13 | 40m | 第二任务线（轻松节日/集市） | 独立 Quest id |
| P14 | 40m | 六区 golden 截图 + Critic 对照 overview | `docs/golden/` |
| P15 | 40m | Windows 导出 + itch 中文说明草稿 | export 步骤可跟做 |
| P16 | 40m | 友谊度/礼物（轻松）最小环 | 送礼改台词 |
| P17 | 40m | 季节一种视觉差（叶色/作物表） | 季节切换可见 |
| P18 | 40m | 平衡与存档版本号 + 回归清单 | SAVE version + PLAYTEST |

**合计估时：** ≈ 11 小时上限；**最低可跑满 5 小时** 的核心路径 = **P01–P08**（≈4.5–5.5h），之后继续 P09+ 直至「接近完整星露谷」。

---

## 本会话进度

- [x] P01（日夜+HUD）  
- [x] P02（作物/水）  
- [x] P03（金币存档）  
- [x] P04（任务打卡初版）  
- [x] P05（CC0 下载 + wet soil / crop remap + catalog）  
- [x] P06（12 NPC 人设 md + characters.json 昼夜台词）  
- [x] P07（NPC 简易日程随 period 换锚点）  
- [x] P08（精力 Stamina + 工具耗能 + 床回满）  
- [x] P09（钓鱼概率玩法 + 斧砍农庄边树得木 + 喂养收蛋/毛/奶）  
- [x] P10（六室内独立场景页 + 家具/调色差异 + 咖啡馆回精力）  
- [x] P11（作物 4 阶重绘更清晰 + 水体棋盘帧动画）  
- [x] P12（脚步/浇水/开箱/卖出/锄地 WAV 占位）  
- [x] P13（集市日第二任务线 MARKET ids）  
- [x] P14（golden 已捕获：`assets/qa/golden/` 六区+overview）  
- [x] P15（export_presets + ITCH_PAGE_DRAFT_CN + EXPORT_AND_PLAYTEST）  
- [x] P16（Friendship 送礼改台词）  
- [x] P17（SeasonClock 春夏秋冬色调 / HUD 季节）  
- [x] P18（save_version 3 + 回归清单）  

## 续跑 Pack（≥4h 完善，竖切仍 ≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P19 | 30m | D 盘导出模板 + Windows exe 冒烟 | `build/Oakhaven.exe` |
| P20 | 40m | 水体重绘 + 中地图填充 + 北缘可读 | golden 河/overview |
| P21 | 40m | 天气（雨）+ 雨天过夜作物加成 | HUD 天气；雨天生长 |
| P22 | 40m | 厨房烹饪最小环（菜谱→料理） | 农舍灶台交互 |
| P23 | 35m | 广场告示板 + 轻松故事邮件 | 告示/邮件文本 |
| P24 | 35m | 环境音乐循环 + 雨声 SFX | 可听到 BGM |
| P25 | 40m | 重抓 golden + Critic + 推送 | qa/golden 更新 |

### 续跑进度
- [x] P19（D 盘模板 junction + `build/Oakhaven.exe` ≈103.8MB）  
- [x] P20（水体波浪重绘 tileset + 中地图灌木/花带走廊）  
- [x] P21（Weather 雨/晴 + 雨粒子 + 过夜湿土/加成生长）  
- [x] P22（Cooking 四菜谱 + 农舍灶台/餐桌）  
- [x] P23（镇告示栏 bulletin + 农舍旁信箱 mail）  
- [x] P24（AmbientMusic BGM + rain_loop + ui/rain SFX）  
- [x] P25（重抓 golden + Critic + push）  

## 视觉密度续跑（Critic 缺口 · ≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P26 | 35m | 北缘双脊山 + 多层瀑布 | golden overview/river |
| P27 | 35m | 遗迹拱廊加密嵌林 | overview 北中可读 |
| P28 | 35m | 路径花田带 + 屋顶色调差 | town/farm 走廊 |
| P29 | 30m | 瀑布雾柱增强 + 脚步扬尘 | runtime FX |
| P30 | 35m | golden + Critic + push | qa/golden |

### 密度进度
- [x] P26（北缘双脊山 + 崖壁嵌瀑布）  
- [x] P27（遗迹拱廊加密）  
- [x] P28（路径花田带 + 屋顶 tint）  
- [x] P29（瀑布雾柱 + 脚步扬尘）  
- [x] P30（golden + Critic + push）  

## 嵌林与故事续跑（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P31 | 35m | 瀑布林冠+崖嵌套（去悬浮感） | golden river |
| P32 | 35m | 遗迹穿树不规则布局 | overview 北中 |
| P33 | 35m | 中空草地填充 + 烟囱剪影 | overview/town |
| P34 | 30m | 信箱/告示随进度 + 遗迹旧箱故事 | 交互文本 |
| P35 | 30m | golden + Critic + push | qa/golden |

### 嵌林进度
- [x] P31（瀑布林冠+崖嵌套）  
- [x] P32（遗迹穿树不规则）  
- [x] P33（中空填充 + 烟囱剪影）  
- [x] P34（信箱/告示进度文 + 遗迹旧箱）  
- [x] P35（golden + Critic + push）  

## 店面视觉续跑（瀑布气势 / 蜿蜒路 / 屋顶 · ≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P36 | 35m | 宽崖瀑布素材重绘 + 推送 | golden river |
| P37 | 30m | 更强蜿蜒土路联网 | overview 路径可读 |
| P38 | 35m | 红/石板/茅草屋顶变体 | town/farm golden |
| P39 | 30m | 全套 golden 重抓 + Critic | qa/golden |
| P40 | 25m | smoke + push + review | 0 error |

### 店面进度
- [x] P36（宽崖瀑布重绘）  
- [x] P37（更强蜿蜒土路）  
- [x] P38（屋顶变体 shop/cafe/townhouse/farm）  
- [x] P39（全套 golden + Critic）  
- [x] P40（smoke + push + review）  

## 北缘与真屋顶续跑（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P41 | 35m | 打破松树墙：天空云+山脊缺口 | overview 北缘 |
| P42 | 40m | 手绘屋顶立面（非重上色） | town golden |
| P43 | 25m | 天空带 + 瀑布走廊留白 | river/overview |
| P44 | 25m | 对话显示友谊心进度 | NPC 对话 |
| P45 | 30m | golden + Critic + push | qa/golden |

### 北缘进度
- [x] P41 · P42 · P43 · P44 · P45  

## 天际线可读续跑（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P46 | 40m | 高对比天空+云；相机允许负Y | overview 北缘见天 |
| P47 | 35m | 双层瀑布 + `07_waterfall` golden | qa/golden |
| P48 | 35m | 更密屋顶立面/遮阳棚 | town golden |
| P49 | 25m | 对话心形行 UI | `08_dialogue` |
| P50 | 30m | day-lock + Critic + push | origin/main |

### 天际线进度
- [x] P46 · P47 · P48 · P49 · P50  

## 云松瀑与试玩证据（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P51 | 40m | 打碎平齐山脊；云→松→瀑层次 | overview |
| P52 | 35m | hero 店面立面 + `08_dialogue` 接入捕获 | town/dialogue |
| P53 | 25m | 瀑布打卡→信箱故事拍 | visit_waterfall |
| P54 | 25m | PLAYTEST_EVIDENCE + itch 更新 | docs |
| P55 | 30m | golden + Critic + push | origin/main |

### 云松瀑进度
- [x] P51 · P52 · P53 · P54 · P55  

## 有机北缘与主线瀑布（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P56 | 40m | 岩石有机脊带，去全宽山墙 | overview |
| P57 | 30m | 土路多频摆动+羽化 | farm/overview |
| P58 | 20m | MAIN 含水瀑→灯塔 | QuestLog |
| P59 | 15m | NPC flip_h | 行走 |
| P60 | 30m | golden + Critic + push | origin/main |

### 有机北缘进度
- [x] P56 · P57 · P58 · P59 · P60  

## 连续天际线与缀边（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P61 | 35m | 连续岩石脊+高天空 | overview |
| P62 | 25m | 路径羽化+草丛缀边 | farm |
| P63 | 30m | 更深店面立面 | town |
| P64 | 25m | golden + Critic + push | origin/main |

### 连续天际线进度
- [x] P61 · P62 · P63 · P64  

## 参考图层次对齐（云→峰→丘 · ≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P65 | 40m | 脊带改天空/蓝峰/绿丘；可见于 overview | golden 00 |
| P66 | 35m | 更深店面（石基/木板/花箱） | town golden |
| P67 | 25m | 路径 pebble+tuft+fringe dither | farm/overview |
| P68 | 30m | 晴天锁定 golden + Critic + push | origin/main |

### 参考图层次进度
- [x] P65 · P66 · P67 · P68  

## 无缝天际线与镇区剪影（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P69 | 40m | 全宽无缝 skyline 单精灵 | overview 无竖缝 |
| P70 | 25m | 瀑布碗口嵌入天际线 | waterfall golden |
| P71 | 30m | 镇区 hero 店面/面包房 | town/overview |
| P72 | 25m | golden + Critic + push | origin/main |

### 无缝天际线进度
- [x] P69 · P70 · P71 · P72  

## 天空加高与可读店招（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P73 | 35m | 更高天空+软碗口 | overview |
| P74 | 30m | 有机崖/瀑减砖感 | waterfall |
| P75 | 25m | SHOP/CAFE/BAKERY 招牌 | town/overview |
| P76 | 25m | 广场毛边 dither | town |
| P77 | 25m | golden + Critic + push | origin/main |

### 天空加高进度
- [x] P73 · P74 · P75 · P76 · P77  

## 山谷林缘围合（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P78 | 40m | 东西南+北麓林缘围合 | overview |
| P79 | 30m | 瀑头不规则 amphitheater | waterfall |
| P80 | 25m | 天空条 240px + 更广 overview | 00_overview |
| P81 | 20m | 广场缀边加密 | town |
| P82 | 25m | golden + Critic + push | origin/main |

### 山谷林缘进度
- [x] P78 · P79 · P80 · P81 · P82  

## 密冠与瀑地貌（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P83 | 35m | 北麓连续密松冠 | overview |
| P84 | 30m | 一体瀑碗 landform | waterfall |
| P85 | 25m | 中空草地补林 | overview |
| P86 | 30m | 远峰加深 + golden/Critic/push | origin/main |

### 密冠瀑地貌进度
- [x] P83 · P84 · P85 · P86  

## 松海与瀑嵌入（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P87 | 40m | 重叠放大北松海 | overview |
| P88 | 35m | 重绘大瀑碗 landform | waterfall |
| P89 | 25m | 池口接河 + 草地杂色 | river/overview |
| P90 | 25m | golden + Critic + push | origin/main |

### 松海瀑嵌入进度
- [x] P87 · P88 · P89 · P90  

## 松冠批处理与河岸（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P91 | 35m | 全宽松冠条替换 2.7k sprites | 启动/overview |
| P92 | 20m | pine_b/c 变体点缀 | N accents |
| P93 | 25m | 池口软岸 + golden | waterfall |
| P94 | 20m | Critic + push | origin/main |

### 松冠批处理进度
- [x] P91 · P92 · P93 · P94  

## 团块林冠与店面放大（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P95 | 35m | 团块层次松冠 | overview |
| P96 | 30m | 加深瀑碗 + 可读 pine_b/c | waterfall |
| P97 | 30m | 店面放大招牌 + 全河软岸 | town/river |
| P98 | 25m | golden + Critic + push | origin/main |

### 团块林冠进度
- [x] P95 · P96 · P97 · P98  

## 店招构图与广场软边（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P99 | 35m | 店招 bitmap + 摊位下移 + 09_storefronts | town/storefronts |
| P100 | 30m | 广场软椭圆 + 路径肩 denser dither | plaza/paths |
| P101 | 25m | NPC 更常走动 / flip / bob | ambient life |
| P102 | 25m | golden + Critic + push | origin/main |

### 店招构图进度
- [x] P99 · P100 · P101 · P102  

## 店面交互同步与有机地面（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P103 | 35m | 门/买卖/烟/面包房内景对齐店面 | 10_shop_door + interiors |
| P104 | 30m | 路径/广场去砖纹 + 变体 dither | tileset + town golden |
| P105 | 25m | golden + Critic + push | origin/main |

### 店面交互进度
- [x] P103 · P104 · P105  

## NPC 排班与进店手感（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P106 | 25m | lin/ka 排班对齐店面 + 缩短 facade coll | characters.json |
| P107 | 20m | 可可/派收费 + 门前接近 | interact_zone |
| P108 | 20m | golden + Critic + push | origin/main |

### NPC 排班进度
- [x] P106 · P107 · P108  

## 参考图视觉对齐（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P109 | 40m | 林冠层次 + 更高瀑碗 + 店面阴影 | canopy/waterfall |
| P110 | 30m | 中图落叶林 denser（避开广场） | overview |
| P111 | 25m | golden + Critic + push | origin/main |

### 参考视觉进度
- [x] P109 · P110 · P111  

## 农庄灯塔与河岸加厚（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P112 | 30m | barn/silo/lighthouse + 河岸 sand | farm/lake/river |
| P113 | 20m | 瀑金帧构图 + canopy 微细节 | waterfall/overview |
| P114 | 20m | Critic + push | origin/main |

### 农庄灯塔进度
- [x] P112 · P113 · P114  

## 冒烟证据与 itch 包装（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P115 | 35m | 农庄生长冒烟 + tween 修复 + itch 图清单 | smoke/16 + ITCH draft |

### 冒烟包装进度
- [x] P115  

## 商店主图海报冲刺（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P116 | 40m | 区划大字标 + 金帧藏 HUD + 镇区院落/农庄装饰作物 | 00_overview + Critic |
| P117 | 25m | Critic + push；催用户签字试玩 / itch URL | origin/main |

### 海报冲刺进度
- [x] P116 · [x] P117  

## 帧动画与拼接对齐（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P118 | 45m | 玩家行走腿帧夸张重绘 + 锄/浇/播专用帧 | player sheet + F5 腿动 |
| P119 | 40m | 农庄床软 fringe + 脚底阴影 + y_sort | farm golden / 对照 stardew ref |
| P120 | 25m | Critic + push；催用户验动画 | origin/main |

### 帧动画拼接进度
- [x] P118 · [x] P119 · [x] P120  

## 草土过渡与建筑嵌地（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P121 | 40m | grass↔dirt 过渡瓦 + 缝合 pass | tileset + 01_farm |
| P122 | 30m | 农舍/谷仓脚垫 doormat/岩石嵌地 | farm golden |
| P123 | 25m | 走路帧 MCP 冒烟 + Critic + push | smoke/17 + origin/main |

### 草土嵌地进度
- [x] P121 · [x] P122 · [x] P123  

## 动物围栏 + 工具帧冒烟 + blob 床缘（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P124 | 35m | 畜栏 clamp + 床缘 nibble/protrude + SE/SW 角瓦 | decor/animal + tileset 25/26 |
| P125 | 30m | 锄/浇 freeze 冒烟 + 动作锁加固 | smoke/18_hoe · 19_water |
| P126 | 25m | 重抓 golden + Critic + push；催用户验腿/工具帧 | origin/main |

### 围栏工具进度
- [x] P124 · [x] P125 · [x] P126  

## 星露谷院子 blob + 木台嵌地（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P127 | 40m | 农舍/谷仓不规则土坪 blob + 蜿蜒路径 | 01_farm vs stardew ref |
| P128 | 30m | 院子碎屑密度 + 木桥瓦门廊台阶；区标默认隐藏 | landmarks + footing |
| P129 | 25m | golden + Critic + push；催用户签字 | origin/main |

### 院子 blob 进度
- [x] P127 · [x] P128 · [x] P129  

## Overview 对齐：畜栏土坪 + 湖田 + 路径软边（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P130 | 35m | 畜栏泥土围场（对照 overview） | 01_farm pen dirt |
| P131 | 35m | 回声湖南田垄 + 梯田 ledge fringe | 06_lake / 05_terrace |
| P132 | 25m | 路径/广场 `_soften_path_edges` + Critic/push | 00_overview |

### Overview 对齐进度
- [x] P130 · [x] P131 · [x] P132  

## 谷仓立面 + Entities y-sort（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P133 | 40m | 重绘 barn/silo（木板/石基/穹顶） | prop_barn*.png |
| P134 | 35m | Player 挂 Entities；NPC/树同 z；作物进 Entities | 01_farm y-sort |
| P135 | 25m | golden + Critic + push | origin/main |

### 立面 y-sort 进度
- [x] P133 · [x] P134 · [x] P135

## 河岸缝合 + 栏杆密铺（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P136 | 40m | jagged water_edge + `_stitch_water_shores`（外圈水瓦软边） | 02_river / 06_lake |
| P137 | 30m | fence 双轨密铺；landmarks `z_index=0` 与 Player y-sort | 01_farm 畜栏 |
| P138 | 25m | golden + Critic + push | origin/main |

### 河岸栏杆进度
- [x] P136 · [x] P137 · [x] P138

## 镇店招立面 + 广场密度（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P139 | 45m | 重绘 shop/cafe/bakery（石基/展窗货品/多层雨棚） | prop_*_awning + bakery |
| P140 | 30m | 广场灯/椅/院树/门垫/碎石密度 | 03_town / 09_storefronts |
| P141 | 25m | golden + Critic + push | origin/main |

### 镇店招进度
- [x] P139 · [x] P140 · [x] P141

## Overview 油画密度（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P142 | 35m | 近色草瓦 + 8×8 草斑破棋盘 | tileset + 00_overview |
| P143 | 40m | 中景/站湖走廊树灌花加密 | decor groves |
| P144 | 25m | overview 取景含四区标 + Critic/push | origin/main |

### Overview 密度进度
- [x] P142 · [x] P143 · [x] P144

## 树冠油画层 + NPC 生活动感（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P145 | 40m | 中谷落叶树冠条带（广场镂空）+ 单树疏化 | prop_meadow_canopy + 00_overview |
| P146 | 30m | NPC 脚影/步速/摆动；更常走动 | smoke/20_npc_life |
| P147 | 25m | golden + Critic + push | origin/main |

### 树冠 NPC 进度
- [x] P145 · [x] P146 · [x] P147

## 民宅/农舍立面（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P148 | 40m | 四色民宅加深（石基/百叶/花箱/门廊） | prop_house_*.png |
| P149 | 30m | 米勒农舍加深 + 筒仓入画取景 | 01_farm |
| P150 | 25m | golden + Critic + push | origin/main |

### 民宅农舍进度
- [x] P148 · [x] P149 · [x] P150

## 瀑布/车站英雄镜头（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P151 | 45m | 松冠站/瀑开窗 + skyline notch + 瀑碗抬层 | prop_pine_canopy / skyline / waterfall_bowl |
| P152 | 30m | 站厅+火车出冠；交互点南移 | 04_station + landmarks._station |
| P153 | 25m | golden + Critic + push | 07_waterfall 瀑入画 · origin/main |

### 瀑布车站进度
- [x] P151 · [x] P152 · [x] P153

## 瀑碗重绘 + overview 海报框（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P157 | 40m | 多级有机瀑碗（喉口水色/苔藓崖） | prop_waterfall_bowl |
| P158 | 25m | overview 紧框 + canopy 减透；站台 hash 去条纹 | 00_overview |
| P159 | 20m | golden + Critic + push | origin/main |

### 瀑碗 overview 进度
- [x] P157 · [x] P158 · [x] P159

## 河岸接缝 + 车站地面（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P154 | 35m | 瀑岸沙/WE 软化 + stitch 少硬边 | 07_waterfall |
| P155 | 40m | 车站有机 yard + 双轨 + 杂物加密 | 04_station |
| P156 | 20m | golden + Critic + push | origin/main |

### 河岸车站进度
- [x] P154 · [x] P155 · [x] P156

## World-driven 中谷构图（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P160 | 50m | REGION 模板 + 实心路脊 + mid-valley dirt ridge + 湖 wobble + canopy 错位 | `P160_MID_VALLEY.md` + golden + VISUAL_QA |

### World-driven 进度
- [x] P160（itch 主图仍否；需试玩签字）

## 树冠裂带 + 路缘 fringe + 软湖岸（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P161 | 45m | 不规则松/落叶冠 lobe + path GD fringe/spit + 湖岸沙缘 dither | prop_*_canopy + golden + VISUAL_QA |

### 树冠湖岸进度
- [x] P161（itch 主图仍否）

## 软接缝纪律 + 镇区密度（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P162 | 40m | PATH 免 dirt-stitch 棋盘；湖岸陆地禁 WE；+民宅/footing | golden 03/06 + VISUAL_QA |

### 软接缝镇区进度
- [x] P162（itch 主图仍否；需试玩签字）

## 非对称广场 + tileset 软边（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P163 | 45m | 广场破镜像 + 石芯；WE/GD 瓦软边重生；湖 lobe | tileset + 03_town + VISUAL_QA |

### 广场软边进度
- [x] P163（itch 主图仍否）

## 中谷植被簇 + 海报框（≠ complete）

| ID | 估时 | 目标 | 完成证据 |
|----|------|------|----------|
| P164 | 35m | mid-valley grove clusters + canopy alpha + overview 0.37 | 00_overview + VISUAL_QA |

### 中谷密度进度
- [x] P164（itch 主图仍否；需试玩签字）





