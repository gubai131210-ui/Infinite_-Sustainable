# GOAL — Farm_Demo Round5：对照参考视频 Godot 一比一重建（多 Agent）

**Goal ID:** `farm-demo-r5-one-to-one-remake`  
**参考源:** `C:\Users\孤白赟悫\Downloads\8c8babec-8cd9-46a8-afda-7f1cec0a98d4.mp4`  
**参考帧:** `docs/ref/r4_video/frame_01.png` … `frame_10.png`（已入库）  
**Playbook:** `PB-Game-Visual` + 玩法迁移  
**团队:** Agent Team v2 + `docs/handoff-v2.md`  
**tools_allowed:** `code` · `mcp` · `image` · `shell` · `publish`  
**引擎:** Godot 4.6 · MCP `user-godot-tomyud1` 必须 Connected 到**新工程路径**

---

## 0. 「一比一」锁定定义（必须先读）

### 做到

| 维度 | 标准 |
|------|------|
| 拓扑 | 视频中标注的六大区位置关系一致：农场 / 河瀑布 / 镇广场 / 火车站 / 梯田 / Lake Echo+灯塔 |
| 地标 | 红谷仓+筒仓、市集摊位+雕像广场、火车+站台、灯塔、瀑布、木桥、阶梯崖壁均可辨认 |
| 风格 | 3/4 俯视像素、分层崖、自然弯曲土路、河湖岸过渡、烟囱烟/涟漪动效 |
| 密度 | 房屋/树/NPC/栅栏密度接近参考帧（非稀疏色块农场） |
| 玩法 | 保留：WASD、锄浇种收、进屋床箱、中文 UI；可在对应区交互 |

### 做不到 / 禁止宣称

- **禁止**声称与 AI 视频逐像素相同（生成片本身帧间不一致）
- **禁止**用几个 ColorRect/单张背景图冒充「一比一地图」
- **禁止**跳过分区 MCP 截图对比参考帧就标 PASS

### 工程决策（锁定）

| 项 | 决策 |
|----|------|
| 工程位置 | **新建** `projects/06-game-factory/Farm_Demo/lake-echo/`（干净 TileMap 架构）；旧 `farm-demo/` 只读归档，不在其上硬补 |
| 地图技术 | Godot **TileMapLayer**（地面/崖/水/装饰）+ YSort 实体层；禁止再写 96×64 每格一个 Sprite2D |
| 尺寸 | 主世界目标约 **192×128 tiles**（TS=16 → 3072×2048 px），相机整数 zoom=2 |
| 分区加载 | 单主场景分 **Zone 节点**；后期可切 chunk，本 Goal 不强制流式加载 |
| 资产 | AI 像素 + 热粉键 + 棋盘格 QA；大地图允许「模块化拼装」同一 tileset |

---

## 1. 参考世界拆解（Scout 必须产出坐标表）

对照 `frame_01`（总览）+ `frame_03/05/07/10`（特写）：

```text
                    [瀑布/崖林]
                         |
[Evergreen Station]——[镇中心广场市集]——[梯田]
        |                    |
   铁轨隧道              [弯曲河+桥]
                             |
              [Pillar's Farmstead 谷仓/田] —— [Lake Echo + 灯塔]
```

| Zone ID | 参考标签 | 必含元素 | 建议 tile 矩形 (粗) |
|---------|----------|----------|---------------------|
| Z1_FARM | The Pillar's Farmstead | 红谷仓×2、筒仓×2、栅栏畜栏、成排田、农舍门可进 | SW 象限 |
| Z2_RIVER | Castlenock / Gillian's River | 瀑布、弯河、≥2 木桥、岸边过渡 | 西偏中 |
| Z3_TOWN | 镇中心 | 石板广场、雕像、≥4 摊位、半木构屋≥6 | 中央 |
| Z4_STATION | Evergreen / Sunnyside / Woodberry Station | 站房、站台、火车、铁轨、隧道口 | NE |
| Z5_TERRACE | 梯田 | 分层田、石阶、作物行 | 东中 |
| Z6_LAKE | Lake Echo | 湖、灯塔、码头、船、湖岸沙/石 | SE |

---

## 2. 多 Agent 编排（强制顺序 + 并行组）

```text
Conductor
  ├─ Scout          参考帧标注 + 旧工程可迁移清单
  ├─ Researcher     TileMapLayer / terrain / YSort 官方做法证据
  ├─ Game           世界规格 + Zone 状态机 + 玩法落点
  ├─ Planner        分 Wave 里程碑与依赖图（本文件落地）
  │
  ├─ Wave0 Foundation（串行）
  │    Asset:  master tileset + 角色朝向契约
  │    Builder: 空工程 + autoload + MCP 接线 + 相机
  │
  ├─ Wave1–6 Zones（每区: Asset ‖ Builder → Verifier）
  │    parallel_group: lake-echo-zN
  │
  ├─ Wave7 Polish   动效(烟/水)、标签、密度补齐
  ├─ Verifier-Full  全图巡航 MCP + golden_r5 vs 参考帧
  ├─ Critic         对照本 Goal DoD / 禁止偷懒
  └─ Memory?        仅沉淀 tileset/朝向/验收模板规律
```

### Cursor Task 映射

| 角色 | 建议 Task |
|------|-----------|
| Scout | explore / 本对话只读 |
| Researcher | generalPurpose + 官方文档 |
| Asset | generalPurpose + image 工具 |
| Builder | generalPurpose + Godot MCP |
| Verifier | Godot MCP 强制 |
| Critic | 独立子 Agent，禁自证 |

