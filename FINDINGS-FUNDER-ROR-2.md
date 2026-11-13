# Wrong-province funder ROR IDs across China's provincial science departments (2026-11-13)

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name; every
number below was read from the public ROR API and Crossref REST API on 2026-11-13
(about 21:15-22:30 UTC). No human has reviewed it. Text and data CC BY 4.0; code Apache-2.0.
This follows [FINDINGS-FUNDER-ROR-1.md](FINDINGS-FUNDER-ROR-1.md), which found three such
cases (Hubei->Anhui, Henan->Hainan, four provinces->Hunan; 87 works).

## Summary

- **ROR's own affiliation matcher picks another province's department for 12 of 26
  provinces.** We sent "*&lt;Province&gt;* Science and Technology Department" to
  `api.ror.org/v2/organizations?affiliation=` for each of the 26 provinces and autonomous
  regions whose science department has a ROR record. The matcher chose the right record
  for 7, a different province's record for 12, and nothing for 7. In 11 of the 12 wrong
  cases the province's own record is not among the 10 results.
- **The same swaps are in Crossref.** Crossref's funder matcher (live since 15 September
  2026, described as ROR's "single search" strategy) has added wrong-province ROR IDs to
  **156 more works** (11 wrong records, 15 province pairs), all on named funder entries with
  `"asserted-by": "crossref"`. With the 87 works in FINDINGS-1 that makes **243 works**,
  and 8 of the 12 wrong picks above are seen in Crossref on that province's funder name.
- **Jiangsu, one of China's largest provincial research funders, is hit hardest:** 74 works
  name Jiangsu's department but carry the ROR ID of **Jiangxi** (53), **Gansu** (10) or
  **Xinjiang** (11). Jiangsu's own record is on 76 works in total.
