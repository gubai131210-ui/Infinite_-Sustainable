# Research — Godot 4.6 TileMapLayer for lake-echo

## Decisions for lake-echo

1. **Use `TileMapLayer` children** under a root `World` node (Godot 4.3+), not legacy multi-layer TileMap API alone — separate layers: `Ground`, `Cliff`, `Water`, `Decor`.
2. **Terrain sets** for grass↔water and grass↔path peering; cliffs as solid tiles + physics on Water/Cliff layers.
3. **Y-sort** on an `Entities` Node2D (`y_sort_enabled=true`) for player/NPC/buildings; tile layers stay non-Y-sorted for perf on 192×128.

## Refs

- https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html
- https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html
- https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html (nearest filter)

## Perf

- Prefer atlas tileset one texture; avoid per-cell Sprite2D (R4 anti-pattern).
- Collision only on Water/Cliff/Building shapes, not every grass cell.
