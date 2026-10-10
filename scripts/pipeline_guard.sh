#!/usr/bin/env bash
# Sourced by run_all.sh, run_fmriprep_one.sh and run_afni_one.sh.
# Prereg 01 deviation 4: the whole sample uses one preprocessing pipeline.
#
#   pipeline_guard OUTDIR afni|fmriprep
#
# OUTDIR/PIPELINE names the pipeline that owns the directory. If it is
# missing, the guard infers the owner from any existing per-participant QC
# JSON ("fmriprep_generated_by" Name) and refuses on a mismatch. It writes
# the marker on first use. Returns non-zero and prints why when refusing.

pipeline_guard() {
  local out=$1 want=$2 have="" qc name
  case "$want" in afni|fmriprep) ;; *) echo "pipeline_guard: unknown pipeline '$want'" >&2; return 2;; esac
  mkdir -p "$out"
  if [ -f "$out/PIPELINE" ]; then
    have=$(tr -d ' \r\n' < "$out/PIPELINE")
  else
    for qc in "$out"/sub-*/sub-*_qc.json; do
      [ -f "$qc" ] || continue
      if grep -q '"Name": *"AFNI' "$qc"; then name=afni; else name=fmriprep; fi
      if [ -n "$have" ] && [ "$have" != "$name" ]; then
        echo "REFUSING: $out already mixes pipelines ($have and $name)" >&2; return 3
      fi
      have=$name
    done
  fi
  if [ -n "$have" ] && [ "$have" != "$want" ]; then
    echo "REFUSING: $out holds $have outputs; PIPELINE=$want would mix pipelines." >&2
    echo "  Use a separate output directory (DS_ROOT or CONN_OUT) for $want." >&2
    return 3
  fi
  echo "$want" > "$out/PIPELINE"
}
