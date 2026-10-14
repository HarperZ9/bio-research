# Brief 06: Forecasting Phytophthora ramorum spread in southwest Oregon (Curry County), with P. lateralis as a related case

Date of research: 2026-10-09. Scope: surveillance, forecasting and management only. Nothing here concerns raising pathogen fitness.
Verification key: VERIFIED = I opened the DOI or URL and read the cited content. UNVERIFIED = I saw it only in search results, or the page refused me (HTTP 403/410). UNVERIFIED items must be re-opened before anyone cites them.

## Result first

1. The best-documented Oregon predictor of spread is rainfall plus past infestation size, not a mechanistic model. Peterson et al. 2015 found that maximum dispersal distance was best predicted by spring and winter precipitation two years before detection plus prior-year infestation size (VERIFIED, high). That gives a testable, cheap forecast target.
2. The only Oregon model I found with a true temporal hold-out is Vaclavik et al. 2010: fit on 2005-2008 field data, tested on 2009, AUC 0.911 (VERIFIED, high). It was never scored against a distance-only baseline, and its dispersal-pressure term is a distance-like input. Whether the model adds anything beyond "near a known site" is open. That is the gap this project can close.
3. The Oregon situation changed after those studies. In 2025 the program reported 51 to 54 new infested sites at or beyond the 2015 quarantine, 495 samples with 170 positive, and an emergency boundary of 289 square miles (VERIFIED against the ODF update dated 2025-12-31; the two site counts disagree inside that document, see section 3).
4. Best data: the USFS Insect and Disease Survey (IDS) Region 6 geodatabases (public, no stated terms, reachable) and PRISM (public, terms page read, reachable). The decisive data, per-site detection coordinates with dates and stream bait results, has no public download that I could confirm. It must be requested from ODF / USFS.
5. Recommended first analysis: a temporal hold-out comparison of a distance-to-nearest-known-site baseline against the same baseline plus tanoak basal area and lagged PRISM precipitation, scored by the share of new infestations captured in the top 5 percent of surveyed area. Details in sections 6 and 7.

## 1. Question and the decision it informs

Question. Given detections through year Y, where in Curry County and adjacent Coos, Douglas and Josephine counties will new P. ramorum infestations be confirmed in year Y+1 (and Y+2), and how much better is that ranking than "closest to a known site"?

Decisions informed (owners: Oregon Department of Forestry (ODF), USFS, Oregon Department of Agriculture (ODA), BLM, private landowners):
- Survey allocation: which cells get helicopter passes, ground delimitation and stream baits next season (the 2025 program flew four helicopter surveys, one fixed-wing survey and used high-resolution imagery over 1021 square miles; VERIFIED, ODF update).
- Quarantine boundary: whether a proposed expansion is warranted. The program reports quarantine law allows any confirmed-infested area to be quarantined without a new emergency order (search summary of ODF materials, UNVERIFIED wording).
- Treatment priority: eradication buffers of 300 to 600 ft radius around outlier sites versus slow-the-spread effort in the generally infested area (VERIFIED, ODF update). Funding is limited: no state treatment funds in 2025, 1:1 federal match, 202 acres treated in 2025 (VERIFIED, ODF update).
- Change trigger: if a model cannot beat the distance baseline on held-out years, survey allocation should stay rule-based.

## 2. Biology relevant to spread

Hosts (confidence in parentheses).
- Tanoak (Notholithocarpus densiflorus, formerly Lithocarpus) is the dying and sporulating host driving the Oregon epidemic (high). Goheen et al. 2017 and Kanaskie et al. 2017 describe tanoak mortality; canopy tanoak mortality rose from near 0 to 87 percent between 2012 and 2016 where eradication treatments stopped (VERIFIED, high).
- Other hosts play a minor role in Oregon. Hansen et al. 2006 (GTR PSW-196) reports inoculum is low and that myrtlewood (the Pacific Northwest name for California bay) is rarely infected and plays little role in the Oregon epidemic (VERIFIED for the quote, high; the myrtlewood equals bay laurel identification is from memory, moderate). Vaclavik et al. 2010 name rhododendron and evergreen huckleberry as common understory hosts in high-risk stands (VERIFIED, moderate that they matter for sporulation).
- Contrast: in California, bay laurel is a major inoculum source (Davidson et al. 2008 per search, UNVERIFIED). Do not import California host roles into Oregon models without Oregon evidence.

