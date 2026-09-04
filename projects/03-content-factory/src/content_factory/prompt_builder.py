"""Expand prompt library presets into full generation prompts."""

from __future__ import annotations

from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "config" / "prompt_library"

PRESETS = {
    "ai_news_data_card": "ai_news_data_card.md",
    "ai_news_high_density": "ai_news_high_density.md",
    "culture_painting_ink": "culture_painting_ink.md",
    "culture_pattern_ornament": "culture_pattern_ornament.md",
    "formula": "formula.md",
}


def list_presets() -> list[str]:
    return sorted(PRESETS)


def load_preset(name: str) -> str:
    if name not in PRESETS:
        raise KeyError(f"unknown preset: {name}; choose from {list_presets()}")
    return (LIB / PRESETS[name]).read_text(encoding="utf-8")


def extract_fenced_prompts(markdown: str) -> list[str]:
    """Return contents of ```text/``` fences (prompt bodies)."""
    chunks: list[str] = []
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("```"):
            i += 1
            buf: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            body = "\n".join(buf).strip()
            if body and not body.startswith("1. SUBJECT"):
                # keep substantial prompt-like fences
                if len(body) > 80:
                    chunks.append(body)
            i += 1
        else:
            i += 1
    return chunks


def build_prompt(preset: str, index: int = 0) -> str:
    md = load_preset(preset)
    prompts = extract_fenced_prompts(md)
    if not prompts:
        return md
    if index < 0 or index >= len(prompts):
        raise IndexError(f"preset {preset} has {len(prompts)} prompts; index={index}")
    return prompts[index]
