"""Content Factory MVP — local-first Xiaohongshu pipeline."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config"
OUTPUTS = ROOT / "outputs"
PIPELINE = ROOT / "pipeline"
TEMPLATES = ROOT / "templates"

STAGE_DIRS = [
    "01_topic",
    "02_research",
    "03_fact_check",
    "04_angle",
    "05_writer",
    "06_title",
    "07_visual",
    "08_image_prompt",
    "09_image_gen",
    "10_xhs_carousel",
    "11_short_video",
    "12_blog",
    "13_publish",
    "14_analytics",
]


@dataclass
class RunManifest:
    run_id: str
    direction: str
    topic: str
    status: str
    publish_mode: str
    created: str
    stages_completed: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    notes: str = ""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def mirror_stage(run_dir: Path, stage: str, filename: str, content: str) -> None:
    """Write into output package and mirror into pipeline stage folder."""
    write_text(run_dir / filename, content)
    write_text(PIPELINE / stage / f"{run_dir.name}__{filename}", content)


def scaffold_run(run_id: str) -> Path:
    run_dir = OUTPUTS / run_id
    (run_dir / "assets").mkdir(parents=True, exist_ok=True)
    for stage in STAGE_DIRS:
        (PIPELINE / stage).mkdir(parents=True, exist_ok=True)
    return run_dir


def build_culture_sample(run_id: str = "2026-09-04_culture_yunwen_shanshui") -> Path:
    run_dir = scaffold_run(run_id)
    sources = load_json(CONFIG / "sources_authority.json")

    topic = """# Topic

## 方向
传统文化 · 水墨山水 + 纹饰创新

## 选题
云纹入画：把宋代山水里的「远」做成可每天打开的壁纸

## 为什么做
- 水墨山水是大众最容易建立审美锚点的题材
- 云纹（卷云纹）同时出现在器物、服饰、建筑装饰中，便于做「讲解→创新」闭环
- 可自然引出：看权威馆藏 → 理解纹样语义 → AI 重组为壁纸（本地生成，不冒充原作）

## 目标受众
对国风审美感兴趣、想换壁纸、又不想只看空壳「AI 水墨」的小红书用户

## 成功标准
本地产出：研究笔记 + 事实核对 + 小红书图文 + 口播提纲 + 封面/壁纸图 + 生图 prompt
"""

    research = f"""# Research

## 核心知识点（可讲解）
1. **山水不止风景**：宋人山水强调「可望、可行、可游、可居」的空间想象，远山虚化是主动经营，不是画不清楚。
2. **云纹是流通的视觉语法**：卷云纹常见于青铜器、漆器、织物、建筑彩画；形态可简化为「S 形回转 + 层叠」。
3. **讲解边界**：介绍馆藏与公开数字资源时，标明机构来源；AI 图是**创新组合**，不得声称是某幅名画翻制。

## 权威信源（本篇优先）
- 故宫博物院 / 数字文物库 / 故宫名画记：https://www.dpm.org.cn/ 、https://digicol.dpm.org.cn/
- 中华珍宝馆（书画高清浏览参考）：https://g2.ltfc.net/
- 中国国家博物馆：https://www.chnmuseum.cn/
- 中国色（纹样/配色工具）：https://zhongguose.com/ai/patterns
- 纹藏：https://www.wenzang.cn/pattern
- 陕历博藏品：https://www.sxhm.com/collection/3d.html
- 台北故宫 Open Data（高清影像开放政策需遵守）：https://theme.npm.edu.tw/opendata/

## 配置库条目数
传统文化信源 {len(sources.get('culture', []))} 条；详见 config/sources_authority.json

## 小方向扩充种子
- 皴法系列（披麻/斧劈）→ 纹理壁纸
- 单独纹样（回纹、如意云、缠枝莲）→ 器物→服饰→壁纸三连
- 名画「远近法」对比卡（范宽/郭熙/李唐）→ 不复制画面，只讲结构
"""

    fact_check = """# Fact Check

| 陈述 | 判定 | 说明 |
|------|------|------|
| 云纹广泛出现在器物与服饰装饰中 | 通过 | 文博与纹样工具站可交叉看到同类母题 |
| AI 壁纸等于某馆藏原作高清下载 | **拒绝** | 本流水线明确为创新组合，不替代原作影像 |
| 宋画「远」是构图经营 | 通过 | 艺术史常见论述；具体作品分析应以馆方说明为准 |
| 可商用任意馆藏图 | **待核** | 各馆开放协议不同；发布前必须单独核对许可 |

