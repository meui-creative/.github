"""Odometer strip: the studio in four numbers, digits rolling into place.

    .venv/bin/python scripts/stats.py

Counted on 27 Sep 2026 from the local clones of the org (see README colophon).
"""

from lib.brand import ASSETS, THEMES
from lib.svgkit import REDUCED_MOTION
from lib.text import measure, text_path

VW, VH = 1600, 330
STATS = [
    ("16231", "", "commits", "on main branches since 2024", "#56745c"),
    ("118", "", "repositories", "most of them client work", "#a085d1"),
    ("78", "", "Payload CMS apps", "Next.js + Payload 3, our default", "#e8906d"),
    ("60", "+", "sites live", "on our own servers", "#5da9a9"),
]
SIZE, WGHT = 104, 80
DIGITS = "0123456789"


def digit_w() -> float:
    return max(measure(d, "display", WGHT, SIZE) for d in DIGITS)


def odometer(value: str, x: float, base: float, ink: str, idx: int, group_gap: float) -> tuple[str, float]:
    """Each digit is a column 0..9 (twice, so bigger numbers spin more) that slides
    up until the target digit sits in the window."""
    dw = digit_w() * 0.92
    line = SIZE * 1.45
    out = []
    cx = x
    n = len(value)
    for i, ch in enumerate(value):
        if i and (n - i) % 3 == 0:
            cx += group_gap  # thin space between thousands
        target = int(ch)
        laps = 1 + (n - i) % 2
        column = DIGITS * laps + DIGITS[: target + 1]
        stop = len(column) - 1
        glyphs = []
        for k, c in enumerate(column):
            d, w = text_path(c, cx + dw / 2, base + k * line, "display", WGHT, SIZE, anchor="middle")
            glyphs.append(f'<path d="{d}"/>')
        dur = 1.6 + 0.25 * i
        out.append(
            f'<g mask="url(#win)"><g class="roll" '
            f'style="--y:{-stop * line:.1f}px;animation-duration:{dur:.2f}s;animation-delay:{0.2 + idx * 0.25 + 0.05 * i:.2f}s">'
            f'{"".join(glyphs)}</g></g>')
        cx += dw
    return "".join(out), cx - x


def build(theme: str) -> str:
    t = THEMES[theme]
    ink_rgb = t["ink_rgb"]
    col_w = VW / len(STATS)
    base = 158
    parts = []
    for i, (value, suffix, label, sub, color) in enumerate(STATS):
        gap = SIZE * 0.12
        # measure first to centre the block
        width = digit_w() * 0.92 * len(value) + gap * ((len(value) - 1) // 3)
        suf_w = measure(suffix, "display", WGHT, SIZE) if suffix else 0
        x = col_w * i + col_w / 2 - (width + suf_w) / 2
        digits, _ = odometer(value, x, base, t["ink"], i, gap)
        suf = ""
        if suffix:
            d, _ = text_path(suffix, x + width + 2, base, "display", WGHT, SIZE)
            suf = f'<path d="{d}" fill="{color}" class="fade" style="animation-delay:{1.4 + i * 0.25:.2f}s"/>'
        ld, lw = text_path(label, col_w * i + col_w / 2, base + 58, "text", 62, 27, anchor="middle")
        sd, _ = text_path(sub, col_w * i + col_w / 2, base + 92, "text", 42, 19, anchor="middle")
        # hand-drawn underline under the label, drawn on after the digits land
        ux = col_w * i + col_w / 2 - lw / 2
        uy = base + 70
        squiggle = (f"M{ux:.1f} {uy}c{lw * .12:.1f} -7 {lw * .22:.1f} 5 {lw * .34:.1f} 0"
                    f"s{lw * .22:.1f} 6 {lw * .33:.1f} 0 {lw * .2:.1f} 4 {lw * .33:.1f} -1")
        parts.append(
            f'<g fill="{t["ink"]}">{digits}</g>{suf}'
            f'<path d="{ld}" fill="{t["ink"]}"/>'
            f'<path d="{squiggle}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" '
            f'pathLength="1" class="draw" style="animation-delay:{1.3 + i * 0.25:.2f}s"/>'
            f'<path d="{sd}" fill="rgba({ink_rgb},0.55)"/>')
        if i:
            parts.append(f'<path d="M{col_w * i} 70v190" stroke="rgba({ink_rgb},0.1)" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>')
    css = f'''
.roll{{transform:translateY(var(--y));animation-name:roll;animation-timing-function:cubic-bezier(.2,.8,.2,1.02);animation-fill-mode:both}}
@keyframes roll{{from{{transform:translateY(0)}}to{{transform:translateY(var(--y))}}}}
.draw{{stroke-dasharray:1;stroke-dashoffset:0;animation:draw .7s ease-out both}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
.fade{{animation:fade .5s ease-out both}}
@keyframes fade{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:none}}}}
{REDUCED_MOTION}
'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}">
<title>16,231 commits, 118 repositories, 78 Payload CMS apps, 60+ sites live on our own servers</title>
<style>{css}</style>
<defs>
<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="13" cy="13" r="1.5" fill="{t["dot"]}"/></pattern>
<linearGradient id="fadeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".2" stop-color="#fff"/><stop offset=".82" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="win" maskUnits="userSpaceOnUse" x="0" y="0" width="{VW}" height="{VH}"><rect x="0" y="{base - SIZE * 1.0:.0f}" width="{VW}" height="{SIZE * 1.3:.0f}" fill="url(#fadeg)"/></mask>
</defs>
<rect width="{VW}" height="{VH}" rx="28" fill="{t["surface"]}"/>
<rect width="{VW}" height="{VH}" rx="28" fill="url(#dots)"/>
{"".join(parts)}
</svg>'''


if __name__ == "__main__":
    for theme in THEMES:
        svg = build(theme)
        (ASSETS / f"numbers-{theme}.svg").write_text(svg)
        print(f"numbers-{theme}.svg", f"{len(svg) / 1024:.0f} KB")
