# Brief 01: Does amygdala-vmPFC connectivity in trauma and PTSD replicate on open data?

Date: 2026-10-09. Prepared for: Zain Dana Harper. Status: research brief, not a result.

Verification legend (applies to every citation in section 8):
- OPENED: page or API content read in this session.
- DOI-RESOLVES: doi.org returned a 302 to the publisher (checked today), but the publisher page blocked automated fetch (403, bot check, or paywall). Bibliographic facts and abstract claims come from search-engine records of the paper. Full text not read.
- UNVERIFIED: could not open the DOI or URL, or the DOI is missing. Treat the claim as a lead.

Confidence labels: high, moderate, low, unknown. Inference is marked INFERRED.

## Result first

1. The textbook model (hypoactive vmPFC failing to regulate a hyperreactive amygdala) rests mostly on small-sample task studies and early coordinate meta-analyses. The two largest harmonized consortium analyses of resting-state connectivity do not report it. Hinojosa 2026 (1,017 PTSD, 1,702 controls, 32 sites) found stronger amygdala-hippocampus and amygdala-lingual connectivity in PTSD, and its abstract does not mention vmPFC (confidence: moderate; abstract only). Tomas 2025 (n=1,035 trauma-exposed) found no robust static or dynamic connectivity group differences (moderate; abstract only).
2. The structural consortium data show a small hippocampal effect (d = -0.17), a nominal and uncorrected amygdala effect (d = -0.11), and smaller lateral orbitofrontal volume (high for direction, moderate for size).
3. Task meta-analyses disagree on direction. Etkin and Wager 2007 report vmPFC hypoactivation in PTSD. Suarez-Jimenez 2020 (7 studies, 156 PTSD, 148 trauma-exposed controls) report medial prefrontal hyper-activation in conditioning and extinction recall. Fullana 2018 found no consistent amygdala or vmPFC activation in healthy extinction (moderate).
4. A pre-registered reanalysis on open data can test the dimensional version (trauma load vs amygdala-vmPFC rest connectivity) on one open sample (OpenNeuro ds005237, n=241). It cannot test the PTSD-diagnosis version, because the number of PTSD cases there is unknown and probably small. At n=241 it can detect |r| >= 0.18 with 80% power and can only declare non-replication against bounds of about +/-0.20.
5. Recommended first analysis: section 6. Fix a single amygdala-vmPFC rest-FC contrast and a single trauma measure (CTQ total), register it, run it once on ds005237, then repeat on a larger application-gated cohort only if stage 1 survives.

## 1. Question and the decision it informs

Question. Is resting-state or task-evoked functional connectivity between amygdala and vmPFC reliably different in trauma-exposed people or people with PTSD, in the direction the regulation model predicts (weaker coupling or reduced vmPFC control), at an effect size that survives replication in an independent sample?

Decisions that change with the answer:
- The operator (trauma neurobiology, Sapolsky frame): whether to build the "Determined" argument on a prefrontal-regulation deficit as a measured trait, or to state that the circuit claim is unsettled. A weak or null connectivity effect shifts the weight toward developmental, endocrine and context explanations, which also fit Sapolsky's emphasis on prior environment. INFERRED; this is an interpretation, not a finding.
- A lab choosing a biomarker or an outcome target for an imaging trial: amygdala-vmPFC rest FC is a poor candidate if the true effect is below about r = 0.1 (see section 5).
- A reviewer or guideline author: whether to keep citing the 2007-2013 small-sample literature as the settled model.
- A future grant: whether to fund a 1,000+ participant dimensional design (section 5 sizes it) or a within-person, task-based design instead.

## 2. State of the evidence

### 2.1 Structural (largest samples, most reliable)

| Study | N | Result | Notes |
|---|---|---|---|
| Logue 2018, ENIGMA-PGC subcortical volumes | 1,868 (794 PTSD), 16 cohorts | Hippocampus d = -0.17, p = .00054. Amygdala d = -0.11, p = .025, fails Bonferroni (p < .0063) | Compared with trauma-exposed controls. Confidence: high (abstract and search record agree) |
| Wang 2021, ENIGMA-PGC cortical volume mega-analysis | 1,379 PTSD, 2,192 controls, 32 labs | Smaller volume in left and right lateral orbitofrontal gyri, left superior temporal, right insula, lingual, superior parietal. Lateral OFC survives adjustment for depression | Cohen d values not retrieved: unknown. Region is lateral OFC, not the medial vmPFC the model names |

