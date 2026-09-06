# TASK HANDOFF v2

### Meta
- handoff_id: 2026-09-06-critic-lake-echo-r5-v3
- playbook: PB-Game-Visual
- from_agent: Critic
- to_agent: Conductor
- parallel_group: none

### Objective
Independent **v3** audit of Lake Echo R5 against `GOAL_R5_ONE_TO_ONE_REMAKE.md` §0 / §4 / §5 after atlas crop + crop densify. Judge PASS / PARTIAL / FAIL with evidence. Decide whether Goal may close. **No fixes implemented.**

### Context
- Goal ID: `farm-demo-r5-one-to-one-remake`
- Reference overview: `docs/ref/frame_01.png` (dense 3/4 village: cliff forest + waterfall, Miller/Pillar farm, plaza houses, station, stone terraces, Lake Echo lighthouse peninsula)
- Current goldens: `assets/qa/golden_r5/00_overview.png` … `06_lake.png` (CLI `--capture_golden`; overview zoom 0.45)
- Prior Critic: `2026-09-06-critic-lake-echo-r5` → FAIL; `…-v2` → FAIL
- ACCEPTANCE self-status: Goal 不可关；视觉一比一 FAIL；MCP→farm-demo FAIL
- Zones card: `2026-09-06-zones-z1-z6.md`（六区均自标 PARTIAL）
- Latest known commit (local): `ff270f0 Fix Lake Echo atlas bleed and densify crop rows.` · `main...origin/main`

### Inputs
- paths:
  - `docs/GOAL_R5_ONE_TO_ONE_REMAKE.md`
  - `docs/ACCEPTANCE.md` · `docs/VERIFY_MCP.md`
  - `docs/ref/frame_01.png`
  - `assets/qa/golden_r5/00_overview.png` … `06_lake.png`
  - `scripts/decor.gd`（AtlasTexture 强制裁单帧）
  - `scripts/world.gd` · `landmarks.gd` · `farm_plots.gd` · `main.gd`
  - `docs/handoffs/2026-09-06-zones-z1-z6.md`
  - prior: `2026-09-06-critic-lake-echo-r5.md` · `…-v2.md`
- tools_allowed: [code]（只读；Read 金图/参考帧/源码）

### Completed
- Re-read Goal §0 / §4 / §5
- Read all seven golden_r5 shots + `frame_01.png`
- Verified `decor.gd` `_atlas_frame` / `_spr_atlas` for animals + NPCs
- Cross-checked ACCEPTANCE, VERIFY_MCP, zones handoff, git tracking vs v2 blockers
- Harsh visual 1:1 vs frame_01; noted atlas delta vs v1/v2 “clone army / sheet bleed”

### Evidence

