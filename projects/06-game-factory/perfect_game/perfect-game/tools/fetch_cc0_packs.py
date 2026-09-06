"""Download approved CC0 packs into assets/cc0/ and update attribution stub.

Usage (PowerShell):
  python tools/fetch_cc0_packs.py

Default: Kenney Pixel Platformer Farm Expansion (CC0) from OpenGameArt mirror.
Style remapping into processed/ is a separate Pack (P05 remap step).
"""
from __future__ import annotations

import zipfile
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cc0"
OUT.mkdir(parents=True, exist_ok=True)

# OpenGameArt direct file (Kenney, CC0)
PACKS = [
    {
        "id": "kenney_pixelplatformer_farm",
        "url": "https://opengameart.org/sites/default/files/kenney_pixelplatformerfarmexpansion.zip",
        "license": "CC0 1.0",
        "source": "https://opengameart.org/content/pixel-platformer-farm-expansion",
        "note": "Platformer perspective — use for crop/prop refs; remap before runtime if style clashes",
    },
]


def main() -> None:
    attr_lines = [
        "# CC0 fetch log",
        "",
        "| id | license | source | path | note |",
        "|----|---------|--------|------|------|",
    ]
    for pack in PACKS:
        dest_dir = OUT / pack["id"]
        dest_dir.mkdir(parents=True, exist_ok=True)
        zip_path = dest_dir / "pack.zip"
        print("GET", pack["url"])
        try:
            urlretrieve(pack["url"], zip_path)
        except Exception as e:
            print("FAIL download", pack["id"], e)
            continue
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(dest_dir / "raw")
        attr_lines.append(
            f"| {pack['id']} | {pack['license']} | {pack['source']} | `assets/cc0/{pack['id']}/` | {pack['note']} |"
        )
        print("OK", pack["id"])
    (OUT / "FETCH_LOG.md").write_text("\n".join(attr_lines) + "\n", encoding="utf-8")
    print("Wrote", OUT / "FETCH_LOG.md")


if __name__ == "__main__":
    main()
