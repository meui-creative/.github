"""Endless shelf of the studio's own products.

    .venv/bin/python scripts/products.py

The card art is the same set meui-creative.com uses on /projekty. The shelf
is drawn once inside <defs> and placed twice with <use>, so the loop costs no
extra bytes.
"""

from lib.brand import ASSETS, BUILD, SITE, THEMES
from lib.svgkit import REDUCED_MOTION, webp_data
from lib.text import text_path

VW, VH = 1600, 500
CW, CH, GAP = 250, 312, 38
Y = 36

P = SITE / "images/projects"
PRODUCTS = [
    ("Fixuj & Mixuj", ["Drink deals from 10 chains,", "with a 14-day price forecast"], P / "FixujAMixuj.jpg", None),
    ("Bombotalk", ["A satirical daily, written", "every morning by an AI routine"], P / "Bombotalk.jpg", None),
    ("Froggies", ["Leapfrog race for 2–4 players,", "bots and online play"], BUILD / "stills/froggies.png", "1180:1475:1100:125"),
    ("Cue", ["Film pre-production: script,", "shot list, storyboard"], P / "Cue.jpg", None),
    ("^peak", ["Biohacking encyclopedia,", "out on the App Store"], P / "Peak.jpg", None),
    ("Stěhuj se", ["Where to move? 214 places", "scored from open data"], P / "StehujSe.jpg", None),
    ("Hodinky Pro Vás", ["Watch configurator", "and e-shop"], P / "HodinkyProVás.jpg", None),
    ("AAC", ["Anonymous Alcoholic Club,", "our own streetwear label"], P / "AnonymousAlcoholicClub.jpg", None),
]


def shelf(t: dict) -> tuple[str, float]:
    cards = []
    x = 0.0
    for i, (name, lines, img, crop) in enumerate(PRODUCTS):
        uri = webp_data(img, CW * 2 // 2 + 50, q=70, crop=crop)
        tilt = (-1.6, 1.2, -0.8, 1.8)[i % 4]
        nd, _ = text_path(name, 4, CH + 44, "display", 72, 25)
        ld = "".join(text_path(line, 4, CH + 74 + k * 24, "text", 45, 17.5)[0] for k, line in enumerate(lines))
        cards.append(
            f'<g transform="translate({x:.0f} 0)"><g transform="rotate({tilt} {CW / 2} {CH / 2})">'
            f'<rect width="{CW}" height="{CH}" rx="18" fill="#000" filter="url(#sh)"/>'
            f'<clipPath id="c{i}"><rect width="{CW}" height="{CH}" rx="18"/></clipPath>'
            f'<image href="{uri}" width="{CW}" height="{CH}" clip-path="url(#c{i})" preserveAspectRatio="xMidYMid slice"/></g>'
            f'<path d="{nd}" fill="{t["ink"]}"/><path d="{ld}" fill="rgba({t["ink_rgb"]},0.58)"/></g>')
        x += CW + GAP
    return "".join(cards), x


def build(theme: str, shelf_markup: tuple[str, float] | None = None) -> str:
    t = THEMES[theme]
    cards, width = shelf_markup or shelf(t)
    css = f'''
.marq{{animation:marq 56s linear infinite}}
@keyframes marq{{from{{transform:translateX(0)}}to{{transform:translateX(-{width:.0f}px)}}}}
{REDUCED_MOTION}
'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}">
<title>Our own products: {", ".join(p[0] for p in PRODUCTS).replace("&", "&amp;")}</title>
<style>{css}</style>
<defs>
<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="13" cy="13" r="1.5" fill="{t["dot"]}"/></pattern>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity="{0.16 if theme == "light" else 0.5}"/></filter>
<linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".07" stop-color="#fff"/><stop offset=".93" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{VW}" height="{VH}"><rect width="{VW}" height="{VH}" fill="url(#edge)"/></mask>
<g id="shelf">{cards}</g>
</defs>
<rect width="{VW}" height="{VH}" rx="28" fill="{t["surface"]}"/>
<rect width="{VW}" height="{VH}" rx="28" fill="url(#dots)"/>
<g mask="url(#fade)"><g transform="translate(60 {Y})"><g class="marq"><use href="#shelf"/><use href="#shelf" x="{width:.0f}"/></g></g></g>
</svg>'''


if __name__ == "__main__":
    for theme in THEMES:
        svg = build(theme)
        (ASSETS / f"products-{theme}.svg").write_text(svg)
        print(f"products-{theme}.svg", f"{len(svg) / 1024:.0f} KB")
