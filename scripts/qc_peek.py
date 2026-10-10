"""Print QC fields for one participant, never connectivity or time-series values.

Usage: python scripts/qc_peek.py /mnt/h/bio-data/ds005237/conn01/sub-<label>
"""
import json
import sys
from pathlib import Path

BLOCK = ("conn", "corr", "fisher", "timeseries", "_ts", "roi_mean", "ctq")

d = Path(sys.argv[1])
for p in sorted(d.iterdir()):
    print(f"{p.name}  {p.stat().st_size} bytes")
for qc in sorted(d.glob("*qc*.json")):
    print(f"--- {qc.name}")
    data = json.loads(qc.read_text())

    def show(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if any(b in k.lower() for b in BLOCK):
                    print(f"{prefix}{k} = <withheld>")
                else:
                    show(v, f"{prefix}{k}.")
        else:
            print(f"{prefix.rstrip('.')} = {obj}")

    show(data)
