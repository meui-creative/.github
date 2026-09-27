"""Client-work cards: a looping showcase clip inside a browser window, with caption.

    .venv/bin/python scripts/cards.py [slug ...] [--frames-only]

For every project and theme this renders an overlay PNG (card, window chrome,
caption; transparent where the video goes), composites the recording under it
with ffmpeg and encodes AVIF + WebP (+ a small GIF fallback for light).

The loop is seamless: the clip's last `XF` seconds cross-fade into its first
frames, so there is no jump when the animation restarts.
"""

import shutil
import subprocess
import sys

from lib.brand import ASSETS, BUILD, SHOWCASE, THEMES
from lib.projects import WORK
from lib.text import text_path

W, H = 880, 720
WX, WY, WW = 40, 34, 800
CHROME = 40
CX, CY, CW, CH = WX, WY + CHROME, WW, 500
FPS = 20
XF = 0.6  # loop cross-fade, seconds


def overlay_svg(p: dict, theme: str) -> str:
    t = THEMES[theme]
    ink = t["ink_rgb"]
    title, tw = text_path(p["name"], 44, 632, "display", 72, 36)
    line, _ = text_path(p["line"], 44, 672, "text", 45, 22)
    stack, _ = text_path(p["stack"], W - 44, 630, "text", 55, 17, anchor="end", tracking=0.01)
    domain, dw = text_path(p["domain"], 0, 0, "text", 55, 15)
    pill_w = max(260, dw + 64)
    px = WX + WW / 2 - pill_w / 2
    lock_x = WX + WW / 2 - (dw + 20) / 2
    domain, _ = text_path(p["domain"], lock_x + 20, WY + 25, "text", 55, 15)
    # ↗ drawn by hand; Goia has no arrows.
    ax, ay = 44 + tw + 14, 605
    arrow = f"M{ax} {ay + 18}L{ax + 18} {ay}M{ax + 5} {ay}H{ax + 18}V{ay + 13}"
    r = 14
    content_hole = (f"M{CX} {CY}H{CX + CW}V{CY + CH - r}a{r} {r} 0 0 1-{r} {r}"
                    f"H{CX + r}a{r} {r} 0 0 1-{r}-{r}Z")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1.3" fill="{t["dot"]}"/></pattern>
  <filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="rgb({t["shadow"]})" flood-opacity="{0.16 if theme == "light" else 0.5}"/></filter>
  <mask id="hole" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
    <rect width="{W}" height="{H}" fill="#fff"/><path d="{content_hole}" fill="#000"/>
  </mask>
</defs>
<g mask="url(#hole)">
  <rect width="{W}" height="{H}" fill="{t["page"]}"/>
  <rect width="{W}" height="{H}" rx="22" fill="{t["surface"]}"/>
  <rect width="{W}" height="{H}" rx="22" fill="url(#dots)"/>
  <rect x="{WX}" y="{WY}" width="{WW}" height="{CHROME + CH}" rx="{r}" fill="{t["chrome"]}" filter="url(#sh)"/>
  <rect x="{WX}" y="{WY}" width="{WW}" height="{CHROME + CH}" rx="{r}" fill="{t["chrome"]}"/>
  <circle cx="{WX + 22}" cy="{WY + 20}" r="6" fill="#ff5f57"/>
  <circle cx="{WX + 42}" cy="{WY + 20}" r="6" fill="#febc2e"/>
  <circle cx="{WX + 62}" cy="{WY + 20}" r="6" fill="#28c840"/>
  <rect x="{px}" y="{WY + 7}" width="{pill_w}" height="26" rx="13" fill="{t["pill"]}"/>
  <g fill="none" stroke="rgba({ink},0.45)" stroke-width="1.6" stroke-linecap="round">
    <rect x="{lock_x}" y="{WY + 16}" width="10" height="8" rx="2" fill="rgba({ink},0.45)" stroke="none"/>
    <path d="M{lock_x + 2.2} {WY + 16}v-2.2a2.8 2.8 0 0 1 5.6 0V{WY + 16}"/>
  </g>
  <path d="{domain}" fill="rgba({ink},0.62)"/>
  <path d="{title}" fill="{t["ink"]}"/>
  <path d="{arrow}" fill="none" stroke="{t["pink"]}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="{line}" fill="rgba({ink},0.6)"/>
  <path d="{stack}" fill="{t["green"]}"/>
</g>
</svg>'''


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def build(p: dict, frames_only: bool) -> None:
    src = SHOWCASE / p["slug"] / f"{p['slug']}.mp4"
    start, dur = p["clip"]
    for theme in THEMES:
        work = BUILD / "cards" / f"{p['slug']}-{theme}"
        shutil.rmtree(work, ignore_errors=True)
        (work / "frames").mkdir(parents=True)
        svg = work / "overlay.svg"
        svg.write_text(overlay_svg(p, theme))
        run(["rsvg-convert", str(svg), "-o", str(work / "overlay.png")])

        graph = (
            f"[0:v]fps={FPS},scale={CW}:{CH}:flags=lanczos,split[a][b];"
            f"[a]trim=start={XF},setpts=PTS-STARTPTS[m];"
            f"[b]trim=end={XF},setpts=PTS-STARTPTS[h];"
            f"[m][h]xfade=transition=fade:duration={XF}:offset={dur - XF},"
            f"pad={W}:{H}:{CX}:{CY}:color=black[v];"
            f"[v][1:v]overlay=0:0:shortest=1,format=rgb24"
        )
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(dur + XF), "-i", str(src),
             "-loop", "1", "-i", str(work / "overlay.png"), "-filter_complex", graph,
             "-frames:v", str(int(dur * FPS)), str(work / "frames/%04d.png")])
        # First frame doubles as the static poster (used in the preview and as og fallback).
        shutil.copy(work / "frames/0001.png", work / "poster.png")
        if frames_only:
            continue

        out = ASSETS / "work"
        out.mkdir(parents=True, exist_ok=True)
        base = out / f"{p['slug']}-{theme}"
        run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(work / "frames/%04d.png"),
             "-c:v", "libsvtav1", "-crf", "42", "-preset", "4", "-pix_fmt", "yuv420p",
             "-svtav1-params", "tune=0", "-f", "avif", f"{base}.avif"])
        frames = sorted((work / "frames").glob("*.png"))
        run(["img2webp", "-loop", "0", "-lossy", "-q", "52", "-m", "6", "-d", str(1000 // FPS),
             *map(str, frames), "-o", f"{base}.webp"])
        if theme == "light":
            # Last-resort fallback for clients without AVIF/WebP. Small on purpose.
            run(["gifski", "--fps", "10", "--width", "440", "--quality", "70", "-q",
                 "-o", str(out / f"{p['slug']}.gif"), *map(str, frames[::2])])


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for p in WORK:
        if not args or p["slug"] in args:
            print("→", p["slug"], flush=True)
            build(p, "--frames-only" in sys.argv)
