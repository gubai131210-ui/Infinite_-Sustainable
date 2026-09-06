# R5 World Blueprint — 192×128 tiles (TS=16)

**World px:** 3072×2048 · **Camera zoom:** (2,2)

## Zone rectangles (x0,y0)–(x1,y1) inclusive tile coords

| Zone | Label | x0 | y0 | x1 | y1 |
|------|-------|----|----|----|----|
| Z1_FARM | Pillar's Farmstead | 8 | 72 | 72 | 118 |
| Z2_RIVER | Castlenock River + waterfall | 4 | 16 | 56 | 88 |
| Z3_TOWN | Town plaza / market | 64 | 28 | 120 | 72 |
| Z4_STATION | Evergreen Station | 120 | 8 | 184 | 40 |
| Z5_TERRACE | Terraced fields | 120 | 40 | 168 | 80 |
| Z6_LAKE | Lake Echo + lighthouse | 112 | 80 | 188 | 124 |

Overlaps at corridors are intentional (paths/bridges).

## Frame → zone

| Frame | Primary zones |
|-------|----------------|
| frame_01 | All (overview) |
| frame_03 | Z2, Z3, Z6 |
| frame_05 | Z3, Z4, Z5 |
| frame_07 | Z4, Z3, Z5 |
| frame_10 | Z6 |

## Migrate from farm-demo (copy, then adapt)

Safe to migrate:
- `scripts/autoload/item_db.gd`, `inventory.gd`, `game_bus.gd`
- `scripts/player.gd` + `scenes/player.tscn` (facing contract)
- `scripts/hud.gd`, `inventory_ui.gd`, `dialogue_ui.gd`, `interact_zone.gd`
- `scripts/house_interior.gd` + scene
- `addons/godot_mcp/` (copy plugin)
- Input map from `project.godot`

Do **not** migrate:
- `farm_field.gd` Sprite-per-tile painter
- R4 procedural tile hack as final art

## Landmark anchors (tile approx)

| Landmark | Tile |
|----------|------|
| Farmhouse door | (40, 90) |
| Barns | (24, 96), (32, 96) |
| Waterfall | (20, 24) |
| Plaza statue | (90, 48) |
| Station platform | (150, 22) |
| Lighthouse | (170, 108) |
