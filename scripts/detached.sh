#!/usr/bin/env bash
# Run a command as a systemd transient unit inside WSL and stay attached until
# it finishes. Detached so a Claude Code restart does not kill it; attached
# because WSL stops the distro (and every unit) a few seconds after the last
# wsl.exe client exits.
#   detached.sh NAME COMMAND [ARGS...]  -> /mnt/h/bio-data/jobs/NAME.{log,done}
set -eu
JOBS=/mnt/h/bio-data/jobs
mkdir -p "$JOBS"
name="$1"; shift
log="$JOBS/$name.log"; done_f="$JOBS/$name.done"
rm -f "$done_f"
systemd-run --quiet --unit="bio-$name" --collect --setenv=HOME="$HOME" \
  --setenv=KEEP_REPORT="${KEEP_REPORT:-0}" \
  bash -c 'log=$0; done_f=$1; shift; "$@" > "$log" 2>&1; echo "exit=$?" > "$done_f"' \
  "$log" "$done_f" "$@"
echo "launched bio-$name"
until [ -f "$done_f" ]; do sleep 30; done
echo "$name $(cat "$done_f")"
tail -5 "$log"
