"""Field map linking (prereg 01 deviation 3) on synthetic BIDS sidecars."""
import json

import nibabel as nib
import numpy as np

import conn01_synth  # noqa: F401  (adds src/ to sys.path)
from conn01 import fmaplink as fl

SUB = "sub-SYN"


def _nifti(path, shape=(8, 8, 4), zoom=2.0, t=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = np.zeros(shape + ((t,) if t else ()), np.int16)
    nib.save(nib.Nifti1Image(data, np.diag([zoom, zoom, zoom, 1.0])), path)


def _sidecar(path, **meta):
    path.with_name(path.name.replace(".nii.gz", ".json")).write_text(json.dumps(meta))


def make_subject(root, ses="", fmap_dirs=("j", "j-"), bold_dir="j-",
                 fmap_shape=(8, 8, 4), fmap_id="SpinEchoFieldMap_fmap",
                 trt=0.0597):
    sub = root / SUB
    base = sub / ses if ses else sub
    tag = f"_{ses}" if ses else ""
    for d, name in zip(fmap_dirs, ("ap", "pa")):
        f = base / "fmap" / f"{SUB}{tag}_dir-{name}_epi.nii.gz"
        _nifti(f, fmap_shape, t=3)
        meta = {"PhaseEncodingDirection": d}
        if trt is not None:
            meta["TotalReadoutTime"] = trt
        if fmap_id:
            meta["B0FieldIdentifier"] = fmap_id
        _sidecar(f, **meta)
    for task in ("restAP", "restPA"):
        b = base / "func" / f"{SUB}{tag}_task-{task}_run-01_bold.nii.gz"
        _nifti(b, (8, 8, 4), t=5)
        _sidecar(b, PhaseEncodingDirection=bold_dir, RepetitionTime=0.8)
    return sub


def _json(path):
    return json.loads(path.read_text())


def test_compatible_session_links_fieldmaps(tmp_path):
    sub = make_subject(tmp_path)
    receipt_path = tmp_path / "work" / "sdc.json"
    fl.main(["--sub-dir", str(sub), "--receipt", str(receipt_path),
             "--backup-dir", str(tmp_path / "work" / "orig")])
    receipt = _json(receipt_path)
    assert receipt["sdc_path"] == "fieldmaps" and receipt["reason"] == ""
    fmap = _json(sub / "fmap" / f"{SUB}_dir-ap_epi.json")
    assert fmap["IntendedFor"] == [f"func/{SUB}_task-restAP_run-01_bold.nii.gz",
                                   f"func/{SUB}_task-restPA_run-01_bold.nii.gz"]
    bold = _json(sub / "func" / f"{SUB}_task-restAP_run-01_bold.json")
    assert bold["B0FieldSource"] == "SpinEchoFieldMap_fmap"
    orig = _json(tmp_path / "work" / "orig" / f"{SUB}_dir-ap_epi.json")
    assert "IntendedFor" not in orig  # backup keeps the untouched sidecar


def test_same_direction_pair_falls_back_to_syn_and_edits_nothing(tmp_path):
    sub = make_subject(tmp_path, fmap_dirs=("j-", "j-"))
    receipt_path = tmp_path / "sdc.json"
    fl.main(["--sub-dir", str(sub), "--receipt", str(receipt_path),
             "--backup-dir", str(tmp_path / "orig")])
    receipt = _json(receipt_path)
    assert receipt["sdc_path"] == "syn" and "opposite" in receipt["reason"]
    assert "IntendedFor" not in _json(sub / "fmap" / f"{SUB}_dir-ap_epi.json")
    assert "B0FieldSource" not in _json(sub / "func" / f"{SUB}_task-restAP_run-01_bold.json")


def test_bold_on_other_axis_falls_back_to_syn(tmp_path):
    receipt = fl.plan(make_subject(tmp_path, bold_dir="i"))
    assert receipt["sdc_path"] == "syn" and "axis" in receipt["reason"]


def test_geometry_mismatch_falls_back_to_syn(tmp_path):
    receipt = fl.plan(make_subject(tmp_path, fmap_shape=(8, 8, 6)))
    assert receipt["sdc_path"] == "syn" and "geometry" in receipt["reason"]


def test_missing_readout_time_or_fieldmaps_falls_back_to_syn(tmp_path):
    assert fl.plan(make_subject(tmp_path / "a", trt=None))["sdc_path"] == "syn"
    sub = make_subject(tmp_path / "b")
    for f in (sub / "fmap").iterdir():
        f.unlink()
    receipt = fl.plan(sub)
    assert receipt["sdc_path"] == "syn" and "no field maps" in receipt["reason"]


def test_sessions_link_only_within_their_own_session(tmp_path):
    make_subject(tmp_path, ses="ses-1")
    sub = make_subject(tmp_path, ses="ses-2")
    receipt = fl.plan(sub)
    assert receipt["sdc_path"] == "fieldmaps"
    fl.apply_links(sub, receipt, tmp_path / "orig")
    f1 = _json(sub / "ses-1" / "fmap" / f"{SUB}_ses-1_dir-ap_epi.json")
    assert f1["IntendedFor"] and all(p.startswith("ses-1/func/") for p in f1["IntendedFor"])
    f2 = _json(sub / "ses-2" / "fmap" / f"{SUB}_ses-2_dir-pa_epi.json")
    assert all(p.startswith("ses-2/func/") for p in f2["IntendedFor"])


def test_one_bad_session_sends_participant_to_syn(tmp_path):
    make_subject(tmp_path, ses="ses-1")
    sub = make_subject(tmp_path, ses="ses-2", bold_dir="i-")
    receipt = fl.plan(sub)
    assert receipt["sdc_path"] == "syn" and receipt["reason"].startswith("ses-2")
    assert receipt["sessions"]["ses-1"]["compatible"]
