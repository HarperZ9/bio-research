"""Censoring and run-exclusion rules for prereg 01 (deviations 5 and 5a).

Primary rule "lowpass" (deviation 5a, after Gratton et al. 2020): FD from
motion parameters low-pass filtered at 0.1 Hz; frames with FD > 0.1 mm are
censored, and so is every uncensored segment shorter than 5 frames.
Sensitivity rules, each selectable and recorded per run:
  "unfiltered"     the original rule: fMRIPrep's framewise_displacement
                   column, FD > 0.5 mm, no segment rule
  "bandstop"       deviation 5: 0.31 to 0.43 Hz band-stop FD, FD > 0.2 mm,
                   no segment rule
  "lowpass_strict" the stricter Gratton threshold: low-pass FD > 0.08 mm,
                   with the 5-frame segment rule
Under every rule a run is unusable if more than 20% of its frames are
censored or its mean FD (the rule's FD, frames after the first) > 0.3 mm, and
a participant needs >= 2 usable runs. The mean-FD covariate is the mean of
the rule's FD over usable runs (deviation 5a: filtered FD for the primary).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from . import motion

RULE_LOWPASS = "lowpass"
RULE_UNFILTERED = "unfiltered"
RULE_BANDSTOP = "bandstop"
RULE_LOWPASS_STRICT = "lowpass_strict"
PRIMARY_RULE = RULE_LOWPASS
RULES = (RULE_LOWPASS, RULE_UNFILTERED, RULE_BANDSTOP, RULE_LOWPASS_STRICT)
FD_CENSOR_MM = 0.5  # original (unfiltered) rule
CENSOR_MM = {RULE_LOWPASS: 0.1, RULE_UNFILTERED: FD_CENSOR_MM, RULE_BANDSTOP: 0.2,
             RULE_LOWPASS_STRICT: 0.08}
MIN_SEGMENT = {RULE_LOWPASS: 5, RULE_UNFILTERED: 0, RULE_BANDSTOP: 0,
               RULE_LOWPASS_STRICT: 5}
FILTERS = {RULE_LOWPASS: motion.LOWPASS_DESC, RULE_UNFILTERED: None,
           RULE_BANDSTOP: motion.BANDSTOP_DESC, RULE_LOWPASS_STRICT: motion.LOWPASS_DESC}
MAX_CENSORED_FRACTION = 0.20
MAX_RUN_MEAN_FD_MM = 0.3
MIN_USABLE_RUNS = 2


@dataclass
class RunQC:
    n_volumes: int
    n_censored: int
    mean_fd: float
    censored_fraction: float
    usable: bool
    reason: str


def check_rule(rule: str) -> None:
    if rule not in RULES:
        raise ValueError(f"unknown FD rule {rule!r}; use one of {RULES}")


def fd_series(confounds: pd.DataFrame, tr: float | None = None,
              rule: str = PRIMARY_RULE) -> np.ndarray:
    """FD per frame under a rule; the undefined first value is 0.

    Filtered rules need the run's TR; "unfiltered" is fMRIPrep's column.
    """
    check_rule(rule)
    if rule == RULE_UNFILTERED:
        return confounds["framewise_displacement"].fillna(0.0).to_numpy(float)
    if tr is None:
        raise ValueError(f"FD rule {rule!r} needs the run's repetition time")
    if rule == RULE_BANDSTOP:
        return motion.bandstop_fd(confounds, tr)
    return motion.lowpass_fd(confounds, tr)


def censor_mask(fd: np.ndarray, threshold: float = FD_CENSOR_MM) -> np.ndarray:
    """True for frames kept; FD strictly above the threshold is censored."""
    return ~(np.asarray(fd) > threshold)


def drop_short_segments(keep: np.ndarray, min_len: int) -> np.ndarray:
    """Censor every run of kept frames shorter than min_len frames."""
    keep = np.asarray(keep, bool).copy()
    if min_len <= 1:
        return keep
    edges = np.diff(np.concatenate([[0], keep.astype(int), [0]]))
    for start, stop in zip(np.flatnonzero(edges == 1), np.flatnonzero(edges == -1)):
        if stop - start < min_len:
            keep[start:stop] = False
    return keep


def keep_mask(confounds: pd.DataFrame, tr: float | None = None,
              rule: str = PRIMARY_RULE) -> np.ndarray:
    """Frames kept under a rule: threshold, then the segment rule."""
    keep = censor_mask(fd_series(confounds, tr, rule), CENSOR_MM[rule])
    return drop_short_segments(keep, MIN_SEGMENT[rule])


def mean_fd(confounds: pd.DataFrame, tr: float | None = None,
            rule: str = PRIMARY_RULE) -> float:
    """Mean FD over defined frames (the first frame has no FD)."""
    if rule == RULE_UNFILTERED:
        raw = confounds["framewise_displacement"].to_numpy(float)
        return float(np.nanmean(raw)) if np.isfinite(raw).any() else float("nan")
    fd = fd_series(confounds, tr, rule)
    return float(np.mean(fd[1:])) if len(fd) > 1 else float("nan")


def run_qc(confounds: pd.DataFrame, tr: float | None = None,
           rule: str = PRIMARY_RULE) -> RunQC:
    """Apply the run exclusion rules to one run under the chosen FD rule."""
    keep = keep_mask(confounds, tr, rule)
    n = len(keep)
    n_cens = int((~keep).sum())
    frac = n_cens / n if n else 1.0
    mfd = mean_fd(confounds, tr, rule)
    reasons = []
    if frac > MAX_CENSORED_FRACTION:
        reasons.append("censored_fraction>0.20")
    if not mfd <= MAX_RUN_MEAN_FD_MM:
        reasons.append("mean_fd>0.3")
    return RunQC(n, n_cens, mfd, frac, not reasons, ";".join(reasons))


def run_qc_all(confounds: pd.DataFrame, tr: float) -> dict:
    """QC record: primary-rule fields at top level, every rule under fd_rules."""
    per_rule = {}
    for rule in RULES:
        q = vars(run_qc(confounds, tr, rule))
        q.update(censor_threshold_mm=CENSOR_MM[rule], min_segment_frames=MIN_SEGMENT[rule],
                 filter=FILTERS[rule])
        per_rule[rule] = q
    top = {k: per_rule[PRIMARY_RULE][k] for k in vars(RunQC(0, 0, 0.0, 0.0, True, ""))}
    return {**top, "fd_rule": PRIMARY_RULE, "tr_s": float(tr), "fd_rules": per_rule}