Lineages in Oregon forests (why it matters: they are separate introductions, so each is a separate eradication problem, and a model fit on pooled data mixes separate invasion fronts).
- NA1: original outbreak, found July 2001 near Brookings (VERIFIED, high). Ireland et al. 2013 state NA1 was the only forest genotype in California and Oregon at that time (VERIFIED).
- EU1: found on one tanoak near a closed nursery by the Pistol River in early 2015, first EU1 report in US forests; trees within about 130 m cut and burned; two post-treatment tests negative (VERIFIED, Kanaskie et al. 2017). The ODF stream-bait program keeps WA-114 as an EU1 positive control (VERIFIED).
- NA2: tanoak north of Port Orford, spring 2021, about 33 km from the nearest known infestation, over 100 positive trees found in follow-up (search summary of Peterson et al. 2022, UNVERIFIED; landing page 403).
- Management consequence: new-lineage outliers imply new introductions (nursery or human movement), which no dispersal kernel fit on NA1 can forecast. Treat long jumps as a separate process with its own survey rule (inference, moderate).

Dispersal.
- Rain splash and wind-driven rain: Fichtner et al. 2009 report splash to about 30 cm height and Davidson et al. 2005 report rain-borne transmission at 5 to 10 m, both California (search summaries only, UNVERIFIED).
- Local scale in Oregon: about half of new infections within 122 m of a prior infection, 79 percent within 300 m, occasional jumps to 4 km (Hansen et al. 2008, abstract seen via search, UNVERIFIED). The program's own summary gives maximum cumulative spread from the 2001 sites as 28 km north, 12 km northeast along the Chetco River and 11 km southeast along the Winchuck River (VERIFIED, Kanaskie et al. 2017).
- Streams: stream baiting detects pathogen in drainages; 22 streams positive by plate culture and 8 more by PCR in 2025 (VERIFIED, ODF update). Streams are detection tools more than proven spread routes in Oregon (inference, moderate).
- Long distance: Cunniffe, Filipe and colleagues model power-law dispersal kernels for California (Filipe 2012: power law fit better than negative exponential; VERIFIED).
- Human movement: logs, soil and plants. The program runs a log persistence study on felled infected tanoak (VERIFIED). Outcomes are not yet reported.

Seasonality and climate.
- Peterson 2015: mortality appears about 2 years after inoculum introduction; wet spring 2010 plus a 2009 treatment delay preceded the 2011 outbreak (VERIFIED, high).
- Filipe 2012 use spring rainfall and temperature as drivers; infection to mortality about 2.5 years (95 percent credible interval 2.3 to 2.9) in Humboldt County, California (VERIFIED, high for California only).
- Ireland et al. 2013 (CLIMEX): heat stress begins near 31 C; all but one of 2696 California and Oregon SODMAP detections fell in moderate to highly favourable areas, and all Curry County locations did (VERIFIED, high). Climate suitability is coarse; it does not rank within the already suitable coast.

## 3. History and management in Oregon

