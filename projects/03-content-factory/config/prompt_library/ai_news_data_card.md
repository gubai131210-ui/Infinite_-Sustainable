# AI 资讯 · 数据卡封面模板（主用）

改编自 [Apiyi Data Visualization Card](https://help.apiyi.com/en/gpt-image-2-xiaohongshu-infographic-content-creation-guide-en.html)  
本仓默认：**不靠文生图写中文**，由 `scripts/render_ai_news_cover.py` 落实同一布局。

## 布局契约（程序必须遵守）

```text
┌─────────────────────────────┐
│ 顶栏：品类标签 + 日期         │  ~6%
│ 主标题（≤18字）               │  ~10%
│ 副标题一句钩子                │  ~5%
├─────────────────────────────┤
│ 核心大数字区（占屏高 ~32%）    │  主数字 + 对照副数字
│ 口径说明两行                  │
├─────────────────────────────┤
│ 3 行补充数据（标签|数值|注释） │  ~22%
├─────────────────────────────┤
│ 换算条 100→150→125           │  ~8%
├─────────────────────────────┤
│ 行动清单 3–4 条               │  ~14%
│ 页脚来源/免责                 │  ~5%
└─────────────────────────────┘
```

配色（保留深色蓝系）：`#0B1220` 底 / `#3B82F6` 强调 / 绿涨红跌 / 琥珀钩子。

## 若使用文生图模型（GPT-Image 等）可直接套

```text
Xiaohongshu data card, 3:4 vertical, dark navy editorial background #0B1220,
Top label 「AI资讯·额度口径」 22pt light blue,
Main title 「Claude Code周限额」 52pt bold white,
Subtitle 「别只看涨25%这半句」 30pt amber,
Core number zone occupying ~35% height: giant 「少约17%」 coral bold,
Secondary number 「涨25%」 teal smaller beside it with captions 「相对今天」 and 「相对基线」,
Below: 3 compact rows — 「临时促销|+50%|用到9/13」「永久调整|+25%|相对基线」「体感变化|-17%|相对今天」,
Then formula strip 「100 → 150 → 125」,
Then 4 action checklist lines in rounded cards,
Footer 「9月14日起生效·以官方为准」,
high-fidelity Chinese typography, crisp small text, modular dense layout, no empty decorative center, no watermark, no extra words, no logos
```

## Negative

```text
abstract empty poster, huge blank space, vague tech HUD without numbers,
illegible glyphs, watermark, brand logos, 3D chrome, purple gradient SaaS look
```
