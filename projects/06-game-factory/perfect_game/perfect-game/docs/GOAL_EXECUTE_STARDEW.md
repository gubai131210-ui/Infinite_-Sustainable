# GOAL 执行说明书 — Oakhaven → 类星露谷水准

> **用法：** 新开 Cursor 对话，粘贴下方「启动提示词」，或执行：  
> `/goal` + 本文「目标原文」。  
> **工程根：** `projects/06-game-factory/perfect_game/perfect-game`  
> **参考图：** `docs/ref/oakhaven_overview.jpg`  
> **路由：** `docs/routing-table.md` · 交接：`docs/handoff-v2.md`

---

## 目标原文（粘贴到 CreateGoal / /goal）

将 perfect-game/Oakhaven 按仓库多 Agent 模式持续打磨到类星露谷水准：一致像素风格与行走/环境动画素材、丰富玩法与故事、人物设计完善；可下载或自生成素材但必须风格一致并兼容现有框架；每轮 Conductor→Scout/Game/Asset/Builder/Verifier/Critic 闭环；有不确定点先问用户；验收以参考图 `docs/ref/oakhaven_overview.jpg` + SPEC + 可玩竖切证据为准，直到 itch 级可发布动态农场生活 Demo 完成。

---

## 启动提示词（新对话第一条消息）

```text
/goal 将 perfect-game/Oakhaven 按仓库多 Agent 模式持续打磨到类星露谷水准：一致像素风格与行走/环境动画素材、丰富玩法与故事、人物设计完善；可下载或自生成素材但必须风格一致并兼容现有框架；每轮 Conductor→Scout/Game/Asset/Builder/Verifier/Critic 闭环；有不确定点先问用户；验收以参考图 docs/ref/oakhaven_overview.jpg + SPEC + 可玩竖切证据为准，直到 itch 级可发布动态农场生活 Demo 完成。

先读并遵守：
- projects/06-game-factory/perfect_game/perfect-game/docs/GOAL_EXECUTE_STARDEW.md（本文件）
- docs/VISUAL_BIBLE.md
- docs/SPEC.md
- docs/WAVE_ROADMAP.md
- 仓库 docs/routing-table.md + docs/handoff-v2.md

硬约束：
1. 不重写框架；在现有 world/farm_plots/GameBus/interiors/NPC 上扩展
2. 风格锁：像素、TS=16、camera zoom=2、中文 UI、暖色星露谷风
3. 素材：可 CC0 下载或 PIL/生图，必须过 Visual Bible 与 QA checker
4. 多 Agent：Conductor 编排；跨角色必须 handoff-v2；Verifier 要 runtime/截图证据；Critic 防偷懒
5. 有 BLOCKER 先问我，禁止擅自定剧情结局/商用授权/大范围删档

本轮先做 Wave 路线图中「当前 Wave」的下一未勾选项，禁止只写文档不交代码。
```

---

## 多 Agent 闭环（每 Wave 强制）

| 顺序 | 角色 | 载体 | 产出 |
|------|------|------|------|
| 1 | Conductor | 主对话 | Wave 目标 + Do-Not + 问清 BLOCKER |
| 2 | Scout | `explore` | 现有脚本/场景地图 |
| 3 | Game | `generalPurpose` | 玩法/故事增量设计（短） |
| 4 | Asset | 主对话 + 生图/下载/PIL | 风格一致素材 + `assets/qa/checker_*` |
| 5 | Builder | 主对话 | 接入 Godot、不破坏六区 |
| 6 | Verifier | Godot MCP / 用户 F5 | 日志或截图证据 |
| 7 | Critic | `generalPurpose` / Bugbot | PASS/PARTIAL + 返工清单 |
| 8 | Memory | 主对话 | 更新 WAVE_ROADMAP 勾选 + 推 GitHub |

交接一律 `docs/handoff-v2.md`。禁止主对话自称「我是全部 Agent」却无证据。

### 禁止偷懒（每轮至少写进 handoff Do-Not）

1. 禁止只改 README/SPEC 假装进度  
2. 禁止生成与 Visual Bible 冲突的素材却不写 QA  
3. 禁止无 runtime/截图宣称「动画/动感 OK」  
4. 禁止把 UI 控件堆进一个面板；新系统新场景/新页  
5. 禁止复制 Farm_Demo 后声称 Oakhaven 完成  
6. 禁止浮点货币做主经济；日夜/生长用 tick，不绑帧率  

---

## 外部经验 → 本仓落地（调研摘要）

| 来源 | 可复用点 | 本仓动作 |
|------|----------|----------|
| GDQuest 模块架构 | systems / content 单向依赖 | 新系统进 `scripts/systems/`，内容进 `content/` 或 Resource |
| Serfdom（Godot 农场） | signal 驱动 UI、CSV/Resource 物品、日夜、精力 | 扩展 GameBus 信号；ItemDB→Resource；加 TimeClock |
| gd-agentic-skills simulation | Tick Manager、整数货币、NPC schedule | 引入 `sim_tick`；金钱用 int；NPC 日程表 |
| Godot 农场教程共性 | TileMapLayer 动画水/作物、Y-sort、存档 | Water 层动画；全 Prop Y-sort；`user://` 存档 |
| pixel-asset-master / fairy-pixel | `spec_lock` + PIL 画像素而非乱生图 | 维护 `VISUAL_BIBLE.md`；优先 `tools/gen_*.py` |
| Chatforce 多 Agent | 共享 brief + 概念图锚点 | 本文件 + overview.jpg 为唯一艺术锚 |

参考链接（执行 Agent 需要时再打开）：

- https://www.gdquest.com/library/modular_game_architecture/  
- https://github.com/thedivergentai/gd-agentic-skills/blob/HEAD/skills/godot-genre-simulation/SKILL.md  
- https://github.com/424431185/pixel-asset-master-skills  
- https://github.com/dbinky/claude-fairy-pixel-art  

---

## 关闭条件（Goal Complete 审计清单）

仅当下列**每项**都有当前证据（文件/截图/日志/导出）才可 `UpdateGoal complete`：

- [ ] **视觉：** 六区 golden 截图接近 overview；风格锁通过 QA  
- [ ] **动感：** 玩家四向走、NPC/动物走、水/烟/树/火车等环境动效可观测  
- [ ] **玩法：** 日夜或等价时间轴；种地全环；商店买卖；至少 1 条任务线（≥5 步）  
- [ ] **故事：** ≥12 NPC 有日程或差异对话；主角人设文档 + 立绘/精灵一致  
- [ ] **建筑：** SPEC 可进建筑均可进且室内不丢农场状态  
- [ ] **素材管线：** Visual Bible + gen 脚本可复现关键道具  
- [ ] **发布：** Windows 导出步骤可跟做；已推 GitHub  
- [ ] **Critic：** 最近一轮对「类星露谷竖切」为 PASS 或仅剩已知非阻塞项  

未满足任一项 → **禁止**标记 Goal 完成。

---

## 当前基线（2026-09-06，供新对话 Scout）

已知已有：六区地图、种地、12 NPC、6 门、城镇/灯塔/站房升档、玩家 walk 表、动物 live scene、部分粒子。  
已知缺口：日夜/精力/商店经济、任务线、NPC 日程、作物动画瓦片、角色设计文档化、golden 截图、真正 itch 包装。

下一 Wave 见 `WAVE_ROADMAP.md`。
