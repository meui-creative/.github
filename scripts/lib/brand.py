"""Meui Creative brand tokens, mirrored from meui-creative/src/app/(frontend)/globals.css."""

from pathlib import Path

GREEN = "#56745c"
GREEN_LOGO = "#43755a"
PINK = "#d87ac9"
PINK_LOGO = "#ffaaf1"
BEIGE = "#f3e9d7"
TURQUOISE = "#5da9a9"
ORANGE = "#e8906d"
PURPLE = "#a085d1"

THEMES = {
    "light": {
        "surface": BEIGE,
        "ink": "#000000",
        "ink_rgb": "0,0,0",
        "card": "#ffffff",
        "chrome": "#f7f4ee",
        "pill": "#ece6db",
        "dot": "rgba(0,0,0,0.09)",
        "page": "#ffffff",  # GitHub light page background, baked into rounded corners
        "shadow": "0,0,0",
        "pink": PINK,
        "green": GREEN,
    },
    "dark": {
        "surface": "#191919",
        "ink": "#e5e5e5",
        "ink_rgb": "229,229,229",
        "card": "#212121",
        "chrome": "#262626",
        "pill": "#1b1b1b",
        "dot": "rgba(255,255,255,0.07)",
        "page": "#0d1117",  # GitHub dark page background
        "shadow": "0,0,0",
        "pink": "#c567b8",
        "green": "#6f9577",
    },
}

ROOT = Path(__file__).resolve().parents[2]
SITE = Path.home() / "DEV/meui-creative/public"
SHOWCASE = Path.home() / "DEV/meui-creative/scripts/showcase/out"
ASSETS = ROOT / "profile/assets"
BUILD = ROOT / "build"


def dot_grid(pid: str, color: str, step: int = 24, r: float = 1.4) -> tuple[str, str]:
    """(defs, fill) for the dotted canvas the studio site uses behind its hero."""
    defs = (f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<circle cx="{step / 2}" cy="{step / 2}" r="{r}" fill="{color}"/></pattern>')
    return defs, f"url(#{pid})"
