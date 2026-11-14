# SPDX-License-Identifier: Apache-2.0
# Tests for award_country_check.py (standard library unittest, no network).
# Made with AI agents working in the name of MV2, Munim, Inc.
import os
import tempfile
import unittest
import urllib.parse

import award_country_check as acc

ZA_ID = "10.13039/501100001321"


class TestCompactAndSplit(unittest.TestCase):
    def test_compact_strips_dashes_and_spaces(self):
        self.assertEqual(acc.compact("RS-2023-00281839"), "RS202300281839")
        self.assertEqual(acc.compact("RS‐2023‐00217778"), "RS202300217778")
        self.assertEqual(acc.compact("UID 96354"), "UID96354")

    def test_compact_drops_lead_words(self):
        self.assertEqual(acc.compact("Grant no. 84379"), "84379")
        self.assertEqual(acc.compact("No. 90341"), "90341")

    def test_split_awards(self):
        self.assertEqual(acc.split_awards("116017, 119588"), ["116017", "119588"])
        self.assertEqual(acc.split_awards("UID109333 and UID 116338)"),
                         ["UID109333", "UID 116338)"])
        self.assertEqual(acc.split_awards(""), [])


class TestClassifyAward(unittest.TestCase):
    def test_korea(self):
        for a in ["2019R1A2C1003456", "NRF-2019R1A2C2011478", "RS-2023-00281839",
                  "RS-2022-NR072349", "NRF-2012-M3C1A1-048860",
                  "2014K1A3A1A09063027", "2013M2A8A1040268", "2012-0001509",
                  "KRF-2009-0072538", "NRF-2010-6145", "NRF-2006-2004042",
                  "2020R1H1A110101311", "NRF‐2022M3C1A3081312"]:
            self.assertEqual(acc.classify_award(a), "KR", a)

    def test_singapore(self):
        for a in ["NRF-CRP22-2019-0001", "NRF2011NRF‐NRFF001‐042",
                  "NRF2016NRF-NSFC002-013", "NRF2021-QEP2-02-P03"]:
            self.assertEqual(acc.classify_award(a), "SG", a)

    def test_china(self):
        self.assertEqual(acc.classify_award("2022A1515010159"), "CN")
        self.assertEqual(acc.classify_award("2023A1515011531"), "CN")

    def test_south_africa(self):
        for a in ["UID 96354", "61251", "TTK2204011621", "PR_MND230213674275",
                  "CSUR160414162143", "SRUG200224506537", "RA22111973672",
                  "MND 200630538954", "Grant no. 84379", "IFR170125217588"]:
            self.assertEqual(acc.classify_award(a), "ZA", a)

    def test_unknown(self):
        for a in ["2090155358", "N/A", "", "62171294", "A423100",
                  "2016RIDIA3B03934419", "JP20K12345"]:
            self.assertIsNone(acc.classify_award(a), a)


class TestNamesAndEntries(unittest.TestCase):
    def test_classify_name(self):
        self.assertEqual(acc.classify_name("National Research Foundation of Korea"), "KR")
        self.assertEqual(acc.classify_name("NRF (NRF) of South Africa"), "ZA")
        self.assertEqual(acc.classify_name("Guangdong Basic and Applied Basic Research Foundation"), "CN")
        self.assertIsNone(acc.classify_name("National Research Foundation"))
        self.assertIsNone(acc.classify_name(None))

    def test_classify_entry_mixed(self):
        e = {"name": "National Research Foundation",
             "award": ["UID 116331", "2019R1A2C1003456"]}
        self.assertEqual(acc.classify_entry(e), {"ZA", "KR"})

    def test_classify_entry_empty(self):
        self.assertEqual(acc.classify_entry({"name": "National Research Foundation"}), set())

    def test_norm_funder(self):
        self.assertEqual(acc.norm_funder("501100001321"), ZA_ID)
        self.assertEqual(acc.norm_funder("https://doi.org/10.13039/501100001321"), ZA_ID)
        self.assertEqual(acc.norm_funder(ZA_ID), ZA_ID)


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

    def test_summarize(self):
        rows = [acc.classify_work(w, ZA_ID, "ZA") for w in (KR_WORK, ZA_WORK, UN_WORK)]
        s = acc.summarize(rows, 3, ZA_ID, "ZA")
        self.assertEqual(s["works_scanned"], 3)
        self.assertEqual(s["verdict"], {"FOREIGN": 1, "HOME": 1, "UNCLEAR": 1})
        self.assertEqual(s["foreign_label"], {"KR": 1})
        self.assertEqual(s["foreign_by_publisher"], {"Elsevier BV": 1})
        self.assertEqual(s["foreign_by_year"], {"2026": 1})
        self.assertEqual(s["foreign_asserted_by"], {"publisher": 1})

    def test_main_writes_files(self):
        fetch, _ = fake_fetch_factory({"*": ([KR_WORK, ZA_WORK], None)})
        orig = acc.http_get_json
        acc.http_get_json = fetch
        try:
            with tempfile.TemporaryDirectory() as d:
                # scan() binds fetch at definition time, so patch its default.
                saved = acc.scan.__defaults__
                acc.scan.__defaults__ = (fetch,) + saved[1:-1] + (0,)
                try:
                    s = acc.main(["--funder", "501100001321", "--home", "za",
                                  "--out-dir", d])
                finally:
                    acc.scan.__defaults__ = saved
                self.assertEqual(s["verdict"], {"FOREIGN": 1, "HOME": 1})
                self.assertTrue(os.path.exists(os.path.join(d, "works-501100001321.csv")))
                self.assertTrue(os.path.exists(os.path.join(d, "summary-501100001321.json")))
        finally:
            acc.http_get_json = orig


if __name__ == "__main__":
    unittest.main()
