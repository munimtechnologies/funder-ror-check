# SPDX-License-Identifier: Apache-2.0
# Tests for mohe_census.py (no network). Made with AI agents working in the
# name of MV2, Munim, Inc.
import json
import os
import tempfile
import unittest

import mohe_census as m

EG = "10.13039/501100002385"
MY = "10.13039/501100003093"


def work(doi, entries, publisher="Elsevier BV", created="2024-01-02"):
    return {"DOI": doi, "publisher": publisher,
            "created": {"date-time": created + "T00:00:00Z"},
            "funder": entries}


def eg(name="Ministry of Higher Education", award=None, by="publisher"):
    e = {"DOI": EG, "name": name, "doi-asserted-by": by}
    if award is not None:
        e["award"] = award
    return e


class TestPatterns(unittest.TestCase):
    def test_my_awards(self):
        for a in ["FRGS/1/2025/TK09/USM/02/4", "USIM/FRGS-FST-5-50311",
                  "LRGS 2018-1.", "R.J130000.7845.4L669",
                  "Q.J130000.3551.07G53", "frgs/1/2019/stg05/ump/02/8"]:
            self.assertTrue(m.is_my_award(a), a)
        for a in ["ANR-15-CE-17-0019-01", "1894/2015", "S/15/2018",
                  "MOE-114-TPRSK-1029-012Y1", "IP2011 049271", "",
                  "AR.J130000.7845.4"]:
            self.assertFalse(m.is_my_award(a), a)

    def test_my_names(self):
        for n in ["Universiti Teknologi Malaysia", "University of Malaya",
                  "Long-term Research Grant Scheme",
                  "Fundamental Research Grant Scheme",
                  "Ministry of Higher Education, Malaysia", "IIUM"]:
            self.assertTrue(m.is_my_name(n), n)
        for n in ["Universiti Brunei Darussalam", "Himalaya Foundation",
                  "Deutsche Forschungsgemeinschaft",
                  "Ministry of Higher Education", None]:
            self.assertFalse(m.is_my_name(n), n)

    def test_eg_names(self):
        for n in ["Egypt-Japan University of Science and Technology",
                  "DAAD Kairo", "E-JUST", "Newton-Mosharafa",
                  "Egyptian Ministry of Higher Education",
                  "Science and Technology Development Fund"]:
            self.assertTrue(m.is_eg_name(n), n)
        self.assertFalse(m.is_eg_name(
            "Science and Technology Development Fund", macau=True))
        for n in ["Alexander von Humboldt-Stiftung",
                  "Special Research Fund of Ghent University",
                  "Ministry of Higher Education", "Adjustment Fund"]:
            self.assertFalse(m.is_eg_name(n), n)


class TestClassify(unittest.TestCase):
    def test_award_my(self):
        r = m.classify_work(work("10.1021/acsomega.6c06914",
                                 [eg(award=["FRGS/1/2025/TK09/USM/02/4"])]))
        self.assertEqual(r["verdict"], "MY")
        self.assertEqual(r["award_my"], 1)
        self.assertEqual(r["name_my"], 0)
        self.assertEqual(r["asserted_by"], "publisher")

    def test_name_eg(self):
        r = m.classify_work(work("10.1016/j.cie.2021.107300",
                                 [eg("Egypt Ministry of Higher Education")]))
        self.assertEqual(r["verdict"], "EG")
        self.assertEqual(r["name_eg"], 1)

    def test_none(self):
        r = m.classify_work(work("10.1/x", [eg()]))
        self.assertEqual(r["verdict"], "NONE")
        self.assertEqual(r["n_target"], 1)

    def test_both(self):
        r = m.classify_work(work("10.1/y", [
            eg(), {"name": "Egypt-Japan University of Science and Technology"},
            {"name": "Universiti Malaya"}]))
        self.assertEqual(r["verdict"], "BOTH")
        self.assertEqual((r["cof_my"], r["cof_eg"]), (1, 1))

    def test_malaysia_id_cofunder(self):
        r = m.classify_work(work("10.1/z", [
            eg(), {"DOI": MY, "name": "Ministry of Higher Education"}]))
        self.assertEqual(r["verdict"], "MY")
        self.assertEqual(r["cof_my"], 1)

    def test_award_on_entry_without_id(self):
        r = m.classify_work(work("10.1/w", [
            eg(), {"name": "MoHE", "award": ["FRGS/1/2023/SKK06/UITM/02/7"]}]))
        self.assertEqual(r["verdict"], "MY")
        self.assertEqual(r["award_my"], 0)
        self.assertEqual(r["cof_my"], 1)

    def test_name_strict(self):
        r = m.classify_work(work("10.1109/icocet63343.2024.10730485", [
            eg("Ministry of Higher Education of Malaysia (MOHE)",
               award=["LRGS/1/2020/UM/01/5/4 (9012-00010)"])]))
        self.assertEqual(r["verdict"], "MY")
        self.assertEqual((r["name_my_strict"], r["name_my"], r["award_my"]),
                         (1, 1, 1))

    def test_macau_stdf_not_egypt(self):
        r = m.classify_work(work("10.1/m", [
            eg(), {"name": "Science and Technology Development Fund"},
            {"name": "Macau University of Science and Technology"}]))
        self.assertEqual(r["verdict"], "NONE")

    def test_doi_case_and_no_target(self):
        e = eg()
        e["DOI"] = "10.13039/501100002385".upper()
        r = m.classify_work(work("10.1/c", [e]))
        self.assertEqual(r["n_target"], 1)
        r2 = m.classify_work(work("10.1/d", [{"DOI": MY, "name": "x"}]))
        self.assertEqual(r2["n_target"], 0)
        self.assertEqual(r2["verdict"], "MY")


