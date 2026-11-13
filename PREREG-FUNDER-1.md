# PREREG-FUNDER-1: scripted census of wrong-province funder ROR IDs (registered 2026-11-13)

By MV2, Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name.
Written and published before the census job runs. Text CC BY 4.0; code Apache-2.0.

## What runs

`run_census.py` (this repository) does two things, with no hand-editing of the output:

1. `ror_matcher_probe.py`: for each of the 26 provincial science departments in
   `DEPARTMENTS`, sends three name forms ("*P* Science and Technology Department",
   "*P* Provincial Department of Science and Technology", "Department of Science and
   Technology of *P* Province") to ROR's affiliation matcher and records right / wrong /
   none.
2. `funder_ror_check.py --ror <id>` (v0.1.0) for each of the 26 department ROR IDs: every
   Crossref work carrying the ID, every entry carrying it, with verdicts
   `province-mismatch`, `country-mismatch`, `doi-ror-conflict`, `ok`, `unchecked`,
   `unpaired`.

Outputs: probe.csv, scan.csv, summary.json, suspect_crossref_dois.txt.

## Predictions

How blind each one is, honestly:

| # | Prediction | Blind? |
|---|---|---|
| P1 | Form 1 ("*P* Science and Technology Department") gives exactly 12 wrong, 7 right, 7 none, matching the hand table in FINDINGS-FUNDER-ROR-2. | Not blind: a reproduction check. A change means ROR's index or matcher moved. |
| P2 | Form 2 ("*P* Provincial Department of Science and Technology") gives at least 5 wrong of 26. | Blind except Jiangsu (seen: none chosen). |
| P3 | Form 3 ("Department of Science and Technology of *P* Province") gives at least 5 wrong of 26. | Blind except Hubei (FINDINGS-1: top scores went to non-Chinese bodies). |
| P4 | At least 220 distinct DOIs have a crossref-asserted entry flagged `province-mismatch`, `country-mismatch` or `doi-ror-conflict` across the 26 scans. | Partly informed: the hand counts total 243 works. |
| P5 | Jiangxi's record (00t30yz20) has more crossref-asserted suspect rows than any other scanned record. | Partly informed (53 hand-counted works; Hunan's 64 candidates were only partly read). |
| P6 | At least 5 distinct DOIs have a publisher-asserted suspect row (MDPI or other). | Blind for the scripted pairing. |

## Grading rules

- Counts come from summary.json as written by the job. A scan that fails (works = -1) is
  reported and counts as missing data, not as zero.
- If P1 fails, the other probe predictions are still graded, and the difference from the
  hand table is published.
- All six are graded and published, whatever the outcome.

## Limits known in advance

- `funder_ror_check` names provinces only from the funder name and the ROR record's names;
  a wrong match whose funder name names no province is `unchecked`, so P4 is a floor.
- The ROR and Crossref indexes change daily.
