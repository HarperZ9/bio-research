"""Synthetic-data checks for censoring, run exclusion and denoising."""
import numpy as np
import pytest

import conn01_synth as syn
from conn01 import denoise as dn
from conn01 import participant as pt


def test_censor_threshold_is_strictly_greater_than_half_mm():
    keep = dn.censor_mask(np.array([0.0, 0.5, 0.5001, 1.2]))
    assert keep.tolist() == [True, True, False, False]


def _fd_with(n: int, n_high: int, base: float = 0.1) -> np.ndarray:
    fd = np.full(n, base)
    fd[1:1 + n_high] = 0.9
    return fd


def test_run_excluded_when_more_than_20_percent_censored():
    rng = np.random.default_rng(0)
    ok, _ = syn.confounds(100, rng, fd=_fd_with(100, 20, base=0.01))
    bad, _ = syn.confounds(100, rng, fd=_fd_with(100, 21, base=0.01))
    # Planted FD column: the original (unfiltered) rule, kept as sensitivity.
    q_ok, q_bad = dn.run_qc(ok, rule=dn.RULE_UNFILTERED), dn.run_qc(bad, rule=dn.RULE_UNFILTERED)
    assert q_ok.censored_fraction == pytest.approx(0.20) and q_ok.usable
    assert q_bad.n_censored == 21 and not q_bad.usable
    assert "censored_fraction" in q_bad.reason


def test_run_excluded_when_mean_fd_above_0_3():
    rng = np.random.default_rng(1)
    conf, _ = syn.confounds(200, rng, fd=np.full(200, 0.31))
    q = dn.run_qc(conf, rule=dn.RULE_UNFILTERED)
    assert q.n_censored == 0 and not q.usable and q.reason == "mean_fd>0.3"
    conf2, _ = syn.confounds(200, rng, fd=np.full(200, 0.299))
    assert dn.run_qc(conf2, rule=dn.RULE_UNFILTERED).usable


def test_compcor_picks_top_five_per_mask_by_singular_value():
    rng = np.random.default_rng(2)
    _, meta = syn.confounds(50, rng)
    meta["a_comp_cor_03"]["SingularValue"] = 1000.0  # CSF component promoted
    meta["a_comp_cor_08"]["Retained"] = False
    csf = dn.compcor_columns(meta, "CSF")
    wm = dn.compcor_columns(meta, "WM")
    assert csf[0] == "a_comp_cor_03" and len(csf) == 5
    assert "a_comp_cor_08" not in wm and len(wm) == 5
    assert all(meta[c]["Mask"] == "WM" for c in wm)


def test_compcor_reads_fmriprep_25_names_and_skips_combined_mask():
    # fMRIPrep >= 21: c_comp_cor = CSF, w_comp_cor = WM, a_comp_cor = combined.
    meta = {f"c_comp_cor_{j:02d}": {"Mask": "CSF", "SingularValue": 50.0 - j}
            for j in range(6)}
    meta.update({f"w_comp_cor_{j:02d}": {"Mask": "WM", "SingularValue": 40.0 - j}
                 for j in range(3)})
    meta.update({f"a_comp_cor_{j:02d}": {"Mask": "combined", "SingularValue": 99.0}
                 for j in range(4)})
    assert dn.compcor_columns(meta, "CSF") == [f"c_comp_cor_{j:02d}" for j in range(5)]
    assert dn.compcor_columns(meta, "WM") == ["w_comp_cor_00", "w_comp_cor_01",
                                              "w_comp_cor_02"]
    assert dn.compcor_counts(meta) == {"WM": 3, "CSF": 5}


def test_compcor_shortfall_uses_available_components_and_counts_them():
    rng = np.random.default_rng(3)
    conf, meta = syn.confounds(120, rng, n_wm=3)
    assert len(dn.compcor_columns(meta, "WM")) == 3
    assert dn.compcor_counts(meta) == {"WM": 3, "CSF": 5}
    assert dn.design_matrix(conf, meta).shape == (120, 1 + 24 + 3 + 5 + 4)