def fake_pages():
    pages = [
        {"message": {"total-results": 3, "next-cursor": "c2", "items": [
            work("10.1021/acsomega.6c06914",
                 [eg(award=["FRGS/1/2025/TK09/USM/02/4"])],
                 created="2026-10-07"),
            work("10.1016/j.cie.2021.107300",
                 [eg("Egypt Ministry of Higher Education")])]}},
        {"message": {"total-results": 3, "next-cursor": "c3", "items": [
            work("10.1016/j.cie.2021.107300",
                 [eg("Egypt Ministry of Higher Education")]),
            work("10.1/none", [eg()], publisher="IEEE")]}},
        {"message": {"total-results": 3, "next-cursor": "c4", "items": []}},
    ]
    calls = []

    def fetch(url):
        calls.append(url)
        return pages[len(calls) - 1]
    return fetch, calls


class TestScanAndMain(unittest.TestCase):
    def test_scan_dedupes_and_follows_cursor(self):
        fetch, calls = fake_pages()
        got = list(m.scan(EG, fetch=fetch, pause=0))
        self.assertEqual(len(got), 3)
        self.assertEqual(len(calls), 3)
        self.assertIn("cursor=%2A", calls[0])
        self.assertIn("cursor=c2", calls[1])
        self.assertIn("funder%3A10.13039%2F501100002385", calls[0])

    def test_max_pages(self):
        fetch, calls = fake_pages()
        got = list(m.scan(EG, fetch=fetch, pause=0, max_pages=1))
        self.assertEqual(len(got), 2)
        self.assertEqual(len(calls), 1)

    def test_main_writes_outputs(self):
        fetch, _ = fake_pages()
        with tempfile.TemporaryDirectory() as d:
            s = m.main(["--out-dir", d, "--pause", "0"], fetch=fetch)
            self.assertTrue(os.path.exists(os.path.join(d, "mohe-works.csv")))
            with open(os.path.join(d, "summary.json"), encoding="utf-8") as f:
                s2 = json.load(f)
        self.assertEqual(s2["works_scanned"], 3)
        self.assertEqual(s["verdict"], {"MY": 1, "EG": 1, "NONE": 1})
        self.assertEqual(s["tiers"]["award_my"], 1)
        self.assertEqual(s["my_created_2026"], 1)
        self.assertEqual(s["my_asserted_by"], {"publisher": 1})
        self.assertTrue(s["sanity"]["10.1021/acsomega.6c06914"]["ok"])
        self.assertTrue(s["sanity"]["10.1016/j.cie.2021.107300"]["ok"])
        self.assertIsNone(
            s["sanity"]["10.1109/icocet63343.2024.10730485"]["found"])


if __name__ == "__main__":
    unittest.main()
