#!/usr/bin/env bash
# Run one preprocessing pipeline over every ds005237 participant, up to 3 at
# once. PIPELINE=fmriprep (default) runs run_fmriprep_one.sh; PIPELINE=afni
# runs run_afni_one.sh (prereg 01 deviation 4) and needs no FreeSurfer
# license. One output directory holds one pipeline: if $ROOT/conn01 (or
# CONN_OUT) already holds the other pipeline's outputs, this refuses to start
# (scripts/pipeline_guard.sh).
# Resumable: a participant with $ROOT/conn01/sub-<label>/DONE is skipped.
# Logs: $ROOT/logs/sub-<label>.{fetch,fmriprep,extract,run}.log and
# $ROOT/logs/run_all.log. A failed participant keeps its logs and is retried
# on the next invocation; its partial inputs are left for inspection.
#
#   [PIPELINE=afni|fmriprep] run_all.sh [PARTICIPANT_LIST_FILE]
#
# fmriprep refuses to start without the FreeSurfer license or the fMRIPrep
# image; afni refuses without the AFNI binaries, the fMRIPrep image (for FSL
# FAST) or the TemplateFlow 2 mm grid.
# Before each participant it waits until H: has MIN_FREE_GB free (default 60;
# one participant needs about 2.5 GB of input plus the fMRIPrep work dir).
set -euo pipefail

DATA=${DATA:-/mnt/h/bio-data}
ROOT=${DS_ROOT:-$DATA/ds005237}
SIF=${SIF:-$DATA/containers/fmriprep-25.2.6.sif}
LICENSE=${FS_LICENSE:-$DATA/freesurfer/license.txt}
VENV=${VENV:-$DATA/venvs/conn01}
ABIN=${AFNI_BIN:-$DATA/afni/abin}
PIPELINE=${PIPELINE:-fmriprep}
OUT=${CONN_OUT:-$ROOT/conn01}
JOBS=${JOBS:-3}
MIN_FREE_GB=${MIN_FREE_GB:-60}
HERE=$(cd "$(dirname "$0")" && pwd)

case "$PIPELINE" in
  fmriprep) ONE="$HERE/run_fmriprep_one.sh" ;;
  afni) ONE="$HERE/run_afni_one.sh" ;;
  *) echo "REFUSING TO START: PIPELINE must be afni or fmriprep, got '$PIPELINE'" >&2; exit 2 ;;
esac

fail=0
if [ "$PIPELINE" = fmriprep ] && [ ! -f "$LICENSE" ]; then
  echo "REFUSING TO START: FreeSurfer license not found at $LICENSE" >&2
  echo "  Get one at https://surfer.nmr.mgh.harvard.edu/registration.html and save it there." >&2
  fail=1
fi
if [ ! -f "$SIF" ]; then
  echo "REFUSING TO START: fMRIPrep image not found at $SIF" >&2
  echo "  Build it with scripts/setup_fmriprep.sh (apptainer build)." >&2
  fail=1
fi
if [ ! -x "$VENV/bin/python" ]; then
  echo "REFUSING TO START: analysis venv not found at $VENV" >&2
  fail=1
fi
if [ "$PIPELINE" = afni ]; then
  TFG=${TEMPLATEFLOW_HOME:-$DATA/templateflow}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-02_T1w.nii.gz
  for f in "$ABIN/afni_proc.py" "$ABIN/MNI152_2009_template_SSW.nii.gz" "$TFG"; do
    if [ ! -s "$f" ]; then echo "REFUSING TO START: missing $f" >&2; fail=1; fi
  done
fi
[ "$fail" = 0 ] || exit 2

# shellcheck source=pipeline_guard.sh
. "$HERE/pipeline_guard.sh"
pipeline_guard "$OUT" "$PIPELINE" || exit 3

mkdir -p "$ROOT/logs" "$OUT"
LIST=${1:-$ROOT/participants_list.txt}
[ -f "$LIST" ] || bash "$HERE/ds005237_fetch.sh" --list
LIST=${1:-$ROOT/participants_list.txt}

one() {
  local sub=$1
  if [ -f "$OUT/sub-$sub/DONE" ]; then echo "skip sub-$sub (done)"; return 0; fi
  while [ "$(df -BG --output=avail "$DATA" | tail -1 | tr -dc 0-9)" -lt "$MIN_FREE_GB" ]; do
    echo "[$(date -Is)] sub-$sub waiting for disk (< ${MIN_FREE_GB} GB free)"; sleep 300
  done
  if CONN_OUT="$OUT" bash "$ONE" "$sub" > "$ROOT/logs/sub-$sub.run.log" 2>&1; then
    echo "[$(date -Is)] ok sub-$sub"
  else
    echo "[$(date -Is)] FAILED sub-$sub (exit $?), see $ROOT/logs/sub-$sub.*.log"
  fi
}
export -f one
export ROOT DATA HERE MIN_FREE_GB SIF LICENSE VENV OUT ONE AFNI_BIN=$ABIN

total=$(grep -c . "$LIST")
done_n=$(find "$OUT" -maxdepth 2 -name DONE | wc -l)
echo "[$(date -Is)] start: PIPELINE=$PIPELINE, $total participants, $done_n already done, $JOBS parallel" \
  | tee -a "$ROOT/logs/run_all.log"
grep . "$LIST" | xargs -P "$JOBS" -I{} bash -c 'one "$@"' _ {} \
  | tee -a "$ROOT/logs/run_all.log"
done_n=$(find "$OUT" -maxdepth 2 -name DONE | wc -l)
echo "[$(date -Is)] end: $done_n of $total done" | tee -a "$ROOT/logs/run_all.log"
