# AI 资讯 · 高密内页（轮播 2–N）

改编自 [AJ OpenClaw 小红书信息图 Skills](https://yuanchang.org/en/posts/aj-openclaw-skills-prompt-xiaohongshu-infographic/)

## 原则

- **每张图 6–7 个模块**，密优于空
- 每模块要有：短标题 + 具体数字/口径 + 一句解释
- 警告区：深底浅字，单独强调

## Prompt 骨架

```text
Create a high-density Xiaohongshu infographic about「[主题]」, 3:4 portrait.

【LAYOUT】
- MUST include 6-7 distinct modules
- Compact spacing, information as coordinates
- Massive bold key numbers vs tiny annotations

【MODULES】
1. 主题条
2. 口径 A（相对基线）
3. 口径 B（相对今天）
4. 时间线
5. 消耗因素
6. 行动清单
7. 免责/来源条

【COLOR】 dark navy editorial OR cream Morandi (pick one, keep consistent)
【TEXT】 Chinese in 「」, specify hierarchy: title 48pt / module title 28pt / body 18pt
high-fidelity typography, crisp text, no watermark, no duplicate words
```

本仓内页也可用 Pillow 扩展；未实现前先用此模板人工/外部模型生成。
