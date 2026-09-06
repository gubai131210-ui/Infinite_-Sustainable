"""Generate tiny placeholder WAV beeps for Oakhaven SFX (P12)."""
from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "sfx"
OUT.mkdir(parents=True, exist_ok=True)

SR = 22050


def write_tone(name: str, freq: float, ms: int, vol: float = 0.25) -> None:
    n = int(SR * ms / 1000)
    path = OUT / f"{name}.wav"
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        for i in range(n):
            t = i / SR
            env = min(1.0, i / 200.0) * min(1.0, (n - i) / 400.0)
            sample = int(32767 * vol * env * math.sin(2 * math.pi * freq * t))
            frames += struct.pack("<h", sample)
        w.writeframes(frames)
    print("OK", path.name)


def main() -> None:
    write_tone("footstep", 120, 60, 0.18)
    write_tone("water", 520, 120, 0.2)
    write_tone("chest", 340, 180, 0.22)
    write_tone("sell", 660, 160, 0.2)
    write_tone("hoe", 180, 90, 0.2)
    print("P12 sfx done")


if __name__ == "__main__":
    main()