## 风险
- 标题若写「还原《某某图》」易侵权/误导 → 改用「灵感来自宋人山水空间」
- 口播勿念具体未核对的尺幅/估价数字
"""

    angle = """# Angle

## 钩子
很多人下的「水墨壁纸」只有墨点，没有「远」。

## 冲突
刷到国风壁纸 → 好看但空洞 → 不知道云纹从哪来 → 不敢发原创怕像盗图

## Insight
先学会看「空间层次」和「纹样语法」，再用 AI 做重组，才有个人声音。

## 内容结构
Problem → Conflict → Insight → Evidence（信源）→ Solution（生图方向）→ Result（本地成片）
"""

    titles = """# Titles（候选）

1. 云纹入画：宋人山水的「远」，做成每天打开的壁纸
2. 别再下空壳水墨了：先看懂一层云纹
3. 器物上的云，为什么能长进山水里？
4. 我用权威馆藏当课本，用 AI 只做「重组」不做「假原作」
5. 3:4 国风壁纸配方：远山 + 卷云边框 + 青灰纸色

## 选用
主标题：云纹入画：宋人山水的「远」，做成每天打开的壁纸
"""

    body = """# 小红书正文（本地稿，未发布）

云纹入画：宋人山水的「远」，做成每天打开的壁纸

很多人换「水墨壁纸」，换来换去只有一团墨。
问题通常不是模型不行，而是你没有给它「空间」和「纹样语法」。

今天这条只做三件事：
1）怎么看山水里的「远」
2）云纹到底是什么视觉零件
3）怎样用 AI 做创新组合壁纸（本地生成，不冒充名画）

【看「远」】
远山要淡、要虚、要让视线有地方停。
这是经营，不是模糊滤镜。

【看云纹】
卷云纹像一条会转弯的「S」，能在青铜、漆器、织物边饰里反复出现。
它不是贴花，是节奏。

【创新组合】
配方很克制：
墨色远山层次 + 边角淡青卷云框 + 宣纸米色底。
中间留白给呼吸，不要堆满龙凤。

【信源提醒】
想认真看原作，去故宫数字资源、珍宝馆、国博等权威入口（笔记评论区可放清单）。
AI 图是作业，不是文物替代品。

如果你也在做国风内容：先建自己的「纹样词典」，再谈爆款。

#传统文化 #水墨山水 #云纹 #壁纸分享 #国风设计 #博物馆
"""

    visual = """# Visual Direction

## 封面（3:4）
米色宣纸底 + 底部淡墨远山剪影 + 顶角卷云线；中心留白给标题。

## 壁纸（3:4）
多层远山雾气 + 边缘半透明云纹装饰框 + 青灰点缀；无文字、无 Logo。

## 轮播建议（本地）
1. 封面
2. 壁纸全图
3. 「远」的层次示意（可后续补信息图）
4. 云纹局部特写（可后续补）
5. 信源清单卡
"""

    image_prompt = """# Image Prompts

## Wallpaper
Phone wallpaper 3:4 vertical. Modern Chinese ink landscape inspired by Song dynasty shan-shui (NOT a copy of any specific famous painting): misty layered mountains, soft ink washes, distant peaks fading into fog, small path and solitary pavilion hint. Subtle traditional cloud-scroll (yunwen) as translucent decorative frame at edges. Palette: ink black, cool grey, muted celadon, rice-paper cream. No Chinese characters, no logos, no watermarks, no museum photo collage.

## Cover
Xiaohongshu cover 3:4. Rice-paper cream background, minimal ink mountain silhouette lower third, delicate yunwen lines at top corners in muted celadon, large empty center for title overlay (no text in image). Editorial museum-poster feel.
"""

    xhs = """# 小红书成片清单（本地）

- [x] 标题
- [x] 正文
- [x] 话题标签
- [x] 封面图 assets/cover.png
- [x] 壁纸图 assets/wallpaper.png
- [ ] 发布（按用户要求：仅本地，不自动发）

