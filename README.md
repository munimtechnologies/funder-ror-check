# funder-ror-check

Find funder ROR IDs in Crossref metadata that name the wrong funder.

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name.
Code Apache-2.0; findings text CC BY 4.0. Version 0.1.0.

## Why

Crossref funding metadata can now identify a funder by its ROR ID, either deposited by the
publisher or, since 15 September 2026, added by Crossref's own name matcher
(`"asserted-by": "crossref"`). On 2026-11-13 we found both kinds pointing at the wrong
organisation ([FINDINGS-FUNDER-ROR-1.md](FINDINGS-FUNDER-ROR-1.md)):

- Crossref's matcher gave "Department of Science and Technology of **Hubei** Province" the
  ROR ID of **Anhui**'s department (25 works), Henan's the ID of **Hainan**'s (20 works), and
  Yunnan, Sichuan, Fujian and Shanxi departments the ID of **Hunan**'s (35 of 40 works read),
  even though Crossref's own Funder Registry has the exact names and ROR maps those Funder
  IDs to the right records.
- MDPI deposited Australia's Department of Education, the Philippines' Department of
  Science and Technology and Singapore's Ministry of Education for Chinese provincial
  and Korean funders.

## What it checks

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

## Use

Python 3.8+, standard library only.

```
python funder_ror_check.py 10.1016/j.mseb.2026.119859
python funder_ror_check.py --ror 01e70gy59                 # every work carrying Anhui's ID
python funder_ror_check.py --ror 03z942k20 --member 1968 --from-pub-date 2026 --csv > out.csv
python funder_ror_check.py --all 10.3390/buildings16193954  # show ok rows too
```

Exit code: 1 if anything suspect, 2 if a lookup failed (and nothing suspect), else 0.
Tests: `python -m unittest -v` (offline; HTTP is faked).

## Limits

- The place checks know Chinese provinces (and their capitals) and a short list of
  countries. They cannot judge generic names that name no place, and they will miss a
  wrong record in the right province.
- A name naming one country for a binational body (for example "Sino-German ...") is
  handled only where the list has both words.
- `doi-ror-conflict` relies on ROR's Funder ID mapping, which can itself be incomplete.
- Every flag is a lead for a human check, not a verdict.

## Disclosure

The code and findings were made with AI agents working in the name of MV2, Munim, Inc.
and were not reviewed by a human. Reports of wrong flags are welcome as GitHub issues.
