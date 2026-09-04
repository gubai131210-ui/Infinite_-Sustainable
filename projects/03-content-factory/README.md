# 03 — AI Content Factory

**状态：MVP 迭代中（本地闭环；已按反馈修正视觉规则）**

## 最新纠正（2026-09-04）

1. **AI 资讯图**：必须把人们关心的信息排进图（数字/口径/时间），使用 `scripts/render_ai_news_cover.py` 字体排版。  
   见：`outputs/2026-09-04_ai_claude_code_limits/assets/cover.jpg`
2. **传统文化**：画 与 纹饰 是两条线，一次只讲一个；图禁止画+纹饰混搭。  
   讲画样例：`outputs/2026-09-04_culture_shanshui_yuan/`  
   旧混搭：`outputs/2026-09-04_culture_yunwen_shanshui/`（已 DEPRECATED）

## 本次约定

| 项 | 选择 |
|----|------|
| 深度 | MVP |
| 发布 | 仅本地 |
| 优先 | 传统文化讲画；纹饰另开 |

## 请你本地打开验证

```text
projects\03-content-factory\outputs\2026-09-04_ai_claude_code_limits\assets\cover.jpg
projects\03-content-factory\outputs\2026-09-04_culture_shanshui_yuan\assets\cover.jpg
projects\03-content-factory\outputs\2026-09-04_culture_shanshui_yuan\assets\wallpaper.jpg
projects\03-content-factory\outputs\2026-09-04_culture_shanshui_yuan\05_xhs_body.md
```

## 重渲染 AI 封面

```powershell
cd "d:\Infinite_ Sustainable\projects\03-content-factory"
python scripts\render_ai_news_cover.py
```

## 禁止偷懒

- 禁止 AI 资讯封面只有抽象装饰没有新闻信息
- 禁止同篇把山水画和纹饰混讲、混生图
- 禁止自动发布
- 禁止继续使用已 DEPRECATED 的混搭样例当正稿
