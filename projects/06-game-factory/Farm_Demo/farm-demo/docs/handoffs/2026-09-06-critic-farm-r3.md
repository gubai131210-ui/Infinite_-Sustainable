# Critic — Farm_Demo R3

**handoff_id:** 2026-09-06-critic-farm-r3  
**from:** Critic → Conductor  
**date:** 2026-09-06  
**against:** `docs/GOAL_R3_POLISH_EXPAND.md` §1 DoD

## 1. DoD PASS/FAIL

| DoD | 判定 | 证据 / 缺口 |
|-----|------|-------------|
| 1. 画面整洁（无热粉；河岸过渡；整数 zoom） | **PASS** | 关键资产抽样 `player/tree/house/chicken` hotpink≈0；`_display_tex` 仅 `gw_*`（停用 gd 红线）；`main.gd`/`house_interior.gd` `zoom=(2,2)`；golden `01`/`03` 目视无粉边 |
| 2. 方向系统正确 | **PASS** | `VERIFY_MCP.md` 2026-09-06 复验表：四向 `walk_*` + facing + 位移轴；`player.gd` atlas 行序 down/left/right/up，工具格=`facing` 下一格；动物 `flip_h`（DoD 允许） |
| 3. 房屋可进可用 | **PASS** | `scenes/house_interior.tscn` Bed/Chest/Exit；`interact_zone` house/bed/exit_house；`game_bus` 换景；golden `02` 含休息 toast +「离开农舍」 |
| 4. 地图 ≥96×64 + 新区 | **PASS** | `farm_field.gd` `W=96 H=64` → `world_size=(1536,1024)`；南牧场 + 东林地；相机 limit + player clamp；golden `03` y≈797 |
| 5. MCP 验收包 | **PASS** | `VERIFY_MCP.md` 含 2026-09-06 复验表；`ACCEPTANCE.md` 全 PASS；`assets/qa/golden_r3/` 5 png；Verifier handoff 存在 |
| 6. 交付（代码 + GitHub push + Critic/Verifier handoff） | **FAIL（仅 push）** | 代码与 handoff 齐；`main` **ahead 1** of `origin/main`（`074d3d1`）；另有未提交的 golden/ACCEPTANCE/VERIFY 复验改动。**已知网络阻塞，本 Critic 不执行 push** |

## 2. 偷懒 / 表面工作

| 项 | 严重度 | 说明 |
|----|--------|------|
| 进屋验收走 `GameBus.enter_house` 捷径 | 低 | 门区 `FarmHouseDoor` 代码真实存在；未强制「走到门→E」完整输入环 |
| golden `04`/`05` 命名 vs 构图 | 低 | 均在牧场坐标附近；四向以 runtime 表为准，截图侧证偏弱 |
| 过渡砖非完整 bitmask | 低（已声明） | 启发式 gw 邻接；可接受，非假扩图 |
| 室内床视觉偏简 | 低 | 功能（toast）达标；美术可后续 polish |
| Scout handoff 仍写 56×40 | n/a | 开工前快照，不扣分 |

未发现：假门无碰撞、纯装饰屋、空草地假扩图、仅 `flip_h` 冒充四向、无截图结案。

## 3. Goal 可否关闭

**功能 DoD 可关；交付 DoD 仅剩 GitHub push。**

网络恢复后 Conductor 应：

1. 纳入未提交的 `golden_r3/02`/`03` + `ACCEPTANCE.md` + `VERIFY_MCP.md`（若需）并 commit  
2. `git push origin main`  
3. 确认 `main` 与 `origin/main` 对齐后再标 Goal Closed

## 4. 结论

**PASS（待 push）** — 与 DoD 功能项一致；**唯一阻断 = GitHub push（网络已知阻塞）**。
