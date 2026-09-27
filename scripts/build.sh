#!/usr/bin/env bash
# Regenerates every asset in profile/assets.
#   scripts/build.sh          everything (client cards take ~10 minutes)
#   scripts/build.sh --fast   SVGs only, keeps the encoded clips
#
# Needs: python3, ffmpeg with libsvtav1, img2webp, gifski, rsvg-convert,
# the Goia fonts in ~/DEV/meui-creative/src/fonts (licensed, never committed)
# and the showcase recordings from `bun run showcase` in that repo.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d .venv ] || { python3 -m venv .venv && .venv/bin/pip -q install fonttools uharfbuzz; }
mkdir -p build/fonts build/stills
[ -f build/fonts/JetBrainsMono.ttf ] || curl -sL -o build/fonts/JetBrainsMono.ttf \
  "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/variable/JetBrainsMono%5Bwght%5D.ttf"
[ -f build/fonts/Nunito.ttf ] || curl -sL -o build/fonts/Nunito.ttf \
  "https://github.com/google/fonts/raw/main/ofl/nunito/Nunito%5Bwght%5D.ttf"
# Froggies has no product art on the website; its card is composed from game
# screenshots in build/froggies/ (captured with scripts/capture-froggies.mjs).
[ -d build/froggies ] && .venv/bin/python scripts/froggies_card.py

PY=.venv/bin/python
for s in hero stats products terminal team headings; do $PY scripts/$s.py; done
[ "${1:-}" = "--fast" ] || $PY scripts/cards.py
