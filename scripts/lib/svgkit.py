"""Small helpers for hand-assembled animated SVGs."""

import base64
import re
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path

from .brand import BUILD, SITE


@lru_cache(maxsize=None)
def doodle(name: str) -> tuple[float, float, float, float, str]:
    """(minx, miny, w, h, inner markup) of a site doodle; `currentColor` is kept
    so the caller decides the colour with a `fill`/`color` on the wrapper."""
    path = SITE / name if "/" in name else SITE / "doodles" / f"{name}.svg"
    src = path.read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).replace(",", " ").split()]
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S)
    inner = re.sub(r"<\?xml.*?\?>|<!--.*?-->", "", inner, flags=re.S)
    inner = inner.replace('fill="currentColor"', "")
    return (*vb, inner.strip())


def place(name: str, x: float, y: float, h: float, fill: str | None = None, extra: str = "",
          cls: str = "") -> tuple[str, float]:
    """Doodle scaled to height `h` with its top-left at (x, y). Returns (markup, width)."""
    mx, my, w, hh, inner = doodle(name)
    s = h / hh
    fill_attr = f' fill="{fill}"' if fill else ""
    cls_attr = f' class="{cls}"' if cls else ""
    g = (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f}) translate({-mx} {-my})"'
         f'{fill_attr}{extra}><g{cls_attr}>{inner}</g></g>')
    return g, w * s


def webp_data(src: Path, width: int, height: int | None = None, q: int = 72,
              crop: str | None = None) -> str:
    """Resize (and optionally crop, ffmpeg syntax `w:h:x:y`) an image into a data URI.

    External images never load inside an SVG used as <img>, so every raster the
    hero shows has to travel inside the SVG itself.
    """
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "o.webp"
        vf = []
        if crop:
            vf.append(f"crop={crop}")
        vf.append(f"scale={width}:{height if height else -1}:flags=lanczos")
        png = Path(tmp) / "o.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-frames:v", "1",
                        "-vf", ",".join(vf), str(png)], check=True)
        subprocess.run(["cwebp", "-quiet", "-q", str(q), "-m", "6", str(png), "-o", str(out)], check=True)
        return "data:image/webp;base64," + base64.b64encode(out.read_bytes()).decode()


def frame_at(video: Path, t: float, name: str) -> Path:
    """Grab one still from a showcase recording."""
    out = BUILD / "stills" / f"{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(video),
                        "-frames:v", "1", str(out)], check=True)
    return out


REDUCED_MOTION = ("@media (prefers-reduced-motion: reduce){*,*::before,*::after{"
                  "animation:none!important;transition:none!important}}")
