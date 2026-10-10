"""Synthetic checks for the AFNI fallback path (prereg 01 deviation 4).

The key property: what the AFNI path writes is read by extract.py,
denoise.py and participant.py unchanged, with the same QC keys as the
fMRIPrep path.
"""
import json
import shutil
import subprocess

import nibabel as nib
import numpy as np
import pandas as pd
import pytest

import conn01_synth as syn
from conn01 import afni_confounds as ac
from conn01 import afni_prep as ap
from conn01 import afni_qc as aq
from conn01 import atlas, extract
from conn01 import denoise as dn
from conn01 import participant as pt


def test_motion_mapping_axes_and_units():
    d = np.array([[10.0, 20.0, 30.0, 1.0, 2.0, 3.0]])  # roll pitch yaw dS dL dP
    m = ac.afni_motion_to_fmriprep(d).iloc[0]
    assert (m.trans_x, m.trans_y, m.trans_z) == (2.0, 3.0, 1.0)
    assert m.rot_x == pytest.approx(np.deg2rad(20))  # pitch, about L-R
    assert m.rot_y == pytest.approx(np.deg2rad(30))  # yaw, about A-P
    assert m.rot_z == pytest.approx(np.deg2rad(10))  # roll, about I-S
    with pytest.raises(ValueError):
        ac.afni_motion_to_fmriprep(np.zeros((4, 5)))


def test_expansion_gives_the_24_names_denoise_reads():
    rng = np.random.default_rng(0)
    motion = ac.afni_motion_to_fmriprep(rng.normal(size=(20, 6)))
    ex = ac.expand_dd1_squared(motion)
    assert list(ex.columns) == dn.MOTION_24
    assert np.isnan(ex["trans_x_derivative1"].iloc[0])
    assert ex["rot_z_power2"].iloc[5] == pytest.approx(motion["rot_z"].iloc[5] ** 2)
    d1 = motion["trans_y"].iloc[7] - motion["trans_y"].iloc[6]
    assert ex["trans_y_derivative1_power2"].iloc[7] == pytest.approx(d1 ** 2)


def test_fd_is_power_with_50_mm_radius():
    motion = pd.DataFrame(0.0, index=range(3), columns=ac.MOTION_COLS)
    motion.loc[1, "trans_x"] = 0.3
    motion.loc[2, ["trans_x", "rot_z"]] = [0.3, 0.01]
    fd = ac.framewise_displacement(motion)
    assert np.isnan(fd[0])
    assert fd[1] == pytest.approx(0.3) and fd[2] == pytest.approx(0.5)


def test_cosine_basis_count_and_orthonormality():
    x = ac.cosine_drift(488, 0.8)
    assert x.shape == (488, 6)  # floor(2 * 488 * 0.8 / 128) = 6, last is constant
    c = x[:, :-1]
    assert np.allclose(c.T @ c, np.eye(5), atol=1e-10)


def test_non_steady_state_counts_leading_outliers_only():
    rng = np.random.default_rng(1)
    g = 1000 + rng.normal(0, 1, 60)
    assert ac.non_steady_state_count(g) == 0
    g[:3] += 200
    g[10] += 200  # a later spike is not a non-steady-state volume
    assert ac.non_steady_state_count(g) == 3


def test_compcor_recovers_planted_component_and_50_percent_rule():
    rng = np.random.default_rng(2)
    t = 300
    tt = np.arange(t)
    sig = np.sin(tt / 3.0)
    vox = 100 + np.outer(rng.normal(3, 0.5, 400), sig) + rng.normal(0, 1, (400, t))
    comps, s, var, cum, k = ac.compcor(vox, tr=0.8)
    assert k == int(np.searchsorted(cum, 0.5) + 1) and cum[k - 1] >= 0.5
    assert abs(np.corrcoef(comps[:, 0], sig)[0, 1]) > 0.95
    assert np.all(np.diff(s) <= 1e-9)


def _series(rng, t, n=(60, 80, 140)):
    return {m: 100 + rng.normal(size=(k, t)) + np.outer(rng.normal(size=k), rng.normal(size=t))
            for m, k in zip(("CSF", "WM", "combined"), n)}


def test_compcor_table_names_padding_and_denoise_compatibility():
    rng = np.random.default_rng(3)
    t, skip = 200, 2
    table, meta = ac.compcor_table(_series(rng, t), tr=0.8, skip=skip, n_vols=t)
    assert all(c.startswith(("c_comp_cor_", "w_comp_cor_", "a_comp_cor_")) for c in table)
    assert all(meta[c]["Mask"] == "CSF" for c in table if c.startswith("c_"))
    assert np.all(table.iloc[:skip].to_numpy() == 0)
    wm = dn.compcor_columns(meta, "WM")
    assert wm and all(c.startswith("w_comp_cor_") for c in wm)
    assert not any(c.startswith("a_comp_cor_") for c in dn.compcor_columns(meta, "CSF"))


