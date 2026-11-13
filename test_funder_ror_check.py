# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. Made with AI agents working in MV2's name.
"""Offline tests for funder_ror_check (no network: HTTP is faked)."""
import io
import unittest

import funder_ror_check as frc


def ror(rid, display, cc, aliases=(), fundref=(), labels=()):
    names = [{"value": display, "types": ["ror_display", "label"], "lang": "en"}]
    names += [{"value": a, "types": ["alias"], "lang": "en"} for a in aliases]
    names += [{"value": v, "types": ["label"], "lang": "zh"} for v in labels]
    return {"id": "https://ror.org/" + rid, "status": "active", "names": names,
            "locations": [{"geonames_details": {"country_code": cc}}],
            "external_ids": [{"type": "fundref", "all": list(fundref),
                              "preferred": fundref[0] if fundref else None}]}


ANHUI = ror("01e70gy59", "Department of Science and Technology of Anhui Province", "CN",
            fundref=("501100010816", "501100017668", "501100018530"),
            labels=("安徽省科学技术厅",))
ANHUI["locations"][0]["geonames_details"]["country_subdivision_name"] = "Yunnan"
HUBEI = ror("00tbh0t11", "Science and Technology Department of Hubei Province", "CN",
            fundref=("501100010580", "501100018806"))
HAINAN = ror("03rbw2w25", "Department of Science and Technology of Hainan Province", "CN",
             aliases=("Hainan Provincial Department of Science and Technology",),
             fundref=("501100008111",))
AU_DOE = ror("03z942k20", "Department of Education", "AU",
             aliases=("Australian Department of Education",), fundref=("501100003521",))
PH_DOST = ror("05tgxx705", "Department of Science and Technology", "PH")
NSFC = ror("01h0zpd94", "National Natural Science Foundation of China", "CN",
           fundref=("501100001809",))


def rid_entry(rid, by, name=None, awards=None, doi=None):
    e = {"id": [{"id": "https://ror.org/" + rid, "id-type": "ROR", "asserted-by": by}]}
    if name is not None:
        e["name"] = name
    if awards is not None:
        e["award"] = list(awards)
    if doi:
        e["DOI"] = doi
        e["doi-asserted-by"] = "publisher"
        e["id"].append({"id": doi, "id-type": "DOI", "asserted-by": "publisher"})
    return e


HENAN_ENTRY = rid_entry("03rbw2w25", "crossref",
                        name="Henan Provincial Department of Science and Technology Research Project",
                        awards=["242102111013"])
HUBEI_CONFLICT = rid_entry("01e70gy59", "crossref",
                           name="Department of Science and Technology of Hubei Province",
                           awards=["2024BCB073"], doi="10.13039/501100018806")


class FakeGet:
    def __init__(self, table):
        self.table = table
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        if url not in self.table:
            raise KeyError(url)
        return self.table[url]


def table(*records, extra=None):
    t = {frc.ror_url(frc.normalize_id(r["id"])): r for r in records}
    t.update(extra or {})
    return t


class TestHelpers(unittest.TestCase):
    def test_normalize_id(self):
        self.assertEqual(frc.normalize_id("https://ror.org/01E70GY59"), "01e70gy59")
        self.assertEqual(frc.normalize_id(" 03rbw2w25 "), "03rbw2w25")
        self.assertEqual(frc.normalize_id("10.13039/501100018806"), "")
        self.assertEqual(frc.normalize_id(""), "")

    def test_places_province(self):
        self.assertEqual(
            frc.places("Henan Provincial Department of Science and Technology"),
            ({"henan"}, {"CN"}))

    def test_places_city_pair_and_spelling(self):
        self.assertEqual(frc.places("Shuguang Program of Wuhan Science and Technology Bureau")[0],
                         {"hubei"})
        self.assertEqual(frc.places("Inner Mongolia Natural Science Foundation")[0],
                         {"inner mongolia"})
        self.assertEqual(frc.places("Ganshu Province Guided Project")[0], {"gansu"})
        self.assertEqual(frc.places("South African Department of Science and Technology")[1],
                         {"ZA"})

    def test_places_shanxi_shaanxi_hunan_henan_hainan_distinct(self):
        self.assertEqual(frc.places("Shanxi and Shaanxi")[0], {"shanxi", "shaanxi"})
        self.assertEqual(frc.places("Hunan Henan Hainan Hubei Hebei")[0],
                         {"hunan", "henan", "hainan", "hubei", "hebei"})

    def test_places_none_for_generic(self):
        self.assertEqual(frc.places("Department of Education"), (set(), set()))
        self.assertEqual(frc.places("Department of Science and Technology"), (set(), set()))

    def test_places_sino_and_binational(self):
        self.assertEqual(frc.places("Sino-German Center")[1], {"CN", "DE"})
        self.assertEqual(frc.places("German–Israeli Foundation")[1], {"DE", "IL"})

    def test_parse_ror_uses_names_not_geocode(self):
        rec = frc.parse_ror(ANHUI)
        self.assertEqual(rec["id"], "01e70gy59")
        self.assertEqual(rec["name"], "Department of Science and Technology of Anhui Province")
        self.assertEqual(rec["provinces"], {"anhui"})
        self.assertEqual(rec["countries"], {"CN"})
        self.assertIn("501100017668", rec["fundref"])

    def test_entry_info(self):
        e = frc.entry_info(HUBEI_CONFLICT)
        self.assertEqual(e["rors"], [("01e70gy59", "crossref")])
        self.assertEqual(e["fdoi"], "501100018806")
        self.assertEqual(e["awards"], ("2024BCB073",))
        e2 = frc.entry_info({"award": ["b", " a ", ""], "id": [
            {"id": "10.13039/501100001809", "id-type": "DOI"}]})
        self.assertEqual(e2["awards"], ("a", "b"))
        self.assertEqual(e2["fdoi"], "501100001809")
        self.assertEqual(e2["rors"], [])

    def test_urls(self):
        self.assertEqual(frc.ror_url("01e70gy59"), "https://api.ror.org/v2/organizations/01e70gy59")
        self.assertIn("query.advanced=external_ids.all%3A501100018806",
                      frc.fundref_url("501100018806"))
        u = frc.list_url("03rbw2w25", member="1968", from_date="2026")
        self.assertIn("filter=ror-id%3Ahttps%3A%2F%2Fror.org%2F03rbw2w25%2Cmember%3A1968"
                      "%2Cfrom-pub-date%3A2026", u)
        self.assertIn("cursor=%2A", u)
        self.assertTrue(frc.work_url("10.1016/j.x.1").startswith(
            "https://api.crossref.org/works/10.1016/j.x.1?mailto="))


