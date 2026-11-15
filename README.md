# funder-ror-check

Find funder IDs (ROR IDs and Funder Registry DOIs) in Crossref metadata that name the wrong funder.

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name.
Code Apache-2.0; findings text and data CC BY 4.0. Release 0.6.0 (funder_ror_check 0.1.0,
ror_matcher_probe 0.2.0, country_swap_scan 0.1.0, award_country_check 0.3.0).

## Why

Crossref funding metadata identifies a funder by a Funder Registry DOI (10.13039/...) or a
ROR ID. Either can be deposited by the publisher or added by Crossref's own name matcher
(`"asserted-by": "crossref"`). Between 2026-11-13 and 15 we found both kinds pointing at the
wrong organisation:

- [FINDINGS-MOST-1.md](FINDINGS-MOST-1.md): **most works carrying Vietnam's and Korea's
  "Ministry of Science and Technology" Funder IDs were funded in Taiwan or China.** Both records
  (10.13039/100007225, Vietnam, 10,597 works; 10.13039/501100003711, South Korea, a ministry
  merged away in 2008, 7,033 works) have the bare name "Ministry of Science and Technology". In
  184 random draws from Vietnam's, 109 carry another country's grant number on that entry
  (Taiwan 73, China 30) and 7 a Vietnamese one. In 100 draws from Korea's, 50 carry another
  country's (Taiwan 34, China 14) and 2 a Korean one. That is roughly 5,300 to 8,000
  Taiwan-funded works missing from Taiwan's own record. The samples are in
  [data/most-vn-kr-sample-2026-11-15.csv](data/most-vn-kr-sample-2026-11-15.csv).
- [FINDINGS-MOE-1.md](FINDINGS-MOE-1.md): **most works carrying Thailand's "Ministry of
  Education" Funder ID are not Thai.** The record (10.13039/100009950, 6,896 works) has the
  bare name "Ministry of Education". In 200 random draws, 46 carry a Korean, Chinese,
  Taiwanese, Singaporean or Slovak grant number on that entry and 4 a Thai one. With co-funders
  and journals counted, 105 point to another country and 10 to Thailand, about 3,100 to 4,100
  works in all. The sample is in [data/moe-th-sample-2026-11-14.csv](data/moe-th-sample-2026-11-14.csv).
- [FINDINGS-NRF-1.md](FINDINGS-NRF-1.md): **Korean, Singaporean and Chinese grants filed
  under South Africa's National Research Foundation.** South Africa's Funder Registry entry
  (10.13039/501100001321) is named just "National Research Foundation". In 200 randomly
  sampled works of the 39,201 that carry it, 45 (22.5%) have a Korean NRF, Singapore NRF or
  Guangdong grant number on that entry, about 6,800 to 11,300 works in all. The sample is in
  [data/nrf-za-sample-2026-11-14.csv](data/nrf-za-sample-2026-11-14.csv).
- [FINDINGS-COUNTRY-1.md](FINDINGS-COUNTRY-1.md): **Crossref links China's Ministry of
  Science and Technology to Taiwan's National Science and Technology Council.** 311 works
  with a funder named exactly "Ministry of Science and Technology of China" carry Taiwan's
  ROR ID (02kv4zf79); 16 carry China's own (027s68j25). In 33 of 40 works read by hand the
  wrong ID is on the China-named entry, asserted by Crossref. MDPI's own deposits also give
  Chinese provincial grants the ROR IDs of South Africa's and India's science departments.
