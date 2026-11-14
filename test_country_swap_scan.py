# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. Made with AI agents working in the name of MV2, Munim, Inc.
"""Offline tests for country_swap_scan (no network)."""
import unittest

import country_swap_scan as c


def ror(rid, by):
    return {"id": "https://ror.org/" + rid, "id-type": "ROR", "asserted-by": by}


class Countries(unittest.TestCase):
    def test_mainland_ministry(self):
        self.assertEqual(c.countries_in("Ministry of Science and Technology of China"), {"CN"})

    def test_prc_long_form_is_mainland(self):
        self.assertEqual(c.countries_in(
            "Ministry of Science and Technology of the People's Republic of China"), {"CN"})

    def test_republic_of_china_is_taiwan(self):
        self.assertEqual(c.countries_in("National Science Council of the Republic of China"), {"TW"})

    def test_roc_abbreviation_is_taiwan(self):
        self.assertEqual(c.countries_in("National Science and Technology Council, Taiwan, R.O.C."),
                         {"TW"})

    def test_province_is_mainland(self):
        self.assertEqual(c.countries_in("Department of Science and Technology of Guangdong Province"),
                         {"CN"})

    def test_no_country(self):
        self.assertEqual(c.countries_in("Department of Science and Technology"), set())

    def test_record_specific_own_pattern(self):
        self.assertEqual(c.countries_in("DOST-PCIEERD Grants-in-Aid", ["dost", "pcieerd"], "PH"),
                         {"PH"})

    def test_word_boundaries(self):
        # 'lao' must not match inside other words; 'india' not inside 'indiana'
        self.assertEqual(c.countries_in("Indiana University Bloomington Laboratory"), set())


class Classify(unittest.TestCase):
    def test_classes(self):
        self.assertEqual(c.classify(set(), "TW"), "unclear")
        self.assertEqual(c.classify({"TW"}, "TW"), "own")
        self.assertEqual(c.classify({"CN"}, "TW"), "foreign")
        self.assertEqual(c.classify({"CN", "TW"}, "TW"), "mixed")


class Pairing(unittest.TestCase):
    def test_unnamed_pairs_by_award(self):
        f = [{"name": "Department of Science and Technology of Xinjiang Uygur Autonomous Region",
              "award": ["2022TSYCCX0047"]},
             {"name": "Other", "award": ["X1"]},
             {"award": ["2022TSYCCX0047"], "id": [ror("05tgxx705", "publisher")]}]
        self.assertEqual(c.pair_name(f, 2),
                         ("Department of Science and Technology of Xinjiang Uygur Autonomous Region", 0))

    def test_unnamed_without_award_takes_previous(self):
        f = [{"name": "Special Project of Zhejiang Provincial Department of Science and Technology"},
             {"id": [ror("048kh7197", "publisher")]}]
        self.assertEqual(c.pair_name(f, 1)[1], 0)

    def test_unnamed_award_without_match(self):
        f = [{"name": "A", "award": ["1"]}, {"award": ["2"], "id": [ror("x", "publisher")]}]
        self.assertEqual(c.pair_name(f, 1), ("", ""))


class Rows(unittest.TestCase):
    def test_taiwan_record_on_mainland_name(self):
        w = {"DOI": "10.1126/SCIENCE.ABE1267", "publisher": "AAAS", "funder": [
            {"name": "the Ministry of Science and Technology of China", "award": ["2017YFA0700700"],
             "id": [ror("02kv4zf79", "crossref")]},
            {"name": "Ministry of Science and Technology, Taiwan", "id": [ror("02kv4zf79", "crossref")]},
            {"name": "National Natural Science Foundation of China",
             "id": [ror("01h0zpd94", "crossref")]}]}
        rows = c.rows_for_work(w, "02kv4zf79")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["klass"], "foreign")
        self.assertEqual(rows[0]["asserted_by"], "crossref")
        self.assertEqual(rows[0]["doi"], "10.1126/science.abe1267")
        self.assertEqual(rows[1]["klass"], "own")

    def test_mdpi_unnamed_south_africa(self):
        w = {"DOI": "10.3390/jcm15228829", "publisher": "MDPI AG", "funder": [
            {"name": "Science and Technology Department of Sichuan Province",
             "DOI": "10.13039/501100004829", "award": ["2026NSFSC1612"]},
            {"award": ["2026NSFSC1612"], "id": [ror("048kh7197", "publisher")]}]}
        rows = c.rows_for_work(w, "048kh7197")
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual((r["klass"], r["paired_from"], r["asserted_by"], r["countries"]),
                         ("foreign", 0, "publisher", "CN"))

    def test_bare_name_unclear(self):
        w = {"DOI": "10.3390/fib14110125", "funder": [
            {"name": "Department of Science and Technology"},
            {"id": [ror("05tgxx705", "publisher")]}]}
        self.assertEqual(c.rows_for_work(w, "05tgxx705")[0]["klass"], "unclear")


class Scan(unittest.TestCase):
    def test_two_pages(self):
        t = "02kv4zf79"
        w1 = {"DOI": "10.1/a", "funder": [{"name": "Chinese Ministry of Science and Technology",
                                           "id": [ror(t, "crossref")]}]}
        w2 = {"DOI": "10.1/b", "funder": [{"name": "NSTC Taiwan", "id": [ror(t, "crossref")]}]}
        w3 = {"DOI": "10.1/c", "funder": []}
        pages = {
            c.works_url(t, "*", 2): {"message": {"total-results": 3, "next-cursor": "c2",
                                                 "items": [w1, w2]}},
            c.works_url(t, "c2", 2): {"message": {"total-results": 3, "next-cursor": "c3",
                                                  "items": [w3]}},
        }
        rows, total, seen = c.scan(pages.__getitem__, t, rows=2, pause=0)
        self.assertEqual((total, seen, len(rows)), (3, 3, 2))
        self.assertEqual(c.summarise(rows)["foreign_dois"], 1)
        self.assertEqual(c.summarise(rows)["by_class_asserted"], {"foreign|crossref": 1,
                                                                  "own|crossref": 1})

    def test_url(self):
        u = c.works_url("02kv4zf79", "*", 1000)
        self.assertIn("filter=ror-id%3Ahttps%3A%2F%2Fror.org%2F02kv4zf79", u)
        self.assertIn("cursor=%2A", u)


if __name__ == "__main__":
    unittest.main()
