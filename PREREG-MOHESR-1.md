# PREREG-MOHESR-1: scripted census of the UAE's "Ministry of Higher Education and Scientific Research" Funder ID

By MV2, Munim, Inc. (mv2@munimtech.com). Written 2026-11-16, before the census ran. Made with
AI agents working in MV2's name; not reviewed by a human. CC BY 4.0.

## What will be counted

Every Crossref work carrying Funder ID 10.13039/100009122 (the UAE's record, main name
"Ministry of Higher Education and Scientific Research", alternate names including "Ministry of
Education" and "MOE"; 1,763 works on 2026-11-16), read through the public API with
[mohesr_census.py](mohesr_census.py) v0.1.0 (standard library only; tests in
`test_mohesr_census.py`). For each work it records:

- `award_countries`: national award formats on the UAE entry itself (Korean NRF/MSIT, Singapore
  MOE AcRF, Malaysian FRGS-type and UTM vote codes, Chinese NCET/IRT/humanities codes, Algerian
  PRFU, Tunisian `LR..` laboratory codes, Japanese `JP..` KAKENHI/AMED, Indian STARS, Czech
  operational programme codes).
- `name_countries`: country words in the UAE entry's own name (UAE words count as AE).
- `cof_countries`: country words in other entries' names, or a known national Funder ID on
  another entry (NRF Korea, MSIT, Korea's Ministry of Education, NSFC, Taiwan's NSTC/MOST/NSC and
  Academia Sinica, NRF Singapore, A*STAR, Malaysia's MOHE, Algeria's DGRSDT, Iraq's MoHESR, JSPS,
  United Arab Emirates University).
- `named_moe`: the UAE entry is named exactly "Ministry of Education", "MOE" or "Ministry of
  Education (MOE)".
- Verdict: `FOREIGN` (only non-UAE signals), `AE` (only UAE), `BOTH`, `NONE`.

The script is narrower than the hand labels in FINDINGS-MOHESR-1 in places (no Spanish, French,
Polish or Brazilian signals; fewer Chinese and Taiwanese words) and broader in one (it counts
Czech and Japanese co-funder IDs or words that the hand rule left unclear when they were the only
signal).

## How blind the predictions are

Not blind to the 198-work hand sample or the record's facets (both in FINDINGS-MOHESR-1). They
are written before any scripted count of the whole record was seen.

## Predictions

1. Works with a Korean award format on the UAE entry (`award_country.KR`): between **300 and
   600**.
2. `FOREIGN` verdicts: between **900 and 1,450**.
3. `AE` verdicts: between **10 and 150**, and `FOREIGN` is at least **8 times** `AE`.
4. Works with any Korean signal (`any_country.KR`): between **350 and 700**, the largest of any
   country.
5. At least **95%** of `FOREIGN` works have the UAE entry asserted by the publisher only.
6. At least **120** `FOREIGN` works were created in 2026.
7. `named_moe` works: between **550 and 950**, and among them `FOREIGN` is at least **10 times**
   `AE`.

Method check (not a prediction): the five known rows (10.1002/celc.202200093,
10.1109/cvpr52733.2024.00944 and 10.1128/aem.00286-26 -> FOREIGN;
10.1016/j.compind.2024.104225 and 10.1016/j.ultsonch.2024.107015 -> AE) must come out as
expected. If any fails, the census is reported as invalid and the predictions are not graded.

## Grading

Each prediction is graded as held or failed in GRADING-MOHESR-1.md with the census CSV, whatever
the outcome. If the total number of works scanned differs from the API's total by more than 2%,
that is reported next to the grades.
