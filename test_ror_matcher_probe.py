# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. Made with AI agents working in the name of MV2, Munim, Inc.
"""Offline tests for ror_matcher_probe (HTTP is faked)."""
import csv
import io
import re
import unittest

import ror_matcher_probe as rmp


def org(rid, name):
    return {"id": "https://ror.org/" + rid,
            "names": [{"value": name + " (label)", "types": ["label"]},
                      {"value": name, "types": ["ror_display", "label"]}]}


# Real shapes, 2026-11-13: Qinghai's form picks Shanxi's record (05vp4an32).
QINGHAI = {"number_of_results": 3, "items": [
    {"score": 0.96, "chosen": True, "matching_type": "SINGLE SEARCH",
     "organization": org("05vp4an32", "Shanxi Science and Technology Department")},
    {"score": 0.95, "chosen": False,
     "organization": org("01c2sx728", "Shaanxi Science and Technology Department")},
    {"score": 0.89, "chosen": False,
     "organization": org("040ebrp24", "Science and Technology Department of Ningxia")},
]}
HEBEI = {"items": [
    {"score": 1.0, "chosen": True,
     "organization": org("05a7g7f24", "Hebei Provincial Department of Science and Technology")},
    {"score": 0.95, "chosen": False,
     "organization": org("05vp4an32", "Shanxi Science and Technology Department")},
]}
NINGXIA_NONE = {"items": [
    {"score": 0.96, "chosen": False,
     "organization": org("00dhpdx54", "Guangxi Science and Technology Department")},
    {"score": 0.89, "chosen": False,
     "organization": org("040ebrp24", "Science and Technology Department of Ningxia")},
]}

T1 = "{p} Science and Technology Department"


class Fake:
    def __init__(self, table):
        self.table = table
        self.calls = []

    def get(self, url):
        self.calls.append(url)
        return self.table[url]          # KeyError for an unexpected URL


class TestParts(unittest.TestCase):
    def test_affiliation_url(self):
        self.assertEqual(
            rmp.affiliation_url("Qinghai Science and Technology Department"),
            "https://api.ror.org/v2/organizations?affiliation="
            "Qinghai%20Science%20and%20Technology%20Department")

    def test_org_id(self):
        self.assertEqual(rmp.org_id({"id": "https://ror.org/05VP4AN32"}), "05vp4an32")
        self.assertEqual(rmp.org_id({"id": "not an id"}), "")
        self.assertEqual(rmp.org_id({}), "")

    def test_display_name_prefers_ror_display(self):
        self.assertEqual(rmp.display_name(org("05vp4an32", "Shanxi X")), "Shanxi X")
        self.assertEqual(rmp.display_name({"names": [{"value": "Only", "types": []}]}), "Only")
        self.assertEqual(rmp.display_name({}), "")

    def test_departments(self):
        self.assertEqual(len(rmp.DEPARTMENTS), 26)
        self.assertEqual(len(set(rmp.DEPARTMENTS.values())), 26)
        for rid in rmp.DEPARTMENTS.values():
            self.assertTrue(re.fullmatch(r"0[0-9a-z]{8}", rid), rid)
        self.assertEqual(rmp.DEPARTMENTS["Jiangsu"], "02mkqta53")
        self.assertEqual(rmp.DEPARTMENTS["Jiangxi"], "00t30yz20")


class TestParse(unittest.TestCase):
    def test_wrong_pick(self):
        r = rmp.parse_result(QINGHAI, "03vz7b375")
        self.assertEqual(r["verdict"], "wrong")
        self.assertEqual(r["chosen_ror"], "05vp4an32")
        self.assertEqual(r["chosen_name"], "Shanxi Science and Technology Department")
        self.assertEqual(r["chosen_score"], 0.96)
        self.assertEqual(r["own_rank"], 0)
        self.assertEqual(r["top_ror"], "05vp4an32")

    def test_right_pick(self):
        r = rmp.parse_result(HEBEI, "05a7g7f24")
        self.assertEqual(r["verdict"], "right")
        self.assertEqual(r["own_rank"], 1)
        self.assertEqual(r["top_score"], 1.0)

    def test_no_pick_but_own_listed(self):
        r = rmp.parse_result(NINGXIA_NONE, "040ebrp24")
        self.assertEqual(r["verdict"], "none")
        self.assertEqual(r["chosen_ror"], "")
        self.assertEqual(r["own_rank"], 2)
        self.assertEqual(r["top_ror"], "00dhpdx54")

    def test_empty(self):
        for data in (None, {}, {"items": []}):
            r = rmp.parse_result(data, "040ebrp24")
            self.assertEqual(r["verdict"], "none")
            self.assertEqual(r["own_rank"], 0)
            self.assertEqual(r["top_score"], "")


class TestMain(unittest.TestCase):
    def table(self):
        return {
            rmp.affiliation_url("Qinghai Science and Technology Department"): QINGHAI,
            rmp.affiliation_url("Hebei Science and Technology Department"): HEBEI,
        }

    def test_csv_and_exit_code(self):
        fake = Fake(self.table())
        out, err = io.StringIO(), io.StringIO()
        code = rmp.main(["--province", "Qinghai", "--province", "Hebei",
                         "--template", T1, "--pause", "0"],
                        get=fake.get, out=out, err=err)
        self.assertEqual(code, 1)
        self.assertEqual(len(fake.calls), 2)
        rows = list(csv.DictReader(io.StringIO(out.getvalue())))
        self.assertEqual([r["province"] for r in rows], ["Qinghai", "Hebei"])
        self.assertEqual(rows[0]["verdict"], "wrong")
        self.assertEqual(rows[0]["chosen_ror"], "05vp4an32")
        self.assertEqual(rows[0]["own_ror"], "03vz7b375")
        self.assertEqual(rows[0]["query"], "Qinghai Science and Technology Department")
        self.assertEqual(rows[1]["verdict"], "right")
        self.assertEqual(rows[1]["own_rank"], "1")
        self.assertEqual(err.getvalue(), "2 queries; right 1, wrong 1\n")

    def test_all_right_exit_zero(self):
        fake = Fake(self.table())
        out, err = io.StringIO(), io.StringIO()
        code = rmp.main(["--province", "Hebei", "--template", T1, "--pause", "0"],
                        get=fake.get, out=out, err=err)
        self.assertEqual(code, 0)

    def test_lookup_error_row(self):
        fake = Fake({})                 # every lookup raises KeyError
        out, err = io.StringIO(), io.StringIO()
        code = rmp.main(["--province", "Ningxia", "--template", T1, "--pause", "0"],
                        get=fake.get, out=out, err=err)
        self.assertEqual(code, 0)
        rows = list(csv.DictReader(io.StringIO(out.getvalue())))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["verdict"], "error")
        self.assertEqual(err.getvalue(), "1 queries; error 1\n")

    def test_default_runs_every_province_and_template(self):
        calls = []

        def get(url):
            calls.append(url)
            return {"items": []}
        out, err = io.StringIO(), io.StringIO()
        code = rmp.main(["--pause", "0"], get=get, out=out, err=err)
        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 26 * 3)
        self.assertEqual(err.getvalue(), "78 queries; none 78\n")

    def test_bad_arguments(self):
        with self.assertRaises(SystemExit):
            rmp.main(["--province", "Atlantis"], get=lambda u: {}, out=io.StringIO(),
                     err=io.StringIO())
        with self.assertRaises(SystemExit):
            rmp.main(["--template", "no placeholder"], get=lambda u: {}, out=io.StringIO(),
                     err=io.StringIO())


if __name__ == "__main__":
    unittest.main()
