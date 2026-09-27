"""Froggies product card, in the same format as the other product art
(meui-creative/public/images/projects/*.jpg): 1024x1280, flat colour, white
mark on top, tilted UI panels bleeding off the edges.

    .venv/bin/python scripts/froggies_card.py

Screens are captured from froggies.meui.cz (desktop at 2x, phone at 390x844 2x)
into build/froggies/ with scripts/capture-froggies.mjs.
"""

import base64
import subprocess
from pathlib import Path

from lib import text as T
from lib.brand import BUILD

T.FONTS["nunito"] = BUILD / "fonts/Nunito.ttf"  # OFL; the game's own face

W, H = 1024, 1280
# meui-pink (dark variant), the one brand colour no other product card uses yet.
# The other cards sit on the dark variant of their brand colour, slightly
# darker along the top edge and into the top corners; this copies that.
BG = "#c567b8"
SRC = BUILD / "froggies"
OUT = BUILD / "stills/froggies-card.jpg"


def uri(path: Path, crop: str | None = None, width: int = 1400) -> str:
    tmp = BUILD / "froggies" / f"_{path.stem}-{width}.jpg"
    vf = (f"crop={crop}," if crop else "") + f"scale={width}:-1:flags=lanczos"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf", vf, "-q:v", "3", str(tmp)], check=True)
    return "data:image/jpeg;base64," + base64.b64encode(tmp.read_bytes()).decode()


def frog_icon(x: float, y: float, s: float) -> str:
    """The favicon frog, redrawn as a white line icon like the other cards' marks."""
    sw = 3.2
    return f'''<g transform="translate({x} {y}) scale({s})" fill="none" stroke="#fff" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">
<circle cx="20.1" cy="20.2" r="7.7"/><circle cx="43.9" cy="20.2" r="7.7"/>
<path d="M13.4 24.6A19 17.9 0 1 0 50.6 24.6"/>
<circle cx="19.6" cy="20.6" r="2.6" fill="#fff" stroke="none"/><circle cx="44.4" cy="20.6" r="2.6" fill="#fff" stroke="none"/>
<path d="M26 39.2q6 5.4 12 0"/></g>'''


def panel(href: str, x, y, w, h, rot, rx=26, extra=""):
    cid = f"c{abs(hash((x, y)))}"
    return f'''<g transform="translate({x} {y}) rotate({rot})">
<rect width="{w}" height="{h}" rx="{rx}" fill="#000" opacity=".28" filter="url(#sh)"/>
<clipPath id="{cid}"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
<image href="{href}" width="{w}" height="{h}" clip-path="url(#{cid})" preserveAspectRatio="xMidYMid slice"/>
<rect width="{w}" height="{h}" rx="{rx}" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="2"/>{extra}</g>'''


def build() -> None:
    word, ww = T.text_path("Froggies", 0, 0, "nunito", 850, 118)
    k = 2.15  # icon scale; the drawing spans x 12..52, y 12..52 of its 64 box
    icon_w, gap = 40 * k, 30
    total = icon_w + gap + ww
    x0 = W / 2 - total / 2
    word, _ = T.text_path("Froggies", x0 + icon_w + gap, 232, "nunito", 850, 118)

    lobby = uri(SRC / "lobby.png", width=1500)
    # the board with the starting frogs and the pond, without the scenery around it
    board = uri(SRC / "board.png", crop="1500:1097:403:144", width=1100)
    phone = uri(SRC / "mobile-home.png", width=560)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="22"/></filter>
<linearGradient id="bgv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".09"/><stop offset=".3" stop-color="#000" stop-opacity="0"/></linearGradient>
<radialGradient id="bgc" cx=".5" cy=".35" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".07"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#bgv)"/><rect width="{W}" height="{H}" fill="url(#bgc)"/>
{frog_icon(x0 - 12.4 * k, 232 - 52.3 * k, k)}
<path d="{word}" fill="#fff"/>
{panel(lobby, 250, 470, 900, 562, -8)}
{panel(board, -120, 800, 700, 512, -8, 22)}
{panel(phone, 610, 690, 300, 649, -8, 38)}
</svg>'''
    svg_path = BUILD / "froggies/card.svg"
    svg_path.write_text(svg)
    png = BUILD / "froggies/card.png"
    subprocess.run(["rsvg-convert", "-w", str(W * 2), str(svg_path), "-o", str(png)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(png), "-vf", f"scale={W}:{H}:flags=lanczos",
                    "-q:v", "2", str(OUT)], check=True)
    print(OUT)


if __name__ == "__main__":
    build()
