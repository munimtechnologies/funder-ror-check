# PREREG-MOE-1: full census of foreign grants under the three bare "Ministry of Education" Funder IDs

Registered 2026-11-14, before the census runs. By MV2, Munim, Inc. (mv2@munimtech.com); made
with AI agents working in MV2's name. Background: [FINDINGS-MOE-1.md](FINDINGS-MOE-1.md).

## What runs

`award_country_check.py` 0.2.0, unchanged, as a sealed batch job:

```
python award_country_check.py --funder 100009950 --home TH --formats KR,SG,CN,TW,TH,SK --out-dir /out --mailto mv2@munimtech.com
python award_country_check.py --funder 100010002 --home TW --formats KR,SG,CN,TW,TH,SK --out-dir /out --mailto mv2@munimtech.com
python award_country_check.py --funder 501100002701 --home KR --formats KR,SG,CN,TW,TH,SK --out-dir /out --mailto mv2@munimtech.com
```

It pages through every Crossref work carrying the Funder ID (cursor, 1,000 per page). For the
funder entries carrying that ID only, it labels each award number by format (KR, SG, CN, TW, TH,
SK; the South African digits-only rule is off) and the entry name by any country it names. A
work is FOREIGN if any label differs from the home country, HOME if it has only home labels,
and UNCLEAR if it has none.

## Predictions

How blind each one is: P1-P6 and P11 are informed by the 200-draw sample in FINDINGS-MOE-1 (not
blind). P9 is informed by a partial 70-item reading of Taiwan's record. P7, P8 and P10 were not
measured before registering.

For 100009950 (Thailand, home TH):

- **P1.** total-results is between 6,850 and 7,200.
- **P2.** FOREIGN works make up 17% to 30% of works scanned.
- **P3.** At least 55% of FOREIGN works carry a KR label.
- **P4.** HOME works make up at most 5% of works scanned.
- **P5.** FOREIGN works are at least 4 times as many as HOME works.
- **P6.** Wiley has more FOREIGN works than any other single publisher name.
- **P7.** At least 90% of FOREIGN works have the ID asserted by the publisher only.
- **P8.** At least 30 FOREIGN works were created in 2025 or 2026.
- **P11.** Among works that are HOME or FOREIGN, FOREIGN makes up at least 80%.

For 100010002 (Taiwan, home TW):

- **P9.** FOREIGN works make up less than 12% of works scanned, and a smaller share than under
  Thailand's ID.

For 501100002701 (South Korea, home KR):

- **P10.** FOREIGN works make up less than 5% of works scanned.

## Grading

Each prediction is graded exactly as written: held or failed. Before any claim is made, 20
FOREIGN rows of Thailand's CSV (picked by a fixed rule: every k-th row, k = FOREIGN count / 20,
rounded down) are re-read raw. If fewer than 18 of the 20 really carry a foreign grant on the
Thai entry, the census counts are reported as unreliable and P2-P11 are not claimed. The
results, the CSVs and the grading go into GRADING-MOE-1.md in this repository, including
predictions that fail.
