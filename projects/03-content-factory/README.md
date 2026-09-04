# 03 — AI Content Factory

**状态：MVP（已接入网研提示词库 + 数据卡排版）**

## 本轮升级

1. 新增提示词库：`config/prompt_library/`（6 槽公式、资讯数据卡、高密模块、水墨、纯纹饰）
2. AI 资讯封面按 **Data Card** 契约重排：核心大数字区约占 30% 屏高 + 3 行数据 + 换算条 + 行动清单  
   → `outputs/2026-09-04_ai_claude_code_limits/assets/cover_data_card.jpg`
3. 用详细提示词重生成：
   - 讲画：`culture_shanshui_yuan/assets/`（三远 + 留白 + 朱文印）
   - 讲纹饰：`culture_pattern_yunwen_huiwen/assets/wallpaper.jpg`（纯纹样，无山水）

## 调研来源（摘要）

- SurePrompts 6-Part Formula  
- Apiyi 小红书 Data Visualization Card  
- AJ OpenClaw 高密 6–7 模块  
- YiceKit：资讯中文优先后期/程序排版  
- AI Tools Guidebook 水墨山水 Prompt  

完整链接见 `config/prompt_library/README.md`。

## 本地请打开

```text
config\prompt_library\
outputs\2026-09-04_ai_claude_code_limits\assets\cover_data_card.jpg
outputs\2026-09-04_culture_shanshui_yuan\assets\cover.jpg
outputs\2026-09-04_culture_pattern_yunwen_huiwen\assets\wallpaper.jpg
```

## 命令

```powershell
cd "d:\Infinite_ Sustainable\projects\03-content-factory"
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m content_factory build-prompt --list
python -m content_factory render-ai-cover
python -m content_factory render-pattern
```

## 禁止偷懒

- 禁止一句话空提示词出图
- 禁止资讯封面大留白无数字
- 禁止画/纹饰提示词混用
- 禁止自动发布
