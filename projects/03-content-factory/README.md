# 03 — AI Content Factory

**状态：MVP 进行中（本地闭环已跑通，未自动发布）**  
**优先级：第 3**

## 本次约定（已确认）

| 项 | 选择 |
|----|------|
| 深度 | MVP：双方向各 1 条完整闭环 |
| 已有资产 | 先不对接 |
| 权限 | 写代码 + MCP/网页调研 + 生图；**生成到本地，不自动发** |
| 优先 | ① 传统文化（水墨山水 + 纹饰创新） |
| 形态 | 小红书图文 + 封面/壁纸方向 + 口播提纲 |

## 闭环阶段

`01_topic` → … → `14_analytics`（见 `pipeline/`）  
成包输出在 `outputs/<run_id>/`。

## MVP 样例（请本地打开）

1. **文化优先**  
   `outputs/2026-09-04_culture_yunwen_shanshui/`  
   选题：云纹入画 · 山水「远」+ 壁纸创新  
   资产：`assets/cover.png`、`assets/wallpaper.png`

2. **AI 资讯**  
   `outputs/2026-09-04_ai_claude_code_limits/`  
   选题：Claude Code 周限额 +25% vs 相对今天 -17%  
   资产：`assets/cover.png`

## 怎么跑（请你本地执行）

因目录含中文空格，建议你在本机 PowerShell 自行测试：

```powershell
cd "d:\Infinite_ Sustainable\projects\03-content-factory"
$env:PYTHONPATH = (Resolve-Path ".\src").Path
python -m content_factory init-mvp
python -m content_factory list
python -m content_factory check 2026-09-04_culture_yunwen_shanshui
python -m content_factory check 2026-09-04_ai_claude_code_limits
```

或运行：`scripts\run_mvp.ps1`

## 关键目录

- `config/sources_authority.json` — 权威信源（持续扩充，不止初始列表）
- `config/directions.md` — 两大方向
- `research/niche_expansion.md` — 小方向扩充池
- `research/github_references.md` — 开源流程学习
- `src/content_factory/` — 流水线代码

## 禁止偷懒

- 禁止只交一篇文案就算 Factory
- 禁止跳过 Fact Check（版权 / 额度口径）
- 禁止 AI 图冒充馆藏原作
- 禁止自动发布小红书
- 禁止信源停在用户给的 6 个链接不再扩充
- 禁止把所有能力堆成单页无结构文档

## 开工前三问（下次迭代仍要问）

1. 深度？ 2. 对接资产？ 3. 是否允许发内容/新权限？
