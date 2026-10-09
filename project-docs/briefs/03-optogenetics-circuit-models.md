# Brief 03: Optogenetic circuit models of fear extinction (amygdala-PFC)

Date: 2026-10-09. Method: research synthesis (anchor, read, classify, extract framework, fill gaps with labeled inference, lead with result).
Verification: every DOI below was resolved through the Crossref API and, for most, the abstract was read in Europe PMC. Items marked UNVERIFIED were not opened. Confidence labels: high / moderate / low / unknown.

## Result first

1. The best-posed, model-testable question in the literature is dose dependence. Bukalo et al. 2021 [R22] varied ChR2 titer in IL neurons and stimulated their BLA terminals during partial extinction: low titer no effect, medium titer facilitated extinction memory, high titer produced acute fear suppression plus lower fear at light-free retrieval. A model with opsin kinetics, a light field, and plasticity should reproduce a non-monotonic dose-response without being fit to it. (high that the paper reports this; effect sizes unknown, I read only the abstract)
2. A second discriminating target is a literature conflict. Do-Monte 2015 [R19] found IL silencing (halorhodopsin) at retrieval had no effect, while Kim 2016 [R20] found IL inactivation impaired extinction retrieval. Opsin choice, light dose, and Cl- loading are candidate explanations that a kinetic model can rank. (moderate; the explanation is my inference)
3. No open model combines opsin kinetics with an amygdala-PFC extinction network. I found opsin models (ModelDB 244414, PyRhO) and amygdala fear models (ModelDB 150288, 142273; Duggins 2024), none joined. Building the join is the first modeling step. (moderate; ModelDB text search is weak, see section 4)
4. Human translation of optogenetics itself is one retinal program. Fear-circuit translation runs through TMS, DBS, and focused ultrasound, and only TMS has a controlled extinction result (Raij 2018, N=28). (high)

## 1. Question and the decision it informs

Question: can a model that couples opsin photocurrent kinetics to a BLA/CeA/IL/PL network make quantitative predictions about optogenetic effects on fear expression and extinction that a rodent lab can test, and that were not used to fit the model?

Decision it informs: whether to invest bench time (virus titer series, light-power series, projection-specific stimulation) in a prediction-first design, and which experiment to run first. Secondary decision: which human neuromodulation targets (vmPFC TMS, BLA DBS, amygdala ultrasound) deserve model-guided parameter choices. The model is a hypothesis generator. It does not support clinical claims.

## 2. State of evidence

### 2a. Opsin biophysics and kinetic models

Model families (all conductance-based, light drives state transitions):
- 3-state ChR2: closed/open/desensitized, C+O+D=1, photocycle factor equals O (PyRhO paper [R5]). Fast to simulate, cannot reproduce biphasic decay or two open states.
- 4-state ChR2: C1, O1, O2, C2 with light-dependent k1, k2 and thermal transitions Gd1, Gd2, Gf, Gb, Gr. Attributed to Nikolic et al. 2009 [R3]. Williams 2013 [R4] adapted it with voltage-dependent G(V), Gr, Gd1 and fitted ChR2(H134R) in HEK293 cells.
- 6-state ChR2: adds two states, used for the best fits to photocurrent families (PyRhO [R5], Table 3).
- Step-function and bistable opsins (C128 mutants) need a long-lived open state; no Markov parameter set for them was located in this pass.

Published or distributed parameters I could read:

| Model | Parameters (units ms^-1 unless noted) | Source and confidence |
|---|---|---|
| ChR2 4-state, PyRhO default | g0 1.14e5 (pS scale), gam 0.00742, phi_m 2.33e17 ph/mm2/s, k1 4.15, k2 0.868, p 0.833, Gf0 0.0373, kf 0.0581, Gb0 0.0161, kb 0.063, q 1.94, Gd1 0.105, Gd2 0.0138, Gr0 0.00033, E 0 mV, v0 43 mV, v1 17.1 mV | Read from `pyrho/parameters.py` in the PyRhO repo [R6]. The file does not state which dataset was fitted. Origin: moderate (PyRhO paper credits Nikolic 2009 for the structure). Values: high (read directly). |
| ChR2 6-state, PyRhO "experimental" set | g0 2.76e4, phi_m 5.07e17, k1 18.5, k2 3.75, p 0.982, Gf0 0.0365, kf 0.121, Gb0 0.0146, kb 0.133, q 1.45, Go1 1.93, Go2 2.65, Gd1 0.108, Gd2 0.0111, Gr0 0.00033 | PyRhO paper Table 3 [R5]. These generated synthetic verification data from ChR2 fits (high that they are listed; they are not an independent ChR2 recording). |
| ChR2 3-state | Gd 0.104, Gr0 0.0002, k_a 5, k_r 0.1, p 0.8, q 0.25, phi_m 5e17 | `parameters.py` [R6]. Moderate. |
| NpHR and ArchT 3-state, PyRhO | NpHR: E -400 mV, Gd 0.1, phi_m 1.32e18; ArchT: E 0 mV, Gr0 0.001. Both share g0, k_a, k_r, p, q, phi_m | Same file. Both entries share identical numbers apart from E and Gr0 and look like starting values, not fits to Zhang 2007 [R9] or Chow 2010 [R10]. Treat as placeholders. Inference, low confidence. |
| ChR2(H134R), Williams 2013 | Fitted in stable HEK293 line, 22 C, holding -80 to -10 mV, 0.34 to 5.5 mW/mm2 at 470 nm, reversal 0 mV, Q10 scaling to 37 C | Text of [R4]; numeric Table 1 is an image and I could not read it. Parameter values: unknown from this pass. Implemented in NEURON as ModelDB 244414 [R11]. |

Opsin properties from primary papers (abstract or full text read):
- Arch: photocurrents of several hundred pA at low power, approaching 900 pA at in vivo-feasible power, spontaneous recovery from inactivation, unlike chloride pumps [R10]. (high)
- ChRmine: about 4 nA inward photocurrent at 585 nm, EPD50 0.03 +/- 0.01 mW/mm2, 100% spike success at 1 ms and 0.08 mW/mm2, half-recovery from desensitization 0.63 +/- 0.08 s [R7]. Off-time constant: not found in the text I read. (high for stated numbers). Structure and faster variants: [R8].
- GtACRs: chloride-conducting channels with higher light sensitivity than pumps [R12]. Soma-targeting reduces axonal excitation caused by an excitatory axonal chloride reversal [R13]. A parallel-photocycle rate model for GtACR1 exists [R14]; I did not read its rate values. No Markov parameter table usable in a neuron model was verified (unknown).
- Step-function opsins: C128 mutants convert a brief pulse into a stable step [R15]. The ChR2(C128S/D156A) variant has a decay time constant near 29 min per a patent restatement of a Yizhar 2011 figure legend [R16]; I did not open the figure itself (low to moderate).
- Cross-opsin comparison under matched conditions: Mattis 2011 [R17] is the right source for a figures-of-merit table; I did not extract its numbers.

Gap: there is no single peer-reviewed parameter table covering ChR2, ChRmine, NpHR, Arch, and GtACR under one protocol. Building one means digitizing [R17] and the primary papers. That is a labeled inference step in section 6.

### 2b. Rodent optogenetic findings

Amygdala:
- LA pyramidal cell ChR2 activation paired with a tone can substitute for shock and instruct fear learning [R18, Johansen 2010]. (high)
- BA neurons form distinct fear and extinction populations whose switching depends on hippocampal and mPFC input [R21, Herry 2008, abstract read]. A BA subpopulation projecting to PL is active in high fear, while BA neurons projecting to IL are recruited with extinction and show plasticity [R23, Senn 2014]. (high)
- CeA inhibitory microcircuits encode conditioned fear [R24 Ciocchi 2010; R25 Haubensak 2010]. DOIs verified; I read titles only for these two (moderate on content).
- BLA holds antagonistic negative and positive excitatory populations with mutual inhibition [R26 Kim 2016]; an extinction engram sits in the reward-linked BLA population [R27 Zhang 2020]. (high)