| Date | Event | Source and status | Confidence |
|---|---|---|---|
| Jul 2001 | First detection in Curry County, found by aerial survey; first Oregon report Goheen et al. 2002, Plant Disease 86:441 | Kanaskie GTR (VERIFIED); Goheen 2002 (search only, UNVERIFIED) | high |
| 2001 | Quarantine 22 km2 (9 mi2) (Goheen 2017 says 23 km2) | VERIFIED | high |
| 2009 | Quarantine 420 km2 | Kanaskie 2011 NZJFS, search summary; PDF 403, UNVERIFIED | low |
| 2010-2011 | Sharp rise after many infestations left untreated | VERIFIED (Kanaskie GTR; Peterson 2015) | high |
| 2012 | Generally Infested Area (GIA) created where eradication is no longer required; expanded four times, 151 km2 by 2017 (Goheen: 145 km2) | VERIFIED | high |
| 2015 | Quarantine 1,333 km2 (515 mi2), 31.8 percent of county | VERIFIED (Kanaskie GTR; Vaclavik reports 1333.3 km2 and 31.8 percent) | high |
| 2015 | EU1 on one tanoak near Pistol River | VERIFIED | high |
| 2012-2016 | Canopy tanoak mortality from near 0 to 87 percent where treatment stopped | VERIFIED | high |
| 2021 | NA2 north of Port Orford; later Humbug area site outside boundary | search only, UNVERIFIED | moderate |
| 2022 | Review: three lineages (NA1, EU1, NA2); control cost over US$32 million 2001-2020 | LeBoldus et al. 2022, search summary, UNVERIFIED | low |
| 2024 | 15 new infestations outside the 2015 quarantine (search summary of COMTF Feb 2025; the fetch of that report was refused by my fetch tool, UNVERIFIED) | | low |
| 2025 | 51 new infested sites outside the 2015 quarantine; the same document later says 54 new infestations at or beyond the GIA; emergency boundary 289 mi2; 495 samples, 170 positive; treatments 202 acres | ODF update 2025-12-31, VERIFIED | high that the figures are in the source; moderate on which count is correct |

Program shift: eradication goal changed to slow the spread on forest land around 2010 (search summary of ODF materials, UNVERIFIED; the Kanaskie GTR confirms the GIA concept from 2012). Treatments use cutting, burning and herbicide on infected and nearby hosts (VERIFIED, Goheen 2017).

Outcomes. Pathogen eliminated from many sites but spread continued mostly north (VERIFIED). Peterson 2015 concludes eradication "likely moderated" the epidemic without eliminating it (VERIFIED, abstract). Cunniffe 2016 concludes for California that slowing the epidemic is no longer feasible but earlier control could have worked (VERIFIED, abstract); it does not transfer to Oregon without a refit.

Caveat on sizes: quarantine, GIA, "emergency boundary" and "proposed 901 mi2 boundary" are different polygons. Pull geometry rather than comparing quoted areas.

### P. lateralis on Port Orford cedar (related case)
- Host: essentially specific to Port-Orford-cedar; Pacific yew sometimes killed slowly (VERIFIED, Hansen 2011).
- History: first reported on ornamental cedars near Seattle in 1923, native range around 1950 (a search summary gives 1952 near Coos Bay), throughout Oregon range by 1970, California 1980 (VERIFIED for the Hansen dates; 1952 UNVERIFIED).
- Dispersal: mud on vehicles and equipment, animals and people; downstream movement in streams once established (VERIFIED). Jules, Steenbock and Carroll report only two new infestations from 1999 to 2012 in their 37 km2 study area, i.e. spread slowed (search summary, UNVERIFIED; Wiley page 403). Roads and stream crossings concentrate risk (Hansen et al. 2000, UNVERIFIED).
- Management: road closure and washing, plus planting resistant stock (VERIFIED in outline, Hansen 2011).
- Modelling relevance: spread is network driven (roads, streams), so a road and watershed network model fits better than a radial kernel (inference, moderate). It also gives a counterexample for the verifier: for P. lateralis the "nearest known site" baseline is the wrong baseline; use road-network distance and upstream-downstream topology.

## 4. State of evidence for spread models

