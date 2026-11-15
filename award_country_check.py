# SPDX-License-Identifier: Apache-2.0
# award_country_check.py - find grants of one country filed under another
# country's same-name funder in Crossref, using award-number formats.
# Made with AI agents working in the name of MV2, Munim, Inc.
"""Classify award numbers by the country whose format they follow, and scan
every Crossref work that carries one Funder Registry ID.

Examples: South Africa's National Research Foundation has the Funder
Registry ID 10.13039/501100001321 and the bare name "National Research
Foundation"; Thailand's Ministry of Education has 10.13039/100009950 and the
bare name "Ministry of Education"; Vietnam's Ministry of Science and
Technology has 10.13039/100007225 and the bare name "Ministry of Science and
Technology". Korean, Taiwanese, Chinese and Singaporean grants are often
deposited under them.

Standard library only.

    python award_country_check.py --funder 501100001321 --home ZA \
        --out-dir out --mailto you@example.org [--max-pages N]
    python award_country_check.py --funder 100009950 --home TH \
        --formats KR,SG,CN,TW,TH,SK --out-dir out
    python award_country_check.py --funder 100007225 --home VN \
        --formats KR,SG,CN,TW,TH,SK,VN,IN --out-dir out
"""
import argparse
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request

__version__ = "0.3.0"

API = "https://api.crossref.org/works"
FUNDER_PREFIX = "10.13039/"

# Characters removed before matching: spaces, all dash forms, and light
# punctuation. Award strings are upper-cased first.
_STRIP = re.compile(r"[\s\-‐‑‒–—−_:#.()\[\]]")
# Leading words dropped after stripping (e.g. "Grant No. 84379").
_LEAD = re.compile(r"^(GRANTNUMBER|GRANTNO|GRANT|PROJECTNO|NUMBER|NO)")
_SPLIT = re.compile(r"[,;/&]|\bAND\b", re.IGNORECASE)

# Korea (National Research Foundation of Korea and its predecessors).
_KR = [
    re.compile(r"RS20\d{2}(NR)?\d{5,}"),            # RS-2023-00281839
    re.compile(r"20\d{2}[RMKN]\d[A-Z]\d[A-Z0-9]*\d{4,}"),  # 2019R1A2C1003456
    re.compile(r"^(NRF|KRF)?(19|20)\d{9}$"),        # 2012-0001509
    re.compile(r"^(NRF|KRF)(19|20)\d{6,9}$"),       # NRF-2010-6145
]
# Singapore (National Research Foundation Singapore; Ministry of Education
# Academic Research Fund; NUS grant codes).
_SG = [
    re.compile(r"^NRF(CRP|NRFF|RSS|NRFI|CSA|MSG|SBP|QEP|IG|CREATE)"),
    re.compile(r"^NRF20\d{2}[A-Z]"),                # NRF2016NRF-NSFC002-013
    re.compile(r"^MOE(20\d{2})?T[123]"),            # MOE2013-T2-2-054, MOE-T2EP10223-0002
    re.compile(r"^R\d{3}000[A-Z0-9]{3}\d{3}$"),     # R-154-000-B18-114 (NUS)
]
# China (Guangdong provincial science programmes, 2022A1515010159; Ministry
# of Education humanities and social science projects, 21YJCZH147,
# 21JZD056, 2025JZDZ093, 24JDSZ3126; Ministry of Science and Technology
# national programmes: National Key R&D 2016YFA0204100, 973 2011CB707906,
# 863 2012AA101801, Key Technologies 2015BAD09B010102, megaprojects
# 2014ZX09507003006, basic work 2012FY120100, SKA 2020SKA0110100,
# instruments 2011YQ120023, international cooperation 2008DFA30770,
# S2012GR0290).
_CN = [
    re.compile(r"^20\d{2}[AB]\d{10}$"),
    re.compile(r"^\d{2}YJ[ACE][A-Z0-9]*\d{3}$"),
    re.compile(r"^(\d{2}|20\d{2})JZD[A-Z]?\d{3}$"),
    re.compile(r"^\d{2}JDSZ\d{3,}$"),
    re.compile(r"^(SQ)?20\d{2}YF[A-H]\d{5,}"),
    re.compile(r"^20\d{2}CB\d{6}$"),
    re.compile(r"^20\d{2}AA\d{2}[A-Z0-9]\d{3}$"),
    re.compile(r"^20\d{2}BA[A-K]\d{2}B\d{2}"),
    re.compile(r"^20\d{2}ZX\d{8,}"),
    re.compile(r"^20\d{2}FY\d{6}$"),
    re.compile(r"^20\d{2}SKA\d{7}$"),
    re.compile(r"^20\d{2}YQ\d{6}$"),
    re.compile(r"^20\d{2}DF[ABR]\d{5}$"),
    re.compile(r"^S20\d{2}GR\d{4}$"),
]
# Taiwan (Ministry of Education, ROC-year codes such as 107L9006,
# 114L9A00303; Ministry of Science and Technology / National Science
# Council / National Science and Technology Council project numbers such as
# MOST 103-2221-E-006-093-MY3, NSC 99-2320-B-002-017, 109-2622-8-002-003,
# 110-2218-E-A49-014-MBK: ROC year, 4-digit programme code starting 2 or 3,
# field letter, 3-4 character institution code, 3-digit serial).
_TW = [
    re.compile(r"^\d{2,3}L\d[A-Z0-9]{3,}$"),
    re.compile(r"^(MOST|NSC|NSTC)?\d{2,3}[23]\d{3}[A-Z8][A-Z0-9]{3,4}\d{3}"
               r"([A-Z]{1,3}\d?)?$"),
]
# Thailand (Thailand Research Fund grant codes, MRG6180091, IRG5980007).
_TH = [re.compile(r"^(MRG|IRG|RSA|PHD|RTA|DBG|TRG|RDG|DPG)\d{7}$")]
# Slovakia (VEGA, the Slovak Ministry of Education's grant agency).
_SK = [re.compile(r"^VEGA\d")]
# South Africa (NRF South Africa). The plain-digits rule is loose: leave ZA
# out of --formats when scanning a funder that is not South Africa's.
_ZA = [
    re.compile(r"^UID\d{4,6}$"),
    re.compile(r"^\d{4,6}$"),
    re.compile(r"^(PRMND|AHPMDS|TTK|CSUR|PMDS|SRUG|NFSG|MND|RA|BAAP|PPNT|CPRR|"
               r"IFR|SFP|PSTD|RCA|SARC|KSC|EQP|CPT)\d{6,}$"),
]

