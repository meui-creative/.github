"""Terminal: the self-hosted things running behind the studio.

    .venv/bin/python scripts/terminal.py

Deliberately no hostnames: the internal tools are listed by what they do,
not where they live.
"""

from lib.brand import ASSETS, THEMES
from lib.svgkit import REDUCED_MOTION
from lib.text import measure, text_path

VW, VH = 1600, 700
FS = 25
CHAR = measure("M", "mono", 400, FS)
LH = 40
X0, Y0 = 92, 150
CYCLE = 20.0  # seconds, whole session replays

C = {
    "prompt": "#8fbf97", "cmd": "#f0ece4", "name": "#6fc3c3", "desc": "#9a968f",
    "dim": "#5e5b56", "pink": "#e59ad8", "ok": "#6fcf7f", "head": "#d6a4f0",
}

COMMAND = "meui status --stack"
FLEET = [
    ("studio", "agency OS: CRM, quotes, invoices, hosting, ads"),
    ("plan", "issue tracker where AI agents pick up tickets"),
    ("forecast", "Chronos-2 price forecasts for Fixuj & Mixuj"),
    ("bg", "background removal API, RMBG-2.0"),
    ("send", "our own mailing platform on top of AWS SES"),
    ("meter", "usage metering for every site we host"),
    ("analytics", "self-hosted, cookieless visitor stats"),
]


def seg(text: str, col: int, row: float, color: str, wght: int = 400) -> str:
    d, _ = text_path(text, X0 + col * CHAR, Y0 + row * LH, "mono", wght, FS)
    return f'<path d="{d}" fill="{color}"/>'


def appear(cls: str, at: float) -> str:
    """Keyframes that show an element at `at` seconds and keep it until the replay."""
    a = at / CYCLE * 100
    return (f".{cls}{{animation:{cls} {CYCLE}s steps(1,end) infinite}}"
            f"@keyframes {cls}{{0%{{opacity:0}}{a:.2f}%{{opacity:1}}97%{{opacity:1}}100%{{opacity:0}}}}")


def build(theme: str) -> str:
    t = THEMES[theme]
    rows, css = [], []

    # row 0: prompt + typed command
    rows.append(seg("~/meui", 0, 0, C["prompt"], 600) + seg("$", 7, 0, C["dim"]))
    cmd_x = 9
    rows.append(f'<g clip-path="url(#typed)">{seg(COMMAND, cmd_x, 0, C["cmd"])}</g>')
    type_start, type_dur = 0.6, 1.9
    n = len(COMMAND)
    a0, a1 = type_start / CYCLE * 100, (type_start + type_dur) / CYCLE * 100
    css.append(f".typed{{transform-box:fill-box;transform-origin:left;animation:typed {CYCLE}s steps({n}) infinite}}"
               f"@keyframes typed{{0%,{a0:.2f}%{{transform:scaleX(0)}}{a1:.2f}%,97%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}")

    t0 = type_start + type_dur + 0.5
    rows.append(f'<g class="l0">{seg("SERVICE", 2, 1.4, C["head"], 700)}{seg("WHAT IT DOES", 16, 1.4, C["head"], 700)}'
                f'{seg("STATE", 66, 1.4, C["head"], 700)}</g>')
    css.append(appear("l0", t0))
    for i, (name, desc) in enumerate(FLEET, start=1):
        r = 1.4 + i
        cy = Y0 + r * LH - FS * 0.36
        rows.append(
            f'<g class="l{i}"><circle cx="{X0 + CHAR * 0.5:.1f}" cy="{cy:.1f}" r="6" fill="{C["ok"]}" class="pulse" '
            f'style="animation-delay:{-i * 0.37:.2f}s"/>{seg(name, 2, r, C["name"], 600)}{seg(desc, 16, r, C["desc"])}'
            f'{seg("running", 66, r, C["ok"])}</g>')
        css.append(appear(f"l{i}", t0 + 0.28 * i))
    k = len(FLEET) + 1
    r = 1.4 + k + 0.6
    summary = [("60+", C["pink"]), (" client sites", C["cmd"]), ("  ·  ", C["dim"]), ("our own servers", C["cmd"]),
               ("  ·  ", C["dim"]), ("3", C["pink"]), (" npm packages", C["cmd"])]
    col, parts = 2, []
    for text, color in summary:
        parts.append(seg(text, col, r, color, 600 if color == C["pink"] else 400))
        col += len(text)
    rows.append(f'<g class="l{k}">{"".join(parts)}</g>')
    css.append(appear(f"l{k}", t0 + 0.28 * k + 0.3))
    r2 = r + 1.5
    rows.append(f'<g class="l{k + 1}">{seg("~/meui", 0, r2, C["prompt"], 600)}{seg("$", 7, r2, C["dim"])}'
                f'<rect class="blink" x="{X0 + 9 * CHAR:.1f}" y="{Y0 + r2 * LH - FS * 0.8:.1f}" width="{CHAR * 0.9:.1f}" height="{FS * 1.05:.1f}" fill="{C["cmd"]}"/></g>')
    css.append(appear(f"l{k + 1}", t0 + 0.28 * k + 0.6))

    wx, wy, ww, wh = 40, 36, VW - 80, VH - 72
    style = "".join(css) + f'''
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.45;transform:scale(.7)}}}}
.blink{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
{REDUCED_MOTION}'''
    title, _ = text_path("meui — zsh — 160×40", VW / 2, wy + 29, "text", 50, 17, anchor="middle")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}">
<title>Terminal listing the self-hosted tools behind Meui Creative</title>
<style>{style}</style>
<defs>
<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="13" cy="13" r="1.5" fill="{t["dot"]}"/></pattern>
<filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000" flood-opacity="{0.2 if theme == "light" else 0.6}"/></filter>
<clipPath id="typed"><rect class="typed" x="{X0 + cmd_x * CHAR:.1f}" y="{Y0 - LH:.0f}" width="{n * CHAR + 4:.1f}" height="{LH * 1.3:.0f}"/></clipPath>
</defs>
<rect width="{VW}" height="{VH}" rx="28" fill="{t["surface"]}"/>
<rect width="{VW}" height="{VH}" rx="28" fill="url(#dots)"/>
<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16" fill="#141414" filter="url(#sh)"/>
<path d="M{wx} {wy + 16}a16 16 0 0 1 16-16H{wx + ww - 16}a16 16 0 0 1 16 16V{wy + 46}H{wx}Z" fill="#232323"/>
<circle cx="{wx + 26}" cy="{wy + 23}" r="7" fill="#ff5f57"/><circle cx="{wx + 50}" cy="{wy + 23}" r="7" fill="#febc2e"/><circle cx="{wx + 74}" cy="{wy + 23}" r="7" fill="#28c840"/>
<path d="{title}" fill="#8a867f"/>
{"".join(rows)}
</svg>'''


if __name__ == "__main__":
    for theme in THEMES:
        svg = build(theme)
        (ASSETS / f"terminal-{theme}.svg").write_text(svg)
        print(f"terminal-{theme}.svg", f"{len(svg) / 1024:.0f} KB")