Cortex:
- IL ChR2 activation during extinction training reduced fear and strengthened extinction memory next day; silencing with halorhodopsin during training impaired retrieval next day; silencing during retrieval at 1 day or 1 week had no effect [R19 Do-Monte 2015]. (high)
- Opposite on retrieval: IL (not PL) inactivation impaired extinction retrieval, and IL photostimulation enhanced post-extinction fear inhibition in a CS-specific way, but not before extinction [R20 Kim 2016]. (high) This is the disagreement named in Result 2.
- PL L5/6 pyramidal cells project to IL L5/6 and activating that link enhanced extinction, which complicates the PL=expression, IL=extinction dichotomy [R28 Marek 2018]. (high)
- PL parvalbumin interneuron phasic inhibition causes disinhibition and fear expression via theta resetting [R29 Courtin 2014]; 4 Hz prefrontal-amygdala oscillations track freezing, and optogenetic induction of PFC 4 Hz coordinates the circuit [R30 Karalis 2016]. (high)

Projections:
- Optogenetic high-frequency stimulation of BLA inputs to mPFC depresses those synapses, attenuates cue responses in mPFC, and facilitates extinction [R31 Klavir 2017]. (high)
- IL to BLA terminal photostimulation facilitated next-day extinction without changing in-session freezing, while IL somatic stimulation lowered freezing immediately but not next day [R32 Hong and Kim 2017]. (high, abstract)
- IL to BLA titer series [R22]. Chemogenetic data show extinction raises IL-BLA excitability [R33 Bloodgood 2018]. (high)

Shared framework (extracted): valence-opposed BLA populations gated by PL/IL inputs, with a CeA output stage, where extinction writes a new inhibitory trace in IL-linked BA/BLA cells. Opsin experiments differ along four axes that the model can parameterize: target compartment (soma vs terminal), opsin class (channel vs pump vs anion channel), dose (titer, power, duty cycle), and timing (training vs retrieval).

### 2c. Translation to humans

Clinical optogenetics:
- Retina only. One patient with retinitis pigmentosa received ChrimsonR AAV plus camera goggles and showed partial visual recovery [R34 Sahel 2021]. n=1, not controlled. (high)
- The GS030 PIONEER study (NCT03326336) is Phase 1/2a, listed ACTIVE_NOT_RECRUITING, status verified 2026-02, last update posted 2026-03-02, read from the ClinicalTrials.gov API today [R35]. I found no efficacy publication in this pass. (high for status, unknown for results)
- No optogenetic trial for a psychiatric indication was found. (moderate; absence in a limited search)

Non-optogenetic routes informed by these circuits:
- TMS: IL-inspired brief 20 Hz trains (300 ms, 4 trains) to a vmPFC-connected cortical target during extinction learning reduced skin conductance at day-3 recall in N=28; the unconnected control target did not [R36 Raij 2018]. This is the closest direct rodent-to-human transfer of an IL stimulation result. (high; single study)
- DBS: a BLA DBS trial protocol for combat PTSD exists [R37 Koek 2014]; a 2019 conference abstract reports the first two cases [R38]. I found no outcome data beyond that. (unknown efficacy)
- Focused ultrasound: a 2025 review addresses low-intensity transcranial ultrasound of the amygdala [R39 Mundorf 2025]. I read the title only. Efficacy for fear or trauma: unknown from this pass.
- Human extinction anatomy: vmPFC activation at extinction recall [R40 Milad 2007], amygdala and vmPFC roles [R41 Phelps 2004].

## 3. Open disagreements and known artifacts

