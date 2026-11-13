#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. Made with AI agents working in the name of MV2,
# Munim, Inc. (mv2@munimtech.com).
"""funder_ror_check: find funder ROR IDs in Crossref metadata that name the wrong funder.

Crossref funding metadata can identify a funder by ROR ID, deposited by the
publisher or (since 15 September 2026) added by Crossref's own name matcher.
Both can pick the wrong record: Crossref's matcher has given Hubei's and
Gansu's provincial science departments the ROR ID of Anhui's, and Henan's the
ROR ID of Hainan's; a publisher has deposited Australia's Department of
Education for Chinese provincial education departments. See
FINDINGS-FUNDER-ROR-1.md.

For every funder ROR ID in a work it runs three checks:

  * doi-ror-conflict: the same entry (or, for an unnamed entry holding only a
    ROR ID, the single named entry with the same award numbers) has a Funder
    Registry DOI (10.13039/...) that ROR lists on a different ROR record;
  * country-mismatch: the funder name names a country (or a Chinese province,
    which implies China) and the ROR record is located elsewhere;
  * province-mismatch: the funder name and the ROR record's own names name
    different Chinese provinces.

If the entry's funder DOI is listed on the ROR record itself, the pair is
"ok" and the name checks are skipped. "unchecked" means no check applied
(for example a bare "Department of Education"); "unpaired" means an unnamed
ROR entry could not be tied to one funder name.

Input: DOIs, or --ror <id> to scan every Crossref work carrying that ROR ID
(optionally --member and --from-pub-date). Exit code 1 if anything suspect is
found; 2 if a lookup failed and nothing suspect was found; else 0.
"""
import argparse
import csv
import io
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

VERSION = "0.1.0"
MAILTO = "mv2@munimtech.com"
UA = "funder-ror-check/%s (MV2, Munim, Inc.; mailto:%s)" % (VERSION, MAILTO)
ROR_API = "https://api.ror.org/v2/organizations"
CROSSREF = "https://api.crossref.org/works"

ROR_RE = re.compile(r"ror\.org/(0[0-9a-z]{8})(?![0-9a-z])", re.I)
BARE_RE = re.compile(r"0[0-9a-z]{8}")
FUNDREF_RE = re.compile(r"10\.13039/(\d+)")
DOI_RE = re.compile(r"^(?:https?://(?:dx\.)?doi\.org/|doi:)?(10\.\d{4,9}/\S+)$", re.I)

SUSPECT = ("doi-ror-conflict", "country-mismatch", "province-mismatch")
ORDER = SUSPECT + ("ok", "unchecked", "unpaired", "error")
FIELDS = ["doi", "entry", "funder_name", "name_source", "award", "funder_doi",
          "ror_id", "asserted_by", "ror_name", "ror_country", "verdict", "detail"]

# Chinese provincial-level divisions, a few spellings, and capitals / large
# cities that name only one province. Keys are lower-case words or word pairs.
PROVINCES = {}
for _p in ("anhui beijing chongqing fujian gansu guangdong guangxi guizhou hainan "
           "hebei heilongjiang henan hubei hunan jiangsu jiangxi jilin liaoning "
           "ningxia qinghai shaanxi shandong shanghai shanxi sichuan tianjin "
           "xinjiang xizang yunnan zhejiang").split():
    PROVINCES[_p] = _p
PROVINCES.update({
    "inner mongolia": "inner mongolia", "ganshu": "gansu", "tibet": "xizang",
    "hefei": "anhui", "wuhan": "hubei", "changsha": "hunan", "kunming": "yunnan",
    "lanzhou": "gansu", "zhengzhou": "henan", "haikou": "hainan", "sanya": "hainan",
    "chengdu": "sichuan", "hangzhou": "zhejiang", "ningbo": "zhejiang",
    "nanjing": "jiangsu", "guangzhou": "guangdong", "shenzhen": "guangdong",
    "qingdao": "shandong", "taiyuan": "shanxi", "harbin": "heilongjiang",
    "changchun": "jilin", "shenyang": "liaoning", "dalian": "liaoning",
    "guiyang": "guizhou", "nanning": "guangxi", "urumqi": "xinjiang",
    "lhasa": "xizang", "hohhot": "inner mongolia", "yinchuan": "ningxia",
    "xining": "qinghai", "nanchang": "jiangxi", "shijiazhuang": "hebei",
    "xiamen": "fujian",
})

