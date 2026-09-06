# GOAL — Farm_Demo Round3：画面整洁 + 方向正确 + 房屋有用 + 地图扩大

**Goal ID:** `farm-demo-r3-polish-expand`  
**工程:** `projects/06-game-factory/Farm_Demo/farm-demo/`  
**Playbook 基线:** `PB-Game-Visual` + 玩法扩展（种地环已存在）  
**团队协议:** Agent Team v2 + `docs/handoff-v2.md`  
**tools_allowed:** `code` · `mcp` · `image` · `shell` · `publish`  
**引擎:** Godot 4.6 · MCP `user-godot-tomyud1`（必须 Connected 到本工程）

---

## 0. 为何开这个 Goal（现状证据）

### MCP 基线（本对话刚跑）

| 检查 | 结果 |
|------|------|
| `run_scene(main.tscn, wait_for_runtime)` | OK · runtime `/root/Main` |
| `get_errors` | **0** |
| 起点 `Player.global_position` | `(128, 288)` |
| `move_up` 后 | `(128, 135)` · `animation=idle_up` |
| 截图 | `assets/qa/screenshot_goal_baseline.png` |

### 用户痛点（必须解决）

1. **画面乱**：粉边/红线伪影、地砖硬切、元素堆叠无层次感  
2. **人物方向**：四向虽有，但观感/朝向/工具交互朝向仍不清晰可靠  
3. **房子无作用**：目前仅装饰 Sprite，无进入/睡眠占位/箱子联动叙事空间  
4. **地图偏小**：需扩大为可探索的多分区世界（仍单场景或分区加载二选一，本 Goal 锁定见下）

### 网研：Agent 在 Godot 中如何验收（决策依据）

来源摘要（2025–2026 MCP/Agent 实践）：

| 模式 | 要点 | 对本 Goal 的启示 |
|------|------|------------------|
| **Observe→Interact→Assert 环**（godot-interactive / agent-loop） | `run` → screenshot → `query_runtime` → `send_input` → 再 screenshot | Verifier **禁止只口述**；每验收项至少 1 条 runtime/截图证据 |
| **Runtime assert 族**（Breakpoint MCP） | 断言节点属性、场景结构、屏上文字、性能基线、截图 diff | 把「方向对不对」写成可断言：`animation` 名 + `position` 变化方向 |
| **Visual regression**（mcp-bridge / agent-loop） | `compare_screenshots` / baseline diff | Round3 要存 **golden** 截图：四向各一、进屋前后、扩图总览 |
| **独立验证**（agent-loop `verify_project`） | Builder 与 Verifier 分离；测试跑完才算完 | 严格执行 Team v2：Builder 不自证「好看」 |

本仓可用 MCP 子集（已接线）：`run_scene` / `stop_scene` / `get_errors` / `send_input` / `wait` / `query_runtime_node` / `call_method` / `take_screenshot` / `rescan_filesystem`。

---

## 1. Goal 完成定义（Definition of Done）

全部满足才可关闭 Goal：

1. **画面整洁**  
   - 关键角色/树/屋/动物无可见粉/洋红不透明底  
   - 河岸/耕地/草地有过渡砖，无明显错误贴错（红线伪影清除或替换）  
   - 相机 **整数缩放**（nearest），像素不糊  

2. **方向系统正确**  
   - WASD 四向：`walk_*` / `idle_*` 与位移轴一致（MCP 断言）  
   - 工具/交互目标格 = **facing 方向** 下一格（锄地可见朝向正确）  
   - NPC/动物朝向与移动一致（侧视 strip + flip 可接受）  

3. **房屋有玩法作用（无剧情长文）**  
   - 农舍可 **靠近提示 → E 进入室内场景**（或室内子场景）  
   - 室内至少：床（E 提示「休息」toast，不实现昼夜）、箱子（与室外箱子逻辑一致或共享）、出门  
   - 禁止房子仅装饰  

