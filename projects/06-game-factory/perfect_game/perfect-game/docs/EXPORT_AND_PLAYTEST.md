# Oakhaven 导出与回归清单（P15 / P18）

## 存档版本

- 当前 `save_version`：**3**（金币/日时/地块键 `x,y`/双任务线/友谊/选中礼物/精力）
- 旧档缺字段时用默认值；地块键会 normalize

## Windows 导出步骤

1. Godot 4.6 打开本工程  
2. 项目 → 导出 → **Windows Desktop**（`export_presets.cfg` → `build/Oakhaven.exe`）  
3. 缺模板则先下载对应版本导出模板  
4. 导出后本地双击 `build/Oakhaven.exe` 冒烟  

itch 文案见 [`ITCH_PAGE_DRAFT_CN.md`](ITCH_PAGE_DRAFT_CN.md)。

## 回归清单（PLAYTEST）

- [ ] 新档：锄地→播种→浇水→睡→生长→收获  
- [ ] HUD：日时 / 季节 / 金币整数 / 精力  
- [ ] 进出 6 室内后地块与金币仍在  
- [ ] 主线一日游 → 集市日第二线可推进  
- [ ] 送礼改台词；小菊触达 `mkt_talk_hua`  
- [ ] 砍树/钓鱼/喂养收取  
- [ ] 河水动画 + 脚步/工具音效  
- [ ] 秋冬色调变化（过 7 天进下一季）  

## Golden 截图

```text
Godot 运行主场景并传用户参数：
  --capture_golden
输出：assets/qa/golden/01_farm … 06_lake + 00_overview.png
```

对照：`docs/ref/oakhaven_overview.jpg` + Visual Bible。