- IL necessity at retrieval: R19 vs R20 conflict (above). Candidate causes: opsin (NpHR vs other), light dose and duration, Cl- loading, extinction protocol, strain. Mechanism not established.
- Heating: illumination raised temperature 0.2 to 2 C in common protocols and suppressed spiking in several regions; in striatum light activated an inwardly rectifying K conductance and biased rotation, with no opsin [R42 Owen 2019]. High-intensity fiber light elevated firing locally without opsin expression, and a light-heat model was validated [R43 Stujenske 2015]. (high) Williams 2013 estimated only 0.013 C for a single 90 ms pulse at 5.5 mW/mm2 [R4], which does not transfer to long continuous in vivo illumination. (high)
- Inhibition artifacts: chloride-pump silencing raised the probability of evoked spiking after photoactivation via a shift in GABA-A reversal, not seen with a proton pump [R44 Raimondo 2012]. At terminals, sustained Arch increased spontaneous release and chloride-conducting channelrhodopsins triggered release at light onset [R45 Mahn 2016]. Review of silencing constraints: [R46 Wiegert 2017]. (high)
- Dose: R22 shows effect sign and size depend on titer. Many studies report no titer, so cross-study comparison is weak. (high)
- Homology: rodent PL/IL versus human dACC/vmPFC. Rodent PFC nomenclature and boundaries are inconsistent across atlases, and human and rodent PFC research have different foci [R47 Laubach 2018]. The vmPFC role in fear, emotion and value spans several functions [R48 Hiser and Koenigs 2018]. Raij 2018 [R36] used functional connectivity to a putative IL homologue, which is a method, not proof of homology. (high that the debate exists; resolution: unknown)
- Model-side: PL vs IL labels in a model are inherited from rodent literature; any mapping to human TMS targets adds an unverified step.

## 4. Resources

Reachability checked 2026-10-09 by HTTP request (curl or WebFetch). "Read" means content inspected.

| Resource | URL | License | Reachable today |
|---|---|---|---|
| ModelDB 244414, ChR2-H134R, Williams 2013 (NEURON) | https://modeldb.science/244414 | Not stated in the API record; unknown, check the download's readme | Yes, page and API HTTP 200 |
| ModelDB 153196, ChR2 pyramidal neuron with fiber-optic light model, Foutz 2012 (NEURON, Python) | https://modeldb.science/153196 | Unknown | Yes, API HTTP 200 (page not separately fetched) |
| ModelDB 150288, 1000-cell lateral amygdala, Kim 2013 (NEURON) | https://modeldb.science/150288 | Unknown | Yes, page and API 200 |
| ModelDB 142273, FRAT fear model, Krasne 2011 (MATLAB) | https://modeldb.science/142273 | Unknown | Yes, API 200 |
| ModelDB API | https://modeldb.science/api/v1/models/ID | Unknown | Yes. Its text search returned empty results for "fear" and "extinction", so absence of a Li 2009 or Vlachos 2011 entry is unconfirmed |
| PyRhO | https://github.com/ProjectPyRhO/PyRhO | BSD-3-Clause (API) | Yes; last push 2023-07-24, not archived. PyPI 0.9.4 dated 2016-03-04 |
| Duggins and Eliasmith 2024 spiking amygdala model | https://doi.org/10.1111/ejn.16338 | Paper CC BY 4.0 (Crossref) | Paper DOI resolves; code repository NOT found (publisher page returned 403, lab page lists no code). Unknown |
| Mattera 2020 cued fear/extinction/reinstatement model | https://doi.org/10.3389/fnsys.2020.569108 | Paper CC BY 4.0 (Crossref) | DOI resolves; code location unknown |
| Vlachos 2011 basal amygdala network | https://doi.org/10.1371/journal.pcbi.1001104 | Paper CC BY (Crossref) | DOI resolves; code location unknown |
| Li, Nair, Quirk 2009 LA model | https://doi.org/10.1152/jn.90765.2008 | Unknown | DOI resolves; no code found |
| Allen Mouse Brain Connectivity | https://brain-map.org/connectivity | Allen Institute Terms of Use, noncommercial research use, citation policy (terms page read; not CC BY) | Yes, HTTP 200 |
| Allen Cell Types Database | https://celltypes.brain-map.org/ | Same terms | Yes, HTTP 200 |
| Allen API | http://api.brain-map.org/api/v2/ | Same terms | Yes, HTTP 200 |
| Brian2 | https://github.com/brian-team/brian2 | License file present ("License for Brian2"); text not read | Yes, active (push 2026-10-09) |
| NEURON | https://github.com/neuronsimulator/nrn | Not confirmed (my guessed LICENSE path returned 404) | Yes, active |
| Nengo | https://github.com/nengo/nengo | Custom "Nengo license"; text not read | Yes |
| NEST | https://github.com/nest/nest-simulator | GPL-2.0 per GitHub API | Yes |

Opsin parameter tables: no standalone open table exists beyond PyRhO's `parameters.py` and Table 3 of [R5]. Data tables in [R17] need manual extraction.