- [FINDINGS-FUNDER-ROR-2.md](FINDINGS-FUNDER-ROR-2.md): for "*Province* Science and
  Technology Department", **ROR's own affiliation matcher picks another province's
  department for 12 of 26 Chinese provinces**. Crossref has added wrong-province ROR IDs
  to at least **243 works** so far. Jiangsu's provincial department alone is credited as
  Jiangxi, Gansu or Xinjiang in 74 works, and in
  [10.3390/vaccines14090806](https://api.crossref.org/works/10.3390/vaccines14090806)
  Crossref added both Jiangsu's Funder ID and Jiangxi's ROR ID to the same entry.
  The DOI list is in [data/](data/).
- [FINDINGS-FUNDER-ROR-1.md](FINDINGS-FUNDER-ROR-1.md): the first three cases
  (Hubei->Anhui 25 works, Henan->Hainan 20, four provinces->Hunan 35 of 40 read), and MDPI
  depositing Australia's, the Philippines' and Singapore's departments for Chinese and
  Korean funders.
- [PREREG-FUNDER-1.md](PREREG-FUNDER-1.md), [PREREG-COUNTRY-1.md](PREREG-COUNTRY-1.md),
  [PREREG-NRF-1.md](PREREG-NRF-1.md), [PREREG-MOE-1.md](PREREG-MOE-1.md) and
  [PREREG-MOST-1.md](PREREG-MOST-1.md): scripted censuses (26 provincial department IDs; 15
  national records; every work under South Africa's and Singapore's NRF Funder IDs; every work
  under the Thai, Taiwanese and Korean "Ministry of Education" IDs; every work under the
  Vietnamese, Korean and Taiwanese "Ministry of Science and Technology" IDs), with predictions
  registered before they run.

## What funder_ror_check checks

For each funder ROR ID in a work:

| verdict | meaning |
|---|---|
| `doi-ror-conflict` | the entry's Funder Registry DOI (10.13039/...) is listed by ROR on a different record |
| `country-mismatch` | the funder name names a country (or a Chinese province) and the ROR record is elsewhere |
| `province-mismatch` | the funder name and the ROR record's names name different Chinese provinces |
| `ok` | the funder DOI is on the ROR record, or the place checks passed |
| `unchecked` | nothing to check, e.g. a bare "Department of Education" |
| `unpaired` | an unnamed entry holding only a ROR ID could not be tied to one funder name |
| `error` | a lookup failed |

Unnamed entries (MDPI deposits the ROR ID as a separate funder) are paired with the single
named entry that has exactly the same award numbers.

## What country_swap_scan does

For one ROR ID, it pages through every Crossref work that carries it. Each funder entry
holding that ID is classed by the countries its name mentions (or, for an unnamed MDPI
twin, the name of the entry it belongs to): `own`, `foreign`, `mixed` or `unclear`. "People's
Republic of China" counts as China, "Republic of China" / "R.O.C." as Taiwan.

## What award_country_check does

For one Funder Registry ID, it pages through every Crossref work that carries it and reads
the award numbers on the entries with that ID. Each award is labelled by its format:

| label | formats |
|---|---|
| `KR` | Korean NRF: `2019R1A2C1003456`, `RS-2023-00281839`, `NRF-2012-M3C1A1-048860`, `2012-0001509` |
| `SG` | Singapore: NRF `NRF-CRP22-2019-0001`, `NRF2016NRF-NSFC002-013`; Ministry of Education `MOE2013-T2-2-054`, `MOE-T2EP10223-0002`; NUS `R-154-000-B18-114` |
| `CN` | Guangdong `2022A1515010159`; Chinese Ministry of Education humanities projects `21YJCZH147`, `21JZD056`, `2025JZDZ093`, `24JDSZ3126`; Ministry of Science and Technology programmes: National Key R&D `2016YFA0204100`, 973 `2011CB707906`, 863 `2012AA101801`, Key Technologies `2015BAD09B010102`, megaprojects `2014ZX09507003006`, `2012FY120100`, `2020SKA0110100`, `2011YQ120023`, `2008DFA30770`, `S2012GR0290` |
| `TW` | Taiwan Ministry of Education `107L9006`, `114L9A00303`; MOST / NSC / NSTC projects `MOST 103-2221-E-006-093-MY3`, `NSC 99-2321-B-005-009`, `109-2622-8-002-003`, `110-2218-E-A49-014-MBK` |
| `TH` | Thailand Research Fund `MRG6180091`, `IRG5980007` |
| `SK` | Slovak VEGA `VEGA 1/0802/20` |
| `ZA` | South African NRF: `UID 96354`, plain 4-6 digit numbers, `TTK…`, `CSUR…`, `SRUG…` |
| `VN` | Vietnamese, read from the whole award field: `2372/QD-BKHCN`, `ĐTĐL.CN-116/21`, `KC01.05/11-15` (any field with the letter Đ) |
| `IN` | Indian DST / DBT / SERB, read from the whole award field: `DST/TMD/HFC/2k18/123`, `BT/PR10903/MED/29/829/2014`, `CRG/2023/005571` |

A country named in the entry name also counts ("Republic of China" without "People's", and
"R.O.C.", count as Taiwan). Each work is `FOREIGN`, `HOME` or `UNCLEAR` against the country you
give with `--home`. `--formats` limits the labels used; leave `ZA` out for any funder that is
not South Africa's, because its plain-digits rule is loose.

## Use

Python 3.8+, standard library only.

```
python funder_ror_check.py 10.3390/vaccines14090806
python funder_ror_check.py --ror 00t30yz20                 # every work carrying Jiangxi's ID
python funder_ror_check.py --ror 03z942k20 --member 1968 --from-pub-date 2026 --csv > out.csv
python funder_ror_check.py --all 10.3390/buildings16193954  # show ok rows too

python ror_matcher_probe.py > probe.csv                      # 26 provinces x 3 name forms
python ror_matcher_probe.py --province Jiangsu --template "{p} Science and Technology Department"

python country_swap_scan.py --ror 02kv4zf79 > rows.csv       # Taiwan's NSTC

python award_country_check.py --funder 501100001321 --home ZA --out-dir out --mailto you@example.org
python award_country_check.py --funder 100009950 --home TH --formats KR,SG,CN,TW,TH,SK --out-dir out
python award_country_check.py --funder 100007225 --home VN --formats KR,SG,CN,TW,TH,SK,VN,IN --out-dir out
```

funder_ror_check exit code: 1 if anything suspect, 2 if a lookup failed (and nothing
suspect), else 0. ror_matcher_probe exit code: 1 if any pick is wrong, else 0.
award_country_check writes `works-<id>.csv` and `summary-<id>.json` to `--out-dir`.
Tests: `python -m unittest -v` (offline; HTTP is faked).

## Limits

- The place checks know Chinese provinces (and their capitals) and a short list of
  countries. They cannot judge generic names that name no place, and they will miss a
  wrong record in the right province.
- A name naming one country for a binational body (for example "Sino-German ...") is
  handled only where the list has both words; country_swap_scan calls it `mixed`.
- `doi-ror-conflict` relies on ROR's Funder ID mapping, which can itself be incomplete.
- ROR's affiliation endpoint is related to, not identical with, Crossref's matcher.
- award_country_check knows nine countries' formats. Entries with no award, or an award in
  another format, stay `UNCLEAR`, so it undercounts both home and foreign works. A field read
  as Vietnamese or Indian is not split further, so another country's number in the same field
  is missed.
- Every flag is a lead for a human check, not a verdict.

## Disclosure

The code and findings were made with AI agents working in the name of MV2, Munim, Inc.
and were not reviewed by a human. Reports of wrong flags are welcome as GitHub issues.
