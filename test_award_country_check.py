# SPDX-License-Identifier: Apache-2.0
# Tests for award_country_check.py (standard library unittest, no network).
# Made with AI agents working in the name of MV2, Munim, Inc.
import os
import tempfile
import unittest
import urllib.parse

import award_country_check as acc

ZA_ID = "10.13039/501100001321"
TH_ID = "10.13039/100009950"
NO_ZA = ("KR", "SG", "CN", "TW", "TH", "SK")


class TestCompactAndSplit(unittest.TestCase):
    def test_compact_strips_dashes_and_spaces(self):
        self.assertEqual(acc.compact("RS-2023-00281839"), "RS202300281839")
        self.assertEqual(acc.compact("RS‐2023‐00217778"), "RS202300217778")
        self.assertEqual(acc.compact("UID 96354"), "UID96354")
        self.assertEqual(acc.compact("#21JZD056"), "21JZD056")

    def test_compact_drops_lead_words(self):
        self.assertEqual(acc.compact("Grant no. 84379"), "84379")
        self.assertEqual(acc.compact("No. 90341"), "90341")

    def test_split_awards(self):
        self.assertEqual(acc.split_awards("116017, 119588"), ["116017", "119588"])
        self.assertEqual(acc.split_awards("UID109333 and UID 116338)"),
                         ["UID109333", "UID 116338)"])
        self.assertEqual(acc.split_awards(""), [])
        self.assertEqual(acc.split_awards("VEGA 1/0802/20"), ["VEGA 1", "0802", "20"])


class TestClassifyAward(unittest.TestCase):
    def test_korea(self):
        for a in ["2019R1A2C1003456", "NRF-2019R1A2C2011478", "RS-2023-00281839",
                  "RS-2022-NR072349", "NRF-2012-M3C1A1-048860",
                  "2014K1A3A1A09063027", "2013M2A8A1040268", "2012-0001509",
                  "KRF-2009-0072538", "NRF-2010-6145", "NRF-2006-2004042",
                  "2020R1H1A110101311", "NRF‐2022M3C1A3081312",
                  "RS-2020-NR049590", "RS-2023–00273372", "2018R1A 6A1A 030 15496"]:
            self.assertEqual(acc.classify_award(a), "KR", a)

    def test_singapore(self):
        for a in ["NRF-CRP22-2019-0001", "NRF2011NRF‐NRFF001‐042",
                  "NRF2016NRF-NSFC002-013", "NRF2021-QEP2-02-P03",
                  "MOE2013-T2-2-054", "MOE2017-T2-1-089", "MOE‐T2EP10223‐0002",
                  "MOE-T2EP50220-0019", "R‐154‐000‐B18‐114", "R154‐000‐660‐112",
                  "NRF-NRFF-2011-04"]:
            self.assertEqual(acc.classify_award(a), "SG", a)

    def test_china(self):
        for a in ["2022A1515010159", "2023A1515011531", "21YJCZH147",
                  "17YJC630149", "#21JZD056", "2025JZDZ093", "24JDSZ3126"]:
            self.assertEqual(acc.classify_award(a), "CN", a)

    def test_taiwan(self):
        for a in ["107L9006", "114L9A00303", "113L9006", "107L4000"]:
            self.assertEqual(acc.classify_award(a), "TW", a)

    def test_thailand_and_slovakia(self):
        self.assertEqual(acc.classify_award("MRG6180091"), "TH")
        self.assertEqual(acc.classify_award("IRG5980007"), "TH")
        self.assertEqual(acc.classify_award("VEGA 1"), "SK")

    def test_south_africa(self):
        for a in ["UID 96354", "61251", "TTK2204011621", "PR_MND230213674275",
                  "CSUR160414162143", "SRUG200224506537", "RA22111973672",
                  "MND 200630538954", "Grant no. 84379", "IFR170125217588"]:
            self.assertEqual(acc.classify_award(a), "ZA", a)

    def test_unknown(self):
        for a in ["2090155358", "N/A", "", "62171294", "A423100",
                  "2016RIDIA3B03934419", "JP20K12345", "2020AC006",
                  "SCU2021D005", "MOE 109-S-0023-A", "24-1317-A0001-0",
                  "ZR202103040494", "2021B68", "2020CX041"]:
            self.assertIsNone(acc.classify_award(a), a)

    def test_formats_limit_labels(self):
        self.assertEqual(acc.classify_award("191653"), "ZA")
        self.assertIsNone(acc.classify_award("191653", NO_ZA))
        self.assertIsNone(acc.classify_award("1001", NO_ZA))
        self.assertEqual(acc.classify_award("2019R1A2C1003456", NO_ZA), "KR")
        self.assertIsNone(acc.classify_award("2019R1A2C1003456", ("ZA",)))

    def test_parse_formats(self):
        self.assertEqual(acc.parse_formats("KR,sg, TW"), ("KR", "SG", "TW"))
        self.assertIsNone(acc.parse_formats(""))
        self.assertIsNone(acc.parse_formats(None))
        with self.assertRaises(ValueError):
            acc.parse_formats("KR,XX")


