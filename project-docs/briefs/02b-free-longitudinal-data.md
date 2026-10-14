# Brief 02b: Free longitudinal structural MRI for project 02

Date: 2026-10-10. Register: research brief, flavored. Follows F-02-1 in project-docs/FINDINGS.md.
Constraints (operator): no fees (UK Biobank out); no institution (ABCD out). The operator does any account or agreement step. Nothing was downloaded, no account created, no form filled.
Key: [OPENED] = official page or listing opened today (2026-10-10). UNVERIFIED = not opened or content not obtained; never read it as eligible.

## Result first

1. No dataset I checked today meets every constraint at once: free, open to an individual, repeated T1w at 2+ year intervals, and a stress or cortisol measure. This is an observed result of a partial search, not proof that none exists.
2. The best usable set is NKI-Rockland Sample (NKI-RS) imaging. It needs no account and no agreement. In the BIDS bucket, 500 participants have 2 or more non-retest T1w sessions, 264 span 2 years or more, 95 span 3 years or more (computed from the bucket today, high confidence on the counts).
3. Its stress-relevant phenotype is the blocker. The public imaging release carries only age, sex and handedness. The full phenotype needs a Data Use Agreement signed and notarized by an institutional representative. Whether an unaffiliated individual can obtain it is UNVERIFIED and the wording points against it.
4. OASIS-3 is closed to the operator: the request form states that only institutional email addresses are approved.
5. One lead to open next: OpenNeuro ds007026 ("stressrisk_openNeuro", 2 sessions, 55 subjects, CC0 per the API). Title only; contents UNVERIFIED.

## Ranked table

Rank is by usefulness for project 02 given what is confirmed. Fee column: "none stated" means no fee appeared on the pages I read.

| Rank | Dataset | Individual without institution? | Fee | Agreement | N with 2+ T1w and interval | Stress / trauma / cortisol | Format |
|---|---|---|---|---|---|---|---|
| 1 | NKI-RS imaging (rocklandsample.org) [OPENED] | Imaging: yes, "The bucket is publicly available" (anonymous S3). Phenotype: UNVERIFIED, see below | none stated | Imaging: none. Phenotype: DUA | 500 with 2+ non-retest sessions; 427 span 1 yr+, 264 span 2 yr+, 95 span 3 yr+; 305 with 3+ sessions; median span 742 days. Plus 207 retests, median 28 days (retest gap max 595) | In dictionary: TSC-40 (trauma symptom checklist), STAI, BDI-II. No cortisol, no Perceived Stress Scale, no life-event list found. Not in the public imaging release | NIfTI in BIDS, JSON sidecars; DICOM not included |
| 2 | OpenNeuro ds007026 "stressrisk_openNeuro" [API only] | OpenNeuro CC0 data are open download; contents UNVERIFIED | none | none (CC0) | 2 sessions, 55 subjects per API summary; T1w per session and interval UNVERIFIED | Title suggests stress; UNVERIFIED | BIDS NIfTI presumably; UNVERIFIED |
| 3 | OpenNeuro multi-session adult sets: ds004856 Dallas Lifespan Brain Study (3 sessions, 464 subjects), ds004169 QTIM (2 sessions, 1202), ds003592 neurocognitive aging (2 sessions, 301), ds005752 NIMH Healthy Research Volunteer (2 sessions, 251), ds007522 Precision Aging Network (5 sessions, 969), ds005112 NIMH structural (6 sessions, 135) | CC0 per API; eligibility not an issue for OpenNeuro | none | none | Session counts from the API summary only; whether each session holds a T1w, and the intervals, are UNVERIFIED | UNVERIFIED for all; phenotype folders not opened | BIDS NIfTI |
| 4 | SIMON ds-INDI (single person, 73 sessions) | Open S3, CC BY-SA 4.0 (from brief 02, opened 2026-10-09) | none | none | 1 person; not a group set | none | NIfTI |
| 5 | MyConnectome ds000031, Day2day, ds003011, ds000224 | See brief 02 section 4 | none | none | Single or tiny samples | none confirmed | NIfTI |
| n/a | OASIS-3 (sites.wustl.edu/oasisbrains) [OPENED] | NO. Request form: "Only email addresses issued by research institutions will be approved (e.g., no Gmail, Yahoo, QQ, etc.)" | none stated | DUA, NITRC account | 1378 participants, 2842 MR sessions; per-participant counts and intervals not on the page | None listed (UDS clinical forms, cognitive tests) | NITRC-IR XNAT; format UNVERIFIED |
| n/a | AOMIC (ds003097 and siblings) | UNVERIFIED: the page fetch returned only the title | UNVERIFIED | UNVERIFIED | UNVERIFIED (I recall mostly single-session designs; from memory, low confidence) | UNVERIFIED | UNVERIFIED |
| n/a | HCP Young Adult retest, HCP Lifespan/Aging | UNVERIFIED: not opened in this pass | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| n/a | Cam-CAN repository | UNVERIFIED: not opened in this pass | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| n/a | SLIM (Southwest University longitudinal) | UNVERIFIED: not opened in this pass | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| n/a | IXI | UNVERIFIED: not opened. Cross-sectional by design (from memory, low confidence), so not a candidate | UNVERIFIED | UNVERIFIED | one time point | none | UNVERIFIED |
| n/a | ABCD | Out by operator constraint (institutional signing official, Federal Wide Assurance) | | | | | |
| n/a | UK Biobank | Out by operator constraint (fee) | | | | | |

