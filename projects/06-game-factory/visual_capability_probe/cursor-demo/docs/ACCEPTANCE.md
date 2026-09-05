# ACCEPTANCE — Game MVP（在探针之上）

Playbook 基线：`PB-Game-Visual`  
本阶段增量：美术 scrub、脚底对齐、门/山路交互、东侧小路占位、Verifier 文档

## Checklist

| 项 | 结果 | 证据 |
|----|------|------|
| 探针项仍成立 | 见下轮 MCP | 分层 / instance / 移动 |
| 前景绿边减轻 | PASS（色键+scrub） | `assets/qa/checker_fg_props.png` 重跑 |
| 门交互 E | PASS | DoorZone + toast |
| 山路交互 E | PASS | PathZone + 东侧小路占位 |
| Verifier 步骤 | PASS | `docs/VERIFY_MCP.md` |

## Controls

- A/D 或方向键移动
- E 交互（靠近门或山路标记时）

## Notes

- **rembg（D 盘已就绪）**：见仓库 `knowledge/godot/rembg-d-drive.md`
- 重跑抠图：`$env:USE_REMBG=1; python tools/cutout_pipeline.py`（在 cursor-demo 下）
- 东侧小路为占位（Polygon2D），完整第二屏美术下一迭代
