# ACCEPTANCE — Farm_Demo Round4

| 项 | 结果 | 证据 |
|----|------|------|
| MCP 无致命错误 | PASS | get_errors=0 |
| 地图 ≥96×64 | PASS | world_size=(1536,1024) |
| 整数缩放 | PASS | Camera2D.zoom=(2,2) |
| 左右朝向正确 | PASS | atlas 行对调；walk_left/right + facing ±x；golden `04`/`05` |
| 上下朝向 | PASS | walk_up y↓；walk_down y↑；golden `06` |
| 草地无粉缝重生 | PASS | `tools/r4_fix_assets.py` 重生 tile_* + QA checker |
| 河岸过渡 | PASS | gw_* 8 向；golden `02_river_shore.png` |
| 村口石板广场 | PASS | T.PLAZA；golden `03_village_plaza.png` |
| 北崖/台阶 | PASS | CLIFF + STAIRS 走廊 |
| 农舍可进 | PASS | HouseInterior；golden `07_house_interior.png` |
| 床交互 | PASS | BedZone._do_interact OK（toast 需同帧读） |
| golden_r4 | PASS | `assets/qa/golden_r4/*` |

## 禁止偷懒核对

- [x] 四向用脸朝向截图，不只 animation 名
- [x] 未假装火车/灯塔全图
- [x] 树/灌木非整排复制
- [x] 参考帧与规格已入库
