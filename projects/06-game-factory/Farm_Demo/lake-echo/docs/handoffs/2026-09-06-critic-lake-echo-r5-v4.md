# TASK HANDOFF v2

### Meta
- handoff_id: 2026-09-06-critic-lake-echo-r5-v4
- playbook: PB-Game-Visual
- from_agent: Critic
- to_agent: Conductor
- parallel_group: none

### Objective
Independent **v4** audit of Lake Echo R5 against `GOAL_R5_ONE_TO_ONE_REMAKE.md` §0 / §4 / §5 after station/tunnel/Z5 cliff/forest densify pass. Judge PASS / PARTIAL / FAIL with evidence. Decide whether Goal may close. **No fixes implemented.**

### Context
- Goal ID: `farm-demo-r5-one-to-one-remake`
- Reference overview: `docs/ref/frame_01.png` (dense 3/4 village: cliff forest + waterfall, farm, plaza houses, station, stone terraces, Lake Echo lighthouse)
- Current goldens: `assets/qa/golden_r5/00_overview.png` … `06_lake.png` (working tree modified vs last commit; CLI capture lineage)
- Prior Critic: v1 FAIL · v2 FAIL · **v3 FAIL** (`2026-09-06-critic-lake-echo-r5-v3.md`)
- ACCEPTANCE self-status (doc as read): Goal 不可关；视觉一比一 FAIL；MCP→farm-demo FAIL；Critic 仅记到 v2（**过时**，未登记 v3）
- Zones card: `2026-09-06-zones-z1-z6.md`（六区均自标 PARTIAL）
- Tip commit on tracking line: `e7b36b0 Strengthen Lake Echo station and terrace cliff bands.` · working tree **dirty**（golden + `world.gd` + `landmarks.gd` 等未提交/未推）

### Inputs
- paths:
  - `docs/GOAL_R5_ONE_TO_ONE_REMAKE.md`
  - `docs/ACCEPTANCE.md` · `docs/VERIFY_MCP.md`
  - `docs/ref/frame_01.png`
  - `assets/qa/golden_r5/00_overview.png` … `06_lake.png`
  - `scripts/world.gd`（Z5 cliff bands · Z4 tunnel mouth）
  - `scripts/landmarks.gd`（`_station` props）
  - `scripts/decor.gd`（atlas 单帧）
  - `docs/handoffs/2026-09-06-zones-z1-z6.md`
  - prior: `…-critic-lake-echo-r5.md` · `…-v2.md` · `…-v3.md`
- tools_allowed: [code]（只读）；MCP `get_godot_status`（证据）

### Completed
- Re-read Goal §0 / §4 / §5
- Read all seven golden_r5 shots + `frame_01.png`
- Spot-check `world.gd` Z5 cliff paint + Z4 tunnel cliff; `landmarks.gd` `_station`
- Confirm atlas path still via `_spr_atlas` / `_atlas_frame`
- MCP status: still Connected to **farm-demo** (not lake-echo)
- Diff vs Critic v3: station building, tunnel, denser forest, Z5 cliff bands

### Evidence

