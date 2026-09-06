## TASK HANDOFF v2

### Meta
- handoff_id: 2026-09-06-critic-lake-echo-r5
- playbook: PB-Game-Visual
- from_agent: Critic
- to_agent: Conductor
- parallel_group: none

### Objective
对照 `GOAL_R5_ONE_TO_ONE_REMAKE.md` §4 Definition of Done 与 §0「一比一」锁定定义，对 Lake Echo R5 给出诚实 PASS/FAIL；判定 Goal 能否关闭。

### Context
- Goal ID: `farm-demo-r5-one-to-one-remake`
- 参考总览: `docs/ref/frame_01.png`（dense 像素村落：谷仓群、市集、车站、梯田、Lake Echo）
- 当前金图: `assets/qa/golden_r5/00_overview` … `06_lake.png`（CLI `--capture_golden`）
- prior: `2026-09-06-builder-lake-echo-w0` · `2026-09-06-verifier-lake-echo-golden`
- 已知事实：Verifier 自认「visual density matches reference video = FAIL」；MCP tomyud1 仍指向旧 `farm-demo`

### Inputs
- paths:
  - `docs/GOAL_R5_ONE_TO_ONE_REMAKE.md`
  - `docs/ACCEPTANCE.md` · `docs/VERIFY_MCP.md`
  - `scripts/world.gd` · `landmarks.gd` · `decor.gd` · `farm_plots.gd` · `main.gd`
  - `scenes/world.tscn` · `house_interior.tscn`
  - `assets/qa/golden_r5/*.png`
  - `docs/ref/frame_01.png` · `frame_10.png`
- prior_handoff_ids: [2026-09-06-builder-lake-echo-w0, 2026-09-06-verifier-lake-echo-golden]
- tools_allowed: [code]（本 Critic 只读）

### Completed
- 读完 Goal DoD / 禁止偷懒清单
- 检查 TileMap 世界、地标、装饰、农田、室内场景接线
- 目视对比 golden_r5（00/01/02/03/04/06）与 frame_01 / frame_10
- 核对 ACCEPTANCE / VERIFY_MCP / handoffs 覆盖度 / git 推送状态

### Evidence
| 类型 | 路径或摘要 | 结果 |
|------|------------|------|
| screenshot | `assets/qa/golden_r5/00_overview.png` | 大面积纯色草+灰石板格；几乎无地标密度 → 相对 frame_01 **FAIL** |
| screenshot | `assets/qa/golden_r5/01_farm.png` | 农舍/筒仓可辨，但大块平涂土、无成排田与畜栏密度 → **PARTIAL** 拓扑 / **FAIL** 密度 |
| screenshot | `assets/qa/golden_r5/02_river.png` | 弯河+木桥色块可走感，无瀑布特写与岸边过渡美术 → **PARTIAL** |
| screenshot | `assets/qa/golden_r5/03_town.png` | 石板广场+4 条纹摊位；屋/雕像常不在镜头；无 NPC 漫游 → **PARTIAL** 骨架 / **FAIL** 密度 |
| screenshot | `assets/qa/golden_r5/04_station.png` | 铁轨+极简火车块；站房细节弱 → **PARTIAL**（剪影级，触碰「禁止色块占位」红线） |
| screenshot | `assets/qa/golden_r5/06_lake.png` vs `docs/ref/frame_10.png` | 灯塔条纹剪影+码头条；无船/涟漪/烟/岸边建筑密度 → **FAIL** 视觉一比一 |
| code | `world.gd` TileMapLayer Ground/Water；W=192 H=128；zoom=2 | **PASS** 架构 |
| code | `landmarks.gd` 六区道具点位；`decor.gd` 树/花/门 | 有点位但稀疏 → 密度 **FAIL** |
| code | `farm_plots.gd` + `main.tscn` FarmPlots；`house_interior.tscn` + GameBus | 玩法/进屋实现存在 → **PASS**（缺 MCP 锄地断言） |
| docs | `ACCEPTANCE.md` Wave3–6 PARTIAL；golden PENDING | 未全行闭环 → **FAIL** DoD5 |
| docs | `VERIFY_MCP.md` 仅 Wave0；MCP 未接到 lake-echo | 清单未全过 → **FAIL** DoD5 |
| handoff | 仅 W0 Builder + Verifier golden；无 z1–z6 分 Wave handoff | **FAIL** DoD6 |
| git | `main` 与 `origin/main` 同步；但 golden_r5 / decor / house_interior 等大量 **未提交** | Goal 终态未入库 → **FAIL** DoD7 |

### Definition of Done — 逐项判定（§4）

| # | DoD 项 | 判定 | 说明 |
|---|--------|------|------|
| 1 | `lake-echo/` 可 F5；MCP `get_errors=0` | **PARTIAL** | CLI 可跑并产出金图；Verifier 写明 MCP 仍连旧工程，**无** tomyud1 `get_errors=0` 证据 |
| 2 | 六区可辨认地标 + 相对位置与总览一致 | **PARTIAL** | Zone 矩形拓扑（SW 农场 / 西河 / 中镇 / NE 站 / 东梯田 / SE 湖）合理；地标多为稀疏剪影，**远未**接近 frame_01 可辨认细节与密度 |
| 3 | TileMap 架构；整数相机缩放；YSort | **PASS** | `TileMapLayer` 铺地；非每格 Sprite 世界；`zoom=(2,2)`；Entities/Decor `y_sort_enabled` |
| 4 | Z1 农场玩法；至少一栋可进室内 | **PASS**（实现） / **PARTIAL**（证据） | `farm_plots` 锄浇种收 + 农舍门/`house_interior` 床箱出口存在；缺 MCP 锄地截图断言与室内金图 |
| 5 | `VERIFY_MCP.md` 全过；`ACCEPTANCE.md` 每行有证据 | **FAIL** | VERIFY 只有 Wave0；ACCEPTANCE 自标 PARTIAL/PENDING；无分区 vs 参考帧对照记录 |
| 6 | 六区 handoff 齐全；Critic PASS | **FAIL** | 缺 z1–z6 handoff；本 Critic **整体不 PASS** |
| 7 | 已推 GitHub | **FAIL** | 远程有 Wave0/W1 旧提交，但 golden、decor、室内、本 Critic 文档等 Goal 关键工件仍 untracked/未推 |

