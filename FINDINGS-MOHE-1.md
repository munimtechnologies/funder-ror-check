# FINDINGS-MOHE-1: Malaysian grants filed under Egypt's "Ministry of Higher Education"

By MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-15. Made with AI agents working in MV2's name;
not reviewed by a human. Text and data CC BY 4.0.

## In short

This is the seventh case in the series on Crossref Funder Registry records whose main name has no
country in it (after FINDINGS-NRF-1, FINDINGS-MOE-1, FINDINGS-MOST-1 and FINDINGS-MOH-1).

- **"Ministry of Higher Education"**, 10.13039/501100002385, is Egypt's ministry (registry location
  Egypt; its ROR record `0512bh102` also displays just "Ministry of Higher Education", country
  Egypt). Among the 40 records a registry search for "Ministry of Higher Education" returns, it is
  the only one whose main name is exactly that phrase. Malaysia's ministry has its own record,
  "Ministry of Higher Education, Malaysia" (10.13039/501100003093, 23,131 works).
- Egypt's record carries **4,177 works** (Crossref API, 2026-11-15).
- In two random draws (199 distinct works), **79 carry Malaysian grants or Malaysian co-funders**
  (39.7%; 95% Wilson interval 33.2% to 46.6%), and 13 more carry another country's
  (Thailand 3, Taiwan 2, and one each from Tunisia, Indonesia, Saudi Arabia, France, Morocco,
  Sri Lanka, Poland and Iraq). Altogether **92 of 199 (46.2%; 39.4% to 53.2%)** point to a country
  other than Egypt, roughly **1,650 to 2,220 works** across the record.
- Only **14 of 199** show a sign of Egypt (an Egyptian name on the entry, the Egypt-Japan
  University of Science and Technology, JICA with E-JUST, Egypt's Science and Technology
  Development Fund, an Egyptian university or the ministry's missions sector). 93 are unclear.
- **By grant number alone, 43 of 199 (21.6%; 16.5% to 27.8%)** carry a foreign award number on
  the Egyptian entry itself: 40 Malaysian (26 Fundamental Research Grant Scheme numbers such as
  `FRGS/1/2025/TK09/USM/02/4`, 2 Long-Term Research Grant Scheme numbers, and university grant
  or vote codes from UTM, UM, UKM, UMS, USM and UTP), 1 Taiwanese, 1 French ANR and 1 Polish.
  That is a floor of roughly 690 to 1,160 works.
- It is still happening: a 2026 ACS Omega paper by Universiti Sains Malaysia authors
  (10.1021/acsomega.6c06914, created 2026-10-07) carries an FRGS number on Egypt's ID.

In every raw record re-read below, the ID was **deposited by the publisher**
(`doi-asserted-by: publisher`). In the sample, 198 of 199 entries were publisher-asserted; the
other one (10.1039/c8nr02647e, labelled unclear) was asserted by Crossref.

## Not just a picker choosing between two equal labels

Some works carry Egypt's ID under a name that says Malaysia (or Taiwan):

- 10.1109/icocet63343.2024.10730485 (IEEE): entry named "Ministry of Higher Education of
  Malaysia (MOHE)", award `LRGS/1/2020/UM/01/5/4 (9012-00010)`, first author at Universiti
  Malaysia Perlis. Re-read raw.
- 10.1016/j.porgcoat.2014.12.012 (Elsevier, created 2015-01-29): entry named "Ministry of Higher
  Education, Malaysia (MOHE)". Re-read raw.
- 10.1109/icocet63343.2024.10730571 (IEEE): "Malaysian Ministry of Higher Education (MOHE)",
  award `FRGS /1/2021/STG07/UITM/02/4`.
- 10.1109/twc.2024.3422399 (IEEE): entry named "Higher Education SPROUT Project of the Ministry of
  Education, Taiwan ...", next to Chinese and Taiwanese funders. Re-read raw.

The record's funder-name facet agrees: across the 4,177 works, "Ministry of Higher Education,
Malaysia" appears 140 times and "Malaysia Ministry of Higher Education" 87 times (on any entry
of those works), next to 191 Universiti Teknologi Malaysia entries and 42 "Fundamental Research
Grant Scheme" entries. Egyptian names appear less often ("Egyptian Ministry of Higher Education"
66, "Ministry of Higher Education, Egypt" 29, "Egypt Ministry of Higher Education" 17,
Egypt-Japan University of Science and Technology 95).

## How it was measured

- Registry search: `api.crossref.org/funders?query=Ministry+of+Higher+Education&rows=100`
  (40 results). ROR: `api.ror.org/v2/organizations?query=501100002385`.
- Counts and facets: `works?filter=funder:10.13039/501100002385&rows=0&facet=publisher-name:15,funder-name:30`.
- Random samples: `works?filter=funder:10.13039/501100002385&sample=100&select=DOI,funder,created`
  (two draws of 100 with different parameter order; 1 work appeared in both and is counted once).
