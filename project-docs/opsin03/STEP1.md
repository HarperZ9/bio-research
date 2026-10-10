# Project 03, step 1: ChR2 kinetic model and validation

Date: 2026-10-09. Brief: `project-docs/briefs/03-optogenetics-circuit-models.md`, section 6 step 2.

## Result first

- Built: 4-state and 6-state ChR2 models in plain NumPy/SciPy, voltage clamp, square light pulses. Equations and parameters follow PyRhO at a pinned commit.
- Controls pass: zero current with no light, state occupancy conserved, integration matches the analytic steady state, peaks rise monotonically from 0.01 to 19.8 mW/mm2 and saturate.
- The brief's 10% peak-agreement criterion fails, three ways. The 6-state peak is 77 to 79% smaller than the 4-state peak in absolute terms. The 4-state normalised peak curve differs from the NEURON Williams model by up to 25% at low light. Only the normalised 4-state vs 6-state shapes agree (largest gap 9.1% at 0.5 mW/mm2).
- Against Lin et al. 2009 wild-type ChR2: the closing time constant passes, and the steady-state to peak ratio fails (model 0.37 to 0.38, range 0.09 to 0.34). The model ratio sits inside the H134R range. The model's closing time constant depends on pulse duration (8 ms after 10 ms, 17 ms after 500 ms), while Lin reports no duration dependence.
- Inference, moderate confidence: the PyRhO default ChR2 set behaves more like ChR2(H134R) than wild type on these two measures. PyRhO does not name its fitted dataset, so this is unconfirmed.

Does not prove: the controls show the code solves the stated equations. They do not show that the equations describe ChR2 in a neuron. Matching one paper's ratio and tau ranges would not validate the light dependence of the kinetics either.

## What was built

| File | Content |
|---|---|
| `src/opsin03/params.py` | PyRhO 4-state and 6-state ChR2 parameter sets with provenance |
| `src/opsin03/chr2.py` | Rate matrices, f(V) rectification, photocurrent, analytic steady state, pulse simulation (LSODA, rtol 1e-9, segments split at light edges) |
| `src/opsin03/metrics.py` | Peak, plateau, ratio, single-exponential tau_off, model-free t_1/e |
| `src/opsin03/reference.py` | Lin 2009 values, acceptance rule, brief tolerance |
| `scripts/opsin03_neuron_williams.py` | Runs ModelDB 244414 in NEURON (WSL), writes `data/opsin03/neuron_williams.json` |
| `scripts/opsin03_step1_numbers.py` | Regenerates `data/opsin03/step1_numbers.json`, the numbers quoted here |
| `tests/test_opsin03_chr2.py`, `tests/test_opsin03_reference.py` | 25 checks |

Environment: Windows venv `H:\bio-data\venvs\opsin` (Python 3.12.10, numpy 2.5.3, scipy 1.18.1, pytest 9.1.1). NEURON comparison in WSL Ubuntu 24.04 venv `/mnt/h/bio-data/venvs/opsin-wsl` (Python 3.12.3, neuron 9.0.2, numpy 2.5.3, scipy 1.18.1). Brian2 was not used; the models are linear ODEs and SciPy is enough and easier to inspect.

Run: `H:/bio-data/venvs/opsin/Scripts/python -m pytest tests/test_opsin03_chr2.py tests/test_opsin03_reference.py -rxX` (about 1.5 s).

## Parameter provenance

- Repo: https://github.com/ProjectPyRhO/PyRhO, BSD-3-Clause.
- File: `pyrho/parameters.py` at commit `dade008ad2f9d18cf7c3b26782b7063e1a597e40` (master on 2026-10-09; commit date 2023-07-24). sha256 of the fetched file `b7ae6fb552d683f386d7477e774a9e6d0b29b88f55b6691967994304ef219acc`.
- Sets used: `modelFits['4']['ChR2']` (lines 179 to 196) and `modelFits['6']['ChR2']` (lines 199 to 218). Equations from `pyrho/models.py` at the same commit (sha256 `d029dfdce9e1c9dbc59de08ea830d5df87cbb74c604c009dffcd418f13152e1f`), classes `RhO_4states` and `RhO_6states`. Irradiance to flux uses `utilities.irrad2flux` (470 nm).
- Discrepancy with the brief: the brief's 6-state row (g0 2.76e4, phi_m 5.07e17, k1 18.5, and others) comes from Table 3 of the PyRhO paper. `parameters.py` at this commit carries a different 6-state set (g0 2.52e4, phi_m 3.54e17, k1 13.4, k2 2.71, p 0.985, Go1 2, Go2 0.0567, Gd1 0.112, Gd2 0.0185, gam 0.0161). Step 1 uses the file, as instructed. The 4-state values match the brief.
- Neither source names the fitted ChR2 variant or dataset.

