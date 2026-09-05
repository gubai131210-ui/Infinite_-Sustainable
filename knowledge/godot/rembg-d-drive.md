# Godot / 2D 资产 — rembg 本机约定（D 盘）

**状态：可用**  
**适用：** Game Factory、写实抠图、Asset Agent、`PB-Game-Visual`

## 强制约定

- **禁止**把 rembg / u2net 权重下到 `C:\Users\...\.rembg` 或 `%USERPROFILE%`
- **必须**使用工程 D 盘目录（`cursor-demo/.gitignore` 忽略 `tools/rembg_models/`，不进仓库）：

```text
projects/06-game-factory/visual_capability_probe/cursor-demo/tools/rembg_models/
  u2net.onnx              # flat，供 U2NET_HOME
  u2net/u2net.onnx        # 新布局副本
```

绝对路径示例：

`d:\Infinite_ Sustainable\projects\06-game-factory\visual_capability_probe\cursor-demo\tools\rembg_models\`

## 首次 / 补下载

```powershell
python "d:\Infinite_ Sustainable\projects\06-game-factory\visual_capability_probe\cursor-demo\tools\download_rembg_u2net.py"
```

模型：`u2net`（约 168MB）。不要默认下 bria（约 1GB）。

## 抠图（下次开发直接用）

```powershell
cd "d:\Infinite_ Sustainable\projects\06-game-factory\visual_capability_probe\cursor-demo"
$env:USE_REMBG = "1"
# 可选：$env:REMBG_MODEL = "u2net"
python .\tools\cutout_pipeline.py
```

`cutout_pipeline.py` 会在 import rembg 前设置：

- `U2NET_HOME` → `tools/rembg_models`
- `REMBG_HOME` → 同上
- `XDG_DATA_HOME` → 同上（避免落到 C: 用户目录）

流程：绿幕色键 → rembg（若 `USE_REMBG=1`）→ fringe scrub → `assets/processed/` + `assets/qa/checker_*`

## Agent 提示

- **Asset Agent**：生图后优先走本管线；写实精灵导入 Godot 用 Linear + Fix Alpha Border
- **Verifier**：棋盘格 QA 通过后再宣称抠图完成
- Playbook：`docs/playbooks/PB-Game-Visual.md`

## 禁止偷懒

- 禁止再往 C 盘缓存扔大模型
- 禁止无棋盘格验收就入库
- 禁止把 `.onnx` 提交进 Git