| Study | System | Method | Validation design | Accuracy reported | Status |
|---|---|---|---|---|---|
| Meentemeyer et al. 2004, For Ecol Manage 200:195 | California | Rule-based GIS risk (host index, temperature, moisture) | Risk at infested vs uninfested field sites | Risk significantly higher at infested sites (P < 0.01, n = 323). No AUC | VERIFIED, high |
| Vaclavik et al. 2010, For Ecol Manage 260:1026 | Oregon | Heuristic risk map + Maxent with dispersal pressure | Chronological: dispersal 2001-2004 (n = 218), calibrate 2005-2008 (n = 482), test 2009 (102 positives, 34 negatives > 200 m from known sites) | AUC 0.911, commission 0.18, omission 0.13. Heuristic map put 29 percent of 802 infected sites in low risk | VERIFIED, high |
| Meentemeyer et al. 2011, Ecosphere 2:art17 | California | Stochastic spatio-temporal epidemic model, MCMC, weather | Treesearch page reports no hold-out or accuracy | Not reported on page I read | VERIFIED page; full PDF not read, unknown |
| Ireland et al. 2013, PLoS ONE 8:e63508 | Global | CLIMEX | California, Oregon and Norway data reserved from fitting | 2695 of 2696 detections in moderate-high suitability | VERIFIED, high |
| Filipe et al. 2012, PLoS Comput Biol | Humboldt County, CA | Spatial transmission model, Bayesian data augmentation, aerial survey 2004-2009 | Authors state cross-validation against independent data "was not possible"; fit to data through 2007 forecast a faster front than final fit | Front about 4 km per year; no quantitative skill score | VERIFIED, high |
| Cunniffe et al. 2016, PNAS 113:5640 | California | Same model family, control optimisation | Not a skill test; scenario comparison | Dynamic front-targeted treatment performed best | VERIFIED abstract |
| Peterson et al. 2015, Phytopathology 105:937 | Oregon | Information-theoretic regression of yearly infestation area and max dispersal distance | Abstract names none | Predictors: lagged precipitation, prior size | VERIFIED abstract; PDF not read |

Synthesis.
- Mechanistic epidemic models (Meentemeyer, Filipe, Cunniffe, Gilligan lineage) are validated by fit and scenario analysis, not by forecast skill on held-out years (high confidence for Filipe 2012, which says so; moderate for the others, since I read only abstracts).
- The Oregon statistical model has a real temporal hold-out but a single test year with 136 cells/samples, and the negatives are survey-selected (inference from Vaclavik methods text, moderate).
- No paper I found compares an Oregon model against a distance-only baseline. Absence of evidence from my search, not proof (low confidence it does not exist).
- Not found: any published forecast evaluation of P. lateralis spread after 2015 (low confidence).

## 5. Data (reachability checked 2026-10-09; I did not download any dataset)

