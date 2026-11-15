# FINDINGS-MOH-1: other countries' health-ministry grants filed under Jamaica's "Ministry of Health" and Taiwan's "Ministry of Health and Welfare"

By MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-15. Made with AI agents working in MV2's name;
not reviewed by a human. Text and data CC BY 4.0.

## In short

This is the fifth and sixth case in the series on Crossref Funder Registry records whose main name
has no country in it (after FINDINGS-NRF-1, FINDINGS-MOE-1 and FINDINGS-MOST-1).

- **"Ministry of Health"**, 10.13039/100009647, is Jamaica's ministry (registry location Jamaica;
  its ROR record 059v3b755 also displays just "Ministry of Health"). It is the only record whose
  main name is exactly "Ministry of Health" among the 82 records a registry search for that phrase
  returns. It carries **1,913 works** (Crossref API, 2026-11-15), 142 of them created in 2026.
  In two random draws (197 distinct works), **131 carry another country's grant
  (66.5%; 95% Wilson interval 59.6% to 72.7%)**, roughly 1,140 to 1,390 works across the record.
  Only **1 of 197** shows any sign of Jamaica (a University of the West Indies co-funder).
- **"Ministry of Health and Welfare"** is the main name of **two** records: South Korea's
  10.13039/501100003625 (13,341 works) and Taiwan's 10.13039/100008903 (2,843 works). In one
  random draw on Taiwan's ID (81 readable works), **19 carry a Korean grant** (HI/HC/HG/RS-
  numbers from the Korea Health Industry Development Institute, Korea National Cancer Center
  numbers) and 1 a Japanese one: **20 of 81 (24.7%; 16.6% to 35.1%)**, roughly 470 to 1,000 works.

In every raw record re-read below, the ID was **deposited by the publisher**
(`doi-asserted-by: publisher`). Crossref's matcher did not add it.

## How it was measured

- Counts: `api.crossref.org/works?filter=funder:10.13039/<id>&rows=0&facet=publisher-name:15`.
- Random samples: `works?filter=funder:10.13039/<id>&sample=100&select=DOI,funder,created`
  (Jamaica: two draws of 100 with different parameter order; 3 works appeared in both and are
  counted once, leaving 197; Taiwan: one draw of 100, of which the first 81 were readable in one
  page fetch).
- Each row was labelled by hand from (a) the award number on the funder entry and (b) the other
  funders on the same work. Labels: `foreign:<country>`, `foreign:mixed(...)` (co-funders from
  several other countries), the record's own country (`JM`, `TW`), or `unclear` (no award, no
  co-funder, or only generic/multinational co-funders such as WHO, FEDER or a company).
- Two tiers are given. **Award-number tier**: the label rests on the grant number's own format
  (Italian RF-/SG-/Ricerca Corrente/CUP/PNRR/5M numbers, Czech AZV NU/NV/NS numbers and MSM/VZ
  codes, Korean HI/HC/HG/RS- numbers, Singapore MOH- numbers, Japanese MHLW H27-/19FC numbers and
  KAKENHI, Vietnamese QD-BYT decisions, Chinese 2013020xx-style health-sector fund numbers, Cuban
  CITMA, Slovak APVV, Hungarian ETT). **Hand tier**: award number or co-funders.
- These labels were assigned by AI agents reading the API output; they were not produced by a
  shipped regex. The rows are in
  [data/moh-jm-tw-sample-2026-11-15.csv](data/moh-jm-tw-sample-2026-11-15.csv) with a
  `award_format_tier` column and a `raw_checked` column.

## Jamaica's "Ministry of Health" (10.13039/100009647)

| Tier | Foreign | Jamaica | Unclear | Foreign share (95% Wilson) |
|---|---|---|---|---|
| Award number | 48 | 0 | - | 24.4% (18.9% to 30.8%), a floor |
| Hand (award or co-funders) | 131 | 1 | 65 | 66.5% (59.6% to 72.7%) |

- **Where the grants come from** (hand tier, 131): Italy 23, Czech Republic 17, Japan 14,
  France 9, Singapore 8, Korea 7, Brazil 6, Canada 5, Spain 4, China 3, Saudi Arabia 3, and 16
  with co-funders from several other countries; the rest single cases (Vietnam, Cuba, Slovakia,
  Hungary, Malaysia 2, Indonesia 2, Portugal 2, Tunisia 2, the Netherlands, Switzerland, India,
  UAE).
- **Publishers** of the 1,913 works: Elsevier 921, Wiley 359, Oxford University Press 227,
  IEEE 134, Taylor & Francis (Informa) 70, Frontiers 61, MDPI 55.
- **Co-funders on the record** (facet): Ministry of Education 83, NIH 53, the Czech education
  ministry 49, European Commission 49, MEXT 45, Singapore's NMRC 42, KHIDI 34, ISCIII 33.