# Country words (deliberately short list; ambiguous words such as "Georgia"
# are left out). Keys are lower-case words or word pairs.
COUNTRIES = {
    "china": "CN", "chinese": "CN", "prc": "CN", "sino": "CN",
    "korea": "KR", "korean": "KR", "south korea": "KR", "gyeongsangnam": "KR",
    "australia": "AU", "australian": "AU",
    "philippines": "PH", "philippine": "PH",
    "india": "IN", "indian": "IN",
    "singapore": "SG", "japan": "JP", "japanese": "JP",
    "spain": "ES", "spanish": "ES", "andalusia": "ES", "galicia": "ES",
    "galician": "ES", "basque": "ES", "catalonia": "ES",
    "south africa": "ZA", "south african": "ZA",
    "taiwan": "TW", "hong kong": "HK", "malaysia": "MY", "thailand": "TH",
    "vietnam": "VN", "pakistan": "PK", "indonesia": "ID", "iran": "IR",
    "turkey": "TR", "turkiye": "TR", "egypt": "EG", "brazil": "BR",
    "mexico": "MX", "canada": "CA", "canadian": "CA",
    "germany": "DE", "german": "DE", "france": "FR", "french": "FR",
    "italy": "IT", "italian": "IT", "poland": "PL", "polish": "PL",
    "israel": "IL", "israeli": "IL",
    "united kingdom": "GB", "uk": "GB", "british": "GB",
    "united states": "US", "usa": "US", "new zealand": "NZ",
}


# ------------------------------------------------------------------ helpers

def normalize_id(x):
    """'https://ror.org/01E70GY59' or '01e70gy59' -> '01e70gy59'; else ''."""
    x = (x or "").strip()
    m = ROR_RE.search(x)
    if m:
        return m.group(1).lower()
    return x.lower() if BARE_RE.fullmatch(x.lower()) else ""