| Dataset | URL | Access terms | Coverage | Reachable today |
|---|---|---|---|---|
| ODF/USFS "Update on Sudden Oak Death in Oregon Forests" (annual) | https://www.oregon.gov/odf/Documents/forestbenefits/sod-update.pdf | Public PDF, no terms stated | 2025 counts, stream bait results, treatment acres, maps (figures only) | Yes, opened; dated 2025-12-31 |
| Oregon per-site detections, quarantine polygons, stream bait results | No public download confirmed. ODF SOD page at /odf/forestbenefits/pages/sudden-oak-death.aspx returned 404 | Likely a data-sharing request to ODF SOD program (Gabi Ritokova) / USFS (Sarah Navarro), named as preparers in the update. Landowner confidentiality probable | 2001 to 2025, per program | NO public source confirmed. Status unknown |
| ODA SOD program and quarantine rule | https://www.oregon.gov/oda/plant-health/Pages/sudden-oak-death-program.aspx; rule at https://secure.sos.state.or.us/oard/viewSingleRule.action?ruleVrsnRsn=158438 | Public | Rule text and nursery programme; page has no map | Page: yes. Rule URL: not tested |
| USFS Insect and Disease Survey (IDS), Region 6 geodatabases | Page https://www.fs.usda.gov/science-technology/data-tools-and-products/fhp-mapping-reporting/detection-surveys ; files e.g. https://www.fs.usda.gov/foresthealth/docs/IDS_Data_for_Download/CONUS_Region6_AllYears.gdb.zip (276 MB listed) | Public; page states no terms | Region 6, annual 2021-2025 files plus an all-years file; polygon accuracy limited by observer, weather, season; flight-coverage layers (1996 on) only on request to Forest Health Protection | Page: yes, opened. File links listed, not fetched |
| ODF re-published aerial survey layers | https://gis.odf.oregon.gov/ags1/rest/services/WebMercator/ForestHealth/MapServer (layer 4 = 2016) | Credits USFS, ODF, Washington DNR; no separate license | Layers 2012-2016 seen in search; fields Year, Acres, Agent1 | Layer 4: yes. A newer service path (InsectAndDisease/MapServer) returned 404 |
| PRISM climate grids | https://prism.oregonstate.edu/ ; terms https://prism.oregonstate.edu/terms/ | Free; data may be reproduced and distributed; cite PRISM Group, OSU, URL, access date. Orders page said to prohibit commercial use without arrangement (search summary, UNVERIFIED) | CONUS, 4 km and 800 m, monthly from 1895, daily from 1981, 1991-2020 normals | Yes, both pages opened. Web service gives one BIL grid per request; rate limit not found |
| Tanoak distribution: LEMMA gradient nearest neighbor (GNN) maps, field LIDE3_BA | https://lemmadownload.forestry.oregonstate.edu/ | Request form with name, organization, email (this is a form; I did not submit it); 5 GB per request. The standard form offers LIDE3_BA for model years 2017 and 2021 directly. The expanded-use form is for more attributes or years; its text still says "1986-2017", which conflicts with the main page (correction 2026-10-14, see outreach/DATA-REQUESTS.md item 9) | WA, OR, CA at 30 m; model years 1986-2021 (GNN 2023.1) | Yes, opened |
| USFS FIA DataMart | https://research.fs.usda.gov/products/dataandtools/fia-datamart | No terms on the page. Public plot coordinates are fuzzed and swapped (search summary of FIESTA docs, moderate); exact coordinates need FIA Spatial Data Services | Oregon plot/tree tables, CSV or SQLite | Yes, opened |
| Sudden Oak Death portal (California Oak Mortality Task Force, COMTF) | https://www.suddenoakdeath.org/ ; monthly reports e.g. https://www.suddenoakdeath.org/wp-content/uploads/2025/02/February-2025-COMTF-Report.pdf | Public; copyright footer only | Newsletters, reports; I found no Oregon data download | Site: yes. February 2025 report: my fetch tool was refused, UNVERIFIED |
| OakMapper / SODmap | oakmapper.org | n/a | n/a | WARNING: the domain now serves an unrelated gambling site. Do not use it. Locate the current SODmap host before relying on it |
| USDA APHIS P. ramorum page | https://www.aphis.usda.gov/plant-pests-diseases/phytophthora-ramorum | Public | Federal quarantine 7 CFR 301.92 | URL returned 404; the ODA-listed APHIS path was not tested |

Sampling bias warning for any detection table: confirmed sites reflect where crews and flights went. Treat "not detected" as "not found among surveyed cells" and obtain survey effort (flight lines, ground survey polygons) before scoring negatives.

## 6. Verifier design

Principle: fit on earlier years, score on later years, beat a naive baseline.

Unit: 1 km grid cell (or 500 m) in host-bearing forest (tanoak basal area above a small threshold) within, say, 40 km of any prior detection. Outcome for year t: cell contains at least one newly confirmed infested site in year t that was not within the same cell earlier.

Splits (rolling origin, no leakage):
- Train years up to Y, test year Y+1. Repeat for Y = 2012 through 2024 where data allow.
- Also test the 2-year lag explicitly, since detection lags inoculum by about 2 years (Peterson 2015).
- Keep the 2025 season as one untouched final test, scored once.

Baselines the model must beat (all fixed before looking at test scores):
- B0: negative distance to nearest known infestation as of Y.
- B1: B0 using only sites first detected in the last 2 years (front-weighted).
- B2: kernel density of prior detections at a fixed bandwidth.
- B3: tanoak basal area only (no spatial history).
- B4: uniform within the buffer (floor).

Candidate models, in order of complexity: B0 plus tanoak basal area; plus lagged PRISM precipitation (winter and spring, lagged 1 and 2 years); plus a long-jump term (distance-decay with heavy tail); optionally a Maxent-like fit as in Vaclavik 2010.