def test_build_confounds_feeds_denoise_unchanged():
    rng = np.random.default_rng(4)
    t, skip = 240, 1
    dfile = np.cumsum(rng.normal(0, 0.02, (t, 6)), axis=0)
    table, meta = ac.build_confounds(dfile, _series(rng, t), 100 + rng.normal(size=t), 0.8, skip)
    x = dn.design_matrix(table, meta)
    n_cc = sum(dn.compcor_counts(meta).values())
    n_cos = sum(c.startswith("cosine") for c in table)
    assert x.shape == (t, 1 + 24 + n_cc + n_cos)
    assert dn.design_matrix(table, meta, gsr=True).shape[1] == x.shape[1] + 1
    assert "non_steady_state_outlier00" in table and "non_steady_state_outlier01" not in table
    q = dn.run_qc(table)
    assert q.n_volumes == t and np.isfinite(q.mean_fd)
    with pytest.raises(ValueError):
        ac.build_confounds(dfile[:-1], _series(rng, t), np.zeros(t), 0.8, 0)


def test_acompcor_pv_masks_remove_dilated_gm_from_wm_not_csf():
    shape = (20, 20, 20)
    gm = np.zeros(shape)
    gm[10, 10, 10] = 0.5
    wm = np.ones(shape)
    csf = np.full(shape, 0.3)
    out = ap.acompcor_pv_masks(gm, wm, csf)
    assert out["WM"][10, 10, 13] == 0 and out["WM"][10, 10, 14] == 1  # ball radius 3
    assert out["WM"][11, 11, 11] == 0 and out["WM"][12, 12, 12] == 1  # 4+4+4 > 9
    assert np.all(out["CSF"] == 0.3)
    assert out["combined"][10, 10, 10] == 0 and out["combined"][0, 0, 0] == pytest.approx(1.3)


def _write_bids(sub_dir, fmap_dirs=("j", "j-"), bold_dirs=("j-", "j")):
    for d in ("fmap", "func"):
        (sub_dir / d).mkdir(parents=True)
    for tag, pe in zip(("ap", "pa"), fmap_dirs):
        base = sub_dir / "fmap" / f"sub-X_dir-{tag}_epi"
        base.with_suffix(".nii.gz").write_bytes(b"")
        base.with_suffix(".json").write_text(json.dumps(
            {"PhaseEncodingDirection": pe, "TotalReadoutTime": 0.05}))
    for task, pe in zip(("restAP", "restPA"), bold_dirs):
        base = sub_dir / "func" / f"sub-X_task-{task}_run-01_bold"
        base.with_suffix(".nii.gz").write_bytes(b"")
        base.with_suffix(".json").write_text(json.dumps({"PhaseEncodingDirection": pe}))


def _geo(_):
    return ((10, 10, 5), (2.0, 2.0, 2.0), np.eye(4))


def test_blip_plan_pairs_each_run_with_matching_forward_map(tmp_path):
    sub = tmp_path / "sub-X"
    _write_bids(sub)
    r = ap.blip_plan(sub, geometry=_geo)
    assert r["afni_sdc"] == "blip_reverse" and len(r["runs"]) == 2
    for bold, pair in r["runs"].items():
        pe = json.loads((sub / "func" / bold.split("/")[-1].replace(".nii.gz", ".json"))
                        .read_text())["PhaseEncodingDirection"]
        fwd = json.loads(open(pair["forward"].replace(".nii.gz", ".json")).read())
        rev = json.loads(open(pair["reverse"].replace(".nii.gz", ".json")).read())
        assert fwd["PhaseEncodingDirection"] == pe != rev["PhaseEncodingDirection"]


def test_blip_plan_falls_back_to_none_when_fieldmaps_do_not_pair(tmp_path):
    sub = tmp_path / "sub-X"
    _write_bids(sub, fmap_dirs=("j", "j"))
    r = ap.blip_plan(sub, geometry=_geo)
    assert r["afni_sdc"] == "none" and r["sdc_path"] == "syn"
    assert all(p == {"forward": None, "reverse": None} for p in r["runs"].values())


def test_slice_times_read_from_sidecar(tmp_path):
    side = tmp_path / "b.json"
    side.write_text(json.dumps({"SliceTiming": [0, 0.4, 0, 0.4]}))
    assert ap.slice_times(side) == [0.0, 0.4, 0.0, 0.4]
    side.write_text("{}")
    with pytest.raises(KeyError):
        ap.slice_times(side)


def test_tsnr_map_matches_mean_over_residual_sd():
    rng = np.random.default_rng(5)
    noise = rng.normal(0, 2.0, (3, 400))
    data = 100 + noise
    out = aq.tsnr_map(data, tr=0.8)
    assert np.allclose(out, 50, rtol=0.1)
    assert aq.tsnr_map(np.full((1, 50), 7.0), 0.8)[0] == 0  # zero variance -> 0


