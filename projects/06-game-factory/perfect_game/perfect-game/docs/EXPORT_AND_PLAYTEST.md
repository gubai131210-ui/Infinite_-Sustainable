# Oakhaven 导出与回归清单（P15 / P18 / P19）

## 存档版本

- 当前 `save_version`：**3**（金币/日时/地块键 `x,y`/双任务线/友谊/选中礼物/精力）
- 旧档缺字段时用默认值；地块键会 normalize

## Windows 导出（已在 D 盘装模板）

1. 导出模板已解压到：`D:\Godot\export_templates\4.6.1.stable.mono\`  
2. AppData 联接：`%APPDATA%\Godot\export_templates\4.6.1.stable.mono` → 上述目录  
3. Godot 4.6.1 mono 打开本工程 → 项目 → 导出 → **Windows Desktop** → `build/Oakhaven.exe`  
4. 实测产物：`build/Oakhaven.exe` ≈ **103.8 MB**（2026-09-07）

> 若 C 盘满：不要把 tpz 解压到 C；用 D 盘 + junction 即可。

itch 文案见 [`ITCH_PAGE_DRAFT_CN.md`](ITCH_PAGE_DRAFT_CN.md)。

## 回归清单（PLAYTEST）

- [ ] 新档：锄地→播种→浇水→睡→生长→收获  
- [ ] HUD：日时 / 季节 / **天气** / 金币整数 / 精力  
- [ ] 雨天：雨粒子 + 过夜作物加成  
- [ ] 农舍灶台烹饪 → 吃饭回精力  
- [ ] 镇告示栏 / 农舍旁信箱  
- [ ] BGM + 雨声 / 工具音效  
- [ ] 进出 6 室内后地块与金币仍在  
- [ ] 主线一日游 → 集市日第二线可推进  
- [ ] 送礼改台词；小菊触达 `mkt_talk_hua`  
- [ ] 砍树/钓鱼/喂养收取  
- [ ] 河水 soft shimmer（无棋盘闪烁）  
- [ ] 秋冬色调变化（过 7 天进下一季）  
- [ ] 双击 `build/Oakhaven.exe` 冒烟  

## Golden 截图

```text
Godot 运行主场景并传用户参数：
  --capture_golden
输出：`00_overview` … `06_lake` + `07_waterfall` + `08_dialogue`
```

对照：`docs/ref/oakhaven_overview.jpg` + Visual Bible。