class TestNamesAndEntries(unittest.TestCase):
    def test_classify_name(self):
        self.assertEqual(acc.classify_name("National Research Foundation of Korea"), "KR")
        self.assertEqual(acc.classify_name("NRF (NRF) of South Africa"), "ZA")
        self.assertEqual(acc.classify_name("Guangdong Basic and Applied Basic Research Foundation"), "CN")
        self.assertIsNone(acc.classify_name("National Research Foundation"))
        self.assertIsNone(acc.classify_name(None))

    def test_classify_name_ministries(self):
        self.assertEqual(acc.classify_name("Ministry of Education in Taiwan"), "TW")
        self.assertEqual(acc.classify_name(
            "Ministry of Education (Ministry of Education, Republic of China"), "TW")
        self.assertEqual(acc.classify_name(
            "Ministry of Education of the People's Republic of China"), "CN")
        self.assertEqual(acc.classify_name("Ministry of Education, Thailand"), "TH")
        self.assertIsNone(acc.classify_name("Ministry of Education"))

    def test_classify_entry_mixed(self):
        e = {"name": "National Research Foundation",
             "award": ["UID 116331", "2019R1A2C1003456"]}
        self.assertEqual(acc.classify_entry(e), {"ZA", "KR"})

    def test_classify_entry_empty(self):
        self.assertEqual(acc.classify_entry({"name": "National Research Foundation"}), set())

    def test_classify_entry_vega(self):
        e = {"name": "Ministry of Education", "award": ["VEGA 1/0802/20"]}
        self.assertEqual(acc.classify_entry(e), {"SK", "ZA"})
        self.assertEqual(acc.classify_entry(e, NO_ZA), {"SK"})

    def test_norm_funder(self):
        self.assertEqual(acc.norm_funder("501100001321"), ZA_ID)
        self.assertEqual(acc.norm_funder("https://doi.org/10.13039/501100001321"), ZA_ID)
        self.assertEqual(acc.norm_funder(ZA_ID), ZA_ID)
        self.assertEqual(acc.norm_funder("100009950"), TH_ID)


def work(doi, entries, publisher="P", created="2026-01-02T00:00:00Z"):
    return {"DOI": doi, "publisher": publisher, "funder": entries,
            "created": {"date-time": created}}


KR_WORK = work("10.1/kr", [
    {"name": "National Research Foundation", "DOI": ZA_ID,
     "doi-asserted-by": "publisher", "award": ["RS-2022-NR072349"]},
    {"name": "National Research Foundation of Korea",
     "DOI": "10.13039/501100003725", "award": ["2021R1A2C1093060"]},
], publisher="Elsevier BV", created="2026-04-27T14:58:15Z")
ZA_WORK = work("10.1/za", [
    {"name": "National Research Foundation", "DOI": ZA_ID,
     "doi-asserted-by": "crossref", "award": ["UID 62620"]},
], created="2019-05-01T00:00:00Z")
UN_WORK = work("10.1/un", [
    {"name": "National Research Foundation", "DOI": ZA_ID,
     "doi-asserted-by": "publisher"},
])

