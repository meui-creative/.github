"""Section headings and the footer, in Goia with a hand-drawn stroke.

    .venv/bin/python scripts/headings.py

Markdown headings would fall back to GitHub's system font; these keep the
studio's type. The words still exist as alt text in the README.
"""

from lib.brand import ASSETS, THEMES
from lib.svgkit import REDUCED_MOTION, place
from lib.text import text_path

VW = 1600
HEADINGS = {
    "work": ("Client work", "Recent launches", "#56745c", "development"),
    "numbers": ("By the numbers", "The studio, counted", "#a085d1", "design"),
    "products": ("Our own products", "Things we made because we wanted them", "#e8906d", "production"),
    "stack": ("Under the hood", "We run our own stack", "#5da9a9", "marketing"),
    "team": ("The people", "Who's behind it", "#56745c", "e"),
}


def squiggle(x: float, y: float, w: float) -> str:
    seg = w / 6
    d = f"M{x:.1f} {y:.1f}"
    for k in range(6):
        d += f"q{seg / 2:.1f} {(-9 if k % 2 else 9)} {seg:.1f} 0"
    return d


def heading(theme: str, label: str, title: str, color: str, doodle: str) -> str:
    t = THEMES[theme]
    VH = 190
    ld, lw = text_path(label.upper(), 20, 52, "text", 70, 22, tracking=0.08)
    td, tw = text_path(title, 20, 136, "display", 76, 70)
    icon, iw = place(doodle, tw + 44, 72, 66, color, cls="wig")
    css = f'''
.draw{{stroke-dasharray:1;animation:draw 1.1s .3s cubic-bezier(.6,0,.2,1) both}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
.wig{{transform-box:fill-box;transform-origin:50% 80%;animation:wig 4s 1s ease-in-out infinite}}
@keyframes wig{{0%,78%,100%{{transform:none}}84%{{transform:rotate(-12deg) scale(1.06)}}90%{{transform:rotate(9deg)}}96%{{transform:rotate(-4deg)}}}}
.rise{{animation:rise .8s cubic-bezier(.2,.9,.3,1) both}}
@keyframes rise{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:none}}}}
{REDUCED_MOTION}'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}">
<title>{label}: {title.replace("&", "&amp;")}</title>
<style>{css}</style>
<path d="{ld}" fill="{color}"/>
<g class="rise"><path d="{td}" fill="{t["ink"]}"/></g>
{icon}
<path class="draw" pathLength="1" d="{squiggle(22, 166, min(tw, 520))}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
</svg>'''


def footer(theme: str) -> str:
    t = THEMES[theme]
    VH = 420
    octo, ow = place("chobotnicka", 0, 0, 170, None, cls="octo")
    line1, w1 = text_path("Create what you", VW / 2, 300, "display", 80, 64, anchor="middle")
    line2, w2 = text_path("wish existed.", VW / 2, 372, "display", 80, 64, anchor="middle")
    css = f'''
.octo{{transform-box:fill-box;transform-origin:50% 100%;animation:octo 2.8s ease-in-out infinite alternate}}
@keyframes octo{{from{{transform:rotate(-7deg)}}to{{transform:rotate(7deg) translateY(-8px)}}}}
.bub{{animation:bub 4s ease-in infinite;opacity:0}}
@keyframes bub{{0%{{opacity:0;transform:translateY(0)}}15%{{opacity:.8}}100%{{opacity:0;transform:translateY(-140px)}}}}
{REDUCED_MOTION}'''
    bubbles = "".join(
        f'<circle class="bub" style="animation-delay:{d}s" cx="{VW / 2 + x}" cy="170" r="{r}" fill="none" stroke="{t["green"]}" stroke-width="3"/>'
        for x, r, d in ((70, 9, 0), (96, 6, 1.3), (60, 5, 2.4), (110, 11, 3.1)))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}">
<title>Create what you wish existed.</title>
<style>{css}</style>
<defs><pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="13" cy="13" r="1.5" fill="{t["dot"]}"/></pattern></defs>
<rect width="{VW}" height="{VH}" rx="28" fill="{t["surface"]}"/>
<rect width="{VW}" height="{VH}" rx="28" fill="url(#dots)"/>
<g transform="translate({VW / 2 - ow / 2:.1f} 40)">{octo}</g>
{bubbles}
<path d="{line1}" fill="{t["ink"]}"/><path d="{line2}" fill="{t["pink"]}"/>
</svg>'''


if __name__ == "__main__":
    out = ASSETS / "headings"
    out.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        for key, spec in HEADINGS.items():
            (out / f"{key}-{theme}.svg").write_text(heading(theme, *spec))
        (ASSETS / f"footer-{theme}.svg").write_text(footer(theme))
    print("headings + footer written")
