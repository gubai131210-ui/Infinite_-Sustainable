# Capture six-zone golden screenshots (P14). Run from PowerShell.
# Godot 4.6 must be on PATH as `godot` OR set $GodotExe.

$ErrorActionPreference = "Stop"
$Project = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
# scripts live in perfect-game/tools → project is parent
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$GodotExe = $env:GODOT_EXE
if (-not $GodotExe) {
  $GodotExe = (Get-Command godot -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source)
}
if (-not $GodotExe) {
  Write-Host "Set GODOT_EXE to your Godot 4.6 console executable, then re-run."
  Write-Host "Example: `$env:GODOT_EXE = 'C:\Godot\Godot_v4.6.1-stable_win64_console.exe'"
  exit 1
}
Write-Host "Using $GodotExe"
& $GodotExe --path $Project -- --capture_golden
Write-Host "Check assets/qa/golden/*.png"
