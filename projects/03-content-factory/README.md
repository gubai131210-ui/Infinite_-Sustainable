# 03 — AI Content Factory

## 最新一轮（请你本地看这些）

### AI 资讯 · 横版四区（不再竖着挤）
`outputs/2026-09-04_ai_claude_code_limits/assets/cover_landscape.jpg`  
①事件｜②涨25%｜③少约17%｜④行动

### 水墨 · 换题江舟 + 古文楷体
`outputs/2026-09-04_culture_shanshui_jiangzhou/assets/cover.jpg`  
竖题：孤舟一葉 / 煙水蒼茫

### 纹饰 · 作用象征常用 + 落到袍服/漆盒
`outputs/2026-09-04_culture_pattern_yunwen_objects/`  
`cover.jpg` · `wallpaper.jpg` · `object_silk_robe.jpg` · `object_lacquer_box.jpg`

## 重渲染

```powershell
cd "d:\Infinite_ Sustainable\projects\03-content-factory"
python scripts\render_ai_news_cover.py
python scripts\render_ink_with_classical_text.py
python scripts\render_pattern_object_cover.py
```

提示词库：`config/prompt_library/`
