#!/usr/bin/env bash
# Project 02 Tier B: SynthSeg 2.0 robust on ds002674 T1w, skipping sessions whose
# seg, vol and qc outputs all exist. Run inside WSL. Launch detached with
#   systemd-run --unit=gm02-synthseg --collect bash scripts/gm02_synthseg_batch.sh
# Log: $D/batch.log; marker: $D/batch.done ("exit=N").
set -u
D=/mnt/h/bio-data/ds002674-derivatives/synthseg
SRC=/mnt/h/bio-data/ds002674/sub-01
mkdir -p "$D/seg" "$D/vol" "$D/qc" "$D/todo"
rm -f "$D/batch.done" "$D/todo/"*.txt
for i in $(seq -w 1 60); do
  seg=$D/seg/sub-01_ses-${i}_synthseg.nii.gz
  if [ -s "$seg" ] && [ -s "$D/vol/ses-${i}_vol.csv" ] && [ -s "$D/qc/ses-${i}_qc.csv" ]; then
    continue
  fi
  echo "$SRC/ses-$i/anat/sub-01_ses-${i}_T1w.nii.gz" >> "$D/todo/in.txt"
  echo "$seg" >> "$D/todo/out.txt"
  echo "$D/vol/ses-${i}_vol.csv" >> "$D/todo/vol.txt"
  echo "$D/qc/ses-${i}_qc.csv" >> "$D/todo/qc.txt"
done
if [ ! -s "$D/todo/in.txt" ]; then
  echo "nothing to do" > "$D/batch.log"; echo "exit=0" > "$D/batch.done"; exit 0
fi
echo "sessions to run: $(wc -l < "$D/todo/in.txt")" > "$D/batch.log"
cd /mnt/h/bio-data/synthseg/SynthSeg
source /mnt/h/bio-data/venvs/synthseg/bin/activate
python scripts/commands/SynthSeg_predict.py --i "$D/todo/in.txt" --o "$D/todo/out.txt" \
  --robust --vol "$D/todo/vol.txt" --qc "$D/todo/qc.txt" --threads 24 >> "$D/batch.log" 2>&1
rc=$?
echo "exit=$rc" > "$D/batch.done"
exit $rc