Reading. The prefrontal signal in structure is real but small and sits in lateral orbitofrontal cortex. The amygdala volume effect is not robust. This is the strongest replicated evidence in the field, and it is not about connectivity.

### 2.2 Resting-state

| Study | N | Result | Caveat |
|---|---|---|---|
| Sripada 2012 (Psychosom Med; salience vs default network) | 15 PTSD, 15 combat-exposed, 15 controls | Weaker DMN coupling including rostral ACC/vmPFC, stronger salience network coupling including amygdala | Tiny sample. Moderate confidence on n (search summary) |
| Sripada 2012 (J Psychiatry Neurosci; amygdala seed) | not retrieved: unknown | Reported decreased amygdala-vmPFC coupling in men with PTSD (as summarized by a later review) | Page fetch failed (expired certificate); UNVERIFIED |
| Koch 2016 meta-analysis and review | 14 whole-brain studies, 663 participants (298 PTSD, 365 controls); 9 seed-based studies reviewed qualitatively | Seed-based studies: stronger salience network, weaker DMN connectivity. ALE: increased vACC and parahippocampus/amygdala activity, decreased posterior insula, cerebellum, middle frontal gyrus | Authors note discrepancy between the ALE and the seed-based review. Not amygdala-vmPFC specific |
| Hinojosa 2026, PGC-ENIGMA amygdala and hippocampus seeds | 1,017 PTSD, 1,702 controls, 32 sites | PTSD: stronger left amygdala to right hippocampus/amygdala and to bilateral lingual gyri. Severity tracks the amygdala-hippocampus connection | Effect sizes not retrieved: unknown. Abstract does not report a vmPFC result. Processed centrally (HALFpipe, IBMMA) |
| Tomas 2025, ENIGMA-PGC dynamic FC | 1,035 trauma-exposed | Static and dynamic FC and state dwell times: no robust group differences | Authors attribute the null partly to heterogeneity of trauma type and sample |

Reading. Small single-site studies report reduced amygdala-vmPFC coupling. The two consortium analyses, which are 30 to 70 times larger, do not find it at the level of their published abstracts. Replication record for the specific amygdala-vmPFC rest effect: not established (moderate confidence; I read abstracts only, so a vmPFC effect may sit in supplementary tables).

### 2.3 Task-based (fear conditioning, extinction, emotional faces)

| Study | N | Result | Caveat |
|---|---|---|---|
| Etkin and Wager 2007 | PTSD, social anxiety, phobia, healthy conditioning studies | Amygdala and insula hyperactivation across disorders, weaker in PTSD than the other two. Only PTSD showed reduced dorsal and rostral ACC and vmPFC | Pre-2007 studies, small n. Sample total not retrieved: unknown |
| Milad 2009 | 16 PTSD, 15 trauma-exposed controls | Poor extinction recall in PTSD with lower hippocampus and vmPFC activation, higher dACC | Single site, two-day paradigm. The classic vmPFC-extinction result |
| Hayes 2012 | 26 studies, 342 patients, 342 controls | Quantitative meta-analysis of PTSD neural activity (abstract details beyond n not retrieved) | Mixed tasks |
| Stevens 2013 | 20 PTSD, 20 trauma-exposed controls (civilian women) | Right amygdala up for fearful faces, right amygdala to left vmPFC connectivity down | Single site. Another review cites increased amygdala-vmPFC coupling during trauma recall, so direction depends on task |
| Fullana 2018 | healthy participants, fMRI extinction studies (n not retrieved) | No consistent amygdala or vmPFC activation. Consistent dACC and anterior insula | The healthy-brain anchor of the extinction circuit is itself weak |
| Suarez-Jimenez 2020 | 7 studies, 156 PTSD, 148 trauma-exposed controls | PTSD: higher anterior hippocampus/amygdala and medial PFC activation across conditioning and extinction, lower thalamus | Opposite sign to the vmPFC hypoactivation story. Very few studies |

Reading. Task findings are inconsistent in sign for medial PFC. They depend on phase (conditioning vs recall), contrast, and control group (trauma-exposed vs not). A reanalysis that ignores that structure will mislead.

### 2.4 Why effect sizes should be small (anchor)

