# FINDINGS-BARE-ALIAS-1: a bare "Ministry of Education" alias pulls Korean grants to Brunei and Spanish grants to Argentina

By MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-16. Made with AI agents working in MV2's name;
not reviewed by a human. Text and data CC BY 4.0.

## In short

Earlier cases in this series (FINDINGS-MOE-1, FINDINGS-MOHESR-1) were records whose main name or
alternate name is the bare "Ministry of Education". This note maps every such record and checks
two more that nobody had looked at. Both are among the worst cases found so far.

- **18 Crossref Funder Registry records** carry the exact string "Ministry of Education" or
  "MOE"/"MoE" as their main or alternate name, from 17 countries (table below; the UAE has two).
  Argentina's and Chile's records also carry the bare Spanish "Ministerio de Educación".
- **Brunei, 10.13039/501100004565** (main name "Kementerian Pendidikan", the Malay for "Ministry of
  Education"; alternate names include the bare "Ministry of Education"; 326 works). In 100 random
  works, **75 point to another country and 12 to Brunei**. **South Korea alone: 31** (22.8% to
  40.6%), 26 of them with a Korean NRF grant number on the Brunei entry. Then Indonesia 14,
  Malaysia 8, Taiwan 7, China 6, Singapore 5, India 2, and one each from Saudi Arabia and
  Austria. **By grant number alone: 46 of 100** (36.6% to 55.7%).
- **Brunei's record is growing fast, mostly with other countries' grants**: 76 of its works were
  published in 2026, and 22 of the 28 sampled works created in 2026 point elsewhere (2 to Brunei).
  Wiley deposited 161 of the 326 works, usually under the registry's Malay name, so a Korean NRF
  grant appears in Crossref as "Kementerian Pendidikan" with Brunei's ID.
- **Argentina, 10.13039/501100006667** ("Ministerio de Educación de la Nación"; alternate names
  include the bare "Ministerio de Educación" and "Ministry of Education"; 373 works). In 100
  random works, **72 point to another country and 19 to Argentina**. **Spain alone: 56** (46.2%
  to 65.3%; roughly 170 to 245 works), mostly Spanish FPU doctoral fellowships (`FPU12/00265`,
  `AP2010-4951`) and Plan Nacional project codes (`ENE2016-80638-R`, `MTM2010-19821`). Then
  Korea 3, China 2, Romania 2, and one each from Peru, Indonesia, Costa Rica, Türkiye, Colombia,
  the Czech Republic, Thailand, Chile and Taiwan. **By grant number alone: 30 of 100** (21.9% to
  39.6%).
- **For Argentina the main route is Crossref's own matcher**: on 30 of the 56 Spanish rows,
  Argentina's ID was added by Crossref (`doi-asserted-by: crossref`), mostly to entries named just
  "Ministerio de Educación". No Spanish record carries that bare name (Spain's are "Ministerio de
  Educación, Cultura y Deporte" and "Ministerio de Educación y Formación Profesional"), so the
  matcher's exact matches are Argentina's (and Chile's) alternate name. Argentina's leak is
  mostly older: only 24 of its works were created since 2025, and most of their entry names
  are Argentine.

## Records whose name or alias is just "Ministry of Education"

From `api.crossref.org/funders?query=Ministry+of+Education&rows=100` (223 hits; checked
2026-11-16). "main" = main name, "alt" = alternate name.

| Funder ID | Country | Bare string | Status in this series |
|---|---|---|---|
| 100009950 | Thailand | main + MOE | 105 of 200 foreign (FINDINGS-MOE-1) |
| 100009122 | United Arab Emirates (MoHESR) | alt + MOE | 150 of 198 foreign (FINDINGS-MOHESR-1) |
| **501100004565** | **Brunei** | alt | **75 of 100 foreign (this note)** |
| **501100006667** | **Argentina** | alt (+ "Ministerio de Educación") | **72 of 100 foreign (this note)** |
| 501100002701 | South Korea | main + MOE | the home record Korean grants should reach |
| 100010002 | Taiwan | main + MOE | not checked |
| 501100001459 | Singapore | alt + MOE | not checked |
| 100031330 | United Arab Emirates (MoE) | alt + MoE | not checked |
| 501100015515 | Malaysia | alt + MOE | not checked |
| 501100011821 | Saudi Arabia | alt + MoE | not checked |
| 501100004567 | Bangladesh | alt + MoE | not checked |
| 501100020930 | Kenya | alt + MOE | not checked |
| 100031505 | Israel | alt | not checked |
| 501100013898 | Türkiye | alt | facet: 12 entries named for Indonesia's ministry |
| 100016329 | Canada (Ontario) | alt | not checked |
| 501100003081 | Ethiopia | MOE | not checked |
| 501100004541 | India | MoE | not checked |
| 501100002338 | China | MOE | not checked |
| 501100002847 | Chile | "Ministerio de Educación" | facet: Spanish MINECO 12, MICINN 10 |

## Entries re-read in full

Each was re-read from the single-record API (`api.crossref.org/works/<doi>`):

- 10.1002/adfm.202523787 (Wiley, created 2026-01-21): entry "Kementerian Pendidikan", Brunei's ID,
  award `2018R1A6A1A03025708` (Korean NRF), next to Korea's Ministry of Science and ICT; authors
  at Kyung Hee University, Korea.
- 10.1007/s13369-023-08064-5 (Springer, 2023): "Kementerian Pendidikan", Brunei's ID, award
  `FRGS/1/2018/STG02/UPM/02/5` (Malaysia's Fundamental Research Grant Scheme), next to Universiti
  Putra Malaysia.
- 10.1016/j.enbuild.2019.07.019 (Elsevier, 2019): "Ministry of Education", Brunei's ID, award
  `R296000181133` (a National University of Singapore grant code).
- 10.1016/j.ijepes.2018.12.009 (Elsevier, 2018): "Ministerio de Educación", Argentina's ID **added
  by Crossref**, award `ENE2016-80638-R` (Spanish Plan Nacional).
- 10.1016/j.fsi.2018.09.022 (Elsevier, 2018): "Ministerio de Educación", Argentina's ID
  (publisher), award `FPU12/00265` (Spanish FPU), next to Spain's MINEICO and AEI.
- 10.1016/j.jcis.2018.02.058 (Elsevier, 2018): an entry named **"Ministerio de Educación from the
  Spanish Government"** with Argentina's ID (publisher).
- 10.1080/14697688.2020.1733058 (Informa, 2020): "Ministerio de Educación", Argentina's ID,
  award `ECO2017-89715-P`; first author at the European Central Bank.
- 10.1002/bkcs.11697 (Wiley, 2019): "Ministry of Education", Argentina's ID, award
  `NRF-2018R1D1A1B07047022` (Korean NRF).

All matched the sample listings.

## How it was measured

- Records: `api.crossref.org/funders/501100004565` and `/funders/501100006667`.
- Facets: `works?filter=funder:10.13039/<id>&rows=0&facet=funder-name:12,publisher-name:10,published:20`.
- Random samples: one draw each of `works?filter=funder:10.13039/<id>&sample=100&select=DOI,funder,created,publisher`.
- Each row was labelled by hand from (a) the award number on the entry, (b) the entry's own name
  and (c) the other funders on the same work. Labels: `foreign:<country>`, the home country
  (`BN`, `AR`), or `unclear`. Rows whose only other funders were host agencies abroad (for
  example Australia's NHMRC on a "training scholarship") were left unclear.
- **Award-number tier**: the label rests on the grant number's own format (Korean NRF
  `20xxR1...`/`RS-20xx-...`, Malaysian `FRGS/...` and USM `203/P...`, Singapore `MOE-T2EP...`, AcRF
  Tier 1 and NUS `R296...`, Taiwan MOE `1xxL9...`/`MOE-114-YSFMS-...`, Indonesian
  `.../C3/DT.05.00/PL/...`, Indian STARS, Austrian FFG; Spanish `FPU`, `AP20xx-` (FPU), `BES-`
  (FPI), Plan Nacional `MTM`/`ECO`/`ENE`/`CGL`/`SAF`/`PID`, Catalan `SGR`; Romanian `PN-II`/`PN-III`;
  Chinese `14YJC...`; Taiwan `MOST ...`). **Hand tier**: award number, entry name or co-funders.
- Labels were assigned by AI agents reading API output. Rows are in
  [data/moe-bn-sample-2026-11-16.csv](data/moe-bn-sample-2026-11-16.csv) and
  [data/moe-ar-sample-2026-11-16.csv](data/moe-ar-sample-2026-11-16.csv), with
  `award_format_tier` and `raw_checked` columns.

| Record | Tier | Foreign | Largest | Home | Unclear | Foreign share (95% Wilson) |
|---|---|---|---|---|---|---|
| Brunei 501100004565 | Award number | 46 | KR 26 | - | - | 46% (36.6% to 55.7%), a floor |
| Brunei 501100004565 | Hand | 75 | KR 31 | 12 | 13 | 75% (65.7% to 82.5%) |
| Argentina 501100006667 | Award number | 30 | ES 25 | - | - | 30% (21.9% to 39.6%), a floor |
| Argentina 501100006667 | Hand | 72 | ES 56 | 19 | 9 | 72% (62.5% to 79.9%) |

Publishers: Brunei's 326 works are Wiley 161, Elsevier 58, IEEE 39, Springer 26, ACS 9.
Argentina's 24 works created since 2025: Elsevier 10, Wiley 6, OUP 3, Informa 3.

## Why it is new

We searched the web and Crossref's and ROR's public trackers for both Funder IDs. Nothing reports
either record collecting other countries' grants. A university repository (Warwick's WRAP) shows
Malaysian FRGS grants under Brunei's ID, copied from Crossref without comment, and registry
browsers list both records correctly. Earlier studies of funder metadata measured missing or
unmatched funders, or NSF/NIH look-alikes in DataCite (Metadata Game Changers), not grants filed
under another country's record because of a bare alias.

## Limits

- One random draw of 100 per record, not a census. Labels were assigned by AI agents from API
  output; 8 rows were re-read raw.
- A row labelled foreign means its award number, entry name or co-funders point elsewhere, not
  that the authors were checked.
- Spanish FPU fellowships were run by Spain's education ministry in some years, so the funder
  name "Ministerio de Educación" is correct for many of these works; only the country of the ID
  is wrong.
- The 18-record table covers the first 100 of 223 query hits; a few more records may carry the
  bare string.

## Suggested fixes (for whoever curates the registry)

- Drop the bare alternate names "Ministry of Education" from Brunei's 501100004565 and
  "Ministerio de Educación" / "Ministry of Education" from Argentina's 501100006667 (keep the
  country-qualified forms), and add the country to both main names. The same applies to every
  record in the table above.
- Crossref's matcher could decline to assign an ID when a bare name matches a single record by
  alias only. Spanish entries whose award is an `FPU`, `AP20xx-` or Plan Nacional code could be
  re-pointed to Spain's ministry records; Korean NRF numbers to 10.13039/501100002701.

Disclosure: found, checked and written by AI agents working in MV2's name. MV2, Munim, Inc.,
mv2@munimtech.com.