## NKI-RS: what I opened and read

- Imaging page, https://rocklandsample.org/accessing-the-neuroimaging-data-releases [OPENED]: "The neuroimaging data releases contain the MRI data, physiological data obtained during scanning (cardiac and respiratory) and only basic phenotypic information (age, sex, handedness)." and "The bucket is publicly available and the path is s3://fcp-indi/data/Projects/RocklandSample/RawDataBIDSLatest". "DICOMs are not included."
- Phenotype page, https://rocklandsample.org/phenotypic-data [OPENED]: "The full phenotypic releases of the Enhanced NKI-RS Sample require a data usage agreement". Steps: "Provide appropriate information regarding their name(s) and institution. Have the document signed and notarized by the appropriate institutional representative." The 2014 DUA PDF (https://rocklandsample.org/wp-content/uploads/2023/03/DUA.pdf) [OPENED] adds that requests are "certified and co-signed by the Principal Investigator and the designated Institutional Official(s)" with a scope of work and a CV. The page states that IRB approval and a Federal Wide Assurance number are not required. No sentence says individuals without an institution are refused, and none says they are accepted. Verdict: UNVERIFIED, and the signature requirement is the likely blocker. The operator can ask RocklandSample.Enduser@nki.rfmh.org (address from the page) whether an independent researcher qualifies.
- Counts: I listed the bucket (112,718 keys) and read each multi-session participant's `sessions.tsv` (columns include `session`, `age`, `days_since_enrollment`). These two files are enough to compute intervals without the DUA.
  - Participants with a T1w: 1326. By number of T1w sessions: 785 with 1, 165 with 2, 183 with 3, 174 with 4, 19 with 5 (retest session counted).
  - Excluding the retest session (TRT): 500 participants with 2 or more T1w sessions. Span first to last: 427 at 365 days or more, 264 at 730 days or more, 95 at 1095 days or more, maximum 2623 days.
  - Ages 6 to 74 in the multi-session group. Children and adolescents are in the set, so adult-only analyses will shrink these numbers; I did not split by age.
  - Scanner and protocol per session were not audited. The one sidecar I read was a Siemens TrioTim MPRAGE. Scanner changes between sessions are UNVERIFIED and must be checked before any analysis.
