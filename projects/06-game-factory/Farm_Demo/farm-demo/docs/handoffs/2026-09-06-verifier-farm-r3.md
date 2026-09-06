# Verifier — Farm_Demo R3

**handoff_id:** 2026-09-06-verifier-farm-r3  
**from:** Verifier → Critic

## Evidence

| 类型 | 摘要 | 结果 |
|------|------|------|
| runtime | world_size 1536×1024 | pass |
| runtime | walk_up / walk_left | pass |
| runtime | enter_house → HouseInterior | pass |
| runtime | exit_house → Main @ door | pass |
| runtime | pasture y≈800 > 640 | pass |
| screenshot | golden_r3/01..05 | pass |
| errors | 0 | pass |

## Acceptance
对照 GOAL DoD 与 ACCEPTANCE.md — 建议 Critic PASS

## Do-Not followed
未在 cursor-demo 上验收；未无截图结案
