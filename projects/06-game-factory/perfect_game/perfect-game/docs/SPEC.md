# SPEC — Paper Isle（纸片沙盘）MVP

**状态：Grill 锁定**  
**决策日：2026-09-06**

## Research Question → Decision

在 Godot MCP + Agent 生图/抠图管线下，选哪类游戏最能验证「无缝地形 + 纸片道具拼接」？  
→ **纸片沙盘俯视探索 + 收集**（非农场、非卡牌、非纯装修）。

## 已知事实

- 工程：`perfect-game`，Godot 4.6，已装 godot_mcp 插件
- rembg u2net 约定在 D 盘 probe 目录（见 `knowledge/godot/rembg-d-drive.md`）
- 外网共识：通用 AI 模型对无缝 tileset 最弱 → 必须有 **seamless 后处理 + 定量 seam QA**

## MVP 玩法边界

| 有 | 无（本轮禁止） |
|----|----------------|
| 可走沙盘岛（草地/小径/水域） | 种地/背包/NPC 对话树 |
| WASD 移动 + Camera2D | 序列帧四向动画（用静帧+镜像即可） |
| ≥5 纸星可收集，HUD 计数 | 战斗/合成/多关卡 |
| 道具：小屋、树、花丛（抠图叠放） | 完整 Wang 47 块手绘 |
| ≥2 地形过渡（草↔水 或 草↔径） | 等距 3D / 侧视平台 |

## 资产契约

| 资产 | 逻辑尺寸 | 说明 |
|------|----------|------|
| 地砖 | 64×64 | 无缝；atlas 入库 |
| 玩家 | 高 ≈ 48–64px | 品红底抠图 |
| 树 | 高 ≈ 96–128px | 明显高于人 |
| 小屋 | 宽 ≈ 96–140px | 可挡碰撞 |
| 纸星 | 32–40px | Area2D 拾取 |
| 花丛 | 40–56px | 装饰无碰撞 |

风格锁：paper-cut layered illustration / papercraft diorama / cream-mint-amber / 品红 `#FF00FF` 底。

## 无缝验收标准

1. `tools/seam_qa.py` 对每种基础地砖输出 `seam_score`（拼缝线平均绝对差）  
2. **PASS 阈值：seam_score ≤ 12.0**（0–255 色差均值）  
3. 必须生成 `assets/qa/seam_<name>_3x3.png` 供人眼看  
4. 运行时地图不得出现明显网格白缝/色条（Verifier 截图）

## Agent 链

```text
Conductor → Game(本 SPEC) → Asset(生图/seamless/抠图/QA)
         → Builder(场景/脚本) → Verifier(MCP 或本机截图) → Critic
```

## 禁止偷懒

- 禁止跳过 seam_qa 数值阈值
- 禁止只生成散图不接入 TileMapLayer
- 禁止把所有系统堆进一个 .gd
- 禁止用 Farm 像素绿幕管线冒充纸片风格而不改提示词/色板
- 禁止 MCP 未连时假装已有 runtime 截图证据（应降级为本机 F5 + qa 图）
