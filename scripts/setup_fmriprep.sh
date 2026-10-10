#!/usr/bin/env bash
# Install Apptainer (official PPA) and build the pinned fMRIPrep image on H:.
# Bulk data and images live on /mnt/h/bio-data; C: has no room (2026-10-09).
set -eu
VERSION=25.2.6
DATA=/mnt/h/bio-data
mkdir -p "$DATA/containers" "$DATA/apptainer-tmp" "$DATA/apptainer-cache"
export DEBIAN_FRONTEND=noninteractive
if ! command -v apptainer >/dev/null; then
  apt-get update -qq
  apt-get install -y -qq software-properties-common >/dev/null
  add-apt-repository -y ppa:apptainer/ppa >/dev/null
  apt-get update -qq
  apt-get install -y -qq apptainer >/dev/null
fi
apptainer --version
# Scratch on the native ext4 disk (E:-backed vhdx): unpacking tens of thousands
# of small files over the /mnt/h 9p mount took 3+ hours without finishing.
export APPTAINER_TMPDIR=/root/apptainer-tmp APPTAINER_CACHEDIR=/root/apptainer-cache
mkdir -p "$APPTAINER_TMPDIR" "$APPTAINER_CACHEDIR"
SIF="$DATA/containers/fmriprep-$VERSION.sif"
[ -f "$SIF" ] || apptainer build "$SIF" "docker://nipreps/fmriprep:$VERSION"
ls -la "$SIF"
sha256sum "$SIF" | tee "$DATA/containers/fmriprep-$VERSION.sif.sha256"
apptainer exec "$SIF" fmriprep --version
