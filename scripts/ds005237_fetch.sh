#!/usr/bin/env bash
# Fetch the files that prereg 01 needs for ONE participant of OpenNeuro
# ds005237 (snapshot 1.1.3) from the public S3 bucket, no credentials.
#
#   ds005237_fetch.sh --list                write participant list from S3 prefixes
#   ds005237_fetch.sh SUBLABEL              T1w, rest BOLD + sidecars, field maps
#   ds005237_fetch.sh SUBLABEL --t1w-only   access check: T1w only
#
# Top-level files fetched: dataset_description.json, participants.tsv (the
# list, not opened here), README, CHANGES, .bidsignore and any top-level
# task-rest sidecars. Never fetched: phenotype/ (CTQ, demographics), the
# derived folders, T2w, task runs. Files already present at full size are
# skipped, so the script is resumable. Prints bytes fetched.
set -euo pipefail

ROOT=${DS_ROOT:-/mnt/h/bio-data/ds005237}
BIDS=${BIDS_DIR:-$ROOT/bids}
BUCKET="https://s3.amazonaws.com/openneuro.org"
DS=ds005237
mkdir -p "$BIDS"

# list_keys PREFIX [DELIM]: prints "size key" lines, follows pagination.
list_keys() {
  local prefix=$1 delim=${2:-} token="" url xml
  while :; do
    url="$BUCKET?list-type=2&prefix=$prefix"
    [ -n "$delim" ] && url="$url&delimiter=$delim"
    [ -n "$token" ] && url="$url&continuation-token=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$token")"
    xml=$(curl -sS --fail --retry 5 "$url")
    grep -o "<Key>[^<]*</Key><LastModified>[^<]*</LastModified><ETag>[^<]*</ETag><Size>[0-9]*</Size>" <<<"$xml" \
      | sed -E 's#<Key>([^<]*)</Key>.*<Size>([0-9]*)</Size>#\2 \1#' || true
    token=$(grep -o "<NextContinuationToken>[^<]*</NextContinuationToken>" <<<"$xml" | sed -E 's#</?NextContinuationToken>##g' || true)
    [ -z "$token" ] && break
  done
}

FETCHED=0
fetch_key() {  # fetch_key SIZE KEY
  local size=$1 key=$2 dest="$BIDS/${2#$DS/}"
  case "$key" in "$DS/phenotype/"*) echo "refusing phenotype key: $key" >&2; exit 3;; esac
  if [ -f "$dest" ] && [ "$(stat -c %s "$dest")" = "$size" ]; then return 0; fi
  mkdir -p "$(dirname "$dest")"
  curl -sS --fail --retry 5 --retry-delay 3 -o "$dest.part" "$BUCKET/$key"
  [ "$(stat -c %s "$dest.part")" = "$size" ] || { echo "size mismatch: $key" >&2; exit 4; }
  mv "$dest.part" "$dest"
  FETCHED=$((FETCHED + size))
}

if [ "${1:-}" = "--list" ]; then
  curl -sS --fail "$BUCKET?list-type=2&prefix=$DS/sub-&delimiter=/&max-keys=1000" \
    | grep -o "<Prefix>$DS/sub-[^<]*/</Prefix>" | sed -E "s#<Prefix>$DS/sub-([^/]*)/</Prefix>#\1#" \
    > "$ROOT/participants_list.txt"
  echo "participants: $(wc -l < "$ROOT/participants_list.txt") -> $ROOT/participants_list.txt"
  exit 0
fi

SUB=${1:?usage: ds005237_fetch.sh SUBLABEL [--t1w-only] | --list}
SUB=${SUB#sub-}
MODE=${2:-full}

# Top-level metadata (no phenotype; participants.tsv is downloaded, not read).
while read -r size key; do
  case "$key" in
    "$DS/dataset_description.json"|"$DS/participants.tsv"|"$DS/README"|"$DS/CHANGES"|"$DS/.bidsignore") fetch_key "$size" "$key";;
    "$DS/task-rest"*.json) fetch_key "$size" "$key";;
  esac
done < <(list_keys "$DS/" "/")

while read -r size key; do
  f=${key##*/}
  case "$MODE:$key" in
    *:*/anat/*_T1w.nii.gz|*:*/anat/*_T1w.json) fetch_key "$size" "$key";;
    --t1w-only:*) ;;
    *:*/func/*task-rest*_bold.nii.gz|*:*/func/*task-rest*_bold.json) fetch_key "$size" "$key";;
    *:*/fmap/*) fetch_key "$size" "$key";;
  esac
done < <(list_keys "$DS/sub-$SUB/")

# Verify.
SD="$BIDS/sub-$SUB"
n_t1=$(find "$SD/anat" -name "*_T1w.nii.gz" 2>/dev/null | wc -l)
[ "$n_t1" -ge 1 ] || { echo "FAIL: no T1w for sub-$SUB" >&2; exit 5; }
if [ "$MODE" != "--t1w-only" ]; then
  n_rest=$(find "$SD/func" -name "*task-rest*_bold.nii.gz" 2>/dev/null | wc -l)
  n_json=$(find "$SD/func" -name "*task-rest*_bold.json" 2>/dev/null | wc -l)
  [ "$n_rest" -ge 1 ] && [ "$n_rest" = "$n_json" ] \
    || { echo "FAIL: sub-$SUB rest runs=$n_rest sidecars=$n_json" >&2; exit 6; }
  echo "sub-$SUB: T1w=$n_t1 rest_runs=$n_rest"
fi
echo "sub-$SUB: bytes_fetched=$FETCHED on_disk=$(du -sb "$SD" | cut -f1)"