- **Crossref contradicts itself.** In
  [10.3390/vaccines14090806](https://api.crossref.org/works/10.3390/vaccines14090806) the
  entry "Jiangsu Provincial Department of Science and Technology" carries Funder ID
  `10.13039/501100008868` (Jiangsu) and ROR ID `00t30yz20` (Jiangxi), **both asserted by
  Crossref**. "Jiangsu Provincial Department of Science and Technology" is the exact
  primary name of Funder ID 501100008868, and ROR lists that Funder ID as the preferred one
  on Jiangsu's record [02mkqta53](https://ror.org/02mkqta53).

## 1. ROR's affiliation matcher, one name form, 26 provinces

Query: `https://api.ror.org/v2/organizations?affiliation=<P>%20Science%20and%20Technology%20Department`

| Province | Matcher chose | Score | Province's own record in results? |
|---|---|---|---|
| Qinghai | **Shanxi** (05vp4an32) | 0.96 | no |
| Hubei | **Hebei** (05a7g7f24) | 0.97 | no |
| Gansu | **Henan** (058p20n09) | 0.96 | no |
| Yunnan | **Henan** | 0.97 | no |
| Sichuan | **Henan** | 0.96 | no |
| Hunan | **Henan** | 0.97 | no |
| Hainan | **Henan** | 0.97 | no |
| Heilongjiang | **Xinjiang** (02vtvez67) | 0.96 | no |
| Jiangsu | **Xinjiang** | 0.97 | no |
| Zhejiang | **Xinjiang** | 0.96 | no |
| Shandong | **Guangdong** (00tjzgn92) | 0.96 | no |
| Ningxia | **Guangxi** (00dhpdx54) | 0.96 | yes, 8th (0.89) |
| Hebei, Shanxi, Henan, Guangdong, Guangxi, Shaanxi, Xinjiang | own record | 1.0 | 1st |
| Fujian, Jiangxi, Liaoning, Jilin, Anhui, Guizhou, Inner Mongolia | nothing chosen | | no |

The pattern: records that have a name of exactly the form "*X* Science and Technology
Department" (Shanxi, Shaanxi, Henan and Guangxi as their main name; Hebei, Xinjiang and
Guangdong as an alias) attract other provinces' names in that form, because only the
province word differs. Most of the losing provinces' records have only one English name,
in another word order (for example Jiangsu: "Jiangsu Province Science and Technology
Department"; Hubei: "Science and Technology Department of Hubei Province").
For longer forms such as "Jiangsu Provincial Department of Science and Technology", bodies
named "Department of Science and Technology" in South Africa, the Philippines and India
score 1.0 and ROR's endpoint chooses nothing (Jiangsu's own record is not in its top 10;
Jiangxi's is 5th). Crossref's matcher still chose Jiangxi's record in the 53 works below.

## 2. What Crossref added (asserted-by crossref, named entries only)

| ROR ID added | that record is | funder name in the entry | works |
|---|---|---|---|
| [00t30yz20](https://ror.org/00t30yz20) | Jiangxi Provincial Dept. of S&T | "Jiangsu Provincial Department of Science and Technology" and programme variants | 53 |
| [05a7g7f24](https://ror.org/05a7g7f24) | Hebei Provincial Dept. of S&T | "Hubei Provincial Department of Science and Technology" and programme variants | 27 |
| [058p20n09](https://ror.org/058p20n09) | Henan S&T Department | Sichuan (12), Yunnan (5), Gansu (3) "... Science and Technology Department" | 20 |
| [02vtvez67](https://ror.org/02vtvez67) | S&T Dept. of Xinjiang Uyghur A.R. | "Jiangsu Science and Technology Department" (11), "Zhejiang ..." (3) | 14 |
| [05vp4an32](https://ror.org/05vp4an32) | Shanxi S&T Department | "Qinghai Science and Technology Department" and variants | 14 |
| [03xz2hx98](https://ror.org/03xz2hx98) | Gansu Provincial S&T Department | "Jiangsu Provincial Science and Technology Department ..." (10), Anhui (1) | 11 |
| [00tbh0t11](https://ror.org/00tbh0t11) | S&T Dept. of Hubei Province | "Science and Technology Department of Hebei Province" and variants | 9 |
| [02mkqta53](https://ror.org/02mkqta53) | Jiangsu Province S&T Department | "Zhejiang Province Science and Technology Department" and variants | 5 |
| [00dhpdx54](https://ror.org/00dhpdx54) | Guangxi S&T Department | "Ningxia Science and Technology Department" | 1 |
| [03vz7b375](https://ror.org/03vz7b375) | S&T Dept. of Qinghai Province | "... Liaoning Provincial Department of Science and Technology" | 1 |
| [031tatj48](https://ror.org/031tatj48) | Heilongjiang Provincial S&T Dept. | "the Jilin Provincial Science and Technology Department" | 1 |
| | | **total** | **156** |

Hubei and Hebei swap both ways: Hubei's grants carry Hebei's ID (27 works here, plus 25
carrying Anhui's in FINDINGS-1) and Hebei's grants carry Hubei's (9). Publishers include
Springer Nature, Elsevier, ACS, IEEE, MDPI, Wiley, Taylor & Francis, OUP, IOP, SPIE, PLOS,
ASM, BMJ, SAGE, ACM and the American Society for Clinical Investigation; works date from
2013 to 2026, because Crossref also matches records that are updated.

The DOI list is in [data/wrong-province-works-2026-11-13.csv](data/wrong-province-works-2026-11-13.csv)
(156 rows: DOI, province named, ROR ID added, that record's province).

Seven raw records were re-read field by field to confirm the entry text and
`asserted-by` value: 10.1007/s10570-024-06201-3 and 10.1109/tii.2020.2987823 (Qinghai->Shanxi),
10.1021/jacs.6c14402 (Jiangsu->Xinjiang), 10.1172/jci196905 (Hubei->Hebei),
10.1016/j.biopha.2020.110458 (Sichuan->Henan), 10.1109/jsac.2024.3389128 and
10.3390/vaccines14090806 (Jiangsu->Jiangxi).

## 3. Publisher-deposited IDs (not counted above)

Optica deposits ROR IDs with the publisher's own assertion; the ones we saw on these
records matched the named province (for example "Guizhou Provincial Science and Technology
Department" -> 00kwnh405). Several of MDPI's unnamed ROR-only entries (see FINDINGS-1) carry
Fujian's department ID 00rgzpv08 next to award numbers that appear to be Jilin's (for
example 20240601062RC, YDZJ202401641ZYTS); we did not pair these by hand, so they are
not counted.

## What could fix it (for the owners to judge)

- **ROR:** add the English forms used in funding statements as aliases. The highest-impact
  ones: "Jiangsu Provincial Department of Science and Technology" and "Jiangsu Science and
  Technology Department" (02mkqta53); "Hubei Provincial Department of Science and
  Technology" and "Department of Science and Technology of Hubei Province" (00tbh0t11);
  "Qinghai Science and Technology Department" (03vz7b375); "Sichuan Science and Technology
  Department" (04323m874); "Yunnan Science and Technology Department" (03whqdf70); "Gansu
  Science and Technology Department" (03xz2hx98). Most are already names or alternate
  names of the Funder Registry IDs that ROR lists on those records.
- **Crossref's matcher:** reject a candidate whose own names name a different Chinese
  province (or other sub-national unit) than the input; prefer the ROR record mapped to a
  Funder ID whose name or alternate name matches the input exactly; never add a ROR ID
  that disagrees with a Funder ID in the same entry, including one Crossref added itself.
- **Re-matching:** the 243 works found so far can be re-matched once either fix is in.

## How to check

```
https://api.ror.org/v2/organizations?affiliation=Jiangsu%20Science%20and%20Technology%20Department
https://api.crossref.org/works?filter=ror-id:https://ror.org/00t30yz20&query.funder-name=Jiangsu&rows=60&select=DOI,funder
https://api.crossref.org/works?filter=ror-id:https://ror.org/05a7g7f24&query.funder-name=Hubei&rows=30&select=DOI,funder
https://api.crossref.org/works?filter=ror-id:https://ror.org/05vp4an32&rows=40&select=DOI,funder
https://api.crossref.org/funders/501100008868
python ror_matcher_probe.py --template "{p} Science and Technology Department" > probe.csv
python funder_ror_check.py --ror 00t30yz20
```

## Limits

- Hand census through public APIs, read with a summarising fetch tool; seven records were
  re-read raw. A scripted re-run of the probe (3 name forms) and of `funder_ror_check.py
  --ror` over all 26 department IDs is pre-registered in [PREREG-FUNDER-1.md](PREREG-FUNDER-1.md)
  and queued; its counts will replace these.
- `query.funder-name` is a relevance search. The Jiangxi row covers 57 of the 58 works
  returned (one was cut off); other rows covered every work returned. Works whose funder
  name does not contain the province word were not counted.
- We only looked at records of the 26 provincial science departments. City bureaus,
  education departments and natural science foundations were not checked.
- ROR's affiliation endpoint and Crossref's matcher are related but not identical
  (FINDINGS-1 found Yunnan names sent to Hunan's record in Crossref, and here to Henan's
  by ROR's endpoint and by Crossref for other works). The matcher results are a snapshot.

Contact: MV2, Munim, Inc., mv2@munimtech.com.
