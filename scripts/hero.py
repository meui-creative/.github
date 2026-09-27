"""Animated hero: the studio desk.

    .venv/bin/python scripts/hero.py

One SVG per theme. Pure CSS keyframes, no script (GitHub renders SVG as <img>).
The artifacts around the headline are real work from all four crafts:
a browser that flips through client sites, a print poster, a reel, a logo on
the design canvas, a paid search ad being typed, an app and a video spot.
Two multiplayer cursors (design + dev) wander the desk the way they do in Figma.
"""

from lib.brand import ASSETS, SHOWCASE, SITE, THEMES
from lib.projects import WORK
from lib.svgkit import REDUCED_MOTION, frame_at, place, webp_data
from lib.text import measure, text_glyphs, text_path

VW, VH = 1600, 900

# Still of each client site for the flipping browser: (slug, second in recording)
BROWSER_STILLS = [("bezove-udoli", 1.2), ("artglass", 4.2), ("masher", 0.6),
                  ("3mag-events", 1.0), ("escapeboom", 2.2), ("bitez", 1.6)]
DOMAINS = {p["slug"]: p["domain"] for p in WORK}
SLIDE = 3.0  # seconds per site


def headline(t: dict) -> tuple[str, str]:
    """Two lines in Goia Display; the 'e' in 'We' and the 'i' in 'wish' are the
    hand-drawn brand letters, like on meui-creative.com."""
    size, wght = 116, 80
    lines = [("We build what", 386, 1), ("we wish existed.", 512, 4)]
    out, css = [], []
    word_i = 0
    for text, base, doodle_at in lines:
        glyphs, width = text_glyphs(text, VW / 2, base, "display", wght, size, anchor="middle")
        # Group glyph paths per word so words can rise one after another.
        words, cur = [], []
        for idx, (ch, d, gx) in enumerate(glyphs):
            if ch == " ":
                words.append(cur)
                cur = []
                continue
            cur.append((idx, ch, d, gx))
        words.append(cur)
        for word in words:
            parts = []
            for idx, ch, d, gx in word:
                if idx == doodle_at:
                    adv = measure(text[: idx + 1], "display", wght, size) - measure(text[:idx], "display", wght, size)
                    if ch == "e":
                        g, dw = place("e", 0, 0, size * 0.74, t["green"], cls="doodle-e")
                        parts.append(f'<g transform="translate({gx + adv / 2 - dw / 2 + 2:.1f} {base - size * 0.66:.1f})">{g}</g>')
                    else:
                        g, dw = place("i", 0, 0, size * 0.8, t["pink"], cls="doodle-i")
                        parts.append(f'<g transform="translate({gx + adv / 2 - dw / 2:.1f} {base - size * 0.8:.1f})">{g}</g>')
                else:
                    parts.append(f'<path d="{d}"/>')
            out.append(f'<g class="word" style="animation-delay:{0.25 + word_i * 0.09:.2f}s">{"".join(parts)}</g>')
            word_i += 1
    return f'<g fill="{t["ink"]}">{"".join(out)}</g>', ""


def crafts(t: dict) -> str:
    items = [("development", "Development", "#56745c"), ("design", "Design", "#a085d1"),
             ("production", "Production", "#e8906d"), ("marketing", "Marketing", "#5da9a9")]
    size = 30
    gap, icon_h, pad = 46, 40, 12
    widths = [icon_h * 0.9 + pad + measure(label, "text", 50, size) for _, label, _ in items]
    total = sum(widths) + gap * (len(items) - 1)
    x = VW / 2 - total / 2
    y = 606
    out = []
    for i, ((doodle, label, color), w) in enumerate(zip(items, widths)):
        g, iw = place(doodle, x, y - icon_h + 8, icon_h, color)
        d, _ = text_path(label, x + iw + pad, y, "text", 50, size)
        out.append(f'<g class="chip" style="animation-delay:{1.0 + i * 0.1:.1f}s">{g}'
                   f'<path d="{d}" fill="rgba({t["ink_rgb"]},0.72)"/></g>')
        x += w + gap
    return "".join(out)


def card(x, y, rot, inner, delay, float_cls):
    return (f'<g transform="translate({x} {y}) rotate({rot})"><g class="in" style="animation-delay:{delay}s">'
            f'<g class="{float_cls}">{inner}</g></g></g>')