## 5. Verifier design

A model result counts only if it predicts a quantity, with sign and rough magnitude, that was not used to set any model parameter, and that a published experiment measured.

Required outputs from the model, per virtual animal:
- Opsin level: peak and steady photocurrent vs irradiance, desensitization, recovery, and (for pumps and ACRs) intracellular Cl- change during and after the light.
- Tissue level: irradiance by depth and temperature rise by duty cycle, so the heat-only effect can be run in opsin-free control runs.
- Circuit level: BLA fear-cell vs extinction-cell rates, CeA output rate (freezing proxy), and an extinction-memory variable (weight of IL to extinction cells) at next-day retrieval.

Candidate hold-out tests, ranked:
1. Titer series, Bukalo 2021 [R22]. Predict the ordering and the non-monotonic shape (no effect, facilitation, acute suppression plus later benefit). Freeze all parameters, write predictions with a hash before extracting effect sizes from the paper. Risk: titer maps to opsin density and axonal coverage only through my assumption.
2. Terminal vs soma stimulation, Hong and Kim 2017 [R32]. Predict immediate freezing drop with somatic IL drive, delayed benefit with terminal BLA input drive. The model must produce the dissociation from plasticity timing, not from a built-in rule.
3. R19 vs R20 retrieval conflict. Predict whether silencing IL at retrieval impairs recall under (a) halorhodopsin-like Cl- pump with post-light rebound and (b) a proton pump or ACR. Check against both papers' protocols.
4. Opsin-level hold-out: Raimondo 2012 [R44] reports increased post-light evoked spiking with a Cl- pump but not a proton pump. A model with dynamic E_GABA should reproduce this without being fit to it. Cheap and decisive for the opsin-plus-chloride module.
5. Heat control: Owen 2019 [R42] spiking suppression at 0.2 to 2 C. The model should predict suppression at those temperatures from a temperature-dependent conductance term; this tests the heat module only if that module is not tuned on [R42].

False-pass guards: run every virtual experiment with opsin density zero (heat and light only) and with randomized plasticity rules; require the dose-response shape to vanish with those controls. A model that reproduces the shape without the opsin kinetics is not testing them.

## 6. First modeling plan (one workstation, WSL Ubuntu, Python)

Time budget is days of compute, not weeks. All steps are inference-labeled design, not published procedure.

1. Environment. WSL Ubuntu, Python 3.11 venv, `pip install brian2 numpy scipy pandas joblib`. Skip PyRhO as a dependency (last PyPI release 2016, Python 3 install notes mention compiling NEURON); copy its parameter dictionaries into a local file with a citation header. Log package versions.
2. Opsin module (Brian2 equations). Implement the 4-state ChR2 model with the PyRhO default set. Unit tests: (a) onset, steady-state ratio and recovery in response to a 1 s step and paired pulses; (b) irradiance scaling; (c) compare against the 6-state set and against ModelDB 244414 run in NEURON for the same protocol. Pass criterion: peak current within 10% of the NEURON model across five irradiances. Exit if the two disagree beyond that.
3. Inhibitory module. Add (a) a Cl- pump with dynamic intracellular Cl- and a GABA-A reversal tied to it, (b) a proton pump, (c) a light-gated anion channel. Pump and ACR parameters are not available in a verified table; fit to digitized curves from [R9], [R10], [R12], [R17], and record every digitization as a data file with its figure reference. Validate with the Raimondo 2012 effect (verifier 4) and then lock.
4. Light and heat. 1D depth profile: exponential attenuation with a literature scattering coefficient, inverse-square fiber spread, and a lumped temperature rise proportional to absorbed power, constrained to the 0.2 to 2 C range in [R42] and the model of [R43]. Temperature enters as a Q10 on membrane conductances. Document that this is a reduced model of [R43].
5. Network skeleton. About 2,000 AdEx neurons: BLA (fear cells, extinction cells, interneurons; Herry/Senn/Kim 2016 organization), CeA (CeL on/off, CeM output), PL, IL (E plus PV), with reciprocal BLA-PL/IL links. Start from Vlachos 2011 [R50] and Duggins 2024 [R49] for nucleus structure and plasticity, with the three-factor rule on IL to BLA extinction cells. Reproduce acquisition and extinction (freezing proxy = CeM rate) with no opsin. Calibrate to published qualitative phenomena only: acquisition, extinction, spontaneous recovery, renewal.
6. Couple. Per-neuron opsin conductance from a lognormal expression distribution times a titer scalar; projection-specific expression for IL to BLA terminals; light field from step 4.
7. Freeze, then predict. Write a prediction file (shape of dose-response, sign of next-day effect for soma vs terminal, retrieval silencing outcome by opsin class) and commit its hash before reading effect sizes from [R22], [R32], [R19], [R20].
8. Sweeps. Titer (6 levels) x irradiance (5) x duration (3) x seeds (20) = 1,800 runs; Brian2 with Cython codegen, one process per core via joblib, 22 workers. Expect minutes per 60 s virtual run at this size (low confidence on timing; benchmark one run first).
9. Controls. No-opsin heat-only, random-plasticity, and sham-light runs on every sweep.
10. Compare to hold-outs, report match and mismatch, including negative results, and list parameters that would need to change to fit (that is a refit, record it as one).

