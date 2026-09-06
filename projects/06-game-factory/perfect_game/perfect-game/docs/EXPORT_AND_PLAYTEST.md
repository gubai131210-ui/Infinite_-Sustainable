# Oakhaven 导出与回归清单（P15 / P18）

## 存档版本

- 当前 `save_version`：**3**（金币/日时/地块键 `x,y`/双任务线/友谊/选中礼物/精力）
- 旧档缺字段时用默认值；地块键会 normalize

## Windows 导出步骤

1. Godot 4.6 打开本工程  
2. **先安装导出模板**（编辑器 → 管理导出模板 → 下载与引擎同版本 `4.6.1.stable.mono`）  
   - 缺模板时 CLI 会报：`export_templates/4.6.1.stable.mono/windows_release_x86_64.exe` 不存在  
3. 项目 → 导出 → **Windows Desktop**（`export_presets.cfg` → `build/Oakhaven.exe`）  
4. 导出后本地双击 `build/Oakhaven.exe` 冒烟  

> 2026-09-06 Agent 实测：  
> 1) 曾因缺导出模板导致 `--export-release` 失败。  
> 2) 尝试下载 `Godot_v4.6.1-stable_mono_export_templates.tpz`（≈1.08GB）成功，但 **C 盘空间不足**，无法解压安装；已删除 tpz 释放空间。  
> **请你本机**：先腾出 ≥3GB，再在 Godot「管理导出模板」下载 mono 4.6.1，然后导出到 `build/Oakhaven.exe`。

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
