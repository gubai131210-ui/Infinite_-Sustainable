# 视觉 Critic — golden vs overview（2026-09-07 · P99–P102）

## 结论
更接近 overview：**是**（GENERAL STORE / OAKHAVEN CAFE / BAKERY 在 `09_storefronts` 全字可读；集市下移不再挡店面；广场软椭圆+路径肩 denser；NPC 更常走动）。  
达到「商店页可直接当主图」：**否**（路径仍偏 tile；林冠/瀑仍 PIL 程序感；缺用户签字试玩 + itch URL）。

## 本轮证据
- MCP `0` error · `GOLDEN_CAPTURE_DONE`（含 `09_storefronts.png`）
- bitmap 招牌 + 窗下移，避免遮字；hero 店面落在广场中心
- `_paint_plaza_soft` 加重 dither；NPC walk bias / speed / bob↑
- `tools/gen_p99_signs.py` 可复现招牌

## 仍差
1. 路径/广场 tile 感仍可见（需更强有机材质或自绘 dirt atlas）
2. 林冠/瀑未达参考油画质感
3. 用户签字试玩 + itch 发布 URL

## Goal
**不可 complete**。
