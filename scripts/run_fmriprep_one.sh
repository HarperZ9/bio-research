#!/usr/bin/env bash
# One participant, end to end: fetch into its own BIDS root
# $ROOT/bids-<label>, fMRIPrep 25.2.6 (Apptainer), region time series
# extraction, cleanup. Leaves only the fMRIPrep confounds, the
# region time series and QC numbers in $ROOT/conn01/sub-<label>/, then
# writes a DONE marker there.
#
#   run_fmriprep_one.sh SUBLABEL
#
# fMRIPrep options: rest runs only (BIDS filter), MNI152NLin2009cAsym:res-2,
# --fs-no-reconall (prereg 01 uses volumetric atlas regions only, so no
# surfaces are needed; the license file is still passed because fMRIPrep
# uses FreeSurfer tools and its docs require the license without
# exempting --fs-no-reconall), --notrack. KEEP_REPORT=1 keeps the fMRIPrep
# HTML report and figures for visual QC.
set -euo pipefail

SUB=${1:?usage: run_fmriprep_one.sh SUBLABEL}
SUB=${SUB#sub-}
DATA=${DATA:-/mnt/h/bio-data}
ROOT=${DS_ROOT:-$DATA/ds005237}
SIF=${SIF:-$DATA/containers/fmriprep-25.2.6.sif}
LICENSE=${FS_LICENSE:-$DATA/freesurfer/license.txt}
VENV=${VENV:-$DATA/venvs/conn01}
REPO=$(cd "$(dirname "$0")/.." && pwd)
BIDS="$ROOT/bids-$SUB"; DERIV="$ROOT/derivatives/fmriprep"; WORK="$ROOT/work/sub-$SUB"
OUT="$ROOT/conn01"; LOGS="$ROOT/logs"
mkdir -p "$DERIV" "$WORK" "$OUT" "$LOGS" "$DATA/templateflow"

log() { echo "[$(date -Is)] sub-$SUB $*"; }
[ -f "$SIF" ] || { echo "missing fMRIPrep image: $SIF" >&2; exit 2; }
[ -f "$LICENSE" ] || { echo "missing FreeSurfer license: $LICENSE" >&2; exit 2; }
if [ -f "$OUT/sub-$SUB/DONE" ]; then log "already done"; exit 0; fi

log "fetch"
BIDS_DIR="$BIDS" bash "$REPO/scripts/ds005237_fetch.sh" "$SUB" > "$LOGS/sub-$SUB.fetch.log" 2>&1

FILTER="$WORK/bids_filter.json"
cat > "$FILTER" <<'EOF'
{"bold": {"datatype": "func", "suffix": "bold", "task": ["restAP", "restPA"]},
 "t1w": {"datatype": "anat", "suffix": "T1w"}}
EOF

log "fmriprep"
export APPTAINERENV_TEMPLATEFLOW_HOME=/data/templateflow
apptainer run --cleanenv -B "$DATA:/data" "$SIF" \
  "/data/${BIDS#$DATA/}" "/data/${DERIV#$DATA/}" participant \
  --participant-label "$SUB" \
  --bids-filter-file "/data/${FILTER#$DATA/}" \
  --output-spaces MNI152NLin2009cAsym:res-2 \
  --fs-license-file "/data/${LICENSE#$DATA/}" \
  --fs-no-reconall \
  --nthreads 8 --omp-nthreads 4 --mem-mb 7000 \
  -w "/data/${WORK#$DATA/}" \
  --notrack --stop-on-first-crash \
  > "$LOGS/sub-$SUB.fmriprep.log" 2>&1

log "extract"
"$VENV/bin/python" -I -c \
  'import sys; sys.path.insert(0, sys.argv[1]); from conn01.extract import main; sys.exit(main(sys.argv[2:]))' \
  "$REPO/src" --fmriprep-dir "$DERIV" --bids-dir "$BIDS" --participant "$SUB" --out "$OUT" \
  > "$LOGS/sub-$SUB.extract.log" 2>&1

log "cleanup"
cp "$LOGS/sub-$SUB.fetch.log" "$OUT/sub-$SUB/"
if [ "${KEEP_REPORT:-0}" = "1" ]; then
  mkdir -p "$OUT/sub-$SUB/report"
  cp -r "$DERIV/sub-$SUB.html" "$DERIV/sub-$SUB/figures" "$OUT/sub-$SUB/report/"     || log "WARNING: report copy failed"
fi
rm -rf "$BIDS" "$WORK" "$DERIV/sub-$SUB" "$DERIV/sub-$SUB.html"
touch "$OUT/sub-$SUB/DONE"
log "done"
