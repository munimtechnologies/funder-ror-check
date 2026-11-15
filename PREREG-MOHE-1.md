# PREREG-MOHE-1: scripted census of Egypt's "Ministry of Higher Education" Funder ID

By MV2, Munim, Inc. (mv2@munimtech.com). Written 2026-11-15, before the census ran. Made with
AI agents working in MV2's name; not reviewed by a human. CC BY 4.0.

## What will be counted

Every Crossref work carrying Funder ID 10.13039/501100002385 (Egypt's record, main name
"Ministry of Higher Education"; 4,177 works on 2026-11-15), read through the public API with
[mohe_census.py](mohe_census.py) v0.1.0 (standard library only; tests in
`test_mohe_census.py`). For each work it records:

- `award_my`: an award on the Egyptian entry in a Malaysian format (FRGS, LRGS, PRGS, ERGS, TRGS,
  RAGS, or a Universiti Teknologi Malaysia vote code such as `R.J130000.7845.4L669`).
- `name_my_strict`: the Egyptian entry's own name contains "Malaysia".
- `cof_my`: another funder entry on the work is Malaysian (Malaysian name words, Malaysia's
  Funder ID 10.13039/501100003093, or a Malaysian award format).
- `name_eg`, `cof_eg`: the Egyptian entry or another entry names Egypt, an Egyptian university or
  an Egyptian programme (E-JUST, Newton-Mosharafa, the Academy of Scientific Research and
  Technology, the Science and Technology Development Fund when no Macau funder is present).
- Verdict: `MY` (Malaysian signal only), `EG` (Egyptian only), `BOTH`, `NONE`.

The script is narrower than the hand labels in FINDINGS-MOHE-1: it ignores other countries,
venue, and university grant codes other than UTM's.

## How blind the predictions are

Not blind to the 199-work hand sample or the record's facets (both in FINDINGS-MOHE-1). They are
written before any scripted count of the whole record was seen.

## Predictions

1. `MY` verdicts: between **1,250 and 1,950** works.
2. `EG` verdicts: between **150 and 550**, and `MY` is at least **3 times** `EG`.
3. `award_my` (Malaysian award format on the Egyptian entry itself): between **450 and 900**.
4. `name_my_strict` (the Egyptian entry is named with "Malaysia"): between **20 and 250**.
5. At least **95%** of `MY` works have the Egyptian entry asserted by the publisher only.
6. At least **50** `MY` works were created in 2026.
7. IEEE plus Elsevier (all name forms) account for at least **65%** of `MY` works.

Method check (not a prediction): the three known rows (10.1021/acsomega.6c06914 -> MY,
10.1109/icocet63343.2024.10730485 -> MY, 10.1016/j.cie.2021.107300 -> EG) must come out as
expected. If any fails, the census is reported as invalid and the predictions are not graded.

## Grading

Each prediction is graded as held or failed in GRADING-MOHE-1.md with the census CSV, whatever
the outcome. If the total number of works scanned differs from the API's total by more than 2%,
that is reported next to the grades.
