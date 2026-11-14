# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. Made with AI agents working in the name of MV2, Munim, Inc.
"""country_swap_scan 0.1.0: find Crossref funder entries whose ROR ID belongs to an
organisation in a different country than the one the entry's own name points to.

For each target ROR ID it pages through every Crossref work carrying that ID
(api.crossref.org/works?filter=ror-id:...) and looks at each funder entry that carries
it. Named entries are classified by the countries their name mentions. Unnamed entries
(MDPI deposits a ROR ID as a separate unnamed entry right after the named one, with the
same award numbers) are paired with the named entry they belong to and classified by its
name.

Classes: own (only the target's country is named), foreign (only other countries are
named), mixed (both), unclear (no country named).

Standard library only. Usage:
  python country_swap_scan.py --ror 02kv4zf79 [--max-works 5000] > rows.csv
"""
import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request

__version__ = "0.1.0"
MAILTO = "mv2@munimtech.com"
UA = "country-swap-scan/%s (https://github.com/munimtechnologies/funder-ror-check; mailto:%s)" % (
    __version__, MAILTO)

CN_PLACES = [
    "anhui", "beijing", "chongqing", "fujian", "gansu", "guangdong", "guangxi", "guizhou",
    "hainan", "hebei", "heilongjiang", "henan", "hubei", "hunan", "jiangsu", "jiangxi", "jilin",
    "liaoning", "inner mongolia", "neimenggu", "ningxia", "qinghai", "shaanxi", "shandong",
    "shanghai", "shanxi", "sichuan", "tianjin", "tibet", "xizang", "xinjiang", "yunnan",
    "zhejiang", "shenzhen", "guangzhou", "wuhan", "chengdu", "hangzhou", "nanjing", "hong kong",
    "macau", "macao", "prcmainland", "china", "chinese",
]

# country code -> word patterns (matched on word boundaries, lower case, after normalise())
COUNTRY_WORDS = {
    "CN": CN_PLACES,
    "TW": ["taiwan", "taiwanese", "taiwanroc", "taipei"],
    "PH": ["philippines", "philippine", "filipino"],
    "ZA": ["south africa", "south african"],
    "IN": ["india", "indian", "uttar pradesh", "kerala", "tamil nadu", "karnataka",
           "maharashtra", "gujarat", "west bengal"],
    "VN": ["vietnam", "viet nam", "vietnamese"],
    "BD": ["bangladesh"],
    "PK": ["pakistan"],
    "NP": ["nepal"],
    "MM": ["myanmar"],
    "LA": ["laos", "lao pdr", "lao"],
    "ET": ["ethiopia", "ethiopian"],
    "BA": ["bosnia", "herzegovina"],
    "KR": ["korea", "korean"],
    "JP": ["japan", "japanese"],
    "TH": ["thailand"],
}

# Target records: ROR ID -> (country, extra own-name patterns specific to that record)
TARGETS = {
    "02kv4zf79": ("TW", ["nstc", "national science council",
                         "national science and technology council"]),
    "027s68j25": ("CN", []),
    "05tgxx705": ("PH", ["dost", "pcieerd", "pchrd", "pcaarrd", "erdt",
                         "science education institute"]),
    "048kh7197": ("ZA", ["dsi", "dsti", "nrf", "department of science and innovation",
                         "department of science, technology and innovation"]),
    "0101xrq71": ("IN", ["serb", "inspire", "fist", "dst-"]),
    "02jx32965": ("IN", ["dstup"]),
    "03emtbt60": ("IN", []),
    "02b207r52": ("VN", []),
    "0031khd05": ("BD", []),
    "03jn2p430": ("PK", []),
    "023bdgq43": ("NP", []),
    "03vch0r71": ("MM", []),
    "03jpstz64": ("LA", []),
    "02q7gp705": ("ET", []),
    "03tqbke55": ("BA", []),
}

FIELDS = ["target", "doi", "publisher", "entry", "name", "paired_from", "award",
          "asserted_by", "funder_doi", "countries", "klass"]


def normalise(name):
    """Lower-case and rewrite the China/Taiwan phrases that would otherwise collide."""
    n = " " + (name or "").lower().replace("’", "'") + " "
    n = re.sub(r"people'?s\s+republic\s+of\s+china", " prcmainland ", n)
    n = re.sub(r"\bp\.\s?r\.\s?(of\s+)?china\b", " prcmainland ", n)
    n = re.sub(r"\bpr\s+china\b", " prcmainland ", n)
    n = re.sub(r"\bprc\b", " prcmainland ", n)
    n = re.sub(r"\brepublic\s+of\s+china\b", " taiwanroc ", n)
    n = re.sub(r"\br\.\s?o\.\s?c\.?(?=\W)", " taiwanroc ", n)
    n = re.sub(r"\broc\b", " taiwanroc ", n)
    n = re.sub(r"\bchina\s+medical\s+university\b", " cmuambiguous ", n)
    return n


