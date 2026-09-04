# 在仓库根或本目录执行前，请你本地确认路径
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..
$env:PYTHONPATH = (Resolve-Path ".\src").Path
python -m content_factory init-mvp
python -m content_factory list
python -m content_factory check 2026-09-04_culture_yunwen_shanshui
python -m content_factory check 2026-09-04_ai_claude_code_limits