Marek 2022 (ABCD n=11,874, HCP n=1,200, UK Biobank n=35,375) report median brain-wide association effect size near |r| = 0.01 and note that published small-sample studies often report 0.2 or more (confidence: moderate; press and search summary, article content blocked). The ENIGMA hippocampal d = -0.17 converts to r of about -0.085 (INFERRED, d/sqrt(d^2+4)). A 15-per-group study cannot detect that. The 2012-2013 amygdala-vmPFC findings should be read as hypotheses.

## 3. Open disagreements and known confounds

Disagreements:
- Direction of medial PFC activity in PTSD (hypo in Etkin and Wager, Milad; hyper in Suarez-Jimenez).
- Whether amygdala hyperreactivity in PTSD is robust at all: structural amygdala volume fails correction in Logue 2018, and the healthy extinction meta-analysis finds no consistent amygdala signal.
- Multivariate vs univariate power. A 2023 matters-arising response argued multivariate BWAS can replicate with moderate samples (UNVERIFIED, found only in a search listing). This matters for the design in section 5: a single pre-specified univariate contrast is the conservative choice.

Confounds and how a reanalysis handles each:
- Head motion. Power 2012 showed motion changes long-range correlations systematically. Trauma and PTSD groups often move more. Handle by mean and censored framewise displacement (FD) as covariates, FD < 0.2 mm scrubbing, a minimum retained volume count, and a motion-matched sensitivity subsample.
- Small samples and winner's curse. Handle by pre-registering one primary contrast and a single-shot test.
- Trauma-type heterogeneity (combat, assault, childhood, disaster). Tomas 2025 names this as a reason for the null. The brief's open dataset carries a childhood-trauma scale, not a mixed adult PTSD sample.
- Medication (SSRIs, antipsychotics, benzodiazepines). Record and run a medication-free or medication-adjusted sensitivity analysis. In ds005237 the README lists "use of psychotropic medication" in the sample characterization.
- Comorbid depression. Wang 2021 shows the lateral OFC result survives depression adjustment, so an analysis should include depression score (QIDS in ds005237) as a covariate in a second model.
- Control choice: trauma-exposed vs trauma-naive controls change the interpretation. Logue 2018 compares with trauma-exposed controls.
- Analytic flexibility: seed definition, parcellation, global signal regression, scrubbing threshold, task contrast. Handle with one registered primary and a registered multiverse as sensitivity only.
- Reliability. Single-session rest FC has modest test-retest reliability; ds005237 has six rest runs, which helps (design fact from README; reliability benefit INFERRED).
- Site and scanner. Consortium analyses use harmonization; single-site open data avoid it but limit generalization.

## 4. Datasets (documentation only; nothing downloaded, no accounts created, no forms submitted)

Reachability column: "HTTP 200" means curl followed redirects and got 200 today (2026-10-09). For single-page-app sites, 200 does not prove the content is as described. "OPENED" means content was read.

