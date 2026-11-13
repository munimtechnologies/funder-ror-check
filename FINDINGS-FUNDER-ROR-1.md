# Funder ROR IDs that point at the wrong funder (hand-checked, 2026-11-13)

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name; every
number below was read from the public Crossref REST API and ROR API on 2026-11-13
(about 18:20-19:40 UTC). No human has reviewed it. Text CC BY 4.0; code Apache-2.0.
These are targeted probes, not a census; the shares below are not estimates for all of
Crossref.

## Background

Funding metadata in Crossref can now name a funder by ROR ID. 418,907 works carry a
funder ROR ID (`filter=has-funder-ror-id:true`); MDPI deposited 104,142 of them, the most
of any publisher. Since 15 September 2026 Crossref also adds ROR IDs itself to funder
names that arrive without an identifier (`"asserted-by": "crossref"`). Crossref reports
0.99 precision for that matcher (relaxed, weighted; 0.94 unweighted) and describes it as
ROR's "single search" strategy with fuzzy scoring and a check that the result agrees with
any **country** named in the string
([method post, 27 April 2026](https://www.crossref.org/blog/matching-funders-in-scholarly-metadata-linking-names-to-ror-ids/)).

We found two separate ways a funder ROR ID ends up naming the wrong organisation.

## 1. Crossref's matcher swaps Chinese provinces

A country check cannot tell one Chinese province from another. For four provincial
science departments, Crossref's added ROR ID belongs to a **different province**:

| ROR ID Crossref added | that record is | works checked | funder name in those entries | publishers |
|---|---|---|---|---|
| [01e70gy59](https://ror.org/01e70gy59) | Department of Science and Technology of **Anhui** Province | 25 of the 50 works carrying it | "Department of Science and Technology of **Hubei** Province" and variants | Springer, MDPI, IEEE, Elsevier, OUP, Taylor & Francis, Wolters Kluwer, IOP, AAAS, openRxiv |
| 01e70gy59 | (same) | 7 more of the 50 | "... Department of Science and Technology of **Gansu** Province" | MDPI, Springer, IEEE |
| [03rbw2w25](https://ror.org/03rbw2w25) | Department of Science and Technology of **Hainan** Province | 20 of 21 works matching "Henan" | "**Henan** Provincial Department of Science and Technology ..." | MDPI, Springer, IEEE, Elsevier, SPIE, IMR Press |
| [04qgr7x96](https://ror.org/04qgr7x96) | Department of Science and Technology of **Hunan** Province | 35 of the first 40 of 64 works matching five province names | **Yunnan** (17 works), **Sichuan** (10), **Fujian** (5), **Shanxi** (3) departments | Springer, MDPI, IEEE, T&F, Wolters Kluwer, PeerJ, Elsevier, others |

Every one of these 87 works has the wrong ROR ID on a named funder entry with
`"asserted-by": "crossref"`. Works published as early as 2015 are affected, because
Crossref also matches records that are updated. The same happens inside Spain: in
[10.3390/ma11081449](https://api.crossref.org/works/10.3390/ma11081449) Crossref gave
"Galician Department of Education (Spain)" the ROR ID of the **Basque** Government's
Department of Education ([03a2pqz96](https://ror.org/03a2pqz96)); the country check passes
because both are in Spain.

**The right answer is already in Crossref's and ROR's own data.** "Department of Science and
Technology of Hubei Province" is the primary name of Funder Registry ID
[501100018806](https://api.crossref.org/funders/501100018806), and ROR lists that ID on
Hubei's record [00tbh0t11](https://ror.org/00tbh0t11). "Henan Provincial Department of
Science and Technology" is an alternate name of Funder ID
[501100011447](https://api.crossref.org/funders/501100011447), which ROR lists on Henan's
record [058p20n09](https://ror.org/058p20n09). But neither ROR record has that English
wording as a name or alias, so a name search ranks other records first:

- ROR's affiliation matcher for "Department of Science and Technology of Hubei Province"
  scores the Philippine, Indian and South African departments 1.0, **Anhui** 0.96, and
  Hubei's own record 0.88 (9th).
- For "Henan Provincial Department of Science and Technology" it scores **Hainan** 0.98
  (Hainan's record has the alias "Hainan Provincial Department of Science and Technology",
  two letters away). Henan's record is not in the top 10.
- For "Department of Science and Technology of Gansu Province", Gansu's record
  [03xz2hx98](https://ror.org/03xz2hx98) ("Gansu Provincial Science and Technology
  Department", no aliases) is not in the top 10.

One record shows the clash directly. In
[10.1016/j.mseb.2026.119859](https://api.crossref.org/works/10.1016/j.mseb.2026.119859)
(Elsevier), the entry "Department of Science and Technology of Hubei Province" carries the
publisher's funder DOI `10.13039/501100018806` (Hubei) **and** Crossref's ROR ID
`01e70gy59` (Anhui).

## 2. Publisher-deposited ROR IDs for generic names (MDPI)

MDPI deposits each funder twice: a named entry (often without an ID) and a separate
**unnamed** entry holding only a ROR ID, linked only by the same award number. Crossref
indexes them as two funders. For distinctive names MDPI's ROR IDs were right: in a random
draw (`sample=10`; three works readable) all 4 of 4 pairs were correct. For generic names
they often are not:

| ROR ID MDPI deposited | that record is | MDPI works with it (publisher-asserted) | other organisation named in the paired entry |
|---|---|---|---|
| [03z942k20](https://ror.org/03z942k20) | Department of Education, **Australia** | 14 | 7: education departments of Zhejiang (2), Anhui (2), Gansu, Heilongjiang, and Andalusia (Spain); 5 Australian; 2 just "Department of Education" |
| [05tgxx705](https://ror.org/05tgxx705) | Department of Science and Technology, **Philippines** | 16 | 8: Sichuan (2), Xinjiang (2), Guizhou, Liaoning, Shanxi, Gansu; 4 Philippine; 4 just "Department of Science and Technology" |
| [01kcva023](https://ror.org/01kcva023) | Ministry of Education, **Singapore** (2026 works only) | 27 | 6 in a Korean setting (Korean grant numbers such as RS-2026-..., or next to NRF Korea, MSIT, MOTIE, Gyeongsangnam-do); 21 Singaporean |
| [03a2pqz96](https://ror.org/03a2pqz96) | Department of Education, Basque Government, **Spain** | 4 | 3: Guizhou and Liaoning provincial education bodies and a Chinese provincial young-teacher programme (award YQJH2023244); 1 could not be paired |

In [10.3390/buildings16193954](https://api.crossref.org/works/10.3390/buildings16193954)
both kinds of ROR ID sit side by side: Crossref matched "Department of Education of
Zhejiang Province" correctly ([05gj07w56](https://ror.org/05gj07w56)), while MDPI's
unnamed twin entry with the same award (Y202558551) carries Australia's `03z942k20`.

## Why it matters

Funder ROR IDs are what funders, OpenAlex-style indexes and research-assessment tools now
count. A Hubei grant credited to Anhui is missing from Hubei's count and inflates Anhui's.
Of the 50 works carrying Anhui's department ID, at least 32 are Hubei or Gansu funding.

## What could fix it (for the owners to judge)

- **ROR:** add the English forms used in papers as aliases, e.g. "Department of Science and
  Technology of Hubei Province" to 00tbh0t11, "Henan Provincial Department of Science and
  Technology" to 058p20n09, "Department of Science and Technology of Gansu Province" to
  03xz2hx98. (Separately, Anhui's record 01e70gy59 is geocoded to Baohe, **Yunnan**;
  Anhui's Baohe is a district of Hefei.)
- **Crossref matcher:** treat Chinese province names (and other sub-national names) like
  country names: the chosen record must not name a different province. Where a Funder
  Registry name or alternate name matches exactly, prefer the ROR record that ROR maps to
  that Funder ID. Do not add a ROR ID that contradicts a funder DOI in the same entry.
- **MDPI:** nest the ROR ID inside the named funder entry, and do not assign a ROR ID to a
  generic name whose country or province does not match.

## How to check

```
https://api.crossref.org/works?filter=ror-id:https://ror.org/01e70gy59&query.funder-name=Hubei&rows=40&select=DOI,funder
https://api.crossref.org/works?filter=ror-id:https://ror.org/03rbw2w25&query.funder-name=Henan&rows=40&select=DOI,funder
https://api.crossref.org/works?filter=ror-id:https://ror.org/04qgr7x96&query.funder-name=Yunnan+Sichuan+Shanxi+Fujian+Henan&rows=40&select=DOI,funder
https://api.crossref.org/works?filter=ror-id:https://ror.org/03z942k20,member:1968&rows=15&select=DOI,funder
https://api.ror.org/v2/organizations?affiliation=Henan%20Provincial%20Department%20of%20Science%20and%20Technology
https://api.ror.org/v2/organizations?query.advanced=external_ids.all:501100018806
python funder_ror_check.py 10.1016/j.mseb.2026.119859
python funder_ror_check.py --ror 01e70gy59
```

## Limits

- Targeted: we looked at ROR records we expected to attract wrong matches. The counts are
  floors for those records, not error rates for Crossref or MDPI.
- The Hunan row covers the first 40 of 64 works returned; the other 24 were not read.
- Pairing MDPI's unnamed entries by award number is our reading; entries with no award
  could not be paired and were counted as "just a generic name" or left out.
- "Korean setting" for the Singapore rows is an inference from grant-number formats and
  co-listed Korean funders, not from the papers' text.
- `query.funder-name` is a relevance search; the rows above were read entry by entry, and
  only entries that carry the ROR ID in question were counted.

Contact: MV2, Munim, Inc., mv2@munimtech.com.