def browser(t: dict) -> str:
    w, h, chrome = 350, 219, 28
    shots = []
    for i, (slug, sec) in enumerate(BROWSER_STILLS):
        still = frame_at(SHOWCASE / slug / f"{slug}.mp4", sec, f"{slug}-{sec}")
        uri = webp_data(still, w * 2 // 2, q=70)
        cls = "slide" + (" first" if i == 0 else "")
        shots.append(f'<image class="{cls}" style="animation-delay:{i * SLIDE - 0.001:.3f}s" href="{uri}" '
                     f'x="0" y="{chrome}" width="{w}" height="{h}" preserveAspectRatio="xMidYMin slice"/>')
    domains = []
    for i, (slug, _) in enumerate(BROWSER_STILLS):
        d, dw = text_path(DOMAINS[slug], w / 2, 18.5, "text", 55, 11.5, anchor="middle")
        cls = "slide" + (" first" if i == 0 else "")
        domains.append(f'<path class="{cls}" style="animation-delay:{i * SLIDE:.3f}s" d="{d}"/>')
    n = len(BROWSER_STILLS)
    inner = f'''
<rect width="{w}" height="{h + chrome}" rx="12" fill="{t["chrome"]}" filter="url(#sh)"/>
<clipPath id="bclip"><rect y="{chrome}" width="{w}" height="{h}" rx="0"/></clipPath>
<g clip-path="url(#bclip)">{"".join(shots)}</g>
<rect width="{w}" height="{h + chrome}" rx="12" fill="none" stroke="rgba({t["ink_rgb"]},0.08)"/>
<circle cx="16" cy="15" r="4.5" fill="#ff5f57"/><circle cx="31" cy="15" r="4.5" fill="#febc2e"/><circle cx="46" cy="15" r="4.5" fill="#28c840"/>
<rect x="{w / 2 - 85}" y="5" width="170" height="18" rx="9" fill="{t["pill"]}"/>
<g fill="rgba({t["ink_rgb"]},0.6)">{"".join(domains)}</g>
<rect x="0" y="{chrome}" width="{w}" height="2" fill="{t["green"]}" class="progress" style="animation-duration:{SLIDE}s"/>
'''
    return inner, n


def polaroid(t: dict) -> str:
    w = 190
    uri = webp_data(SITE / "images/hero/foto.webp", 170 * 2 // 2, q=72)
    back = webp_data(SITE / "images/hero/some.webp", 170, q=60)
    return f'''
<g transform="rotate(-9 95 110)" opacity="0.95"><rect x="0" y="0" width="{w}" height="226" rx="3" fill="#fbf8f2" filter="url(#sh)"/>
<image href="{back}" x="10" y="10" width="170" height="170" preserveAspectRatio="xMidYMid slice"/></g>
<rect x="0" y="0" width="{w}" height="226" rx="3" fill="#fffdf8" filter="url(#sh)"/>
<image href="{uri}" x="10" y="10" width="170" height="170" preserveAspectRatio="xMidYMid slice"/>
<rect x="10" y="10" width="170" height="170" fill="#fff" class="flash"/>
'''


def design_canvas(t: dict) -> str:
    w, h = 250, 164
    uri = webp_data(SITE / "images/hero/logo.webp", w, q=78)
    handles = "".join(f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" fill="#fff" stroke="#a085d1" stroke-width="1.5"/>'
                      for x, y in ((0, 0), (w, 0), (0, h), (w, h)))
    return f'''
<rect width="{w}" height="{h}" rx="6" fill="#fff" filter="url(#sh)"/>
<image href="{uri}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{w}" height="{h}" fill="none" stroke="#a085d1" stroke-width="1.5" class="select"/>
<g class="select">{handles}</g>
'''


def phone(t: dict, src: str, w: int, h: int, notch: bool = True) -> str:
    uri = webp_data(SITE / src, w * 2 // 2, q=70)
    return f'''
<rect x="-6" y="-6" width="{w + 12}" height="{h + 12}" rx="26" fill="#111" filter="url(#sh)"/>
<clipPath id="pc{w}"><rect width="{w}" height="{h}" rx="20"/></clipPath>
<image href="{uri}" width="{w}" height="{h}" clip-path="url(#pc{w})" preserveAspectRatio="xMidYMin slice"/>
{f'<rect x="{w / 2 - 22}" y="6" width="44" height="12" rx="6" fill="#111"/>' if notch else ""}
'''


def print_poster(t: dict) -> str:
    w, h = 214, 300
    uri = webp_data(SITE / "images/hero/print.webp", w, q=72)
    ink = f"rgba({t['ink_rgb']},0.45)"
    m = 14
    marks = "".join(f'<path d="{d}" stroke="{ink}" stroke-width="1.2" fill="none"/>' for d in (
        f"M{-m} 0h{m - 4}M0 {-m}v{m - 4}", f"M{w + m} 0h-{m - 4}M{w} {-m}v{m - 4}",
        f"M{-m} {h}h{m - 4}M0 {h + m}v-{m - 4}", f"M{w + m} {h}h-{m - 4}M{w} {h + m}v-{m - 4}"))
    cmyk = "".join(f'<rect x="{i * 14}" y="{h + 8}" width="14" height="7" fill="{c}"/>'
                   for i, c in enumerate(("#00aeef", "#ec008c", "#fff200", "#231f20")))
    return f'''
<rect width="{w}" height="{h}" fill="#fff" filter="url(#sh)"/>
<image href="{uri}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>
{marks}{cmyk}
'''


def search_ad(t: dict) -> str:
    """A paid-search result for one of our clients, typed out live."""
    w, h = 360, 150
    ink = t["ink_rgb"]
    query = "únikové hry liberec"
    q, qw = text_path(query, 44, 38, "text", 48, 17)
    spons, _ = text_path("Sponzorováno", 20, 78, "text", 70, 13)
    url, _ = text_path("escapeboom.cz", 20, 97, "text", 45, 13)
    title, _ = text_path("Únikové hry v Liberci: 5 her", 20, 122, "text", 55, 19)
    desc, _ = text_path("Rezervujte online, dárkové vouchery, akce pro firmy.", 20, 142, "text", 40, 12.5)
    return f'''
<rect width="{w}" height="{h + 12}" rx="14" fill="{t["card"]}" filter="url(#sh)"/>
<rect x="12" y="12" width="{w - 24}" height="38" rx="19" fill="{t["pill"]}"/>
<circle cx="31" cy="31" r="6" fill="none" stroke="rgba({ink},0.5)" stroke-width="2"/><path d="M35.5 35.5l4 4" stroke="rgba({ink},0.5)" stroke-width="2" stroke-linecap="round"/>
<clipPath id="typed"><rect class="typing" x="44" y="14" width="{qw + 2:.0f}" height="34"/></clipPath>
<path d="{q}" fill="rgba({ink},0.85)" clip-path="url(#typed)"/>
<rect class="caret" x="44" y="22" width="1.8" height="20" fill="{t["ink"]}"/>
<g class="results"><path d="{spons}" fill="{t["ink"]}"/><path d="{url}" fill="rgba({ink},0.6)"/>
<path d="{title}" fill="#5da9a9"/><path d="{desc}" fill="rgba({ink},0.6)"/></g>
''', qw


def video_player(t: dict) -> str:
    w, h = 300, 176
    uri = webp_data(SITE / "images/hero/video.webp", w, q=70)
    return f'''
<rect width="{w}" height="{h}" rx="10" fill="#000" filter="url(#sh)"/>
<clipPath id="vclip"><rect width="{w}" height="{h}" rx="10"/></clipPath>
<g clip-path="url(#vclip)"><image class="kenburns" href="{uri}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>
<rect y="{h - 34}" width="{w}" height="34" fill="rgba(0,0,0,0.45)"/></g>
<circle cx="{w / 2}" cy="{h / 2 - 10}" r="22" fill="#e8906d"/><path d="M{w / 2 - 6} {h / 2 - 22}l18 12-18 12z" fill="#fff"/>
<rect x="14" y="{h - 17}" width="{w - 28}" height="3" rx="1.5" fill="rgba(255,255,255,0.3)"/>
<rect class="scrub" x="14" y="{h - 17}" width="{w - 28}" height="3" rx="1.5" fill="#e8906d"/>
'''


def cursor(name: str, color: str, t: dict, cls: str) -> str:
    g, cw = place("cursors/cursor.svg", 0, 0, 30, color)
    label, lw = text_path(name, 26, 44, "text", 60, 13)
    return (f'<g class="{cls}">{g}<rect x="18" y="30" width="{lw + 16:.0f}" height="20" rx="6" fill="{color}"/>'
            f'<path d="{label}" fill="#fff" transform="translate(0 -1)"/></g>')


def logo(t: dict) -> str:
    """The wordmark, letters dropping in the way the animated logo GIF does it."""
    import re
    src = (SITE / "logo" / ("meui-creative.svg" if True else "")).read_text()
    paths = re.findall(r"<(?:path|polygon|rect)([^>]*)/>", src)
    h = 54
    s = h / 788.54
    x0 = VW / 2 - 2000 * s / 2
    out = []
    for i, attrs in enumerate(paths):
        if m := re.search(r'points="([^"]+)"', attrs):
            d = "M" + m.group(1).strip() + "Z"
        elif m := re.search(r'x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)"', attrs):
            x, y, rw, rh = m.groups()
            d = f"M{x} {y}h{rw}v{rh}h-{rw}Z"
        else:
            d = re.search(r' d="([^"]+)"', attrs).group(1)
        fill = t["ink"]
        if 'cls-2' in attrs:
            fill = t["green"]
        elif 'cls-1' in attrs:
            fill = t["pink"]
        out.append(f'<path class="drop" style="animation-delay:{0.05 * i:.2f}s" d="{d}" fill="{fill}"/>')
    return f'<g transform="translate({x0:.1f} 150) scale({s:.5f})">{"".join(out)}</g>'


def build(theme: str) -> str:
    t = THEMES[theme]
    head, _ = headline(t)
    bro, n = browser(t)
    ad, qw = search_ad(t)
    loop = n * SLIDE
    pct = 100 / n
    typing_steps = 19
    css = f'''
.in{{animation:pop .9s cubic-bezier(.2,1.4,.4,1) both;transform-box:fill-box;transform-origin:center}}
@keyframes pop{{from{{opacity:0;transform:scale(.8) translateY(30px)}}to{{opacity:1;transform:none}}}}
.word{{animation:rise .8s cubic-bezier(.2,.9,.3,1) both}}
@keyframes rise{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
.chip{{animation:rise .7s cubic-bezier(.2,.9,.3,1) both}}
.drop{{animation:drop .9s cubic-bezier(.3,1.5,.5,1) both}}
@keyframes drop{{from{{opacity:0;transform:translateY(-260px)}}to{{opacity:1;transform:none}}}}
.f1,.f2,.f3,.f4{{transform-box:fill-box;transform-origin:center;animation:float 6s ease-in-out infinite alternate}}
.f2{{animation-duration:7.5s;animation-delay:-2s}}.f3{{animation-duration:5.2s;animation-delay:-4s}}.f4{{animation-duration:8.4s;animation-delay:-1s}}
@keyframes float{{from{{transform:translateY(-7px) rotate(-.8deg)}}to{{transform:translateY(7px) rotate(.8deg)}}}}
.doodle-e{{transform-box:fill-box;transform-origin:50% 90%;animation:epop 1s .9s cubic-bezier(.2,1.6,.4,1) both,wiggle 5s 2.4s ease-in-out infinite}}
@keyframes epop{{from{{transform:scale(0) rotate(-40deg)}}to{{transform:none}}}}
@keyframes wiggle{{0%,80%,100%{{transform:rotate(0)}}85%{{transform:rotate(-9deg)}}90%{{transform:rotate(7deg)}}95%{{transform:rotate(-3deg)}}}}
.doodle-i{{transform-box:fill-box;transform-origin:50% 100%;animation:idrop .9s 1.2s cubic-bezier(.3,1.6,.5,1) both,hop 4.2s 3s ease-in-out infinite}}
@keyframes idrop{{from{{transform:translateY(-300px)}}to{{transform:none}}}}
@keyframes hop{{0%,70%,100%{{transform:none}}76%{{transform:scale(1.08,.86)}}84%{{transform:translateY(-26px) scale(.96,1.06)}}92%{{transform:scale(1.05,.94)}}}}
.slide{{opacity:0;animation:slide {loop}s linear infinite}}
.slide.first{{opacity:1}}
@keyframes slide{{0%{{opacity:0}}{pct * 0.08:.2f}%{{opacity:1}}{pct:.2f}%{{opacity:1}}{pct * 1.08:.2f}%{{opacity:0}}100%{{opacity:0}}}}
.progress{{transform-box:fill-box;transform-origin:left;animation:grow linear infinite}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.scrub{{transform-box:fill-box;transform-origin:left;animation:grow 9s linear infinite}}
.kenburns{{transform-box:fill-box;transform-origin:center;animation:kb 9s ease-in-out infinite alternate}}
@keyframes kb{{from{{transform:scale(1)}}to{{transform:scale(1.12) translateX(-8px)}}}}
.flash{{opacity:0;animation:flash 7s 2s infinite}}
@keyframes flash{{0%,96%,100%{{opacity:0}}97%{{opacity:.9}}}}
.typing{{transform-box:fill-box;transform-origin:left;animation:type 8s steps({typing_steps}) infinite}}
@keyframes type{{0%{{transform:scaleX(0)}}45%,100%{{transform:scaleX(1)}}}}
.caret{{animation:caret 8s steps({typing_steps}) infinite,blink .8s steps(1) infinite}}
@keyframes caret{{0%{{transform:translateX(0)}}45%,100%{{transform:translateX({qw + 3:.0f}px)}}}}
@keyframes blink{{50%{{opacity:0}}}}
.results{{animation:results 8s infinite}}
@keyframes results{{0%,48%{{opacity:.15}}56%,96%{{opacity:1}}100%{{opacity:.15}}}}
.select{{animation:sel 12s infinite}}
@keyframes sel{{0%,14%{{opacity:0}}18%,62%{{opacity:1}}66%,100%{{opacity:0}}}}
.cur-a{{animation:cura 12s cubic-bezier(.45,0,.25,1) infinite}}
.cur-a{{transform:translate(1236px,214px)}}
@keyframes cura{{0%{{transform:translate(1300px,430px)}}14%{{transform:translate(1236px,214px)}}17%{{transform:translate(1236px,214px) scale(.85)}}20%{{transform:translate(1236px,214px)}}40%{{transform:translate(1210px,196px)}}62%{{transform:translate(1210px,196px)}}82%{{transform:translate(1270px,560px)}}100%{{transform:translate(1300px,430px)}}}}
.cur-b{{animation:curb 14s cubic-bezier(.45,0,.25,1) infinite}}
.cur-b{{transform:translate(214px,104px)}}
@keyframes curb{{0%{{transform:translate(320px,440px)}}20%{{transform:translate(214px,104px)}}24%{{transform:translate(214px,104px) scale(.85)}}28%{{transform:translate(214px,104px)}}55%{{transform:translate(300px,260px)}}80%{{transform:translate(330px,640px)}}100%{{transform:translate(320px,440px)}}}}
.octo{{transform-box:fill-box;transform-origin:50% 100%;animation:octo 3.6s ease-in-out infinite alternate}}
@keyframes octo{{from{{transform:rotate(-6deg) translateY(4px)}}to{{transform:rotate(6deg) translateY(-6px)}}}}
.octo-in{{animation:peek 1.2s 1.6s cubic-bezier(.2,1.4,.4,1) both}}
@keyframes peek{{from{{transform:translateY(160px)}}to{{transform:none}}}}
{REDUCED_MOTION}
'''
    octo, _ = place("chobotnicka", 0, 0, 110, None, cls="octo")
    pron, _ = text_path("mý · jů · áj   —   Liberec, CZ", VW / 2, 238, "text", 45, 20, anchor="middle")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}">
<title>Meui Creative, a creative studio from Liberec: we build what we wish existed</title>
<style>{css}</style>
<defs>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="13" cy="13" r="1.5" fill="{t["dot"]}"/></pattern>
  <filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#000" flood-opacity="{0.14 if theme == "light" else 0.55}"/></filter>
</defs>
<rect width="{VW}" height="{VH}" rx="28" fill="{t["surface"]}"/>
<rect width="{VW}" height="{VH}" rx="28" fill="url(#dots)"/>
{card(40, 78, -5, bro, 0.2, "f1")}
{card(482, 34, 7, polaroid(t), 0.35, "f2")}
{card(1000, 62, 3, design_canvas(t), 0.5, "f3")}
{card(1340, 118, 8, phone(t, "images/hero/some.webp", 150, 268, notch=False), 0.45, "f4")}
{card(78, 540, -4, print_poster(t), 0.6, "f2")}
{card(1010, 650, 6, phone(t, "images/hero/app.webp", 124, 290), 0.7, "f1")}
{card(1232, 660, 5, video_player(t), 0.65, "f3")}
{card(410, 694, 3, ad, 0.75, "f4")}
{logo(t)}
<path d="{pron}" fill="rgba({t["ink_rgb"]},0.5)" class="chip" style="animation-delay:.6s"/>
{head}
{crafts(t)}
<g transform="translate(832 782)"><g class="octo-in">{octo}</g></g>
{cursor("Marián", "#a085d1", t, "cur-a")}
{cursor("Matěj", "#56745c", t, "cur-b")}
</svg>'''


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        svg = build(theme)
        path = ASSETS / f"hero-{theme}.svg"
        path.write_text(svg)
        print(path.name, f"{len(svg) / 1024:.0f} KB")
