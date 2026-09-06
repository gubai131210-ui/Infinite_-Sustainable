## TASK HANDOFF v2

### Meta
- handoff_id: 2026-09-06-critic-lake-echo-r5-v2
- playbook: PB-Game-Visual
- from_agent: Critic
- to_agent: Conductor
- parallel_group: none

### Objective
Independent re-audit of Lake Echo R5 against `GOAL_R5_ONE_TO_ONE_REMAKE.md` §0 / §4 / §5 after densify Wave. Judge PASS / PARTIAL / FAIL with evidence paths. Decide whether Goal may close. **No fixes implemented.**

### Context
- Goal ID: `farm-demo-r5-one-to-one-remake`
- Reference: `docs/ref/frame_01.png` (dense 3/4 village: waterfall forest, Miller farm, plaza, Cresthaven Station, stone terraces, Lake Echo)
- Current goldens: `assets/qa/golden_r5/00_overview.png` … `06_lake.png` (CLI `--capture_golden`, overview zoom 0.45)
- Prior Critic: `2026-09-06-critic-lake-echo-r5` → FAIL
- Prior densify claim: `2026-09-06-builder-lake-echo-density` (self-marked PARTIAL; visual 1:1 open)
- Prior Verifier: `2026-09-06-verifier-lake-echo-golden-v2` → CLI pack OK; **visual 1:1 FAIL**; MCP unused

### Inputs
- paths:
  - `docs/GOAL_R5_ONE_TO_ONE_REMAKE.md`
  - `docs/ACCEPTANCE.md` · `docs/VERIFY_MCP.md`
  - `docs/ref/frame_01.png`
  - `assets/qa/golden_r5/00_overview.png` … `06_lake.png`
  - `assets/processed/prop_barn.png` · `prop_farmhouse.png` · `prop_lighthouse.png` · `prop_train.png`
  - `scripts/world.gd` · `landmarks.gd` · `decor.gd` · `farm_plots.gd` · `house_interior.gd` · `main.gd`
  - `scenes/house_interior.tscn` · `scenes/world.tscn` · `scenes/player.tscn`
- prior_handoff_ids:
  - 2026-09-06-critic-lake-echo-r5
  - 2026-09-06-builder-lake-echo-density
  - 2026-09-06-verifier-lake-echo-golden-v2
  - 2026-09-06-builder-lake-echo-w0
- tools_allowed: [code]（本 Critic 只读；Read 金图/参考帧）

### Completed
- Re-read Goal DoD + 禁止偷懒清单
- Read all seven golden_r5 shots + `frame_01.png`
- Spot-checked TileMap paint, landmarks/decor placement, house interior scene
- Spot-checked landmark PNG fidelity (barn / farmhouse / lighthouse / train)
- Checked ACCEPTANCE / VERIFY_MCP / handoff coverage / git dirty vs origin

### Evidence
| 类型 | 路径或摘要 | 结果 |
|------|------------|------|
| screenshot | `assets/qa/golden_r5/00_overview.png` vs `docs/ref/frame_01.png` | 六区象限大致对；大片条纹草空地、矩形色块区、无分层崖林/密屋 → 密度/风格 **FAIL** |
| screenshot | `01_farm.png` | 土块田+极简农舍/红柱筒仓感；栅栏畜栏与成排作物远低于 frame 左下 → 拓扑 **PARTIAL** / 密度 **FAIL** |
| screenshot | `02_river.png` | TileMap 弯河+木桥可辨；瀑布常不进镜头；岸边过渡弱 → **PARTIAL** |
| screenshot | `03_town.png` | 灰石板矩形广场+条纹摊；屋/雕像细节弱；空格多 → 骨架 **PARTIAL** / 密度 **FAIL** |
| screenshot | `04_station.png` | 铁轨+极简火车块+小站房；触碰「色块占位」红线 → **PARTIAL**（剪影）/ 地标质量 **FAIL** |
| screenshot | `05_terrace.png` | 水平色带土条，非石墙分层梯田+作物行 → **FAIL** vs frame 右中 |
| screenshot | `06_lake.png` | 灯塔条纹块+船/码头；大片空水；岸边建筑/沙石密度不足 → **FAIL** 视觉 |
| asset | `prop_barn.png` · `prop_farmhouse.png` · `prop_lighthouse.png` · `prop_train.png` | 扁平几何色块、无阴影纹理 → **违反** §5「禁止色块占位算完成」 |
| code | `world.gd` `W:=192` `H:=128`；`_paint_base` → TileMapLayer `set_cell` | 架构 **PASS**（非每格 Sprite 世界） |
| code | `landmarks.gd` 六区 `_spr` 点位齐全 | 有点位 ≠ 达标；美术级 **FAIL** |
| code | `decor.gd` 树带/花/动物/6 NPC/烟涟漪粒子 | 相对 v1 有进步；相对 frame_01 仍稀疏 → 密度 **FAIL** |
| code | `farm_plots.gd` 锄浇种收；`decor.gd` door→house；`house_interior.tscn` 床箱出口 | 玩法接线 **PASS**（缺 MCP/室内金图） |
| docs | `VERIFY_MCP.md` 首选 MCP 未跑；CLI 后备已用 | DoD5 **FAIL** |
| docs | `ACCEPTANCE.md` 自标 Goal 不可关；多项 PARTIAL/FAIL | 诚实，但未闭环 → DoD5 **FAIL** |
| handoff | 无 `*-z1`…`*-z6`；仅 W0/density/verifier/critic | DoD6 **FAIL** |
| git | `main...origin/main`；大量 M/??（golden、props、decor、density handoff）未提交 | 终态未推 → DoD7 **FAIL** |

