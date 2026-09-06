# Oakhaven — itch.io 中文说明草稿（P15）

> 状态：可跟做导出；正式上传前请本地 F5 / 导出冒烟。

## 一句话

**橡木湾（Oakhaven）**：轻松日常像素农场生活 Demo——种地、聊天、集市、钓鱼、喂牲口。

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
- 日夜流转与精力；农舍床睡觉回满  
- 12 位村民昼夜台词与简易日程  
- 一日游主线 + **小镇集市日**第二任务线  
- 送礼提升友谊；咖啡馆热可可回精力  
- 钓鱼、砍木、动物产出（蛋/毛/奶）  
- 六栋可进室内  

## Windows 导出（跟做）

1. 用 Godot **4.6** 打开 `perfect-game/`  
2. 项目 → 导出 → 选 **Windows Desktop**（见 `export_presets.cfg`）  
3. 若缺导出模板：编辑器 → 管理导出模板 → 下载与引擎同版本  
4. 导出到例如 `build/Oakhaven.exe`  
5. 把 `Oakhaven.exe` 与 `.pck`（若分离）打成 zip 上传 itch  

```text
建议 itch 标签：pixel-art, farming, cozy, chinese, godot
定价：免费 / name your own
```

## 已知 Demo 边界

- 音效为占位哔声  
- 无完整季节作物表 / 婚姻线（后续 Pack）  
- 存档：`user://oakhaven_save.json`  

## 致谢

见 `docs/ASSET_ATTRIBUTION.md`（含 Kenney CC0 catalog 参考）。