## 7. Does not prove, and risks

Does not prove:
- That a model reproducing dose-response shape identifies the mechanism; several mechanisms (plasticity timing, E/I shift, heat) can give non-monotonic curves.
- That any rodent circuit result will carry to humans. R36 is one TMS study with N=28.
- Anything about a clinical benefit of optogenetics in psychiatry; none exists in the evidence I found.

Risks:
- Parameter provenance: PyRhO ChR2 values do not name a dataset, NpHR/ArchT entries look like placeholders, and ChR2(H134R) numeric Table 1 in Williams was unreadable. Mitigation: refit from digitized curves, version the data.
- Titer to model density mapping is an assumption, and Bukalo's effect sizes are unread.
- Light-heat model is reduced; no calibration against in vivo temperature.
- No open code found for Duggins 2024, Li 2009, or Vlachos 2011; rebuilding from papers risks drift from the originals.
- ModelDB licenses are unknown; check each download before redistribution. Allen data are noncommercial-use.
- Coverage: this pass opened abstracts and metadata, not every full text. Sources I read only as titles are noted above.
- Fear-extinction behavior in rodents is a proxy for trauma pathology in humans; PTSD heterogeneity is not modeled.

## 8. References

All DOIs resolved in Crossref on 2026-10-09 unless tagged. URLs opened as stated in section 4.

