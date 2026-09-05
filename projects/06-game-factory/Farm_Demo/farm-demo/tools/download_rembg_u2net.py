"""Download rembg u2net weights to D: project folder (never C: user profile)."""
from __future__ import annotations

import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "tools" / "rembg_models" / "u2net"
MODEL_PATH = MODEL_DIR / "u2net.onnx"
# Also place flat copy for older U2NET_HOME layouts
FLAT_DIR = ROOT / "tools" / "rembg_models"
FLAT_PATH = FLAT_DIR / "u2net.onnx"

URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"

# Point rembg away from C:
os.environ["U2NET_HOME"] = str(FLAT_DIR)
os.environ["REMBG_HOME"] = str(FLAT_DIR)
os.environ["XDG_DATA_HOME"] = str(FLAT_DIR)


def main() -> int:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    FLAT_DIR.mkdir(parents=True, exist_ok=True)

    if MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 100_000_000:
        print(f"Already present: {MODEL_PATH} ({MODEL_PATH.stat().st_size} bytes)")
        if not FLAT_PATH.exists():
            FLAT_PATH.write_bytes(MODEL_PATH.read_bytes())
        return 0

    print(f"Downloading u2net -> {MODEL_PATH}")
    print(f"URL: {URL}")
    tmp = MODEL_PATH.with_suffix(".onnx.part")
    try:
        urllib.request.urlretrieve(URL, tmp)
        tmp.replace(MODEL_PATH)
    except Exception as e:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        print(f"FAILED: {e}", file=sys.stderr)
        return 1

    size = MODEL_PATH.stat().st_size
    print(f"OK {MODEL_PATH} ({size} bytes)")
    FLAT_PATH.write_bytes(MODEL_PATH.read_bytes())
    print(f"Also copied flat: {FLAT_PATH}")
    print("Env for future shells:")
    print(f'  $env:U2NET_HOME = "{FLAT_DIR}"')
    print(f'  $env:REMBG_HOME = "{FLAT_DIR}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
