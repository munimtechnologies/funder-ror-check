# FINDINGS-MOHESR-1: Korean, Chinese and Singaporean "Ministry of Education" grants filed under the UAE's former ministry

By MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-16. Made with AI agents working in MV2's name;
not reviewed by a human. Text and data CC BY 4.0.

## In short

This is the eighth case in the series on Crossref Funder Registry records that collect other
countries' grants (after FINDINGS-NRF-1, FINDINGS-MOE-1, FINDINGS-MOST-1, FINDINGS-MOH-1 and
FINDINGS-MOHE-1). It is the most lopsided one so far.

- **10.13039/100009122** is the United Arab Emirates' "Ministry of Higher Education and Scientific
  Research" (registry location United Arab Emirates; ROR `00kab6t91`, country AE). The UAE
  folded that ministry into its Ministry of Education years ago; the registry record has no
  `replaced-by`. Its **alternate names include the bare "Ministry of Education" and "MOE"**,
  next to "UAE Ministry of Education" and "MOHESR". Its main name is also, word for word, the name
  of the higher-education ministries of Iraq, Algeria, Tunisia, Libya and others.
- The record carries **1,763 works** (Crossref API, 2026-11-16), **208 of them created in 2026**.
- In two random draws (**198 distinct works**), only **5 show a sign of the UAE**. **150 point to
  another country** (75.8%; 95% Wilson interval 69.3% to 81.2%; roughly **1,220 to 1,430 works**
  across the record), and 43 are unclear. Even if every unclear row were Emirati, the UAE's share
  of the sample would be at most 48 of 198 (24%).
- **South Korea alone: 51 of 198** (25.8%; 20.2% to 32.3%), 46 of them with a Korean National
  Research Foundation grant number on the UAE entry itself (`2021R1I1A3052320`,
  `RS-2023-00241749`, `NRF-2022R1A2C1003624` and similar). Then China 25, Taiwan 11, Singapore 10,
  Malaysia 8, Algeria 8, Tunisia 8, India 6, Japan 4, Iraq 4, Czech Republic 3, Saudi Arabia 3,
  Spain 2, Indonesia 2, France 2, and one each from Libya, Poland and Brazil.
- **By grant number alone, 79 of 198 (39.9%; 33.3% to 46.8%)** carry another country's award
  format on the UAE entry: a floor of roughly 590 to 830 works.
- It is still happening: **21 of the 23 sampled works created in 2026 point to another country**;
  none points to the UAE. The newest, 10.1093/bib/bbag603 (OUP, created November 2026), carries
  `RS-2025-25441317` on an entry named "Ministry of Education".

196 of the 198 UAE entries in the sample were deposited by the publisher
(`doi-asserted-by: publisher`). The other two were added by Crossref's matcher, one of them on an
Algerian grant (below).

## Two ways in

1. **The bare alternate name "Ministry of Education".** Across the record's works, the
   funder-name facet counts **830 entries named exactly "Ministry of Education"**, 28 named
   "MOE" and 11 "Ministry of Education (MOE)", against 706 named "Ministry of Higher Education
   and Scientific Research". Korea's own record (10.13039/501100002701, main name "Ministry of
   Education", location South Korea, 52,898 works) exists, but publishers' pickers sent these
   grants to the UAE's ID. Some Wiley deposits even replace the author's
   name with the UAE record's: 10.1002/celc.202200093 (re-read raw) has an entry named
   "Ministry of Higher Education and Scientific Research" carrying Korean NRF number
   `2021R1I1A3052320`, next to the National Research Foundation of Korea.
2. **The shared main name.** 21 sampled works come from Iraq (4), Algeria (8), Tunisia (8) and
   Libya (1), whose ministries carry exactly the same English name. Iraq has its own record
   (10.13039/501100007335); two sampled works carry both IDs.

Some entries say outright that they are someone else, which no name match can explain:

- 10.1109/cvpr52733.2024.00944 (IEEE): the only funder entry is named "Singapore Ministry of
  Education (MOE)" and carries the UAE's ID. Re-read raw.
- 10.1109/ppps56198.2025.11248256 (IEEE, created 2025-11-28): an entry named "Korea Ministry of
  Environment", award `2023003660001`, carries the UAE's ID. Re-read raw.
