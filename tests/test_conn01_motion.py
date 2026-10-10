"""Respiration-filtered FD (prereg 01 deviation 5) on synthetic motion traces."""
import json

import numpy as np
import pandas as pd
import pytest

from conn01 import denoise as dn
from conn01 import extract, motion

TR = 0.8
T = 488  # volumes per run in ds005237
EDGE = 10  # filtfilt edge transient: a few volumes at each run end may exceed 0.2


def _trace(t=T, tr=TR, resp_hz=0.35, resp_mm=0.4, drift_mm=0.5, jerk_at=None,
           jerk_mm=1.5, seed=0):
    """Six motion parameters: breathing on trans_y, slow drift on trans_z."""
    rng = np.random.default_rng(seed)
    time = np.arange(t) * tr
    m = np.zeros((t, 6))
    m[:, 1] = resp_mm * np.sin(2 * np.pi * resp_hz * time)
    m[:, 2] = drift_mm * time / time[-1]
    m += rng.normal(0, 1e-6, m.shape)
    if jerk_at is not None:
        m[jerk_at:, 0] += jerk_mm
    return m


def _confounds(m):
    df = pd.DataFrame(m, columns=motion.MOTION_6)
    df["framewise_displacement"] = motion.power_fd(m)  # what fMRIPrep reports
    df.loc[0, "framewise_displacement"] = np.nan
    return df


def test_power_fd_uses_50_mm_radius_for_rotations():
    m = np.zeros((3, 6))
    m[1, 0] = 0.1  # 0.1 mm translation
    m[2, 3] = 0.002  # 0.002 rad -> 0.1 mm
    assert motion.power_fd(m).tolist() == pytest.approx([0.0, 0.1, 0.2])


def test_pure_respiration_gives_near_zero_filtered_fd_and_large_raw_fd():
    m = _trace()
    raw = motion.power_fd(m)
    filt = motion.power_fd(motion.bandstop(m, TR))
    assert raw[1:].mean() > 0.35  # fails the original 0.3 mm mean rule
    assert np.mean(raw > dn.FD_CENSOR_MM) > 0.2  # and the 20% censoring rule
    assert filt[1:].mean() < 0.02  # drift step is 0.5 mm / 487 volumes, about 0.001
    inner = filt[EDGE:-EDGE]
    assert inner.mean() < 0.005 and inner.max() < 0.1  # ringing decays inward
    cens = np.flatnonzero(filt > dn.FD_CENSOR_FILTERED_MM)
    assert len(cens) <= 6 and all(i < EDGE or i >= T - EDGE for i in cens)


def test_sudden_jerk_is_still_censored_after_filtering():
    jerk = 200
    m = _trace(jerk_at=jerk)
    conf = _confounds(m)
    keep = dn.keep_mask(conf, TR, dn.RULE_FILTERED)
    assert not keep[jerk]  # the step volume is censored
    inner = np.flatnonzero(~keep[EDGE:-EDGE]) + EDGE
    assert all(abs(i - jerk) <= 3 for i in inner)  # only the jerk and its ringing
    q = dn.run_qc(conf, TR)
    assert q.usable and q.n_censored == (~keep).sum() <= 12


def test_filter_respects_tr():
    # 0.35 Hz at TR 0.8 is 0.28 cycles per sample. Read the same samples as
    # TR 0.5 and they are 0.56 Hz, outside the stop band: they must survive.
    m = _trace(drift_mm=0.0)
    right = motion.power_fd(motion.bandstop(m, 0.8))
    wrong = motion.power_fd(motion.bandstop(m, 0.5))
    assert right[EDGE:-EDGE].mean() < 0.005 and wrong[EDGE:-EDGE].mean() > 0.3
    # A true 0.35 Hz breath sampled at TR 0.5 is removed when TR 0.5 is given.
    m05 = _trace(tr=0.5, drift_mm=0.0)
    assert motion.power_fd(motion.bandstop(m05, 0.5))[EDGE:-EDGE].mean() < 0.005
    # A TR whose Nyquist frequency is below the band cannot use the rule.
    with pytest.raises(ValueError):
        motion.bandstop(m, 1.5)
    with pytest.raises(ValueError):
        dn.fd_series(_confounds(m), None, dn.RULE_FILTERED)


def test_qc_records_both_rules_and_breathing_only_run_is_usable_only_filtered():
    rec = dn.run_qc_both(_confounds(_trace()), TR)
    assert rec["usable"] and rec["usable_filtered"] and not rec["usable_unfiltered"]
    assert rec["mean_fd_filtered"] < 0.02 and rec["mean_fd_unfiltered"] > 0.35
    assert rec["n_censored_filtered"] <= 6 and rec["n_censored_unfiltered"] > 0.2 * T
    assert rec["tr_s"] == TR and rec["fd_filter"]["band_hz"] == [0.31, 0.43]
    assert rec["fd_rule"] == "filtered"


def test_repetition_time_prefers_sidecar_then_confounds_json():
    assert motion.repetition_time({"RepetitionTime": 0.7}, {"RepetitionTime": 0.8}) == 0.8
    assert motion.repetition_time({"RepetitionTime": 0.7}, {}) == 0.7
    with pytest.raises(KeyError):
        motion.repetition_time({}, {"InstitutionName": "x"})


def test_regressors_stay_unfiltered():
    conf = _confounds(_trace())
    for c in [c for c in dn.MOTION_24 if c not in conf]:
        conf[c] = 0.0
    x = dn.design_matrix(conf, {})
    assert np.array_equal(x[:, 1 + dn.MOTION_24.index("trans_y")], conf["trans_y"])


def test_requalify_recomputes_motion_qc_without_reading_time_series(tmp_path):
    label = "SYNRQ"
    out = tmp_path / "conn01" / f"sub-{label}"
    out.mkdir(parents=True)
    runs = []
    for k, m in enumerate((_trace(seed=1), _trace(seed=2), _trace(seed=3, resp_mm=0.0,
                                                                    jerk_at=100)), 1):
        stem = f"sub-{label}_task-restAP_run-{k:02d}"
        conf = _confounds(m)
        conf.to_csv(out / f"{stem}_desc-confounds_timeseries.tsv", sep="\t", index=False)
        (out / f"{stem}_desc-confounds_timeseries.json").write_text("{}")
        runs.append({"run": stem, "n_volumes": T, "usable": False,
                     "scanner": {"RepetitionTime": TR, "InstitutionName": "S"}})
    # No *_timeseries.tsv exists: requalify must not need them.
    (out / f"sub-{label}_qc.json").write_text(json.dumps(
        {"fmriprep_generated_by": [{"Name": "fMRIPrep"}], "sdc": {"sdc_path": "syn"},
         "runs": runs}))
    assert extract.main(["--requalify", "--participant", label,
                         "--out", str(tmp_path / "conn01")]) == 0
    qc = json.loads((out / f"sub-{label}_qc.json").read_text())
    assert qc["n_usable_runs"] == 3 and qc["meets_min_usable_runs"]
    assert qc["n_usable_runs_unfiltered"] == 1  # only the run without breathing
    assert not qc["meets_min_usable_runs_unfiltered"]
    assert qc["sdc"] == {"sdc_path": "syn"}
    r0 = qc["runs"][0]
    assert r0["tr_s"] == TR and r0["scanner"]["InstitutionName"] == "S"
    assert "unavailable" in r0["roi_signal"]
