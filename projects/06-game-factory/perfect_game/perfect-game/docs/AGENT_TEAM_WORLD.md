# Oakhaven 多团队协作 — World-driven（入库版）

> 来源：[ChatGPT · Godot世界设计提示词](https://chatgpt.com/share/6a9e585e-6e10-83ea-98fc-30457ff86eac)  
> 映射到仓库 Agent Team v2（`docs/agent-team-v2.md` · `docs/routing-table.md`）

## 核心诊断

当前「割裂」主因不是不会写 Godot / 素材不够，而是流程仍偏 **Asset-driven Map**。  
目标改为 **World-driven Map**：先世界构图，再让 Tile/建筑/路/植被服务世界。

## 角色分工（语义）

```text
 WORLD ART DIRECTOR（世界视觉总监）  ← Skill: game-world-art-director
        ↓
 WORLD DESIGNER（世界地图设计）      ← docs/WORLD_DESIGN.md
        ↓
   ┌────┴────┐
   ↓         ↓
 ASSET       MAP COMPOSER
 DIRECTOR    （地图构图）
   ↓         ↓
 TILE        GODOT BUILDER
 SYSTEM      （实现）
        ↓
 VISUAL QA / Critic（截图打分）
```

| ChatGPT 角色 | 仓库映射 |
|--------------|----------|
| World Art Director | Skill `game-world-art-director` + Conductor 强制读取 `GAME_VISION` |
| World Designer | Game Agent + Planner（出区域模板） |
| Asset Director | Asset Agent |
| Map Composer | Game / Builder（构图规格，非堆瓦） |
| Tile System | Asset + Builder（`gen_tileset_*` / stitch） |
| Godot Builder | Builder |
| Visual QA | Verifier（截图）+ Critic（打分/`VISUAL_QA.md`） |

## 强制闭环（Oakhaven 视觉任务）

```text
Conductor
  → Scout（读 GAME_VISION + 对照 golden/ref）
  → World Art Director 规则检查（Skill）
  → Game/Planner（填 REGION 模板，禁止直接铺瓦）
  → Asset ‖ Map Composer ‖ Builder（按 WORLD_DESIGN 阶段）
  → Verifier（MCP 截图 / golden）
  → Critic（VISUAL_QA 打分；World Cohesion）
  → 返工按 ART_DIRECTION 优先级（禁止只堆碎屑）
```

Playbook：`docs/playbooks/PB-Oakhaven-World.md`（仓库根）+ 本目录文档。

## 必读清单（任何视觉改动）

1. `GAME_VISION.md`  
2. `WORLD_DESIGN.md`  
3. `ART_DIRECTION.md`  
4. Skill `game-world-art-director`  
5. `VISUAL_QA.md`  

## 当前状态：HOLD

**等用户命令再继续画面优化。**  
本轮只入库提示词 / Skill / 协作方式，不改玩法与地图实现。
