# SPDX-License-Identifier: Apache-2.0
# Tests for mohesr_census.py (no network). Made with AI agents working in
# the name of MV2, Munim, Inc.
import json
import os
import tempfile
import unittest

import mohesr_census as m

AE = "10.13039/100009122"
NRF_KR = "10.13039/501100003725"
UAEU = "10.13039/501100006013"


def work(doi, entries, publisher="Wiley", created="2024-01-02"):
    return {"DOI": doi, "publisher": publisher,
            "created": {"date-time": created + "T00:00:00Z"},
            "funder": entries}


def ae(name="Ministry of Higher Education and Scientific Research",
       award=None, by="publisher"):
    e = {"DOI": AE, "name": name, "doi-asserted-by": by}
    if award is not None:
        e["award"] = award
    return e


class TestAwardFormats(unittest.TestCase):
    def check(self, cases):
        for award, want in cases:
            self.assertEqual(m.award_countries(award), want, award)

    def test_korea(self):
        self.check([
            ("2021R1I1A3052320", {"KR"}),
            ("RS-2023-00241749", {"KR"}),
            ("RS-2021-NR060087", {"KR"}),
            ("RS-2025-25398164", {"KR"}),
            ("NRF-2015H1A2A1034022", {"KR"}),
            ("2022R1 A6 C101 A751", {"KR"}),
            ("2020R1A6A3-A01099283", {"KR"}),
            ("NRF–2020R1I1A1A01065877", {"KR"}),
            ("2020R1I1A1A01065541, RS-2023-00273372", {"KR"}),
        ])

    def test_not_korea(self):
        self.check([
            ("2021A1515012447", set()),
            ("2023M733566", set()),
            ("2024ZD007", set()),
            ("2020AAA0108800", set()),
            ("JP21H02847", {"JP"}),
            ("G00003563", set()),
            ("2023003660001", set()),
            ("IFP22UQU4331237DSR236", set()),
            ("MOE-111-YSFMS-0008-001-P1", set()),
            ("PID2020-119620RB-I00", set()),
            ("", set()),
        ])

    def test_singapore(self):
        self.check([
            ("MOE-T2EP30122-0005", {"SG"}),
            ("T2EP30121-0015", {"SG"}),
            ("MOE2018-T2-2-161,SRG ISTD 2017 129", {"SG"}),
            ("2019-T1-001-126", {"SG"}),
            ("2023T160501", set()),
            ("MOE 106N506CE1", set()),
        ])

    def test_others(self):
        self.check([
            ("FRGS/1/2021/TK0/UKM/02/9", {"MY"}),
            ("R.J130000.7851.5F123", {"MY"}),
            ("NCET-05-0680", {"CN"}),
            ("NCET-05–0680", {"CN"}),
            ("IRT_17R86", {"CN"}),
            ("17YJC630041", {"CN"}),
            ("20XJC910001", {"CN"}),
            ("B00L01UN400120210002 (PRFU)", {"DZ"}),
            ("B00L02UN130120180004", {"DZ"}),
            ("LR11IP03", {"TN"}),
            ("LR15CBS06_2015-2018", {"TN"}),
            ("LR16IPT05", {"TN"}),
            ("LR22F030003", set()),
            ("MoE/STARS-1/293", {"IN"}),
            ("STARS-2/2023-0186", {"IN"}),
            ("CZ.02.01.01/00/22_008/0004575", {"CZ"}),
            ("OPVVV/0000759", {"CZ"}),
        ])


class TestNames(unittest.TestCase):
    def test_names(self):
        cases = [
            ("Singapore Ministry of Education (MOE)", {"SG"}),
            ("United Arab Emirates Ministry of Higher Education and "
             "Scientific Research", {"AE"}),
            ("UAE Ministry of Education", {"AE"}),
            ("Korea Ministry of Environment", {"KR"}),
            ("Ministry of Education, Republic of China (Taiwan)", {"TW"}),
            ("National Natural Science Foundation of China", {"CN"}),
            ("Tunisian Ministry of Higher Education and Scientific Research",
             {"TN"}),
            ("Iraqi Ministry of Higher Education and Scientific Research",
             {"IQ"}),
            ("Direction Générale de la Recherche Scientifique et du "
             "Développement Technologique", {"DZ"}),
            ("Universiti Brunei Darussalam", set()),
            ("Ministry of Higher Education and Scientific Research", set()),
            ("Ministry of Education", set()),
            ("Himalaya Foundation", set()),
            (None, set()),
        ]
        for name, want in cases:
            self.assertEqual(m.name_countries(name), want, name)