def test_participant_records_smallest_compcor_count_over_usable_runs():
    rng = np.random.default_rng(10)
    full = _run(rng)
    conf, meta = syn.confounds(500, rng, n_csf=2)
    short = (syn.regions(conf, rng, 0.3), conf, meta)
    s = pt.summarize_runs([full, short])
    assert s["included"] and s["n_compcor_wm_min"] == 5 and s["n_compcor_csf_min"] == 2


def test_design_has_intercept_24_motion_10_compcor_and_cosines():
    rng = np.random.default_rng(4)
    conf, meta = syn.confounds(120, rng)
    assert dn.design_matrix(conf, meta).shape == (120, 1 + 24 + 10 + 4)
    assert dn.design_matrix(conf, meta, gsr=True).shape == (120, 1 + 24 + 10 + 4 + 1)


def test_denoising_recovers_planted_coupling():
    rng = np.random.default_rng(5)
    conf, meta = syn.confounds(3000, rng)
    ts = syn.regions(conf, rng, coupling=0.4, nuisance_scale=5.0)
    raw_r = np.corrcoef(ts["amygdala_bilateral"], ts["vmpfc_fmc"])[0, 1]
    z = dn.run_connectivity(ts, conf, meta, [pt.PRIMARY])
    r = np.tanh(z["amygdala_bilateral__vmpfc_fmc"])
    assert abs(r - 0.4) < 0.05
    assert abs(raw_r - 0.4) > 0.1  # the nuisance really distorted the raw value


def test_censored_volumes_do_not_influence_connectivity():
    rng = np.random.default_rng(6)
    fd = np.full(400, 0.1)
    spikes = [50, 51, 200, 333]
    fd[spikes] = 2.0
    conf, meta = syn.confounds(400, rng, fd=fd)
    ts = syn.regions(conf, rng, coupling=0.3)
    base = dn.run_connectivity(ts, conf, meta, [pt.PRIMARY], rule=dn.RULE_UNFILTERED)
    ts2 = ts.copy()
    ts2.loc[spikes, ["amygdala_bilateral", "vmpfc_fmc"]] += 1e4
    assert dn.run_connectivity(ts2, conf, meta, [pt.PRIMARY], rule=dn.RULE_UNFILTERED) == pytest.approx(base)


def test_region_mean_denoising_equals_voxelwise_then_mean():
    rng = np.random.default_rng(7)
    conf, meta = syn.confounds(300, rng)
    x = dn.design_matrix(conf, meta)
    vox = rng.normal(size=(300, 40)) + x[:, 1:6] @ rng.normal(size=(5, 40))
    a = dn.residualize(vox, x).mean(axis=1)
    b = dn.residualize(vox.mean(axis=1, keepdims=True), x)[:, 0]
    assert np.allclose(a, b)


def _run(rng, fd=None, coupling=0.3):
    conf, meta = syn.confounds(500, rng, fd=fd)
    return syn.regions(conf, rng, coupling), conf, meta


def test_participant_needs_two_usable_runs_and_averages_only_usable():
    rng = np.random.default_rng(8)
    good1, good2 = _run(rng), _run(rng)
    bad = _run(rng, fd=_fd_with(500, 200))
    s = pt.summarize_runs([good1, bad, good2], rule=dn.RULE_UNFILTERED)
    assert s["n_runs"] == 3 and s["n_usable_runs"] == 2 and s["included"]
    z1 = dn.run_connectivity(*good1, pt.ALL_PAIRS, rule=dn.RULE_UNFILTERED)
    z2 = dn.run_connectivity(*good2, pt.ALL_PAIRS, rule=dn.RULE_UNFILTERED)
    key = "amygdala_bilateral__vmpfc_fmc"
    assert s[f"z__{key}"] == pytest.approx((z1[key] + z2[key]) / 2)
    assert s["n_retained"] == 1000
    fds = np.concatenate([good1[1]["framewise_displacement"],
                          good2[1]["framewise_displacement"]])
    assert s["mean_fd"] == pytest.approx(np.nanmean(fds))
    one = pt.summarize_runs([good1, bad, _run(rng, fd=np.full(500, 0.4))], rule=dn.RULE_UNFILTERED)
    assert one["n_usable_runs"] == 1 and not one["included"]
