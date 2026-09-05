# ACCEPTANCE — visual_capability_probe / cursor_demo

Playbook: `docs/playbooks/PB-Game-Visual.md`  
Engine: Godot 4.6 · GL Compatibility · 1280×720

## Spec (grill locked)

- 横版 + 重力 + 水平地面
- 山间木屋前院 · 黄昏
- 成年男性旅人 · 静止站立 + 平移
- 远景 / 木屋中景 / 近景遮挡 / 角色
- Cursor 生图 + 色键抠图（绿幕）+ 棋盘格 QA

## Checklist

| 项 | 结果 | 证据 |
|----|------|------|
| 主场景可运行无致命错误 | PASS | MCP `get_errors` → 0 |
| ≥3 层分层 / 前景可遮挡 | PASS | Far/Mid parallax + Foreground z=20；截图见分层 |
| Player 独立 instance | PASS | `res://scenes/player.tscn` instanced in main |
| 左右移动 + 地面 | PASS | x 360→720，y=420 稳定，velocity.y=0 |
| HUD 与世界分离 | PASS | CanvasLayer HUD 显示 `pos:` |
| 抠图棋盘格 | PASS | `assets/qa/checker_*.png` |

## Layer notes

- Far：`ParallaxBackground`（慢卷）
- Mid cabin：世界空间 `MidCabin`（与角色 1:1，避免视差卷走木屋）
- Foreground：高 `z_index` 遮挡
- rembg 大模型下载过慢，本探针用绿幕色键 + 硬边 alpha；可选 `USE_REMBG=1` 再跑 `tools/cutout_pipeline.py`
- 角色 `min_x/max_x` 限制在木屋前院可视范围