| Dataset | URL | Access terms | N | Trauma/symptom measures | Reachable today |
|---|---|---|---|---|---|
| OpenNeuro ds005237, Transdiagnostic Connectome Project (Yale and McLean) | https://openneuro.org/datasets/ds005237 (DOI 10.18112/openneuro.ds005237.v1.1.3) | Open, CC0. No account needed to browse; no DUA stated | 241 adults aged 18-70 (148 psychiatric, 93 healthy comparison); 6 rest runs, 3 task runs (2 Stroop, 1 Faces/Shapes), HCP-style 3T Prisma | Childhood Trauma Questionnaire, QIDS, DASS, PSS, STAI, ASI, SCID-5 interview, medication use. A PTSD-specific scale is not listed in the README. Number of PTSD diagnoses: unknown | OPENED via OpenNeuro API (v1.1.3, README read), page HTTP 200 |
| OpenNeuro ds003721, trauma film paradigm | https://openneuro.org/datasets/ds003721 | Open, CC0 | 35 | Intrusive-memory diary after trauma film, fMRI during film. Healthy volunteers, not clinical trauma | OPENED (README), HTTP 200 |
| OpenNeuro ds004407 and ds004393, imagery-based fear extinction and acquisition | https://openneuro.org/datasets/ds004407 | Open, CC0 | 28 and 32 | Fear conditioning and extinction task fMRI in healthy participants. No trauma measures | Metadata via API only. Page not separately opened |
| OpenNeuro ds005896 and ds005901, AHDC adolescent study (Columbus, Ohio) | https://openneuro.org/datasets/ds005896 | Open, CC0 | 262 listed; 214 with the Emotional Faces task per README | Adolescent substance and health study with Emotional Faces task. Trauma measure not found in README: unknown | OPENED (README), HTTP 200 |
| HCP Young Adult (WU-Minn) | https://www.humanconnectome.org/study/hcp-young-adult | Open Access tier: free ConnectomeDB account plus Open Access terms. Restricted tier: PI application and Restricted Data Use Terms (family structure, exact age). OPENED terms page | 1,206 healthy adults (1,113 with structural MRI); 3T rest and tasks | A trauma or PTSD item set is not stated on the page I opened. From memory (low confidence), the SSAGA interview contains a PTSD section and sits in the restricted tier. Verify in the HCP Data Dictionary before relying on it | OPENED (release page and terms), HTTP 200 |
| ABCD Study, release 7.0 | https://abcdstudy.org/scientists/data-sharing/ ; https://nda.nih.gov/abcd | Application. Data Use Certification, required training, NIST SP 800-171 or ISO 27001-class security attestation, via NIH Brain Development Cohorts (NBDC) Data Hub. NDA stopped taking new ABCD requests on 2025-06-02 per the page | 11,878 at baseline (ages 9 to 11), follow-up to age 17 | KSADS includes a PTSD module and trauma-events items (memory; not confirmed on pages opened: moderate confidence). Rest and task fMRI incl. emotional n-back | OPENED (data-sharing page), HTTP 200 |
| UK Biobank imaging subcohort | https://www.ukbiobank.ac.uk/ | Application via UKB Research Analysis Platform. Fee tiers per search record of the fees page: Tier 3 (includes imaging) GBP 9,000 for 3 years, reduced GBP 500 for students or lower-income countries. Not opened by me | About 100,000 planned imaging; the online mental health questionnaire completed by 157,366 (as of August 2017). Overlap between questionnaire and scan was 16,307 in one published analysis | Online mental health questionnaire with traumatic-event and current-PTSD items. The specific scale is not confirmed here (PCL-6 not confirmed): unknown | HTTP 403 to automated fetch (site blocks bots); fees page seen only as a search record |
| Healthy Brain Network (Child Mind Institute) | https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/ | Open release via INDI; release 1 data descriptor is CC BY 4.0. Current DUA terms: unknown | Release 1: 664 (ages 5 to 21); target 10,000. Current count: unknown | Psychiatric interview and questionnaires; trauma or PTSD fields not confirmed: unknown | HTTP 200; content not read |
| NKI-Rockland Sample | https://rocklandsample.org/ (legacy: https://fcon_1000.projects.nitrc.org/indi/enhanced/) | Described as openly shared; legacy page says it is no longer maintained and points to rocklandsample.org | Target N > 1000 lifespan sample | Trauma or PTSD measures not confirmed: unknown | rocklandsample.org HTTP 200; legacy page OPENED |
| PGC-ENIGMA PTSD working group | https://enigma.ini.usc.edu/ongoing/enigma-ptsd-working-group/ | Collaboration by proposal to the working group; not open download. Terms: unknown | 1,017 PTSD and 1,702 controls in Hinojosa 2026; about 32 sites | Clinician-rated and self-report PTSD, trauma type | HTTP 200 |

Also searched: OpenNeuro keyword search for "PTSD", "posttraumatic", "trauma", "fear conditioning", "maltreatment". Result: no dedicated clinical PTSD imaging dataset surfaced (most "PTSD" hits were false matches on "post"). The keyword index is noisy, so absence is moderate evidence only. The largest cohorts with PTSD imaging (ENIGMA, AURORA-type emergency department cohorts) are not open downloads.

Best open dataset for a first test: ds005237. Best large gated cohort for stage 2: ABCD for developmental trauma, UK Biobank for adult exposure at population scale. The choice depends on access time, which I did not test.

## 5. Verifier design

Principle. The verifier must be able to fail the textbook claim. It fixes the contrast, the sign, the covariates, and the decision thresholds before any outcome is computed on the confirmatory data.

Hypothesis H1 (dimensional, registered). In ds005237, higher Childhood Trauma Questionnaire total score is associated with lower resting-state functional connectivity between bilateral amygdala and a vmPFC region, adjusting for age, sex, site, mean FD and number of retained volumes. Direction: negative. Primary estimate: partial Pearson r (also report standardized beta).