### Handoff

每个 Wave / Zone 结束必须写：  
`docs/handoffs/YYYY-MM-DD-{role}-lake-echo-zN.md`（`handoff-v2` 字段齐全）

---

## 3. 分 Wave 详细任务卡

### Wave 0 — Foundation（阻塞后续一切）

**Scout**
- Objective: 在 `docs/specs/R5_WORLD_BLUEPRINT.md` 画 192×128 网格分区 + 标注帧→坐标映射；列出 `farm-demo` 可迁移脚本清单（Inventory/ItemDB/GameBus/Player）
- Do-Not: 禁止改玩法代码；禁止只写散文无坐标表

**Researcher**
- Objective: 产出 `docs/research/2026-09-godot-tilemap-terrain.md`（Godot 4.6 TileMapLayer、terrain set、YSort、性能）
- Acceptance: 含官方链接 + 对本工程的 3 条决策建议

**Game**
- Objective: `docs/specs/R5_ZONE_AND_GAMEPLAY.md` — 每区碰撞/交互点；农舍/商店门；火车不可上车（装饰+可选站台 toast）
- Do-Not: 禁止加昼夜存档经济剧情长文

**Asset ‖ Builder（汇合）**
- Asset: `tileset_master.png`（草/土/石板/崖/水/铁轨/岸边 8 向）+ 棋盘格；player 四向契约自检
- Builder: 创建 `lake-echo/` Godot 4.6 工程；MCP addon；Main/World/Player/HUD；空 TileMap 六 Zone 节点占位
- Verifier: `run_scene` + get_errors=0 + 相机 zoom=(2,2)

### Wave 1 — Z1_FARM

- Asset: 谷仓、筒仓、栅栏、田土、鸡牛羊比例
- Builder: 铺西南农场；迁移锄浇种收到本区农田；农舍可进
- Verifier: golden vs `frame_01` 左下象限；MCP 锄地断言

### Wave 2 — Z2_RIVER

- Asset: 瀑布条、桥、河岸 terrain
- Builder: 弯河 + 瀑布假高度崖 + 桥可走
- Verifier: 截图对照 frame 瀑布/桥；玩家不可落水（碰撞）

### Wave 3 — Z3_TOWN

- Asset: 半木构屋变体≥3、摊位条纹篷、雕像、灯柱
- Builder: 石板广场 + ≥6 屋 + ≥4 摊 + NPC 漫游路径
- Verifier: 广场密度截图；YSort 人物过屋前

### Wave 4 — Z4_STATION

- Asset: 火车、站房、铁轨条、隧道口
- Builder: NE 铁轨水平带 + 站台；火车装饰动画（烟）
- Verifier: 对照 frame 火车站特写

### Wave 5 — Z5_TERRACE

- Asset: 梯田作物行、石阶
- Builder: 东侧分层崖 + 台阶可行走
- Verifier: 分层可见；可从镇下到湖

### Wave 6 — Z6_LAKE

- Asset: 灯塔、码头、帆船/小船、湖面涟漪帧
- Builder: SE 湖面 + 灯塔地标 + 岸边
- Verifier: 对照 `frame_10` Lake Echo

### Wave 7 — Polish + 全图验收

- 地名标签（中文或保留英文参考名，UI 中文）
- 烟囱/瀑布/湖面简单动画
- 全图巡航：Player warp 六区各一金图 `assets/qa/golden_r5/`
- Critic 对照本文件 DoD
- `git push`

---

## 4. Definition of Done（全部满足才可关 Goal）

1. 新工程 `lake-echo/` 可 F5 运行，MCP `get_errors=0`
2. 六区均有可辨认地标，且相对位置与参考总览一致（Verifier 分区金图 + Critic）
3. TileMap 架构（非每格 Sprite）；整数相机缩放；YSort 正确
4. 农场玩法在 Z1 可用；至少一栋可进室内
5. `VERIFY_MCP.md` R5 清单全过；`ACCEPTANCE.md` 每行有证据路径
6. 多 Agent handoff 六区齐全；Critic PASS
7. 已推 GitHub

---

## 5. 禁止偷懒（Conductor 每 Wave 检查）

- 禁止继续在旧 `farm_field.gd` Sprite 铺地上「扩一扩」冒充重建
- 禁止单张背景大图当世界
- 禁止火车站/灯塔用 16×16 色块占位就算完成（至少可辨认剪影+细节）
- 禁止 Verifier 只查坐标不截图对比参考帧
- 禁止 Asset 跳过棋盘格 QA
- 禁止六区未齐就宣称一比一完成
- 禁止主对话一人包办全部 Wave 而不写 handoff
- 禁止未推 GitHub 宣称 Goal 完成

---

## 6. 新对话启动词（复制到 Goal 模式）

```text
执行 GOAL_R5_ONE_TO_ONE_REMAKE.md
工程：projects/06-game-factory/Farm_Demo/lake-echo/
参考：docs/ref/r4_video/ + 用户视频
按 Agent Team v2：Scout→Researcher→Game→Wave0…Wave7
强制 MCP；每区 handoff-v2；禁止偷懒清单全文遵守
tools_allowed: code mcp image shell publish
```

---

## 7. 与 R4 关系

R4（朝向+农场河村口切片）**不作为**一比一终态；仅提供：朝向契约、玩法脚本参考、参考帧路径。R5 为正式重建。