| 类型 | 路径或摘要 | 结果 |
|------|------------|------|
| screenshot | `00_overview.png` vs `docs/ref/frame_01.png` | 六区象限粗可辨（SW 农场 / 西河 / 中镇 / NE 站 / 东田带 / SE 湖）。相对 frame_01：棋盘草空地巨大、树网格刷、无密林崖分层、屋/路径有机度弱 → 密度/风格 **FAIL** |
| screenshot | `01_farm.png` | 红仓×2、筒仓×2、农舍、作物行、牛羊鸡可见。**Atlas：** 动物为单只剪影，非整条图集横条。仍远低于 frame 左下畜栏/栅栏/成排田质感；NPC 叠树冠 → 拓扑 **PARTIAL** / 视觉 **FAIL** |
| screenshot | `02_river.png` | 瀑布剪影+竖河+岸边泥土带进镜；棋盘草刺眼；瀑布基座灰盒感 → **PARTIAL** |
| screenshot | `03_town.png` | 石板广场+≥4 条纹摊+灰雕像；**NPC 已单帧裁切（无 sheet bleed）**，但仍是同一老人多份同姿 →「图集军团」已灭、「克隆 NPC」仍在。屋体多在镜头外/边缘 → 骨架 **PARTIAL** / 密度·多样性 **FAIL** |
| screenshot | `04_station.png` | 铁轨+火车+小站房可辨；NPC 站在火车头上；站房/火车仍偏色块剪影 → **PARTIAL**（触碰 §5 色块红线） |
| screenshot | `05_terrace.png` | 相对 v2：作物行已铺满水平带。仍是平铺土条+木板路，非 frame 石墙分层崖+阶梯感 → 作物密度 **改善** / 地形一比一 **FAIL** |
| screenshot | `06_lake.png` | 灯塔条纹+码头+帆船；大片空水网格；岸建筑/沙石林缘不足 → **FAIL** vs frame 东侧湖区 |
| code | `decor.gd` `_atlas_frame` + `_spr_atlas`；`_animals`/`_npcs` 全走 atlas | **PASS** — 无对 npc/animal 整张 `load()` 当 Sprite 纹理 |
| code | `world.gd` W/H 192×128 TileMapLayer；`main.gd`/`player.gd` zoom=(2,2)；y_sort | 架构 **PASS** |
| code | `farm_plots.gd` + door `interact_zone` house + `house_interior` | 玩法接线 **PASS**（仍缺 MCP 运行时断言） |
| docs | `VERIFY_MCP.md` 首选 MCP 清单；CLI 后备已用 | 首选未满足 → DoD5 **FAIL** |
| docs | `ACCEPTANCE.md` 诚实标 FAIL/PARTIAL/NO | 未闭环 → DoD5 **FAIL** |
| handoff | `2026-09-06-zones-z1-z6.md` 合并卡；无独立 `*-z1`…`*-z6` Wave 卡 | DoD6 **PARTIAL**（有证据卡，非 Goal 要求的分 Wave handoff 齐全） |
| git | `main...origin/main`；`ff270f0` atlas+crops 已在 tip | 相对 v2「densify 未推」**已改善**；本 v3 文档写出时尚 dirty/未推 → DoD7 **PARTIAL** |

### Atlas fix 专项（相对 Critic v1/v2）

| 检查 | 判定 | 证据 |
|------|------|------|
| 代码强制 AtlasTexture 单帧 | **PASS** | `decor.gd` L17–38, L53–66, `_animals` / `_npcs` |
| 农场动物整条图集 bleed（横条「动物军」） | **已修复** | `01_farm.png`：独立 cow/sheep/chicken 剪影，非横向 sprite strip |
| 镇 NPC 整条图集 bleed | **已修复** | `03_town.png`：单角色轮廓清晰，无相邻帧拼贴出血 |
| 「克隆军」同款 NPC 刷屏 | **未消除（降级问题）** | 镇/站仍多份同一老人同姿；站台 NPC 叠火车。属变体/布局问题，**不再是 atlas bleed** |
| ACCEPTANCE「动物/NPC 不整条图集误显 PASS」 | **同意（窄义）** | Critic 确认窄义 PASS；不可外推为视觉一比一 PASS |

### Definition of Done — 逐项判定（Goal §4）

| # | DoD 项 | 判定 | 证据 |
|---|--------|------|------|
| 1 | `lake-echo/` 可 F5；MCP `get_errors=0` | **PARTIAL** | CLI 可跑并写 golden（`VERIFY_MCP.md` CLI；金图存在）。**无** `user-godot-tomyud1` Connected 到 lake-echo 的 `get_errors=0` 日志；zones handoff / ACCEPTANCE 明示 MCP→farm-demo。 |
| 2 | 六区可辨认地标 + 相对位置与总览一致 | **PARTIAL** | 拓扑粗一致（`00_overview` + ZONES）。地标「能认出类别」但火车/灯塔/瀑布/站房仍剪影级，**不满足** §0 地标细节标准。 |
| 3 | TileMap 架构；整数相机缩放；YSort | **PASS** | `world.gd` TileMapLayer；zoom=(2,2)；Decor/实体 y_sort。主世界非每格 Sprite 铺地。YSort 仍有叠树/叠火车瑕疵，不降级本条架构 PASS。 |
| 4 | Z1 农场玩法；至少一栋可进室内 | **PASS**（代码） / **PARTIAL**（验收证据） | `farm_plots` + door→house + interior 存在；缺 MCP 锄地/进屋金图断言。 |
| 5 | `VERIFY_MCP.md` R5 全过；`ACCEPTANCE.md` 每行有证据 | **FAIL** | VERIFY 首选 MCP 未跑；ACCEPTANCE 多行 PARTIAL/FAIL；无逐区「金图 \| frame \| 差异」对照表。 |
| 6 | 多 Agent handoff 六区齐全；Critic PASS | **FAIL** | 仅合并 zones 卡；本 Critic **整体 FAIL**（未勾选 PASS）。 |
| 7 | 已推 GitHub | **PARTIAL** | atlas/densify 终态 `ff270f0` 已在 `origin/main` 跟踪线上；ACCEPTANCE「PENDING」过时。本 Critic v3 文件需另推才算审计闭环。 |

