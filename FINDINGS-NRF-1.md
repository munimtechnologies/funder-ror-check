# FINDINGS-NRF-1: Korean, Singaporean and Chinese grants filed under South Africa's National Research Foundation in Crossref

By MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-14. Made with AI agents working in MV2's name;
not reviewed by a human. Text and data CC BY 4.0.

## Summary

The Crossref Funder Registry entry for South Africa's National Research Foundation,
[10.13039/501100001321](https://api.crossref.org/funders/501100001321), is named just
"National Research Foundation". On 2026-11-14, 39,201 Crossref works carried it. We drew two
random samples of 100 of these works through Crossref's own `sample` parameter and read the
award numbers on the funder entry with that ID:

| what the award number or entry name shows | works (of 200) |
|---|---|
| a Korean NRF grant (e.g. `2019R1A2C2011478`, `RS-2023-00281839`, `NRF-2012-M3C1A1-048860`) | **37** |
| a Singapore NRF grant (e.g. `NRF-CRP22-2019-0001`, `NRF2016NRF-NSFC002-013`) | 4 |
| a Chinese Guangdong grant, with the entry named "Guangdong Basic and Applied Basic Research Foundation" | 4 |
| a South African NRF grant (UID numbers, `TTK…`, `CSUR…`, `SRUG…`, plain 5-6 digit numbers) or "South Africa" in the name | 70 |
| no award or a format we could not place | 85 |

So **45 of 200 sampled works (22.5%; 95% Wilson interval 17.3% to 28.8%) credit another
country's grant to South Africa's NRF**, which is about **6,800 to 11,300 works** of the 39,201.
Among the 115 sampled works whose entry can be placed at all, 45 (39%) are not South African.
The Korean share alone (37 of 200, interval 13.7% to 24.5%) is about 5,400 to 9,600 works.
Each of these works is missing from counts by Korea's own Funder ID
([501100003725](https://api.crossref.org/funders/501100003725), 281,527 works) and is counted
for South Africa instead.

It is still happening: 3,927 works created since 2026-01-01 carry South Africa's NRF ID
(Elsevier 1,660; IEEE 665 under its two member names; Wiley 388; MDPI 273; Springer 258).
Two of the seven records we re-read raw were created in 2025 and one in 2026.

The 200 rows are in [data/nrf-za-sample-2026-11-14.csv](data/nrf-za-sample-2026-11-14.csv).

## Seven records re-read raw

Each was read in full from `https://api.crossref.org/works/<DOI>`:

1. [10.1016/j.cmet.2026.04.001](https://api.crossref.org/works/10.1016/j.cmet.2026.04.001)
   (Elsevier, created 2026-04-27). Four entries named "National Research Foundation" carry
   10.13039/501100001321 with awards `RS-2022-NR072349`, `RS-2025-02263462`,
   `RS-2023-00225555` and `RS-2024-00440228`, all asserted by the publisher. A separate entry,
   "National Research Foundation of Korea", carries Korea's ID with no award.
2. [10.1371/journal.pone.0305350](https://api.crossref.org/works/10.1371/journal.pone.0305350)
   (PLOS, created 2024-06-11). "National Research Foundation", award
   `NRF-2019R1A2C2011478`, with South Africa's ID **asserted by Crossref**: here Crossref's
   own matcher added the ID.
3. [10.1117/1.jbo.20.11.111207](https://api.crossref.org/works/10.1117/1.jbo.20.11.111207)
   (SPIE, re-deposited 2026-10-01). Each of five Korean awards appears both under
   "National Research Foundation of Korea" (Korea's ID or ROR 013aysd81) and under
   "National Research Foundation" with South Africa's Funder ID **and South Africa's ROR ID
   05s0g1g46**, all asserted by the publisher.
4. [10.1117/1.ap.7.5.050503](https://api.crossref.org/works/10.1117/1.ap.7.5.050503)
   (SPIE, created 2025-10-28). `RS-2022-NR067559` under South Africa's Funder ID and ROR ID.
5. [10.21468/scipostphyscore.6.4.077](https://api.crossref.org/works/10.21468/scipostphyscore.6.4.077)
   (SciPost). `RS-2023-00281839` under South Africa's Funder ID and ROR ID; the work's second
   Korean grant is correctly under Korea's ID.
6. [10.1109/tits.2025.3562867](https://api.crossref.org/works/10.1109/tits.2025.3562867)
   (IEEE, created 2025-07-28). An entry **named "Guangdong Basic and Applied Basic Research
   Foundation"**, award `2022A1515010159`, carries South Africa's NRF ID (publisher-asserted).
   A name match cannot explain this one; we do not know how the pair arose.
7. [10.1093/gigascience/giae043](https://api.crossref.org/works/10.1093/gigascience/giae043)
   (OUP, created 2024-07-11). `NRF-CRP22-2019-0001`, a Singapore Competitive Research
   Programme grant, under South Africa's ID.

## Why it happens (likely)

- South Africa's Funder Registry record has the bare name "National Research Foundation"
  (alt-names "National Research Foundation (South Africa)", "NRF", "The NRF", "South
  Africa's National Research Foundation"). Korea's is "National Research Foundation of
  Korea" and Singapore's is "National Research Foundation Singapore". Korean acknowledgements
  usually say "the National Research Foundation (NRF) grant funded by the Korea government
  (MSIT)". An author or a matcher looking up "National Research Foundation" finds an exact
  name match on South Africa's record.
- Korea's record also lists a garbled alt-name, "한국연구재단이 창의적 연구와" (a sentence
  fragment), rather than a clean Korean name.
- ROR keeps the same bare display name for South Africa (05s0g1g46), Singapore (03cpyc314)
  and the UAE (01xpa3123). Where Crossref or a publisher adds ROR IDs from the Funder ID
  (records 3-5 above), the error carries into ROR-based funder counts too.
- Most of the wrong IDs are deposited by publishers (six of seven re-read records); one
  (PLOS) was added by Crossref.

## Prior art

Ted Habermann (Metadata Game Changers) showed the same kind of error for "NSF" and "NIH"
look-alikes and used award-number formats to find it, in DataCite records:
[Funder Acronyms Are Still Not Enough (2024)](https://metadatagamechangers.com/blog/2024/4/12/funder-acronyms-are-still-not-enough)
and [Using Award Numbers to Check Funder Identifiers (2026-01-06)](https://metadatagamechangers.com/blog/2026/1/6/using-award-numbers-to-check-funder-identifiers).
Neither post covers the National Research Foundations. Crossref's
[funder matching post](https://www.crossref.org/blog/matching-funders-in-scholarly-metadata-linking-names-to-ror-ids/)
says its matcher checks countries named in the funder string; a bare "National Research
Foundation" names none. We found no report, forum thread or paper on Korean, Singaporean or
Chinese grants filed under South Africa's NRF.

## What we did not show

- The samples were drawn by Crossref's `sample` parameter on 2026-11-14 and cannot be
  re-drawn identically; the CSV is the record.
- Rows were classed from the API listings by an AI reader using award-number formats, then
  seven were re-read raw. A plain 5-6 digit award is taken as South African, which can be
  wrong. A few borderline rows: `2016RIDIA3B03934419` (a likely typo of a Korean number) is
  counted as Korean in the CSV; the scripted checker below leaves it unplaced.
- 85 of 200 entries have no usable award. Some of them sit next to Korean or Singaporean
  co-funders, so the true foreign share is probably higher than 22.5%, but we did not count
  them.
- These are counts of works, not of grants or money.

## Check it yourself

```
https://api.crossref.org/funders/501100001321
https://api.crossref.org/works?filter=funder:10.13039/501100001321&rows=0
https://api.crossref.org/works?filter=funder:10.13039/501100001321&sample=100&select=DOI,funder
```

`award_country_check.py` (in this repository, standard library only) pages through every work
carrying a Funder ID and classes each entry's award numbers as Korean, Singaporean, Chinese
(Guangdong) or South African:

```
python award_country_check.py --funder 501100001321 --home ZA --out-dir out --mailto you@example.org
```

A full scripted census is registered in [PREREG-NRF-1.md](PREREG-NRF-1.md) before it runs.

## Disclosure

Found, checked and written by AI agents working in the name of MV2, Munim, Inc. Corrections
are welcome as GitHub issues on this repository.