- Phenotype variables: the LORIS dictionary zip (https://rocklandsample.org/wp-content/uploads/2026/04/Rockland-Sample-LORIS-data-dictionaries_w_Codebook.zip) [OPENED, 82 instrument files]. Searching for cortisol, stress, life event, trauma and abuse found TSC-40, and passing mentions in NEO-FFI-3 and others. Blood instruments are "Labs" (glucose, BUN, etc.; no cortisol seen in the first rows I read) and "Metabolites" sets. Whether TSC-40, STAI or BDI-II were collected at the follow-up sessions: UNVERIFIED.
- Legacy page https://fcon_1000.projects.nitrc.org/indi/enhanced/ states "THIS WEBSITE IS NO LONGER MAINTAINED"; use rocklandsample.org. Imaging licence text was not found: UNVERIFIED.

## Best option and exact access steps (NKI-RS imaging, no agreement)

Use: the noise-floor and aging-slope test across 2+ years in a real group. It cannot test stress without the DUA phenotype.

1. No account, form or signature is needed for imaging. Optional: open the page above to confirm the path has not moved.
2. Browse or download with an S3 client set to anonymous: server `s3.amazonaws.com`, "Anonymous Login" checked, path `fcp-indi/data/Projects/RocklandSample/RawDataBIDSLatest` (Cyberduck steps are on the imaging page). A command-line equivalent is `aws s3 cp --no-sign-request`.
3. Fetch only `participants.tsv`, each `sub-*/sub-*_sessions.tsv`, and `sub-*/ses-*/anat/*_T1w.nii.gz` plus `.json`. The T1-only MIVAC list on the bucket (about 6 GB) covers only the MIVAC subset (337 participants, almost all one session); do not use it for the longitudinal group.
4. Select: 2+ non-TRT sessions, span 730 days or more, adults, same scanner by sidecar. Freeze this rule in a dated prereg file before looking at any volume.
5. Segment with the same SynthSeg setup used in F-02-1 so the noise floor transfers.
6. If the operator wants the stress phenotype: email the contact above first and ask in writing whether a non-institutional individual qualifies. Do not start the DUA before the answer, since it needs a notarized institutional signature.

## Alternative path if the DUA is closed

Open ds007026 on OpenNeuro (CC0, open download) and read its README, `participants.tsv`, `sessions.tsv` and the T1w tree. Accept it only if it has two T1w sessions per participant at a known interval and a numeric stress measure. Until then it is a lead, not a candidate. Then repeat the same API check on the six multi-session sets in rank 3.

## OpenNeuro search method and its limits

- GraphQL endpoint https://openneuro.org/crn/graphql, query `datasets(modality:"mri")` with `latestSnapshot.summary` [OPENED]. It returned 1188 MRI datasets; 207 have 2 or more sessions and 20 or more subjects in the summary.
- The `sessions` field also counts task or sub-visit labels and animal datasets (rat, mouse, aneurysm and phantom sets appear). It does not say a session contains a T1w. A proper filter needs each file tree. I did not run one, and several of the 207 were not reviewed (the listing was truncated after the 125th entry).
- So rank 3 is a shortlist from titles and counts, not a verified set.

## Power note (uses the F-02-1 noise floor)

Inputs from F-02-1: within-person CV of hippocampus/TIV 0.77 percent (90% CI 0.67 to 0.92), typical error between consecutive days 0.65 percent. Two single scans resolve a within-person change of about 1.8 percent or more. Literature effects are about 1.2 to 1.5 percent (consortium) and about 2 percent (training).

- Measurement noise alone gives a per-person difference between two scans with SD about sqrt(2) x 0.77 = 1.09 percent (inferred; the pipeline noise of a different scanner or a sequence with a gap of years will differ).
- Two-group comparison of change, 80 percent power, two-sided alpha 0.05, n per group = 2 x (2.8 x SD / delta)^2 (hand calculation, inferred):
  - SD 1.09 percent (noise only, a lower bound): delta 1.0 percent needs about 19 per group; delta 0.5 percent needs about 75.
  - SD 2.5 percent (assumed, adds real between-person differences in change over 2+ years; the true value is unknown until the data are seen): delta 1.0 percent needs about 98 per group; delta 0.5 percent needs about 392.
- NKI-RS has 264 participants with a span of 2 years or more, children included. With an exposed fraction of 20 percent (assumed) that is about 53 exposed, so 1.0 percent is reachable only if the SD is near the noise-only bound, and 0.5 percent is not. Reaching 98 per group needs roughly 500 or more participants at that exposure share.
- Several scans per visit reduce noise by about sqrt(k) only when errors are independent. F-02-1 found lag-1 autocorrelation 0.41 and 0.10 in the two halves, so the gain is smaller than sqrt(k) in the worst case.
- Regression to the mean and cohort-level scanner drift are not in these numbers. Include baseline volume and a scanner indicator.

## Does not prove

- That nothing better exists. HCP, Cam-CAN, SLIM, AOMIC and the OpenNeuro shortlist were not verified.
- That an unaffiliated individual can or cannot obtain the NKI-RS phenotype. The pages are silent on individuals and ask for an institutional signature.
- That NKI-RS follow-up sessions hold usable stress items, or that TSC-40 and STAI proxy cortisol.
- That the session counts reflect usable T1w images. QC, motion and scanner changes were not checked.
- The power figures depend on my assumed SD of 2.5 percent and an exposed share of 20 percent.

## Sources opened today

- https://rocklandsample.org/accessing-the-neuroimaging-data-releases
- https://rocklandsample.org/phenotypic-data
- https://rocklandsample.org/wp-content/uploads/2023/03/DUA.pdf
- https://rocklandsample.org/for-researchers/rockland-sample-i-2011-2022
- s3://fcp-indi/data/Projects/RocklandSample/RawDataBIDSLatest (anonymous HTTPS listing and sessions.tsv files)
- https://sites.wustl.edu/oasisbrains/home/oasis-3/ , .../home/access/ , .../request-access/
- https://openneuro.org/crn/graphql
