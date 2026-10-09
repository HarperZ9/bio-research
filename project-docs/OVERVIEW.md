# Overview: seven projects, ranked

Briefs written 2026-10-09 by research agents; anchor claims spot-checked by
the lead session (checks listed per project). Ranking weighs decision value,
whether data is usable now, verifier strength, and cost on one workstation.

## Ranked plan

| Rank | Project | Can start now? | Verifier | Cost |
|---|---|---|---|---|
| 1 | 04 Mycorrhizal network citation audit | Yes, public literature APIs | The cited papers themselves | Days |
| 2 | 07 Microtubule-regulator gene-set screen | Yes, GEO open data | Held-out strain and lab | Hours |
| 3 | 01 Amygdala-vmPFC vs childhood trauma | Yes, CC0 data; needs operator choices first | Pre-registered single test | Weeks of compute (fMRIPrep on ~240 subjects) |
| 4 | 02 Grey matter noise floor, single subject | Yes, CC0 data | Within-person noise floor, lagged test | Days of compute |
| 5 | 03 Opsin kinetics to extinction circuit | Yes, pure modeling | Bukalo titer shape, predicted before reading effect sizes | Weeks |
| 6 | 06 P. ramorum forecast vs distance baseline | Partly; per-site records need a request | Rolling-origin, beat distance in 8 of 13 years | Days once data arrives |
| 7 | 05 Root disease detection from lidar | Partly; labels need a request | Held-out watersheds, precision at top 25 | Weeks |

## Headline per project

- **01** Large consortium resting-state work (Hinojosa 2026, 1,017 PTSD vs
  1,702 controls) finds stronger amygdala-hippocampus coupling and reports no
  vmPFC deficit; the textbook picture rests mainly on small studies.
  Checked: paper and DOI; ds005237 = Transdiagnostic Connectome Project, CC0.
- **02** Hippocampal volume effects in PTSD and depression are about d = -0.15
  (1 to 1.4 percent), against 8 to 10 percent in early reports; part predates
  stress. Hydration alone moves volume 0.5 to 0.7 percent. Checked: ds002674 =
  "28andMe", CC0, 60 sessions, 63.6 GB.
- **03** No open model joins opsin kinetics to an amygdala-PFC extinction
  circuit. Bukalo's non-monotonic titer result is a clean out-of-sample target.
  Checked: Bukalo et al., Behav Brain Res 396:112913 (online Sept 2020).
- **04** Physical fungal links and lab carbon transfer hold; seedling benefit is
  mixed (5 of 28 experiments); "amounts that matter", kin preference and
  warning signals are weak or untested in the field. Checked: Karst 2023 and
  Beiler DOIs via Crossref.
- **05** No published satellite or time-series detection of Armillaria or
  laminated root rot in the PNW; best work is one 1,257 ha site, not held out.
  Checked: Oblinger et al. 2022, For. Ecol. Manage. 511.
- **06** No Oregon SOD model has been scored against distance to the nearest
  known site. Checked: Vaclavik et al. 2010, 802 infested locations 2001-2009.
- **07** Stress raises tau phosphorylation (two labs); tau knockout protects
  dendrites (one lab); microtubule stability in stressed dendrites was never
  measured directly. Checked: GSE109315 (88 samples); GSE127812 has only 6,
  so its sign check carries little weight; add a larger independent set.

## Decisions that belong to the operator

1. Project 01 before pre-registration: vmPFC mask definition, held-out split
   vs single full-sample test, smallest effect of interest (proposed |r| = 0.10).
2. Data requests to people (permissioned, operator sends): Region 6 Forest
   Health Protection root disease center polygons (05); ODF/USFS per-site
   P. ramorum detections and quarantine polygons (06); LEMMA tanoak maps (06).
3. UK Biobank application for project 02 Tier A (cost unknown).
4. Downloads: ds005237 and the ds002674 T1 subset (a few hundred MB for T1
   only; full dataset 63.6 GB).
