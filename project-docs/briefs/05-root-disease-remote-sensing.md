# Brief 05: Root disease centers from above (Armillaria and laminated root rot, Pacific Northwest conifers)

Date: 2026-10-09. Scope: detection and management only. Register: internal research brief.
Verification tags: OPENED = page or PDF read in this session. META = DOI resolved in Crossref (title, year, venue match) but full text not read. SEEN = appeared only in a search result snippet. UNVERIFIED = could not open; do not rely on it.

## Result first

1. No published study maps laminated root rot (LRR) or Armillaria centers from satellite time series in the PNW. I searched for it and found none (confidence: moderate; search was broad but not a systematic review).
2. The strongest conifer result is Oblinger et al. 2022 (OPENED): airborne lidar with SWIR-band intensity plus orthoimagery, Armillaria in true fir, south central Oregon. Four-class tree health accuracy 83.3% on 150 field trees; live/dead 95.3%. Accuracy is random forest out-of-bag error from one 1257-ha site, so it is not an independent held-out test (confidence: high that it is OOB; the paper names OOB as its model-selection criterion).
3. Its useful manager product is a stand screen, not a tree classifier: dead trees clustered in canopy gaps. All 27 of 27 tested stands were called root disease positive. Those 27 stands all had long-term root disease plots, so the test contained no confirmed negative stands that I could see (confidence: moderate; I read the methods and abstract, not the supplement).
4. The Aerial Detection Survey (ADS) under-records root disease. Oregon's 2025 forest health report says so in its own words (OPENED). ADS cannot serve as complete ground truth. It can serve as a weak, sparse positive source and as the baseline to beat.
5. The binding constraint is labels, not imagery. I found no public, georeferenced root disease center map or plot set for Oregon or Washington (confidence: moderate).

## 1. Question and the decision it informs

Question: can a model flag root disease centers (mapped as polygons of 0.1 ha and up) in PNW conifer stands from lidar, aerial imagery and satellite data, and be scored against ground or survey data it never saw?

Who uses root disease maps and for what:
- Land managers (federal, state, industrial, small owners): choose which stands to cruise first, since field surveys are slow and expensive (Oblinger 2022 states this).
- Silviculture: thinning and replanting. Inside LRR centers, plant or retain non-host or resistant species (cedars, pines, hardwoods per Forest Pathology page, OPENED) rather than Douglas-fir. For Armillaria west of the Cascades, avoid stressed or off-site stock (PNW Handbooks, OPENED).
- Hazard tree work: LRR can weaken roots enough that trees fall before crown symptoms show, especially on good sites and small trees (Forest Pathology LRR page, OPENED). Roadside and recreation-site hazard crews would use center maps to prioritize.
- Wildlife and snag planning: dead trees in root disease gaps matter for habitat (Oblinger 2022).

Decision this brief informs: whether a first model is worth building, on what labels, and which sensor stack to start with.

## 2. Biology relevant to detection

| Feature | Armillaria (A. ostoyae and relatives) | Laminated root rot (Coniferiporia sulphurascens) |
|---|---|---|
| Spread | Along roots; black rhizomorphs ("shoestrings") in soil and bark; root contact. Spores are not a significant route to healthy trees but colonize stumps (PNW Handbooks, OPENED) | Root contact and grafts only; does not grow through soil; infected stumps and roots carry the inoculum (Forest Pathology, OPENED) |
| Center growth | "1 to 3 feet per year" per PNW Handbooks (OPENED). Moderate confidence: single handbook page | Root-surface growth of about 0.33 to 0.67 m per year seen in a search snippet citing a later Forest Service report; UNVERIFIED. Not the same as center radius growth |
| Crown signs | Thin or chlorotic foliage, dieback, sparse cones; trees usually die standing (PNW Handbooks, OPENED) | Crown thinning, chlorosis, reduced growth, stress cone crop in non-cedar hosts (Forest Pathology, OPENED) |
| Other signs | Basal resinosis (heavy resin at root collar), white mycelial fans under bark (PNW Handbooks, OPENED) | Windthrow or butt failure with decayed roots, random fall directions. Page does not mention resinosis (OPENED) |
| Hosts, susceptible | Douglas-fir, grand fir, white fir, sugar pine (PNW Handbooks, OPENED). Grand and white fir east of the Cascades crest are the most frequently killed (DecAID, SEEN only) | Douglas-fir is the key host. Several true firs and mountain hemlock also. Western hemlock, spruces, western larch are "less commonly infected" (OPENED) |
| Hosts, resistant | Western larch, incense-cedar (OPENED) | Pines, cedars, hardwoods most resistant for the non-cedar form (OPENED). A separate cedar form infects western redcedar and Alaska yellow-cedar, usually without crown symptoms |
| Time scale | West of Cascades: common in Douglas-fir plantations about 10 to 25 years old, uncommon in older stands. East: can appear at 5 years and persist for the stand's life (OPENED) | Pathogen survives many years in old stumps; will not invade dead roots (OPENED). Gaps expand slowly (DecAID snippet, SEEN) |

