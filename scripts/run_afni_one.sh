#!/usr/bin/env bash
# One participant through the AFNI fallback path (prereg 01 deviation 4):
# fetch, @SSwarper, afni_proc.py per rest run, fMRIPrep-format confounds,
# region time series via conn01.extract (unchanged), QC, cleanup. Leaves
# the same files as run_fmriprep_one.sh in $OUT/sub-<label>/ (confounds,
# region time series, sub-<label>_qc.json with the same keys) plus
# sub-<label>_desc-afni_qc.json (tSNR, non-steady-state count, mask sizes,
# distortion correction per run) and a registration overlay PNG, then DONE.
#
#   run_afni_one.sh SUBLABEL
#
# No FreeSurfer license is used. Steps, matched to the fMRIPrep path:
#  * anatomy: @SSwarper skull strip + nonlinear warp to AFNI's
#    MNI152_2009_template_SSW (the MNI152NLin2009cAsym template on the same
#    1 mm grid as TemplateFlow's res-01 image); EPI output resampled onto
#    TemplateFlow tpl-MNI152NLin2009cAsym_res-02_T1w (97 x 115 x 97, 2 mm),
#    the grid extract.py and the atlas use;
#  * tissue partial-volume maps: FSL FAST with sMRIPrep's flags (-N -I 0 -g
#    -p), run from the fMRIPrep container (FAST needs no FreeSurfer license);
#    aCompCor masks built as fMRIPrep does (conn01.afni_prep);
#  * per run: slice timing (3dTshift, SliceTiming from the sidecar), blip-up/
#    blip-down distortion correction with the spin-echo field maps when
#    conn01.fmaplink accepts them (else none), motion correction, EPI-T1
#    alignment, one-step warp to MNI 2 mm. No blurring, no scaling, no
#    regression (fMRIPrep's preproc BOLD is not smoothed either).
set -euo pipefail

