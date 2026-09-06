# Critic — Farm_Demo R4

**handoff_id:** 2026-09-06-critic-farm-r4  
**from:** Critic → Conductor  
**date:** 2026-09-06  
**against:** `docs/specs/R4_VISUAL_AND_FACING.md` DoD（朝向修复 + 视频风农场+河+村口切片；禁止火车/灯塔全图）  
**inputs:** `ACCEPTANCE.md` · `VERIFY_MCP.md` · `assets/qa/golden_r4/` · `player.gd` / `farm_field.gd` / `world.gd` · `tools/r4_fix_assets.py` · Verifier handoff

## 1. DoD PASS/FAIL

| DoD | 判定 | 证据 / 缺口 |
|-----|------|-------------|
| A. 左右朝向契约（atlas 行序 + WASD + facing + 脸朝向截图） | **PASS** | `player.gd` `DIRS=["down","left","right","up"]`；`r4_fix_assets.fix_player_atlas` 对调 row1/2；QA `player_row_1_left` 面朝左、`player_row_2_right` 面朝右；`VERIFY_MCP`：`move_left` facing=(-1,0)+walk_left，`move_right` facing=(1,0)+walk_right；golden `05` 右脸清晰。**缺口：** golden `04_facing_left` 构图里玩家侧影易读成朝右（证据偏弱，不以 animation 名单独结案，靠 atlas QA + runtime facing 兜底） |
| B. 上下朝向 | **PASS** | `VERIFY_MCP` walk_up/down + facing y；golden `06_facing_up` 玩家背对镜头明确 |
| C. 视频风切片：西农田 + 弯河 + 农舍院 | **PASS** | `farm_field._build_grid`：FARMLAND(4–18,14–34)、sin 弯河+dirt 岸、院落 DIRT(34–44,18–28)、桥 PATH；golden `01`/`02` 可见农田+河+农舍；无火车/灯塔资产或布局 |
| D. 村口石板广场（path/石砖 + 摊位 + 2 屋） | **PASS** | `T.PLAZA` 核 + PATH 环；`world._spawn_props` 两屋 + 两 chest 摊位；golden `03_village_plaza` |
| E. 北崖/台阶 + 南牧场/东林（切片内） | **PASS** | HILL/CLIFF y0–10 + STAIRS 走廊 x10–13；南牧场 dirt 斑 + 畜；东林错落树（非整排复制） |
| F. 河岸 8 向 gw_* + 整数 zoom + nearest | **PASS** | `edge_tex` 含 gw_n/e/s/w + 四角；`main.gd`/`house_interior.gd` `zoom=(2,2)`；player/tiles `TEXTURE_FILTER_NEAREST` |
| G. 草地/砖无粉洋红缝（重生） | **PASS（残留）** | `r4_fix_assets` 程序化重铺 tile_* + scrub；golden 草地/广场目视无粉缝。**残留：** `player_row_*` QA 仍见品红描边晕（scrub 未尽），本机 F5 需再确认纹理缓存 |
| H. 农舍可进 + 床交互 | **PASS** | `FarmHouseDoor` mode=house；golden `07` 有「离开农舍」+ toast「休息了一会儿…」（床证据比 Verifier 同帧空读更强） |
| I. 地图 ≥96×64 + MCP 无致命错 | **PASS** | `W=96 H=64` → `world_size=(1536,1024)`；`VERIFY_MCP` get_errors=0 |
| J. Out-of-scope：不假装火车/灯塔/全镇 1:1 | **PASS** | 规格/ACCEPTANCE 勾选；代码与 golden 无相关内容；Verifier Residual 已声明 |
| K. 证据包入库 | **PASS（未 commit）** | `golden_r4/` 7 png；规格 `R4_VISUAL_AND_FACING.md`；`docs/ref/r4_video/`；Verifier handoff。工作区大量 R4 改动仍 **未提交** |

## 2. 偷懒 / 表面工作

| 项 | 严重度 | 说明 |
|----|--------|------|
| golden `04` 左向脸证据弱 | 中 | 文件名宣称 left，目视侧影易判右；未单列 `facing_down` golden（down 仅 runtime 表） |
| 进屋环仍可能走 `GameBus.enter_house` | 低 | 门区代码真实；未强制「走到门→E」输入环（同 R3） |
| 村口「摊位」= chest 道具 | 低 | 满足 1–2 摊位数量，非独立摊位美术 |
| 农舍院 x 起 34 非规格 32 | 低 | 与河弯避让，功能无影响 |
| 玩家品红描边残留 | 中（视觉） | 朝向已修，粉边 scrub 未清干净；勿宣称「全资产零粉」 |
| ACCEPTANCE 全 PASS 略乐观 | 低 | 与上两项残留不完全对齐，但不构成 DoD 功能 FAIL |

未发现：火车/灯塔假扩图、仅 animation 名结案左右、整排树复制、假门无脚本、空草地冒充新区。

## 3. Push 可否进行

**功能 DoD：可关（PASS）。Push：暂不可直接进行。**

阻断（流程，非功能）：

1. `main` 与 `origin/main` 对齐，但 R4 大量 **modified + untracked**（processed tiles/player、`golden_r4/`、`r4_fix_assets.py`、specs/ref、scripts、ACCEPTANCE/VERIFY、本 Critic handoff）尚未 commit。  
2. 本 Critic **不执行 push**（任务约束）。  
3. 建议 commit 范围：Farm_Demo R4 相关代码/资产/文档/golden；排除无关 `visual_capability_probe` 与 `.godot` 缓存。

Commit 后：Conductor 可 push；本机再 F5 确认 A/D 脸朝向与粉边。

## 4. 结论

**PASS（待 commit + push）** — 朝向契约与农场+河+村口切片达标；未越界做火车/灯塔全图。  
**唯一流程阻断 = 未提交的 R4 变更集（Critic 不 push）。** 可选 polish：重截 golden `04` 左脸特写、再 scrub 玩家品红边。