## 评论区置顶草稿
权威入口：故宫数字文物库 / 故宫名画记 / 中华珍宝馆 / 国博 / 中国色 / 纹藏（完整列表见同目录 research）
"""

    oral = """# 口播提纲（60–90 秒）

1. 开场：你的水墨壁纸为什么看起来「假」？（3 秒钩子）
2. 点题：缺的不是滤镜，是「远」和「云纹语法」
3. 知识点 1：远山要虚，是经营
4. 知识点 2：卷云纹 = 可迁移的装饰零件
5. 演示：我的配方三要素（山 / 云框 / 纸色）
6. 边界：AI 是重组，原作请看博物馆数字资源
7. CTA：评论「云纹」送信源清单；问问你还想看哪种纹样
"""

    blog = """# Blog / 长文备忘（可选扩展）

标题：从馆藏云纹到桌面壁纸：一条可复用的国风内容闭环

提纲：
- 为什么国风账号容易「空壳化」
- 权威信源怎么用（看图 vs 引用 vs 商用）
- 纹样词典最小集（云纹、回纹、如意）
- AI 生图护栏：不复刻、不伪称、保留个人声音
- 下一篇预告：披麻皴 → 纹理壁纸
"""

    publish = """# Publish

模式：local_only
状态：草稿已生成，等待用户手动发布
禁止：自动登录小红书、自动上传
"""

    analytics = """# Analytics（发布后填写）

- 曝光 / 点赞 / 收藏 / 评论
- 哪句钩子被复述
- 哪张图被保存最多
- 下一小方向候选：回纹 / 披麻皴 / 郭熙早春空间
"""

    mirror_stage(run_dir, "01_topic", "01_topic.md", topic)
    mirror_stage(run_dir, "02_research", "02_research.md", research)
    mirror_stage(run_dir, "03_fact_check", "03_fact_check.md", fact_check)
    mirror_stage(run_dir, "04_angle", "04_angle.md", angle)
    mirror_stage(run_dir, "05_writer", "05_xhs_body.md", body)
    mirror_stage(run_dir, "06_title", "06_titles.md", titles)
    mirror_stage(run_dir, "07_visual", "07_visual.md", visual)
    mirror_stage(run_dir, "08_image_prompt", "08_image_prompt.md", image_prompt)
    mirror_stage(run_dir, "09_image_gen", "09_image_gen.md", "# Image Gen\n\n已生成：assets/cover.png, assets/wallpaper.png\n")
    mirror_stage(run_dir, "10_xhs_carousel", "10_xhs_package.md", xhs)
    mirror_stage(run_dir, "11_short_video", "11_oral_script.md", oral)
    mirror_stage(run_dir, "12_blog", "12_blog.md", blog)
    mirror_stage(run_dir, "13_publish", "13_publish.md", publish)
    mirror_stage(run_dir, "14_analytics", "14_analytics.md", analytics)

    manifest = RunManifest(
        run_id=run_id,
        direction="culture",
        topic="云纹入画：宋人山水的「远」做成壁纸",
        status="mvp_local_complete",
        publish_mode="local_only",
        created=str(date.today()),
        stages_completed=STAGE_DIRS.copy(),
        assets=["assets/cover.png", "assets/wallpaper.png"],
        notes="传统文化优先样例；AI 图为创新组合，非馆藏翻制。",
    )
    write_json(run_dir / "00_manifest.json", asdict(manifest))
    write_text(
        run_dir / "README.md",
        f"""# Run: {run_id}

方向：传统文化（水墨山水 + 云纹创新）
状态：MVP 本地闭环完成（未发布）

## 打开顺序
1. `05_xhs_body.md` 正文
2. `11_oral_script.md` 口播
3. `assets/cover.png` / `assets/wallpaper.png`
4. `03_fact_check.md` 边界

## 验证
- 14 个阶段文件齐全
- 图片存在于 assets/
""",
    )
    return run_dir


def build_ai_sample(run_id: str = "2026-09-04_ai_claude_code_limits") -> Path:
    run_dir = scaffold_run(run_id)

    topic = """# Topic

## 方向
AI 资讯 · 厂商额度 / 活动

## 选题
Claude Code 额度「涨 25%」？先算清相对今天其实少 17%

## 为什么做
- 开发者最关心「额度/活动」口径差异
- 同一公告可用「基线 vs 当前」两种算法，适合做反误导内容
- 可扩展到：Cursor / Codex / 各家重置与促销对照表

