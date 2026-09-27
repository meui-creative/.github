"""Team: polaroids pegged to a string, swaying a little out of sync.

    .venv/bin/python scripts/team.py

Same people, photos and roles as meui-creative.com/o-nas.
"""

from lib.brand import ASSETS, SITE, THEMES
from lib.svgkit import REDUCED_MOTION, webp_data
from lib.text import text_path

VW, VH = 1600, 390
T = SITE / "images/team"
TEAM = [
    ("Marián", "Creative Lead", T / "marian.jpg"),
    ("Matěj", "Lead Developer", T / "matej.jpg"),
    ("Adam", "Art Director", T / "adam.jpg"),
    ("Filip", "Project Engineer", T / "filip.jpg"),
    ("Radek", "Visual Content", T / "radek.jpg"),
    ("Sarah", "Design Creator", T / "sarah.jpg"),
    ("Chiko", "Head of Morale", T / "chiko/chiko3.webp"),
]
PW, PH, PHOTO = 180, 258, 160


def string_y(x: float) -> float:
    """A slack string: a shallow parabola between two nails."""
    mid = VW / 2
    return 58 + 44 * (1 - ((x - mid) / (VW / 2)) ** 2)


def build(theme: str, photos: list[str]) -> str:
    t = THEMES[theme]
    step = (VW - 300) / (len(TEAM) - 1)
    cards = []
    for i, ((name, role, _), uri) in enumerate(zip(TEAM, photos)):
        cx = 150 + i * step
        top = string_y(cx) + 6
        tilt = (-3, 2, -1.5, 3, -2.5, 1.5, -3.5)[i]
        nd, _ = text_path(name, cx, top + PHOTO + 52, "display", 72, 24, anchor="middle")
        rd, _ = text_path(role, cx, top + PHOTO + 76, "text", 50, 15.5, anchor="middle")
        x = cx - PW / 2
        py = top + (PW - PHOTO) / 2
        dur = 3.4 + (i % 3) * 0.7
        cards.append(f'''
<g transform="rotate({tilt} {cx:.1f} {top:.1f})"><g class="sway" style="animation-duration:{dur:.1f}s;animation-delay:{-i * 0.8:.1f}s">
<rect x="{x:.1f}" y="{top:.1f}" width="{PW}" height="{PH}" rx="3" fill="#fffdf8" filter="url(#sh)"/>
<clipPath id="p{i}"><rect x="{cx - PHOTO / 2:.1f}" y="{py:.1f}" width="{PHOTO}" height="{PHOTO}"/></clipPath>
<image href="{uri}" x="{cx - PHOTO / 2:.1f}" y="{py:.1f}" width="{PHOTO}" height="{PHOTO}" clip-path="url(#p{i})" preserveAspectRatio="xMidYMin slice"/>
<path d="{nd}" fill="#1a1a1a"/><path d="{rd}" fill="rgba(0,0,0,0.5)"/>
<rect x="{cx - 7:.1f}" y="{top - 16:.1f}" width="14" height="30" rx="3" fill="{("#d8b98a", "#c9a36b")[i % 2]}"/>
<rect x="{cx - 1:.1f}" y="{top - 14:.1f}" width="2" height="26" fill="rgba(0,0,0,0.18)"/>
</g></g>''')
    rope = " ".join(f"{x:.0f},{string_y(x):.1f}" for x in range(0, VW + 1, 40))
    css = f'''
.sway{{transform-box:fill-box;transform-origin:50% 0;animation:sway ease-in-out infinite alternate}}
@keyframes sway{{from{{transform:rotate(-2.2deg)}}to{{transform:rotate(2.2deg)}}}}
{REDUCED_MOTION}'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}">
<title>The team: {", ".join(f"{n} ({r})" for n, r, _ in TEAM)}</title>
<style>{css}</style>
<defs>
<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="13" cy="13" r="1.5" fill="{t["dot"]}"/></pattern>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity="{0.16 if theme == "light" else 0.5}"/></filter>
</defs>
<rect width="{VW}" height="{VH}" rx="28" fill="{t["surface"]}"/>
<rect width="{VW}" height="{VH}" rx="28" fill="url(#dots)"/>
<polyline points="{rope}" fill="none" stroke="rgba({t["ink_rgb"]},0.35)" stroke-width="2.5"/>
{"".join(cards)}
</svg>'''


if __name__ == "__main__":
    photos = [webp_data(p, 320, q=74, crop="iw:min(iw\\,ih):0:0") for _, _, p in TEAM]
    for theme in THEMES:
        svg = build(theme, photos)
        (ASSETS / f"team-{theme}.svg").write_text(svg)
        print(f"team-{theme}.svg", f"{len(svg) / 1024:.0f} KB")
