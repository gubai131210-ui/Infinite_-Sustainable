# PB-Oakhaven-World

**用途：** Oakhaven / 类星露谷 **世界驱动** 地图与视觉（解决「素材拼接割裂」）。  
**证据强度：** 高（golden / MCP 截图 + `VISUAL_QA` 打分）  
**来源：** [ChatGPT share](https://chatgpt.com/share/6a9e585e-6e10-83ea-98fc-30457ff86eac)

## 链

```text
Conductor → Scout → (game-world-art-director Skill)
         → Game/Planner（REGION 模板）
         → Asset ‖ Map Composer ‖ Builder（分阶段，禁止一口气铺满）
         → Verifier（截图）→ Critic（VISUAL_QA）→ 返工
```

## 输入

- 工程：`projects/06-game-factory/perfect_game/perfect-game`
- `docs/GAME_VISION.md` + `WORLD_DESIGN.md` + `ART_DIRECTION.md`
- 参考：`docs/ref/oakhaven_overview.jpg`

## 验收

- [ ] 开工前有 REGION 模板（见 WORLD_DESIGN）
- [ ] 工作流非「找素材→铺 Tile→补草」
- [ ] 远景 / 游玩距 / 近景三档有截图证据
- [ ] `VISUAL_QA.md` 打分表填写；World Cohesion 有数字
- [ ] 若像贴图拼接：已 STOP 并改构图，而非加碎屑

## 禁止偷懒

- 禁止跳过 Macro 直接改 Micro  
- 禁止无截图宣称不割裂  
- 禁止一个 Agent 同时拍脑袋做「设计+素材+Godot」且无 handoff  
- 禁止用户 HOLD 期间擅自继续画面优化（除非用户下令）