### Definition of Done — 逐项判定（Goal §4）

| # | DoD 项 | 判定 | 证据 |
|---|--------|------|------|
| 1 | `lake-echo/` 可 F5；MCP `get_errors=0` | **PARTIAL** | CLI 可跑并写 golden（`VERIFY_MCP.md` CLI 段；`main.gd` `--capture_golden`）。**无** `user-godot-tomyud1` 对 lake-echo 的 `get_errors=0` 日志。Verifier-v2 明示 MCP 未用。 |
| 2 | 六区可辨认地标 + 相对位置与总览一致 | **PARTIAL** | 拓扑：`world.gd` ZONES + `00_overview.png` 与 frame_01 象限粗一致（SW 农场 / 西河 / 中镇 / NE 站 / 东梯田 / SE 湖）。地标可「认出类别」但质量为色块剪影，**不可**按 §0 地标标准视为达标。 |
| 3 | TileMap 架构；整数相机缩放；YSort | **PASS** | `world.gd` TileMapLayer Ground/Water；`player.tscn` / `main.gd` `zoom=(2,2)`；`world.tscn` Entities/Decor `y_sort_enabled=true`。禁止项「每格 Sprite 铺地」未用于主世界。 |
| 4 | Z1 农场玩法；至少一栋可进室内 | **PASS**（代码） / **PARTIAL**（验收证据） | `farm_plots.gd` + player Space 锄地；`interact_zone` mode=house → `GameBus.enter_house`；`scenes/house_interior.tscn` 存在床/箱/出口。缺 MCP 锄地断言与室内 golden。 |
| 5 | `VERIFY_MCP.md` R5 全过；`ACCEPTANCE.md` 每行有证据 | **FAIL** | VERIFY 首选 MCP 清单未执行；ACCEPTANCE 多行 PARTIAL/FAIL/NO；无「金图 vs 参考帧」逐区对照表。 |
| 6 | 多 Agent handoff 六区齐全；Critic PASS | **FAIL** | 无 z1–z6（或等价六区证据卡）；本 Critic **整体 FAIL**。 |
| 7 | 已推 GitHub | **FAIL** | densify 后 golden/props/scripts/handoffs 仍 dirty/untracked；`origin/main` 未含本轮终态。 |

### 「一比一」锁定维度（Goal §0）

| 维度 | 判定 | 证据要点 |
|------|------|----------|
| 拓扑 | **PASS**（粗） | 六区相对方位与蓝图/frame_01 一致 |
| 地标 | **FAIL** | 谷仓/灯塔/火车等为色块剪影（`prop_*.png` + golden 04/06）；瀑布/站台/半木构屋细节不足 |
| 风格 | **FAIL** | 条纹草、硬直角岸、少 8 向过渡；烟/涟漪仅为 CPUParticles 点缀，非参考帧像素氛围 |
| 密度 | **FAIL** | `00_overview` / `05_terrace` / `06_lake` 大片空 tile；frame_01 树屋栅栏作物填满 → 数量级差距 |
| 玩法 | **PASS**（代码层） | WASD、Z1 农事、进屋床箱、中文 UI/toast 线路在 |

### 禁止偷懒抽查（Goal §5）

| 禁令 | 判定 |
|------|------|
| 禁止旧 farm-demo Sprite 铺地扩一扩 | **遵守** — 新 `lake-echo` TileMap |
| 禁止单张背景大图当世界 | **遵守** |
| 禁止火车站/灯塔色块占位算完成 | **违规** — `prop_train.png` / `prop_lighthouse.png` + golden 04/06 |
| 禁止 Verifier 只查坐标不截图对比参考帧 | **部分遵守** — 有 golden；Verifier-v2 承认 visual FAIL，但缺正式对照表 |
| 禁止 Asset 跳过棋盘格 QA | **遵守（形式）** — `assets/qa/checker_*.png` 存在；不代表美术达标 |
| 禁止六区未齐宣称一比一 | **勿宣称** |
| 禁止主对话一人包办无六区 handoff | **违规** — 无 z1–z6 handoff |
| 禁止未推 GitHub 宣称完成 | **勿宣称** |

