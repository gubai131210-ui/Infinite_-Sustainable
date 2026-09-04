"""Content Factory MVP — local-first Xiaohongshu pipeline."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config"
OUTPUTS = ROOT / "outputs"
PIPELINE = ROOT / "pipeline"
SCRIPTS = ROOT / "scripts"

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

RULE_ONE_CULTURE_SUBDIR = (
    "culture painting and pattern must be separate runs; never mix in one post or one image"
)
RULE_AI_NEWS_TYPOGRAPHY = (
    "AI news cover must put key numbers/facts on the image via typography render"
)


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
    write_text(run_dir / filename, content)
    write_text(PIPELINE / stage / f"{run_dir.name}__{filename}", content)


def scaffold_run(run_id: str) -> Path:
    run_dir = OUTPUTS / run_id
    (run_dir / "assets").mkdir(parents=True, exist_ok=True)
    for stage in STAGE_DIRS:
        (PIPELINE / stage).mkdir(parents=True, exist_ok=True)
    return run_dir


def render_ai_news_cover() -> None:
    script = SCRIPTS / "render_ai_news_cover.py"
    subprocess.check_call([sys.executable, str(script)])


def build_culture_painting_sample(run_id: str = "2026-09-04_culture_shanshui_yuan") -> Path:
    """Painting-only sample. Pattern content belongs in a separate run."""
    run_dir = scaffold_run(run_id)

    files = {
        ("01_topic", "01_topic.md"): """# Topic

## 大方向
传统文化

## 本篇小方向（单选）
**山水画讲解**（本篇不讲纹饰）

## 选题
宋人山水的「远」：先学会看空间，再谈壁纸

## 明确不做
- 不讲云纹/回纹/服饰器物纹样
- 封面与壁纸不做「画 + 纹饰」混搭
""",
        ("02_research", "02_research.md"): """# Research

## 本篇只讲「画」
宋人山水的「远」是空间经营：远山淡、虚、有停靠。

## 权威信源（看画）
故宫数字文物库 / 名画记、中华珍宝馆、国博、上博、台北故宫 Open Data。

纹饰另开 run。
""",
        ("03_fact_check", "03_fact_check.md"): """# Fact Check

| 陈述 | 判定 |
|------|------|
| 本篇同时讲解纹饰 | 拒绝 |
| AI 壁纸 = 名画复制 | 拒绝 |
""",
        ("04_angle", "04_angle.md"): """# Angle

钩子：水墨壁纸为什么只有一团墨？
Insight：先看近—中—远；纹饰下次单独讲。
""",
        ("05_writer", "05_xhs_body.md"): """# 小红书正文（本地稿，未发布）

宋人山水的「远」：先学会看，再谈壁纸

今天这条**只讲画**，不讲纹饰。

【怎么看「远」】
近处可辨、中景可游、远山要虚。

【壁纸】
本地图是山水氛围参考，不是名画复制件。

纹饰下次单独做，不混在一张图里。

#传统文化 #水墨山水 #宋画 #壁纸分享
""",
        ("06_title", "06_titles.md"): """# Titles

选用：宋人山水的「远」：先学会看，再谈壁纸
""",
        ("07_visual", "07_visual.md"): """# Visual

硬规则：纯山水；禁止纹样边框/器物装饰混搭。
""",
        ("08_image_prompt", "08_image_prompt.md"): """# Image Prompts

Pure ink landscape only. NO decorative patterns, NO cloud-scroll frames, NO textile motifs.
""",
        ("09_image_gen", "09_image_gen.md"): """# Image Gen

assets/cover.jpg, assets/wallpaper.jpg（纯山水）
""",
        ("10_xhs_carousel", "10_xhs_package.md"): """# 小红书成片清单

- [x] 正文（只讲画）
- [x] assets/cover.jpg
- [x] assets/wallpaper.jpg
- [ ] 发布 local_only
""",
        ("11_short_video", "11_oral_script.md"): """# 口播提纲

1. 只讲画，不讲纹饰
2. 近—中—远
3. 壁纸是氛围参考
4. CTA：要纹饰评论「纹饰」
""",
        ("12_blog", "12_blog.md"): """# Blog

