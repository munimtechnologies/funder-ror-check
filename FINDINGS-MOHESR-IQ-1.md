# FINDINGS-MOHESR-IQ-1: Algerian and Tunisian grants filed under Iraq's "Ministry of Higher Education and Scientific Research"

By MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-16. Made with AI agents working in MV2's name;
not reviewed by a human. Text and data CC BY 4.0.

## In short

This is the ninth case in the series on Crossref Funder Registry records that collect other
countries' grants (after FINDINGS-NRF-1, FINDINGS-MOE-1, FINDINGS-MOST-1, FINDINGS-MOH-1,
FINDINGS-MOHE-1 and FINDINGS-MOHESR-1). This one has no bare alternate name to blame. It comes
from **one English name shared by seven countries' records**.

- **10.13039/501100007335** is Iraq's "Ministry of Higher Education and Scientific Research"
  (registry location Iraq; only alternate name "MHESR"; ROR `03m5ehy13`, country IQ). It carries
  **887 works** (Crossref API, 2026-11-16), **70 of them created in 2026**.
- In two random draws (**187 distinct works**), **59 point to another country** (31.6%; 95% Wilson
  interval 25.3% to 38.5%; roughly **225 to 340 works** across the record), **27 point to Iraq**
  and 101 are unclear.
- **Algeria 21 and Tunisia 21** make up most of the foreign rows. Then Egypt 6, Libya 4,
  Morocco 2, Malaysia 2, and one each from France, Jordan and Germany.
- **By grant number alone, 13 of 187 (7.0%; 4.1% to 11.5%)** carry another country's award format
  on the Iraq entry itself: Tunisian laboratory codes (`LR14ES08`, `LR11ES31`, `LRCBS05`,
  `UR13AGR09` ...), Algerian PRFU project codes (`D01N01UN230120190005`), a Malaysian FRGS grant
  (`FRGS15-203-0444`) and a German BMBF grant (`16SV7111`).
- It is still happening: of the 16 sampled works created in 2026, **7 point to another country
  (6 Algerian, 1 Tunisian) and 6 to Iraq**. Across all 70 works created in 2026, the funder-name
  facet shows Algeria's DGRSDT (10.13039/501100005307) on 12 of them.

All Iraq entries in the sample were deposited by the publisher (`doi-asserted-by: publisher`),
except two that Crossref's matcher added to entries naming Kurdistan (both Iraqi).

## One name, seven records

`api.crossref.org/funders?query=Ministry+of+Higher+Education+and+Scientific+Research` returns
these records whose main or alternate name is exactly "Ministry of Higher Education and
Scientific Research" (2026-11-16):

| Funder ID | Registry location | How the name appears |
|---|---|---|
| 501100007335 | Iraq | main name, no country |
| 100010450 | Libya | main name, no country |
| 100017057 | Egypt | main name, no country |
| 100009122 | United Arab Emirates | main name, no country (FINDINGS-MOHESR-1) |
| 100031330 | United Arab Emirates | alternate name |
| 100012964 | Tunisia | alternate name (main name in French) |
| 501100002717 | Algeria | alternate name (main name in French) |

A publisher's funder picker that shows names without countries offers four identical
"Ministry of Higher Education and Scientific Research" entries. Iraq's is one of them, and it is
the one that collects Algerian and Tunisian grants, whose authors usually write the English name.

## Entries that say who they are

The entry's own name sometimes names another country or body, but it carries Iraq's ID. Each of
these was re-read from the single-record API (`api.crossref.org/works/<doi>`):

- 10.1080/0144929x.2016.1278561 (Informa, created 2017-01): the only funder entry is named
  **"German Federal Ministry of Education and Research"**, award `16SV7111`, ID 501100007335.
  Authors at RWTH Aachen.
- 10.1080/00305316.2023.2187892 (Informa, 2023): **"Ministry of Higher Education and Scientific
  Research of Algeria"**, award `D01N01UN230120190005` (Algerian PRFU), Iraq's ID. Study area in
  Algeria.
- 10.1016/j.ijhydene.2018.10.208 (Elsevier, 2018): **"Tunisian Ministry of Higher Education and
  Scientific Research"**, Iraq's ID.
