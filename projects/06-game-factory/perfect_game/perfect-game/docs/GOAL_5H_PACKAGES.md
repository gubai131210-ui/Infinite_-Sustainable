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