### Forbidden-claim checklist（用户审计要点）

| 禁止宣称项 | Critic 判定 |
|------------|-------------|
| Sprite-per-tile ground 冒充重建 | **未犯**（主世界 TileMapLayer） |
| Big BG fake map | **未犯** |
| Color-block landmarks as “done” | **犯** — 若以此关 Goal 即违规 |

### Top 5 blockers（关 Goal 前必须清）

1. **密度未接近 `docs/ref/frame_01.png`** — golden 空草/空水/空梯田带 vs 参考帧密植被/密建筑（主阻塞）。
2. **地标资产仍是色块占位** — barn / farmhouse / lighthouse / train 等扁平几何块，直接违反 §5。
3. **Z5 梯田不是参考拓扑** — 水平土条 ≠ 石墙分层崖+作物行（`05_terrace.png`）。
4. **MCP 未 Connected 到 lake-echo** — `VERIFY_MCP.md` 首选清单无证据；CLI 不能替代 DoD1/5 的 MCP 要求。
5. **流程工件缺口** — 无六区 handoff；ACCEPTANCE/VERIFY 未全 PASS；densify 终态未 commit/push。

### Acceptance（本 Critic）
- [x] 对 Goal §4 七项给出 PASS / PARTIAL / FAIL + 证据路径
- [x] 视觉一比一与密度严厉判定（相对 densify 后仍 FAIL）
- [x] 列出 Top 5 blockers
- [x] 产出本文件
- [ ] Critic 整体 PASS ← **未勾选**
- [ ] 建议关 Goal ← **否**

### Open Questions
- **BLOCKER:** 「密度接近 frame_01」的可量化门槛（每屏 decor 数 / 空白 tile 占比）仍未写进规格，否则下轮仍可橡皮图章。
- **BLOCKER:** Asset 是否允许继续用 `gen_landmarks.py` 色块，还是必须换高保真像素剪影（至少达「可辨认细节」）。
- MCP 改接 lake-echo 后是否重采 golden（与 CLI 像素一致性）。

### Risks
- Conductor 若因「六区标签 + TileMap + 能锄地」关 Goal → 违反 §0/§4/§5。
- densify 未入库：本地金图与 GitHub 分叉，复审证据易丢。
- `decor.gd` 自称 Dense、金图仍空 → 文档/代码命名会误导后续 Agent 偷懒勾选。

### Suggested Next Agent
**Asset（重做地标像素，禁止色块）‖ Builder（有机路径 + Z5 真分层 + 密化）** → **Verifier-Full（MCP Connected lake-echo，逐区 vs frame 对照表）** → **Critic v3**。  
并行：补 z1–z6 handoff + commit/push。

### Required Output（下一 Agent）
1. 新 landmark/tileset 非色块资产 + checker QA
2. 新 `golden_r5` + 书面对照表（每区：金图 | 参考帧 | 差异）
3. MCP `get_errors=0` + 锄地/进屋运行时证据
4. `ACCEPTANCE.md` 无 FAIL/NO；六区 handoff 齐全
5. push 后再请 Critic

### Do-Not
- 禁止因 densify「比 Wave0 好看」就把视觉 DoD 标 PASS
- 禁止用更多同款色块 NPC/树刷屏冒充接近 frame_01
- 禁止只改 ACCEPTANCE 勾选不改美术
- 禁止在 MCP 未接 lake-echo 时伪造 get_errors=0
- 禁止未 push 终态就关 Goal

### Related Files
- `docs/GOAL_R5_ONE_TO_ONE_REMAKE.md`
- `docs/ACCEPTANCE.md` · `docs/VERIFY_MCP.md`
- `assets/qa/golden_r5/00_overview.png` … `06_lake.png`
- `docs/ref/frame_01.png`
- `scripts/world.gd` · `landmarks.gd` · `decor.gd` · `farm_plots.gd`
- `scenes/house_interior.tscn`
- `docs/handoffs/2026-09-06-builder-lake-echo-density.md`
- `docs/handoffs/2026-09-06-verifier-lake-echo-golden-v2.md`

---

## Verdict（给 Conductor / 用户）

**Goal 不能关闭。**

| 项 | 结论 |
|----|------|
| Critic 整体 | **FAIL** |
| 架构骨架 | TileMap 192×128 + zoom=2 + YSort → **PASS** |
| 玩法骨架 | Z1 农事 + 农舍室内 → **PASS**（证据仍 PARTIAL） |
| 视觉一比一 / 密度 | **FAIL**（densify 后仍远低于 `frame_01`） |
| 色块地标禁令 | **违规** |
| 关 Goal 前置 | 清 Top 5 blockers → Verifier-Full → Critic PASS → push |