### 「一比一」锁定维度（Goal §0）— 严厉

| 维度 | 判定 | 证据要点 |
|------|------|----------|
| 拓扑 | **PASS**（粗） | 六区相对方位与蓝图/frame_01 象限一致 |
| 地标 | **FAIL** | 谷仓/灯塔/火车/瀑布可「认类」；细节/材质远低于参考；§5 色块占位风险仍在（尤其站/灯塔） |
| 风格 | **FAIL** | 棋盘草、硬直角区界、少 8 向岸/崖过渡；粒子烟/涟漪无法弥补像素氛围落差 |
| 密度 | **FAIL** | 作物行相对 v2 **有进步**；总览/湖/林缘/屋群仍数量级低于 `frame_01` |
| 玩法 | **PASS**（代码层） | WASD、Z1 农事、进屋、中文 UI/toast 线路在 |

### 禁止偷懒抽查（Goal §5）

| 禁令 | 判定 |
|------|------|
| 禁止旧 farm-demo Sprite 铺地扩一扩 | **遵守** — 新 `lake-echo` TileMap |
| 禁止单张背景大图当世界 | **遵守** |
| 禁止火车站/灯塔色块占位算完成 | **仍违规风险** — golden 04/06 剪影级；不可标地标 PASS |
| 禁止 Verifier 只查坐标不截图 | **部分遵守** — 有 golden；缺正式 vs-frame 对照表 |
| 禁止 Asset 跳过棋盘格 QA | **形式遵守**（历史 checker）；≠ 美术达标 |
| 禁止六区未齐宣称一比一 | **勿宣称** |
| 禁止无六区 handoff 包办 | **部分违规** — 仅合并卡，非分 Wave 齐全 |
| 禁止未推 GitHub 宣称完成 | **勿宣称**（代码 tip 已推；Goal 仍未关） |

### Forbidden-claim checklist

| 禁止宣称项 | Critic 判定 |
|------------|-------------|
| Sprite-per-tile ground 冒充重建 | **未犯** |
| Big BG fake map | **未犯** |
| Atlas 未修仍宣称 NPC/动物 OK | **未犯** — 本轮窄义已修 |
| Color-block landmarks / 视觉一比一完成 | **若宣称则违规** |
| Atlas 修了 = 密度/一比一达标 | **禁止外推** |

### Top 5 blockers（关 Goal 前必须清）

1. **视觉密度与有机度仍远低于 `docs/ref/frame_01.png`** — 总览空草、网格树、湖空、屋群不足（主阻塞；作物 densify 不够关 Goal）。
2. **地标资产仍偏色块/剪影** — 火车、站房、灯塔、瀑布基座未达 §0/§5「可辨认细节」；直接卡死地标 PASS。
3. **Z5 仍非参考梯田拓扑** — 水平土条+作物 ≠ 石墙分层崖+石阶可走感（`05_terrace.png`）。
4. **MCP 未 Connected 到 lake-echo** — DoD1/5 首选证据缺失；CLI 不能永久替代。
5. **验收与 handoff 未闭环** — 无逐区金图↔参考对照表；分 Wave z1–z6 handoff 不齐；Critic 未 PASS；ACCEPTANCE 仍 FAIL/NO。