# Tested in this order: Korea first (NRF-2019R1A... must not count as
# Singapore), South Africa's loose digits rule last.
_FORMATS = (("KR", _KR), ("SG", _SG), ("CN", _CN), ("TW", _TW),
            ("TH", _TH), ("SK", _SK), ("ZA", _ZA))

# Formats read from a whole award field before it is split on "/" and ",":
# Vietnamese numbers (2372/QD-BKHCN, ĐTCB.12/21/VNCHN, KC01.05/11-15,
# NĐT.101.TW/21; the letter Đ is used only in Vietnamese) and Indian DST,
# DBT and SERB numbers (DST/TMD/HFC/2k18/123, BT/PR10903/MED/29/829/2014,
# CRG/2023/005571). The field is upper-cased with spaces removed first.
_VN = [re.compile(r"Đ|BKHCN|VNCHN|^KC\d{2}\.\d{2}/")]
_IN = [re.compile(r"^(BT|DST|SERB|CRG|EMR|ECR|SRG|NRDMS)/")]
_FIELD_FORMATS = (("VN", _VN), ("IN", _IN))

ALL_FORMATS = (tuple(label for label, _ in _FORMATS)
               + tuple(label for label, _ in _FIELD_FORMATS))

# Country words matched anywhere in an entry name.
_NAME_HINTS = [
    ("KR", ("KOREA",)),
    ("SG", ("SINGAPORE",)),
    ("TW", ("TAIWAN",)),
    ("CN", ("CHINA", "CHINESE", "GUANGDONG")),
    ("TH", ("THAILAND",)),
    ("SK", ("SLOVAK",)),
    ("ZA", ("SOUTH AFRICA", "THUTHUKA", "SARCHI")),
]
# Country words matched only as whole words ("INDIA" must not match
# "Indiana").
_NAME_WORDS = [
    ("VN", ("VIETNAM", "VIET NAM", "VIETNAMESE")),
    ("IN", ("INDIA",)),
]