Metrics:
- Primary, decision-shaped: fraction of the year's new infestations captured within the top 5 percent and top 10 percent of ranked surveyed cells (what crews can actually fly or walk).
- Secondary: AUC, plus average precision (positives are rare), log score for calibrated versions.
- Uncertainty: block bootstrap by year and by 20 km spatial blocks. Report intervals, not single numbers.
- Success criterion set before running: the full model beats B0 on top-5-percent capture in at least 8 of 13 test years with a bootstrap interval for the paired difference that excludes zero. Otherwise report a null.
- False-success controls: shuffle tanoak layer across cells (should lose skill), shuffle precipitation across years (should lose skill), and check that skill is not just proximity to the road network or to the survey flight lines.

For P. lateralis: replace B0 with road-network and stream-network distance; use the same rolling-origin design if dated infestation records are obtainable (unknown whether they are).

## 7. First concrete analysis plan (one workstation, Python or R)

Hardware assumption: 16 GB RAM, no GPU needed.

1. Send the data request (human step, not performed here): ask ODF/USFS for per-site P. ramorum confirmations (coordinates, confirmation date, lineage, ownership class), annual survey effort polygons, the quarantine boundary history, and stream bait results. Ask what landowner-confidentiality rules apply to coordinates.
2. In parallel, plan the public-data fallback: IDS Region 6 all-years geodatabase, filtered to the tanoak/SOD damage agent code (confirm the code list in the IDS data dictionary). This gives mortality polygons, a proxy for infested area, not confirmed sites.
3. Obtain PRISM monthly precipitation and mean temperature for the Oregon southwest window, 1981 to 2025, at 800 m via the one-grid-per-request web service. Cite as the terms require.
4. Obtain LEMMA GNN tanoak basal area (LIDE3_BA), 2017 and 2021 model years, clipped to the study window. This is a form-based request; a human submits it.
5. Build the grid and tables: cell id, tanoak basal area, annual PRISM winter and spring totals, distance to nearest prior detection as of each year, survey-effort flag.
6. Implement baselines B0 to B4 first and score them on all rolling splits. Freeze the scoring script and commit it before any richer model runs.
7. Fit candidate models (logistic regression with spline on log distance, then gradient-boosted trees as a check). Fit only on years up to Y for each split.
8. Score on test years; produce capture curves, intervals, and control checks (section 6).
9. Write a one-page result: model versus B0 by year, with the decision (survey allocation rule) stated, including a null if there is no uplift.
10. Re-run once on 2025 after the model is frozen. Archive the data hashes and code version.

Runtime estimate: minutes for baselines on roughly 10^5 to 10^6 cells (inference, moderate). The effort is the data request, not computation.

## 8. Does not prove, and risks

Does not prove:
- That a model with skill is causal. Distance and rainfall capture spread plus survey behaviour. A pass shows ranking skill for crews, not mechanism.
- That a result for NA1 in Curry County transfers to EU1 or NA2 outliers, which are new introductions (inference).
- That California models (Meentemeyer, Filipe, Cunniffe) predict Oregon spread. They are fitted to different hosts (bay laurel in California) and climate.
- That a temporal hold-out is independent: the outcome partly depends on where surveys went the year before.
- Management efficacy. The confound between treatment timing, weather and funding (Peterson 2015 notes a 2009 delay and wet 2010) means treatment effects cannot be read from detection counts alone.

Risks.
- Data access: per-site coordinates may not be shareable. Then only IDS polygons and published figures remain, and the verifier weakens to a polygon-level test.
- Survey-effort bias: aerial detection covers 787,500 acres of flight in 2024 but ground sampling is 860 acres (search summary of COMTF Feb 2025, UNVERIFIED). Detected area is an effort product.
- Small samples: each year has tens of new sites; confidence intervals will be wide.
- Source drift: counts in the ODF update disagree internally (51 vs 54). Quarantine areas quoted by news and ODF differ (148 mi2 vs 289 mi2 emergency boundary in different documents). Pull polygons, not numbers.
- Link rot: forestphytophthoras.org says it is no longer developed and retires 2026-09-01 per a search snippet, and several of its pages returned 410 today. Archive copies of cited papers.
- Domain hijack: oakmapper.org (see section 5).
- This analysis answers a survey and treatment question. It is not an offensive or fitness-related tool; no pathogen-modification content is included.