class TestJudging(unittest.TestCase):
    def check(self, funders, tab, only=None):
        get = FakeGet(tab)
        ck = frc.Checker(get=get, pause=0)
        return ck.check_work("10.1/t", funders, only=only), get

    def test_doi_ror_conflict(self):
        tab = table(ANHUI, extra={frc.fundref_url("501100018806"): {"items": [HUBEI]}})
        rows, _ = self.check([HUBEI_CONFLICT], tab)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["verdict"], "doi-ror-conflict")
        self.assertIn("00tbh0t11", rows[0]["detail"])
        self.assertEqual(rows[0]["funder_doi"], "10.13039/501100018806")
        self.assertEqual(rows[0]["asserted_by"], "crossref")

    def test_province_mismatch_henan_hainan(self):
        rows, _ = self.check([HENAN_ENTRY], table(HAINAN))
        self.assertEqual(rows[0]["verdict"], "province-mismatch")
        self.assertIn("henan", rows[0]["detail"])
        self.assertIn("hainan", rows[0]["detail"])
        self.assertEqual(rows[0]["name_source"], "entry")
        self.assertEqual(rows[0]["ror_country"], "CN")

    def test_same_province_ok(self):
        e = rid_entry("00tbh0t11", "crossref",
                      name="Department of Science and Technology of Hubei Province")
        rows, _ = self.check([e], table(HUBEI))
        self.assertEqual(rows[0]["verdict"], "ok")

    def test_country_mismatch_via_award_pair(self):
        funders = [{"name": "Department of Education of the Zhejiang Province",
                    "award": ["Y202559181"]},
                   rid_entry("03z942k20", "publisher", awards=["Y202559181"])]
        rows, _ = self.check(funders, table(AU_DOE))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["entry"], 1)
        self.assertEqual(rows[0]["name_source"], "award-pair")
        self.assertEqual(rows[0]["funder_name"], "Department of Education of the Zhejiang Province")
        self.assertEqual(rows[0]["verdict"], "country-mismatch")
        self.assertIn("AU", rows[0]["detail"])

    def test_ok_when_paired_doi_listed(self):
        funders = [{"name": "National Natural Science Foundation of China", "award": ["52033011"],
                    "DOI": "10.13039/501100001809"},
                   rid_entry("01h0zpd94", "publisher", awards=["52033011"])]
        rows, get = self.check(funders, table(NSFC))
        self.assertEqual(rows[0]["verdict"], "ok")
        self.assertEqual(rows[0]["funder_doi"], "10.13039/501100001809")
        self.assertEqual(len(get.calls), 1)          # no FundRef owner query needed

    def test_generic_name_unchecked(self):
        funders = [{"name": "Department of Science and Technology", "award": ["11233"]},
                   rid_entry("05tgxx705", "publisher", awards=["11233"])]
        rows, _ = self.check(funders, table(PH_DOST))
        self.assertEqual(rows[0]["verdict"], "unchecked")

    def test_unpaired(self):
        rows, _ = self.check([rid_entry("05tgxx705", "publisher", awards=[])], table(PH_DOST))
        self.assertEqual(rows[0]["verdict"], "unpaired")
        funders = [{"name": "A Foundation", "award": ["1"]}, {"name": "B Council", "award": ["1"]},
                   rid_entry("05tgxx705", "publisher", awards=["1"])]
        rows, _ = self.check(funders, table(PH_DOST))
        self.assertEqual(rows[0]["verdict"], "unpaired")

    def test_ror_not_found_is_error(self):
        e = rid_entry("0abcdef12", "publisher", name="Hubei Foundation")
        rows, _ = self.check([e], {frc.ror_url("0abcdef12"): None})
        self.assertEqual(rows[0]["verdict"], "error")

    def test_only_filter(self):
        funders = [HENAN_ENTRY, rid_entry("01h0zpd94", "crossref",
                                          name="National Natural Science Foundation of China")]
        rows, get = self.check(funders, table(HAINAN), only={"03rbw2w25"})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["ror_id"], "03rbw2w25")

    def test_fundref_owner_cache(self):
        tab = table(ANHUI, extra={frc.fundref_url("501100018806"): {"items": [HUBEI]}})
        rows, get = self.check([HUBEI_CONFLICT, HUBEI_CONFLICT], tab)
        self.assertEqual([r["verdict"] for r in rows], ["doi-ror-conflict"] * 2)
        self.assertEqual(len(get.calls), 2)          # one ROR record, one owner query


