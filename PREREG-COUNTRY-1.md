# PREREG-COUNTRY-1: entry-level census of cross-country funder ROR IDs (registered 2026-11-14)

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name.
Registered before the census runs; it will be graded as it stands, and any change will be
a dated addendum. Background: [FINDINGS-COUNTRY-1.md](FINDINGS-COUNTRY-1.md).

## Method

`run_country_census.py` (code in this repository, tests in `test_country_swap_scan.py`)
runs `country_swap_scan.py` over 15 national records: Taiwan's NSTC 02kv4zf79, China's
MOST 027s68j25 (capped at 30,000 works), the national science departments of the
Philippines (05tgxx705) and South Africa (048kh7197), India's DST 0101xrq71 and Uttar Pradesh's
DST 02jx32965, and the "Ministry of Science and Technology" records of India, Vietnam,
Bangladesh, Pakistan, Nepal, Myanmar, Laos, Ethiopia, and Bosnia and Herzegovina. For every Crossref work carrying the ID it
takes each funder entry with that ROR ID. Unnamed entries are paired with the earlier named
entry that has the same award list, or with the entry just before when neither has an award. Each entry is classified by the countries its
name mentions: own, foreign, mixed or unclear. Chinese provinces and major cities count as
China, and "Republic of China" or "R.O.C." count as Taiwan unless preceded by "People's".

## Predictions

How blind each one is: **seen** means we saw facet or sample data pointing that way;
**blind** means we had no data on it.

- **P1 (seen):** On 02kv4zf79, at least 250 distinct DOIs have a `foreign` entry (naming
  mainland China) asserted by `crossref`.
- **P2 (seen):** On 02kv4zf79, at least 90% of `foreign` entries are asserted by `crossref`
  (not `publisher`).
- **P3 (blind):** On 02kv4zf79, at least one `foreign` entry also carries the Funder ID of
  China's ministry, 10.13039/501100002855 (a self-contradicting entry).
- **P4 (blind):** The reverse is rare. On 027s68j25 (China's MOST), fewer than 20 entries are
  `foreign` (naming Taiwan or another country).
- **P5 (seen):** On the Philippines', South Africa's and India's departments (05tgxx705,
  048kh7197, 0101xrq71) together, at least 15 distinct DOIs have a `foreign` entry asserted
  by `publisher`.
- **P6 (seen):** At least 90% of the DOIs in P5 are from MDPI.
- **P7 (blind):** Across the nine "Ministry of Science and Technology" records of India,
  Vietnam, Bangladesh, Pakistan, Nepal, Myanmar, Laos, Ethiopia and Bosnia and Herzegovina,
  there are at least 10 `foreign` entries in total.
- **P8 (blind):** On 02kv4zf79, `foreign` entries make up at least 10% of all entries that
  carry the ID.

## Grading

Each prediction is graded held / failed from `summary.json` and `rows.csv`, reading 10
random `foreign` rows per target by hand as a check on the classifier. Classifier errors
found in that check are reported, not fixed after the fact. If the job fails or Crossref's
data changes before it runs, that is reported too.
