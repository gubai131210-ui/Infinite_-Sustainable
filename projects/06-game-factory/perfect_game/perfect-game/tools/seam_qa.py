"""Quantitative seam QA for Paper Isle base wrap tiles only."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from seamless import seam_score, stitch_grid

ROOT = Path(__file__).resolve().parents[1]
TILES = ROOT / "assets" / "tiles"
QA = ROOT / "assets" / "qa"
THRESHOLD = 12.0
BASE_TILES = ("tile_grass.png", "tile_path.png", "tile_water.png")


def main() -> int:
    QA.mkdir(parents=True, exist_ok=True)
    report: dict = {"threshold": THRESHOLD, "tiles": {}}
    all_ok = True
    for name in BASE_TILES:
        path = TILES / name
        if not path.is_file():
            print("MISS", name)
            all_ok = False
            continue
        img = Image.open(path)
        score = seam_score(img)
        ok = score <= THRESHOLD
        all_ok = all_ok and ok
        grid = stitch_grid(img, 3)
        out = QA / f"seam_{path.stem}_3x3.png"
        grid.save(out)
        report["tiles"][path.name] = {
            "seam_score": round(score, 3),
            "pass": ok,
            "qa": str(out.relative_to(ROOT)),
        }
        print(f"{'PASS' if ok else 'FAIL'} {path.name} seam_score={score:.3f}")
    report["all_pass"] = all_ok
    (QA / "seam_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