def compact(award):
    """Upper-case an award string and drop spaces, dashes and light
    punctuation, then a leading 'GRANT NO' style word."""
    s = _STRIP.sub("", str(award).upper())
    return _LEAD.sub("", s)


def split_awards(text):
    """Split one award field that may hold several numbers."""
    parts = [p.strip() for p in _SPLIT.split(str(text))]
    return [p for p in parts if p]


def parse_formats(text):
    """'KR,sg, TW' -> ('KR', 'SG', 'TW'); '' or None -> None (all)."""
    if not text:
        return None
    out = []
    for part in str(text).split(","):
        p = part.strip().upper()
        if not p:
            continue
        if p not in ALL_FORMATS:
            raise ValueError("unknown format %r (known: %s)"
                             % (p, ",".join(ALL_FORMATS)))
        out.append(p)
    return tuple(out) or None


def classify_award(award, formats=None):
    """Return a country label ('KR', 'SG', 'CN', 'TW', 'TH', 'SK', 'ZA') or
    None for one award number. formats limits which labels may be given
    (None: all)."""
    s = compact(award)
    if not s:
        return None
    for label, patterns in _FORMATS:
        if formats is not None and label not in formats:
            continue
        for pat in patterns:
            if pat.search(s):
                return label
    return None


def classify_field(text, formats=None):
    """Return 'VN' or 'IN' for a whole award field in a Vietnamese or Indian
    format, else None. formats limits which labels may be given."""
    up = re.sub(r"\s", "", str(text or "").upper()).lstrip("[(")
    if not up:
        return None
    for label, patterns in _FIELD_FORMATS:
        if formats is not None and label not in formats:
            continue
        for pat in patterns:
            if pat.search(up):
                return label
    return None


def classify_name(name):
    """Country named in a funder-entry name, or None. 'Republic of China'
    without 'People's', and 'R.O.C.', count as Taiwan."""
    up = str(name or "").upper()
    if "REPUBLIC OF CHINA" in up and "PEOPLE" not in up:
        return "TW"
    if "R.O.C" in up and "P.R.O.C" not in up:
        return "TW"
    for label, words in _NAME_HINTS:
        for w in words:
            if w in up:
                return label
    padded = " " + re.sub(r"[^A-Z]+", " ", up) + " "
    for label, words in _NAME_WORDS:
        for w in words:
            if " " + w + " " in padded:
                return label
    return None


def classify_entry(entry, formats=None):
    """Set of country labels for one Crossref funder entry, from its name
    and every award number on it. A field in a whole-field format
    (Vietnamese, Indian) is not split further."""
    labels = set()
    n = classify_name(entry.get("name"))
    if n:
        labels.add(n)
    for field in entry.get("award") or []:
        f = classify_field(field, formats)
        if f:
            labels.add(f)
            continue
        for a in split_awards(field):
            c = classify_award(a, formats)
            if c:
                labels.add(c)
    return labels


def norm_funder(fid):
    """'501100001321', '10.13039/501100001321' or a doi.org URL ->
    '10.13039/501100001321'."""
    s = str(fid).strip()
    for p in ("https://doi.org/", "http://dx.doi.org/", "http://doi.org/"):
        if s.lower().startswith(p):
            s = s[len(p):]
    if not s.startswith(FUNDER_PREFIX):
        s = FUNDER_PREFIX + s
    return s


def target_entries(work, funder_doi):
    """Funder entries of a work whose DOI is the target Funder ID."""
    out = []
    for e in work.get("funder") or []:
        if str(e.get("DOI", "")).lower() == funder_doi.lower():
            out.append(e)
    return out


def classify_work(work, funder_doi, home, formats=None):
    """Row for one work: the target entries' labels and a verdict.
    verdict: 'FOREIGN' (any non-home label), 'HOME' (only home labels),
    'UNCLEAR' (no label)."""
    entries = target_entries(work, funder_doi)
    labels = set()
    asserted = set()
    names = []
    awards = []
    for e in entries:
        labels |= classify_entry(e, formats)
        asserted.add(e.get("doi-asserted-by") or "")
        names.append(str(e.get("name") or ""))
        awards.extend(str(a) for a in (e.get("award") or []))
    foreign = sorted(l for l in labels if l != home)
    if foreign:
        verdict = "FOREIGN"
    elif labels:
        verdict = "HOME"
    else:
        verdict = "UNCLEAR"
    created = ((work.get("created") or {}).get("date-time") or "")[:10]
    return {
        "doi": work.get("DOI", ""),
        "publisher": work.get("publisher", ""),
        "created": created,
        "entries": len(entries),
        "names": " | ".join(names),
        "awards": " | ".join(awards),
        "labels": ",".join(sorted(labels)),
        "foreign": ",".join(foreign),
        "asserted_by": ",".join(sorted(a for a in asserted if a)),
        "verdict": verdict,
    }


