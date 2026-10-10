#!/usr/bin/env bash
# Render selected fMRIPrep report SVGs to PNG for visual QC: both frames of
# each before/after animation (frame1 = first layer, frame2 = second layer).
# Usage: render_report_figs.sh SUBDIR OUTDIR
set -eu
command -v rsvg-convert >/dev/null || { apt-get install -y -qq librsvg2-bin >/dev/null; }
here="$(cd "$(dirname "$0")" && pwd)"
sub="$1"; out="$2"; mkdir -p "$out"
tmp=$(mktemp -d)
for pat in 'task-restAP_run-01_desc-sdc_bold' 'task-restAP_run-01_desc-coreg_bold' \
           'space-MNI152NLin2009cAsym_T1w' 'task-restAP_run-01_desc-rois_bold'; do
  f=$(ls "$sub"/report/figures/*"$pat".svg | head -1)
  base=$(basename "$f" .svg)
  rsvg-convert -w 1400 "$f" -o "$out/${base}_frame1.png"
  if python3 "$here/svg_second_frame.py" "$f" "$tmp/$base.svg"; then
    rsvg-convert -w 1400 "$tmp/$base.svg" -o "$out/${base}_frame2.png"
  fi
  echo "rendered $base"
done
rm -rf "$tmp"
