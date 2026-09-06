## TASK HANDOFF v2

### Meta
- handoff_id: 2026-09-06-verifier-lake-echo-golden
- playbook: PB-Game-Visual
- from_agent: Verifier
- to_agent: Critic

### Objective
Capture golden_r5 six-zone screenshots via Godot CLI `--capture_golden`.

### Evidence
| 类型 | 路径 | 结果 |
|------|------|------|
| CLI run | Godot 4.6.1 --capture_golden | GOLDEN_CAPTURE_DONE |
| screenshot | assets/qa/golden_r5/00..06.png | saved |
| errors | get_debug_output | warnings only (int div) |

### Acceptance
- [x] six zone shots exist
- [ ] visual density matches reference video (FAIL / incomplete)
- [x] TileMap architecture
- [x] farmhouse door interact present
- [ ] Critic art DoD vs video

### Open Questions
MCP tomyud1 still on farm-demo — golden via CLI instead.

### Suggested Next Agent
Critic — then Asset densify toward video
