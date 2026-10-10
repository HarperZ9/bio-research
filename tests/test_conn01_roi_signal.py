"""Per-region tSNR and coverage QC on a synthetic BOLD with planted dropout."""
import json

import nibabel as nib
import numpy as np
import pytest

import conn01_synth as syn
from conn01 import atlas, extract
from conn01 import roi_signal as rs


def _masks(shape):
    masks = {}
    for i, name in enumerate(syn.REGIONS):
        m = np.zeros(shape, bool)
        m[i] = True
        masks[name] = m
    return masks


def _bold(tmp_path, t=120):
    """Brain rows 0..5; vmPFC (row 3) has half its voxels at 10% signal."""
    rng = np.random.default_rng(0)
    shape = (len(syn.REGIONS) + 1, 4, 4)
    mean = np.full(shape, 1000.0)
    sd = np.full(shape, 20.0)  # tSNR 50 everywhere ...
    sd[0] = 100.0  # ... except amygdala_l, tSNR 10
    mean[3, :2] = 100.0  # vmPFC dropout: 8 of 16 voxels, tSNR 5 there
    noise = rng.normal(size=shape + (t,))
    noise = (noise - noise.mean(3, keepdims=True)) / noise.std(3, keepdims=True)
    vol = (mean[..., None] + sd[..., None] * noise).astype(np.float32)
    func = tmp_path / "func"
    func.mkdir()
    bold = func / f"sub-S_task-restAP_run-01_{extract.SPACE}_desc-preproc_bold.nii.gz"
    nib.Nifti1Image(vol, np.eye(4)).to_filename(str(bold))
    brain = np.ones(shape, np.uint8)
    nib.Nifti1Image(brain, np.eye(4)).to_filename(str(extract.brain_mask_path(bold)))
    return bold, shape


def test_tsnr_and_coverage_recover_planted_values(tmp_path, monkeypatch):
    bold, shape = _bold(tmp_path)
    monkeypatch.setattr(atlas, "load_masks",
                        lambda reference_img=None: (_masks(shape), np.eye(4)))
    monkeypatch.setattr(extract, "CHUNK", 7)  # accumulate over several chunks
    _, sig = extract.extract_run(bold)
    reg = sig["regions"]
    assert set(reg) == {"amygdala_l", "amygdala_r", "vmpfc_fmc", "subcallosal"}
    assert sig["brain_mask"].endswith("desc-brain_mask.nii.gz")
    assert sig["n_volumes"] == 120
    assert reg["amygdala_r"]["tsnr_median"] == pytest.approx(50, rel=1e-3)
    assert reg["amygdala_l"]["tsnr_median"] == pytest.approx(10, rel=1e-3)
    assert reg["amygdala_r"]["coverage"] == 1.0
    assert reg["vmpfc_fmc"]["coverage"] == 0.5  # 100 < 0.5 x median 1000
    assert reg["vmpfc_fmc"]["n_voxels"] == 16


def test_accumulator_matches_direct_mean_and_sd():
    rng = np.random.default_rng(1)
    data = 50 + rng.normal(size=(3, 3, 2, 40))
    acc = rs.SignalAccumulator((3, 3, 2))
    for t0 in range(0, 40, 9):
        acc.add(data[..., t0:t0 + 9])
    mean, sd = acc.mean_sd()
    assert np.allclose(mean, data.mean(3)) and np.allclose(sd, data.std(3))


def test_roi_signal_is_recorded_in_qc_and_changes_no_usability(tmp_path, monkeypatch):
    bold, shape = _bold(tmp_path)
    monkeypatch.setattr(atlas, "load_masks",
                        lambda reference_img=None: (_masks(shape), np.eye(4)))
    rng = np.random.default_rng(2)
    conf, meta = syn.confounds(120, rng)
    stem = extract.run_stem(bold)
    conf.to_csv(bold.parent / f"{stem}_desc-confounds_timeseries.tsv", sep="\t", index=False)
    (bold.parent / f"{stem}_desc-confounds_timeseries.json").write_text(json.dumps(meta))
    fmriprep = tmp_path / "fmriprep"
    (fmriprep / "sub-S").mkdir(parents=True)
    (tmp_path / "func").rename(fmriprep / "sub-S" / "func")
    out = extract.process_participant(fmriprep, tmp_path / "bids", "S", tmp_path / "conn01")
    run = json.loads((out / "sub-S_qc.json").read_text())["runs"][0]
    assert run["roi_signal"]["regions"]["vmpfc_fmc"]["coverage"] == 0.5
    # Record only: usability is decided by motion QC alone.
    assert run["usable"] == (run["censored_fraction"] <= 0.2 and run["mean_fd"] <= 0.3)