## Results

Holding potential -70 mV unless noted. Pulses 50 ms for peak sweeps, 500 ms and 10 ms for the Lin protocol.

### (a) 4-state vs 6-state, five irradiances

| Irradiance (mW/mm2) | 0.5 | 1 | 2 | 5 | 10 |
|---|---|---|---|---|---|
| 4-state peak (nA) | 1.917 | 2.745 | 3.684 | 4.911 | 5.693 |
| 6-state peak (nA) | 0.396 | 0.606 | 0.847 | 1.148 | 1.320 |
| Absolute gap, % of 4-state | 79.3 | 77.9 | 77.0 | 76.6 | 76.8 |
| Normalised to 19.8 mW/mm2, gap % | 9.1 | 2.9 | 1.1 | 2.8 | 1.9 |

The absolute test fails (strict xfail). Most of the gap is g0: 1.14e5 vs 2.52e4 pS, a factor of 4.5. The two sets were fitted with independent scale. The shape test passes, with 0.5 mW/mm2 close to the limit.

### (b) Lin et al. 2009, wild-type ChR2

Source: Lin JY, Lin MZ, Steinbach P, Tsien RY. 2009. Biophys J 96:1803. doi:10.1016/j.bpj.2008.11.034, full text read at https://pmc.ncbi.nlm.nih.gov/articles/PMC2717302/ on 2026-10-09 (DOI checked against Europe PMC). HEK293 cells, room temperature, 470 nm. Table 3, ChR2 (n = 7, mean and SEM): plateau/max 0.215 +/- 0.023; closing tau 13.39 +/- 1.05 ms after a 10 ms pulse and 13.54 +/- 1.39 ms after a 500 ms pulse. Fig. 1 text gives a plateau of 23.0% +/- 1.4% (n = 11).

Acceptance rule: mean +/- 2 SD, with SD = SEM x sqrt(n). I chose this rule after seeing the exploratory run. It is the conventional rule and was not tuned; the ratio still fails under it. Protocol: 19.8 mW/mm2, the top irradiance Lin used, and -80 mV. I inferred the holding potential from the stated driving force of about 87 mV and E_rev of about 8 mV. The paper text I read does not state it.

| Measure | 4-state | 6-state | WT range | H134R range (Lin Table 3) | Result |
|---|---|---|---|---|---|
| Plateau/peak, 500 ms | 0.380 | 0.366 | 0.093 to 0.337 | 0.286 to 0.488 | FAIL (xfail) |
| tau_off after 500 ms (ms) | 16.6 | 16.7 | 6.2 to 20.9 | 10.7 to 25.2 | pass |
| tau_off after 10 ms (ms) | 8.2 | 8.0 | 7.8 to 18.9 | 11.7 to 24.2 | pass, near the lower edge |
| tau 10 ms / tau 500 ms | 0.49 | 0.48 | 0.8 to 1.25 (Lin: 0.99) | | FAIL (xfail) |

The ratio at 9.7 mW/mm2 is 0.384 (4-state) and 0.359 (6-state), so the failure does not depend on the irradiance chosen. The duration dependence comes from the biexponential off kinetics (Gd1 0.105 and Gd2 0.0138 ms^-1). A short pulse leaves most channels in O1, which closes fast. A long pulse loads O2, which closes slowly.

### (c) No-light control

Both models give exactly 0 nA for 500 ms with no light, and all occupancy stays in C1. The NEURON model also gives exactly 0 with no light. Pass.

### (d) Irradiance scaling

Sweep from 0.01 to 1e5 mW/mm2, one point per decade, 50 ms pulses. 4-state peak: 0.117, 0.683, 2.745, 5.693, 6.849, 7.077, 7.146, 7.157 nA. Monotonic and saturating. Pass.

6-state peak: 0.0133, 0.113, 0.606, 1.320, 1.463, 1.396, 1.392, 1.392 nA. It saturates but falls 5% after 100 mW/mm2. The result does not change at dt 0.001 ms, so it comes from the parameter set: light-driven Gf moves channels into the low-conductance O2 state faster. The full-range monotonic test fails for the 6-state set (strict xfail). I added a narrower test after seeing this, 0.01 to 19.8 mW/mm2, and both models pass it. It is labeled post hoc in the test.

### Implementation checks

- Occupancy sums to 1 within 1e-6, and no state goes below -1e-9.
- After 10 s of light at 5 mW/mm2, the integrated states match the generator's null vector within 1e-4.
- At 1 mW/mm2 and 470 nm, the photon flux is 2.366e15 photons mm^-2 s^-1.

## ModelDB 244414 (Williams et al. 2013, ChR2-H134R, NEURON)

