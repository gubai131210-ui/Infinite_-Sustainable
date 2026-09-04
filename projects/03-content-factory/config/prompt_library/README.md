# 生图提示词库（Prompt Library）

本目录把网上已验证的写法沉淀进 Content Factory，禁止再写「一句话随便生成」。

## 来源（调研）

| 主题 | 来源 | 吸收点 |
|------|------|--------|
| 通用 6 槽公式 | [SurePrompts 2026 Guide](https://sureprompts.com/blog/ai-image-prompting-complete-guide-2026) / [6-Part Formula](https://sureprompts.com/blog/how-to-write-ai-image-prompts) | Subject / Style / Lighting / Composition / Mood / Technical + Negative |
| 小红书高密信息图 | [Apiyi gpt-image-2 指南](https://help.apiyi.com/en/gpt-image-2-xiaohongshu-infographic-content-creation-guide-en.html) | Background→Subject→Details→Text→Style；字号层级；「」括中文 |
| 数据卡封面 | 同上 Data Visualization Card | 核心大数字占屏高约 40%；3 行补充数据 |
| 高密 6–7 模块 | [AJ OpenClaw 小红书信息图](https://yuanchang.org/en/posts/aj-openclaw-skills-prompt-xiaohongshu-infographic/) | 必须 6–7 模块，密优于空 |
| 封面稳妥流程 | [YiceKit 小红书提示词](https://yicekit.com/guides/xiaohongshu-ai-image-prompts/) | 资讯类：**AI 出氛围可选，中文标题优先后期/程序排版** |
| 水墨山水 | [AI Tools Guidebook 水墨 Prompt](https://aitoolsguidebook.com/zh/articles/chinese-ink-landscape-prompts/) | monochrome + 60–80% 留白 + 三远显式命名 + 禁 chinoiserie 纹样顶替山水 |
| 纹样线稿 | 电商美工网祥云教程等 | vector / clean edges / symmetrical；负向禁山水 |

## 本项目硬规则

1. **AI 资讯**：默认用 `scripts/render_ai_news_cover.py`（程序排版，中文可控）；提示词模板见 `ai_news_*.md`（若换 GPT-Image 等模型可直接套）。
2. **讲画**：只用 `culture_painting_ink.md`，禁止纹饰边框。
3. **讲纹饰**：只用 `culture_pattern_ornament.md`，禁止山水/亭台/雾气画意；纹饰×纹饰。
4. 生成前用 `python -m content_factory build-prompt --preset ...` 展开完整提示词。

## 文件

- `formula.md` — 6 槽公式与检查清单
- `ai_news_data_card.md` — 数据卡（本仓 AI 封面主模板）
- `ai_news_high_density.md` — 高密 6–7 模块（轮播内页）
- `culture_painting_ink.md` — 水墨山水详细提示词
- `culture_pattern_ornament.md` — 纯纹饰组合详细提示词