### Acceptance（本 Critic）
- [x] 对 Goal §4 七项给出 PASS / PARTIAL / FAIL + 证据路径
- [x] 严厉判定视觉一比一（atlas 进步不抬视觉 PASS）
- [x] 记录 atlas 对农场/小镇「整条图集军团」的改善
- [x] 列出 Top 5 blockers
- [x] 产出本文件
- [ ] Critic 整体 PASS ← **未勾选**
- [ ] 建议关 Goal ← **否**

### Open Questions
- **BLOCKER:** 密度可量化门槛（空白 tile %、每屏 prop 数）仍未写入规格。
- **BLOCKER:** 地标是否强制重画高保真像素，还是允许「更好的剪影」过关——需 Product/Conductor 书面标准。
- MCP 改接后是否必须重采 golden（与 CLI 像素一致性）。

### Risks
- 因「atlas PASS + 作物更密 + tip 已推」误关 Goal → 违反 §0 视觉锁定与 §5。
- 把「无 sheet bleed」写成「无克隆 NPC」→ 误导 Asset 停工。
- YSort/叠层瑕疵（NPC 上树、上火车）若被忽略，会污染后续 Verifier 金图。

### Suggested Next Agent
**Asset（非色块地标 + 屋/崖/岸变体）‖ Builder（有机路径、Z5 真分层、NPC 变体与落点）** → **Verifier-Full（MCP→lake-echo；逐区 vs frame 对照表）** → **Critic v4**。  
并行：拆/补 z1–z6 handoff；刷新 ACCEPTANCE 后 push。

### Required Output（下一 Agent）
1. 非色块 landmark/tileset + 可展示 checker
2. 新 `golden_r5` + 书面对照表（每区：金图 | 参考帧区域 | 差异）
3. MCP `get_errors=0` + 锄地/进屋运行时证据
4. `ACCEPTANCE.md` 无视觉 FAIL/NO；六区 handoff 齐全
5. push 后再请 Critic

### Do-Not
- 禁止因 atlas 修复就把视觉/密度标 PASS
- 禁止用更多同款 NPC/树刷屏冒充接近 frame_01
- 禁止只改 ACCEPTANCE 勾选不改美术
- 禁止在 MCP 未接 lake-echo 时伪造 get_errors=0
- 禁止未达 §0 地标/密度标准就关 Goal

### Related Files
- `docs/GOAL_R5_ONE_TO_ONE_REMAKE.md`
- `docs/ACCEPTANCE.md` · `docs/VERIFY_MCP.md`
- `assets/qa/golden_r5/00_overview.png` … `06_lake.png`
- `docs/ref/frame_01.png`
- `scripts/decor.gd` · `world.gd` · `landmarks.gd` · `farm_plots.gd`
- `docs/handoffs/2026-09-06-zones-z1-z6.md`
- `docs/handoffs/2026-09-06-critic-lake-echo-r5.md`
- `docs/handoffs/2026-09-06-critic-lake-echo-r5-v2.md`

---

## Verdict（给 Conductor / 用户）

**Goal 不能关闭。 Critic 整体 FAIL。**

| 项 | 结论 |
|----|------|
| Critic 整体 | **FAIL** |
| Atlas 整条图集 bleed | **已改善（窄义 PASS）** — 农场动物/镇 NPC 不再整 sheet 误显 |
| 克隆同款 NPC / 布局叠层 | **仍 PARTIAL/FAIL** |
| 架构 TileMap + zoom + YSort | **PASS** |
| 玩法骨架 | **PASS**（证据 PARTIAL） |
| 视觉一比一 / 密度 / 地标 | **FAIL**（相对 frame_01 仍严厉不合格） |
| Git tip（atlas 提交） | **已跟踪 origin**（相对 v2 改善） |
| 关 Goal | **否** — 清 Top 5 → Verifier-Full → Critic PASS |
