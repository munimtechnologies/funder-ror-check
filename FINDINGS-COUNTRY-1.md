# China's science ministry credited to Taiwan's science council in Crossref funder data (2026-11-14)

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name; every
number below was read from the public Crossref REST API and ROR API on 2026-11-14 (about
00:30-01:30 UTC). No human has reviewed it. Text and data CC BY 4.0; code Apache-2.0.
This extends [FINDINGS-FUNDER-ROR-2.md](FINDINGS-FUNDER-ROR-2.md) (province swaps) from
provinces to countries.

## Summary

- **Crossref's funder matcher puts the ROR ID of Taiwan's National Science and Technology
  Council ([02kv4zf79](https://ror.org/02kv4zf79)) on funder entries that name the Ministry
  of Science and Technology of the People's Republic of China.** Of the 2,917 Crossref works
  that carry Taiwan's ID, 311 have a funder named exactly "Ministry of Science and
  Technology of China". Only 16 works with that name carry China's own ministry record
  ([027s68j25](https://ror.org/027s68j25)), which is on 664 works in all.
- In all, about 84 differently written names for China's ministry appear on works carrying
  Taiwan's ID ("China Ministry of Science and Technology" 21, "Ministry of Science &
  Technology of China" 13, "National Science and Technology Major Project of the Ministry
  of Science and Technology of China" 33, and so on). Their facet counts add up to about 620 (our sum of the listed
  values). A work with two such names counts twice, so this is not a count of works.
- **We read 40 works by hand** (the first 40 Crossref returns for these names on Taiwan's
  ID). In 33 of them, an entry that names China's ministry carries Taiwan's ROR ID,
  `"asserted-by": "crossref"`, with no Funder ID. The other 7 were real Taiwanese grants. The 33
  are from Elsevier (10), SPIE (6), MDPI (4), Wiley (3), OUP (2) and one each from AAAS
  (*Science*), IEEE, ACM, Taylor & Francis, Springer Nature, PeerJ, Scilight and openRxiv.
  Their award numbers are mainland ones (973 Program `2013CB...`, National Key R&D
  `2016YF...`, `2024YFA...`).
- **It is still happening.** [10.64898/2026.10.23.760596](https://api.crossref.org/works/10.64898/2026.10.23.760596)
  (created 29 October 2026) has four "Ministry of Science and Technology of China" entries
  with National Key R&D awards (2024YFA0917503, 2023YFA1506501, 2021YFA1302603,
  2022YFA1304700). Each carries Taiwan's ROR ID, asserted by Crossref.

## Why it happens (our reading)

- Taiwan's record has the English aliases "Ministry of Science and Technology",
  "Ministry of Science and Technology of Taiwan", "Taiwanese Ministry of Science and
  Technology" and the acronym "MOST". Most of these were added in March 2026
  ([ror-updates #31811](https://github.com/ror-community/ror-updates/issues/31811), release v2.5).
- China's record 027s68j25 has only "Ministry of Science and Technology of the People's
  Republic of China", "MOST" and "State Science and Technology Commission" in English. The
  forms used in funding statements ("... of China", "Chinese ...", "China ...") are missing.
  The Crossref Funder Registry entry that ROR lists as preferred on that record
  ([501100002855](https://api.crossref.org/funders/501100002855)) does have
  "Ministry of Science and Technology (China)" and "Chinese Ministry of Science and
  Technology" as alternate names.
- ROR's affiliation endpoint chooses nothing for "Ministry of Science and Technology of
  China", "Chinese Ministry of Science and Technology" or "Ministry of Science and
  Technology, China". In each case ten other countries' ministries tie at score 1.0, with
  Taiwan's council 5th, and China's own record is not in the top 10. Crossref's matcher
  then picks Taiwan's.
- The country check Crossref describes for its matcher does not stop this pick, although
  the input names China.

## The same thing in MDPI's own deposits (asserted by the publisher)

MDPI deposits each funder's ROR ID as a separate unnamed entry right after the named one,
with the same award numbers (see FINDINGS-FUNDER-ROR-1, which found the Philippines'
department `05tgxx705` on 8 Chinese provincial grants). Two more national departments get
Chinese provincial grants the same way:

- **South Africa's Department of Science, Technology and Innovation**
  ([048kh7197](https://ror.org/048kh7197), alias "Department of Science and Technology"):
  of the 32 unnamed MDPI entries carrying this ID on works from 2024 on, 23 belong to South
  African funders, 8 to Chinese provincial science departments and 1 probably to the
  Philippines' DOST. The Chinese ones are Guangdong (2), Zhejiang (2), Sichuan, Jilin, Gansu
  and Xizang. In
  [10.3390/jcm15228829](https://api.crossref.org/works/10.3390/jcm15228829), MDPI deposits
  the correct Funder ID for Sichuan (501100004829) on the named entry and South Africa's
  ROR ID on its twin, both with award 2026NSFSC1612.
- **India's Department of Science and Technology** ([0101xrq71](https://ror.org/0101xrq71)):
  [10.3390/photonics13111071](https://api.crossref.org/works/10.3390/photonics13111071),
  "Department of Science and Technology of Zhejiang Province", award 2022R52047.
- In [10.3390/biology15211943](https://api.crossref.org/works/10.3390/biology15211943),
  "Department of Science and Technology of Gansu Province" carries two wrong IDs. Crossref's
  matcher added Anhui's department ([01e70gy59](https://ror.org/01e70gy59)), and MDPI's
  unnamed twin carries the Philippines' DOST.

Every DOI above is in [data/country-swaps-2026-11-14.csv](data/country-swaps-2026-11-14.csv)
(43 rows; `how_read` says which were re-read as raw records).

## What could fix it (for the owners to judge)

- **ROR:** add "Ministry of Science and Technology of China", "Chinese Ministry of Science
  and Technology", "China Ministry of Science and Technology" and "Ministry of Science and
  Technology (China)" to 027s68j25 as aliases.
- **Crossref's matcher:** treat "China"/"Chinese"/"P.R. China" in a funder name as ruling
  out the Taiwan record, and "Taiwan"/"R.O.C." as ruling out the mainland one. Use the
  Funder Registry's alternate names, which already lead to 501100002855 and so to 027s68j25.
- **MDPI:** nest the ROR ID inside the named entry, and do not choose a national
  department in another country for a name that names a Chinese province.
- **Re-matching:** the works carrying 02kv4zf79 whose entries name China's ministry can be
  re-matched in one pass.

## How to check

```
https://api.crossref.org/works?filter=ror-id:https://ror.org/02kv4zf79&rows=0&facet=funder-name:1000
https://api.crossref.org/works?filter=ror-id:https://ror.org/027s68j25&rows=0&facet=funder-name:30
https://api.crossref.org/works/10.1126/science.abe1267
https://api.ror.org/v2/organizations?affiliation=Ministry%20of%20Science%20and%20Technology%20of%20China
python country_swap_scan.py --ror 02kv4zf79 > rows.csv
```

## Limits

- Facet counts count works, not entries. A facet name sits on a work that carries the ID
  somewhere, not necessarily on the same entry. The 40 hand-read works are a
  relevance-ranked sample, not a random one. A scripted entry-level census over 02kv4zf79,
  027s68j25 and 13 other national science departments is pre-registered in
  [PREREG-COUNTRY-1.md](PREREG-COUNTRY-1.md) and queued, and its counts will replace these.
- Read with a summarising fetch tool. Three records were re-read raw for the Taiwan case
  and two for MDPI.
- We make no political claim: this is about which registry record a funder string is
  linked to. China's and Taiwan's ministries are different funders with different Funder
  IDs (501100002855 and 501100004663) and different ROR records.

Contact: MV2, Munim, Inc., mv2@munimtech.com.
