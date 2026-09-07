# Oakhaven — itch.io 中文说明草稿（P166 更新）

> 状态：可跟做导出；正式上传前请本地 F5 / `build/Oakhaven.exe` 冒烟并在 `PLAYTEST_EVIDENCE.md` 签字。  
> 证据索引：[`PLAYTEST_EVIDENCE.md`](PLAYTEST_EVIDENCE.md) · 截图：`assets/qa/golden/` · `assets/qa/smoke/`

## 一句话

**橡木湾（Oakhaven）**：轻松日常像素农场生活 Demo——种地、听雨、聊天、集市、瀑布与灯塔小故事。

## 建议商店图（上传 itch 时选用）

| 用途 | 文件 |
|------|------|
| 主封面 / Cover | `assets/qa/golden/00_overview.png` |
| 镇区 / 店招 | `assets/qa/golden/09_storefronts.png` 或 `smoke/15_storefronts.png` |
| 瀑布 | `assets/qa/golden/07_waterfall.png` 或 `smoke/14_waterfall.png` |
| 农庄 | `assets/qa/golden/01_farm.png` 或 `smoke/16_farm_growth.png` |
| 室内 | `smoke/11_shop_interior.png` · `12_cafe_interior.png` · `13_bakery_interior.png` |

## 操作

| 键 | 作用 |
|----|------|
| WASD / 方向键 | 移动 |
| E | 交互 / 对话 / 进出建筑 |
| 空格（use_tool） | 使用当前工具 |
| 1–4 | 锄头 / 水壶 / 斧头 / 钓竿 |
| Tab | 背包（点种子播种；点作物等选送礼） |

## 你能做什么

- 米勒农庄锄地、播种、浇水、过夜生长、收获  
- 日夜 / 季节 / **天气**（雨粒子 + 过夜加成）  
- 农舍灶台烹饪与吃饭回精力  
- 12 位村民昼夜台词、日程与 **友谊心**  
- 一日游主线 + **小镇集市日** + **暮色故事**第三任务线（钓→青渔→瀑→信箱）  
- 告示栏 / 信箱进度信；遗迹纸条 → 瀑布 → 灯塔  
- 钓鱼、砍木、动物产出  
- **七栋可进室内**：农舍、谷仓、杂货店、咖啡馆、**面包房**、火车站厅、灯塔底层  
- 玩家走路腿部交替 + 锄/浇/播专用动作帧（证据：`smoke/17`–`19` · `21_plant_anim`）  

## Windows 导出（跟做）

1. 用 Godot **4.6.1** 打开 `perfect-game/`  
2. 项目 → 导出 → **Windows Desktop**（`export_presets.cfg`）  
3. 模板在 D 盘：见 `EXPORT_AND_PLAYTEST.md`  
4. 导出到 `build/Oakhaven.exe`（已有 ≈103.8MB / 108870760 bytes · 2026-09-07）  
5. 打 zip 上传 itch（免费 / name your own）

```text
建议标签：pixel-art, farming, cozy, chinese, godot, stardew-like
```

## 已知 Demo 边界

- 视觉仍在追参考图 `docs/ref/oakhaven_overview.jpg`（Critic：未达商店页主图）  
- 无完整婚姻线 / 完整季节作物表  
- 存档：`user://oakhaven_save.json`  
- **Goal 关闭需：** 用户签字试玩 + itch URL  

## 致谢

见 `docs/ASSET_ATTRIBUTION.md`。