- R3 Nikolic K et al. 2009. Photocycles of channelrhodopsin-2. Photochem Photobiol. doi:10.1111/j.1751-1097.2008.00460.x
- R4 Williams JC et al. 2013. Computational optogenetics: empirically derived voltage- and light-sensitive ChR2 model. PLoS Comput Biol. doi:10.1371/journal.pcbi.1003220
- R5 Evans BD et al. 2016. PyRhO: a multiscale optogenetics simulation platform. Front Neuroinform. doi:10.3389/fninf.2016.00008
- R6 PyRhO repository. https://github.com/ProjectPyRhO/PyRhO (file pyrho/parameters.py)
- R7 Marshel JH et al. 2019. Cortical layer-specific critical dynamics triggering perception (ChRmine). Science. doi:10.1126/science.aaw5202
- R8 Kishi KE et al. 2022. Structural basis for channel conduction in ChRmine. Cell. doi:10.1016/j.cell.2022.01.007
- R9 Zhang F et al. 2007. Multimodal fast optical interrogation of neural circuitry (NpHR). Nature. doi:10.1038/nature05744
- R10 Chow BY et al. 2010. High-performance genetically targetable optical neural silencing by light-driven proton pumps. Nature. doi:10.1038/nature08652
- R11 ModelDB 244414. https://modeldb.science/244414
- R12 Govorunova EG et al. 2015. Natural light-gated anion channels. Science. doi:10.1126/science.aaa7484
- R13 Mahn M et al. 2018. High-efficiency optogenetic silencing with soma-targeted anion-conducting channelrhodopsins. Nat Commun. doi:10.1038/s41467-018-06511-8
- R14 Szundi I, Kliger DS et al. 2024. Parallel photocycle kinetic model of anion channelrhodopsin GtACR1 function. Biophys J. doi:10.1016/j.bpj.2024.05.016
- R15 Berndt A et al. 2009. Bi-stable neural state switches. Nat Neurosci. doi:10.1038/nn.2247
- R16 Yizhar O et al. 2011. Neocortical excitation/inhibition balance in information processing and social dysfunction. Nature. doi:10.1038/nature10360 (29 min value via patent restatement, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10568307, figure itself UNVERIFIED)
- R17 Mattis J et al. 2011. Principles for applying optogenetic tools derived from direct comparative analysis of microbial opsins. Nat Methods. doi:10.1038/nmeth.1808
- R18 Johansen JP et al. 2010. Optical activation of lateral amygdala pyramidal cells instructs associative fear learning. PNAS. doi:10.1073/pnas.1002418107
- R19 Do-Monte FH et al. 2015. Revisiting the role of infralimbic cortex in fear extinction with optogenetics. J Neurosci. doi:10.1523/jneurosci.3137-14.2015
- R20 Kim HS et al. 2016. Selective control of fear expression by optogenetic manipulation of infralimbic cortex after extinction. Neuropsychopharmacology. doi:10.1038/npp.2015.276
- R21 Herry C et al. 2008. Switching on and off fear by distinct neuronal circuits. Nature. doi:10.1038/nature07166
- R22 Bukalo O et al. 2021. Effects of optogenetic photoexcitation of infralimbic cortex inputs to the basolateral amygdala on conditioned fear and extinction. Behav Brain Res. doi:10.1016/j.bbr.2020.112913 (PMC8299731)
- R23 Senn V et al. 2014. Long-range connectivity defines behavioral specificity of amygdala neurons. Neuron. doi:10.1016/j.neuron.2013.11.006
- R24 Ciocchi S et al. 2010. Encoding of conditioned fear in central amygdala inhibitory circuits. Nature. doi:10.1038/nature09559
- R25 Haubensak W et al. 2010. Genetic dissection of an amygdala microcircuit that gates conditioned fear. Nature. doi:10.1038/nature09553
- R26 Kim J et al. 2016. Antagonistic negative and positive neurons of the basolateral amygdala. Nat Neurosci. doi:10.1038/nn.4414
- R27 Zhang X et al. 2020. Amygdala reward neurons form and store fear extinction memory. Neuron. doi:10.1016/j.neuron.2019.12.025
- R28 Marek R et al. 2018. Excitatory connections between the prelimbic and infralimbic medial prefrontal cortex show a role for the prelimbic cortex in fear extinction. Nat Neurosci. doi:10.1038/s41593-018-0137-x
- R29 Courtin J et al. 2014. Prefrontal parvalbumin interneurons shape neuronal activity to drive fear expression. Nature. doi:10.1038/nature12755
- R30 Karalis N et al. 2016. 4-Hz oscillations synchronize prefrontal-amygdala circuits during fear behavior. Nat Neurosci. doi:10.1038/nn.4251
- R31 Klavir O et al. 2017. Manipulating fear associations via optogenetic modulation of amygdala inputs to prefrontal cortex. Nat Neurosci. doi:10.1038/nn.4523
- R32 Hong J, Kim D. 2017. Freezing response-independent facilitation of fear extinction memory in the prefrontal cortex. Sci Rep. doi:10.1038/s41598-017-04335-y
- R33 Bloodgood DW et al. 2018. Fear extinction requires infralimbic cortex projections to the basolateral amygdala. Transl Psychiatry. doi:10.1038/s41398-018-0106-x
- R34 Sahel JA et al. 2021. Partial recovery of visual function in a blind patient after optogenetic therapy. Nat Med. doi:10.1038/s41591-021-01351-4
- R35 ClinicalTrials.gov NCT03326336 (GS030). https://clinicaltrials.gov/study/NCT03326336 (status read via API v2)
- R36 Raij T et al. 2018. Prefrontal cortex stimulation enhances fear extinction memory in humans. Biol Psychiatry. doi:10.1016/j.biopsych.2017.10.022
- R37 Koek RJ et al. 2014. Deep brain stimulation of the basolateral amygdala for treatment-refractory combat PTSD (protocol). Trials. doi:10.1186/1745-6215-15-356
- R38 Basolateral amygdala DBS for treatment refractory combat PTSD: data from the first two cases. Brain Stimul 2019;12:429-430 (conference abstract). doi:10.1016/j.brs.2018.12.391 (authors garbled in Crossref)
- R39 Mundorf A et al. 2025. Low-intensity transcranial focused ultrasound neuromodulation of the amygdala. Mol Psychiatry. doi:10.1038/s41380-025-03319-z (title only read)
- R40 Milad MR et al. 2007. Recall of fear extinction in humans activates the ventromedial prefrontal cortex and hippocampus. Biol Psychiatry. doi:10.1016/j.biopsych.2006.10.011
- R41 Phelps EA et al. 2004. Extinction learning in humans. Neuron. doi:10.1016/j.neuron.2004.08.042
- R42 Owen SF et al. 2019. Thermal constraints on in vivo optogenetic manipulations. Nat Neurosci. doi:10.1038/s41593-019-0422-3
- R43 Stujenske JM et al. 2015. Modeling the spatiotemporal dynamics of light and heat propagation for in vivo optogenetics. Cell Rep. doi:10.1016/j.celrep.2015.06.036
- R44 Raimondo JV et al. 2012. Optogenetic silencing strategies differ in their effects on inhibitory synaptic transmission. Nat Neurosci. doi:10.1038/nn.3143
- R45 Mahn M et al. 2016. Biophysical constraints of optogenetic inhibition at presynaptic terminals. Nat Neurosci. doi:10.1038/nn.4266
- R46 Wiegert JS et al. 2017. Silencing neurons: tools, applications, and experimental constraints. Neuron. doi:10.1016/j.neuron.2017.06.050
- R47 Laubach M et al. 2018. What, if anything, is rodent prefrontal cortex? eNeuro. doi:10.1523/ENEURO.0315-18.2018
- R48 Hiser J, Koenigs M. 2018. The multifaceted role of the ventromedial prefrontal cortex in emotion, decision making, social cognition, and psychopathology. Biol Psychiatry. doi:10.1016/j.biopsych.2017.10.030
- R49 Duggins P, Eliasmith C. 2024. A scalable spiking amygdala model that explains fear conditioning, extinction, renewal and generalization. Eur J Neurosci 59:3093-3116. doi:10.1111/ejn.16338
- R50 Vlachos I et al. 2011. Context-dependent encoding of fear and extinction memories in a large-scale network model of the basal amygdala. PLoS Comput Biol. doi:10.1371/journal.pcbi.1001104
- R51 Mattera A et al. 2020. A computational model integrating multiple phenomena on cued fear conditioning, extinction, and reinstatement. Front Syst Neurosci. doi:10.3389/fnsys.2020.569108
- R52 Li G, Nair SS, Quirk GJ. 2009. A biologically realistic network model of acquisition and extinction of conditioned fear associations in lateral amygdala neurons. J Neurophysiol. doi:10.1152/jn.90765.2008
- R53 Kim D, Pare D, Nair SS. 2013. Assignment of model amygdala neurons to the fear memory trace depends on competitive synaptic interactions. J Neurosci. doi:10.1523/jneurosci.2430-13.2013
- R54 Krasne FB et al. 2011. Design of a neurally plausible model of fear learning. Front Behav Neurosci. doi:10.3389/fnbeh.2011.00041
- R55 Tye KM et al. 2011. Amygdala circuitry mediating reversible and bidirectional control of anxiety. Nature. doi:10.1038/nature09820 (not cited above; context only)
- R56 Namburi P et al. 2015. A circuit mechanism for differentiating positive and negative associations. Nature. doi:10.1038/nature14366 (context only)
- R57 Milad MR, Quirk GJ. 2002. Neurons in medial prefrontal cortex signal memory for fear extinction. Nature. doi:10.1038/nature01138 (context only)
- R58 Burgos-Robles A et al. 2017. Amygdala inputs to prefrontal cortex guide behavior amid conflicting cues of reward and punishment. Nat Neurosci. doi:10.1038/nn.4553 (context only)