### 「一比一」锁定维度（§0）— Critic 摘要

| 维度 | 判定 | 证据要点 |
|------|------|----------|
| 拓扑 | **PASS**（粗） | 六 Zone 相对方位与蓝图/frame_01 象限一致 |
| 地标 | **PARTIAL** | 谷仓/灯塔/桥/火车「有」；瀑布/站台/半木构屋细节不足；触碰「禁止 16×16 色块占位」风险（火车/站房） |
| 风格 | **FAIL** | 平涂 tile、少岸边 8 向过渡、无烟囱烟/涟漪；非参考帧 3/4 密集像素观感 |
| 密度 | **FAIL** | golden 大片空草/空土/空湖；frame_01/10 树屋 NPC 栅栏作物填满 → 差距数量级 |
| 玩法 | **PASS**（代码层） | WASD、Z1 农事、进屋床箱、中文 toast/UI 线路在 |

### 禁止偷懒清单抽查（§5）

| 禁令 | 现状 |
|------|------|
| 禁止旧 farm-demo Sprite 铺地扩一扩 | **遵守** — 新 `lake-echo` TileMap |
| 禁止单张背景大图当世界 | **遵守** |
| 禁止火车站/灯塔纯色块占位 | **违规风险** — 金图中火车为极简块；灯塔有条纹但仍属剪影级 |
| 禁止 Verifier 只查坐标不截图 | **部分遵守** — 有 golden，但缺「对照参考帧」书面对比 |
| 禁止 Asset 跳过棋盘格 QA | **部分遵守** — `assets/qa/checker_*.png` 存在 |
| 禁止六区未齐宣称一比一 | **勿宣称** — Critic 禁止关 Goal |
| 禁止主对话一人包办无 handoff | **违规** — 缺六区 handoff |
| 禁止未推 GitHub 宣称完成 | **勿宣称** — 终态未推 |

### Acceptance（本 Critic）
- [x] 对 Goal §4 七项给出 PASS/FAIL/PARTIAL（不橡皮图章）
- [x] 视觉一比一明确标 FAIL/PARTIAL，并指出密度为关 Goal 主阻塞
- [x] 产出本 handoff 路径
- [ ] Critic 整体 PASS ← **未勾选**
- [ ] 建议关 Goal ← **否**

### Open Questions
- **BLOCKER:** 美术密度与参考视频/frame 对齐标准（模块化 tileset 拼装到何密度才算 §0「接近」）未量化
- **BLOCKER:** MCP 必须改接到 `lake-echo` 后重跑 VERIFY 全清单
- Wave7 动效（烟/水）与地名标签美术化仍未做
- 室内场景用逐格 Sprite 铺地板（可接受作室内例外，但与「禁止每格 Sprite 世界」精神需在规格里写明）

### Risks
- 若 Conductor 因「能跑 + 有六区标签」关 Goal → 直接违反 Goal「禁止宣称一比一」与 DoD 全满足条款
- 未提交的 decor/室内/golden 易丢；本地与 GitHub 终态不一致
- 金图 zoom=2 视野窄，00_overview 不能代表全图；需另做缩小总览或拼接证据，否则拓扑验收易误判

### Suggested Next Agent
**Asset ‖ Builder（Wave7 densify）** → 对照 frame_01/03/05/07/10 按区补树/屋变体/栅栏/作物行/船/涟漪/烟；然后 **Verifier-Full**（MCP 接 lake-echo）→ 再开 Critic。

### Required Output（下一 Agent）
1. 分区美术密度补齐 + 新 golden_r5 对照表（每区：金图路径 | 参考帧 | 差异笔记）
2. 补齐 `docs/handoffs/*-z1`…`z6`（或合并为完整 Wave handoff 但须覆盖六区证据）
3. 更新 `ACCEPTANCE.md` / `VERIFY_MCP.md` 至无 PENDING
4. commit + push 后再请 Critic 复审

### Do-Not
- 禁止因「骨架能跑」把视觉 DoD 标 PASS
- 禁止跳过密度补齐只改文档勾选
- 禁止在 MCP 未接 lake-echo 时伪造 get_errors=0
- 禁止宣称与视频逐像素相同
- 禁止未 push 终态就关 Goal

### Related Files
- `docs/GOAL_R5_ONE_TO_ONE_REMAKE.md`
- `docs/ACCEPTANCE.md` · `docs/VERIFY_MCP.md`
- `assets/qa/golden_r5/00_overview.png` … `06_lake.png`
- `docs/ref/frame_01.png` · `frame_10.png`
- `scripts/world.gd` · `landmarks.gd` · `decor.gd` · `farm_plots.gd`
- `scenes/house_interior.tscn`

---

## Verdict（给 Conductor / 用户）

**Goal 不能关闭。**

- 整体 Critic：**FAIL**
- 架构/玩法骨架：可用（TileMap + WASD + Z1 农事 + 进屋）
- 相对参考视频/frame 的视觉一比一：**FAIL**（密度与风格是主缺口；地标多为 PARTIAL 剪影）
- 关 Goal 前置：美术密化 → MCP 全量 VERIFY → 六区 handoff → ACCEPTANCE 无 PENDING → push → Critic 复审 PASS
