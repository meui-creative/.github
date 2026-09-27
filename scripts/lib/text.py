"""Text -> SVG path outlines in Goia / Goia Display.

GitHub renders SVGs as <img>, which never loads webfonts. Instead of shipping
the licensed font (even subsetted), every piece of display text is shaped with
HarfBuzz and baked into plain <path> outlines at build time.
"""

from functools import lru_cache
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path.home() / "DEV/meui-creative/src/fonts"
FONTS = {
    "display": FONT_DIR / "GoiaDisplayVariable.ttf",
    "text": FONT_DIR / "GoiaVariable.ttf",
    # OFL, fetched into build/ by scripts/build.sh; only used for the terminal.
    "mono": Path(__file__).resolve().parents[2] / "build/fonts/JetBrainsMono.ttf",
}


@lru_cache(maxsize=None)
def _tt(face: str) -> TTFont:
    return TTFont(FONTS[face])


@lru_cache(maxsize=None)
def _hb_face(face: str):
    blob = hb.Blob.from_file_path(str(FONTS[face]))
    return hb.Face(blob)


@lru_cache(maxsize=None)
def _glyphset(face: str, wght: float):
    return _tt(face).getGlyphSet(location=_loc(face, wght))


def _loc(face: str, wght: float) -> dict:
    axes = {a.axisTag for a in _tt(face)["fvar"].axes}
    return {k: v for k, v in (("wght", wght), ("slnt", 0)) if k in axes}


def shape(text: str, face: str = "display", wght: float = 85, size: float = 64,
          tracking: float = 0.0):
    """Return (glyphs, advance) where glyphs = [(name, x, y)] in font units scaled."""
    font = hb.Font(_hb_face(face))
    font.set_variations(_loc(face, wght))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    upem = _tt(face)["head"].unitsPerEm
    scale = size / upem
    order = _tt(face).getGlyphOrder()
    x = 0.0
    out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((order[info.codepoint], x + pos.x_offset * scale, pos.y_offset * scale, info.cluster))
        x += pos.x_advance * scale + tracking * size
    if out:
        x -= tracking * size
    return out, x, scale


def glyph_path(name: str, face: str, wght: float, scale: float, x: float, y: float) -> str:
    gs = _glyphset(face, wght)
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    # Font y-up -> SVG y-down.
    gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
    return pen.getCommands()


def text_path(text: str, x: float = 0, y: float = 0, face: str = "display", wght: float = 85,
              size: float = 64, anchor: str = "start", tracking: float = 0.0) -> tuple[str, float]:
    """One combined path `d` for a line of text. Returns (d, width)."""
    glyphs, width, scale = shape(text, face, wght, size, tracking)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    d = "".join(glyph_path(n, face, wght, scale, x + gx, y - gy) for n, gx, gy, _ in glyphs)
    return d, width


def text_glyphs(text: str, x: float = 0, y: float = 0, face: str = "display", wght: float = 85,
                size: float = 64, anchor: str = "start", tracking: float = 0.0):
    """Per-character paths, for staggered animations. Returns ([(char, d, gx)], width)."""
    glyphs, width, scale = shape(text, face, wght, size, tracking)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    out = []
    for n, gx, gy, cluster in glyphs:
        d = glyph_path(n, face, wght, scale, x + gx, y - gy)
        out.append((text[cluster], d, x + gx))
    return out, width


def measure(text: str, face: str = "display", wght: float = 85, size: float = 64,
            tracking: float = 0.0) -> float:
    return shape(text, face, wght, size, tracking)[1]