单篇讲画，不混纹饰。
""",
        ("13_publish", "13_publish.md"): """# Publish

local_only
""",
        ("14_analytics", "14_analytics.md"): """# Analytics

记录是否仍有人要求画+纹饰同图。
""",
    }
    for (stage, name), content in files.items():
        mirror_stage(run_dir, stage, name, content)

    manifest = RunManifest(
        run_id=run_id,
        direction="culture_painting",
        topic="宋人山水的「远」",
        status="mvp_local_complete",
        publish_mode="local_only",
        created=str(date.today()),
        stages_completed=STAGE_DIRS.copy(),
        assets=["assets/cover.jpg", "assets/wallpaper.jpg"],
        notes=RULE_ONE_CULTURE_SUBDIR,
    )
    write_json(run_dir / "00_manifest.json", asdict(manifest))
    write_text(run_dir / "README.md", f"# Run: {run_id}\n\n只讲山水画。旧混搭 yunwen 样例已废弃。\n")
    return run_dir


def build_ai_sample(run_id: str = "2026-09-04_ai_claude_code_limits") -> Path:
    run_dir = scaffold_run(run_id)

    files = {
        ("01_topic", "01_topic.md"): """# Topic

## 方向
AI 资讯 · 厂商额度

## 选题
Claude Code 额度：涨 25%？相对今天少约 17%

## 视觉硬规则
封面必须信息上图（标题/关键数字/对照行/生效日），禁止无信息抽象图。
""",
        ("02_research", "02_research.md"): """# Research

相对基线永久 +25%；临时 +50% 至 9/13；相对今天约 -17%。以官方公告为准。
""",
        ("03_fact_check", "03_fact_check.md"): """# Fact Check

| 陈述 | 判定 |
|------|------|
| 相对基线 +25% | 通过（核官方） |
| 相对今天约 -17% | 通过（核官方） |
| 能换算成固定对话条数 | 拒绝量化 |
""",
        ("04_angle", "04_angle.md"): """# Angle

先问：相对谁？
""",
        ("05_writer", "05_xhs_body.md"): """# 小红书正文（本地稿，未发布）

Claude Code 涨 25%？相对今天其实少约 17%

你会同时看到两种说法：
- 涨 25%：相对原始基线
- 少约 17%：相对今天临时 +50% 的额度

封面已把对照表排进图里。数字以官方最终公告为准。

#AI资讯 #Claude #开发者工具 #API额度
""",
        ("06_title", "06_titles.md"): """# Titles

选用：Claude Code 涨 25%？相对今天其实少约 17%
""",
        ("07_visual", "07_visual.md"): """# Visual

使用 scripts/render_ai_news_cover.py 输出信息图封面。
必须包含：标题、+25%、-17%、三行对照、生效说明。
""",
        ("08_image_prompt", "08_image_prompt.md"): """# Image

Typography poster via Pillow，不是抽象装饰图。
""",
        ("09_image_gen", "09_image_gen.md"): """# Image Gen

assets/cover.jpg（信息排版）
""",
        ("10_xhs_carousel", "10_xhs_package.md"): """# Package

- [x] cover.jpg 信息图
- [ ] 发布 local_only
""",
        ("11_short_video", "11_oral_script.md"): """# 口播

1. 两种说法 2. 算式 3. 先查自己用量
""",
        ("12_blog", "12_blog.md"): """# Blog

可扩厂商额度对照表。
""",
        ("13_publish", "13_publish.md"): """# Publish

local_only
""",
        ("14_analytics", "14_analytics.md"): """# Analytics