Not tested by H1: PTSD diagnosis, task-evoked connectivity. Those would need a PTSD-case sample (see risks).

Fixed before analysis (register on OSF before running stage 1; I have not created any registration):
- Amygdala: one atlas amygdala mask (for example a standard probabilistic atlas, thresholded), bilateral average. vmPFC: one predefined mask. Registered choice is the decision of the operator; do not tune after seeing results.
- Preprocessing and denoising pipeline version and parameters.
- Primary outcome: Fisher-z Pearson correlation of mean time series after denoising, averaged across retained rest runs.
- Exclusion rule: mean FD > 0.2 mm or fewer than a registered number of retained volumes.

Held-out structure. Stage 0 (development, not for inference): random 30% of ds005237 (about 72 participants) used only to confirm the pipeline runs and the QC thresholds are workable. Stage 1 (confirmatory): the remaining 70% (about 169) tested once. Stage 2 (external held-out): an independent cohort (ABCD, UK Biobank or HBN subject to access), same pipeline, same contrast. Because power is low in stage 1 (table below), I recommend analyzing all 241 as the confirmatory test and treating the external cohort as the true held-out. The 30/70 split buys protection against pipeline tuning at the cost of power: at r = 0.15, power falls from 0.64 to 0.49. This is a trade the operator should choose before registration.

Decision rules (smallest effect size of interest, SESOI, set at |r| = 0.10; this value is a judgement, INFERRED from Marek 2022 and the ENIGMA anchor of about 0.085, and is open to change before registration):
- Replication: estimate negative, two-sided 95% CI excludes 0, and point estimate r <= -0.10.
- Non-replication: 90% CI lies entirely inside (-0.10, +0.10) (equivalence, TOST at alpha = 0.05).
- Inconclusive: everything else.
- Sensitivity: add QIDS as a covariate; run again at FD < 0.15; run again excluding psychotropic medication users. A result that flips with these is reported as fragile.

Power (computed today with Fisher z, two-sided alpha = 0.05; confidence: high for the arithmetic, low for the assumption that the true effect is any specific value):

| True r | n for 80% power | Power at n=241 | Power at n=169 | Power at n=1,000 | Power at n=5,000 |
|---|---|---|---|---|---|
| 0.05 | 3,138 | 0.12 | 0.10 | 0.35 | 0.94 |
| 0.10 | 783 | 0.34 | 0.25 | 0.89 | 1.00 |
| 0.15 | 347 | 0.64 | 0.49 | 1.00 | 1.00 |
| 0.20 | 194 | 0.88 | 0.74 | 1.00 | 1.00 |
| 0.30 | 85 | 1.00 | 0.98 | 1.00 | 1.00 |

Equivalence test sample sizes (80% power, true r = 0, alpha = 0.05 per side): bounds +/-0.10 need n = 854; bounds +/-0.15 need n = 378; bounds +/-0.20 need n = 212.

Consequences, in plain terms:
- At n = 241 a significant result at r = 0.1 to 0.15 is more likely noise-inflated than not (power 0.34 to 0.64).
- At n = 241 the study can only declare non-replication against bounds of +/-0.20. It cannot rule out r = 0.1.
- Establishing or excluding r = 0.1 needs n of about 850 or more, which means a stage 2 cohort.
- For a group comparison at d = 0.17 (the ENIGMA hippocampal size), 544 per group are needed (high confidence on arithmetic). With 241 total and k PTSD cases, the minimum detectable d at 80% power is about 0.90 (k=10), 0.65 (k=20), 0.55 (k=30), 0.49 (k=40). Case count in ds005237 is unknown, so the diagnosis comparison is not feasible to size yet.

## 6. First concrete analysis plan (one workstation: 24 cores, Windows 11 + WSL Ubuntu, no GPU)

Estimated times below are rough guesses (confidence: low). Check tool versions against current releases at execution time and record them.

