from pathlib import Path

base = Path(__file__).resolve().parents[1] / "scenes" / "interiors"
src = (base / "interior.tscn").read_text(encoding="utf-8")
for name in ["farmhouse", "barn", "shop", "cafe", "station", "lighthouse"]:
    out = src.replace('[node name="Interior"', f'[node name="{name}"')
    (base / f"{name}.tscn").write_text(out, encoding="utf-8")
    print("wrote", name)