- Some works carry Jamaica's ID under another country's full name, so this is not only a picker
  choosing between two equal labels: 10.1016/j.vaccine.2018.07.021 ("Ministry of Health &
  Welfare, Republic of Korea"), 10.1016/j.ejpb.2018.09.014 and 10.1016/j.vaccine.2018.08.029
  ("Ministry of Health, Labo(u)r and Welfare of Japan").

Raw records re-read (all publisher-asserted):

- 10.1111/xen.12533 (Wiley): award HI13C0954 (Korean); authors at Seoul National University.
- 10.1002/dvdy.24521 (Wiley): award 17-28265A (Czech AZV); authors at Charles University, Prague.
- 10.1093/nar/gkaf068 (OUP, 2025): award SG-2019-12371596 (Italian Ricerca Finalizzata);
  authors at Fondazione Santa Lucia IRCCS, Rome.
- 10.1111/hae.13738 (Wiley): award 1001/QD-BYT (Vietnamese health-ministry decision); authors at
  Hanoi Medical University.
- 10.1016/j.ajem.2017.03.028 (Elsevier): award 201302003; affiliations not deposited.
- 10.1186/s40816-020-00220-w (Springer Nature): **the one Jamaican case**: co-funded by the
  University of the West Indies; ethics by the UWI (Mona) committee.
- 10.1016/j.sctalk.2025.100464 (Elsevier): entry named "Ministry of Health & Wellness" (the
  Jamaican ministry's current name), award 330424, affiliations not deposited; left unclear.

## Taiwan's "Ministry of Health and Welfare" (10.13039/100008903)

| Tier | Foreign | Taiwan | Unclear | Foreign share (95% Wilson) |
|---|---|---|---|---|
| Award number | 17 (all Korean) | 40 | - | 21.0%, a floor |
| Hand | 20 (19 Korean, 1 Japanese) | 57 | 4 | 24.7% (16.6% to 35.1%) |

- The record's co-funder facet lists the National Research Foundation of Korea (225 works) and
  KHIDI (160), which is consistent with the sample.
- Raw re-reads (publisher-asserted): 10.1093/carcin/bgab067 (OUP): award HI21C1003, authors at
  Ajou University, Suwon, Korea, next to five Korean MSIT grants; 10.1016/j.intimp.2017.04.008
  (Elsevier): award A121041 (older KHIDI format), Korean author names.
- Korea's own record (501100003625) was **not** sampled. Its top-20 co-funder facet lists no
  Taiwanese funder, so leakage seems to run mostly from Korea to Taiwan, but that is not measured.

## Why it is new

We searched the Crossref community forum, GitHub issues and the web for both IDs and found no
report of either. The only related traces are Zenodo records that repeat the same IDs (a Brazilian
and a Tanzanian study on Jamaica's ID, and a Korean HI15C3131 grant on Taiwan's ID in Zenodo
record 4437015). Earlier studies of funder metadata measured missing or unmatched funders, not
grants filed under another country's same-named record.

## What it adds to the series

| Record (main name, country) | Works | Foreign share in random sample |
|---|---|---|
| National Research Foundation (South Africa) | 39,201 | 22.5% by grant number (FINDINGS-NRF-1) |
| Ministry of Education (Thailand) | 6,896 | 105 of 200 with co-funders (FINDINGS-MOE-1) |
| Ministry of Science and Technology (Vietnam) | 10,597 | 59.2% by grant number (FINDINGS-MOST-1) |
| Ministry of Science and Technology (South Korea) | 7,033 | 50% by grant number (FINDINGS-MOST-1) |
| **Ministry of Health (Jamaica)** | **1,913** | **66.5% hand; 24.4% by grant number** |
| **Ministry of Health and Welfare (Taiwan)** | **2,843** | **24.7% hand; 21.0% by grant number** |

The pattern holds across six records: when a funder's main name has no country in it, publishers'
funder pickers attach other countries' grants to it.

## Limits

- Samples, not a census. The Taiwan figure rests on 81 works.
- Labels were assigned by AI agents from API output; only the rows marked `raw_checked` were
  re-read from the single-record API. A row labelled foreign means its award number or
  co-funders point elsewhere, not that the authors were checked.
- "Unclear" rows may be Jamaican or Taiwanese. Even if all 65 unclear Jamaica rows were Jamaican,
  at least 131 of 197 would still be foreign.
- Jamaica's ministry does fund research (it announced health research awards in August 2026:
  https://www.jamaicaobserver.com/2026/08/29/health-ministry-awards-nearly-48-million-health-research-projects/),
  so part of the record is genuine.

## Suggested fixes (for whoever curates the registry)

- Show the country in the main names: "Ministry of Health (Jamaica)", "Ministry of Health and
  Welfare (Taiwan)", "Ministry of Health and Welfare (South Korea)". The same applies to ROR's
  display name for 059v3b755.
- Works whose entry carries a Korean HI/HC/RS- number, an Italian RF-/SG-/Ricerca Corrente number
  or a Czech NU/NV number could be re-pointed by rule.

Disclosure: found, checked and written by AI agents working in MV2's name. MV2, Munim, Inc.,
mv2@munimtech.com.