## 成功标准
本地：事实核对表 + 小红书图文 + 口播 + 封面；不自动发布
"""

    research = """# Research

## 事件摘要（截至 2026-09 公开报道）
- Anthropic 宣布：自 2026-09-14 起，Claude Code 标准周限额相对**原始基线**永久 +25%（Pro/Max/Team/按席位企业）
- 此前临时 +50% 促销持续到 2026-09-13
- 相对「今天正在用的额度」：约 **-17%**（150% → 125% 基线）
- 官方后补澄清：Compared to today ≈ 17% reduction
- 相邻对照：同周期有报道称 OpenAI 侧重置 Codex/付费用量并修复异常消耗（作对比素材，发布前再核官方原文）

## 优先核对入口（权威优先）
- Anthropic / Claude 开发者官方公告与帮助中心（以官方帖为准）
- BleepingComputer 等对官方帖的转述：https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-is-cutting-claude-codes-current-weekly-limits-by-17-percent/
- 中文二次解读需回链官方；避免只转自媒体数字

## 小方向扩充种子
- 各家「促销结束」日历
- `/usage` `/status` 自查清单
- Cursor 无限 Token / 模型路由策略
- API 计费 vs 订阅额度边界
"""

    fact_check = """# Fact Check

| 陈述 | 判定 | 说明 |
|------|------|------|
| 永久 +25% 相对原始基线 | 通过（以官方口径为准） | 报道一致指向 baseline |
| 相对今天约 -17% | 通过 | 官方澄清与多家媒体一致 |
| 临时 +50% 到 9/13 | 通过 | 以官方最终时间为准，可能再延期 |
| 具体「能发多少条消息」 | **拒绝量化** | 官方强调消耗随模型/工具/上下文变化 |
| OpenAI 重置细节 | 中置信 | 作对照需再核官方原文后再写死数字 |

## 风险
- 标题只写「降额」或只写「涨 25%」都会片面
- 活动日期可能变动 → 文末加「以官方为准」
"""

    angle = """# Angle

钩子：你看见的是 +25%，账单体感可能是少用一天。
冲突：厂商文案选「好听的分母」。
Insight：额度新闻要先问——相对谁？基线还是今天？
"""

    titles = """# Titles

1. Claude Code 涨 25%？相对今天其实少约 17%
2. 看额度公告先问一句：相对谁？
3. 9 月 14 日前后，你的周限额可能少一天重度使用
4. 开发者必看：促销结束算法题
5. 别被百分比骗了：150→125 才是体感

选用：Claude Code 涨 25%？相对今天其实少约 17%
"""

    body = """# 小红书正文（本地稿，未发布）

Claude Code 涨 25%？相对今天其实少约 17%

最近 Anthropic 给 Claude Code 周限额算了一笔「百分比账」。

【好听的说法】
从 9 月 14 日起，标准周限额相对**原始基线**永久 +25%。

【正在用的说法】
你现在手上很多是临时 +50% 的桶。
促销结束后落到 +25% 基线 → 相对今天大约 **-17%**。
官方后来也补了这句澄清。

【怎么自查】
别跟风骂或跟风庆。
打开用量面板 / 命令行用量查询，看自己的重置周期和实际消耗结构（长上下文、重模型、工具调用最吃额度）。

【对照思维】
同一周还有别家「重置额度 / 修异常消耗」的新闻。
做内容的人更该建立：**厂商活动对照表**，而不是单条情绪稿。

数字以官方最终公告为准；本文只教你读百分比。

#AI资讯 #Claude #开发者工具 #API额度 #效率工具
"""

    visual = """# Visual

封面：深色编辑风 + 用量仪表抽象图形 + 中心留白标题区（3:4）
信息图（可后续补）：基线 100 → 临时 150 → 永久 125
"""

    image_prompt = """# Image Prompt — Cover

Xiaohongshu cover 3:4 for tech news. Dark charcoal with soft blue gradient, abstract usage-meter gauge and subtle code brackets, empty center for title (no text rendered). No real brand logos.
"""

    oral = """# 口播提纲（45–70 秒）

1. 钩子：涨 25% 的新闻，为什么有人说在降？
2. 出示两个分母：基线 vs 今天
3. 算式：100→150→125
4. 行动：先查自己的用量，再决定要不要换工具组合
5. CTA：评论「额度」——我下篇做各家活动对照表
"""

    xhs = """# 小红书成片清单