# Shaped like 10.1155/2022/3930795: four entries named for Thailand, each with
# one of four Chinese award numbers.
TH_CN_WORK = work("10.1/thcn", [
    {"name": "Ministry of Education, Thailand", "DOI": TH_ID,
     "doi-asserted-by": "publisher", "award": [a]}
    for a in ["2021B68", "ZR202103040494", "21YJCZH147", "2020CX041"]
], publisher="Wiley", created="2022-08-31T16:05:17Z")
TH_HOME_WORK = work("10.1/thhome", [
    {"name": "Ministry of Education", "DOI": TH_ID,
     "doi-asserted-by": "publisher", "award": ["MRG6180091"]},
])
TH_MY_WORK = work("10.1/thmy", [
    {"name": "MOE", "DOI": TH_ID, "doi-asserted-by": "publisher",
     "award": ["RUI/1001/PTEKIND8014119"]},
])
TH_KR_WORK = work("10.1/thkr", [
    {"name": "Ministry of Education", "DOI": TH_ID,
     "doi-asserted-by": "publisher", "award": ["RS-2023-00242673"]},
    {"name": "National Research Foundation of Korea(NRF)",
     "DOI": "10.13039/501100003725", "doi-asserted-by": "publisher"},
], publisher="IEEE", created="2025-02-18T18:17:22Z")


class TestClassifyWork(unittest.TestCase):
    def test_foreign_ignores_other_entries(self):
        r = acc.classify_work(KR_WORK, ZA_ID, "ZA")
        self.assertEqual(r["verdict"], "FOREIGN")
        self.assertEqual(r["foreign"], "KR")
        self.assertEqual(r["entries"], 1)
        self.assertEqual(r["awards"], "RS-2022-NR072349")
        self.assertEqual(r["asserted_by"], "publisher")
        self.assertEqual(r["created"], "2026-04-27")

    def test_home_and_unclear(self):
        self.assertEqual(acc.classify_work(ZA_WORK, ZA_ID, "ZA")["verdict"], "HOME")
        self.assertEqual(acc.classify_work(UN_WORK, ZA_ID, "ZA")["verdict"], "UNCLEAR")

    def test_no_target_entry(self):
        w = work("10.1/x", [{"name": "Other", "DOI": "10.13039/1"}])
        r = acc.classify_work(w, ZA_ID, "ZA")
        self.assertEqual(r["entries"], 0)
        self.assertEqual(r["verdict"], "UNCLEAR")

    def test_thai_ministry_cases(self):
        r = acc.classify_work(TH_CN_WORK, TH_ID, "TH", NO_ZA)
        self.assertEqual(r["entries"], 4)
        self.assertEqual(r["labels"], "CN,TH")
        self.assertEqual(r["foreign"], "CN")
        self.assertEqual(r["verdict"], "FOREIGN")
        self.assertEqual(acc.classify_work(TH_HOME_WORK, TH_ID, "TH", NO_ZA)["verdict"], "HOME")
        k = acc.classify_work(TH_KR_WORK, TH_ID, "TH", NO_ZA)
        self.assertEqual((k["verdict"], k["foreign"], k["entries"]), ("FOREIGN", "KR", 1))

    def test_loose_digits_rule_needs_formats(self):
        # With every format on, the "1001" in a Malaysian grant code would be
        # read as South African; leaving ZA out keeps it UNCLEAR.
        self.assertEqual(acc.classify_work(TH_MY_WORK, TH_ID, "TH")["foreign"], "ZA")
        self.assertEqual(acc.classify_work(TH_MY_WORK, TH_ID, "TH", NO_ZA)["verdict"], "UNCLEAR")


def fake_fetch_factory(pages):
    """pages: dict cursor -> (items, next_cursor). Records cursors asked."""
    asked = []

    def fetch(url):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        cur = q["cursor"][0]
        asked.append((cur, q["filter"][0], q["rows"][0]))
        items, nxt = pages[cur]
        return {"message": {"items": items, "total-results": 3,
                            "next-cursor": nxt}}
    return fetch, asked