收藏率 / 要对照表的评论
""",
    }
    for (stage, name), content in files.items():
        mirror_stage(run_dir, stage, name, content)

    render_ai_news_cover()

    manifest = RunManifest(
        run_id=run_id,
        direction="ai_news",
        topic="Claude Code 周限额口径",
        status="mvp_local_complete",
        publish_mode="local_only",
        created=str(date.today()),
        stages_completed=STAGE_DIRS.copy(),
        assets=["assets/cover.jpg"],
        notes=RULE_AI_NEWS_TYPOGRAPHY,
    )
    write_json(run_dir / "00_manifest.json", asdict(manifest))
    write_text(run_dir / "README.md", f"# Run: {run_id}\n\n封面为信息排版图，见 assets/cover.jpg\n")
    return run_dir


def cmd_init_mvp(_: argparse.Namespace) -> None:
    c = build_culture_painting_sample()
    a = build_ai_sample()
    print(f"culture_painting -> {c}")
    print(f"ai_news -> {a}")
    print("NOTE:", RULE_ONE_CULTURE_SUBDIR)
    print("NOTE:", RULE_AI_NEWS_TYPOGRAPHY)


def cmd_list(_: argparse.Namespace) -> None:
    if not OUTPUTS.exists():
        print("no outputs")
        return
    for p in sorted(OUTPUTS.iterdir()):
        if p.is_dir():
            man = p / "00_manifest.json"
            deprecated = (p / "DEPRECATED.md").exists()
            flag = " DEPRECATED" if deprecated else ""
            if man.exists():
                data = load_json(man)
                print(f"{p.name}\t{data.get('direction')}\t{data.get('status')}{flag}")
            else:
                print(f"{p.name}{flag}")


def cmd_check(args: argparse.Namespace) -> None:
    run_dir = OUTPUTS / args.run_id
    if not run_dir.exists():
        raise SystemExit(f"missing run: {run_dir}")
    if (run_dir / "DEPRECATED.md").exists():
        raise SystemExit(f"run deprecated: {args.run_id}")
    required = [
        "00_manifest.json",
        "01_topic.md",
        "03_fact_check.md",
        "05_xhs_body.md",
        "11_oral_script.md",
        "13_publish.md",
    ]
    missing = [r for r in required if not (run_dir / r).exists()]
    assets = list((run_dir / "assets").glob("*")) if (run_dir / "assets").exists() else []
    publish_mode = None
    if (run_dir / "00_manifest.json").exists():
        publish_mode = load_json(run_dir / "00_manifest.json").get("publish_mode")
    print(
        json.dumps(
            {
                "run": args.run_id,
                "missing": missing,
                "assets": [a.name for a in assets],
                "publish_mode": publish_mode,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if missing or publish_mode not in (None, "local_only"):
        if publish_mode not in (None, "local_only"):
            raise SystemExit(f"unexpected publish_mode: {publish_mode}")
        raise SystemExit(1)
    if not assets:
        raise SystemExit("no assets in run package")


def cmd_render_ai(_: argparse.Namespace) -> None:
    render_ai_news_cover()


def cmd_build_prompt(args: argparse.Namespace) -> None:
    from .prompt_builder import build_prompt, list_presets, load_preset

    if args.list:
        print("\n".join(list_presets()))
        return
    if args.raw:
        print(load_preset(args.preset))
        return
    print(build_prompt(args.preset, index=args.index))


def cmd_render_pattern(_: argparse.Namespace) -> None:
    script = SCRIPTS / "render_pattern_yunwen_huiwen.py"
    subprocess.check_call([sys.executable, str(script)])


def main() -> None:
    parser = argparse.ArgumentParser(description="Content Factory MVP")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init-mvp", help="Refresh painting + AI news MVP samples")
    p_init.set_defaults(func=cmd_init_mvp)

    p_list = sub.add_parser("list", help="List local runs")
    p_list.set_defaults(func=cmd_list)

    p_check = sub.add_parser("check", help="Validate a run package")
    p_check.add_argument("run_id")
    p_check.set_defaults(func=cmd_check)

    p_render = sub.add_parser("render-ai-cover", help="Re-render AI news data-card cover")
    p_render.set_defaults(func=cmd_render_ai)

    p_pat = sub.add_parser("render-pattern", help="Re-render programmatic pattern assets")
    p_pat.set_defaults(func=cmd_render_pattern)

    p_prompt = sub.add_parser("build-prompt", help="Print a prompt library preset")
    p_prompt.add_argument("preset", nargs="?", default="culture_painting_ink")
    p_prompt.add_argument("--index", type=int, default=0)
    p_prompt.add_argument("--list", action="store_true")
    p_prompt.add_argument("--raw", action="store_true", help="print full markdown file")
    p_prompt.set_defaults(func=cmd_build_prompt)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