def _afni_like_participant(root, label, rng, n_runs=2, t=220):
    """Synthetic AFNI derivative written through afni_prep.write_confounds."""
    func = root / "afni" / f"sub-{label}" / "func"
    func.mkdir(parents=True)
    shape = (len(syn.REGIONS) + 3, 6, 6)
    aff = np.diag([2.0, 2.0, 2.0, 1.0])
    pv_dir = root / "pv"
    pv_dir.mkdir(exist_ok=True)
    brain = np.ones(shape, np.uint8)
    nib.Nifti1Image(brain, aff).to_filename(str(root / "mask.nii.gz"))
    for i, k in enumerate(("CSF", "WM", "combined")):
        pv = np.zeros(shape, np.float32)
        pv[len(syn.REGIONS) + i] = 1.0
        nib.Nifti1Image(pv, aff).to_filename(str(pv_dir / f"acompcor_{k}.nii.gz"))
    for k in range(1, n_runs + 1):
        stem = f"sub-{label}_task-restAP_run-{k:02d}"
        vol = (100 + rng.normal(size=shape + (t,))).astype(np.float32)
        bold = func / f"{stem}_{extract.SPACE}_desc-preproc_bold.nii.gz"
        nib.Nifti1Image(vol, aff).to_filename(str(bold))
        dfile = root / f"{stem}_dfile.1D"
        np.savetxt(dfile, np.cumsum(rng.normal(0, 0.01, (t, 6)), axis=0))
        ap.write_confounds(bold, root / "mask.nii.gz", pv_dir, dfile, 0.8, 0,
                           func / f"{stem}_desc-confounds_timeseries.tsv")
    (root / "afni" / "dataset_description.json").write_text(json.dumps(
        {"GeneratedBy": [{"Name": "AFNI", "Version": "synthetic"}]}))
    return shape


def _fake_masks(shape):
    masks = {}
    for i, name in enumerate(syn.REGIONS):
        m = np.zeros(shape, bool)
        m[i] = True
        masks[name] = m
    return masks


def test_afni_outputs_run_through_extract_and_participant_unchanged(tmp_path, monkeypatch):
    rng = np.random.default_rng(6)
    shape = _afni_like_participant(tmp_path, "AFN01", rng)
    monkeypatch.setattr(atlas, "load_masks",
                        lambda reference_img=None: (_fake_masks(shape), np.eye(4)))
    receipt = tmp_path / "sdc.json"
    receipt.write_text(json.dumps({"sdc_path": "fieldmaps", "afni_sdc": "blip_reverse"}))
    out = extract.process_participant(tmp_path / "afni", tmp_path / "bids", "AFN01",
                                      tmp_path / "conn01", receipt)
    qc = json.loads((out / "sub-AFN01_qc.json").read_text())
    assert set(qc) == {"participant", "fmriprep_generated_by", "n_runs", "n_usable_runs",
                       "meets_min_usable_runs", "acompcor_min_used", "sdc", "regions", "runs"}
    assert qc["fmriprep_generated_by"][0]["Name"] == "AFNI"
    assert qc["acompcor_min_used"]["WM"] >= 1 and qc["acompcor_min_used"]["CSF"] >= 1
    assert set(qc["runs"][0]) >= {"run", "n_volumes", "n_censored", "mean_fd", "usable",
                                  "n_acompcor_wm_used", "n_non_steady_state"}
    (out / "DONE").touch()
    table = pt.build_outcome_table(tmp_path / "conn01")
    assert table.loc[0, "included"] and table.loc[0, "error"] == ""


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_pipeline_guard_refuses_to_mix(tmp_path):
    from pathlib import Path

    guard = Path(__file__).resolve().parents[1] / "scripts" / "pipeline_guard.sh"
    out = tmp_path / "conn01"

    def run(pipe):
        cmd = f'. "{guard.as_posix()}"; pipeline_guard "{out.as_posix()}" {pipe}'
        return subprocess.run(["bash", "-c", cmd], capture_output=True, text=True).returncode

    if run("afni") != 0:
        pytest.skip("bash cannot reach the temp path on this platform")
    assert (out / "PIPELINE").read_text().strip() == "afni"
    assert run("afni") == 0 and run("fmriprep") == 3 and run("other") == 2
    (out / "PIPELINE").unlink()  # no marker: inferred from an existing QC JSON
    (out / "sub-A").mkdir()
    (out / "sub-A" / "sub-A_qc.json").write_text(json.dumps(
        {"fmriprep_generated_by": [{"Name": "fMRIPrep"}]}, indent=2))
    assert run("afni") == 3 and run("fmriprep") == 0