- Each row was labelled by hand from (a) the award number on the Egyptian entry, (b) the entry's
  own name and (c) the other funders on the same work. Labels: `foreign:<country>`, `EG`, or
  `unclear`. Rows whose only other funders were Western agencies (DFG, ANR, British Heart
  Foundation, Spain's MINECO and the like) were left **unclear**, because Egypt's ministry funds
  Egyptian researchers abroad. Malaysian universities (Universiti ..., University of Malaya, IIUM,
  Management and Science University, Taylor's University) count as Malaysian co-funders.
- **Award-number tier**: the label rests on the grant number's own format. **Hand tier**: award
  number, entry name or co-funders.
- The labels were assigned by AI agents reading API output, not by a shipped regex. Rows are in
  [data/mohe-eg-sample-2026-11-15.csv](data/mohe-eg-sample-2026-11-15.csv), with
  `award_format_tier` and `raw_checked` columns.

| Tier | Foreign | of which Malaysia | Egypt | Unclear | Foreign share (95% Wilson) |
|---|---|---|---|---|---|
| Award number | 43 | 40 | - | - | 21.6% (16.5% to 27.8%), a floor |
| Hand (award, name or co-funders) | 92 | 79 | 14 | 93 | 46.2% (39.4% to 53.2%) |

- **Publishers** of the 4,177 works: Elsevier 1,538 (two name forms), IEEE 1,583 (two name forms),
  Wiley 288, Springer Nature 185, Taylor & Francis (Informa) 172, ACS 84, MDPI 80, OUP 63, RSC 42.
- Many of the unclear rows are IEEE conference papers with no award and no co-funder, from
  conference series held in Malaysia (ICSPC, SCOReD, I2CACIS, ICSIMA, ISCAIE, ICCCE, ICSIPA).
  The venue was **not** used as evidence, so the true Malaysian share is probably higher than 39.7%.

Raw records re-read (all publisher-asserted):

- 10.1021/acsomega.6c06914 (ACS, created 2026-10-07): award `FRGS/1/2025/TK09/USM/02/4`; all
  authors at Universiti Sains Malaysia.
- 10.1109/icocet63343.2024.10730485 (IEEE): see above.
- 10.1016/j.porgcoat.2014.12.012 (Elsevier): see above.
- 10.1109/twc.2024.3422399 (IEEE): see above.

## Why it is new

We searched the web, the Crossref community forum and GitHub for the ID and for Malaysian FRGS
grants under an Egyptian funder, and found no report. Registry browsers (for example KCSE's) list
the record correctly as Egypt's. Earlier studies of funder metadata measured missing or
unmatched funders, not grants filed under another country's same-named record.

## The series so far

| Record (main name, country) | Works | Foreign share in random sample |
|---|---|---|
| National Research Foundation (South Africa) | 39,201 | 22.5% by grant number (FINDINGS-NRF-1) |
| Ministry of Education (Thailand) | 6,896 | 105 of 200 with co-funders (FINDINGS-MOE-1) |
| Ministry of Science and Technology (Vietnam) | 10,597 | 59.2% by grant number (FINDINGS-MOST-1) |
| Ministry of Science and Technology (South Korea) | 7,033 | 50% by grant number (FINDINGS-MOST-1) |
| Ministry of Health (Jamaica) | 1,913 | 66.5% hand; 24.4% by grant number (FINDINGS-MOH-1) |
| Ministry of Health and Welfare (Taiwan) | 2,843 | 24.7% hand; 21.0% by grant number (FINDINGS-MOH-1) |
| **Ministry of Higher Education (Egypt)** | **4,177** | **46.2% hand; 21.6% by grant number** |

## Limits

- A sample, not a census. A scripted count of the whole record is pre-registered in
  [PREREG-MOHE-1.md](PREREG-MOHE-1.md).
- Labels were assigned by AI agents from API output; only the rows marked `raw_checked` were
  re-read from the single-record API. A row labelled foreign means its award number, entry name
  or co-funders point elsewhere, not that the authors were checked.
- "Unclear" rows may be Egyptian. Even if all 93 were Egyptian, 92 of 199 would still be foreign.
- Egypt's ministry funds a great deal of research and many scholarships, so much of the record
  is genuine.

## Suggested fixes (for whoever curates the registry)

- Show the country in the main name: "Ministry of Higher Education (Egypt)". The same applies to
  ROR's display name for `0512bh102`.
- Works whose Egyptian entry carries an `FRGS/`, `LRGS/` or other Malaysian grant number, or whose
  entry name contains "Malaysia", could be re-pointed by rule to 10.13039/501100003093.

Disclosure: found, checked and written by AI agents working in MV2's name. MV2, Munim, Inc.,
mv2@munimtech.com.
