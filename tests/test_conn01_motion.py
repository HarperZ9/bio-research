"""Filtered FD rules (prereg 01 deviations 5 and 5a) on synthetic motion traces."""
import json

import numpy as np
import pandas as pd
import pytest
from scipy.signal import butter, filtfilt

import conn01_synth as syn
from conn01 import denoise as dn
from conn01 import extract, motion
from conn01 import participant as pt

TR = 0.8
T = 488  # volumes per run in ds005237
EDGE = 10


def _trace(t=T, tr=TR, resp_hz=0.35, resp_mm=0.4, drift_mm=0.5, jerk_at=None,
           jerk_mm=1.5, phase=0.0, seed=0):
    """Six motion parameters: breathing on trans_y, slow drift on trans_z."""
    rng = np.random.default_rng(seed)
    time = np.arange(t) * tr
    m = np.zeros((t, 6))
    m[:, 1] = 0.8 + resp_mm * np.sin(2 * np.pi * resp_hz * time + phase)
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


# Primary rule: 0.1 Hz low-pass (deviation 5a)

@pytest.mark.parametrize("hz", [0.35, 0.2])
def test_planted_respiration_vanishes_under_the_lowpass(hz):
    m = _trace(resp_hz=hz)
    raw = motion.power_fd(m)
    low = motion.lowpass_fd(_confounds(m), TR)
    assert raw[1:].mean() > 0.2  # raw FD sees large motion
    assert not (low > dn.CENSOR_MM[dn.RULE_LOWPASS]).any()  # nothing censored
    assert low[1:].mean() < 0.25 * raw[1:].mean()
    q = dn.run_qc(_confounds(m), TR)
    assert q.usable and q.n_censored == 0
    if hz == 0.35:  # the first participant's case: the original rule fails it
        assert not dn.run_qc(_confounds(m), TR, dn.RULE_UNFILTERED).usable


def test_step_jerk_is_still_censored_under_the_lowpass():
    jerk = 200
    conf = _confounds(_trace(jerk_at=jerk))
    keep = dn.keep_mask(conf, TR)
    cens = np.flatnonzero(~keep)
    assert not keep[jerk] and len(cens) >= 5
    assert all(abs(i - jerk) <= 10 for i in cens)
    assert dn.run_qc(conf, TR).usable


def test_segments_shorter_than_5_frames_are_censored():
    keep = np.array([0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1], bool)
    out = dn.drop_short_segments(keep, 5)
    assert out.tolist() == [False] * 6 + [True] * 5 + [False, False]
    # Through the rule: two spikes 4 frames apart also censor the 3 between.
    m = _trace(resp_mm=0.0, drift_mm=0.0)
    m[100:, 0] += 1.0
    m[104:, 0] += 1.0
    conf = _confounds(m)
    fd = dn.fd_series(conf, TR)
    thresh_only = dn.censor_mask(fd, dn.CENSOR_MM[dn.RULE_LOWPASS])
    keep = dn.keep_mask(conf, TR)
    assert (~keep).sum() >= (~thresh_only).sum()
    assert not keep[thresh_only.argmin():len(keep) - thresh_only[::-1].argmin()].any()
    segs = np.diff(np.concatenate([[0], keep.astype(int), [0]]))
    lengths = np.flatnonzero(segs == -1) - np.flatnonzero(segs == 1)
    assert lengths.min() >= 5
    # The original and band-stop rules have no segment rule.
    assert dn.MIN_SEGMENT[dn.RULE_UNFILTERED] == dn.MIN_SEGMENT[dn.RULE_BANDSTOP] == 0


@pytest.mark.parametrize("phase", [0.0, 0.7, 1.9])
def test_mirrored_padding_removes_the_end_of_run_artifact(phase):
    m = _trace(drift_mm=0.0, phase=phase)
    low = motion.power_fd(motion.lowpass(m, TR))
    inner = low[EDGE:-EDGE].max()
    assert max(low[1:EDGE].max(), low[-EDGE:].max()) <= inner + 0.02
    assert low.max() < dn.CENSOR_MM[dn.RULE_LOWPASS_STRICT]
    # The same filter with scipy's default odd padding has the artifact.
    b, a = butter(1, 0.1 / (0.5 / TR), btype="low")
    odd = motion.power_fd(filtfilt(b, a, m, axis=0))
    if phase == 1.9:
        assert max(odd[1:EDGE].max(), odd[-EDGE:].max()) > dn.CENSOR_MM[dn.RULE_LOWPASS]