def words(s):
    """Lower-case ASCII words of a string, accents removed."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z]+", s.lower())


def places(s):
    """(provinces, countries) named in a string; a province implies 'CN'."""
    w = words(s)
    grams = list(w) + ["%s %s" % (a, b) for a, b in zip(w, w[1:])]
    provs, ctys = set(), set()
    for g in grams:
        if g in PROVINCES:
            provs.add(PROVINCES[g])
        if g in COUNTRIES:
            ctys.add(COUNTRIES[g])
    if provs:
        ctys.add("CN")
    return provs, ctys


def parse_ror(org):
    """Summary of a ROR API v2 record."""
    names, display = [], ""
    for n in org.get("names") or []:
        v = (n.get("value") or "").strip()
        types = n.get("types") or []
        if not v or "acronym" in types:
            continue
        names.append(v)
        if "ror_display" in types:
            display = v
    countries = set()
    for loc in org.get("locations") or []:
        cc = ((loc.get("geonames_details") or {}).get("country_code") or "").strip()
        if cc:
            countries.add(cc.upper())
    provs = set()
    for v in names:                       # names only: geocodes can be wrong
        provs |= places(v)[0]
    fundref = set()
    for ext in org.get("external_ids") or []:
        if (ext.get("type") or "").lower() == "fundref":
            fundref |= set(str(x) for x in (ext.get("all") or []))
            if ext.get("preferred"):
                fundref.add(str(ext["preferred"]))
    return {"id": normalize_id(org.get("id")), "name": display or (names[0] if names else ""),
            "countries": countries, "provinces": provs, "fundref": fundref,
            "status": org.get("status") or ""}


def entry_info(f):
    """Name, award tuple, ROR IDs [(id, asserted-by)] and Funder ID of a funder entry."""
    name = (f.get("name") or "").strip()
    awards = tuple(sorted(str(a).strip() for a in (f.get("award") or []) if str(a).strip()))
    fdoi = ""
    m = FUNDREF_RE.search(f.get("DOI") or "")
    if m:
        fdoi = m.group(1)
    rors = []
    for i in f.get("id") or []:
        if not isinstance(i, dict):
            continue
        t = (i.get("id-type") or "").upper()
        v = i.get("id") or ""
        if t == "ROR":
            rid = normalize_id(v)
            if rid:
                rors.append((rid, i.get("asserted-by") or ""))
        elif t == "DOI" and not fdoi:
            m = FUNDREF_RE.search(v)
            if m:
                fdoi = m.group(1)
    return {"name": name, "awards": awards, "rors": rors, "fdoi": fdoi}


# ---------------------------------------------------------------- URLs, HTTP

def work_url(doi):
    return "%s/%s?mailto=%s" % (CROSSREF, urllib.parse.quote(doi, safe="/"), MAILTO)


def ror_url(rid):
    return "%s/%s" % (ROR_API, rid)


def fundref_url(fid):
    return "%s?query.advanced=%s" % (ROR_API, urllib.parse.quote("external_ids.all:" + fid))


def list_url(rid, member="", from_date="", cursor="*", rows=100):
    filt = "ror-id:https://ror.org/" + rid
    if member:
        filt += ",member:%s" % member
    if from_date:
        filt += ",from-pub-date:%s" % from_date
    q = [("filter", filt), ("select", "DOI,funder"), ("rows", str(rows)),
         ("cursor", cursor), ("mailto", MAILTO)]
    return CROSSREF + "?" + urllib.parse.urlencode(q)


def http_get(url, tries=5):
    """GET a JSON URL; None on 404; retries on 429, 5xx and network errors."""
    delay = 2.0
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                   "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code not in (429, 500, 502, 503, 504) or i == tries - 1:
                raise
        except (urllib.error.URLError, OSError):
            if i == tries - 1:
                raise
        time.sleep(delay)
        delay *= 2
    return None


# ------------------------------------------------------------------- checker

def blank_row(doi):
    row = dict.fromkeys(FIELDS, "")
    row["doi"] = doi
    return row


class Checker:
    def __init__(self, get=None, pause=0.1):
        self.get = get or http_get
        self.pause = pause
        self.cache = {}
        self.fcache = {}

    def fetch(self, url):
        if self.pause:
            time.sleep(self.pause)
        return self.get(url)

    def lookup(self, rid):
        if rid not in self.cache:
            data = self.fetch(ror_url(rid))
            self.cache[rid] = parse_ror(data) if data else None
        return self.cache[rid]

    def fundref_owners(self, fid):
        """ROR IDs whose record lists Funder ID fid."""
        if fid not in self.fcache:
            data = self.fetch(fundref_url(fid)) or {}
            owners = []
            for item in data.get("items") or []:
                for ext in item.get("external_ids") or []:
                    if (ext.get("type") or "").lower() != "fundref":
                        continue
                    if fid in [str(x) for x in (ext.get("all") or [])]:
                        rid = normalize_id(item.get("id"))
                        if rid and rid not in owners:
                            owners.append(rid)
            self.fcache[fid] = owners
        return self.fcache[fid]

    def judge(self, doi, idx, name, src, awards, fdoi, rid, by):
        row = blank_row(doi)
        row.update({"entry": idx, "funder_name": name, "name_source": src,
                    "award": ";".join(awards),
                    "funder_doi": ("10.13039/" + fdoi) if fdoi else "",
                    "ror_id": rid, "asserted_by": by})
        try:
            rec = self.lookup(rid)
        except Exception as ex:                       # network trouble
            row["verdict"], row["detail"] = "error", "ROR lookup failed: %s" % ex
            return row
        if rec is None:
            row["verdict"], row["detail"] = "error", "ROR ID not found"
            return row
        row["ror_name"] = rec["name"]
        row["ror_country"] = ",".join(sorted(rec["countries"]))
        if fdoi:
            if fdoi in rec["fundref"]:
                row["verdict"] = "ok"
                row["detail"] = "funder DOI is listed on the ROR record"
                return row
            try:
                owners = self.fundref_owners(fdoi)
            except Exception:
                owners = []
            if owners:
                row["verdict"] = "doi-ror-conflict"
                row["detail"] = "funder DOI 10.13039/%s is on ROR %s, not %s" % (
                    fdoi, ", ".join(owners), rid)
                return row
        if not name:
            row["verdict"] = "unpaired"
            row["detail"] = "no funder name for this ROR ID"
            return row
        provs, ctys = places(name)
        if ctys and rec["countries"] and not (ctys & rec["countries"]):
            row["verdict"] = "country-mismatch"
            row["detail"] = "name points to %s; ROR record is in %s" % (
                ",".join(sorted(ctys)), row["ror_country"])
            return row
        if provs and rec["provinces"] and not (provs & rec["provinces"]):
            row["verdict"] = "province-mismatch"
            row["detail"] = "name names %s; ROR record names %s" % (
                ", ".join(sorted(provs)), ", ".join(sorted(rec["provinces"])))
            return row
        checked = bool(ctys and rec["countries"]) or bool(provs and rec["provinces"])
        row["verdict"] = "ok" if checked else "unchecked"
        return row

    def check_work(self, doi, funders, only=None):
        infos = [entry_info(f) for f in funders or [] if isinstance(f, dict)]
        rows = []
        for idx, e in enumerate(infos):
            for rid, by in e["rors"]:
                if only and rid not in only:
                    continue
                name, src, fdoi = e["name"], ("entry" if e["name"] else ""), e["fdoi"]
                if not name and e["awards"]:
                    pairs = [o for o in infos
                             if o is not e and o["name"] and o["awards"] == e["awards"]]
                    names = sorted(set(o["name"] for o in pairs))
                    if len(names) == 1:
                        name, src = names[0], "award-pair"
                        if not fdoi:
                            dois = sorted(set(o["fdoi"] for o in pairs if o["fdoi"]))
                            if len(dois) == 1:
                                fdoi = dois[0]
                rows.append(self.judge(doi, idx, name, src, e["awards"], fdoi, rid, by))
        return rows

    def check_doi(self, doi):
        try:
            data = self.fetch(work_url(doi))
        except Exception as ex:
            row = blank_row(doi)
            row["verdict"], row["detail"] = "error", "Crossref lookup failed: %s" % ex
            return [row]
        if not data:
            row = blank_row(doi)
            row["verdict"], row["detail"] = "error", "DOI not found in Crossref"
            return [row]
        msg = data.get("message") or {}
        return self.check_work(msg.get("DOI") or doi, msg.get("funder") or [])

    def scan_ror(self, rid, member="", from_date="", limit=0):
        """Check the entries carrying rid in every Crossref work that has it."""
        rows, n, cursor = [], 0, "*"
        while True:
            data = self.fetch(list_url(rid, member, from_date, cursor)) or {}
            msg = data.get("message") or {}
            items = msg.get("items") or []
            for it in items:
                rows.extend(self.check_work(it.get("DOI") or "", it.get("funder") or [],
                                            only={rid}))
                n += 1
                if limit and n >= limit:
                    return rows, n
            total = msg.get("total-results")
            nxt = msg.get("next-cursor")
            if not items or not nxt or (isinstance(total, int) and n >= total):
                return rows, n
            cursor = nxt


# ------------------------------------------------------------------- output

def summary_line(rows, n_works):
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    parts = ["%d works" % n_works, "%d funder ROR IDs" % len(rows)]
    for v in ORDER:
        if counts.get(v):
            parts.append("%s %d" % (v, counts[v]))
    return "; ".join(parts)


def render_text(rows, n_works, show_all=False):
    out = []
    for r in rows:
        if show_all or r["verdict"] in SUSPECT or r["verdict"] == "error":
            out.append("%s  entry %s  %s\n    funder: %s%s\n    ror: %s %s (%s), asserted by %s\n    %s"
                       % (r["doi"], r["entry"], r["verdict"].upper(),
                          r["funder_name"] or "(no name)",
                          (" [%s]" % r["funder_doi"]) if r["funder_doi"] else "",
                          r["ror_id"], r["ror_name"], r["ror_country"],
                          r["asserted_by"] or "?", r["detail"]))
    out.append(summary_line(rows, n_works))
    return "\n".join(out) + "\n"


def render_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, FIELDS, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def exit_code(rows):
    if any(r["verdict"] in SUSPECT for r in rows):
        return 1
    if any(r["verdict"] == "error" for r in rows):
        return 2
    return 0


def main(argv=None, get=None, out=None):
    out = out or sys.stdout
    p = argparse.ArgumentParser(
        prog="funder_ror_check",
        description="Find funder ROR IDs in Crossref metadata that name the wrong funder.")
    p.add_argument("dois", nargs="*", help="DOIs to check")
    p.add_argument("--ror", action="append", default=[],
                   help="scan every Crossref work carrying this ROR ID (repeatable)")
    p.add_argument("--member", default="", help="with --ror: only this Crossref member ID")
    p.add_argument("--from-pub-date", default="", help="with --ror: e.g. 2026-01-01")
    p.add_argument("--limit", type=int, default=0, help="with --ror: at most N works per ID")
    p.add_argument("--csv", action="store_true", help="CSV output (all rows)")
    p.add_argument("--all", action="store_true", help="show ok/unchecked rows too")
    p.add_argument("--pause", type=float, default=0.1, help="seconds between requests")
    p.add_argument("--version", action="version", version="funder_ror_check " + VERSION)
    a = p.parse_args(argv)
    if not a.dois and not a.ror:
        p.error("give one or more DOIs or --ror <id>")
    ck = Checker(get=get, pause=a.pause)
    rows, n = [], 0
    for d in a.dois:
        m = DOI_RE.match(d.strip())
        n += 1
        if not m:
            row = blank_row(d)
            row["verdict"], row["detail"] = "error", "not a DOI"
            rows.append(row)
            continue
        rows.extend(ck.check_doi(m.group(1)))
    for r in a.ror:
        rid = normalize_id(r)
        if not rid:
            p.error("not a ROR ID: %s" % r)
        got, k = ck.scan_ror(rid, a.member, a.from_pub_date, a.limit)
        rows.extend(got)
        n += k
    out.write(render_csv(rows) if a.csv else render_text(rows, n, a.all))
    return exit_code(rows)


if __name__ == "__main__":
    sys.exit(main())
