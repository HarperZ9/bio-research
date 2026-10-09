# Brief 02: Stress, glucocorticoids and activity-dependent grey matter change

Date: 2026-10-09. Register: research brief, flavored. Method: anchor, read, classify, extract framework, label inference.
Verification key: [V] = DOI resolved in Crossref and abstract read in Europe PMC today. [S] = seen only in a secondary source (search summary). [U] = UNVERIFIED (could not open a primary page). Claims from my own reasoning are tagged "inferred". Confidence: high / moderate / low / unknown.

## Result first

1. The human case for "stress or cortisol shrinks the hippocampus" rests on small cross-sectional samples plus a few treatment-reversal cohorts. The one large, preregistration-like consortium estimate is small: d = -0.17 for PTSD vs trauma-exposed controls (N = 1868) and d = -0.14 for MDD (N = 8927), about 1.2 to 1.4 percent volume (high, [V]).
2. Two designs argue that part of the effect is a pre-existing trait: monozygotic twins discordant for trauma (Gilbertson 2002) and a 5-year population cohort (Lindgren 2016, n = 111) found smaller hippocampi before stress and no differential change (high that these papers say so, [V]; moderate that this settles causation).
3. The best causal human evidence is Cushing's disease: hippocampal volume rose by a mean 3.2 percent after cortisol fell (n = 22, Starkman 1999, [V]). Uncontrolled, no water or motion control.
4. Training-induced grey matter change is real in some designs (taxi trainees over 3 to 4 years, exercise RCT with n = 120 at +2 percent), but the short-interval VBM literature has weak replication and design flaws (Thomas and Baker 2013, [V]).
5. MRI volume cannot tell dendrite, synapse, glia, vessel or water changes apart. A hydration swing alone moves apparent brain volume by about 0.5 to 0.7 percent in hours (Duning 2005, [V]), the same order as the effects claimed.
6. No open dataset I could confirm combines cortisol with repeated structural MRI. The best open options are (a) UK Biobank repeat imaging with a life-event field (application needed), and (b) the single-subject daily-scan set ds002674 with daily Perceived Stress Scale (open, CC0, confirmed).
7. Recommended first analysis: estimate the within-person noise floor and a lagged stress-to-hippocampus association on ds002674 (60 daily T1 scans), then decide whether the UK Biobank test is worth the application. Details in section 6.

## 1. Question and the decision it informs

Question. Does exposure to stress or elevated glucocorticoids change hippocampal (and other) grey matter volume within a person over time, in the direction predicted by the glucocorticoid cascade hypothesis, and is that distinguishable from (i) a pre-existing smaller hippocampus that raises vulnerability and (ii) measurement artifact? The companion question is whether use and training grow grey matter on the same MRI measure, which gives a positive control for what the measure can detect.

Decision. Whether to commit workstation time and a data-access application to a preregistered longitudinal test, and which dataset and effect-size margin to commit to. Success criteria are in section 5. The framing follows Sapolsky's glucocorticoid cascade (1986, [V]) and his later review of glucocorticoids and hippocampal atrophy (2000, [V]). The book "Determined" (Sapolsky, 2023) is the operator's frame; I did not open a primary page for its bibliographic details [U].

## 2. State of evidence

### 2.1 Glucocorticoid hypothesis of hippocampal atrophy

Evidence ranking used: consortium meta-analysis > randomized or longitudinal human > case-control human > animal histology.