Detection-relevant points:
- Both diseases kill slowly and persist, so the signal is a spatial pattern over years (a gap with standing dead and declining edge trees), not a single-date event (Oblinger 2022).
- Dead trees tend to stand along the perimeter of Armillaria gaps rather than in the center (Oblinger 2022, field plots 2018).
- LRR note for the operator's hypothesis: a gap that holds surviving cedar, pine or hardwood while Douglas-fir and true fir die is a plausible LRR signature. That is inference from host range, not a tested detector (confidence: low).
- Vigor has little or no effect on LRR infection (OPENED), so "healthy-looking" stands are not safe, and drought indices will not explain it.
- Wording correction: the project note groups hemlock with susceptible hosts. Mountain hemlock is a host; western hemlock is listed as less commonly infected. Keep species strata separate in the model.

## 3. State of evidence for remote detection

| Study | Disease and host | Sensor | Result | Validation design | Status |
|---|---|---|---|---|---|
| Oblinger et al. 2022, For. Ecol. Manage. 511:120126 | Armillaria, white and Shasta red fir, Oregon | Airborne lidar (incl. SWIR intensity) plus orthoimagery | 4 classes 83.3% (n=150); alive/dead 95.3%; 290,964 tree objects mapped; about 20% unhealthy, 4% dead or recently killed | OOB error, one site, field plots 2018 (15 plots, 587 trees). Stand screen checked on 27 of 161 stands with prior plots | OPENED |
| Leckie et al. 2004, Int. J. Remote Sens. 25:793 | LRR, Douglas-fir, British Columbia | High resolution multispectral (CASI) | 55 to 60% for 8 health classes; about 82% when off-by-one class counts (as reported by Oblinger) | Not read | META; numbers via Oblinger only. Allen 2022 cites up to 80% for Leckie, which differs, so treat both as unconfirmed |
| Allen et al. 2022, Remote Sens. 14:3830 | Root, butt, stem rot (Heterobasidion, Armillaria), Norway spruce, Norway | UAV hyperspectral, SVM | 76% accuracy, kappa 0.24 (490 bands); about 60%, kappa 0.13 (29 bands) | Labels from harvester data after harvest; split design not read | Crossref abstract OPENED, full text 403 |
| Boman et al. 2025, ISPRS Archives XLVIII-2/W11:33 | Heterobasidion and Armillaria, Norway spruce, Sweden | UAV multispectral plus lidar | Significant NIR and lidar intensity differences, 110 trees (59 healthy, 51 infected). No accuracy reported | Stump decay survey after harvest | OPENED (abstract) |
| Navarro-Cerrillo et al. 2019, For. Ecol. Manage. | Phytophthora root rot, holm oak, Spain | WorldView-2 plus lidar | 87% for two defoliation levels (as reported by Oblinger) | Not read | META |
| Iversen 2020 (thesis) | Root and butt rot, spruce | Hyperspectral plus lidar | 63% (as reported by Oblinger) | Not read | UNVERIFIED |
| Rodman et al. 2021, Remote Sens. Environ. 253:112244 | Wildfire and spruce beetle, Colorado, Landsat LandTrendr | Landsat | Detection depends on mortality agent and severity; about 40% less area than alternative maps (Dryad snippet) | Field data | META |
| Turkish red pine Heterobasidion, Sentinel-2, J. Indian Soc. Remote Sens. 2024 | Regeneration-stage pine | Sentinel-2 RF | 89% OA, kappa 0.84 reported | Unknown | SEEN only; UNVERIFIED |