## 9. References

VERIFIED (I opened the page or file and read the cited content):
1. Cunniffe NJ, Cobb RC, Meentemeyer RK, Rizzo DM, Gilligan CA (2016). Modeling when, where, and how to manage a forest epidemic, motivated by sudden oak death in California. PNAS 113(20):5640-5645. DOI 10.1073/pnas.1602153113. Opened via https://research.fs.usda.gov/treesearch/52554 (the doi.org redirect to pnas.org returned 403).
2. Meentemeyer RK, Cunniffe NJ, Cook AR, Filipe JAN, Hunter RD, Rizzo DM, Gilligan CA (2011). Epidemiological modeling of invasion in heterogeneous landscapes: spread of sudden oak death in California (1990-2030). Ecosphere 2(2):art17. DOI 10.1890/ES10-00192.1. Opened via https://research.fs.usda.gov/treesearch/38357 (abstract page only).
3. Filipe JAN, Cobb RC, Meentemeyer RK, Lee CA, Valachovic YS, Cook AR, Rizzo DM, Gilligan CA (2012). Landscape epidemiology and control of pathogens with cryptic and long-distance dispersal: sudden oak death in northern Californian forests. PLoS Comput Biol. DOI 10.1371/journal.pcbi.1002328. Opened at https://journals.plos.org/plosone/doi?id=10.1371/journal.pcbi.1002328.
4. Vaclavik T, Kanaskie A, Hansen EM, Ohmann JL, Meentemeyer RK (2010). Predicting potential and actual distribution of sudden oak death in Oregon: prioritizing landscape contexts for early detection and eradication of disease outbreaks. For Ecol Manage 260:1026-1035. DOI 10.1016/j.foreco.2010.06.026. Full text read from https://www.suddenoakdeath.org/wp-content/uploads/2010/03/Vaclavik.ORrisk.2010.For_.ecol_.mgt_.pdf.
5. Meentemeyer R, Rizzo D, Mark W, Lotz E (2004). Mapping the risk of establishment and spread of sudden oak death in California. For Ecol Manage 200:195-214. Abstract read at https://www.suddenoakdeath.org/wp-content/uploads/2010/03/Meentemeyer_etal_ForestEcologyMgmt2004.pdf. DOI not read from the file; not asserted here.
6. Ireland KB, Hardy GESJ, Kriticos DJ (2013). Combining inferential and deductive approaches to estimate the potential geographical range of the invasive plant pathogen Phytophthora ramorum. PLoS ONE 8(5):e63508. DOI 10.1371/journal.pone.0063508. Full text read at https://pestrisk.org/wp-content/uploads/2017/05/Ireland_et_al_P_ramorum_CX_PLOS_ON_2013.pdf.
7. Peterson EK, Hansen EM, Kanaskie A (2015). Temporal epidemiology of sudden oak death in Oregon. Phytopathology 105(7):937-946. DOI 10.1094/PHYTO-12-14-0348-FI. Abstract at https://research.fs.usda.gov/treesearch/48713.
8. Kanaskie A, Wiese R, Norlander D, Laine J, Navarro S, Goheen EM, Rhatigan R, Hansen E, Sutton W, Reeser P, Grunwald N, Kamvar Z, Osterbauer N (2017). Slowing spread of sudden oak death in Oregon forests, 2001-2015. USDA FS GTR PSW-255. Abstract at https://research.fs.usda.gov/treesearch/53987.
9. Goheen EM, Kanaskie A, Navarro S, Hansen E (2017). Sudden oak death management in Oregon tanoak forests. Forest Phytophthoras 7(1). https://journals3.library.oregonstate.edu/ForestPhytophthora/article/view/5011 (DOI not shown on page).
10. Hansen EM, Kanaskie A, Goheen EM, Osterbauer N, Sutton W (2006). Epidemiology of Phytophthora ramorum in Oregon. GTR PSW-196:27-29. https://research.fs.usda.gov/treesearch/26514 (no DOI on page).
11. Hansen EM (2011). Phytophthora lateralis. Forest Phytophthoras 1(1). DOI 10.5399/osu/fp.1.1.1816. Full text read at https://journals3.library.oregonstate.edu/ForestPhytophthora/article/download/4886/6586?inline=1.
12. Navarro S, Ritokova G (2025). Update on Sudden Oak Death in Oregon Forests, 2025-12-31 (ODF and USFS). https://www.oregon.gov/odf/Documents/forestbenefits/sod-update.pdf. Text extracted and read.
13. PRISM Group, Oregon State University: https://prism.oregonstate.edu/ and https://prism.oregonstate.edu/terms/ (both opened).
14. LEMMA GNN download: https://lemmadownload.forestry.oregonstate.edu/ (opened). USFS IDS page (opened): https://www.fs.usda.gov/science-technology/data-tools-and-products/fhp-mapping-reporting/detection-surveys. ODF aerial survey layer: https://gis.odf.oregon.gov/ags1/rest/services/WebMercator/ForestHealth/MapServer/4 (opened). FIA DataMart (opened): https://research.fs.usda.gov/products/dataandtools/fia-datamart. ODA program page (opened): https://www.oregon.gov/oda/plant-health/Pages/sudden-oak-death-program.aspx.