| Evidence | Design | N | Result | Source |
|---|---|---|---|---|
| Glucocorticoid cascade | Review/hypothesis | n/a | Stress, GC feedback loss, hippocampal damage, further GC excess | Sapolsky, Krey, McEwen 1986 [V] |
| Rat CA3 dendrites | Corticosterone 10 mg/day 21 days, Golgi | small groups (n not read) | Fewer apical branch points and shorter apical length in CA3 only; no change in CA1 or dentate | Woolley 1990 [V] |
| Chronic immobilization stress, rat | Dendritic morphometry | n not read | CA3 dendritic atrophy; opposite sign (more arborization) in basolateral amygdala | Vyas 2002 [V] |
| Primate | Cortisol pellets in hippocampus, 1 year | 4 vervet monkeys | Neuronal damage in CA3/CA2 on cortisol side | Sapolsky 1990 [V] |
| Aging cortisol | Cortisol history + MRI | not read | Prolonged cortisol elevation linked to smaller hippocampus and worse memory; correlation of atrophy with cortisol "strong" | Lupien 1998 [V] |
| Cushing's, cross-sectional | Manual tracing | 12 | HF volume vs plasma cortisol r = -0.73 | Starkman 1992 [V] |
| Cushing's, 3T VBM | Patients vs controls | 19 | Hippocampus about 2.9 vs 3.2 mL (about 10 percent smaller), also cerebellum | Burkhardt 2015 [V] |
| Cushing's, treatment | Pre/post surgery | 22 | HF volume up by mean 3.2 +/- 2.5 percent, up to 10 percent | Starkman 1999 [V] |
| PTSD, early | Case-control | 26 vs 22 | 8 percent smaller right hippocampus | Bremner 1995 [V] |
| PTSD meta-analysis | 9 published studies | 133 PTSD, 148 + 53 controls | Smaller bilateral hippocampi | Kitayama 2005 [V] |
| PTSD, consortium | ENIGMA-PGC, 16 cohorts | 1868 (794 PTSD) | Hippocampus d = -0.17, p = 0.00054 vs trauma-exposed controls | Logue 2018 [V] |
| Twin design | MZ twins discordant for trauma | numbers not read | Smaller hippocampi in PTSD patients and in their trauma-unexposed co-twins: a risk factor, not only a consequence | Gilbertson 2002 [V] |
| MDD, early meta-analysis | 12 studies | 351 vs 279 | 8 percent (left) and 10 percent (right) smaller; scaled with episode count | Videbech 2004 [V] |
| MDD, consortium | ENIGMA-MDD, 15 samples | 1728 vs 7199 | d = -0.14 (-1.24 percent); d = -0.17 in recurrent MDD; none in first episode | Schmaal 2016 [V] |
| Prospective natural exposure | Pre/post earthquake MRI | 42 non-PTSD | Orbitofrontal GMV decrease through the quake tracked symptoms; pre-quake anterior cingulate GMV predicted symptoms | Sekiguchi 2013 [V] |
| Population cohort | Perceived stress, scans 5 yr apart | 35 high vs 76 low stress | Smaller hippocampus at baseline in high-stress group; group difference unchanged at follow-up | Lindgren 2016 [V] |

