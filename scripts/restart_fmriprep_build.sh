#!/usr/bin/env bash
# Stop the slow 9p-scratch build, clear its scratch and partial image, and
# relaunch setup_fmriprep.sh (now with native ext4 scratch). 2026-10-09.
set -u
pkill -f 'apptainer build' || true
sleep 3
find /mnt/h/bio-data/apptainer-tmp -mindepth 1 -delete 2>/dev/null || true
find /mnt/h/bio-data/containers -name 'fmriprep-25.2.6.sif' -delete 2>/dev/null || true
echo "remaining builds: $(pgrep -fc 'apptainer build' || true)"
echo "free on native disk: $(df -h / | tail -1)"
bash "$(dirname "$0")/setup_fmriprep.sh"
