"""Load SynthSeg volumes, QC scores and participants.tsv into one session table."""
from pathlib import Path

import numpy as np
import pandas as pd

N_SESSIONS = 30 * 2
VOL_COLS = {"total intracranial": "tiv", "left hippocampus": "hipp_l",
            "right hippocampus": "hipp_r", "left amygdala": "amy_l",
            "right amygdala": "amy_r"}


def _read_one(path):
    df = pd.read_csv(path, index_col=0)  # first column is the subject name
    if len(df) != 1:
        raise ValueError(f"expected one row in {path}, found {len(df)}")
    return df.iloc[0]


def load_synthseg(root):
    """One row per session with the five volumes, every QC score and their mean."""
    root = Path(root)
    rows, qc_names = [], None
    for s in range(1, N_SESSIONS + 1):
        vol_path = root / "vol" / f"ses-{s:02d}_vol.csv"
        qc_path = root / "qc" / f"ses-{s:02d}_qc.csv"
        if not (vol_path.exists() and qc_path.exists()):
            rows.append({"session": s, "failed": True})
            continue
        vol, qc = _read_one(vol_path), _read_one(qc_path)
        qc_names = list(qc.index)
        row = {"session": s, "failed": False}
        row.update({short: float(vol[long]) for long, short in VOL_COLS.items()})
        row.update({f"qc_{k}": float(v) for k, v in qc.items()})
        row["qc_mean"] = float(qc.astype(float).mean())
        rows.append(row)
    return pd.DataFrame(rows), qc_names


def load_pss(participants_tsv):
    """Map session number to perceived_stress (NaN where missing)."""
    df = pd.read_csv(participants_tsv, sep="\t", na_values=["n/a", "NA", ""])
    num = df["session_id"].astype(str).str.extract(r"(\d+)")[0].astype(int)
    return pd.Series(pd.to_numeric(df["perceived_stress"], errors="coerce").values,
                     index=num.values, name="pss")


def build_table(synthseg_root, participants_tsv, excluded=()):
    """Session table with study, day, derived volumes and PSS; excluded rows flagged."""
    vols, qc_names = load_synthseg(synthseg_root)
    pss = load_pss(participants_tsv)
    t = vols.set_index("session")
    t["pss"] = pss.reindex(t.index)
    t["study"] = np.where(t.index <= 30, 1, 2)
    t["day"] = t.index - 30 * (t["study"] - 1)
    t["excluded"] = t["failed"] | t.index.isin(list(excluded))
    t["hipp"] = t["hipp_l"] + t["hipp_r"]
    t["amy"] = t["amy_l"] + t["amy_r"]
    t["hipp_ratio"] = t["hipp"] / t["tiv"]
    t["amy_ratio"] = t["amy"] / t["tiv"]
    return t, qc_names


def pct_dev(x, keep):
    """Percent deviation from the mean over kept rows (NaN elsewhere)."""
    x = np.asarray(x, float)
    out = np.full(len(x), np.nan)
    out[keep] = 100.0 * (x[keep] / x[keep].mean() - 1.0)
    return out
