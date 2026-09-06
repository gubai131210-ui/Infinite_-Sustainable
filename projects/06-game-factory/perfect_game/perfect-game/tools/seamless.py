"""Make a texture tileable via wrap-offset + feather blend, then optional tile crop."""
from __future__ import annotations

from PIL import Image, ImageFilter, ImageChops
import numpy as np


def _to_rgb(img: Image.Image) -> Image.Image:
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        return bg
    return img.convert("RGB")


def make_seamless(img: Image.Image, feather: int | None = None) -> Image.Image:
    """Classic half-offset blend so opposite edges match."""
    rgb = _to_rgb(img)
    w, h = rgb.size
    if feather is None:
        feather = max(8, min(w, h) // 8)

    # Roll so old seams sit in the center cross.
    arr = np.asarray(rgb, dtype=np.float32)
    ox, oy = w // 2, h // 2
    rolled = np.roll(np.roll(arr, ox, axis=1), oy, axis=0)

    # Soft mask: heal center cross (where discontinuous edges meet after roll).
    yy, xx = np.mgrid[0:h, 0:w]
    dx = np.minimum(np.abs(xx - ox), np.abs(xx - (ox + w) % w))
    # distance to vertical seam line at x=ox and horizontal at y=oy
    dist_v = np.abs(xx - ox)
    dist_h = np.abs(yy - oy)
    dist = np.minimum(dist_v, dist_h).astype(np.float32)
    # Also use radial falloff from center for corner heal
    dist = np.minimum(dist, np.sqrt((xx - ox) ** 2 + (yy - oy) ** 2) * 0.5)

    mask = np.clip(1.0 - dist / float(feather), 0.0, 1.0)
    mask = mask[..., None]

    # Blurred rolled as heal source
    blur = Image.fromarray(np.clip(rolled, 0, 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(radius=max(2, feather // 3))
    )
    blur_arr = np.asarray(blur, dtype=np.float32)
    healed = rolled * (1.0 - mask) + blur_arr * mask
    out = Image.fromarray(np.clip(healed, 0, 255).astype(np.uint8))

    # Roll back so content roughly matches original framing
    out_arr = np.asarray(out, dtype=np.uint8)
    out_arr = np.roll(np.roll(out_arr, -ox, axis=1), -oy, axis=0)
    return Image.fromarray(out_arr)


def extract_tile(img: Image.Image, size: int = 64) -> Image.Image:
    """Center-crop square then resize to tile size."""
    rgb = _to_rgb(img)
    w, h = rgb.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    crop = rgb.crop((left, top, left + side, top + side))
    return crop.resize((size, size), Image.Resampling.LANCZOS)


def seam_score(tile: Image.Image) -> float:
    """Mean abs diff across horizontal & vertical wrap seams (RGB)."""
    arr = np.asarray(_to_rgb(tile), dtype=np.float32)
    h, w, _ = arr.shape
    vert = np.mean(np.abs(arr[:, 0, :] - arr[:, -1, :]))
    horiz = np.mean(np.abs(arr[0, :, :] - arr[-1, :, :]))
    return float((vert + horiz) * 0.5)


def stitch_grid(tile: Image.Image, n: int = 3) -> Image.Image:
    t = _to_rgb(tile)
    w, h = t.size
    canvas = Image.new("RGB", (w * n, h * n))
    for y in range(n):
        for x in range(n):
            canvas.paste(t, (x * w, y * h))
    return canvas