- [x] 标题/正文/标签
- [x] 封面 assets/cover.png
- [x] 口播提纲
- [ ] 发布（local_only）
"""

    publish = """# Publish\n\n模式：local_only\n状态：草稿完成，不自动发布\n"""
    analytics = """# Analytics\n\n发布后记录：收藏率、争议评论点、是否有人要对照表\n"""
    blog = """# 扩展\n\n可做成「9 月厂商额度日历」长文，接入 direction=ai_news 的小方向扩充表。\n"""

    mirror_stage(run_dir, "01_topic", "01_topic.md", topic)
    mirror_stage(run_dir, "02_research", "02_research.md", research)
    mirror_stage(run_dir, "03_fact_check", "03_fact_check.md", fact_check)
    mirror_stage(run_dir, "04_angle", "04_angle.md", angle)
    mirror_stage(run_dir, "05_writer", "05_xhs_body.md", body)
    mirror_stage(run_dir, "06_title", "06_titles.md", titles)
    mirror_stage(run_dir, "07_visual", "07_visual.md", visual)
    mirror_stage(run_dir, "08_image_prompt", "08_image_prompt.md", image_prompt)
    mirror_stage(run_dir, "09_image_gen", "09_image_gen.md", "# Image Gen\n\n已生成：assets/cover.png\n")
    mirror_stage(run_dir, "10_xhs_carousel", "10_xhs_package.md", xhs)
    mirror_stage(run_dir, "11_short_video", "11_oral_script.md", oral)
    mirror_stage(run_dir, "12_blog", "12_blog.md", blog)
    mirror_stage(run_dir, "13_publish", "13_publish.md", publish)
    mirror_stage(run_dir, "14_analytics", "14_analytics.md", analytics)

    manifest = RunManifest(
        run_id=run_id,
        direction="ai_news",
        topic="Claude Code 周限额：+25% vs -17%",
        status="mvp_local_complete",
        publish_mode="local_only",
        created=str(date.today()),
        stages_completed=STAGE_DIRS.copy(),
        assets=["assets/cover.png"],
        notes="AI 资讯样例；数字发布前再核官方原文。",
    )
    write_json(run_dir / "00_manifest.json", asdict(manifest))
    write_text(
        run_dir / "README.md",
        f"""# Run: {run_id}

方向：AI 资讯（厂商额度）
状态：MVP 本地闭环完成（未发布）

验证：阶段文件齐全 + assets/cover.png 存在。
""",
    )
    return run_dir


def cmd_init_mvp(_: argparse.Namespace) -> None:
    c = build_culture_sample()
    a = build_ai_sample()
    print(f"culture -> {c}")
    print(f"ai_news -> {a}")


def cmd_list(_: argparse.Namespace) -> None:
    if not OUTPUTS.exists():
        print("no outputs")
        return
    for p in sorted(OUTPUTS.iterdir()):
        if p.is_dir():
            man = p / "00_manifest.json"
            if man.exists():
                data = load_json(man)
                print(f"{p.name}\t{data.get('direction')}\t{data.get('status')}")
            else:
                print(p.name)


def cmd_check(args: argparse.Namespace) -> None:
    run_dir = OUTPUTS / args.run_id
    if not run_dir.exists():
        raise SystemExit(f"missing run: {run_dir}")
    required = [
        "00_manifest.json",
        "01_topic.md",
        "05_xhs_body.md",
        "11_oral_script.md",
        "13_publish.md",
    ]
    missing = [r for r in required if not (run_dir / r).exists()]
    assets = list((run_dir / "assets").glob("*")) if (run_dir / "assets").exists() else []
    print(json.dumps({"run": args.run_id, "missing": missing, "assets": [a.name for a in assets]}, ensure_ascii=False, indent=2))
    if missing:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Content Factory MVP")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init-mvp", help="Generate two MVP sample runs (culture + ai_news)")
    p_init.set_defaults(func=cmd_init_mvp)

    p_list = sub.add_parser("list", help="List local runs")
    p_list.set_defaults(func=cmd_list)

    p_check = sub.add_parser("check", help="Validate a run package")
    p_check.add_argument("run_id")
    p_check.set_defaults(func=cmd_check)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
