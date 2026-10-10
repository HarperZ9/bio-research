"""Synthetic-data checks for region extraction and the per-participant files."""
import json

import nibabel as nib
import numpy as np
import pytest

import conn01_synth as syn
from conn01 import atlas, extract, participant as pt


def test_masks_from_labels_bilateral_is_union_of_sides():
    sub = np.zeros((4, 4, 4), int)
    sub[0, 0, 0], sub[1, 1, 1], sub[2, 2, 2] = 10, 20, 9  # 9 = hippocampus
    cort = np.zeros((4, 4, 4), int)
    cort[3, 3, 3], cort[0, 3, 0] = 25, 27
    m = atlas.masks_from_labels({"HOSPA": sub, "HOCPA": cort})
    assert m["amygdala_bilateral"].sum() == 2 and not m["amygdala_bilateral"][2, 2, 2]
    assert m["amygdala_l"][0, 0, 0] and m["amygdala_r"][1, 1, 1]
    assert m["vmpfc_fmc"].sum() == 1 and m["subcallosal"][0, 3, 0]


def test_masks_from_labels_rejects_empty_region():
    with pytest.raises(ValueError):
        atlas.masks_from_labels({"HOSPA": np.zeros((2, 2, 2), int),
                                 "HOCPA": np.zeros((2, 2, 2), int)})


def test_region_means_are_voxel_means():
    data = np.arange(2 * 2 * 1 * 3, dtype=float).reshape(2, 2, 1, 3)
    mask = np.zeros((2, 2, 1), bool)
    mask[0, 0, 0] = mask[1, 1, 0] = True
    out = atlas.region_means(data, {"r": mask})["r"]
    assert np.allclose(out, (data[0, 0, 0] + data[1, 1, 0]) / 2)


def _fake_masks(shape):
    masks = {}
    for i, name in enumerate(syn.REGIONS):
        m = np.zeros(shape, bool)
        m[i, :, :] = True
        masks[name] = m
    return masks


def _write_fake_fmriprep(root, label, rng, n_runs=3, t=300):
    func = root / "fmriprep" / f"sub-{label}" / "func"
    func.mkdir(parents=True)
    shape = (len(syn.REGIONS), 3, 3)
    for k in range(1, n_runs + 1):
        stem = f"sub-{label}_task-restAP_run-{k:02d}"
        conf, meta = syn.confounds(t, rng)
        ts = syn.regions(conf, rng, coupling=0.3)
        vol = np.zeros(shape + (t,), np.float32)
        for i, name in enumerate(syn.REGIONS):
            vol[i] = ts[name].to_numpy()[None, None, :]
        img = nib.Nifti1Image(vol, np.eye(4))
        nib.save(img, func / f"{stem}_{extract.SPACE}_desc-preproc_bold.nii.gz")
        conf.to_csv(func / f"{stem}_desc-confounds_timeseries.tsv", sep="\t", index=False)
        (func / f"{stem}_desc-confounds_timeseries.json").write_text(json.dumps(meta))
    (root / "fmriprep" / "dataset_description.json").write_text(
        json.dumps({"GeneratedBy": [{"Name": "fMRIPrep", "Version": "synthetic"}]}))
    return shape


def test_process_participant_end_to_end(tmp_path, monkeypatch):
    rng = np.random.default_rng(0)
    shape = _write_fake_fmriprep(tmp_path, "SYN01", rng)
    monkeypatch.setattr(atlas, "load_masks",
                        lambda reference_img=None: (_fake_masks(shape), np.eye(4)))
    monkeypatch.setattr(extract, "CHUNK", 7)  # force several chunks
    receipt = tmp_path / "sdc.json"
    receipt.write_text(json.dumps({"sdc_path": "syn", "reason": "synthetic"}))
    out = extract.process_participant(tmp_path / "fmriprep", tmp_path / "bids",
                                      "SYN01", tmp_path / "conn01", receipt)
    ts_files = sorted(out.glob("*_run-0?_timeseries.tsv"))
    assert len(ts_files) == 3
    qc = json.loads((out / "sub-SYN01_qc.json").read_text())
    assert qc["n_runs"] == 3 and qc["meets_min_usable_runs"]
    assert qc["runs"][0]["n_acompcor_wm_retained"] == 7
    assert qc["runs"][0]["n_acompcor_wm_used"] == 5
    assert qc["acompcor_min_used"] == {"WM": 5, "CSF": 5}
    assert qc["sdc"]["sdc_path"] == "syn"
    assert qc["fmriprep_generated_by"][0]["Version"] == "synthetic"
    assert "z__" not in json.dumps(qc)  # extraction stores no connectivity
    (out / "DONE").touch()
    table = pt.build_outcome_table(tmp_path / "conn01")
    assert table.loc[0, "participant_id"] == "sub-SYN01" and table.loc[0, "included"]
    r = np.tanh(table.loc[0, "z__amygdala_bilateral__vmpfc_fmc"])
    assert abs(r - 0.3) < 0.12


def test_extracted_series_match_planted_voxel_values(tmp_path, monkeypatch):
    rng = np.random.default_rng(1)
    shape = _write_fake_fmriprep(tmp_path, "SYN02", rng, n_runs=1, t=50)
    monkeypatch.setattr(atlas, "load_masks",
                        lambda reference_img=None: (_fake_masks(shape), np.eye(4)))
    bold = extract.find_runs(tmp_path / "fmriprep", "SYN02")[0]
    ts = extract.extract_timeseries(bold)
    vol = np.asarray(nib.load(str(bold)).dataobj)
    assert np.allclose(ts["vmpfc_fmc"], vol[3, 0, 0], atol=1e-4)


def test_participant_with_compcor_shortfall_is_kept_with_count(tmp_path):
    rng = np.random.default_rng(2)
    d = tmp_path / "sub-X"
    d.mkdir()
    for k in (1, 2):
        conf, meta = syn.confounds(200, rng, n_wm=4)
        stem = f"sub-X_task-restAP_run-{k:02d}"
        syn.regions(conf, rng, 0.3).to_csv(d / f"{stem}_timeseries.tsv", sep="\t", index=False)
        conf.to_csv(d / f"{stem}_desc-confounds_timeseries.tsv", sep="\t", index=False)
        (d / f"{stem}_desc-confounds_timeseries.json").write_text(json.dumps(meta))
    (d / "DONE").touch()
    table = pt.build_outcome_table(tmp_path)
    row = table.loc[0]
    assert row["included"] and row["error"] == ""
    assert row["n_compcor_wm_min"] == 4 and row["n_compcor_csf_min"] == 5
