# Farm Demo — locked grill spec (2026-09-05)

## Decisions

- Depth: playable demo (no story)
- View: top-down 2D
- Loop: hoe → plant → water → grow → harvest + inventory
- No day/night, save, economy balance
- Map: medium continuous (farm / house / river / hills / village) + fishing
- Art: procedural pixel (green-screen → chroma cutout → QA checker)
- Tools: WASD, E interact, 1–4 tools, Tab inventory, Space use tool
- Crops: radish(2), greens(3), wheat(4), tomato(5), pumpkin(6) waterings
- NPCs: 阿禾, 小满, 青渔, 林婶, 石匠周
- Animals: chicken×3, cow×1, sheep×2
- Pixel: chars 32px / tiles 16px; walk 8 FPS; tools 10 FPS
- UI: Chinese

## Anti-lazy

1. No ColorRect pretending to be art
2. No skip cutout QA
3. Separate Player / World / HUD / Inventory / Dialogue
4. Full farm loop required
5. MCP screenshot/runtime evidence
6. No fake day/save/shop systems
7. NPCs visually distinct
8. Inventory & dialogue are own panels/layers
