"""Per-region signal quality QC: temporal SNR and coverage (record only).

Computed on the minimally processed BOLD (fMRIPrep desc-preproc, before any
denoising), streamed in volume chunks alongside region extraction:
  tsnr_median  median over the region's voxels of mean over time / SD over
               time (population SD; voxels with SD 0 are left out)
  coverage     fraction of the region's voxels whose temporal mean is above
               50% of the median temporal mean over the brain mask
No exclusion rule uses these numbers; adding one would need a
pre-registration deviation. They flag susceptibility dropout near vmPFC.
"""
from __future__ import annotations

import numpy as np

COVERAGE_FRACTION_OF_MEDIAN = 0.5
QC_REGIONS = ("amygdala_l", "amygdala_r", "vmpfc_fmc", "subcallosal")


class SignalAccumulator:
    """Running per-voxel sum and sum of squares over time chunks."""

    def __init__(self, shape3: tuple[int, int, int]):
        self.s1 = np.zeros(shape3, np.float64)
        self.s2 = np.zeros(shape3, np.float64)
        self.n = 0

    def add(self, block: np.ndarray) -> None:
        """Add a (x, y, z, t) block of volumes."""
        b = np.asarray(block, np.float64)
        self.s1 += b.sum(axis=3)
        self.s2 += np.square(b).sum(axis=3)
        self.n += b.shape[3]

    def mean_sd(self) -> tuple[np.ndarray, np.ndarray]:
        if self.n < 2:
            raise ValueError("signal QC needs at least two volumes")
        mean = self.s1 / self.n
        var = np.maximum(self.s2 / self.n - mean ** 2, 0.0)
        return mean, np.sqrt(var)


def summarize(acc: SignalAccumulator, masks: dict[str, np.ndarray],
              brain_mask: np.ndarray, mask_source: str,
              regions: tuple[str, ...] = QC_REGIONS) -> dict:
    """tSNR median and coverage per region, plus how the reference was set."""
    mean, sd = acc.mean_sd()
    brain = np.asarray(brain_mask, bool)
    if not brain.any():
        raise ValueError("brain mask is empty")
    ref = float(np.median(mean[brain]))
    cut = COVERAGE_FRACTION_OF_MEDIAN * ref
    out = {"brain_mask": mask_source, "brain_median_mean_signal": ref,
           "coverage_cut": cut, "n_volumes": acc.n, "regions": {}}
    for name in regions:
        m = np.asarray(masks[name], bool)
        mu, s = mean[m], sd[m]
        ok = s > 0
        tsnr = mu[ok] / s[ok]
        out["regions"][name] = {
            "n_voxels": int(m.sum()),
            "tsnr_median": float(np.median(tsnr)) if tsnr.size else float("nan"),
            "coverage": float(np.mean(mu > cut)) if mu.size else float("nan"),
        }
    return out