Reading across the table (synthesis, labeled inference where stated):
- Accuracy rises with active lidar reflectance and with structure, and falls for the subtle live-infected versus asymptomatic split. Both Oblinger and Leckie report most confusion between healthy and slightly unhealthy classes.
- The only validation that matches a manager question (is there a center here?) is Oblinger's stand screen, and it lacks negatives. Everything else is tree-level, small n, same-site.
- 1960s to 1970s film and thermal work found visible and near infrared photography could not separate LRR trees, while disease centers were identifiable on small-scale photographs (1972 Forest Service report found in search; SEEN only, UNVERIFIED). This supports detecting centers as patterns rather than trees (inference, moderate).
- Satellite evidence for slow root disease is absent for conifers in the PNW. Landsat detectability depends on agent and severity (Rodman), so low-severity, patchy root disease mortality is likely to be under-detected at 30 m (inference, moderate).

## 4. Data

Reachability was checked on 2026-10-09 with HTTP requests from this workstation (status 200 unless noted) and, where noted, page content read. I downloaded no datasets.

| Source | URL | Terms | Resolution and coverage | Root disease recorded? | Reachable today |
|---|---|---|---|---|---|
| USFS Insect and Disease Detection Survey (ADS) | https://www.fs.usda.gov/science-technology/data-tools-and-products/fhp-mapping-reporting/detection-surveys | Free download; file geodatabases in ZIP by Forest Service region and year, plus All Years bundles | Sketch-mapped polygons and points; state, private and federal land; R6 (OR, WA) All Years file is 289,610,899 bytes (HEAD check); year files listed for 2021 to 2025 | Weak. Oregon 2025 report: root diseases "underrepresented", "diseases are greatly underrepresented because they are hard to capture via aerial survey" (OPENED). Oblinger notes older dead trees are not mapped in ADS. Which damage codes cover LRR or Armillaria I could not confirm | Yes, 200; R6 file 200 |
| ADS GIS handbook (code lists) | https://www.uvm.edu/femc/attachments/project/1021/ADS_GISHandbook_body_apndxA-C.pdf | Public PDF, November 2005 edition, appendices A to C | Not data | I did not find root disease agent codes in this text. Appendix E reportedly holds the full list (SEEN only) | Yes |
| FIA DataMart | https://research.fs.usda.gov/products/dataandtools/fia-datamart (old path https://apps.fs.usda.gov/fia/datamart/datamart.html) | Free CSV and SQLite downloads | Plots about 1 acre (4 subplots of 24 ft radius, SEEN). Public coordinates are fuzzed and swapped; sources conflict on distance (0.5 mile vs 1 mile, SEEN) | Partly. Tree damage agent codes exist; root disease category 21000 reported in a 2026 supplement (SEEN, low confidence). FIADB user guide not opened | Yes, 200 |
| Oregon lidar (DOGAMI, Oregon Lidar Consortium) | https://www.oregon.gov/dogami/lidar/Pages/index.aspx ; viewer https://gis.dogami.oregon.gov/ | Free download; data "for informational purposes", update windows third Wednesday monthly | About 99% of the state covered by at least one project as of January 2026 (OPENED). Point density not stated on the page; see per-project acquisition reports. Viewer notes updated tile downloads "to be published soon", so bulk access path may be in flux | No | Yes, both 200 |
| Washington Lidar Portal (DNR) | https://lidarportal.dnr.wa.gov/ | Described as "publicly available"; license text not confirmed | LAZ point clouds, DEMs, hillshades; EPT for browser viewing (SEEN via NOAA metadata and DNR slides). Coverage list not obtained | No | Yes, 200; page body gave only a title |
| Sentinel-2 (Copernicus Data Space Ecosystem) | https://dataspace.copernicus.eu/ | Free and open; individual quotas, larger use under commercial terms (SEEN) | 10 to 60 m bands; record from 2015; dense revisit from 2017 (Fordead snippet, SEEN) | No | Yes, 200 |
| Landsat Collection 2 Level-2 (USGS EarthExplorer) | https://earthexplorer.usgs.gov/ | Free; open data policy since 2008 (SEEN) | 1982 to present for Level-2 (Landsat 4 to 9); 30 m is from memory, unverified here | No | Yes, 200 |
| NAIP orthoimagery | https://naip-usdaonline.hub.arcgis.com/ | Free; terms not read | Roughly 0.6 to 1 m, multi-year cycle: from memory, UNVERIFIED | No | Yes, 200 |
| USGS 3DEP | https://www.usgs.gov/3d-elevation-program | Not read | Not read | No | HTTP 403 to my request (likely bot block); content UNVERIFIED |
| Forest Service Research Data Archive | https://www.fs.usda.gov/rds/archive/ | Public | Searched for root disease plot datasets; found none | Not found | Yes, 200 |

