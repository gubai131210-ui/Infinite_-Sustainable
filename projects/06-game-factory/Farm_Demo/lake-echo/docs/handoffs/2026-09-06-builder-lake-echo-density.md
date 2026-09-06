# Handoff — Builder densify Wave (lake-echo R5)

**date:** 2026-09-06  
**from:** Builder  
**to:** Verifier / Critic  
**project:** `projects/06-game-factory/Farm_Demo/lake-echo`  
**status:** PARTIAL — topology + denser props shipped; visual 1:1 vs `docs/ref/frame_01.png` still open

## Objective advanced
- Richer `tileset_master.png` (32 tiles: grass variants, water edges)
- Dense landmarks: barns×2 styles, silos, townhouses, stalls, train, waterfall, lighthouse, boat
- Decor: NW tree belt, animals, sparse NPCs (flip_h), chimney smoke + lake ripples (CPUParticles2D)
- Re-captured `assets/qa/golden_r5/00–06.png` via Godot CLI `--capture_golden` (overview zoom 0.45)

## Evidence
| Artifact | Path |
|----------|------|
| Overview | `assets/qa/golden_r5/00_overview.png` |
| Zones | `01_farm` … `06_lake` |
| Code | `scripts/world.gd`, `landmarks.gd`, `decor.gd`, `main.gd` |
| Gen | `tools/gen_tileset_master.py`, `tools/gen_landmarks.py` |

## Known gaps (do not claim PASS)
- Grass still striped/blocky vs video organic mess
- Paths too straight; cliff/forest density below frame_01
- Farmhouse/barn scale still small in close-ups
- Waterfall prop may miss river close golden (camera mid-river)
- MCP `user-godot-tomyud1` may still be on `farm-demo` — CLI used instead

## Next
1. Organic path painter + stronger waterfall/station close frames  
2. User: open **lake-echo** in Godot + reconnect tomyud1 MCP  
3. Critic re-audit; Goal stays open until visual DoD