- 10.1109/access.2026.3678997 (IEEE, created 2026-03-30): "Ministry of Higher Education (MOHE),
  Malaysia, through the Fundamental Research Grant Scheme", award `FRGS/1/2021/TK0/UKM/02/9`.
  Re-read raw. (Malaysia's ministry has its own record, 10.13039/501100003093.)
- 10.1007/s13738-024-03110-x (Springer, 2024): "Ministry of Higher Education and Scientific
  Research MESRS", award `B00L01UN400120210002 (PRFU)` (an Algerian university project code). Here
  **Crossref** added the UAE's ID (`doi-asserted-by: crossref`). Re-read raw.
- Others in the sample: "Ministry of Education (MoE), Govt. of India"; "Tunisian Ministry of
  Higher Education and Scientific Research"; "... of the Algerian Government"; "Iraqi Ministry
  of Higher Education and Scientific Research"; "(MOHESR), Libya"; a Polish AGH University
  programme; two French Brittany region entries.

## How it was measured

- Record: `api.crossref.org/funders/100009122`. ROR: `api.ror.org/v2/organizations/00kab6t91`.
- Counts and facets: `works?filter=funder:10.13039/100009122&rows=0&facet=publisher-name:15,funder-name:40,published:30`
  and the same with `from-created-date:2026-01-01`.
- Random samples: `works?filter=funder:10.13039/100009122&sample=100&select=DOI,funder,created,publisher`
  (two draws of 100 with different parameter order; 2 works appeared in both and are counted once).
- Each row was labelled by hand from (a) the award number on the UAE entry, (b) the entry's own
  name and (c) the other funders on the same work. Labels: `foreign:<country>`, `AE`, or
  `unclear`. Rows whose only other funders were Western or other agencies that host foreign
  students (EPSRC, ERC, Austrian FWF, Quebec FCAR, Brazil's CNPq on a "MOHESR" entry, Czech
  agencies without a ministry name) were left **unclear**, because the UAE funds Emirati
  researchers abroad.
- **Award-number tier**: the label rests on the grant number's own format (Korean NRF
  `20xxR1...`/`RS-20xx-...`, Singapore `MOE20xx-T2-...`/`T2EP...`, Malaysian `FRGS/...`, Chinese
  `NCET-`/`IRT_`/`17YJC...`, Algerian PRFU, Tunisian `LR..`, Japanese `JP..H.....`, Indian STARS,
  Czech `CZ.02.`/`OPVVV`, Spanish `PID`/`TIN`/`FPU`, Saudi `IFP...UQU...`, Taiwan MOE). **Hand
  tier**: award number, entry name or co-funders.
- The labels were assigned by AI agents reading API output, not by a shipped regex. Rows are in
  [data/mohesr-ae-sample-2026-11-16.csv](data/mohesr-ae-sample-2026-11-16.csv), with
  `award_format_tier` and `raw_checked` columns.

| Tier | Foreign | of which Korea | UAE | Unclear | Foreign share (95% Wilson) |
|---|---|---|---|---|---|
| Award number | 79 | 46 | - | - | 39.9% (33.3% to 46.8%), a floor |
| Hand (award, name or co-funders) | 150 | 51 | 5 | 43 | 75.8% (69.3% to 81.2%) |

- **Publishers** of the 1,763 works: Wiley 442, OUP 344, IEEE 416 (two name forms), Taylor &
  Francis (Informa) 263, Elsevier 186, then Springer 14, SAGE 11, Optica 11, APS 11, ACS 10.
  Of the 208 created in 2026: OUP 68, IEEE 82, Informa 41, Elsevier 6, Wiley 4.
- The 5 UAE rows: an entry named "UAE Ministry of Education" with Khalifa University
  (10.3390/en17102293); one named "United Arab Emirates Ministry of Higher Education and
  Scientific Research" (10.1016/j.compind.2024.104225); United Arab Emirates University as
  co-funder with award `G00003563` (10.1016/j.ultsonch.2024.107015), and the same award on
  10.1016/j.ijbiomac.2024.135593; and the UAE Research Program for Rain Enhancement Science
  (10.5194/acp-22-10099-2022).

Raw records re-read (single-record API): 10.1002/celc.202200093, 10.1093/llc/fqag003
(created 2026-01-15, `RS-2023-00241749`), 10.1128/aem.00286-26 (created 2026-05-05,
`2020R1I1A1A01065541, RS-2023-00273372`), 10.1109/cvpr52733.2024.00944,
10.1109/ppps56198.2025.11248256, 10.1109/access.2026.3678997, 10.1007/s13738-024-03110-x. All
matched the sample listing.

## Why it is new

We searched the web, the Crossref community forum and ror-updates for the ID and the ROR ID, and
found no report. The only ror-updates mention of `00kab6t91` is a triage bot listing it among
same-named candidates when Yemen's ministry was added (ror-updates #29605). Registry browsers
(for example KCSE's) list the record correctly as the UAE's. Earlier studies of funder metadata
measured missing or unmatched funders, or NSF/NIH look-alikes in DataCite (Metadata Game
Changers), not grants filed under another country's same-named record.

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
| **Ministry of Higher Education and Scientific Research (UAE)** | **1,763** | **75.8% hand; 39.9% by grant number** |

## Limits

- A sample, not a census. A scripted count of the whole record is pre-registered in
  [PREREG-MOHESR-1.md](PREREG-MOHESR-1.md).
- Labels were assigned by AI agents from API output; only the 7 rows marked `raw_checked` were
  re-read from the single-record API. A row labelled foreign means its award number, entry name
  or co-funders point elsewhere, not that the authors were checked.
- Iraqi, Algerian, Tunisian and Libyan rows may be the publisher picking the right name but the
  wrong country; they are still other countries' grants on the UAE's ID.
- The UAE and Korea run some joint research calls; none of the 51 Korean rows names a UAE
  funder or programme.

## Suggested fixes (for whoever curates the registry)

- Drop the bare alternate names "Ministry of Education" and "MOE" from 10.13039/100009122 (keep
  "UAE Ministry of Education" and "Ministry of Education UAE"), and show the country in the main
  name: "Ministry of Higher Education and Scientific Research (United Arab Emirates)". The same
  applies to ROR's display name for `00kab6t91`.
- Works whose UAE entry carries a Korean NRF number (`20xxR1...`, `RS-20xx-...`) could be
  re-pointed by rule to Korea's Ministry of Education (10.13039/501100002701); Singapore
  `MOE20xx-T`/`T2EP` numbers to Singapore's ministry; `FRGS/` numbers to 10.13039/501100003093.

Disclosure: found, checked and written by AI agents working in MV2's name. MV2, Munim, Inc.,
mv2@munimtech.com.