def test_lowpass_respects_tr():
    m = _trace(drift_mm=0.0)
    # Same samples read as TR 4 s are 0.07 Hz, below the cutoff: they survive.
    right = motion.power_fd(motion.lowpass(m, 0.8))[1:].mean()
    wrong = motion.power_fd(motion.lowpass(m, 4.0))[1:].mean()
    assert right < 0.05 and wrong > 4 * right
    with pytest.raises(ValueError):
        motion.lowpass(m, 6.0)  # Nyquist 0.083 Hz is below the 0.1 Hz cutoff
    with pytest.raises(ValueError):
        dn.fd_series(_confounds(m), None, dn.RULE_LOWPASS)


def test_mean_fd_covariate_is_lowpass_fd_over_usable_runs():
    rng = np.random.default_rng(3)
    runs = []
    for _ in range(2):
        conf, meta = syn.confounds(300, rng)
        runs.append((syn.regions(conf, rng, 0.3), conf, meta))
    s = pt.summarize_runs(runs)
    fds = np.concatenate([dn.fd_series(c, m["RepetitionTime"])[1:] for _, c, m in runs])
    assert s["mean_fd"] == pytest.approx(fds.mean())
    col = np.concatenate([c["framewise_displacement"].to_numpy() for _, c, _ in runs])
    assert s["mean_fd"] != pytest.approx(np.nanmean(col))


# Sensitivity rule: band-stop (deviation 5)

def test_bandstop_removes_035_hz_and_keeps_a_jerk():
    jerk = 200
    m = _trace(jerk_at=jerk)
    filt = motion.bandstop_fd(_confounds(_trace()), TR)
    assert filt[EDGE:-EDGE].mean() < 0.005
    keep = dn.keep_mask(_confounds(m), TR, dn.RULE_BANDSTOP)
    assert not keep[jerk]
    assert all(abs(i - jerk) <= 3 for i in np.flatnonzero(~keep[EDGE:-EDGE]) + EDGE)
    with pytest.raises(ValueError):
        motion.bandstop(m, 1.5)  # band above Nyquist


def test_qc_records_every_rule():
    rec = dn.run_qc_all(_confounds(_trace()), TR)
    rules = rec["fd_rules"]
    assert set(rules) == {"lowpass", "unfiltered", "bandstop", "lowpass_strict"}
    assert rec["fd_rule"] == "lowpass" and rec["usable"] == rules["lowpass"]["usable"]
    assert rules["lowpass"]["usable"] and not rules["unfiltered"]["usable"]
    assert rules["unfiltered"]["mean_fd"] > 0.35 > 0.05 > rules["lowpass"]["mean_fd"]
    assert [rules[r]["censor_threshold_mm"] for r in dn.RULES] == [0.1, 0.5, 0.2, 0.08]
    assert rules["lowpass"]["filter"]["cutoff_hz"] == 0.1
    assert rules["bandstop"]["filter"]["band_hz"] == [0.31, 0.43]
    assert rec["tr_s"] == TR


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
    traces = (_trace(seed=1), _trace(seed=2), _trace(seed=3, resp_mm=0.0, jerk_at=100))
    for k, m in enumerate(traces, 1):
        stem = f"sub-{label}_task-restAP_run-{k:02d}"
        _confounds(m).to_csv(out / f"{stem}_desc-confounds_timeseries.tsv", sep="\t",
                             index=False)
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
    assert qc["fd_rule"] == "lowpass" and qc["n_usable_runs"] == 3
    assert qc["n_usable_runs_by_rule"]["unfiltered"] == 1  # only the run without breathing
    assert not qc["meets_min_usable_runs_by_rule"]["unfiltered"]
    assert qc["sdc"] == {"sdc_path": "syn"}
    r0 = qc["runs"][0]
    assert r0["tr_s"] == TR and r0["scanner"]["InstitutionName"] == "S"
    assert "unavailable" in r0["roi_signal"]