Reading across rows (inferred, moderate):
- Effect size shrinks as N grows. Early studies reported 8 to 10 percent; consortium estimates are 1.2 to 1.5 percent. This is the signature of small-sample inflation and excess significance (Ioannidis 2011 found 142 positive data sets observed vs about 78.5 expected across 41 brain-volume meta-analyses, [V]; Button 2013 [V]).
- Dose-response in humans appears where exposure is extreme (Cushing's, recurrent MDD) and is absent where it is mild (first-episode MDD).
- The animal literature localizes the effect to CA3 apical dendrites, a compartment smaller than the neighbouring bulk tissue that MRI averages over (see 2.3).
- Direction of causation is unresolved: twin and cohort data support a pre-existing trait; Cushing's reversal supports a state effect. Both can be true.

### 2.2 Training-induced and use-dependent grey matter change in humans

| Study | Design | N | Result | Source |
|---|---|---|---|---|
| Taxi drivers, cross-sectional | Licensed drivers vs controls | n not read here | Larger posterior, smaller anterior hippocampus; correlates with years driving | Maguire 2000 [V] |
| London taxi trainees | Longitudinal over about 4 years | 79 trainees (39 qualified), 31 controls ([S], primary n not read) | Posterior hippocampal GM increased in qualifiers only; none in failers or controls | Woollett and Maguire 2011 [V] (journal: Current Biology) |
| Juggling, young | 3-ball cascade, 3 scans | 24 total ([S]) | Bilateral mid-temporal (hMT/V5) GM increase after learning, partial decline after 3 months without practice | Draganski 2004 [V citation; abstract not machine-readable, details [S]] |
| Juggling, elderly | Same paradigm | not read | hMT/V5 plus transient left hippocampus and nucleus accumbens increases | Boyke 2008 [V] |
| Aerobic exercise RCT | 1 year, older adults | 120 | Anterior hippocampus +2 percent vs decline in controls; BDNF association | Erickson 2011 [V] |
| MBSR, 8 weeks | Pre/post vs wait-list | 16 vs 17 | Left hippocampus GM concentration up (VBM, ROI) | Holzel 2011 [V] |
| Meditation meta-analysis | 21 studies | about 300 practitioners | Global d = 0.46; authors flag publication bias | Fox 2014 [V] |
| Pregnancy | Pre/post, mothers, fathers, controls | not read | Widespread GM reduction, persists 2 years | Hoekzema 2017 [V] |
| Critical review | Training-dependent plasticity | n/a | Many reported effects may reflect design, statistics, artifact; most robust: anterior hippocampus with exercise in the elderly | Thomas and Baker 2013 [V]; response: Erickson 2013 [V citation] |

Replication record (inferred from the above, moderate): the taxi work replicates within one group across designs; juggling and short meditation effects have no large independent replication that I read. The exercise RCT is the strongest controlled design. Notably the two best-supported use-dependent hippocampal changes are slow (months to years) and about 2 percent, close to the claimed stress effect size in the opposite direction.

### 2.3 Cellular mechanisms and what MRI volume can resolve

Proposed mechanisms, with the strength of direct evidence:
- Dendritic remodeling and spine loss: direct histology in rodents and monkeys (Woolley 1990, Vyas 2002, Sapolsky 1990). Human evidence: none in vivo.
- Synaptogenesis and neuropil change: reviewed as candidate (Zatorre 2012 [V]; the abstract states the cellular link is hard to ascribe, details of the review not read).
- Adult neurogenesis: disputed in humans. Sorrells 2018 found no young neurons in adult dentate gyrus (17 controls, 12 epilepsy) [V]; Boldrini 2018 [V] and Moreno-Jimenez 2019 [V] report thousands of immature neurons into old age. Even if present, neuron-count change in the dentate is too small to move whole-hippocampus volume by 2 percent (inferred, low-moderate).
- Glia and vasculature: Boldrini 2018 reports age-related decline in angiogenesis in anterior-mid dentate without DG volume change [V]. Glial contributions to MRI volume: proposed, no direct human test I opened.
- Water: Dehydration lowered total brain volume 0.55 percent (SD 0.69) after 16 h, with rehydration +0.72 percent (Duning 2005, n not read) [V]; GM/WM loss and ventricular expansion across states in 6 volunteers (Streitburger 2012) [V]; time-of-day reduction detectable in n = 19 (Trefler 2016) [V] and in 755 MS patients and 834 ADNI participants (Nakamura 2015) [V].
- Fast structural signal: DTI changes in hippocampus after 2 h of spatial learning in humans and rats (Sagi 2012) [V]. The authors interpret as cellular rearrangement; DTI is not T1 volume.

What MRI volume can and cannot resolve (inferred, moderate to high):
- Resolution: T1 voxels are about 1 mm^3, which holds on the order of 10^4 to 10^5 cell bodies and a majority neuropil volume (order-of-magnitude, from memory, low confidence). Volume and VBM "density" are readouts of tissue-class partial volume, not of any single cell compartment.
- It cannot separate dendrite retraction from glial swelling, perfusion, myelin change at the GM/WM boundary, or water shifts.
- Segmentation of the hippocampus on 1 mm T1 uses mostly atlas priors; boundary error is comparable in size to a 1 to 2 percent effect.
- Therefore the supportable claim from MRI is "net apparent volume changed by x percent", never "dendrites retracted".

## 3. Open disagreements and confounds

| Issue | Evidence | Handling |
|---|---|---|
| Cause vs vulnerability | Gilbertson 2002 and Lindgren 2016 vs Starkman 1999 | Test both directions in one design (section 5) |
| Neurogenesis in adult humans | Sorrells 2018 vs Boldrini 2018, Moreno-Jimenez 2019 | Do not use neurogenesis as the explanation for MRI change |
| Training effects real? | Thomas and Baker 2013 vs Erickson 2013 comment | Use a positive control with a controlled design |
| Scanner drift and site | Multi-site 3T reproducibility is sensitive to protocol and to cross-sectional vs longitudinal segmentation (Jovicich 2013 [V]); harmonization methods exist (Fortin 2018 [V]) | Same-scanner pairs only, or site as fixed effect |
| Segmentation reliability | Within-subject template reduces bias and variance (Reuter 2012 [V]) | Longitudinal pipeline with common template, symmetric treatment of all time points |
| Hydration and time of day | Duning 2005, Streitburger 2012, Trefler 2016, Nakamura 2015 | Model scan clock time and difference in clock time; flag if unknown |
| Head motion | About 0.7 percent apparent GM loss per mm/min of motion (Reuter 2015, 12 volunteers) [V] | Motion QC covariate; motion correlates with stress and anxiety (inferred) so it can fake the effect |
| Regression to the mean | Groups chosen on extreme baseline stress or volume | Select on exposure measured independently of the outcome; ANCOVA with baseline; no selection on outcome |
| Publication bias | Ioannidis 2011; meditation meta-analysis flags it | Preregister, hold out, report nulls |
| Small samples | Button 2013; Marek 2022 (median neuroimaging N about 25, stable brain-behavior associations need thousands) [V] | Power section below |
| MRI itself as a stressor | A search hit titled "Cortisol responses to serial MRI scans in healthy adults and in depression" (repository.uel.ac.uk) [U, not opened] | Note as possible dependence between exposure and scan; unverified |

## 4. Datasets (documented only; nothing downloaded, no accounts created)

Reachability was checked on 2026-10-09 with HTTP requests or page fetches. A 200 on an OpenNeuro page is a single-page app and proves little, so I also queried the OpenNeuro GraphQL API and the GitHub mirror for each OpenNeuro set.

| Dataset | URL | Access | N and time points | Stress or behavior measures | Reachable today |
|---|---|---|---|---|---|
| 28andMe, ds002674 | https://openneuro.org/datasets/ds002674 ; https://github.com/OpenNeuroDatasets/ds002674 | CC0, open, 63.6 GB total (snapshot 1.0.6) | 1 participant, 60 daily sessions (30 naturally cycling, 30 on oral contraceptive); 60 T1w files confirmed in the repo tree | participants.tsv: Perceived Stress Scale, PSQI, STAI state anxiety, POMS subscales, calorie intake (columns confirmed). README says daily serum hormones; hormone columns not in participants.tsv, location unconfirmed. No cortisol confirmed | Yes: API snapshot, README and TSV read |
| MyConnectome, ds000031 | https://openneuro.org/datasets/ds000031 ; paper https://doi.org/10.1038/ncomms9885 | CC0, open | 1 participant, 104 sessions over 532 days; paper Table 1 lists T1 as 21 total, 10 usable (repo tree shows 26 T1w files) | Mood surveys, sleep (ZEO), food and alcohol logs, blood draws (48), RNA-seq, metabolomics. I read 100k of 152k characters of the paper and found no cortisol; remainder unread | OpenNeuro and GitHub yes; myconnectome.org did not respond (curl code 000) |
| Midnight Scan Club, ds000224 | https://openneuro.org/datasets/ds000224 | CC0, open, 27 GB | 10 participants, 12 sessions each, only 2 structural sessions (4 T1 each) | Neuropsychological testing; no stress measure confirmed | Yes: API and README |
| SIMON | https://fcon_1000.projects.nitrc.org/indi/retro/SIMON.html ; DOI 10.15387/fcp_indi.retro.simon | CC BY-SA 4.0, AWS S3 anonymous, literal filenames | 1 male, 73 sessions, ages 29 to 46 (15+ years), multi-site, T1 in every session | None relevant; session dates in phenotype CSV | Yes: page read |
| Day2day | paper https://doi.org/10.1186/s12868-017-0383-y | Hosting not confirmed [U] | 6 completers of 8, 40 to 50 sessions over 6 months, T1 and T2 hippocampal sequences | Behavioural and physiological variables (details not read) | Paper yes; data location not confirmed |
| Traveling phantoms, ds003011 | https://openneuro.org/datasets/ds003011 | CC0, open, 4.1 GB | 4 participants, 10 sessions across 3 sites over 4 years | None | Yes: API |
| UK Biobank repeat imaging | https://biobank.ndph.ox.ac.uk/showcase/ ; programme page https://ukbiobank.ac.uk/explore-your-participation/contribute-further/repeat-imaging-study | Approved application, fees unknown [U]; showcase category 100003 returned 200 | Visit 2 imaging plus repeat visit 3 "2+ years" later; 20,927 participants at instance 3 in a search-snippet mirror dated 2025-08-30 (moderate); target 60,000. Left hippocampus field 25019: 81,995 participants, two instances (labels not confirmed) | Field 6145 "Illness, injury, bereavement, stress in last 2 years", 4 instances (counts per instance not read). I found no cortisol; unconfirmed | Showcase yes; the programme page returned 403 to my fetch and the ukbiobank.ac.uk imaging page 403 to curl |
| ABCD | Release notes https://docs.abcdstudy.org/latest/documentation/release_notes/6_0.html ; access via NIH NBDC Data Hub (https://nda.nih.gov/abcd returned 200 with no useful content) | Data use certification through the NBDC Data Hub; release 7.0 now exists | 11,868 participants, 13 events to 6-year follow-up; imaging through baseline, 2-year, 4-year and about half of 6-year (search summary of Data Hub text, moderate) | Life Events (PhenX); the 6.0 notes say summary scores "should not be used" due to a coding error, fix planned for 7.0. Saliva hormones (testosterone, estradiol, DHEA) per a vendor release; cortisol in ABCD unconfirmed [U] | Release notes read; abcdstudy.org returned 403 to curl |
| OASIS-3 | https://sites.wustl.edu/oasisbrains/ | DUA plus review, non-commercial | 1,378 participants, 2,842 MR sessions | Cognition and clinical; no stress, life event or cortisol listed | Yes: page read |
| ADNI, HCP-Aging, Cam-CAN | https://adni.loni.usc.edu/ ; https://www.humanconnectome.org/study/hcp-lifespan-aging ; https://cam-can.mrc-cbu.cam.ac.uk/ | Not examined | Not examined | Not examined | Pages returned 200; contents not read |

Gap (observed): I found no open dataset combining repeated structural MRI at a useful interval with salivary, hair or serum cortisol and a controlled stress exposure. Prior work I saw that does combine them (previously institutionalized youth, 156 participants, 306 scans, diurnal cortisol) has no confirmed public release [U]. There is also no open training-intervention T1 set that I confirmed.

## 5. Verifier design (preregisterable)

Two tiers. Tier A is the confirmatory test on UK Biobank (requires an approved application; tabular imaging-derived phenotypes only, so no image processing is required). Tier B is the exploratory single-subject test on ds002674 that sets the noise floor.

### Tier A: UK Biobank repeat-imaging cohort

- Population: participants with QC-passing T1 at visit 2 and visit 3, interval of 2 to 7 years (programme text), complete covariates.
- Exposure E: at least one stressful life event reported in field 6145 at visit 3 (covering the 2 years before it) vs none. Dose variant: event count. Event category labels to be read from the data dictionary before freezing (not verified here).
- Outcome Y: annualized percent change in mean bilateral hippocampal volume between visits (FIRST IDPs, fields 25019 left and the matching right field to be confirmed), divided by ICV from the same scans. Pre-specified secondary outcome: amygdala (exploratory; animal data predict the opposite sign, Vyas 2002). Negative-control outcome: thalamus and putamen change.
- Model: Y standardized to SD units. Linear model Y ~ E + age + age^2 + sex + interval + baseline volume + site at each visit + scanner-change indicator + clock time of each scan + motion/QC proxy at each visit. Baseline volume is included to handle regression to the mean.
- Split rule: before looking at outcomes, hash participant IDs with a fixed salt, assign 50 percent discovery and 50 percent held-out, stratified by visit-3 site. Freeze the model on discovery, then run once on held-out.
- Hypothesis H1: E is associated with more negative annualized hippocampal change; effect on Y of E on the held-out half.
- Support: held-out estimate of E <= -0.10 SD, one-sided 97.5 percent CI excludes 0, same sign in discovery, and the negative-control outcomes show no comparable shift (|effect| < half of the hippocampal effect).
- Null: held-out 90 percent CI for E lies inside +/- 0.10 SD (equivalence test). Anything else is inconclusive.
- Margin rationale (inferred): -0.10 SD is the smallest effect I can power here; it is a standardized change and its percent-volume meaning depends on the SD of annualized change, which is unknown to me until the data are seen. For scale, the cross-sectional consortium effects are d about -0.14 to -0.17.
- Power (computed today with statsmodels, two-sided alpha 0.05, 80 percent target; the exposed share and counts are assumptions, inferred, low): equal groups need 6280, 1571, 699, 393 per group for d = 0.05, 0.10, 0.15, 0.20. With 20,000 participants and 10 percent exposed, the held-out half has 1000 exposed vs 9000 unexposed: power 0.19 at d = 0.05, 0.85 at d = 0.10 (well powered), 0.99 at d = 0.15. With 2000 exposed in the whole sample, held-out power at d = 0.10 is 0.85. For a correlational dose analysis, r = 0.03 needs N = 8,719 and r = 0.05 needs N = 3,137.
- Reverse-direction test (vulnerability): visit-2 hippocampal volume predicting E at visit 3 (logistic), same split. Support for the vulnerability account: odds ratio below 1 per SD of volume with CI excluding 1.
- Positive control: the age slope of hippocampal atrophy over the interval must show the expected acceleration with age; if not, the pipeline is not measuring change and the test is void.
- Positive-control for training: not available in the same data. Gap.

### Tier B: single-subject dense sampling (ds002674)

- Y: hippocampal volume per session (SynthSeg or FreeSurfer), ICV-normalized. X: Perceived Stress Scale on the scan day (lag 0) and prior day (lag 1), from participants.tsv.
- Pre-specified: AR(1) generalized least squares; covariates oral contraceptive regime, scan order, motion QC. Permutation test with block shuffling to respect autocorrelation.
- Power: 60 sessions detect r >= 0.35 at 80 percent (N = 62 needed for r = 0.35; N = 85 for r = 0.30). So only a large within-person association is testable. Inference is for one person and does not generalize.
- Primary deliverable is the day-to-day SD of hippocampal volume, which decides what Tier A can resolve.

## 6. First concrete analysis plan (one workstation: 24 cores, Windows 11 + WSL Ubuntu)

Target: Tier B on ds002674, then Tier A feasibility. Time estimates are from experience, low confidence.

1. Freeze the plan. Write the hypotheses, models, thresholds and split rule from section 5 into a dated file in the repo and commit it before any image is processed. Optional registration on OSF is an account step for the operator.
2. Environment in WSL Ubuntu: Python 3.11 venv, `datalad`, `nibabel`, `statsmodels`, `pingouin`, MRIQC (container or pip), FreeSurfer 7.4+ (free license file needed; operator registers), optionally FastSurfer. Pin versions in a lockfile.
3. Get the data (operator-approved step): `datalad clone https://github.com/OpenNeuroDatasets/ds002674`, then `datalad get sub-01/ses-*/anat/*T1w.nii.gz` and `participants.tsv`. Expect a few hundred MB for T1 only; skip the 63 GB of functional data.
4. QC: run MRIQC on all 60 T1; record motion/QC metrics per session; apply the frozen exclusion rule (for example, worst 10 percent by MRIQC CNR or EFC removed, or modeled as covariate, decided before outcomes).
5. Segment: run SynthSeg (`mri_synthseg --parc --robust --threads 24`) on each session for speed (minutes each), and FreeSurfer longitudinal (`recon-all -base`, then `-long`) as the primary pipeline for within-subject bias control. Budget about 60 sessions x 6 to 8 h cross-sectional, 10 to 20 jobs in parallel, so about 1 day wall-clock.
6. Extract left and right hippocampus and ICV into one CSV keyed by session. Compare SynthSeg vs FreeSurfer-long hippocampal series; report their correlation as a pipeline-sensitivity check.
7. Noise floor: compute the SD and robust MAD of ICV-normalized hippocampal volume across sessions, separately for the natural-cycle and contraceptive halves, and in percent. Compare to the effect sizes in section 2 (about 1 to 3 percent) and to the SIMON T1 series (same extraction on a handful of sessions, listed in the phenotype CSV).
8. Run the frozen model: AR(1) GLS of hippocampal volume on PSS lag 0 and lag 1 plus covariates; block-permutation p-value; report estimate in percent volume per SD of PSS with a CI. Report a model without motion covariates to show the sensitivity to motion.
9. Decision rule (inferred): if the day-to-day SD of hippocampal volume is at or above about 1.5 percent, single-scan changes of 1 to 2 percent are not resolvable and Tier A must use annualized differences over 2+ years with averaging of repeated measures; if the SD is at or below about 0.5 percent, the UK Biobank margin of 0.10 SD is realistic and the application proceeds. Thresholds are my own and should be reviewed before freezing.
10. Tier A preparation: draft the UK Biobank application text and variable list (fields 25019 and right-hippocampus counterpart, 6145, ICV, QC, site, scan time). Check whether the operator's institution already holds access. Do not submit anything without the operator.
11. Report: one page with the noise floor, the lagged-association estimate, the decision, and the does-not-prove line. Publish the nulls.

## 7. Does not prove, and risks

Does not prove:
- That any MRI volume change reflects dendritic, synaptic, glial or neuronal change. It is net apparent tissue volume.
- That stress, cortisol or glucocorticoids caused a change. Tier A tests a self-reported life-event proxy with no cortisol measure; cortisol was not confirmed in any open longitudinal MRI set.
- That a single-subject result (ds002674, SIMON, MyConnectome) generalizes.
- That null in one dataset refutes the cascade hypothesis; the hypothesis predicts effects at extreme or prolonged exposure that these cohorts may not contain.
- That the effect-size margin is correct. The -0.10 SD margin and the exposed-share assumption are mine.

Risks:
- Access and cost: the UK Biobank application, fee and timeline are unknown to me; ABCD requires a data use certification and life-event summary scores are flagged unreliable in release 6.0.
- Life-event self-report is non-random, recall-biased, and confounded with illness, bereavement and socioeconomic status; motion and hydration may covary with stress.
- UK Biobank scanner and software changes between visits could create spurious change; visit-3 site and protocol must be checked from the data.
- Healthy-volunteer selection: repeat imagers are likely healthier than the full cohort (inferred), which restricts range of E.
- Exposure misclassification biases toward the null, which can look like support for "no effect".
- Multiplicity: restrict to the primary outcome and call everything else exploratory.
- Possible confirmation bias from the operator's frame: the plan includes the reverse-direction test and the negative-control outcomes for this reason.
- Source gaps: several primary papers' sample sizes were not read (Maguire 2000, Draganski 2004, Gilbertson 2002, Lupien 1998), and Draganski details come from secondary summaries.

## 8. References (all checked 2026-10-09)

[V] = DOI resolved via Crossref API and abstract read via Europe PMC. Paywalled full text was not read.

1. Sapolsky RM, Krey LC, McEwen BS. The neuroendocrinology of stress and aging: the glucocorticoid cascade hypothesis. Endocr Rev 1986. https://doi.org/10.1210/edrv-7-3-284 [V citation; abstract not read]
2. Sapolsky RM. Glucocorticoids and hippocampal atrophy in neuropsychiatric disorders. Arch Gen Psychiatry 2000. https://doi.org/10.1001/archpsyc.57.10.925 [V citation; abstract not read]
3. Woolley CS, Gould E, McEwen BS. Exposure to excess glucocorticoids alters dendritic morphology of adult hippocampal pyramidal neurons. Brain Res 1990. https://doi.org/10.1016/0006-8993(90)90778-a [V]
4. Sapolsky RM, Uno H, Rebert CS, Finch CE. Hippocampal damage associated with prolonged glucocorticoid exposure in primates. J Neurosci 1990. https://doi.org/10.1523/jneurosci.10-09-02897.1990 [V]
5. Vyas A, Mitra R, Shankaranarayana Rao BS, Chattarji S. Chronic stress induces contrasting patterns of dendritic remodeling in hippocampal and amygdaloid neurons. J Neurosci 2002. https://doi.org/10.1523/jneurosci.22-15-06810.2002 [V]
6. Lupien SJ et al. Cortisol levels during human aging predict hippocampal atrophy and memory deficits. Nat Neurosci 1998. https://doi.org/10.1038/271 [V]
7. Starkman MN et al. Hippocampal formation volume, memory dysfunction, and cortisol levels in patients with Cushing's syndrome. Biol Psychiatry 1992. https://doi.org/10.1016/0006-3223(92)90079-f [V]
8. Starkman MN et al. Decrease in cortisol reverses human hippocampal atrophy following treatment of Cushing's disease. Biol Psychiatry 1999. https://doi.org/10.1016/s0006-3223(99)00203-6 [V]
9. Burkhardt T et al. Hippocampal and cerebellar atrophy in patients with Cushing's disease. Neurosurg Focus 2015. https://doi.org/10.3171/2015.8.focus15324 [V]
10. Bremner JD et al. MRI-based measurement of hippocampal volume in patients with combat-related PTSD. Am J Psychiatry 1995. https://doi.org/10.1176/ajp.152.7.973 [V]
11. Kitayama N et al. MRI measurement of hippocampal volume in posttraumatic stress disorder: a meta-analysis. J Affect Disord 2005. https://doi.org/10.1016/j.jad.2005.05.014 [V]
12. Logue MW et al. Smaller hippocampal volume in PTSD: a multisite ENIGMA-PGC study. Biol Psychiatry 2018. https://doi.org/10.1016/j.biopsych.2017.09.006 [V]
13. Gilbertson MW et al. Smaller hippocampal volume predicts pathologic vulnerability to psychological trauma. Nat Neurosci 2002. https://doi.org/10.1038/nn958 [V]
14. Videbech P, Ravnkilde B. Hippocampal volume and depression: a meta-analysis of MRI studies. Am J Psychiatry 2004. https://doi.org/10.1176/appi.ajp.161.11.1957 [V]
15. Schmaal L et al. Subcortical brain alterations in MDD: findings from the ENIGMA MDD working group. Mol Psychiatry 2016. https://doi.org/10.1038/mp.2015.69 [V]
16. Sekiguchi A et al. Brain structural changes as vulnerability factors and acquired signs of post-earthquake stress. Mol Psychiatry 2013. https://doi.org/10.1038/mp.2012.51 [V]
17. Lindgren L et al. Longitudinal evidence for smaller hippocampus volume as a vulnerability factor for perceived stress. Cereb Cortex 2016. https://doi.org/10.1093/cercor/bhw154 [V]
18. Maguire EA et al. Navigation-related structural change in the hippocampi of taxi drivers. PNAS 2000. https://doi.org/10.1073/pnas.070039597 [V]
19. Woollett K, Maguire EA. Acquiring "the Knowledge" of London's layout drives structural brain changes. Curr Biol 2011. https://doi.org/10.1016/j.cub.2011.11.018 [V]
20. Draganski B et al. Neuroplasticity: changes in grey matter induced by training. Nature 2004. https://doi.org/10.1038/427311a [V citation; full text paywalled, details from secondary summaries]
21. Boyke J et al. Training-induced brain structure changes in the elderly. J Neurosci 2008. https://doi.org/10.1523/jneurosci.0742-08.2008 [V]
22. Erickson KI et al. Exercise training increases size of hippocampus and improves memory. PNAS 2011. https://doi.org/10.1073/pnas.1015950108 [V]
23. Holzel BK et al. Mindfulness practice leads to increases in regional brain gray matter density. Psychiatry Res 2011. https://doi.org/10.1016/j.pscychresns.2010.08.006 [V]
24. Fox KCR et al. Is meditation associated with altered brain structure? Neurosci Biobehav Rev 2014. https://doi.org/10.1016/j.neubiorev.2014.03.016 [V]
25. Hoekzema E et al. Pregnancy leads to long-lasting changes in human brain structure. Nat Neurosci 2017. https://doi.org/10.1038/nn.4458 [V]
26. Thomas C, Baker CI. Teaching an adult brain new tricks: a critical review of evidence for training-dependent structural plasticity in humans. NeuroImage 2013. https://doi.org/10.1016/j.neuroimage.2012.03.069 [V]
27. Erickson KI et al. Evidence for structural plasticity in humans: comment on Thomas and Baker (2012). NeuroImage 2013. https://doi.org/10.1016/j.neuroimage.2012.07.003 [V citation via Crossref; abstract not read]
28. Zatorre RJ, Fields RD, Johansen-Berg H. Plasticity in gray and white: neuroimaging changes in brain structure during learning. Nat Neurosci 2012. https://doi.org/10.1038/nn.3045 [V]
29. Sagi Y et al. Learning in the fast lane: new insights into neuroplasticity. Neuron 2012. https://doi.org/10.1016/j.neuron.2012.01.025 [V]
30. Sorrells SF et al. Human hippocampal neurogenesis drops sharply in children to undetectable levels in adults. Nature 2018. https://doi.org/10.1038/nature25975 [V]
31. Boldrini M et al. Human hippocampal neurogenesis persists throughout aging. Cell Stem Cell 2018. https://doi.org/10.1016/j.stem.2018.03.015 [V]
32. Moreno-Jimenez EP et al. Adult hippocampal neurogenesis is abundant in neurologically healthy subjects and drops sharply in patients with Alzheimer's disease. Nat Med 2019. https://doi.org/10.1038/s41591-019-0375-9 [V]
33. Duning T et al. Dehydration confounds the assessment of brain atrophy. Neurology 2005. https://doi.org/10.1212/01.wnl.0000150542.16969.cc [V]
34. Streitburger D-P et al. Investigating structural brain changes of dehydration using voxel-based morphometry. PLoS ONE 2012. https://doi.org/10.1371/journal.pone.0044195 [V]
35. Trefler A et al. Impact of time-of-day on brain morphometric measures derived from T1-weighted MRI. NeuroImage 2016. https://doi.org/10.1016/j.neuroimage.2016.02.034 [V]
36. Nakamura K et al. Diurnal fluctuations in brain volume: statistical analyses of MRI from large populations. NeuroImage 2015. https://doi.org/10.1016/j.neuroimage.2015.05.077 [V]
37. Reuter M et al. Head motion during MRI acquisition reduces gray matter volume and thickness estimates. NeuroImage 2015. https://doi.org/10.1016/j.neuroimage.2014.12.006 [V]
38. Reuter M et al. Within-subject template estimation for unbiased longitudinal image analysis. NeuroImage 2012. https://doi.org/10.1016/j.neuroimage.2012.02.084 [V]
39. Jovicich J et al. Brain morphometry reproducibility in multi-center 3T MRI studies. NeuroImage 2013. https://doi.org/10.1016/j.neuroimage.2013.05.007 [V]
40. Fortin J-P et al. Harmonization of cortical thickness measurements across scanners and sites. NeuroImage 2018. https://doi.org/10.1016/j.neuroimage.2017.11.024 [V citation; abstract not read]
41. Ioannidis JPA. Excess significance bias in the literature on brain volume abnormalities. Arch Gen Psychiatry 2011. https://doi.org/10.1001/archgenpsychiatry.2011.28 [V]
42. Button KS et al. Power failure: why small sample size undermines the reliability of neuroscience. Nat Rev Neurosci 2013. https://doi.org/10.1038/nrn3475 [V]
43. Marek S et al. Reproducible brain-wide association studies require thousands of individuals. Nature 2022. https://doi.org/10.1038/s41586-022-04492-9 [V]
44. Littlejohns TJ et al. The UK Biobank imaging enhancement of 100,000 participants. Nat Commun 2020. https://doi.org/10.1038/s41467-020-15948-9 [V]
45. Poldrack RA et al. Long-term neural and physiological phenotyping of a single human. Nat Commun 2015. https://doi.org/10.1038/ncomms9885 (PMC4682164 opened, partial text read) [V]
46. Pritschet L et al. Functional reorganization of brain networks across the human menstrual cycle. NeuroImage 2020. https://doi.org/10.1016/j.neuroimage.2020.117091 [V citation; the 28andMe dataset's associated paper]
47. Gordon EM et al. Precision functional mapping of individual human brains. Neuron 2017. https://doi.org/10.1016/j.neuron.2017.07.011 [V citation]
48. Filevich E et al. Day2day: investigating daily variability of MRI measures over half a year. BMC Neurosci 2017. https://doi.org/10.1186/s12868-017-0383-y [V citation; page via PMC5571657 appeared in search, not opened]
49. Duchesne S et al. SIMON dataset. https://doi.org/10.15387/fcp_indi.retro.simon [V citation via Crossref; page https://fcon_1000.projects.nitrc.org/indi/retro/SIMON.html read]
50. ABCD release 6.0 notes. https://docs.abcdstudy.org/latest/documentation/release_notes/6_0.html [opened]
51. OpenNeuro datasets ds002674, ds000031, ds000224, ds003011 (GraphQL API and GitHub mirror read). https://openneuro.org/
52. UK Biobank showcase fields 25019 and 6145. https://biobank.ndph.ox.ac.uk/ukb/field.cgi?id=25019 ; https://biobank.ndph.ox.ac.uk/ukb/field.cgi?id=6145 [opened; instance labels and per-instance counts not shown]
53. OASIS-3. https://sites.wustl.edu/oasisbrains/ [opened]
54. Sapolsky RM. Determined: A Science of Life Without Free Will (2023). [U: book; bibliographic details not opened]
55. "Cortisol responses to serial MRI scans in healthy adults and in depression", https://repository.uel.ac.uk/item/860vx [U: appeared in search results, not opened]