The model downloaded and ran. Zip from https://modeldb.science/download/244414, sha256 `12349d0d919a7398a0f6616a29fa2fd17432818858cda1283d8b687fb7df73f2`, stored at `H:\bio-data\opsin03\modeldb244414` and not committed. The readme states no license. `ChR2H134R.mod` compiled with nrnivmodl (NEURON 9.0.2, WSL). Protocol: SEClamp, 22 C, 500 ms pulses, dt 0.01 ms. Output: `data/opsin03/neuron_williams.json`.

Absolute currents cannot be compared. Williams reports mA/cm2 from gmax 0.4 mS/cm2, and PyRhO reports nA per cell from g0 in pS. The test therefore compares shape only, with peaks normalised to 19.8 mW/mm2.

| Irradiance (mW/mm2) | 0.5 | 1 | 2 | 5 | 10 |
|---|---|---|---|---|---|
| Williams normalised peak | 0.405 | 0.564 | 0.716 | 0.870 | 0.948 |
| PyRhO 4-state normalised peak | 0.306 | 0.438 | 0.587 | 0.783 | 0.908 |
| Gap, % of Williams | 24.5 | 22.4 | 17.9 | 10.0 | 4.3 |

The test fails (strict xfail). Williams saturates at lower light. Other differences, read from the same runs:
- Williams plateau/peak rises with light, from 0.405 at 0.5 to 0.515 at 19.8 mW/mm2. PyRhO falls with light, from 0.52 to 0.38.
- Williams tau_off is 9.9 ms after 500 ms and 8.5 ms after 10 ms, a ratio of 0.86. It changes little with duration.
- Williams vs Lin H134R: the ratio of 0.515 at 19.8 mW/mm2 lies outside Lin's H134R range (0.29 to 0.49), and tau_off of 9.9 ms lies below it (10.7 to 25.2). These two H134R sources disagree with each other. Lin and Williams used different labs, cells and fitting.

## Disagreements and open items

1. PyRhO 4-state vs 6-state absolute amplitude: a factor of 4.5. Before the network step, choose one set and set g0 per neuron from a target current density, not from either file.
2. PyRhO ChR2 vs Lin WT: the ratio is too high and the closing tau depends on duration. Either the set is H134R-like, or it was fitted to another protocol. Unknown which.
3. PyRhO vs Williams: light dependence differs (saturation point, and the sign of the ratio trend).
4. The brief's 10% criterion is not met. Per section 6, the brief says to exit if the models disagree beyond 10%. My recommendation, for the operator to decide: the circuit step should not rely on one ChR2 parameter set. Run both PyRhO and a Python port of Williams and report results that differ between them as model-dependent.
5. The 6-state peak falls above 100 mW/mm2. That level lies above typical slice irradiance, but fiber tips can reach it in vivo.

## What step 2 needs (chloride pump, validated on Raimondo et al. 2012)

- Raimondo JV et al. 2012, Nat Neurosci, doi:10.1038/nn.3143, in full text: cell type, light power and duration, measured [Cl-]i or E_GABA shift, and how long the post-light effect on evoked spiking lasts. The brief lists the abstract only; I did not open this paper in this step (UNVERIFIED beyond the brief).
- A verified NpHR and Arch (or ArchT) kinetic set. The PyRhO 3-state NpHR and ArchT entries look like placeholders (brief section 2a). The candidate is digitized curves from Zhang 2007 (doi:10.1038/nature05744), Chow 2010 (doi:10.1038/nature08652) and Mattis 2011 (doi:10.1038/nmeth.1808), with each digitization stored as a data file that cites its figure.
- A pump current model: a light-driven current with no reversal potential (PyRhO uses E = -400 mV as a stand-in), converted to a Cl- influx with Faraday's constant and a cell volume.
- Intracellular Cl- dynamics: a single compartment with volume, a KCC2 extrusion time constant from a cited source, and E_GABA from Nernst (or GHK with HCO3-).
- A single-compartment neuron with a GABA-A synapse and an evoked-spike protocol, plus a proton-pump control with no Cl- coupling. The test: increased post-light spiking with the Cl- pump, and none with the proton pump. The model must not be fit to that result.
- Lock all parameters and commit a hash before reading Raimondo's effect sizes, as section 5 of the brief requires.

## Lead decision, 2026-10-10

The 10% agreement exit criterion fired. Decision: do not exit; carry both ChR2 parameter sets (PyRhO file at dade008 and a Python port of Williams 2013) into the circuit step. Any circuit-level prediction that changes direction or rank between the two sets is reported as model-dependent, not as a prediction. Reason: the disagreement is itself the step-1 finding, and choosing one set would hide it.
