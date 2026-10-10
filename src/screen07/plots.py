"""QC plot: PCA of samples, marked by condition and covariate."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def pca_plot(logexpr: pd.DataFrame, samples: pd.DataFrame,
             covariates: list[str], out: Path, title: str) -> None:
    """PC1 vs PC2 on the 2,000 most variable genes."""
    top = logexpr.loc[logexpr.var(axis=1).nlargest(2000).index]
    Z = (top.T - top.T.mean()).to_numpy()
    u, s, _ = np.linalg.svd(Z, full_matrices=False)
    pcs = u[:, :2] * s[:2]
    var = s ** 2 / np.sum(s ** 2)
    fig, ax = plt.subplots(figsize=(5, 4))
    markers = ["o", "s", "^", "D"]
    cov = samples[covariates[0]] if covariates else pd.Series("all", index=samples.index)
    for i, lev in enumerate(sorted(cov.unique())):
        for cond, color in (("control", "#444444"), ("defeated", "#c0392b")):
            m = ((cov == lev) & (samples["condition"] == cond)).to_numpy()
            ax.scatter(pcs[m, 0], pcs[m, 1], c=color, marker=markers[i % 4],
                       label=f"{cond} {lev}", s=30)
    ax.set_xlabel(f"PC1 ({var[0]:.0%})")
    ax.set_ylabel(f"PC2 ({var[1]:.0%})")
    ax.set_title(title, fontsize=8)
    ax.legend(fontsize=6)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
