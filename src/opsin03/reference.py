"""Reference values and acceptance rules for step 1.

Primary characterization paper (opened and read 2026-10-09):
Lin JY, Lin MZ, Steinbach P, Tsien RY. 2009. Characterization of engineered
channelrhodopsin variants with improved properties and kinetics. Biophys J
96:1803-1814. doi:10.1016/j.bpj.2008.11.034, PMC2717302
(https://pmc.ncbi.nlm.nih.gov/articles/PMC2717302/). HEK293 cells, room
temperature, 470 nm LED.

Table 3, wild-type ChR2 (n = 7, mean +/- SEM):
  I_plateau / I_max = 0.215 +/- 0.023
  closing tau = 13.39 +/- 1.05 ms (10 ms pulse), 13.54 +/- 1.39 ms (500 ms)
Table 3, ChR2(H134R) (n = 7): ratio 0.387 +/- 0.019, closing tau
  17.96 +/- 1.18 ms (10 ms pulse), 17.92 +/- 1.37 ms (500 ms pulse).
Text: closure rates "independent of stimulus intensity or duration".
Fig. 1 text: ChR2 plateau 23.0% +/- 1.4% of maximum, 500 ms light, n = 11.

Holding potential: not stated in the passages I read. A ~87 mV driving force
with E_rev ~8 mV implies about -80 mV (inferred). Light level for the Table 3
ratio: "projected" from intensity-response curves, so the high-irradiance
limit; this mapping is my reading of the table caption (inferred).

Acceptance rule, set before writing the tests: a model value passes if it lies
within mean +/- 2 SD, with SD = SEM * sqrt(n). The exploratory run had been
seen when this rule was chosen; the rule is the conventional one and was not
tuned to the result.
"""
import math


def sd_range(mean, sem, n, k=2.0):
    sd = sem * math.sqrt(n)
    return (mean - k * sd, mean + k * sd)


LIN2009_WT = {
    "ratio": sd_range(0.215, 0.023, 7),
    "tau_off_500ms": sd_range(13.54, 1.39, 7),
    "tau_off_10ms": sd_range(13.39, 1.05, 7),
}

LIN2009_H134R = {
    "ratio": sd_range(0.387, 0.019, 7),
    "tau_off_500ms": sd_range(17.92, 1.37, 7),
    "tau_off_10ms": sd_range(17.96, 1.18, 7),
}

# Lin 2009 measured 13.39 vs 13.54 ms (ratio 0.99). Model passes if the
# 10 ms / 500 ms closing tau ratio lies in [0.8, 1.25].
DURATION_INDEPENDENCE = (0.8, 1.25)

# Brief 03, section 6: peak current agreement within 10%.
PEAK_TOLERANCE = 0.10
FIVE_IRRADIANCES = [0.5, 1.0, 2.0, 5.0, 10.0]  # mW/mm^2
NORM_IRRADIANCE = 19.8  # mW/mm^2, used for shape-only comparisons
V_LIN = -80.0  # mV, inferred holding potential