UNVERIFIED (seen only as search-result metadata, or the publisher refused my fetch with 403/410 or a connection error; do not cite until opened):
15. Hansen EM, Kanaskie A, Prospero S, McWilliams M, Goheen EM, Osterbauer N, Reeser P, Sutton W (2008). Epidemiology of Phytophthora ramorum in Oregon tanoak forests. Can J For Res 38:1133-1143. DOI 10.1139/X07-217 (publisher 403; author list confirmed in Ireland 2013 reference list, DOI and numbers from search only).
16. Peterson EK, Sondreli KL, Reeser P, Navarro S, Nichols C, Wiese R, Fieland VJ, Grunwald NJ, LeBoldus JM (2022). First report of the NA2 clonal lineage of Phytophthora ramorum infecting tanoak in Oregon forests. Plant Dis. DOI 10.1094/PDIS-10-21-2152-PDN (APS 403).
17. LeBoldus JM, Navarro SM, Kline N, Ritokova G, Grunwald NJ (2022). Repeated emergence of sudden oak death in Oregon: chronology, impact, and management. Plant Dis 106(12):3013-3021 (pestinfo wiki 'connection refused'; DOI not given).
18. Jules ES, Steenbock CM, Carroll AL. Update on the 35-year expansion of Phytophthora lateralis (Forest Pathology 45(2), 2015 or 2014 per source). DOI 10.1111/efp.12158 (Wiley 403; title wording not confirmed).
19. Hansen EM, Goheen DJ, Jules ES, Ullian B (2000). Managing Port-Orford-cedar and the introduced pathogen Phytophthora lateralis. Plant Dis 84:4-14 (APS page 403). https://www.apsnet.org/publications/plantdisease/2000/January/Pages/84_1_4.aspx
20. Kanaskie A et al. (2011). NZ J For Sci 41S:S169-S175. https://www.scionresearch.com/__data/assets/pdf_file/0004/58711/NZJFS-41S2011S169-S175_KANASKIE.pdf (403).
21. Davidson JM, Wickland AC, Patterson HA, Falk KR, Rizzo DM (2005). Transmission of Phytophthora ramorum in mixed-evergreen forest in California. Phytopathology 95:587-596 (APS 403). Fichtner EJ, Lynch SC, Rizzo DM (2009). Phytopathology 99:608-619 (not opened).
22. Goheen EM et al. (2002). Plant Dis 86:441 (first Oregon report); Peterson et al. 2016 EU1 first report DOI 10.1094/PDIS-10-15-1169-PDN (not opened).
23. COMTF Report, February 2025: https://www.suddenoakdeath.org/wp-content/uploads/2025/02/February-2025-COMTF-Report.pdf (fetch tool declined; figures for 2024 come from a search summary).