class TestScanAndMain(unittest.TestCase):
    def test_check_doi(self):
        doi = "10.1016/j.mseb.2026.119859"
        tab = table(ANHUI, extra={
            frc.work_url(doi): {"message": {"DOI": doi, "funder": [HUBEI_CONFLICT]}},
            frc.fundref_url("501100018806"): {"items": [HUBEI]}})
        rows = frc.Checker(get=FakeGet(tab), pause=0).check_doi(doi)
        self.assertEqual(rows[0]["doi"], doi)
        self.assertEqual(rows[0]["verdict"], "doi-ror-conflict")

    def test_check_doi_missing(self):
        rows = frc.Checker(get=FakeGet({frc.work_url("10.9/none"): None}),
                           pause=0).check_doi("10.9/none")
        self.assertEqual(rows[0]["verdict"], "error")

    def scan_table(self):
        page = {"message": {"total-results": 2, "next-cursor": "abc", "items": [
            {"DOI": "10.1/a", "funder": [HENAN_ENTRY]},
            {"DOI": "10.1/b", "funder": [
                rid_entry("03rbw2w25", "crossref",
                          name="Hainan Provincial Department of Science and Technology"),
                rid_entry("01h0zpd94", "crossref",
                          name="National Natural Science Foundation of China")]}]}}
        return table(HAINAN, extra={frc.list_url("03rbw2w25"): page})

    def test_scan_ror(self):
        rows, n = frc.Checker(get=FakeGet(self.scan_table()), pause=0).scan_ror("03rbw2w25")
        self.assertEqual(n, 2)
        self.assertEqual([r["verdict"] for r in rows], ["province-mismatch", "ok"])

    def test_scan_limit(self):
        rows, n = frc.Checker(get=FakeGet(self.scan_table()), pause=0).scan_ror(
            "03rbw2w25", limit=1)
        self.assertEqual(n, 1)
        self.assertEqual(len(rows), 1)

    def test_main_csv_and_exit(self):
        doi = "10.1016/x"
        tab = table(HAINAN, extra={
            frc.work_url(doi): {"message": {"DOI": doi, "funder": [HENAN_ENTRY]}}})
        out = io.StringIO()
        code = frc.main(["--pause", "0", "--csv", doi], get=FakeGet(tab), out=out)
        self.assertEqual(code, 1)
        lines = out.getvalue().splitlines()
        self.assertEqual(lines[0], ",".join(frc.FIELDS))
        self.assertIn("province-mismatch", lines[1])

    def test_main_text(self):
        doi = "https://doi.org/10.1016/x"
        tab = table(HAINAN, extra={
            frc.work_url("10.1016/x"): {"message": {"DOI": "10.1016/x",
                                                    "funder": [HENAN_ENTRY]}}})
        out = io.StringIO()
        frc.main(["--pause", "0", doi], get=FakeGet(tab), out=out)
        text = out.getvalue()
        self.assertIn("PROVINCE-MISMATCH", text)
        self.assertIn("1 works; 1 funder ROR IDs; province-mismatch 1", text)

    def test_main_ror_scan(self):
        out = io.StringIO()
        code = frc.main(["--pause", "0", "--ror", "https://ror.org/03rbw2w25"],
                        get=FakeGet(self.scan_table()), out=out)
        self.assertEqual(code, 1)
        self.assertIn("2 works; 2 funder ROR IDs; province-mismatch 1; ok 1", out.getvalue())

    def test_main_not_a_doi(self):
        out = io.StringIO()
        self.assertEqual(frc.main(["--pause", "0", "notadoi"], get=FakeGet({}), out=out), 2)

    def test_exit_codes(self):
        self.assertEqual(frc.exit_code([]), 0)
        self.assertEqual(frc.exit_code([{"verdict": "error"}]), 2)
        self.assertEqual(frc.exit_code([{"verdict": "error"}, {"verdict": "country-mismatch"}]), 1)
        self.assertEqual(frc.exit_code([{"verdict": "ok"}, {"verdict": "unchecked"}]), 0)


if __name__ == "__main__":
    unittest.main()
