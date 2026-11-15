# PREREG-MOST-1: full census of foreign grants under the two bare "Ministry of Science and Technology" Funder IDs

Registered 2026-11-15, before the census runs. By MV2, Munim, Inc. (mv2@munimtech.com); made
with AI agents working in MV2's name. Background: [FINDINGS-MOST-1.md](FINDINGS-MOST-1.md).

## What runs

`award_country_check.py` 0.3.0, unchanged, as a sealed batch job:

```
python award_country_check.py --funder 100007225 --home VN --formats KR,SG,CN,TW,TH,SK,VN,IN --out-dir /out --mailto mv2@munimtech.com
python award_country_check.py --funder 501100003711 --home KR --formats KR,SG,CN,TW,TH,SK,VN,IN --out-dir /out --mailto mv2@munimtech.com
python award_country_check.py --funder 501100004663 --home TW --formats KR,SG,CN,TW,TH,SK,VN,IN --out-dir /out --mailto mv2@munimtech.com
```

It pages through every Crossref work carrying the Funder ID (cursor, 1,000 per page). For the
funder entries carrying that ID only, it labels each award number by format (KR, SG, CN, TW, TH,
SK, VN, IN; the South African digits-only rule is off) and the entry name by any country it
names. A work is FOREIGN if any label differs from the home country, HOME if it has only home
labels, and UNCLEAR if it has none.

## Predictions

How blind each one is: P1-P5 and P9-P12 are informed by the random samples in FINDINGS-MOST-1
(not blind). P6 is a guess from the publisher facet. P7, P8, P13 and P14 were not measured before
registering.

For 100007225 (Vietnam, home VN):

- **P1.** total-results is between 10,550 and 10,900.
- **P2.** FOREIGN works make up 52% to 67% of works scanned.
- **P3.** At least 55% of FOREIGN works carry a TW label.
- **P4.** HOME works make up at most 7% of works scanned.
- **P5.** FOREIGN works are at least 8 times as many as HOME works.
- **P6.** Elsevier BV has more FOREIGN works than any other single publisher name.
- **P7.** At least 95% of FOREIGN works have the ID asserted by the publisher only.
- **P8.** At least 200 FOREIGN works were created in 2025 or 2026.

For 501100003711 (South Korea, home KR):

- **P9.** total-results is between 7,000 and 7,250.
- **P10.** FOREIGN works make up 40% to 60% of works scanned.
- **P11.** At least 55% of FOREIGN works carry a TW label.
- **P12.** HOME works make up at most 6% of works scanned.
- **P13.** At least 90% of FOREIGN works were created in 2009 or later.

For 501100004663 (Taiwan's "Ministry of Science and Technology, Taiwan", home TW), as a control:

- **P14.** FOREIGN works make up less than 5% of works scanned.

## Grading

Each prediction is graded exactly as written: held or failed. Before any claim is made, 20
FOREIGN rows of Vietnam's CSV (picked by a fixed rule: every k-th row, k = FOREIGN count / 20,
rounded down) are re-read raw. If fewer than 18 of the 20 really carry a foreign grant on the
entry with Vietnam's ID, the census counts are reported as unreliable and P2-P8 are not claimed.
The same check is done with 10 FOREIGN rows of Korea's CSV (at least 9 must hold for P10-P13).
The results, the CSVs and the grading go into GRADING-MOST-1.md in this repository, including
predictions that fail.