class TestScanAndSummary(unittest.TestCase):
    def test_scan_follows_cursor_and_dedups(self):
        fetch, asked = fake_fetch_factory({
            "*": ([KR_WORK, ZA_WORK], "c2"),
            "c2": ([UN_WORK, KR_WORK], "c3"),
            "c3": ([], "c4"),
        })
        out = list(acc.scan(ZA_ID, "ZA", fetch=fetch, rows=2, pause=0))
        self.assertEqual([r["doi"] for _, r in out], ["10.1/kr", "10.1/za", "10.1/un"])
        self.assertEqual([a[0] for a in asked], ["*", "c2", "c3"])
        self.assertEqual(asked[0][1], "funder:" + ZA_ID)
        self.assertEqual(asked[0][2], "2")
        self.assertEqual(out[0][0], 3)

    def test_scan_max_pages(self):
        fetch, asked = fake_fetch_factory({"*": ([KR_WORK], "c2"),
                                           "c2": ([ZA_WORK], None)})
        out = list(acc.scan(ZA_ID, "ZA", fetch=fetch, max_pages=1, pause=0))
        self.assertEqual(len(out), 1)
        self.assertEqual(len(asked), 1)

    def test_scan_passes_formats(self):
        fetch, _ = fake_fetch_factory({"*": ([TH_MY_WORK, TH_KR_WORK], None)})
        out = list(acc.scan(TH_ID, "TH", fetch=fetch, formats=NO_ZA, pause=0))
        self.assertEqual([r["verdict"] for _, r in out], ["UNCLEAR", "FOREIGN"])

    def test_summarize(self):
        rows = [acc.classify_work(w, ZA_ID, "ZA") for w in (KR_WORK, ZA_WORK, UN_WORK)]
        s = acc.summarize(rows, 3, ZA_ID, "ZA")
        self.assertEqual(s["works_scanned"], 3)
        self.assertEqual(s["verdict"], {"FOREIGN": 1, "HOME": 1, "UNCLEAR": 1})
        self.assertEqual(s["foreign_label"], {"KR": 1})
        self.assertEqual(s["foreign_by_publisher"], {"Elsevier BV": 1})
        self.assertEqual(s["foreign_by_year"], {"2026": 1})
        self.assertEqual(s["foreign_asserted_by"], {"publisher": 1})

    def _run_main(self, pages, argv_tail, tag):
        fetch, _ = fake_fetch_factory(pages)
        with tempfile.TemporaryDirectory() as d:
            # scan() binds fetch at definition time, so patch its default.
            saved = acc.scan.__defaults__
            acc.scan.__defaults__ = (fetch,) + saved[1:-1] + (0,)
            try:
                s = acc.main(argv_tail + ["--out-dir", d])
            finally:
                acc.scan.__defaults__ = saved
            self.assertTrue(os.path.exists(os.path.join(d, "works-%s.csv" % tag)))
            self.assertTrue(os.path.exists(os.path.join(d, "summary-%s.json" % tag)))
        return s

    def test_main_writes_files(self):
        s = self._run_main({"*": ([KR_WORK, ZA_WORK], None)},
                           ["--funder", "501100001321", "--home", "za"], "501100001321")
        self.assertEqual(s["verdict"], {"FOREIGN": 1, "HOME": 1})
        self.assertEqual(s["formats"], list(acc.ALL_FORMATS))

    def test_main_with_formats(self):
        s = self._run_main({"*": ([TH_CN_WORK, TH_HOME_WORK, TH_MY_WORK, TH_KR_WORK], None)},
                           ["--funder", "100009950", "--home", "th",
                            "--formats", "KR,SG,CN,TW,TH,SK"], "100009950")
        self.assertEqual(s["verdict"], {"FOREIGN": 2, "HOME": 1, "UNCLEAR": 1})
        self.assertEqual(s["foreign_label"], {"CN": 1, "KR": 1})
        self.assertEqual(s["formats"], list(NO_ZA))
        self.assertEqual(s["foreign_by_year"], {"2022": 1, "2025": 1})


if __name__ == "__main__":
    unittest.main()
