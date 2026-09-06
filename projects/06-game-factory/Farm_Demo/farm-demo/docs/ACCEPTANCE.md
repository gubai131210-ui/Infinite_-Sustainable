# ACCEPTANCE — Farm_Demo Round3

| 项 | 结果 | 证据 |
|----|------|------|
| MCP 无致命错误 | PASS | get_errors=0 |
| 地图 ≥96×64 | PASS | world_size=(1536,1024) |
| 整数缩放 | PASS | Camera2D.zoom=(2,2) |
| 去粉边抽样 | PASS | player/tree/house/chicken hotpink=0 |
| 河岸过渡（无 dirt 边红线） | PASS | 仅 gw_* 边角 |
| 四向动画 | PASS | walk_up / walk_left runtime |
| 农舍可进 | PASS | root→HouseInterior；golden `02_house_interior.png` |
| 出门回室外 | PASS | root→Main；pos≈(592,392) |
| 床休息 | PASS | toast「休息了一会儿…」 |
| 南牧场新区 | PASS | warp y≈800；`03_south_pasture.png` |
| golden_r3 | PASS | `assets/qa/golden_r3/*` |

## 禁止偷懒核对

- [x] MCP 证据
- [x] 房子非纯装饰
- [x] 地图扩分区
- [x] 四向用 atlas 行
- [x] 相机整数 zoom
- [x] 室内独立场景
