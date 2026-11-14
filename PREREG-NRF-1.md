# PREREG-NRF-1: full census of foreign grants under South Africa's NRF Funder ID

Registered 2026-11-14, before the census runs. By MV2, Munim, Inc. (mv2@munimtech.com); made
with AI agents working in MV2's name. Background: [FINDINGS-NRF-1.md](FINDINGS-NRF-1.md).

## What runs

`award_country_check.py` 0.1.0, unchanged, as a sealed batch job:

```
python award_country_check.py --funder 501100001321 --home ZA --out-dir /out --mailto mv2@munimtech.com
python award_country_check.py --funder 501100001381 --home SG --out-dir /out --mailto mv2@munimtech.com
```

It pages through every Crossref work carrying the Funder ID (cursor, 1,000 per page) and, for
the funder entries carrying that ID only, labels each award number by format: KR (Korean NRF
formats), SG (Singapore NRF), CN (Guangdong `20xxA15…`), ZA (UID, plain 4-6 digits, `TTK`,
`CSUR`, `SRUG`… prefixes). A country named in the entry's name also counts. A work is
FOREIGN if any label differs from the home country, HOME if it has only home labels, and
UNCLEAR if it has none.

## Predictions

How blind each one is: P1-P5 are informed by the 200-work sample in FINDINGS-NRF-1 (not
blind). P6-P9 were not measured before registering.

For 501100001321 (South Africa, home ZA):

- **P1.** total-results is between 38,500 and 41,000.
- **P2.** FOREIGN works make up 15% to 30% of works scanned.
- **P3.** At least 75% of FOREIGN works carry a KR label.
- **P4.** At least 5,000 works are FOREIGN.
- **P5.** Among works that are HOME or FOREIGN, FOREIGN makes up 30% to 50%.
- **P6.** Elsevier BV has more FOREIGN works than any other publisher name.
- **P7.** At least 1,000 FOREIGN works were created in 2025 or 2026.
- **P8.** At least 80% of FOREIGN works have the ID asserted by the publisher only.

For 501100001381 (Singapore, home SG), whose registry name includes "Singapore":

- **P9.** FOREIGN works make up less than 5% of works scanned.

## Grading

Each prediction is graded exactly as written: held or failed. Before any claim is made, 20
FOREIGN rows (picked by a fixed rule: every k-th row of the CSV, k = FOREIGN count / 20) are
re-read raw. If fewer than 18 of 20 really carry a foreign grant on the South African entry,
the census counts are reported as unreliable and P2-P8 are not claimed. The results, the CSV
and the grading go into GRADING-NRF-1.md in this repository, including predictions that fail.
