# funder-ror-check

Find funder ROR IDs in Crossref metadata that name the wrong funder.

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name.
Code Apache-2.0; findings text and data CC BY 4.0. Release 0.2.0 (funder_ror_check 0.1.0,
ror_matcher_probe 0.2.0).

## Why

Crossref funding metadata can now identify a funder by its ROR ID, either deposited by the
publisher or, since 15 September 2026, added by Crossref's own name matcher
(`"asserted-by": "crossref"`). On 2026-11-13 we found both kinds pointing at the wrong
organisation:

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
- [PREREG-FUNDER-1.md](PREREG-FUNDER-1.md): a scripted census of all 26 provincial
  department IDs, with predictions registered before it runs.

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

## Use

Python 3.8+, standard library only.

```
python funder_ror_check.py 10.3390/vaccines14090806
python funder_ror_check.py --ror 00t30yz20                 # every work carrying Jiangxi's ID
python funder_ror_check.py --ror 03z942k20 --member 1968 --from-pub-date 2026 --csv > out.csv
python funder_ror_check.py --all 10.3390/buildings16193954  # show ok rows too

python ror_matcher_probe.py > probe.csv                      # 26 provinces x 3 name forms
python ror_matcher_probe.py --province Jiangsu --template "{p} Science and Technology Department"
```

funder_ror_check exit code: 1 if anything suspect, 2 if a lookup failed (and nothing
suspect), else 0. ror_matcher_probe exit code: 1 if any pick is wrong, else 0.
Tests: `python -m unittest -v` (offline; HTTP is faked).

## Limits

- The place checks know Chinese provinces (and their capitals) and a short list of
  countries. They cannot judge generic names that name no place, and they will miss a
  wrong record in the right province.
- A name naming one country for a binational body (for example "Sino-German ...") is
  handled only where the list has both words.
- `doi-ror-conflict` relies on ROR's Funder ID mapping, which can itself be incomplete.
- ROR's affiliation endpoint is related to, not identical with, Crossref's matcher.
- Every flag is a lead for a human check, not a verdict.

## Disclosure

The code and findings were made with AI agents working in the name of MV2, Munim, Inc.
and were not reviewed by a human. Reports of wrong flags are welcome as GitHub issues.
