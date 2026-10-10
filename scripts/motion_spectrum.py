"""Respiratory contamination check on motion parameters (QC data only).

For each confounds file: fraction of motion-parameter power in 0.2-0.5 Hz
(typical adult breathing) versus 0.01-0.1 Hz, the dominant peak frequency of
each translation, and FD (Power) before and after a 0.1 Hz low-pass filter of
the motion parameters (Gratton et al. 2020 approach).
Usage: python scripts/motion_spectrum.py DIR TR
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, welch

MOT = ["trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z"]


def fd(m):
    d = np.abs(np.diff(m, axis=0))
    d[:, 3:] *= 50.0  # radians to mm on a 50 mm sphere
    return np.concatenate([[0.0], d.sum(1)])


def main():
    root, tr = Path(sys.argv[1]), float(sys.argv[2])
    fs = 1.0 / tr
    b, a = butter(2, 0.1 / (fs / 2), btype="low")
    for f in sorted(root.glob("*desc-confounds_timeseries.tsv")):
        m = pd.read_csv(f, sep="\t")[MOT].fillna(0).to_numpy()
        m = m[2:]  # skip non-steady-state volumes
        parts = []
        for i, name in enumerate(MOT[:3]):
            fr, p = welch(m[:, i] - m[:, i].mean(), fs=fs, nperseg=128)
            resp = p[(fr >= 0.2) & (fr <= 0.5)].sum()
            slow = p[(fr >= 0.01) & (fr <= 0.1)].sum()
            parts.append(f"{name}: peak {fr[p.argmax()]:.2f} Hz, resp/slow {resp / slow:.2f}")
        raw = fd(m)
        filt = fd(filtfilt(b, a, m, axis=0))
        print(f.name.split("_desc")[0])
        print("  " + "; ".join(parts))
        print(f"  FD raw mean {raw.mean():.3f}, >0.5 {np.mean(raw > 0.5):.2%} | "
              f"FD low-pass mean {filt.mean():.3f}, >0.5 {np.mean(filt > 0.5):.2%}, "
              f">0.2 {np.mean(filt > 0.2):.2%}")


if __name__ == "__main__":
    main()
