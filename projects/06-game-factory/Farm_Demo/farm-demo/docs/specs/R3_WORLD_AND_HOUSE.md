# R3 — 世界扩图 + 房屋交互规格

## 地图（单主场景）

| 常量 | 值 |
|------|-----|
| W×H | **96 × 64** tiles（16px） |
| 世界像素 | 1536 × 1024 |

### 分区（tile 坐标）

| 区 | 范围（约） | 内容 |
|----|------------|------|
| 北山 | y=0..10 | HILL + 树 |
| 西农场 | x=4..16, y=14..32 | FARMLAND |
| 河流 | x≈28±3 蜿蜒 | WATER + dirt 岸 |
| 农舍院 | x=32..42, y=18..28 | DIRT + **可进农舍** |
| 村口 | x=70..90, y=20..34 | PATH + 装饰屋 |
| **南牧场**（新区） | x=20..50, y=44..58 | GRASS + 牛羊鸡 |
| **东林地**（新区） | x=72..92, y=40..58 | GRASS/树 + 砍树点 |

出生点：`(10, 22)` 农场旁。

## 房屋状态机

```text
Outdoor ──E near DoorZone──► HouseInterior
     ▲                              │
     └──────── E ExitDoor ──────────┘
Bed: E → toast「休息了一会儿，精神满满。」（无昼夜）
Chest: E → 同室外箱子逻辑（GameBus.chest_claimed 共享）
```

### 节点

- 室外：`World/YSort/FarmHouseDoor`（InteractZone mode=`house`）位置约农舍门口 `(36, 24)`
- 室内场景：`res://scenes/house_interior.tscn`
- GameBus：`outdoor_return_pos`、`enter_house()` / `exit_house()`、`consume_spawn()`

## 四向断言表（Verifier）

| 输入 | position 期望 | animation 期望（移动中/停下） |
|------|---------------|------------------------------|
| move_up | y 减小 | walk_up / idle_up |
| move_down | y 增大 | walk_down / idle_down |
| move_left | x 减小 | walk_left / idle_left |
| move_right | x 增大 | walk_right / idle_right |

工具目标格 = `facing` 方向一格。

## 相机

- `zoom = Vector2(2, 2)`（整数）
- `limit_*` = 新 world_size
- texture filter nearest（项目已设）

## 画面整洁策略

1. 关键角色/树热粉像素必须为 0  
2. 河岸过渡：仅 grass↔water 边角；**停用易出错的 grass↔dirt 边**（防红线）  
3. 室内用程序像素地板/墙/床（NEAREST）