Published root disease ground truth:
- Oblinger 2022 used 15 plots (587 trees) from 2018 and older monitoring plots from Maffei et al. 2008 and Filip et al. 2010 (Winema National Forest, Oregon). I did not find those plots posted as a public dataset (confidence: moderate). Authors are at the Forest Service; a data request is the realistic route.
- A 2011 Forest Service report describes 260 plots of 0.04 ha across the East Cascades of Oregon for Armillaria species (treesearch/39258, SEEN only). Whether coordinates are public is unknown.
- Region 6 Forest Health Protection holds ground checks of aerial survey polygons (Oblinger and ADS documents say ground checks are done). Not public as far as I found.

## 5. Verifier design

Principle: scoring must use labels the model, and the person tuning it, did not see, and the label source must not be derived from the same imagery the model reads.

Label tiers (strongest first):
1. Field-confirmed centers: pathologist or crew survey with fungus confirmed (mycelial fans, rhizomorphs, or conks) and polygon boundaries. Source: Region 6 Forest Health Protection, Oblinger-type plots. Sparse, highest value.
2. Plot-level FIA root disease damage codes. Fuzzed coordinates, so usable only at stand or 1-mile scale, not to score 10 m pixels. Use as a regional sanity check.
3. ADS polygons coded to root disease. High precision when present, very low recall. Use only as positives and never to count a miss as a false positive.
4. Expert photo-interpretation on imagery the model does not use (for example operator or crew labeling of historical aerial photos or oblique photos) with a second labeler. Weakest; report separately.

Splits:
- Spatial blocks by watershed (HUC10) so neighbors never straddle train and test.
- Temporal: train on lidar epoch A and imagery through year Y, test on centers confirmed after Y.
- Region holdout as a stress test: train east Cascades Armillaria (Oblinger-like), test west-side Douglas-fir LRR, and the reverse. Expect a large drop; report it (inference: host, disease, forest structure all differ).
- Test labels frozen and hashed before any model tuning.

Unit of scoring: the disease center (polygon, at least about 0.1 ha), not the pixel and not the tree. Tree-level accuracy is a diagnostic only.

Metrics, proposed (I derived these; the thresholds are inference and a manager must set the final ones, confidence: low):
- Center recall at a fixed review budget: of confirmed centers, what fraction fall inside the top N flagged areas, where N is what a crew can visit in a season.
- Precision at top-k (for example top 25 flagged sites): fraction confirmed on a ground visit.
- Lift over three baselines: random stands of the same host type, ADS root disease polygons, and a no-learning rule (dead trees inside canopy gaps, from Oblinger).
- Negatives: include confirmed healthy stands matched on species, age and site, and confirmed lookalikes (bark beetle, windthrow, harvest, fire, Swiss needle cast) so false positive rates are real.
- Report intervals (bootstrap by watershed) and the denominator of confirmed centers.

Useful versus not useful for a manager (proposed targets, to be agreed):
- Useful: at least half of the top 25 sites confirmed, with lift of at least 2 over the best baseline on held-out watersheds, and recall that finds centers ADS missed.
- Not useful: beating random stands only; accuracy that holds in-region but collapses cross-region without a stated limit; any claim built on tree-level overall accuracy alone.

## 6. First concrete analysis plan (one workstation, 24 cores, Windows 11 with WSL Ubuntu, Python)

Goal of the first run: test whether the no-learning "dead trees in canopy gaps" screen, then a simple learned model, beats ADS and random on held-out watersheds in one region. Cheapest decisive experiment first.