- 10.1080/00202967.2019.1551284 (Informa, 2018): "Ministry of Higher Education", award
  `FRGS15-203-0444` (Malaysia's Fundamental Research Grant Scheme), Iraq's ID.
- 10.1021/acsomega.3c03772 (ACS, 2023): award `LR14ES08` on Iraq's entry; first author at the
  University of Sfax, Tunisia.
- 10.1016/j.ces.2016.06.055 (Elsevier, 2016): two entries with the same name, one with Libya's ID
  (100010450) and one with Iraq's. Three more sampled works carry both Libya's or Egypt's
  same-named record and Iraq's.

Also in the sample, not re-read: 10.1016/j.jappgeo.2020.104145, an entry named "... of Algeria"
with Iraq's ID; 10.1016/j.jtumed.2019.01.003, Iraq's ID on an entry named "University of Duhok"
(an Iraqi university, so the right country but the wrong body).

## How it was measured

- Record: `api.crossref.org/funders/501100007335`. ROR: `api.ror.org/v2/organizations/03m5ehy13`.
- Counts and facets: `works?filter=funder:10.13039/501100007335&rows=0&facet=publisher-name:15,funder-name:40,published:30`
  and the same with `from-created-date:2026-01-01`.
- Random samples: `works?filter=funder:10.13039/501100007335&sample=100&select=DOI,funder,created,publisher`
  (two draws of 100 with different parameter order; 13 works appeared in both and are counted once).
- Each row was labelled by hand from (a) the award number on the Iraq entry, (b) the entry's own
  name and (c) the other funders on the same work. Labels: `foreign:<country>`, `IQ`, or `unclear`.
  Iraq sends many doctoral students abroad on ministry scholarships, so rows whose only other
  funders were British, Australian, Canadian, Japanese, Spanish, Malaysian-university or other
  host agencies were left **unclear**. Iraqi signs: an Iraqi university or HCED as co-funder, or
  "Iraq", "Iraqi" or "Kurdistan" in the entry's name.
- **Award-number tier**: the label rests on the grant number's own format. **Hand tier**: award
  number, entry name or co-funders (for example Algeria's DGRSDT or its ministry record
  501100002717, Tunisia's ministry records 100012964 and 501100004409, Libya's or Egypt's
  ministry record, Morocco's CNRST, Egypt's STDF).
- The labels were assigned by AI agents reading API output, not by a shipped regex. Rows are in
  [data/mohesr-iq-sample-2026-11-16.csv](data/mohesr-iq-sample-2026-11-16.csv), with
  `award_format_tier` and `raw_checked` columns.

| Tier | Foreign | of which Algeria + Tunisia | Iraq | Unclear | Foreign share (95% Wilson) |
|---|---|---|---|---|---|
| Award number | 13 | 11 | - | - | 7.0% (4.1% to 11.5%), a floor |
| Hand (award, name or co-funders) | 59 | 42 | 27 | 101 | 31.6% (25.3% to 38.5%) |

- **Publishers** of the 887 works: Elsevier 571, ACS 134, Wiley 47, IEEE 44 (two name forms),
  Informa 30, RSC 13, Springer 12, Optica 8.
- Funder-name facet over all 887 (facet counts, approximate): Algeria's DGRSDT appears 45 times
  under its French name and 7 under its English name; "Enseignement Supérieur et de la Recherche
  Scientifique" (Tunisia's record) 18 times; and "Ministère de l'Enseignement Supérieur et de la
  Recherche Scientifique" (the French name both Algeria and Tunisia use) 30 times across three
  spellings.

## Why it is new

We searched the web and ror-updates for the Funder ID, the ROR ID and the name, and found no
report that Iraq's record collects other countries' grants. The ror-updates issues on same-named
ministries concern other records (for example #41936, where a curator refused to conflate Libya's
Tripoli and Benghazi ministries, and #44087, an open request to merge two Egyptian ministry
records). A study of research funding in the Middle East and North Africa (arXiv 2310.04426)
kept full funder names, adding the country where the text allowed, to avoid confusing funders
that share acronyms across countries; it did not measure grants filed under another country's
Crossref Funder ID.

## The series so far

| Record (main name, country) | Works | Foreign share in random sample |
|---|---|---|
| National Research Foundation (South Africa) | 39,201 | 22.5% by grant number (FINDINGS-NRF-1) |
| Ministry of Education (Thailand) | 6,896 | 105 of 200 with co-funders (FINDINGS-MOE-1) |
| Ministry of Science and Technology (Vietnam) | 10,597 | 59.2% by grant number (FINDINGS-MOST-1) |
| Ministry of Science and Technology (South Korea) | 7,033 | 50% by grant number (FINDINGS-MOST-1) |
| Ministry of Health (Jamaica) | 1,913 | 66.5% hand; 24.4% by grant number (FINDINGS-MOH-1) |
| Ministry of Health and Welfare (Taiwan) | 2,843 | 24.7% hand; 21.0% by grant number (FINDINGS-MOH-1) |
| Ministry of Higher Education (Egypt) | 4,177 | 46.2% hand; 21.6% by grant number (FINDINGS-MOHE-1) |
| Ministry of Higher Education and Scientific Research (UAE) | 1,763 | 75.8% hand; 39.9% by grant number (FINDINGS-MOHESR-1) |
| **Ministry of Higher Education and Scientific Research (Iraq)** | **887** | **31.6% hand; 7.0% by grant number** |

## Limits

- A sample, not a census. No scripted census was filed for this record, because seven earlier
  pre-registered censuses in the series are still waiting for compute.
- Labels were assigned by AI agents from API output; only the 6 rows marked `raw_checked` were
  re-read from the single-record API. A row labelled foreign means its award number, entry name
  or co-funders point elsewhere, not that the authors were checked.
- Over half the sample is unclear. Most unclear rows carry Iraq's ID with no award and no other
  funder, so they could be from any of the seven countries above; Iraq is the likeliest home for
  many of them. Even if every unclear row were Iraqi, at least 59 of 187 would still be foreign.
- A work labelled Algerian or Tunisian may also have Iraqi co-authors. None of the 42 Algerian or
  Tunisian rows names an Iraqi university or an Iraqi programme.

## Suggested fixes (for whoever curates the registry)

- Show the country in the main name of all four records named exactly "Ministry of Higher
  Education and Scientific Research" (Iraq 501100007335, Libya 100010450, Egypt 100017057, UAE
  100009122), for example "Ministry of Higher Education and Scientific Research (Iraq)". The same
  applies to ROR's display name for `03m5ehy13`.
- Works whose Iraq entry carries a Tunisian `LR`/`UR` laboratory code could be re-pointed by rule to
  Tunisia's ministry (10.13039/100012964), and works with an Algerian PRFU code to Algeria's
  (10.13039/501100002717).

Disclosure: found, checked and written by AI agents working in MV2's name. MV2, Munim, Inc.,
mv2@munimtech.com.