4. **地图扩大**  
   - 世界尺寸 ≥ **96×64 tiles**（现 56×40）或等价像素面积 ≥ 约 2×  
   - 分区清晰：农场 / 河流 / 北山 / 村口广场 / **东侧林地或南侧牧场** 至少 +1 新区  
   - 相机 limit 跟随新世界；玩家不可走出边界  

5. **MCP 验收包**  
   - 更新 `docs/VERIFY_MCP.md` 为 Round3 清单（含四向、进屋、扩图）  
   - `docs/ACCEPTANCE.md` 全表 PASS 且每行有证据路径  
   - golden 截图目录：`assets/qa/golden_r3/`  

6. **交付**  
   - 代码进 `Farm_Demo/farm-demo`  
   - 推 GitHub  
   - 子 Agent Critic/Verifier handoff 各一份  

---

## 2. 锁定决策（新对话勿再 grill 翻案，除非用户改）

| 项 | 锁定 |
|----|------|
| 视角 | 俯视 2D（保持） |
| 地图 | **单主场景扩大**（暂不做多场景流式加载）；室内用 **独立 scene + 传送** |
| 房屋 | 农舍可进；床=休息 toast；不做昼夜数值 |
| 美术 | AI 像素 + 品红/玫红色键；`PIXEL_PROMPT_SKILL.md` |
| 验收 | **强制 MCP**；无证据不算完成 |
| 语言 | 中文 UI |

---

## 3. 多团队 Agent 编排（Goal 模式执行顺序）

```text
Conductor
  ├─ Scout        工程/MCP 现状盘点
  ├─ Researcher   （可选）autotile/粉边处理补充证据
  ├─ Game         扩图规格 + 房屋交互规格 + 方向状态机规格
  ├─ Asset ‖      清边/重生过渡砖/室内 tiles + 棋盘格 QA
  ├─ Builder ‖    地图扩大、进屋场景、方向修复、相机整数缩放
  ├─ Verifier     MCP 全环证据包
  ├─ Critic       对照本 Goal DoD / 禁止偷懒
  └─ Memory?      仅沉淀可复用规律（粉边键、VERIFY 模板）
```

`‖` = 可并行（同一 `parallel_group: farm-r3`），汇合前 Conductor 检查冲突。

### 角色任务卡（Handoff 摘要）

#### A. Scout
- **Objective:** 列出当前场景树、地图尺寸、房屋节点、方向动画名、已知粉边资产路径  
- **Acceptance:** 产出 `docs/handoffs/2026-xx-xx-scout-farm-r3.md`  
- **Do-Not:** 禁止改玩法代码  

#### B. Game
- **Objective:** 写出扩图分区坐标表 + 房屋状态机（Door→Indoor→Exit）+ 四向断言表  
- **Required Output:** `docs/specs/R3_WORLD_AND_HOUSE.md`  
- **Do-Not:** 禁止只写空话不写坐标/节点名  

#### C. Asset
- **Objective:** 清除粉边；必要时重生河岸/屋/树；室内地板墙门床素材；棋盘格 QA  
- **Evidence:** `assets/qa/checker_*` + 无热粉像素抽样脚本报告  
- **Do-Not:** 禁止跳过色键；禁止鸡人同高回退  

#### D. Builder
- **Objective:** 实现地图扩大、室内场景、传送、方向/相机修复、房子交互  
- **Related:** `farm_field.gd` `world.gd` `player.gd` `scenes/*`  
- **Do-Not:** 禁止把室内 UI 塞进主 HUD 一团；禁止无碰撞的假门  

#### E. Verifier（强制 MCP）
执行环（必须按序）：

```text
1. get_godot_status → project_path 必须含 Farm_Demo/farm-demo
2. run_scene(res://scenes/main.tscn, wait_for_runtime=true)
3. get_errors → 0 fatal
4. 四向：对 move_up/down/left/right 各 press→wait→release
   断言：position 轴变化方向正确 + animation 为 walk_* 或结束后 idle_*
5. 走到农舍门：prompt 非空 → try_interact / E → 室内场景或室内节点可见
6. 室内 E 床 → toast；E 出门 → 回到室外坐标合理
7. 扩图：走到原地图外新区，position 超出旧 56×40 范围仍有效
8. take_screenshot → assets/qa/golden_r3/*.png（≥5 张）
9. stop_scene
10. 填写 ACCEPTANCE + VERIFY_MCP
```