SUB=${1:?usage: run_afni_one.sh SUBLABEL}
SUB=${SUB#sub-}
DATA=${DATA:-/mnt/h/bio-data}
ROOT=${DS_ROOT:-$DATA/ds005237}
ABIN=${AFNI_BIN:-$DATA/afni/abin}
SIF=${SIF:-$DATA/containers/fmriprep-25.2.6.sif}
VENV=${VENV:-$DATA/venvs/conn01}
TF=${TEMPLATEFLOW_HOME:-$DATA/templateflow}/tpl-MNI152NLin2009cAsym
MASTER="$TF/tpl-MNI152NLin2009cAsym_res-02_T1w.nii.gz"
BASE="$ABIN/MNI152_2009_template_SSW.nii.gz"
REPO=$(cd "$(dirname "$0")/.." && pwd)
BIDS="$ROOT/bids-$SUB"; WORK="$ROOT/work-afni/sub-$SUB"; DERIV="$ROOT/derivatives/afni"
OUT=${CONN_OUT:-$ROOT/conn01}; LOGS="$ROOT/logs"
SPACE="space-MNI152NLin2009cAsym_res-2"
export PATH="$ABIN:$PATH" OMP_NUM_THREADS=${OMP_NUM_THREADS:-8} AFNI_NIFTI_TYPE_WARN=NO
mkdir -p "$WORK" "$DERIV/sub-$SUB/func" "$LOGS"

log() { echo "[$(date -Is)] sub-$SUB $*"; }
for f in "$ABIN/afni_proc.py" "$SIF" "$MASTER" "$BASE"; do
  [ -s "$f" ] || { echo "missing: $f" >&2; exit 2; }
done
# shellcheck source=pipeline_guard.sh
. "$REPO/scripts/pipeline_guard.sh"
pipeline_guard "$OUT" afni || exit 3
if [ -f "$OUT/sub-$SUB/DONE" ]; then log "already done"; exit 0; fi

pyrun() {  # pyrun MODULE ARGS...: run a conn01 module in isolated mode
  local mod=$1; shift
  "$VENV/bin/python" -I -c \
    'import sys, importlib; sys.path.insert(0, sys.argv[1]); m = importlib.import_module(sys.argv[2]); sys.exit(m.main(sys.argv[3:]))' \
    "$REPO/src" "$mod" "$@"
}

log "fetch"
BIDS_DIR="$BIDS" bash "$REPO/scripts/ds005237_fetch.sh" "$SUB" > "$LOGS/sub-$SUB.fetch.log" 2>&1

log "blip plan"
SDC_RECEIPT="$WORK/sdc_receipt.json"
pyrun conn01.afni_prep blip-plan --sub-dir "$BIDS/sub-$SUB" --receipt "$SDC_RECEIPT" \
  > "$WORK/runs.tsv" 2> "$LOGS/sub-$SUB.fmaplink.log"
[ -s "$WORK/runs.tsv" ] || { echo "no rest runs planned for sub-$SUB" >&2; exit 3; }

log "anatomy: @SSwarper"
T1=$(find "$BIDS/sub-$SUB" -path "*/anat/*_T1w.nii.gz" | sort | head -1)
SSW="$WORK/ssw"
@SSwarper -input "$T1" -base "$BASE" -subid "$SUB" -odir "$SSW" \
  > "$LOGS/sub-$SUB.sswarper.log" 2>&1
ANAT_SS="$SSW/anatSS.$SUB.nii"
NLW=("$SSW/anatQQ.$SUB.nii" "$SSW/anatQQ.$SUB.aff12.1D" "$SSW/anatQQ.${SUB}_WARP.nii")

log "anatomy: FAST and aCompCor masks"
mkdir -p "$WORK/fast" "$WORK/pv" "$WORK/pv_mni"
apptainer exec --cleanenv -B "$DATA:$DATA" "$SIF" \
  fast -N -I 0 -g -p -o "$WORK/fast/anat" "$ANAT_SS" > "$LOGS/sub-$SUB.fast.log" 2>&1
pyrun conn01.afni_prep acompcor-masks --csf "$WORK/fast/anat_pve_0.nii.gz" \
  --gm "$WORK/fast/anat_pve_1.nii.gz" --wm "$WORK/fast/anat_pve_2.nii.gz" --out-dir "$WORK/pv"
for k in CSF WM combined; do
  3dNwarpApply -overwrite -quiet -nwarp "${NLW[2]} ${NLW[1]}" -source "$WORK/pv/acompcor_$k.nii.gz" \
    -master "$MASTER" -interp linear -prefix "$WORK/pv_mni/acompcor_$k.nii.gz" >> "$LOGS/sub-$SUB.nwarp.log" 2>&1
done
3dNwarpApply -overwrite -quiet -nwarp "${NLW[2]} ${NLW[1]}" -source "$ANAT_SS" -master "$MASTER" \
  -interp wsinc5 -prefix "$WORK/anat_mni.nii.gz" >> "$LOGS/sub-$SUB.nwarp.log" 2>&1

AFNI_RUNS="[]"
while IFS=$'\t' read -r -u 3 bold fwd rev; do
  stem=$(basename "$bold" _bold.nii.gz)
  side="${bold%.nii.gz}.json"
  rd="$WORK/$stem"; mkdir -p "$rd"
  tr=$("$VENV/bin/python" -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["RepetitionTime"])' "$side")
  skip=$(pyrun conn01.afni_prep nss --bold "$bold" | tail -1)
  pyrun conn01.afni_prep slice-times --bold-json "$side" --out "$rd/slice_times.1D"
  blip=()
  if [ "$fwd" != none ]; then blip=(-blip_forward_dset "$fwd" -blip_reverse_dset "$rev"); fi
  log "afni_proc $stem (blip: ${fwd##*/} / ${rev##*/}, non-steady-state: $skip)"
  (cd "$rd" && afni_proc.py -subj_id "$stem" -script proc.tcsh -out_dir results \
     -dsets "$bold" -copy_anat "$ANAT_SS" -anat_has_skull no \
     -blocks tshift align tlrc volreg mask \
     -tshift_opts_ts -tpattern "@$rd/slice_times.1D" \
     ${blip[@]+"${blip[@]}"} \
     -tlrc_base "$BASE" -tlrc_NL_warp -tlrc_NL_warped_dsets "${NLW[@]}" \
     -align_unifize_epi local -align_opts_aea -cost lpc+ZZ -giant_move -check_flip \
     -volreg_align_to MIN_OUTLIER -volreg_align_e2a -volreg_tlrc_warp \
     -volreg_warp_master "$MASTER" -volreg_compute_tsnr yes \
     -mask_epi_anat yes -html_review_style none \
     > "$LOGS/$stem.afni_proc.log" 2>&1 \
   && tcsh -xef proc.tcsh > "$LOGS/$stem.proc.log" 2>&1)
  res="$rd/results"
  vr=$(ls "$res"/pb0*."$stem".r01.volreg+tlrc.HEAD | tail -1)
  preproc="$DERIV/sub-$SUB/func/${stem}_${SPACE}_desc-preproc_bold.nii.gz"
  3dAFNItoNIFTI -overwrite -prefix "$preproc" "$vr" > /dev/null 2>&1
  3dAFNItoNIFTI -overwrite -prefix "$rd/mask.nii.gz" "$res/full_mask.$stem+tlrc.HEAD" > /dev/null 2>&1
  3dTstat -overwrite -mean -prefix "$rd/epi_mean.nii.gz" "$preproc" > /dev/null 2>&1
  counts=$(pyrun conn01.afni_prep confounds --bold "$preproc" --mask "$rd/mask.nii.gz" \
    --pv-dir "$WORK/pv_mni" --dfile "$res/dfile_rall.1D" --tr "$tr" --skip "$skip" \
    --out-tsv "$DERIV/sub-$SUB/func/${stem}_desc-confounds_timeseries.tsv" | tail -1)
  tsnr=$(pyrun conn01.afni_qc tsnr --bold "$preproc" --mask "$rd/mask.nii.gz" --tr "$tr" --skip "$skip" | tail -1)
  AFNI_RUNS=$("$VENV/bin/python" -I -c 'import json,sys
r = json.loads(sys.argv[1]); r.append({"run": sys.argv[2], "blip_forward": sys.argv[3],
  "blip_reverse": sys.argv[4], "repetition_time": float(sys.argv[5]), "n_non_steady_state": int(sys.argv[6]),
  "acompcor_mask_voxels": json.loads(sys.argv[7])["mask_voxels"], "tsnr": json.loads(sys.argv[8])})
print(json.dumps(r))' "$AFNI_RUNS" "$stem" "${fwd##*/}" "${rev##*/}" "$tr" "$skip" "$counts" "$tsnr")
done 3< "$WORK/runs.tsv"

AFNI_VER=$(afni -ver | sed -E 's/.*\(Version ([^)]*)\).*/\1/')
AP_VER=$(afni_proc.py -ver | head -1)
"$VENV/bin/python" -I -c 'import json,sys
json.dump({"Name": "AFNI fallback (prereg 01 deviation 4)", "BIDSVersion": "1.9.0", "DatasetType": "derivative",
  "GeneratedBy": [{"Name": "AFNI", "Version": sys.argv[2], "Description": "afni_proc.py " + sys.argv[3]}]},
  open(sys.argv[1], "w"), indent=2)' "$DERIV/dataset_description.json" "$AFNI_VER" "$AP_VER"

log "extract"
pyrun conn01.extract --fmriprep-dir "$DERIV" --bids-dir "$BIDS" --participant "$SUB" \
  --out "$OUT" --sdc-receipt "$SDC_RECEIPT" > "$LOGS/sub-$SUB.extract.log" 2>&1

log "qc"
first=$(head -1 "$WORK/runs.tsv" | cut -f1); first=$(basename "$first" _bold.nii.gz)
pyrun conn01.afni_qc overlay --template "$MASTER" --t1w "$WORK/anat_mni.nii.gz" \
  --epi "$WORK/$first/epi_mean.nii.gz" --out "$OUT/sub-$SUB/sub-${SUB}_desc-afnireg.png" \
  >> "$LOGS/sub-$SUB.extract.log" 2>&1
"$VENV/bin/python" -I -c 'import json,sys
sdc = json.load(open(sys.argv[3]))
json.dump({"participant": "sub-" + sys.argv[2], "afni_version": sys.argv[4], "afni_proc_version": sys.argv[5],
  "afni_sdc": sdc.get("afni_sdc"), "runs": json.loads(sys.argv[6])}, open(sys.argv[1], "w"), indent=2)' \
  "$OUT/sub-$SUB/sub-${SUB}_desc-afni_qc.json" "$SUB" "$SDC_RECEIPT" "$AFNI_VER" "$AP_VER" "$AFNI_RUNS"

log "cleanup"
cp "$LOGS/sub-$SUB.fetch.log" "$OUT/sub-$SUB/"
if [ "${KEEP_WORK:-0}" = "1" ]; then
  log "KEEP_WORK=1: leaving $WORK and $DERIV/sub-$SUB"
  rm -rf "$BIDS"
else
  rm -rf "$BIDS" "$WORK" "$DERIV/sub-$SUB"
fi
touch "$OUT/sub-$SUB/DONE"
log "done"