def page_url(funder_doi, cursor, rows, mailto):
    q = {
        "filter": "funder:" + funder_doi,
        "rows": str(rows),
        "cursor": cursor,
        "select": "DOI,funder,publisher,created",
    }
    if mailto:
        q["mailto"] = mailto
    return API + "?" + urllib.parse.urlencode(q)


def http_get_json(url, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "award-country-check/" + __version__})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as exc:  # network errors and 429s: back off
            last = exc
            time.sleep(5 * (i + 1))
    raise RuntimeError("failed: %s (%s)" % (url, last))


def scan(funder_doi, home, fetch=http_get_json, rows=1000, mailto="",
         max_pages=0, formats=None, pause=1.0):
    """Yield (total_results, row) for every work carrying funder_doi."""
    cursor = "*"
    pages = 0
    seen = set()
    while True:
        data = fetch(page_url(funder_doi, cursor, rows, mailto))
        msg = data.get("message") or {}
        items = msg.get("items") or []
        total = msg.get("total-results", 0)
        for w in items:
            doi = w.get("DOI", "")
            if doi in seen:
                continue
            seen.add(doi)
            yield total, classify_work(w, funder_doi, home, formats)
        pages += 1
        nxt = msg.get("next-cursor")
        if not items or not nxt or (max_pages and pages >= max_pages):
            return
        cursor = nxt
        if pause:
            time.sleep(pause)


def summarize(rows, total, funder_doi, home):
    s = {"funder": funder_doi, "home": home, "total_results": total,
         "works_scanned": 0, "verdict": {}, "foreign_label": {},
         "foreign_by_publisher": {}, "foreign_by_year": {},
         "foreign_asserted_by": {}, "version": __version__}
    for r in rows:
        s["works_scanned"] += 1
        s["verdict"][r["verdict"]] = s["verdict"].get(r["verdict"], 0) + 1
        if r["verdict"] != "FOREIGN":
            continue
        for l in r["foreign"].split(","):
            s["foreign_label"][l] = s["foreign_label"].get(l, 0) + 1
        p = r["publisher"]
        s["foreign_by_publisher"][p] = s["foreign_by_publisher"].get(p, 0) + 1
        y = r["created"][:4]
        s["foreign_by_year"][y] = s["foreign_by_year"].get(y, 0) + 1
        a = r["asserted_by"] or "none"
        s["foreign_asserted_by"][a] = s["foreign_asserted_by"].get(a, 0) + 1
    return s


FIELDS = ["doi", "publisher", "created", "entries", "names", "awards",
          "labels", "foreign", "asserted_by", "verdict"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--funder", required=True)
    ap.add_argument("--home", required=True, help="country code of the funder")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--mailto", default="")
    ap.add_argument("--max-pages", type=int, default=0)
    ap.add_argument("--formats", default="",
                    help="comma list of award formats to use (default: all of "
                         + ",".join(ALL_FORMATS) + ")")
    a = ap.parse_args(argv)
    fdoi = norm_funder(a.funder)
    formats = parse_formats(a.formats)
    os.makedirs(a.out_dir, exist_ok=True)
    tag = fdoi.split("/")[-1]
    rows, total = [], 0
    for total, row in scan(fdoi, a.home.upper(), mailto=a.mailto,
                           max_pages=a.max_pages, formats=formats):
        rows.append(row)
    with open(os.path.join(a.out_dir, "works-%s.csv" % tag), "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    s = summarize(rows, total, fdoi, a.home.upper())
    s["formats"] = list(formats) if formats else list(ALL_FORMATS)
    with open(os.path.join(a.out_dir, "summary-%s.json" % tag), "w",
              encoding="utf-8") as f:
        json.dump(s, f, indent=1, sort_keys=True)
    print(json.dumps(s["verdict"]), s["works_scanned"], "of", total)
    return s


if __name__ == "__main__":
    main()