- **Do-Not:** 禁止无截图宣称画面 OK；禁止在 cursor-demo 工程上跑本清单  

#### F. Critic
- 对照本节 DoD 与禁止偷懒；输出 PASS/FAIL 表  

---

## 4. 禁止偷懒（Goal 级，执行 Agent 必读）

1. 禁止无 MCP runtime/截图证据结案  
2. 禁止房子继续只做装饰 Sprite  
3. 禁止地图只加空草地不分区  
4. 禁止四向只改 `flip_h` 假装有上下帧（本仓已有 4 行 atlas，必须用对）  
5. 禁止跳过粉边/棋盘格 QA  
6. 禁止把室内所有控件堆进主场景一个 CanvasLayer 应付  
7. 禁止伪造「扩图」却不改相机 limit / 边界钳制  
8. 禁止 Verifier 与 Builder 同一人自说自话无 handoff  

---

## 5. 建议工作分解（实现侧 checklist）

### P0 — 方向与画面
- [ ] 抽样 `processed/*.png` 热粉像素 = 0；失败则重跑 import chroma  
- [ ] Player：确认 atlas 行序 down/left/right/up 与 `_dir_name_from_vec` 一致  
- [ ] 相机：`zoom` 改为整数倍（如 `2,2` 或 `3,3`）+ 文档说明  
- [ ] 过渡砖：修错误映射导致的红线；必要时只在邻接带使用  

### P1 — 房屋
- [ ] `scenes/house_interior.tscn` + `scripts/door_zone.gd` / `scripts/interior.gd`  
- [ ] 门外 Area2D 提示「按 E 进屋」  
- [ ] 室内：床、箱、门；传送回室外固定点  

### P2 — 扩图
- [ ] `W,H` → ≥96×64；更新河道路径、村口、新区装饰与碰撞  
- [ ] 更新 `player` clamp 与 `Camera2D.limit_*`  
- [ ] 新区至少一种可交互（钓鱼点 / 砍树点 / NPC）  

### P3 — 验收文档
- [ ] `docs/VERIFY_MCP.md` Round3  
- [ ] `docs/ACCEPTANCE.md`  
- [ ] `docs/specs/R3_WORLD_AND_HOUSE.md`  
- [ ] push GitHub  

---

## 6. 新对话 Goal 模式启动提示词（可复制）

```text
按 Agent Team v2 执行 Goal：
文件：projects/06-game-factory/Farm_Demo/farm-demo/docs/GOAL_R3_POLISH_EXPAND.md

强制：
1) Godot MCP 必须 Connected 到 Farm_Demo/farm-demo
2) 先 Scout 再 Game 规格，再 Asset‖Builder，再 Verifier MCP 全环，再 Critic
3) 交接一律 handoff-v2；Evidence 空 = 未完成
4) 完成 DoD：画面整洁、四向断言、农舍可进可用、地图≥96×64、golden_r3 截图、推 GitHub

禁止偷懒清单见该文档第 4 节。
```

---

## 7. 风险

| 风险 | 缓解 |
|------|------|
| AI 过渡砖质量差导致更乱 | 失败则回退基础砖 + 仅河岸 dirt 带 |
| 室内场景切换丢 MCP runtime | Verifier 分两段 run_scene（室外/室内） |
| 扩图性能（每格 Sprite） | 分区绘制或 TileMapLayer；Builder 需测 FPS monitor |
| 方向行序与生成图不一致 | Scout 用 checker_player 人工确认行含义 |

---

## 8. 非目标（本 Goal 不做）

- 昼夜循环 / 存档 / 商店经济 / 剧情任务线  
- 换引擎或换 MCP 插件品牌（沿用现有 godot_mcp）  
- 全屏多场景流式大世界  
