#!/usr/bin/env bash
# Render one fMRIPrep reportlet with each layer removed in turn.
# Usage: render_layers.sh SVG OUTPREFIX
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
svg="$1"; out="$2"; tmp=$(mktemp -d)
echo "classes: $(grep -o 'class="[^"]*"' "$svg" | sort -u | head -8 | tr '\n' ' ')"
for drop in background foreground; do
  if python3 "$here/svg_second_frame.py" "$svg" "$tmp/x.svg" "$drop"; then
    rsvg-convert -w 1400 "$tmp/x.svg" -o "${out}_no-${drop}.png"
  fi
done
rm -rf "$tmp"