| 类型 | 路径或摘要 | 结果 |
|------|------------|------|
| screenshot | `00_overview.png` vs `docs/ref/frame_01.png` | 六区象限粗可辨（SW 农场 / 西河 / 中镇 / NE 站+隧道 / 东梯田带 / SE 湖灯塔）。相对 frame_01：开敞棋盘草仍大、林密仍差一个数量级、屋群/路径有机度弱、河更直、湖近正圆空心 → 密度/风格 **FAIL** |
| screenshot | `01_farm.png` | 红仓×2、筒仓×2、农舍、作物行、牛羊鸡单帧。动物脚下暗底、田块仍网格感；无 frame 级畜栏围合质感 → 拓扑 **PARTIAL** / 视觉 **FAIL** |
| screenshot | `02_river.png` | 竖河+岸泥带+桥缘；北缘树带更密，远景针叶剪影可读。瀑布/泉基仍偏玩具感；棋盘草刺眼 → **PARTIAL**（林密 **改善**） |
| screenshot | `03_town.png` | 石板广场+≥4 条纹摊+雕像；屋多在镜头外。NPC 已单帧但 **同款老人×6 克隆漫游** → 骨架 **PARTIAL** / 多样性 **FAIL** |
| screenshot | `04_station.png` | **站房**（门+多窗+灰顶）+火车+站台摊位清晰可读；烟小团。本帧未含隧道（隧道偏东，见 overview）。轨向/平台网格仍假；相对 v3「小站房色块」**改善** → 地标可读 **PARTIAL**（仍远低于 frame 站区） |
| screenshot | `05_terrace.png` | 多层水平带+灰阶/坡+石块过渡；相对 v3 平土条 **有崖带意图**。仍非 frame 石墙分层崖+有机阶田；彩灯串偏装饰噪声 → 分层 **PARTIAL** / 一比一 **FAIL** |
| screenshot | `06_lake.png` | 灯塔条纹+码头+帆船可辨；水面白点网格空旷；岸林/沙石/建筑密度仍弱 → **FAIL** vs frame 东侧湖区 |
| code | `landmarks.gd` `_station` L70–77 | `prop_station` + `prop_canopy` + `prop_train` + **`prop_tunnel`** + stall/fence — 站区 props **齐全接线** |
| code | `world.gd` L189–225 | Z4 三轨+plaza+**tunnel cliff mouth**；Z5 **5 band** farm ledge + thick `T_CLIFF` + stair cuts — 意图对齐 Goal；金图观感仍弱 |
| code | `decor.gd` `_atlas_frame` / `_spr_atlas`；animals+npcs | atlas 窄义 **仍 PASS**（无整 sheet bleed） |
| code | `world.gd` W/H 192×128 TileMapLayer；`player.gd` zoom=(2,2)；y_sort | 架构 **PASS** |
| code | `farm_plots` + door→house（沿用；本轮未重跑） | 玩法接线 **PASS**（缺 MCP 运行时金证据） |
| runtime | MCP `get_godot_status` | `project_path` = `…/Farm_Demo/farm-demo/` → DoD1/5 首选 **FAIL** |
| docs | `VERIFY_MCP.md` / `ACCEPTANCE.md` | 首选 MCP 未过；ACCEPTANCE 仍 FAIL/NO；未更新 v3/v4 Critic 行 → DoD5 **FAIL** |
| handoff | 仅 `2026-09-06-zones-z1-z6.md`；无独立 `*-z1`…`*-z6` | DoD6 **PARTIAL** |
| git | `main...origin/main`；WT dirty（golden + scripts） | tip `e7b36b0` 已在线上；**当前金图/脚本改动未提交未推** → DoD7 **FAIL**（不可宣称已推终态） |

### 相对 Critic v3 的可见改善（诚实记账，不抬整体 PASS）

| 项 | v3 | v4 观察 | 判定 |
|----|----|---------|------|
| Atlas 单帧（动物/NPC 无 sheet bleed） | 窄义 PASS | `01`/`03` 仍单只轮廓；代码路径未回退 | **保持 PASS（窄义）** |
| 站房建筑 | 小站房/偏色块剪影 | `04_station` 长站房门窗顶可读；`prop_station.png` | **改善 → PARTIAL** |
| 隧道 | v3 未记为可见完成 | overview NE 轨端暗拱口；`prop_tunnel` + cliff mouth 代码 | **新增可读 → PARTIAL** |
| 林密 | 网格树、空草过大 | `02`/`00` 河岸/北缘树带更密 + 针叶远景 | **改善，仍不够 frame → FAIL→更接近但 FAIL** |
| Z5 崖分层 | 平铺土条+作物 | `world.gd` thick cliff bands；`05` 阶/坡/崖带可读 | **改善 → PARTIAL**（非一比一） |
| 克隆 NPC / YSort 叠层 | 未消 | 镇广场仍同款×N；布局问题仍在 | **未解决** |
| 视觉一比一 vs frame_01 | FAIL | 仍数量级差距 | **仍 FAIL** |

### Definition of Done — 逐项判定（Goal §4）

