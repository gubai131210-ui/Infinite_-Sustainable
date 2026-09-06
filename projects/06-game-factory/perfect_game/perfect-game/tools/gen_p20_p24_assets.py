"""P21–P24 assets: food icons + ui/rain SFX + soft BGM/rain loops."""
from __future__ import annotations

import math
import random
import struct
import wave
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise SystemExit("pip install pillow")

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "assets" / "processed"
SFX = ROOT / "assets" / "sfx"
PROC.mkdir(parents=True, exist_ok=True)
SFX.mkdir(parents=True, exist_ok=True)
SR = 22050
rng = random.Random(42)


def write_tone(name: str, freq: float, ms: int, vol: float = 0.22) -> None:
    n = int(SR * ms / 1000)
    path = SFX / f"{name}.wav"
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        for i in range(n):
            t = i / SR
            env = min(1.0, i / 180.0) * min(1.0, (n - i) / 350.0)
            sample = int(32767 * vol * env * math.sin(2 * math.pi * freq * t))
            frames += struct.pack("<h", sample)
        w.writeframes(frames)
    print("OK", path.name)


def write_noise(name: str, ms: int, vol: float = 0.08) -> None:
    n = int(SR * ms / 1000)
    path = SFX / f"{name}.wav"
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        prev = 0.0
        for i in range(n):
            # brown-ish noise for rain
            white = rng.uniform(-1.0, 1.0)
            prev = (prev + 0.02 * white) * 0.98
            env = 0.85 + 0.15 * math.sin(i / 800.0)
            sample = int(32767 * vol * env * max(-1.0, min(1.0, prev * 8)))
            frames += struct.pack("<h", sample)
        w.writeframes(frames)
    print("OK", path.name)


def write_bgm(name: str, seconds: float = 8.0) -> None:
    n = int(SR * seconds)
    path = SFX / f"{name}.wav"
    chords = [
        [261.63, 329.63, 392.00],
        [293.66, 349.23, 440.00],
        [246.94, 311.13, 392.00],
        [220.00, 277.18, 329.63],
    ]
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        for i in range(n):
            t = i / SR
            ch = chords[int(t / 2.0) % len(chords)]
            s = 0.0
            for f in ch:
                s += math.sin(2 * math.pi * f * t) * 0.12
                s += math.sin(2 * math.pi * (f * 0.5) * t) * 0.05
            env = 0.7 + 0.3 * math.sin(t * 0.7)
            sample = int(32767 * env * max(-1.0, min(1.0, s)))
            frames += struct.pack("<h", sample)
        w.writeframes(frames)
    print("OK", path.name)


def food_icon(name: str, colors: list[tuple[int, int, int]], shape: str) -> None:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # plate
    d.ellipse((1, 3, 14, 14), fill=(230, 220, 200, 255), outline=(160, 140, 110, 255))
    if shape == "salad":
        for i, c in enumerate(colors):
            d.ellipse((3 + i * 2, 5 + (i % 2), 7 + i * 2, 9 + (i % 2)), fill=c + (255,))
    elif shape == "omelette":
        d.ellipse((3, 5, 12, 12), fill=colors[0] + (255,))
        d.ellipse((5, 6, 10, 10), fill=colors[1] + (255,))
    elif shape == "soup":
        d.ellipse((3, 5, 12, 12), fill=colors[0] + (255,))
        d.rectangle((7, 2, 9, 6), fill=colors[1] + (255,))
    else:  # pie
        d.pieslice((3, 4, 13, 13), 200, 340, fill=colors[0] + (255,))
        d.arc((3, 4, 13, 13), 200, 340, fill=colors[1] + (255,))
    path = PROC / f"item_{name}.png"
    img.save(path)
    print("OK", path.name)


def improve_water_in_tileset() -> None:
    """Rewrite water cells in master tileset if present."""
    ts_path = PROC / "tileset_master.png"
    if not ts_path.exists():
        print("SKIP tileset_master.png missing")
        return
    # Re-run water tile painters via sibling module if available
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "gen_tileset_master", ROOT / "tools" / "gen_tileset_master.py"
        )
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(mod)
        # Patch water function richer foam then rebuild
        def water(deep: bool = False):
            base = (36, 92, 168, 255) if deep else (52, 124, 198, 255)
            foam = (150, 210, 240, 255)
            dark = (28, 70, 130, 255)
            img = Image.new("RGBA", (16, 16), base)
            for y in range(16):
                for x in range(16):
                    wave = math.sin((x + y * 0.6) * 0.9) 
                    if wave > 0.55:
                        img.putpixel((x, y), foam if not deep else (90, 150, 210, 255))
                    elif wave < -0.65 and deep:
                        img.putpixel((x, y), dark)
            # soft highlight dashes
            for y in (2, 6, 10, 14):
                for x in range(1, 15, 4):
                    xx = (x + y // 2) % 15
                    img.putpixel((xx, y), foam)
            return img

        mod.water = water  # type: ignore
        mod.main()
        print("OK regenerated tileset_master.png")
    except Exception as e:
        print("WARN tileset regen:", e)


def main() -> None:
    food_icon("salad", [(60, 160, 70), (220, 80, 70), (240, 140, 60)], "salad")
    food_icon("omelette", [(240, 200, 80), (255, 230, 140)], "omelette")
    food_icon("fish_soup", [(70, 140, 190), (200, 180, 120)], "soup")
    food_icon("pumpkin_pie", [(210, 120, 50), (160, 90, 40)], "pie")
    write_tone("ui", 880, 90, 0.16)
    write_tone("rain", 180, 200, 0.12)
    write_noise("rain_loop", 2500, 0.07)
    write_bgm("bgm_soft", 10.0)
    improve_water_in_tileset()
    print("P20-P24 assets done")


if __name__ == "__main__":
    main()
