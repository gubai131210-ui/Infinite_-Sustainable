# PLAYTEST — 橡木湾试玩与导出

## 试玩

1. Godot 4.6 打开本工程  
2. 项目 → 项目设置 → 应用 → 主场景 = `res://scenes/main.tscn`  
3. F5  
4. 建议路线：农庄锄地播种 → 镇中心对话 → 火车站进厅 → 回声湖灯塔 → 钓鱼  

## Windows 导出（itch Demo）

1. 编辑器：项目 → 导出  
2. 添加预设 **Windows Desktop**（若列表空：安装 Godot export templates）  
3. 导出路径建议：`build/Oakhaven.exe`  
4. 勾选嵌入 PCK；导出后连同 `.pck` 一并打包 zip 上传 itch  

本仓库提供 [`export_presets.cfg`](../export_presets.cfg) 骨架；首次需在本机选择 Godot 导出模板路径。

## 验收自检

- [ ] 六区均能走到  
- [ ] 农舍/谷仓/店/咖啡/车站/灯塔可进可出  
- [ ] 12 名村民有台词  
- [ ] 背包可见种子/收获  
