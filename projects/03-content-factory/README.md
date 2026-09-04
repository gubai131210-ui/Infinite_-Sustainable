# 03 — AI Content Factory

**状态：MVP 迭代中**

## 本轮修正

1. **AI 资讯封面**：改为密排版（双栏对比 / 100→150→125 / 时间线 / 行动清单），保留深色蓝配色。  
   `outputs/2026-09-04_ai_claude_code_limits/assets/cover.jpg`
2. **传统文化分轨**  
   - 只讲画：`outputs/2026-09-04_culture_shanshui_yuan/`  
   - 只讲纹饰组合：`outputs/2026-09-04_culture_pattern_yunwen_huiwen/`（回纹×卷云，**无山水**）  
   - 旧混搭：`culture_yunwen_shanshui` 仍为 DEPRECATED

## 本地请你打开看

```text
outputs\2026-09-04_ai_claude_code_limits\assets\cover.jpg
outputs\2026-09-04_culture_pattern_yunwen_huiwen\assets\cover.jpg
outputs\2026-09-04_culture_pattern_yunwen_huiwen\assets\wallpaper.jpg
outputs\2026-09-04_culture_shanshui_yuan\assets\cover.jpg
```

## 重渲染

```powershell
cd "d:\Infinite_ Sustainable\projects\03-content-factory"
python scripts\render_ai_news_cover.py
python scripts\render_pattern_yunwen_huiwen.py
```

## 禁止偷懒

- 禁止 AI 资讯大留白空洞图
- 禁止纹饰篇混入山水
- 禁止讲画篇加纹样边框当「高级感」
- 禁止自动发布