def has_word(n, w):
    return re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", n) is not None


def countries_in(name, extra_own=(), own_country=None):
    n = normalise(name)
    found = set()
    for cc, words in COUNTRY_WORDS.items():
        if any(has_word(n, w) for w in words):
            found.add(cc)
    if own_country and any(has_word(n, w) for w in extra_own):
        found.add(own_country)
    return found


def classify(found, own_country):
    if not found:
        return "unclear"
    if found == {own_country}:
        return "own"
    if own_country in found:
        return "mixed"
    return "foreign"


def ror_ids(entry):
    out = []
    for i in entry.get("id") or []:
        if i.get("id-type") == "ROR":
            out.append((i.get("id", "").rstrip("/").rsplit("/", 1)[-1], i.get("asserted-by") or ""))
    return out


def pair_name(funders, k):
    """Name for funder entry k: its own, or for an unnamed entry the nearest earlier named
    entry with the same non-empty award list (else the entry just before, if named and the
    unnamed one has no award). Returns (name, paired_from_index or '')."""
    e = funders[k]
    if e.get("name"):
        return e["name"], ""
    award = list(e.get("award") or [])
    if award:
        for j in range(k - 1, -1, -1):
            f = funders[j]
            if f.get("name") and list(f.get("award") or []) == award:
                return f["name"], j
        return "", ""
    if k > 0 and funders[k - 1].get("name") and not funders[k - 1].get("award"):
        return funders[k - 1]["name"], k - 1
    return "", ""


def rows_for_work(work, target):
    cc, extra = TARGETS.get(target, (None, []))
    funders = work.get("funder") or []
    rows = []
    for k, e in enumerate(funders):
        for rid, by in ror_ids(e):
            if rid != target:
                continue
            name, src = pair_name(funders, k)
            found = countries_in(name, extra, cc)
            rows.append({
                "target": target, "doi": (work.get("DOI") or "").lower(),
                "publisher": work.get("publisher") or "", "entry": k, "name": name,
                "paired_from": src, "award": "|".join(e.get("award") or []),
                "asserted_by": by, "funder_doi": e.get("DOI") or "",
                "countries": "|".join(sorted(found)), "klass": classify(found, cc),
            })
    return rows


def works_url(target, cursor, rows=1000):
    q = {"filter": "ror-id:https://ror.org/%s" % target, "rows": str(rows), "cursor": cursor,
         "select": "DOI,funder,publisher", "mailto": MAILTO}
    return "https://api.crossref.org/works?" + urllib.parse.urlencode(q)


def http_get(url, tries=4):
    last = None
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as ex:  # network errors, 429/5xx
            last = ex
            time.sleep(5 * (t + 1))
    raise last


def scan(get, target, max_works=0, rows=1000, pause=1.0):
    """Return (rows, total_results, works_seen)."""
    cursor, seen, out, total = "*", 0, [], None
    while True:
        msg = get(works_url(target, cursor, rows))["message"]
        if total is None:
            total = msg.get("total-results", 0)
        items = msg.get("items") or []
        for w in items:
            out.extend(rows_for_work(w, target))
        seen += len(items)
        cursor = msg.get("next-cursor")
        if not items or not cursor or (max_works and seen >= max_works) or seen >= total:
            return out, total, seen
        time.sleep(pause)


def summarise(rows):
    s = {}
    for r in rows:
        k = "%s|%s" % (r["klass"], r["asserted_by"] or "?")
        s[k] = s.get(k, 0) + 1
    foreign = sorted(set(r["doi"] for r in rows if r["klass"] == "foreign"))
    return {"rows": len(rows), "by_class_asserted": s, "foreign_dois": len(foreign)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ror", required=True, help="target ROR ID, e.g. 02kv4zf79")
    ap.add_argument("--max-works", type=int, default=0)
    a = ap.parse_args(argv)
    rid = a.ror.rstrip("/").rsplit("/", 1)[-1]
    rows, total, seen = scan(http_get, rid, a.max_works)
    w = csv.DictWriter(sys.stdout, FIELDS, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    sys.stderr.write(json.dumps(dict(summarise(rows), total=total, seen=seen)) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