class TestClassify(unittest.TestCase):
    def test_korean_award_on_uae_entry(self):
        r = m.classify_work(work("10.1002/celc.202200093", [
            ae(award=["2021R1I1A3052320"]), ae(),
            {"DOI": NRF_KR, "name": "National Research Foundation of Korea",
             "doi-asserted-by": "publisher"}]))
        self.assertEqual(r["verdict"], "FOREIGN")
        self.assertEqual(r["award_countries"], "KR")
        self.assertEqual(r["cof_countries"], "KR")
        self.assertEqual(r["n_target"], 2)
        self.assertEqual(r["named_moe"], 0)
        self.assertEqual(r["asserted_by"], "publisher")

    def test_named_moe(self):
        r = m.classify_work(work("10.1128/aem.00286-26", [
            ae("Ministry of Education",
               ["2020R1I1A1A01065541, RS-2023-00273372"])]))
        self.assertEqual(r["verdict"], "FOREIGN")
        self.assertEqual(r["named_moe"], 1)
        r2 = m.classify_work(work("10.1/moe", [ae("  MOE ")]))
        self.assertEqual(r2["named_moe"], 1)
        self.assertEqual(r2["verdict"], "NONE")

    def test_uae(self):
        r = m.classify_work(work("10.1016/j.ultsonch.2024.107015", [
            {"DOI": UAEU, "name": "United Arab Emirates University"},
            ae(award=["G00003563"])]))
        self.assertEqual(r["verdict"], "AE")
        self.assertEqual(r["cof_countries"], "AE")

    def test_both(self):
        r = m.classify_work(work("10.1/b", [
            ae("UAE Ministry of Education", ["RS-2024-00445180"])]))
        self.assertEqual(r["verdict"], "BOTH")
        self.assertEqual(r["name_countries"], "AE")
        self.assertEqual(r["award_countries"], "KR")

    def test_cofunder_id_only(self):
        r = m.classify_work(work("10.1/i", [
            ae(), {"DOI": "10.13039/501100007335",
                   "name": "Ministry of Higher Education and Scientific "
                           "Research"}]))
        self.assertEqual(r["verdict"], "FOREIGN")
        self.assertEqual(r["cof_countries"], "IQ")

    def test_award_on_other_entry_ignored(self):
        r = m.classify_work(work("10.1/o", [
            ae(), {"name": "Basic Science Research Program",
                   "award": ["2020R1A6A1A03043026"]}]))
        self.assertEqual(r["verdict"], "NONE")

    def test_doi_case_and_no_target(self):
        e = ae()
        e["DOI"] = AE.upper()
        r = m.classify_work(work("10.1/c", [e]))
        self.assertEqual(r["n_target"], 1)
        r2 = m.classify_work(work("10.1/d", [{"DOI": NRF_KR, "name": "x"}]))
        self.assertEqual(r2["n_target"], 0)
        self.assertEqual(r2["verdict"], "FOREIGN")


def fake_pages():
    pages = [
        {"message": {"total-results": 3, "next-cursor": "c2", "items": [
            work("10.1002/celc.202200093", [ae(award=["2021R1I1A3052320"])],
                 created="2026-03-01"),
            work("10.1016/j.compind.2024.104225", [
                ae("United Arab Emirates Ministry of Higher Education and "
                   "Scientific Research")], publisher="Elsevier BV")]}},
        {"message": {"total-results": 3, "next-cursor": "c3", "items": [
            work("10.1016/j.compind.2024.104225", [
                ae("United Arab Emirates Ministry of Higher Education and "
                   "Scientific Research")], publisher="Elsevier BV"),
            work("10.1/none", [ae("Ministry of Education")],
                 publisher="IEEE")]}},
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
        got = list(m.scan(AE, fetch=fetch, pause=0))
        self.assertEqual(len(got), 3)
        self.assertEqual(len(calls), 3)
        self.assertIn("cursor=%2A", calls[0])
        self.assertIn("cursor=c2", calls[1])
        self.assertIn("funder%3A10.13039%2F100009122", calls[0])

    def test_max_pages(self):
        fetch, calls = fake_pages()
        got = list(m.scan(AE, fetch=fetch, pause=0, max_pages=1))
        self.assertEqual(len(got), 2)
        self.assertEqual(len(calls), 1)

    def test_main_writes_outputs(self):
        fetch, _ = fake_pages()
        with tempfile.TemporaryDirectory() as d:
            s = m.main(["--out-dir", d, "--pause", "0"], fetch=fetch)
            self.assertTrue(
                os.path.exists(os.path.join(d, "mohesr-works.csv")))
            with open(os.path.join(d, "summary.json"), encoding="utf-8") as f:
                s2 = json.load(f)
        self.assertEqual(s2["works_scanned"], 3)
        self.assertEqual(s["verdict"], {"FOREIGN": 1, "AE": 1, "NONE": 1})
        self.assertEqual(s["award_country"], {"KR": 1})
        self.assertEqual(s["any_country"], {"KR": 1, "AE": 1})
        self.assertEqual(s["named_moe"], 1)
        self.assertEqual(s["named_moe_verdict"], {"NONE": 1})
        self.assertEqual(s["foreign_created_2026"], 1)
        self.assertEqual(s["foreign_asserted_by"], {"publisher": 1})
        self.assertEqual(s["foreign_by_publisher"], {"Wiley": 1})
        self.assertTrue(s["sanity"]["10.1002/celc.202200093"]["ok"])
        self.assertTrue(s["sanity"]["10.1016/j.compind.2024.104225"]["ok"])
        self.assertIsNone(
            s["sanity"]["10.1109/cvpr52733.2024.00944"]["found"])


if __name__ == "__main__":
    unittest.main()
