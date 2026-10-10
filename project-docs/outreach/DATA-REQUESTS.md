# Data requests: drafts for the operator to review and send

Drafted 2026-10-09.

## Send log
- 2026-10-09: Request 1 sent from Gmail to brent.oblinger@usda.gov (message id 1a123e3672abc39a). Operator approval in chat: "Send."
- 2026-10-09: Request 2 sent from Gmail to gabriela.ritokova@odf.oregon.gov, cc sarah.navarro@usda.gov (message id 1a123e372a97a023). Same approval.
- Sent text differs from the drafts below only in: greeting by full name (no titles), and the reply-address placeholder removed.
- Request 3 (LEMMA web form) and the optional LEMMA email: not sent; the form is the operator's to fill.
Sources for the data needs: `project-docs/briefs/05-root-disease-remote-sensing.md` (sections 4 to 6) and `project-docs/briefs/06-phytophthora-ramorum-forecast.md` (sections 5 to 7).

## Where the addresses came from

All USFS and ODF addresses below come from one official page, checked 2026-10-09:

- Source: 2025 Oregon Forest Health Highlights Report (USDA Forest Service and Oregon Department of Forestry), page 3, "Technical Assistance Resources".
- URL: https://www.fs.usda.gov/foresthealth/docs/fhh/OR_FHH_2025.pdf
- PDF metadata: created 2026-06-16, modified 2026-06-18.
- The plain-text layer of this PDF drops "fl" and "fi" ligatures (it prints "robbie.fowers" and "melissa.fscher"). I read the embedded `mailto:` links instead, which carry the correct spellings. The addresses used below match those `mailto:` links exactly.