| # | DoD 项 | 判定 | 证据 |
|---|--------|------|------|
| 1 | `lake-echo/` 可 F5；MCP `get_errors=0` | **PARTIAL** | CLI/金图证明工程可跑。MCP **仍** Connected 到 `farm-demo/`（本轮 `get_godot_status`），无 lake-echo `get_errors=0`。 |
| 2 | 六区可辨认地标 + 相对位置与总览一致 | **PARTIAL** | 拓扑粗一致；站房/隧道/灯塔/谷仓「认类」提升。细节/材质仍远低于 §0；§5 色块风险在湖/瀑/部分 props 仍在。 |
| 3 | TileMap 架构；整数相机缩放；YSort | **PASS** | TileMapLayer 主地；zoom=(2,2)；Decor/Entities y_sort。叠层瑕疵不降级本条。 |
| 4 | Z1 农场玩法；至少一栋可进室内 | **PASS**（代码） / **PARTIAL**（验收证据） | 接线存在；缺 MCP 锄地/进屋断言与金图。 |
| 5 | `VERIFY_MCP.md` R5 全过；`ACCEPTANCE.md` 每行有证据 | **FAIL** | VERIFY 首选未过；ACCEPTANCE 多行 PARTIAL/FAIL/NO；无逐区「金图 \| frame \| 差异」对照表；Critic 行过时。 |
| 6 | 多 Agent handoff 六区齐全；Critic PASS | **FAIL** | 仅合并 zones 卡；本 Critic **整体 FAIL**。 |
| 7 | 已推 GitHub | **FAIL** | tip 历史提交在 origin；**当前** golden/`world.gd`/`landmarks.gd` 等 dirty，终态未推。ACCEPTANCE「PENDING」方向正确。 |

### 「一比一」锁定维度（Goal §0）— 严厉

| 维度 | 判定 | 证据要点 |
|------|------|----------|
| 拓扑 | **PASS**（粗） | 六区相对方位与蓝图/frame_01 象限一致；隧道落 NE 合理 |
| 地标 | **PARTIAL→偏 FAIL** | 站房/隧道相对 v3 进步；火车/灯塔/瀑布/梯田石墙仍未达参考可辨细节；禁止标地标 PASS |
| 风格 | **FAIL** | 棋盘草、硬区界、弱 8 向岸/崖过渡；3/4 分层氛围不足 |
| 密度 | **FAIL** | 林/岸/屋有进步；总览与湖区仍远低于 `frame_01` |
| 玩法 | **PASS**（代码层） | WASD、Z1 农事、进屋、中文 UI 线路在 |

### 禁止偷懒抽查（Goal §5）

| 禁令 | 判定 |
|------|------|
| 禁止旧 farm-demo Sprite 铺地扩一扩 | **遵守** — `lake-echo` TileMap |
| 禁止单张背景大图当世界 | **遵守** |
| 禁止火车站/灯塔色块占位算完成 | **部分缓解、未清** — 站房改善；灯塔/瀑/湖 props 仍剪影级 |
| 禁止 Verifier 只查坐标不截图 | **部分遵守** — 有 golden；缺正式 vs-frame 对照表 |
| 禁止 Asset 跳过棋盘格 QA | **形式遵守** ≠ 美术达标 |
| 禁止六区未齐宣称一比一 | **勿宣称** |
| 禁止无六区 handoff 包办 | **部分违规** — 仅合并卡 |
| 禁止未推 GitHub 宣称完成 | **勿宣称**（WT dirty） |

### Forbidden-claim checklist

| 禁止宣称项 | Critic 判定 |
|------------|-------------|
| Sprite-per-tile ground 冒充重建 | **未犯** |
| Big BG fake map | **未犯** |
| Atlas 未修仍宣称 NPC/动物 OK | **未犯**（窄义仍修） |
| 站房/隧道改善 = 视觉一比一完成 | **若宣称则违规** |
| Color-block landmarks / Goal 可关 | **若宣称则违规** |

### Top 5 blockers（关 Goal 前必须清）

1. **视觉密度与有机度仍远低于 `docs/ref/frame_01.png`** — 总览空草、湖空、屋/路径有机度不足（主阻塞；站房/隧道/林密不够关 Goal）。
2. **地标保真仍不足** — 灯塔/瀑布/火车/梯田石墙未达 §0/§5「可辨认细节」；站房仅升到 PARTIAL。
3. **Z5 仍非参考梯田拓扑** — cliff band 有意图，金图仍是水平色带+木阶，非 frame 石崖分层可走感。
4. **MCP 未 Connected 到 lake-echo** — DoD1/5 首选证据缺失；实测仍 `farm-demo/`。
5. **验收/推送未闭环** — 无逐区金图↔参考对照表；分 Wave z1–z6 handoff 不齐；WT dirty 未推；Critic 未 PASS；ACCEPTANCE 仍 FAIL/NO。

