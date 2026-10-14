#!/usr/bin/env bash
# Resume the ds005237 fMRIPrep batch after any stop (WSL shutdown, reboot).
# Clears the fMRIPrep work and derivative folders of participants that have
# no DONE marker, so nipype cannot reuse a half-written cached file, then runs
# run_all.sh with 2 parallel jobs (3 ran out of memory on 2026-10-10).
# Run by the bio-batch01 systemd unit at every WSL boot.
set -euo pipefail
ROOT=/mnt/h/bio-data/ds005237
for i in $(seq 1 60); do [ -d "$ROOT" ] && break; sleep 5; done
[ -d "$ROOT" ] || { echo "H: not mounted at $ROOT" >&2; exit 1; }
for d in "$ROOT"/work/sub-*; do
  [ -e "$d" ] || continue
  s=$(basename "$d")
  if [ ! -f "$ROOT/conn01/$s/DONE" ]; then
    echo "[$(date -Is)] clearing partial $s"
    rm -rf "$d" "$ROOT/derivatives/fmriprep/$s" "$ROOT/derivatives/fmriprep/$s.html"
  fi
done
exec env JOBS=2 bash "$(dirname "$0")/run_all.sh"
