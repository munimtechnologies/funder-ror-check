# FINDINGS-MOST-1: Taiwanese and Chinese grants filed under Vietnam's and Korea's "Ministry of Science and Technology" in Crossref

By MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-15. Made with AI agents working in MV2's name;
not reviewed by a human. Text and data CC BY 4.0.

## In short

Of the 48 Crossref Funder Registry records that a search for "ministry of science and technology"
returns, two carry the bare name **"Ministry of Science and Technology"**, with no country in the
name:

| Funder ID | Registry name | Country | Alternative names | Works carrying it (2026-11-15) | Created in 2026 |
|---|---|---|---|---|---|
| [10.13039/100007225](https://api.crossref.org/funders/100007225) | Ministry of Science and Technology | Vietnam | MOST; ... of the Socialist Republic of Vietnam; Vietnamese ... | 10,597 | 553 |
| [10.13039/501100003711](https://api.crossref.org/funders/501100003711) | Ministry of Science and Technology | South Korea | MOST | 7,033 | 113 |

The other science ministries have the country in their registry name: "Ministry of Science and
Technology, Taiwan" ([501100004663](https://api.crossref.org/funders/501100004663), 78,315 works)
and "Ministry of Science and Technology of the People's Republic of China"
([501100002855](https://api.crossref.org/funders/501100002855)). Korea's ministry of that name
was merged into a new ministry in February 2008, yet 93 of the 100 works we sampled under its ID
were registered in 2009 or later.

**Most works carrying either bare-named ID were funded in Taiwan or China.**

### Vietnam's ID (10.13039/100007225): 184 random draws

Two calls with Crossref's `sample=100` returned 100 and 84 readable items (the fetch tool cut
the second page). One DOI came up in both, so there are 183 distinct works.

- **By grant number or entry name alone** (what `award_country_check.py` 0.3.0 labels):
  **109 of 184 draws (59.2%; 95% Wilson interval 52.0% to 66.1%) carry another country's grant**
  on the entry with Vietnam's ID: **Taiwan 73** (MOST/NSC/NSTC project numbers such as
  `MOST 103-2221-E-006-093-MY3`), **China 30** (`2016YFA0204100`, `2011CB707906`,
  `2015ZX04005003`), India 4, Korea 2. **7 are Vietnamese** (3.8%; 1.9% to 7.6%), for example
  `2372/QD-BKHCN` and `ĐTĐL.CN-116/21`. 68 have no award in a known format. That is about
  **5,500 to 7,000 works**, of which Taiwan's share alone is about 3,500 to 5,000.
- **Adding co-funders** (judged by hand, row by row in the CSV): **141 of 184 draws (76.6%; 70.0%
  to 82.2%) point to another country**: Taiwan 79, China 50, India 5, Korea 3, Spain 2, Indonesia
  1, Israel 1. 6 point to Vietnam, 1 is mixed, 36 have no signal.

### Korea's ID (10.13039/501100003711): 100 random draws

- **By grant number or entry name alone: 50 of 100 (40.4% to 59.6%) carry another country's
  grant**: Taiwan 34, China 14, India 2. **2 carry a Korean NRF number.** 48 have none in a
  known format. That is about **2,800 to 4,200 works**.
- **Adding co-funders: 62 of 100 (52.2% to 70.9%) point to another country** (Taiwan 39, China 15,
  India 6, Spain 1, Brazil 1); **10 point to Korea** (5.5% to 17.4%); 28 have no signal.

Taken together, roughly **5,300 to 8,000 works funded by Taiwan's science ministry or council sit
on Vietnam's or Korea's Funder ID** (by grant number alone: about 3,500 to 5,000 on Vietnam's and
1,800 to 3,100 on Korea's). They are missing from the count on Taiwan's own record.

The samples are in
[data/most-vn-kr-sample-2026-11-15.csv](data/most-vn-kr-sample-2026-11-15.csv): one row per
draw, with the target entry's awards, the tool's label, our hand label and its basis.

## Seven records re-read raw

Each was read in full from `api.crossref.org/works/<doi>`. In all seven the bare-named ID is on
an entry with `"doi-asserted-by": "publisher"`, so the publisher deposited it. Crossref's matcher
did not add it.

| DOI | Publisher | Entry carrying the ID | Why it is not that country's |
|---|---|---|---|
| [10.1002/sim.7652](https://api.crossref.org/works/10.1002/sim.7652) | Wiley | Vietnam's, "Ministry of Science and Technology", awards `MOST 105-2118-M-006-007-MY2 and MOST 106-2118-M-006-011-MY3` | Taiwan MOST project numbers; first author at National Cheng Kung University, Tainan |
| [10.1109/nano63165.2025.11113507](https://api.crossref.org/works/10.1109/nano63165.2025.11113507) | IEEE, 2025 | Vietnam's, "Ministry of Science and Technology (MOST)", award `111-2221-E-002-080-MY3` | all six authors at National Taiwan University; the other entry is Taiwan's NSTC |
| [10.1093/nsr/nwy065](https://api.crossref.org/works/10.1093/nsr/nwy065) | OUP | Vietnam's (two entries), awards `2016YFA0204100`, `2017YFA0208200` | China's National Key R&D Programme; authors at Soochow University, Suzhou, and Hong Kong PolyU |
| [10.1016/j.biortech.2026.134194](https://api.crossref.org/works/10.1016/j.biortech.2026.134194) | Elsevier, created 2026-02-12 | Vietnam's, award `2025YFA0921202` | China's National Key R&D Programme; co-funders National Key R&D Program of China and Jiangnan University |
| [10.1016/j.asjsur.2026.05.002](https://api.crossref.org/works/10.1016/j.asjsur.2026.05.002) | Elsevier, created 2026-05-29 | Vietnam's, named **"Socialist Republic of Vietnam Ministry of Science and Technology"**, no award | every other funder is Taiwanese (Taipei Veterans General Hospital, Health Promotion Administration, Ministry of Health and Welfare, and "Ministry of Science and Technology, Taiwan" with `NSTC 112-2314-B-075-016`); the Vietnamese name looks like the label of a picker choice |
| [10.1109/tia.2023.3281537](https://api.crossref.org/works/10.1109/tia.2023.3281537) | IEEE | Korea's, seven entries, awards `110-2221-E-007-074` and six more | Taiwan MOST project numbers; all authors at National Tsing Hua University, Hsinchu |
| [10.1002/adsr.202200052](https://api.crossref.org/works/10.1002/adsr.202200052) | Wiley | Korea's, three entries, awards `2021YFF0703500`, `2022YFE0103500`, `2021YFA0910100` | China's National Key R&D Programme; authors at Shanghai Jiao Tong University |

## Where it comes from

- **Publishers** of the 10,597 works on Vietnam's ID: Elsevier 2,520, Wiley 2,153, IEEE 2,318
  ("IEEE" 1,765 plus the long name 553), Springer 957, OUP 945. Of the 553 created in 2026,
  Elsevier deposited 289.
- On Korea's ID (7,033 works): Elsevier 2,978, IEEE 2,184 (1,427 plus 757), Wiley 435, ACS 285.
  IEEE deposited 70 of the 113 created in 2026.
- **Registry names.** Taiwan's and China's records carry the country in their main name, so a
  funding statement that says just "Ministry of Science and Technology" (as most Taiwanese and
  many Chinese papers do) matches the two bare-named records exactly. ROR's record for Vietnam's
  ministry ([02b207r52](https://ror.org/02b207r52), which lists Funder ID 100007225) also
  displays just "Ministry of Science and Technology".
- We do not know how each publisher's form picks among them. The 2026 Elsevier record above,
  labelled "Socialist Republic of Vietnam ...", suggests the author or editor chose from a list
  that offers Vietnam's record for the bare name.

## Prior art

We searched the web, Crossref's documentation and community forum, and GitHub (issues mentioning
`100007225`) for reports that Vietnam's or Korea's Funder ID carries other countries' grants. We
found none. Web search does turn up single instances in public records (for example Zenodo
deposits that cite 100007225 next to a Taiwan MOST number), but we found no one who has measured
it. A 2023 Crossref forum thread
([t/4466](https://community.crossref.org/t/funder-registry-1-missing-relationships-and-statuses-2-obsolete-labels/4466))
notes that Taiwan's MOST was renamed NSTC; it does not touch the bare-name records. Our own
[FINDINGS-COUNTRY-1.md](FINDINGS-COUNTRY-1.md) covers a different path (Crossref's ROR matcher
giving China's ministry Taiwan's ROR ID). [FINDINGS-NRF-1.md](FINDINGS-NRF-1.md) (South Africa's
"National Research Foundation") and [FINDINGS-MOE-1.md](FINDINGS-MOE-1.md) (Thailand's "Ministry
of Education") found the same bare-name pattern for other funders.

## How to check

```
https://api.crossref.org/funders?query=ministry+of+science+and+technology&rows=100
https://api.crossref.org/funders/100007225
https://api.crossref.org/works?filter=funder:10.13039/100007225&rows=0&facet=publisher-name:15
https://api.crossref.org/works?filter=funder:10.13039/100007225,from-created-date:2026-01-01&rows=0&facet=publisher-name:10
https://api.crossref.org/works?filter=funder:10.13039/100007225&sample=100&select=DOI,funder,publisher,created
https://api.crossref.org/works?filter=funder:10.13039/501100003711&sample=100&select=DOI,funder,created
python award_country_check.py --funder 100007225 --home VN --formats KR,SG,CN,TW,TH,SK,VN,IN --out-dir out
python award_country_check.py --funder 501100003711 --home KR --formats KR,SG,CN,TW,TH,SK,VN,IN --out-dir out
```

A Taiwan MOST/NSC/NSTC project number reads: ROC year (98 to 114), a 4-digit programme code,
a field letter, an institution code and a serial, e.g. `MOST 106-2221-E-156-005`.

## Limits

- The samples came from Crossref's `sample` parameter and were read through a summarising fetch
  tool. Seven records were re-read raw and all matched; the CSV is our transcription.
- The tool tier counts only formats `award_country_check.py` 0.3.0 knows. Vietnamese and Korean
  grants often have no number at all, so both tiers undercount home rows; the hand tier uses
  co-funders to make up for this. Co-funders show where the work was funded, not which ministry
  the authors meant.
- The 184 Vietnam draws include one repeat; counting each work once gives 108 of 183 (59.0%) by
  grant number and 140 of 183 (76.5%) with co-funders.
- Many IEEE conference papers carry the bare ID with no award and no co-funder; they stay
  unplaced although many are from conferences held in Taiwan.
- Counts change daily; every number is from 2026-11-15. A census by script is pre-registered in
  [PREREG-MOST-1.md](PREREG-MOST-1.md) and has not run yet.

## Who could fix it

- Publishers' funder pickers (Elsevier, Wiley, IEEE, Springer, OUP): show the country next to each
  "Ministry of Science and Technology" and check grant formats. A `MOST 1xx-2xxx-X-xxx-xxx` number
  belongs to Taiwan (501100004663, or NSTC 100020595 since 2022); a `20xxYFx…`, `…CB…`, `…ZX…`
  number to China (501100002855).
- Crossref's Funder Registry and ROR: put the country in the displayed name of both bare-named
  records, as is already done for Taiwan's and China's, and consider marking Korea's 2008-defunct
  ministry as replaced.
- Re-matching: works whose entry carries a Taiwanese or Chinese grant number can be moved by rule.
  The census CSV will list them.
