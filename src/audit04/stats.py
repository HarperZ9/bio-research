"""Agreement and interval statistics (stdlib only)."""
import math
from collections import Counter


def wilson(k, n, z=1.959964):
    """Wilson 95% score interval for k successes in n trials."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, mid - half), min(1.0, mid + half))


def cohen_kappa(a, b):
    """Cohen's kappa for two equal-length label lists."""
    if len(a) != len(b) or not a:
        raise ValueError("label lists must be equal length and non-empty")
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan"), po


def fmt_share(k, n):
    lo, hi = wilson(k, n)
    if n == 0:
        return "0/0"
    return f"{k}/{n} = {k / n:.1%} [{lo:.1%}, {hi:.1%}]"
