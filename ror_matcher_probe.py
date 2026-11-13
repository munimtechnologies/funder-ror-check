#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. Made with AI agents working in the name of MV2,
# Munim, Inc. (mv2@munimtech.com).
"""ror_matcher_probe: which record does ROR's affiliation matcher pick for each
Chinese provincial science department?

For every province it sends common English forms of the department's name to
https://api.ror.org/v2/organizations?affiliation=... and reports the record the
matcher marks "chosen", whether that is the province's own department, and at
what rank the province's own record appears (0 = not in the results).

Crossref's funder matcher (live since 15 September 2026) is described as ROR's
"single search" strategy, so a wrong pick here is a lead for wrong funder ROR
IDs in Crossref metadata. See FINDINGS-FUNDER-ROR-2.md.

Output: CSV on stdout; a one-line count on stderr. Exit code 1 if any pick is
"wrong", else 0.
"""
import argparse
import csv
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = "0.2.0"
MAILTO = "mv2@munimtech.com"
UA = "ror-matcher-probe/%s (MV2, Munim, Inc.; mailto:%s)" % (VERSION, MAILTO)
ROR_API = "https://api.ror.org/v2/organizations"

# Province -> ROR ID of its provincial science and technology department, as
# found with a ROR search (country CN, type funder) on 2026-11-13. The four
# municipalities (Beijing, Shanghai, Tianjin, Chongqing) use "commission" names
# and are left out; no Tibet department record was found.
DEPARTMENTS = {
    "Anhui": "01e70gy59",
    "Fujian": "00rgzpv08",
    "Gansu": "03xz2hx98",
    "Guangdong": "00tjzgn92",
    "Guangxi": "00dhpdx54",
    "Guizhou": "00kwnh405",
    "Hainan": "03rbw2w25",
    "Hebei": "05a7g7f24",
    "Heilongjiang": "031tatj48",
    "Henan": "058p20n09",
    "Hubei": "00tbh0t11",
    "Hunan": "04qgr7x96",
    "Inner Mongolia": "02v4g3v80",
    "Jiangsu": "02mkqta53",
    "Jiangxi": "00t30yz20",
    "Jilin": "049x38272",
    "Liaoning": "02f09cx53",
    "Ningxia": "040ebrp24",
    "Qinghai": "03vz7b375",
    "Shaanxi": "01c2sx728",
    "Shandong": "01b9fvd84",
    "Shanxi": "05vp4an32",
    "Sichuan": "04323m874",
    "Xinjiang": "02vtvez67",
    "Yunnan": "03whqdf70",
    "Zhejiang": "05yj3y977",
}

TEMPLATES = (
    "{p} Science and Technology Department",
    "{p} Provincial Department of Science and Technology",
    "Department of Science and Technology of {p} Province",
)

FIELDS = ["province", "own_ror", "query", "verdict", "chosen_ror", "chosen_name",
          "chosen_score", "own_rank", "top_ror", "top_score"]

ID_RE = re.compile(r"(0[0-9a-z]{8})$")


def affiliation_url(name):
    return "%s?affiliation=%s" % (ROR_API, urllib.parse.quote(name))


def org_id(org):
    """'https://ror.org/05vp4an32' -> '05vp4an32'; '' if it does not look like one."""
    m = ID_RE.search((org.get("id") or "").strip().lower())
    return m.group(1) if m else ""


def display_name(org):
    names = [n for n in (org.get("names") or []) if isinstance(n, dict)]
    for n in names:
        if "ror_display" in (n.get("types") or []):
            return n.get("value") or ""
    return (names[0].get("value") or "") if names else ""


def parse_result(data, own):
    """Summarise one affiliation response for a province whose own record is `own`."""
    items = (data or {}).get("items") or []
    row = {"verdict": "none", "chosen_ror": "", "chosen_name": "", "chosen_score": "",
           "own_rank": 0, "top_ror": "", "top_score": ""}
    for i, it in enumerate(items):
        org = it.get("organization") or {}
        rid = org_id(org)
        if i == 0:
            row["top_ror"] = rid
            row["top_score"] = it.get("score", "")
        if rid and rid == own and not row["own_rank"]:
            row["own_rank"] = i + 1
        if it.get("chosen") is True and not row["chosen_ror"] and rid:
            row["chosen_ror"] = rid
            row["chosen_name"] = display_name(org)
            row["chosen_score"] = it.get("score", "")
    if row["chosen_ror"]:
        row["verdict"] = "right" if row["chosen_ror"] == own else "wrong"
    return row


def http_get(url, tries=5):
    """GET a JSON URL; retries on 429, 5xx and network errors."""
    delay = 2.0
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                   "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or i == tries - 1:
                raise
        except (urllib.error.URLError, OSError):
            if i == tries - 1:
                raise
        time.sleep(delay)
        delay *= 2
    return None


def probe(get, provinces, templates, pause=0.2):
    rows = []
    for p in provinces:
        own = DEPARTMENTS[p]
        for t in templates:
            q = t.replace("{p}", p)
            row = {"province": p, "own_ror": own, "query": q}
            try:
                row.update(parse_result(get(affiliation_url(q)), own))
            except Exception as ex:                      # keep going
                row.update(parse_result(None, own))
                row["verdict"] = "error"
                row["chosen_name"] = str(ex)[:200]
            rows.append(row)
            if pause:
                time.sleep(pause)
    return rows


def to_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, FIELDS, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def counts(rows):
    c = {}
    for r in rows:
        c[r["verdict"]] = c.get(r["verdict"], 0) + 1
    return c


def main(argv=None, get=None, out=None, err=None):
    out = out or sys.stdout
    err = err or sys.stderr
    ap = argparse.ArgumentParser(
        prog="ror_matcher_probe",
        description="Which ROR record does ROR's affiliation matcher pick for each "
                    "Chinese provincial science department?")
    ap.add_argument("--province", action="append", default=[],
                    help="only this province (repeatable); default all %d" % len(DEPARTMENTS))
    ap.add_argument("--template", action="append", default=[],
                    help="name form with {p} for the province (repeatable)")
    ap.add_argument("--pause", type=float, default=0.2, help="seconds between requests")
    ap.add_argument("--version", action="version", version="ror_matcher_probe " + VERSION)
    a = ap.parse_args(argv)
    provs = a.province or sorted(DEPARTMENTS)
    for x in provs:
        if x not in DEPARTMENTS:
            ap.error("unknown province: %s" % x)
    temps = a.template or list(TEMPLATES)
    for t in temps:
        if "{p}" not in t:
            ap.error("template must contain {p}: %s" % t)
    rows = probe(get or http_get, provs, temps, a.pause)
    out.write(to_csv(rows))
    c = counts(rows)
    err.write("%d queries; %s\n" % (len(rows), ", ".join(
        "%s %d" % (k, c[k]) for k in ("right", "wrong", "none", "error") if c.get(k))))
    return 1 if c.get("wrong") else 0


if __name__ == "__main__":
    sys.exit(main())
