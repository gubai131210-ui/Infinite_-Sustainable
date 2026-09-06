# R4 — Visual + Facing Spec

**Goal:** 对照参考视频风格重铺「农场 + 河 + 村口」可玩切片；修复左右朝向。  
**参考帧:** `docs/ref/r4_video/frame_01.png` … `frame_10.png`  
**Out of scope:** 火车、灯塔、全镇 1:1。

## 朝向契约（强制）

Atlas `assets/processed/player.png`：48×48 格，**4 行 × 6 列**

| 行 | 方向 | 精灵应显示 |
|----|------|------------|
| 0 | down | 正面（朝向屏幕） |
| 1 | left | 侧面朝左 |
| 2 | right | 侧面朝右 |
| 3 | up | 背面 |

代码：`player.gd` `DIRS = ["down","left","right","up"]` 必须与上表一致。  
验收：WASD 位移轴 + `facing` + 截图脸朝向三者一致（禁止只断言 animation 名）。

## 分区草图（96×64 tiles，TS=16）

| 区 | 大致坐标 | 内容 |
|----|----------|------|
| 北丘崖 | y 0–10 | HILL/CLIFF + 台阶缺口 |
| 西农田 | x 4–18, y 14–34 | FARMLAND 成排 |
| 弯曲河 | x≈26–34 随 sin | WATER + 完整 gw_* 岸 |
| 农舍院 | x 32–44, y 18–28 | DIRT + 可进农舍 |
| 村口广场 | x 68–90, y 18–34 | PATH/石砖 + 摊位/房屋 |
| 南牧场 | y 46–58, x 22–48 | 草+畜 |
| 东林 | x 78–92, y 42–58 | 树错落 |

## 视觉规则

- 相机 `zoom=(2,2)` nearest，无粉/洋红缝
- 河岸用 4 边 + 4 角过渡砖；dirt/path 与草用软边或干净实心砖（无红线）
- 树/灌木禁止整排同一偏移复制；YSort 角色与高物
- 村口：石板质感 path、1–2 摊位、2 栋屋

## MCP 验收要点

见 `docs/VERIFY_MCP.md` Round4 表。