1. Environment. In WSL Ubuntu, create a clean conda or venv environment. Install DataLad (or openneuro-py), a container runtime (Docker Desktop with WSL backend, or Apptainer), nilearn, pandas, statsmodels, pingouin. Keep downloaded data in its own empty directory, scripts elsewhere, and run Python with `-I` when reading downloaded files.
2. Pre-check, no data touched. Write the pre-registration text: H1, masks, covariates, exclusion rules, SESOI, decision rules, split choice. Freeze it with a timestamp (OSF registration or a signed git tag) before step 4. This step requires the operator to create the registration; I did not.
3. Download ds005237 (this step is outside the brief; no download was done). Use DataLad or `openneuro-py` for BIDS. Fetch phenotype files first (CTQ, QIDS, medication, demographics). Check the CTQ and the SCID-5 diagnosis fields: record counts of PTSD diagnoses and CTQ missingness before looking at any imaging. Missing codes are 999 per README.
4. Stage 0 on the 30% development subset only. Run fMRIPrep on rest runs and T1w. Expect hours per participant on CPU; run 4 to 6 participants in parallel with 4 to 6 threads each. Skip task runs. Use `--skip-bids-validation` only after running the validator once. Confirm the rest runs have enough volumes after scrubbing.
5. Denoising. Use XCP-D (or an equivalent in nilearn): 36-parameter model or equivalent registered model, band-pass or none as registered, FD threshold 0.2 mm, no global signal regression in the primary (GSR as a sensitivity variant).
6. Extract the registered amygdala and vmPFC time series, compute the Fisher-z correlation per run, average over retained runs. Output one row per participant.
7. QC gate before any association test: report FD distribution, retained volumes, correlation between FD and CTQ, and correlation between FD and the outcome. If FD correlates with CTQ above |r| = 0.2, add a motion-matched subsample analysis to the registered sensitivity list.
8. Stage 1 test. One model: outcome ~ CTQ + age + sex + site + mean FD + retained volumes. Report partial r, 95% CI and 90% CI, and the registered decision (replication, non-replication, inconclusive). Run the registered sensitivity analyses. Do not add models after seeing the result; any extra analysis is labelled exploratory.
9. Multiverse as description only: vary atlas mask, GSR, FD threshold, and plot the distribution of r. Do not use it to select a winner.
10. Report. Publish the code, registration, QC table and all estimates, including nulls. Use the section 5 power table to state what the study could and could not exclude.
11. Next gate. If stage 1 gives replication or an inconclusive result with CI overlapping -0.10, apply for ABCD or UK Biobank and repeat with the same frozen pipeline. If stage 1 is an equivalence null at +/-0.20, say so, and do not call it a null at 0.10.

## 7. Does not prove, and risks

Does not prove:
- A test on ds005237 says nothing about PTSD as a diagnosis. CTQ is retrospective self-report of childhood adversity, in a transdiagnostic psychiatric sample with healthy comparison.
- Rest FC is not regulation. A negative amygdala-vmPFC correlation is a statistical coupling, not evidence of top-down control.
- A cross-sectional association cannot separate trauma effects from pre-existing vulnerability, or from shared causes (genetics, adversity-related poverty, sleep, substance use). Whether connectivity differences are consequences of trauma, or markers of vulnerability, remains open. This also limits any use of the result inside a determinism argument.
- A null at n=241 does not refute the model. It rules out only large effects.

Risks:
- Scope drift: choosing the vmPFC mask after seeing data would void the pre-registration.
- Verification gaps in this brief: most journal pages blocked automated reading, so effect sizes for Hinojosa 2026, Tomas 2025 and Wang 2021 come from abstracts and search records. Read the full texts and supplementary tables before citing a vmPFC null, since the abstract may omit it.
- Dataset facts for UK Biobank, HBN, NKI and HCP trauma items are incomplete. Treat the "unknown" entries as open tasks.
- Access timelines for ABCD (NBDC) and UK Biobank (application and fee) are not tested.
- Multiple testing across studies: this brief ranks several datasets but the registered test is a single contrast.
- Computing cost: fMRIPrep on 241 participants with 6 rest runs may take days on a single workstation (confidence: low).
- Privacy: ABCD and UK Biobank have security attestation requirements (ABCD: NIST SP 800-171 or ISO 27001-class). A personal workstation may not qualify. Check before applying.

## 8. References

Each entry gives the verification tag from the legend.

