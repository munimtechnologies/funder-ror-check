# FINDINGS-MOE-1: Korean, Chinese, Taiwanese and Singaporean grants filed under Thailand's Ministry of Education in Crossref

By MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-14. Made with AI agents working in MV2's name;
not reviewed by a human. Text and data CC BY 4.0.

## In short

Three records in the Crossref Funder Registry carry the bare name "Ministry of Education", with
no country in the name:

| Funder ID | Registry name | Country | Works carrying it (2026-11-14) |
|---|---|---|---|
| [10.13039/100009950](https://api.crossref.org/funders/100009950) | Ministry of Education | Thailand | 6,896 |
| [10.13039/100010002](https://api.crossref.org/funders/100010002) | Ministry of Education | Taiwan | 12,996 |
| [10.13039/501100002701](https://api.crossref.org/funders/501100002701) | Ministry of Education | South Korea | 52,897 |

Most works carrying **Thailand's** ID are not Thai. We drew 200 works at random from the 6,896
(two calls with `sample=100`) and read the funder entry that carries the Thai ID:

- **By grant number or entry name alone** (the rule `award_country_check.py` 0.2.0 applies):
  **46 of 200 draws (23%; 95% Wilson interval 17.7% to 29.3%) carry another country's grant**
  (Korea 31, China 5, Taiwan 5, Singapore 4, Slovakia 1), against **4 Thai**. The other 150 have
  no award number in a known format. That is about **1,200 to 2,000 works**.
- **Adding co-funders and the journal** (judged by hand, row by row in the CSV): **105 of 200
  draws (52.5%; 45.6% to 59.3%) point to another country**: Korea 48, China 21, Taiwan 11,
  Singapore 5 and 20 elsewhere (India 3, Malaysia 3, Germany 3, Saudi Arabia 2, Czech Republic
  2, and one each for Japan, the US, Oman, Russia, Slovakia, Serbia and Chile). **Only 10 point
  to Thailand (5%; 2.7% to 9.0%)**, 4 are mixed, and 81 have no signal. That is about **3,100 to
  4,100 works** credited to Thailand's ministry that another country's funder paid for.
- Of the 119 draws that can be placed at all, 10 (8%) are Thai.

The same DOI came up in both calls three times, so the 200 draws cover 197 distinct works;
counting each once gives 45 of 197 (22.8%) by grant number and 103 of 197 (52.3%) with
co-funders.

It is still happening: **499 works created in 2026 carry the Thai ID, 340 of them from IEEE.**

The sample is in [data/moe-th-sample-2026-11-14.csv](data/moe-th-sample-2026-11-14.csv) (one row per
draw: the Thai entry's name and awards, the tool's label, our hand label and its basis).

## Seven records re-read raw

Each was read in full from `api.crossref.org/works/<doi>`. In all seven, the Thai ID is on the
entry with `"doi-asserted-by": "publisher"`, so the publisher deposited it; Crossref's matcher
did not add it.

| DOI | Publisher, created | Entry carrying 10.13039/100009950 | Why it is not Thai |
|---|---|---|---|
| [10.1111/coa.13597](https://api.crossref.org/works/10.1111/coa.13597) | Wiley, 2020 | "Ministry of Education", award `NRF‐2019R1I1A3A01063629` | Korean NRF Basic Science grant number |
| [10.1002/pola.70190](https://api.crossref.org/works/10.1002/pola.70190) | Wiley, 2026-06 | "Ministry of Education", award `114L9006` | Taiwan's ministry code (ROC year 114); all seven authors at National Cheng Kung University, Tainan; Taiwan's NSTC is the other funder |
| [10.1177/0271678x261444202](https://api.crossref.org/works/10.1177/0271678x261444202) | SAGE, 2026-07 | "ministry of education", awards `RS-2023-00237665, RS-2024-00463129` | Korean RS- grant numbers; all authors at Chungnam National University, Daejeon |
| [10.1093/nsr/nwac231](https://api.crossref.org/works/10.1093/nsr/nwac231) | OUP, 2022 | "Ministry of Education", award `2020AC006` | the other ten entries are Chinese (NSFC, Guangdong, Guangzhou, Qingyuan, Fundamental Research Funds for the Central Universities) |
| [10.1155/2022/3930795](https://api.crossref.org/works/10.1155/2022/3930795) | Wiley (Hindawi), 2022 | **"Ministry of Education, Thailand"** (four entries), awards include `21YJCZH147` | `YJC` is the Chinese Ministry of Education's humanities and social science project format; authors in Jinan and Changsha, China |
| [10.1109/iceic64972.2025.10879611](https://api.crossref.org/works/10.1109/iceic64972.2025.10879611) | IEEE, 2025 | "Ministry of Education", award `RS-2023-00242673` | Korean RS- grant number; all authors at Dong-A University, Busan |
| [10.1016/j.neubiorev.2018.07.016](https://api.crossref.org/works/10.1016/j.neubiorev.2018.07.016) | Elsevier, 2018 | "Ministry of Education" (two entries), awards `MOE2013-T2-2-054`, `MOE2017-T2-1-089` | Singapore's Academic Research Fund Tier 2 format; A*STAR and Duke-NUS co-fund |

The name goes wrong in both directions. In one work an entry named "**Ministry of Education in
Taiwan**" (award `114L9A00303`) carries Thailand's ID
([10.1080/13548506.2025.2594761](https://api.crossref.org/works/10.1080/13548506.2025.2594761),
Taylor & Francis, 2025). In another, a Chinese grant is deposited under the name "Ministry of
Education, **Thailand**" (the Hindawi record above). That looks like the author or the
publisher's form picking the first "Ministry of Education" offered, which is shown as Thailand's.

## Where it comes from

- **Publishers:** IEEE deposits 3,705 of the 6,896 works (54%; "IEEE" 3,578 plus "Institute of
  Electrical and Electronics Engineers (IEEE)" 127), then Wiley 1,157, Elsevier 1,087 and
  OUP 323. Most IEEE rows in the sample are conference papers with a bare "Ministry of
  Education" and no award number, so they stay unplaced.
- **Co-funders:** a `funder-name` facet over the 6,896 works (it counts every entry's name, so it
  is an upper bound) shows "National Natural Science Foundation of China" on 705 works and
  "National Research Foundation of Korea" on 661, plus Korean variants (65, 47, 40, 24). The
  Thai co-funders are much rarer: Office of the Higher Education Commission 217, Thailand
  Research Fund 147, National Research Council of Thailand 51.
- **Registry names:** the Thai record's own name has no country; its alternative names are
  "Ministry of Education of Thailand", "MOE" and the Thai name. ROR's record for the same ministry
  ([036nq5137](https://ror.org/036nq5137), which lists Funder ID 100009950) also displays just
  "Ministry of Education". Korea's and Taiwan's records have the same bare name, yet Thailand's
  receives many of the wrong deposits. Our guess is ordering in the lists that authors and
  publishers pick from, but we could not check that.

## Taiwan's record, for comparison (partial)

One `sample=100` draw from Taiwan's 100010002 was read for its first 70 items only, because the
fetch tool cut the rest. Of those 70, 35 point to Taiwan, 13 elsewhere (Korea 4 with grant
numbers such as `NRF-2019R1A6A1A11051177`, China 4, Singapore 3, Malaysia 1, India 1) and 22
have no signal. The records include one entry named "Ministry of Education (MOE), Singapore"
(award `MOE-T2EP50220-0019`, IEEE TIFS 2024) that carries Taiwan's ID. The bare-name problem
is smaller there, and the census below measures it.

## Prior art

We searched the web, Crossref's documentation and community pages, and GitHub for reports
of `100009950` or bare "Ministry of Education" funder IDs going to the wrong country. We found
none. Metadata Game Changers (Habermann, 2024 and 2026) checked US NSF and NIH look-alikes in
DataCite by award format. arXiv:2609.09984 (Han et al., 2026) disambiguates funder names from
Web of Science; it does not measure wrong IDs in Crossref. One Zenodo dataset
([zenodo.org/records/5108215](https://zenodo.org/records/5108215)) cites the Thai ID with what
looks like a National University of Singapore grant code (`R15400A56133`). That is one more
instance; it is not a report. Our own earlier
[FINDINGS-NRF-1.md](FINDINGS-NRF-1.md) found the same pattern for South Africa's bare
"National Research Foundation".

## How to check

```
https://api.crossref.org/funders/100009950
https://api.crossref.org/works?filter=funder:10.13039/100009950&rows=0&facet=publisher-name:10
https://api.crossref.org/works?filter=funder:10.13039/100009950,from-created-date:2026-01-01&rows=0&facet=publisher-name:10
https://api.crossref.org/works?filter=funder:10.13039/100009950&sample=100&select=DOI,funder,publisher
https://api.crossref.org/works?filter=funder:10.13039/100009950&rows=0&facet=funder-name:40
python award_country_check.py --funder 100009950 --home TH --formats KR,SG,CN,TW,TH,SK --out-dir out
```

`--formats` leaves out the South African digits-only rule, which would otherwise read a plain
number such as the `1001` in a Malaysian grant code as South African.

## Limits

- The two samples came from Crossref's `sample` parameter and were read through a summarising
  fetch tool. Seven records were re-read raw and all matched. The CSV is our transcription; check
  any row against its raw record before relying on it.
- The tool rule only counts award formats it knows: Korean NRF, Singapore MOE/NRF/NUS, Chinese
  Ministry of Education humanities codes and Guangdong, Taiwan's `…L…` ministry codes, Thailand
  Research Fund prefixes and Slovak VEGA. Thai ministry grants often have no number, so the tool
  undercounts Thai rows; the hand tier uses co-funders to make up for this.
- Co-funder evidence shows where the work was funded, not which ministry the authors meant. In
  international collaborations a Thai ministry grant can sit next to foreign co-funders; we
  labelled those MIXED when the signals disagreed.
- Counts change daily, and every number here is from 2026-11-14.
- A full census by script is pre-registered in [PREREG-MOE-1.md](PREREG-MOE-1.md) and has not
  run yet.

## Who could fix it

- Publishers' funder pickers, IEEE's above all: show the country next to each "Ministry of
  Education", and check grant formats (a Korean `RS-` or `…R1A…` number belongs to Korea's
  501100002701).
- Crossref's Funder Registry and ROR: put the country in the displayed name of bare-named
  ministry records ("Ministry of Education (Thailand)"), as the registry already does for
  Singapore's ministry.
- Re-matching: works whose Thai entry carries a Korean, Taiwanese, Chinese or Singaporean grant
  number can be moved by rule. The census CSV will list them.
