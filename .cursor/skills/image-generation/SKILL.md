# Skill: Image Generation（已接线 Prompt Library）

**状态：MVP**

## 原则（来自网研）

1. 用 **6 槽公式**：Subject / Style / Lighting / Composition / Mood / Technical + Negative  
   见 `projects/03-content-factory/config/prompt_library/formula.md`
2. **AI 资讯中文**：优先程序排版 `render_ai_news_cover.py`（数据卡契约），不要用空洞抽象图
3. **讲画 / 讲纹饰** 分预设，禁止混用

## 展开提示词

```powershell
cd "d:\Infinite_ Sustainable\projects\03-content-factory"
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m content_factory build-prompt --list
python -m content_factory build-prompt culture_painting_ink
python -m content_factory build-prompt culture_pattern_ornament
python -m content_factory build-prompt ai_news_data_card --raw
```

## 关联

- Prompt library: `projects/03-content-factory/config/prompt_library/`
- Content Agent: `prompts/04-domain/content.md`