1. Etkin A, Wager TD. Functional neuroimaging of anxiety: a meta-analysis of emotional processing in PTSD, social anxiety disorder, and specific phobia. Am J Psychiatry 2007;164(10):1476-1488. doi:10.1176/appi.ajp.2007.07030504. https://doi.org/10.1176/appi.ajp.2007.07030504 . DOI-RESOLVES (abstract via search record, PMC3318959 listed).
2. Milad MR, Pitman RK, Ellis CB, et al. Neurobiological basis of failure to recall extinction memory in posttraumatic stress disorder. Biol Psychiatry 2009;66(12):1075-1082. doi:10.1016/j.biopsych.2009.06.026. https://pubmed.ncbi.nlm.nih.gov/19748076/ . DOI-RESOLVES.
3. Hayes JP, Hayes SM, Mikedis AM. Quantitative meta-analysis of neural activity in posttraumatic stress disorder. Biol Mood Anxiety Disord 2012;2:9. doi:10.1186/2045-5380-2-9. https://doi.org/10.1186/2045-5380-2-9 . DOI-RESOLVES (author list from search record).
4. Stevens JS, Jovanovic T, Fani N, et al. Disrupted amygdala-prefrontal functional connectivity in civilian women with posttraumatic stress disorder. J Psychiatr Res 2013. https://scholarblogs.emory.edu/nomeslab/files/2017/09/Stevens_2013_JPR.pdf . Appeared in a search listing, not opened. DOI UNVERIFIED. Author list and title from memory: UNVERIFIED.
5. Sripada RK, King AP, Garfinkel SN, et al. Altered resting-state amygdala functional connectivity in men with posttraumatic stress disorder. J Psychiatry Neurosci 2012;37(4):241-249. https://www.jpn.ca/content/37/4/241.full.pdf . Fetch failed (expired certificate). UNVERIFIED.
6. Sripada RK, King AP, Welsh RC, et al. Neural dysregulation in posttraumatic stress disorder: evidence for disrupted equilibrium between salience and default mode brain networks. Psychosom Med 2012. https://sro.sussex.ac.uk/id/eprint/56669/ (title listed as "Neural dysregulation in posttraumatic stress disorder"). Not opened. DOI UNVERIFIED. Author lists in 5 and 6 are from memory: UNVERIFIED.
7. Koch SBJ, van Zuiden M, Nawijn L, et al. Aberrant resting-state brain activity in posttraumatic stress disorder: a meta-analysis and systematic review. Depress Anxiety 2016. https://psychotraumanet.org/en/node/2529 . Abstract surfaced in a search listing, not opened. DOI UNVERIFIED. Author list from memory: UNVERIFIED.
8. Suarez-Jimenez B, Albajes-Eizagirre A, Lazarov A, et al. Neural signatures of conditioning, extinction learning, and extinction recall in posttraumatic stress disorder: a meta-analysis of functional magnetic resonance imaging studies. Psychol Med 2020 (online 2019). doi:10.1017/S0033291719001387. https://doi.org/10.1017/S0033291719001387 . DOI-RESOLVES.
9. Fullana MA, Albajes-Eizagirre A, Soriano-Mas C, et al. Fear extinction in the human brain: a meta-analysis of fMRI studies in healthy participants. Neurosci Biobehav Rev 2018. doi:10.1016/j.neubiorev.2018.03.002. https://doi.org/10.1016/j.neubiorev.2018.03.002 . DOI-RESOLVES. Related NeuroVault record: https://neurovault.org/collections/9474/ (listed, not opened).
10. Logue MW, van Rooij SJH, Dennis EL, et al. Smaller hippocampal volume in posttraumatic stress disorder: a multisite ENIGMA-PGC study. Biol Psychiatry 2018;83(3):244-253. doi:10.1016/j.biopsych.2017.09.006. https://doi.org/10.1016/j.biopsych.2017.09.006 . DOI-RESOLVES (PMC5951719 listed). Co-author list beyond first author: from memory, UNVERIFIED.
11. Wang X, Xie H, Chen T, et al. Cortical volume abnormalities in posttraumatic stress disorder: an ENIGMA-psychiatric genomics consortium PTSD workgroup mega-analysis. Mol Psychiatry 2021;26(8):4331-4343. doi:10.1038/s41380-020-00967-1. https://doi.org/10.1038/s41380-020-00967-1 . DOI-RESOLVES (PMC8180531 listed). Only first author confirmed by search record; others UNVERIFIED.
12. Hinojosa CA, et al. Resting-state functional connectivity of the amygdala and hippocampus in PTSD: results from the PGC-ENIGMA PTSD working group. Am J Psychiatry 2026;183:333-342. doi:10.1176/appi.ajp.20250062. https://doi.org/10.1176/appi.ajp.20250062 . DOI-RESOLVES; publisher returned 403 on fetch. Abstract content via search record only.
13. Tomas CW, Fitzgerald JM, Baird L, et al. Data-driven approach to dynamic resting state functional connectivity in post-traumatic stress disorder: an ENIGMA-PGC PTSD study. Hum Brain Mapp 2025;46(11):e70116. doi:10.1002/hbm.70116. https://doi.org/10.1002/hbm.70116 . DOI-RESOLVES (PMC12308910 listed).
14. Marek S, Tervo-Clemmens B, Calabro FJ, et al. Reproducible brain-wide association studies require thousands of individuals. Nature 2022;603:654-660. doi:10.1038/s41586-022-04492-9. https://doi.org/10.1038/s41586-022-04492-9 . DOI-RESOLVES; publisher fetch blocked (auth redirect). Effect-size statements from press and search summaries. Full author list from memory beyond first three names in the record: UNVERIFIED.
15. Power JD, Barnes KA, Snyder AZ, Schlaggar BL, Petersen SE. Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion. NeuroImage 2012;59(3):2142-2154. doi:10.1016/j.neuroimage.2011.10.018. https://pubmed.ncbi.nlm.nih.gov/22019881/ . DOI-RESOLVES. A corrigendum exists (doi:10.1016/j.neuroimage.2012.01.069, DOI not separately tested); content of the corrigendum not read.
16. Spisak T, Bingel U, Wager TD. Multivariate BWAS can be replicable with moderate sample sizes (matters arising, Nature 2023). Seen only in a search summary. DOI UNVERIFIED. URL UNVERIFIED.
17. Patel R, Spreng RN, Shin LM, Girard TA. Neurocircuitry models of posttraumatic stress disorder and beyond: a meta-analysis of functional neuroimaging studies. Neurosci Biobehav Rev 2012;36:2130-2142. Candidate DOI 10.1016/j.neubiorev.2012.06.003 resolves at doi.org, but the identity of the paper behind it was not confirmed and the title is from memory. UNVERIFIED. Not used for any number in this brief.
18. Chopra S, Cocuzza CV, Lawhead C, et al. The Transdiagnostic Connectome Project. OpenNeuro ds005237 v1.1.3, CC0. doi:10.18112/openneuro.ds005237.v1.1.3 . https://openneuro.org/datasets/ds005237 . OPENED (README and metadata read through the OpenNeuro API). The README cites the preprint https://www.medrxiv.org/content/10.1101/2024.06.18.24309054v1 (not opened).
19. OpenNeuro ds003721 (trauma film paradigm, n=35, CC0) https://openneuro.org/datasets/ds003721 ; ds004407 https://openneuro.org/datasets/ds004407 ; ds005896 https://openneuro.org/datasets/ds005896 . OPENED via API (metadata and README).
20. HCP Young Adult 1200 Subjects data release page https://www.humanconnectome.org/study/hcp-young-adult/document/1200-subjects-data-release and data use terms https://www.humanconnectome.org/study/hcp-young-adult/data-use-terms . OPENED.
21. ABCD Study data sharing https://abcdstudy.org/scientists/data-sharing/ . OPENED. NDA ABCD page https://nda.nih.gov/abcd : HTTP 200 only.
22. UK Biobank fee schedule https://www.ukbiobank.ac.uk/use-our-data/fees/ : appeared in a search record, not opened (site returned 403 to direct fetch). Mental health questionnaire description: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7176892/ (BJPsych Open reanalysis, n=157,366; a search record showed an earlier version flagged as retracted, status not checked). UNVERIFIED for both.
23. Healthy Brain Network data descriptor, Sci Data 2017. doi:10.1038/sdata.2017.181. https://doi.org/10.1038/sdata.2017.181 . DOI-RESOLVES; author list not confirmed.
24. NKI-Rockland Sample: https://rocklandsample.org/ (HTTP 200); legacy page https://fcon_1000.projects.nitrc.org/indi/enhanced/ OPENED.
25. ENIGMA PTSD working group: https://enigma.ini.usc.edu/ongoing/enigma-ptsd-working-group/ . HTTP 200, not read.
26. Sapolsky RM. Determined: a science of life without free will. Penguin Press, 2023. Cited only as the operator's framing; not verified here.
