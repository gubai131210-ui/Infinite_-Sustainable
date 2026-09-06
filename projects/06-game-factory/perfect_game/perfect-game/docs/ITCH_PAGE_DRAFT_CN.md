# Oakhaven — itch.io 中文说明草稿（P15 / P54 更新）

> 状态：可跟做导出；正式上传前请本地 F5 / `build/Oakhaven.exe` 冒烟。  
> 证据索引：[`PLAYTEST_EVIDENCE.md`](PLAYTEST_EVIDENCE.md)

## 一句话

**橡木湾（Oakhaven）**：轻松日常像素农场生活 Demo——种地、听雨、聊天、集市、瀑布与灯塔小故事。

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
- 一日游主线 + **小镇集市日**第二任务线  
- 告示栏 / 信箱进度信；遗迹纸条 → 瀑布 → 灯塔  
- 钓鱼、砍木、动物产出；六栋可进室内  

## Windows 导出（跟做）

1. 用 Godot **4.6.1** 打开 `perfect-game/`  
2. 项目 → 导出 → **Windows Desktop**（`export_presets.cfg`）  
3. 模板在 D 盘：见 `EXPORT_AND_PLAYTEST.md`  
4. 导出到 `build/Oakhaven.exe`（已有 ≈103.8MB 产物可作参考）  
5. 打 zip 上传 itch（免费 / name your own）

```text
建议标签：pixel-art, farming, cozy, chinese, godot, stardew-like
```

## 已知 Demo 边界

- 视觉仍在追参考图 `docs/ref/oakhaven_overview.jpg`（未达商店页主图）  
- 无完整婚姻线 / 完整季节作物表  
- 存档：`user://oakhaven_save.json`  

## 致谢

见 `docs/ASSET_ATTRIBUTION.md`。