1. Choose the region by label access, not by preference. Ask the operator to contact Region 6 Forest Health Protection and Oblinger et al. for confirmed center polygons and plot coordinates (a human request; I did not and will not submit forms or create accounts). Fallback region: east Cascades Oregon near Winema National Forest, where published plots exist.
2. Inventory the Oregon lidar projects over the area in the DOGAMI viewer. Record for each project: acquisition year, point density from the acquisition report, whether intensity is present. Prefer two epochs. Document only; download tiles after the label decision.
3. Set up WSL Ubuntu with Python environment: pdal or laspy, rasterio, geopandas, scikit-learn, lightgbm, scikit-image, whitebox or lidR via R if wanted. Keep scripts outside the data directory; open downloads in their own empty directories and run readers with `python -I`.
4. For each lidar tile (parallel across 24 cores): build a 1 m digital terrain model and canopy height model, canopy gap raster (minimum opening about 202 m2, the value Oblinger used; confidence moderate that I read the symbol correctly, since text extraction garbled it), standing dead tree candidates from crown segmentation plus return intensity and structure.
5. Rule baseline: dead tree density in 30 m cells (Oblinger used a threshold near 24 trees per hectare, text garbled) intersected with gaps. Output candidate center polygons.
6. Add ADS: rasterize R6 root disease and other damage polygons for the same years; compute baseline recall and precision on the held-out labels.
7. Add satellite features for the same polygons: Landsat annual composites and Sentinel-2 summer composites from 2015, trend and slope of NDVI and SWIR indices, years since first decline. Test whether they add anything beyond lidar (expected small gain at 10 to 30 m for centers under about 1 ha; inference, low confidence).
8. Learned model: gradient boosting on polygon or 30 m cell features (gap size and shape, dead density, edge dead fraction, surviving non-host stems inside the gap, species mix from NAIP or lidar, slope, aspect, HUC, stand age if known). Spatially blocked cross-validation by HUC10, then one frozen test set of unseen watersheds.
9. Lookalike controls: include mapped Douglas-fir beetle and fire polygons from ADS and perimeters, harvest edges (from land cover change), and windthrow, as negative or confusion classes.
10. Report per Section 5 with intervals, the confusion with lookalikes, and an explicit does-not-prove paragraph. Decision point: continue only if the learned model beats the rule baseline and ADS on held-out watersheds at the review budget.

Compute: tile processing is embarrassingly parallel; storage need is unknown until project sizes are read in step 2.

## 7. Does not prove, and risks

This brief does not prove that any model can find root disease centers in the PNW. It shows what exists, what labels are scarce, and a design to test it. All accuracy figures are from other regions, hosts or sensors and from same-site validation.

Risks:
- Label noise and label bias. Field-confirmed centers are few, were chosen by surveyors, and cluster near roads and known problem stands. ADS labels are sketch-mapped from aircraft and miss root disease. Photo-interpreted labels from the same imagery would leak.
- Confusion with other mortality. Bark beetles (Douglas-fir beetle in large Douglas-fir, fir engraver in true fir) often follow root disease stress, so an ADS "beetle" polygon can sit on a root disease center. Oregon's report notes insect damage "often indicates underlying stress from a different primary causal agent" (OPENED). Do not treat beetle polygons as true negatives.
- Drought and fire. Both produce dead stands in patches. Spatial pattern (expanding, edge-weighted dead, multi-year persistence) is the separating cue (inference).
- Swiss needle cast. It yellows Douglas-fir foliage and is visible from the air (Oregon report, OPENED), mostly in the coast range. It is a crown-color confounder for spectral methods, not for gap and dead-tree structure. Oregon is moving SNC monitoring to a fixed-radius plot network and SNC is not shown in annual survey totals (OPENED). A satellite lidar chapter on SNC exists in the 2014 cooperative report (SEEN only, UNVERIFIED).
- Other root diseases: black stain root disease and Heterobasidion/annosus also make gaps in conifers (Oregon report mentions blackstain, OPENED). Armillaria and LRR often co-occur. A "root disease" label may be a mixture; say so.
- Sensor and epoch mismatch: lidar epochs differ in season, density and intensity calibration. Intensity-based features (the strongest in Oblinger) may not transfer across vendors without normalization (inference, moderate).
- Domain shift: Oblinger's setting (dry east side, white and Shasta red fir) differs from west-side Douglas-fir LRR plantations.
- Gap origin: many canopy gaps are natural, harvest or fire. A gap detector alone will have high false positives.
- Access risk: the DOGAMI bulk download path is described as changing; Washington license terms were not confirmed.
- Reporting risk: avoid calling model output "root disease maps" without field confirmation. Output is "candidate centers for field verification".

## 8. References

All DOIs below were resolved in Crossref on 2026-10-09 unless tagged. "OPENED" means I read the page or PDF.