The ODF/USFS "Update on Sudden Oak Death in Oregon Forests" (https://www.oregon.gov/odf/Documents/forestbenefits/sod-update.pdf, checked 2026-10-09) names its preparers as Sarah Navarro (US Forest Service) and Gabi Ritokova (Oregon Dept of Forestry). It prints no email addresses. That confirms request 2 goes to the right two people.

---

## Request 1: Root disease ground truth (Region 6 Forest Health Protection)

**Recipient:** Brent Oblinger, Pathologist, USDA Forest Service Forest Health Protection, Pacific Northwest Region (Central Oregon Service Center, Bend). He is lead author of Oblinger et al. 2022. Address: `brent.oblinger@usda.gov`

**Source URL for the address:** https://www.fs.usda.gov/foresthealth/docs/fhh/OR_FHH_2025.pdf (page 3, `mailto:` link), checked 2026-10-09. A 2022 OSU conference page (https://forestry.oregonstate.edu/cpe/forest-health-2022) also lists him with FHP in Bend; I saw that only in a search summary.

**Subject:** Data request: root disease plot locations from Oblinger et al. 2022, for a remote-sensing test

**Body:**

Dear Dr. Oblinger,

I am an independent researcher with years of field experience on a Pacific Northwest tree crew. I have no institutional affiliation and no funding.

I am designing a test of whether lidar and imagery can flag Armillaria and laminated root rot centers in Oregon conifer stands, scored against field data the model never sees. The limit is labels. I could not find a public, georeferenced set of confirmed root disease centers.

Would you or Region 6 Forest Health Protection be willing to share any of the following?

1. Field-confirmed root disease center polygons or plot locations (Armillaria, laminated root rot), with confirmation year and method.
2. The plot locations and tree data behind Oblinger et al. 2022 on the Winema National Forest.
3. Any confirmed healthy or lookalike stands, so false positives can be counted.

In return I will send you the results, the code, and a short written report, including a null result if the model does not beat simple baselines. I am glad to sign a data-use agreement and to follow any rules on location precision or landowner privacy.

Thank you for considering this.

Zain Dana Harper
[operator to confirm reply address]

---

## Request 2: Phytophthora ramorum detection records (ODF and USFS Sudden Oak Death program)

**Recipients:**
- To: Gabriela Ritokova, Pathologist, Oregon Department of Forestry (Salem). `gabriela.ritokova@odf.oregon.gov`
- Cc: Sarah Navarro, SOD Pathologist, USDA Forest Service (Portland). `sarah.navarro@usda.gov`

**Source URL for the addresses:** https://www.fs.usda.gov/foresthealth/docs/fhh/OR_FHH_2025.pdf (page 3, `mailto:` links), checked 2026-10-09. Their program roles are confirmed by the "Prepared by" line of https://www.oregon.gov/odf/Documents/forestbenefits/sod-update.pdf, checked 2026-10-09. The ODF Sudden Oak Death web page path used in brief 06 returned 404, so I found no program-level inbox.

**Subject:** Data request: dated P. ramorum detections, quarantine boundaries and stream baiting, for a forecast test

**Body:**

Dear Ms. Ritokova and Dr. Navarro,

I am an independent researcher with years of field experience on a Pacific Northwest tree crew. I have no institutional affiliation and no funding.

I am testing whether a simple forecast can rank where new Phytophthora ramorum infestations will be confirmed next season in southwest Oregon better than distance to the nearest known site. The test fits on earlier years and scores on later ones. It needs data I could not find for public download:

1. Per-site detection records with confirmation dates, and lineage if recorded.
2. Quarantine boundary polygons by year.
3. Stream-baiting results by drainage and year.
4. Survey effort, such as flight lines or ground survey areas, so unsurveyed ground is not scored as negative.

Coarsened locations would still work if confidentiality requires it. Please tell me which rules apply.

In return I will send you the results, the code, and a short written report, including a null result if the forecast does not beat the distance baseline. I am glad to sign a data-use agreement.

Thank you for considering this.

Zain Dana Harper
[operator to confirm reply address]

---

## Request 3: Tanoak basal area (LEMMA, Oregon State University and USFS PNW Research Station)

**LEMMA uses a web request form, not email. I did not fill it.**

- Form: https://lemmadownload.forestry.oregonstate.edu/ , checked 2026-10-09. Fields: First Name, Last Name, Organization, Email. The page offers GNN.2023.1 (model years 1986 to 2021) and GNN.2020.1 (1986 to 2017), lists the attribute "LIDE3_BA: Basal area of Lithocarpus densiflorus", shows 2017 and 2021 in the year selector, and limits each request to 5.0 GB. A link to the data is emailed after processing. The page states no license terms.
- Expanded-use form (more attributes or years): https://lemmadownload.forestry.oregonstate.edu/request-expanded-use , checked 2026-10-09. Fields: First Name, Last Name, Organization, Email, Study Objective, Description of Data Needs, Date needed. Its text still says years run "currently 1986-2017", which conflicts with the main page's 2021. Not needed for the brief 06 plan as written.

**What to enter in the standard form (operator does this):** model series GNN.2023.1 only (the page recommends one series); attribute LIDE3_BA; model years 2017 and 2021; area clipped to Curry County plus adjacent Coos, Douglas and Josephine counties. Organization field: the operator decides what to enter (see decisions below).

**Optional email, only if a question comes up** (for example the license terms, or LIDE3_BA for years other than 2017 and 2021):

- Recipient: Matthew Gregory, LEMMA. The site footer "Contact us" links to his contact page. Address as printed: "matt.gregory at oregonstate.edu", that is `matt.gregory@oregonstate.edu`.
- Source URL: https://lemma.forestry.oregonstate.edu/about , checked 2026-10-09.

**Subject:** Question on LEMMA GNN tanoak basal area (LIDE3_BA) for southwest Oregon

**Body:**

Dear Mr. Gregory,

I am an independent researcher with years of field experience on a Pacific Northwest tree crew. I have no institutional affiliation and no funding.

I plan to request the GNN.2023.1 LIDE3_BA layer for 2017 and 2021, clipped to Curry, Coos, Douglas and Josephine counties, through your download form. I will use it as the host layer in a test of whether a Phytophthora ramorum forecast beats distance to the nearest known infestation.

Two questions before I submit:

1. What terms of use and citation apply to the GNN layers?
2. How reliable is LIDE3_BA at the 30 m pixel scale for tanoak, compared with summaries over larger areas such as 1 km cells?

I will send you the results, the code, and a short written report, and I will cite LEMMA as you direct. I am glad to sign a data-use agreement if one applies.

Thank you.

Zain Dana Harper
[operator to confirm reply address]

---

## Decisions for the operator

1. **Reply address.** Each draft ends with a placeholder. Choose the address to send from.
2. **Deadline.** None is proposed. Leave it out unless there is a real date.
3. **Request 1 cc.** Optional cc to Betsy Goodrich, Pathologist, USFS Main Office, Portland (`anne.goodrich@usda.gov`, same source page), if you want the regional office to see the request. Not included by default.
4. **Request 2 addressing.** Drafted To: Ritokova, Cc: Navarro. You could send it to Navarro first, since the USFS hosts the survey data, or split it into two emails.
5. **Titles.** The drafts say "Dr." for Oblinger and Navarro and "Ms." for Ritokova and "Mr." for Gregory. I did not confirm degrees or preferred titles. Switching to first and last names avoids the guess.
6. **LEMMA form "Organization" field.** It is required. Options: your sole-proprietor name, "Independent researcher", or "None". Make no claim of affiliation.
7. **Whether to send the LEMMA email at all.** The standard form already offers LIDE3_BA for 2017 and 2021, so the email is only needed for license or accuracy questions.
8. **Data handling.** Agreeing to a data-use agreement may restrict publishing coordinates or sharing derived maps. Read any agreement before committing to share code that embeds the data.
9. **Brief 06 error to fix.** The brief says the expanded-use form is needed for extra years. The main page offers 2021 directly; only the expanded-use page says "1986-2017". Low stakes, but the brief should note the conflict.
