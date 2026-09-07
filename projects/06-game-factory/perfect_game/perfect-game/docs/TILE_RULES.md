# Tile Rules — Oakhaven

## 原则

Terrain **不得**只靠一张中心瓦无限重复。需要：

- center variants  
- edge / corner variants  
- transition variants  
- worn / decorative variants  

## 过渡链（禁止硬切）

```text
GRASS → sparse → dry → mixed grass/dirt → dirt → worn path
GRASS → wet grass → mud → water edge
DIRT → rocky dirt → gravel → stone road
```

已有实现入口：`world.gd` 的 `_stitch_dirt_seams` / `_stitch_water_shores`、`gen_tileset_master.py` 的 `grass_dirt` / `water_edge`。

## 禁止

- 大块完美矩形自然区（玩法耕地除外）  
- 可见 AAAAA 重复纹样 / 明显 2×2·3×3 周期  
- 长直纹理缝当「自然边界」  

## 偏好

弯曲边界、小湾、渐变、过渡植被、局部斑块、簇状侵蚀感。