1. Oblinger BW, Bright BC, Hanavan RP, Simpson M, Hudak AT, Cook BD, Corp LA. 2022. Identifying conifer mortality induced by Armillaria root disease using airborne lidar and orthoimagery in south central Oregon. Forest Ecology and Management 511:120126. https://doi.org/10.1016/j.foreco.2022.120126 ; PDF https://research.fs.usda.gov/download/treesearch/63932.pdf (OPENED, full text).
2. Leckie DG, Jay C, Gougeon FA, Sturrock RN, Paradine D. 2004. Detection and assessment of trees with Phellinus weirii (laminated root rot) using high resolution multi-spectral imagery. Int J Remote Sensing 25(4):793-818. https://doi.org/10.1080/0143116031000139926 (META; accuracy numbers via Oblinger).
3. Allen BJ, Dalponte M, Orka HO, Naesset E, Puliti S, Astrup R, Gobakken T. 2022. UAV-based hyperspectral imagery for detection of root, butt, and stem rot in Norway spruce. Remote Sensing 14(15):3830. https://doi.org/10.3390/rs14153830 (abstract OPENED via Crossref; publisher page 403).
4. Boman G, Dahy B, Sengun E, Witzell J, Fransson JES. 2025. Detecting root rot infected Norway spruce trees using multispectral and LiDAR UAV data. ISPRS Archives XLVIII-2/W11:33-38. https://doi.org/10.5194/isprs-archives-XLVIII-2-W11-2025-33-2025 (OPENED, abstract).
5. Navarro-Cerrillo RM, Varo-Martinez MA, Acosta C, Palacios Rodriguez G, Sanchez-Cuesta R, Ruiz Gomez FJ. 2019. Integration of WorldView-2 and airborne laser scanning data to classify defoliation levels in Quercus ilex L. dehesas affected by root rot mortality. Forest Ecology and Management. https://doi.org/10.1016/j.foreco.2019.117564 (META; 87% figure via Oblinger).
6. Coleman TW, Graves AD, Heath Z, Flowers RW, Hanavan RP, Cluck DR, Ryerson D. 2018. Accuracy of aerial detection surveys for mapping insect and disease disturbances in the United States. Forest Ecology and Management 430:321-336. https://doi.org/10.1016/j.foreco.2018.08.020 (META; summary of an abstract: overall accuracy above 70% in error matrices, lower at species level; abstract found at https://spb.clemson.edu/?p=505, SEEN).
7. Rodman KC, Andrus RA, Carlson TT, et al. 2021. Disturbance detection in Landsat time series is influenced by tree mortality agent and severity, not by prior disturbance. Remote Sensing of Environment. https://doi.org/10.1016/j.rse.2020.112244 (META; findings via https://datadryad.org/dataset/doi:10.5061/dryad.dv41ns1ws, SEEN). Author list not verified.
8. Thies WG, Sturrock RN. 1995. Laminated root rot in western North America. USDA Forest Service PNW-GTR-349. https://research.fs.usda.gov/treesearch/3065 (OPENED, abstract only; no spread rate or detectability statement found there).
9. Forest Pathology. Laminated root rot (Coniferiporia sulphurascens). https://forestpathology.org/root-diseases/laminated/ (OPENED).
10. PNW Pest Management Handbooks. Fir, Douglas and True: Armillaria root rot, revised March 2026. https://pnwhandbooks.org/plantdisease/host-disease/fir-douglas-true-armillaria-root-rot (OPENED).
11. Oregon Department of Forestry and Forest Service. 2025 Oregon Forest Health Highlights. https://www.fs.usda.gov/foresthealth/docs/fhh/OR_FHH_2025.pdf (OPENED, text extracted).
12. USDA Forest Service. Insect and Disease Detection Survey data. https://www.fs.usda.gov/science-technology/data-tools-and-products/fhp-mapping-reporting/detection-surveys (OPENED).
13. USDA Forest Service. Aerial Survey GIS Handbook, Appendices A-C, November 2005. https://www.uvm.edu/femc/attachments/project/1021/ADS_GISHandbook_body_apndxA-C.pdf (OPENED, text extracted).
14. DOGAMI Oregon lidar. https://www.oregon.gov/dogami/lidar/Pages/index.aspx (OPENED).
15. Washington Lidar Portal. https://lidarportal.dnr.wa.gov/ (reachable; content not read).
16. FIA DataMart. https://research.fs.usda.gov/products/dataandtools/fia-datamart (OPENED).
17. Copernicus Data Space Ecosystem. https://dataspace.copernicus.eu/ ; USGS EarthExplorer https://earthexplorer.usgs.gov/ ; NAIP hub https://naip-usdaonline.hub.arcgis.com/ (reachability only).
18. UNVERIFIED items: DecAID Armillaria and LRR pages (https://apps.fs.usda.gov/decaid/views/armillaria_root_disease.html , .../laminated_root_rot.html; connection reset on every attempt, content seen only in search snippets); Iversen 2020 thesis; 1972 Forest Service report on LRR photography; Turkish red pine Sentinel-2 Heterobasidion study (2024); 2011 East Cascades Armillaria report https://research.fs.usda.gov/treesearch/39258 ; SNC 2014 cooperative report chapter; LRR 0.33 to 0.67 m per year figure; NAIP resolution; Landsat 30 m.
