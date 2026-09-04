# AI 资讯 · 横版分区大图（当前主用）

竖版密堆易拥挤。本仓资讯主图改为 **16:9 横版四区**：

```text
┌──────────┬──────────┬──────────┬──────────┐
│ ① 事件   │ ② 宣传口径│ ③ 体感口径│ ④ 行动   │
│ 发生什么 │ 涨25%    │ 少约17%  │ 查/排/备/问│
└──────────┴──────────┴──────────┴──────────┘
底栏：100→150→125 + 免责
```

脚本：`scripts/render_ai_news_cover.py` → `cover_landscape.jpg` / `cover.jpg`

## 文生图备用 Prompt（若改用 GPT-Image）

```text
Xiaohongshu wide editorial infographic 16:9, dark navy #0B1220,
FOUR equal vertical panels with gaps, not one crowded column:
Panel1 title 「①事件」 facts about promo +50% until 9/13 then permanent +25%,
Panel2 「②宣传口径」 giant 「涨25%」 teal, caption 相对原始基线,
Panel3 「③体感口径」 giant 「少约17%」 coral, caption 相对今天,
Panel4 「④行动」 four action cards 查/排/备/问,
top bar title 「Claude Code周限额：同一公告，两种读法」,
bottom strip formula 100→150→125 and disclaimer,
high-fidelity Chinese typography, crisp modular layout, generous panel padding, no cluttered vertical stack, no watermark
```