### Acceptance（本 Critic）
- [x] 对 Goal §4 七项给出 PASS / PARTIAL / FAIL + 证据路径
- [x] 严厉判定视觉一比一（站房/隧道/林密进步不抬视觉 PASS）
- [x] 记录相对 v3 的改善（station building、tunnel、atlas 保持、denser forest、Z5 cliff）
- [x] 列出 Top 5 blockers
- [x] 产出本文件
- [ ] Critic 整体 PASS ← **未勾选**
- [ ] 建议关 Goal ← **否**

### Open Questions
- **BLOCKER:** 密度可量化门槛（空白 tile %、每屏 prop 数）仍未写入规格。
- **BLOCKER:** 地标「更好的剪影」能否过关——需 Product/Conductor 书面标准（v3 未决）。
- 当前 dirty golden 与已推 tip 像素差是否需统一后再评 v5。

### Risks
- 因「站房+隧道+林密+崖带」误关 Goal → 违反 §0 视觉锁定。
- 把 PARTIAL 站区写成地标 PASS → 误导 Asset 停工。
- MCP 仍指 farm-demo 时伪造 lake-echo 验收。
- 不提交 dirty 金图却宣称 Verifier 过 → 证据漂移。

### Suggested Next Agent
**Asset（高保真灯塔/瀑/崖墙/岸变体；NPC 变体）‖ Builder（有机路径、湖岸密度、Z5 石崖可读、NPC 落点）** → **commit+push 当前金图** → **Verifier-Full（用户改接 MCP→lake-echo；逐区 vs frame 对照表）** → **Critic v5**。  
并行：拆/补 z1–z6 handoff；刷新 ACCEPTANCE（含 Critic v3/v4 行）。

### Required Output（下一 Agent）
1. 非色块 landmark/tileset 再提一档 + checker
2. 提交并推送一致的 `golden_r5` + 书面对照表（每区：金图 | 参考帧区域 | 差异）
3. MCP `get_errors=0`（path 含 lake-echo）+ 锄地/进屋运行时证据
4. `ACCEPTANCE.md` 无视觉 FAIL/NO；六区 handoff 齐全
5. push 后再请 Critic

### Do-Not
- 禁止因站房/隧道/林密改善就把视觉/密度标 PASS
- 禁止用更多同款 NPC/树刷屏冒充接近 frame_01
- 禁止只改 ACCEPTANCE 勾选不改美术
- 禁止在 MCP 未接 lake-echo 时伪造 get_errors=0
- 禁止未达 §0 地标/密度标准就关 Goal
- 禁止本 Critic 实现修复（审计只读）

### Related Files
- `docs/GOAL_R5_ONE_TO_ONE_REMAKE.md`
- `docs/ACCEPTANCE.md` · `docs/VERIFY_MCP.md`
- `assets/qa/golden_r5/00_overview.png` … `06_lake.png`
- `docs/ref/frame_01.png`
- `scripts/decor.gd` · `world.gd` · `landmarks.gd` · `farm_plots.gd`
- `docs/handoffs/2026-09-06-zones-z1-z6.md`
- `docs/handoffs/2026-09-06-critic-lake-echo-r5.md`
- `docs/handoffs/2026-09-06-critic-lake-echo-r5-v2.md`
- `docs/handoffs/2026-09-06-critic-lake-echo-r5-v3.md`

---

## Verdict（给 Conductor / 用户）

**Goal 不能关闭。 Critic 整体 FAIL。**

| 项 | 结论 |
|----|------|
| Critic 整体 | **FAIL** |
| 相对 v3 | 站房、隧道、林密、Z5 cliff band **可见改善**；atlas **保持** |
| 视觉一比一 / 密度 | **仍 FAIL**（严厉；相对 frame_01 不合格） |
| 架构 TileMap + zoom + YSort | **PASS** |
| 玩法骨架 | **PASS**（证据 PARTIAL） |
| MCP→lake-echo | **FAIL**（仍 farm-demo） |
| Git 终态 | **FAIL**（dirty 未推） |
| 关 Goal | **否** — 清 Top 5 → Verifier-Full → Critic PASS |
