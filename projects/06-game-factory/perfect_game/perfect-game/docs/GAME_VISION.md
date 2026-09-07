# Game Vision — Oakhaven

> 来源：[ChatGPT 分享 · Godot世界设计提示词](https://chatgpt.com/share/6a9e585e-6e10-83ea-98fc-30457ff86eac)  
> 所有改地图 / 改素材 / 改场景的 Agent **开工前必读**。

## Game Identity

This is not a TileMap demo.

This is a handcrafted pixel-art life simulation world (Oakhaven).

The player should feel that they are exploring a real place.

## Visual Reference

Primary reference: `docs/ref/oakhaven_overview.jpg`  
Stitch reference: `docs/ref/stardew_farm_stitch_ref.jpg`

The reference is a **quality target for composition and cohesion**, NOT a pixel-perfect copy.

It represents:

- handcrafted pixel art
- rich environmental composition
- organic terrain
- strong visual hierarchy
- varied regions
- interconnected roads
- clustered vegetation
- coherent architecture
- detailed but controlled decoration

## Fundamental Rule

```text
NEVER build the world around the assets.

BUILD THE WORLD FIRST,
THEN MAKE THE ASSETS SERVE THE WORLD.
```

The world must feel handcrafted before it feels procedural.  
Procedural systems may be used internally, but the output must look intentionally designed.

## Asset-driven vs World-driven

| Asset-driven Map（禁止） | World-driven Map（目标） |
|--------------------------|-------------------------|
| 草地Tile→土地Tile→建筑→重复 | 先区域/道路/水系/聚落，再铺 Tile |
| 割裂、单调、贴图拼接感 | 地形过渡、密度梯度、POI、留白 |
| 以现有素材为中心 | 以世界观与构图为中心 |

## Forbidden Result

- repetitive square terrain / obvious tile repetition
- isolated buildings floating on grass
- uniform vegetation / random decoration everywhere
- perfectly rectangular natural regions
- disconnected asset packs / inconsistent styles
- large empty areas filled only with noise
- polishing micro details while macro composition is weak

## Desired Result

Player should perceive one connected environment:

Forest → path → river → bridge → village → farms → houses → gardens → roads → landmarks

## Design Philosophy

**Macro composition > terrain > architecture > decoration > micro details.**

Never reverse this order.

## Every New System Must Answer

1. How does it fit the world?
2. How does it interact with neighboring elements?
3. How does it avoid visual repetition?
4. How does it preserve the global art style?
5. How does it help create believable environments?

## Agent Rule

Before implementing a visual feature, READ:

- `GAME_VISION.md`（本文件）
- `WORLD_DESIGN.md`
- `ART_DIRECTION.md`
- `TILE_RULES.md` / `MAP_RULES.md`
- `ASSET_SPEC.md` / `VISUAL_BIBLE.md`
- Skill: `game-world-art-director`

Do not invent a new visual language. Extend the existing one.

## Hold — 优化暂停

用户明确：**先入库提示词 / Skill / 多团队协作方式，等命令再继续画面优化。**  
在用户下达「继续优化 / 开工」前，**禁止**继续改地图密度、瀑碗、站台等视觉实现。
