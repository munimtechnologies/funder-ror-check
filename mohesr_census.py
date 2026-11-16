# SPDX-License-Identifier: Apache-2.0
# mohesr_census.py - count other countries' grants on every Crossref work
# that carries the UAE's "Ministry of Higher Education and Scientific
# Research" Funder ID (10.13039/100009122).
# Made with AI agents working in the name of MV2, Munim, Inc.
"""Scripted census for PREREG-MOHESR-1 (funder-ror-check).

Standard library only.

    python mohesr_census.py --out-dir out --mailto you@example.org [--max-pages N]

For each work it reads the funder entries and records country signals:
  award_countries  an award on the UAE entry in a national format
                   (KR, SG, MY, CN, DZ, TN, JP, IN, CZ; see AWARD_FORMATS)
  name_countries   country words in the UAE entry's own name
  cof_countries    country words in another entry's name, or a known
                   national Funder ID on another entry
Verdict: FOREIGN (only non-UAE signals), AE (only UAE), BOTH, NONE.
"""
import argparse
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request

__version__ = "0.1.0"

API = "https://api.crossref.org/works"
UAE = "10.13039/100009122"

# Spaces and every kind of hyphen or dash are removed before award formats
# are tested, so "RS-2023-00241749" becomes "RS202300241749".
_SQUASH = re.compile(r"[\s\-‐‑‒–—−]+")

AWARD_FORMATS = {
    # Korean NRF / MSIT: 2021R1I1A3052320, NRF-2015H1A2A1034022,
    # RS-2023-00241749, RS-2021-NR060087
    "KR": re.compile(r"RS20\d{2}(?:NR)?\d{5,8}"
                     r"|(?<!\d)(?:19|20)\d{2}[A-Z]\d[A-Z]\d"),
    # Singapore MOE AcRF: MOE2018-T2-2-161, MOE-T2EP30122-0005,
    # T2EP30121-0015, 2019-T1-001-126
    "SG": re.compile(r"MOE\d{4}T\d|T2EP\d{5}|MOET[123]"
                     r"|(?<!\d)20\d{2}T1\d{6}(?!\d)"),
    # Malaysian MOHE schemes and Universiti Teknologi Malaysia vote codes
    "MY": re.compile(r"FRGS|LRGS|PRGS|ERGS|TRGS|RAGS"
                     r"|(?<![A-Z0-9])[RQ]\.[JK]\d{6}\.\d{4}\."),
    # Chinese MoE: NCET-05-0680, IRT_17R86, 17YJC630041, 20XJC910001
    "CN": re.compile(r"NCET\d|(?<![A-Z0-9])IRT_?\d"
                     r"|(?<!\d)\d{2}[XY]J[A-Z]\d{6}"),
    # Algerian PRFU projects: B00L01UN400120210002 (PRFU)
    "DZ": re.compile(r"PRFU|(?<![A-Z0-9])[A-Z]00L\d{2}[A-Z]{2}\d{6}"),
    # Tunisian laboratory codes: LR11IP03, LR15CBS06, LR11ES48
    "TN": re.compile(r"(?<![A-Z0-9])LR\d{2}[A-Z]{2,4}\d{2}"),
    # Japanese KAKENHI / AMED with the JP prefix: JP21H02847
    "JP": re.compile(r"(?<![A-Z0-9])JP\d{2}[A-Z]{1,2}\d{4,7}"),
    # Indian MoE STARS: STARS-2/2023-0186, MoE/STARS-1/293
    "IN": re.compile(r"STARS[12]?/"),
    # Czech operational programme codes
    "CZ": re.compile(r"CZ\.02\.|OPVVV"),
}

_NAME_WORDS = {
    "AE": r"EMIRATES|\bUAE\b|ABU DHABI|\bDUBAI\b|SHARJAH|KHALIFA UNIVERSITY"
          r"|\bAJMAN\b",
    "KR": r"KOREA|\bKAIST\b|POSTECH|\bSEOUL\b|\bPUSAN\b|\bBUSAN\b|YONSEI"
          r"|SAMSUNG",
    "CN": r"\bCHINA\b|\bCHINESE\b|\bNSFC\b|SHANGHAI|BEIJING|GUANGDONG"
          r"|ZHEJIANG|JIANGSU|SHANDONG|HUBEI|SHENZHEN|CHONGQING|ANHUI"
          r"|YUNNAN|SHAANXI|HAINAN|CENTRAL UNIVERSITIES",
    "TW": r"TAIWAN|ACADEMIA SINICA|NATIONAL SCIENCE AND TECHNOLOGY COUNCIL"
          r"|\bNSTC\b|NATIONAL TAIWAN|TSING HUA|YANG MING|SPROUT",
    "SG": r"SINGAPORE|A\*STAR|NANYANG",
    "MY": r"MALAYSIA|\bMALAYA\b|\bUNIVERSITI\b|\bIIUM\b|RESEARCH GRANT SCHEME",
    "IN": r"\bINDIA\b|\bINDIAN\b|\bIIT\b|\bSERB\b"
          r"|SCIENCE AND ENGINEERING RESEARCH BOARD|\bICMR\b|\bMEITY\b",
    "JP": r"JAPAN|\bJSPS\b|\bAMED\b|KAKENHI",
    "DZ": r"ALGERIA|\bDGRSDT\b|D[EÉ]VELOPPEMENT TECHNOLOGIQUE|\bPRFU\b"
          r"|CNEPRU",
    "TN": r"TUNISI",
    "IQ": r"\bIRAQ|KURDISTAN|BAGHDAD|SULAIMAN",
    "LY": r"LIBYA",
    "EG": r"EGYPT",
    "SA": r"\bSAUDI|KING ABDULAZIZ|KING SAUD\b|KING KHALID|PRINCE SATTAM"
          r"|UMM AL-QURA",
    "ID": r"INDONESIA",
}
NAME_WORDS = {k: re.compile(v) for k, v in _NAME_WORDS.items()}

# National Funder IDs seen as co-funders in the hand sample.
COUNTRY_IDS = {
    "10.13039/501100003725": "KR",  # National Research Foundation of Korea
    "10.13039/501100014188": "KR",  # Ministry of Science and ICT
    "10.13039/501100002701": "KR",  # Ministry of Education (Korea)
    "10.13039/501100001809": "CN",  # NSFC
    "10.13039/100020595": "TW",     # National Science and Technology Council
    "10.13039/501100004663": "TW",  # Ministry of Science and Technology, TW
    "10.13039/501100001869": "TW",  # Academia Sinica
    "10.13039/501100001868": "TW",  # National Science Council
    "10.13039/501100001381": "SG",  # National Research Foundation Singapore
    "10.13039/501100001348": "SG",  # A*STAR
    "10.13039/501100003093": "MY",  # Ministry of Higher Education, Malaysia
    "10.13039/501100005307": "DZ",  # DGRSDT
    "10.13039/501100007335": "IQ",  # Iraq's MoHESR
    "10.13039/501100001691": "JP",  # JSPS
    "10.13039/501100006013": "AE",  # United Arab Emirates University
}

# Exact entry names that are the bare "Ministry of Education" alternates.
MOE_NAMES = {"MINISTRY OF EDUCATION", "MOE", "MINISTRY OF EDUCATION (MOE)"}

# Known rows from the hand sample (FINDINGS-MOHESR-1), checked in every run.
SANITY = {
    "10.1002/celc.202200093": "FOREIGN",
    "10.1109/cvpr52733.2024.00944": "FOREIGN",
    "10.1128/aem.00286-26": "FOREIGN",
    "10.1016/j.compind.2024.104225": "AE",
    "10.1016/j.ultsonch.2024.107015": "AE",
}


def up(text):
    return str(text or "").upper()


def squash(award):
    return _SQUASH.sub("", up(award))


def award_countries(award):
    """Countries whose award format appears in one award string."""
    s = squash(award)
    return {c for c, rx in AWARD_FORMATS.items() if rx.search(s)}


def name_countries(name):
    """Countries named in one funder name. Taiwan wins over China
    ("Republic of China (Taiwan)"); Brunei's universities are not Malaysian."""
    u = up(name)
    found = {c for c, rx in NAME_WORDS.items() if rx.search(u)}
    if "TW" in found:
        found.discard("CN")
    if "MY" in found and "BRUNEI" in u:
        found.discard("MY")
    return found


def entry_doi(entry):
    return str(entry.get("DOI") or "").strip().lower()


def classify_work(work, target=UAE):
    """Row with the signals and verdict for one work."""
    t = target.lower()
    entries = work.get("funder") or []
    tgt = [e for e in entries if entry_doi(e) == t]
    others = [e for e in entries if entry_doi(e) != t]
    tgt_names = [str(e.get("name") or "") for e in tgt]
    tgt_awards = [str(a) for e in tgt for a in (e.get("award") or [])]

    aw = set()
    for a in tgt_awards:
        aw |= award_countries(a)
    nm = set()
    for n in tgt_names:
        nm |= name_countries(n)
    cof = set()
    for e in others:
        cof |= name_countries(e.get("name"))
        c = COUNTRY_IDS.get(entry_doi(e))
        if c:
            cof.add(c)

    allc = aw | nm | cof
    foreign = allc - {"AE"}
    if foreign and "AE" in allc:
        verdict = "BOTH"
    elif foreign:
        verdict = "FOREIGN"
    elif "AE" in allc:
        verdict = "AE"
    else:
        verdict = "NONE"
    named_moe = any(" ".join(up(n).split()) in MOE_NAMES for n in tgt_names)
    asserted = sorted({str(e.get("doi-asserted-by") or "") for e in tgt}
                      - {""})
    created = ((work.get("created") or {}).get("date-time") or "")[:10]
    other_names = " | ".join(str(e.get("name") or "") for e in others)
    return {
        "doi": str(work.get("DOI") or ""),
        "publisher": str(work.get("publisher") or ""),
        "created": created,
        "n_target": len(tgt),
        "target_names": " | ".join(tgt_names),
        "target_awards": " | ".join(tgt_awards),
        "other_names": other_names[:400],
        "award_countries": ",".join(sorted(aw)),
        "name_countries": ",".join(sorted(nm)),
        "cof_countries": ",".join(sorted(cof)),
        "named_moe": int(named_moe),
        "asserted_by": ",".join(asserted),
        "verdict": verdict,
    }


FIELDS = ["doi", "publisher", "created", "n_target", "target_names",
          "target_awards", "other_names", "award_countries",
          "name_countries", "cof_countries", "named_moe", "asserted_by",
          "verdict"]


def page_url(target, cursor, rows, mailto):
    q = {
        "filter": "funder:" + target,
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
                url, headers={"User-Agent": "mohesr-census/" + __version__})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as exc:  # network errors and 429s: back off
            last = exc
            time.sleep(5 * (i + 1))
    raise RuntimeError("failed: %s (%s)" % (url, last))


def scan(target=UAE, fetch=http_get_json, rows=1000, mailto="",
         max_pages=0, pause=1.0):
    """Yield (total_results, work) for every distinct work on target."""
    cursor = "*"
    pages = 0
    seen = set()
    while True:
        data = fetch(page_url(target, cursor, rows, mailto))
        msg = data.get("message") or {}
        items = msg.get("items") or []
        total = msg.get("total-results", 0)
        for w in items:
            doi = str(w.get("DOI") or "").lower()
            if doi in seen:
                continue
            seen.add(doi)
            yield total, w
        pages += 1
        nxt = msg.get("next-cursor")
        if not items or not nxt or (max_pages and pages >= max_pages):
            return
        cursor = nxt
        if pause:
            time.sleep(pause)


def _bump(d, k):
    d[k] = d.get(k, 0) + 1


def _split(cell):
    return [c for c in str(cell or "").split(",") if c]


def summarize(rows, total, target=UAE):
    s = {"funder": target, "total_results": total, "works_scanned": 0,
         "verdict": {}, "award_country": {}, "any_country": {},
         "named_moe": 0, "named_moe_verdict": {},
         "foreign_by_publisher": {}, "foreign_by_year": {},
         "foreign_asserted_by": {}, "foreign_created_2026": 0,
         "sanity": {}, "version": __version__}
    by_doi = {}
    for r in rows:
        s["works_scanned"] += 1
        _bump(s["verdict"], r["verdict"])
        for c in _split(r["award_countries"]):
            _bump(s["award_country"], c)
        anyc = (set(_split(r["award_countries"]))
                | set(_split(r["name_countries"]))
                | set(_split(r["cof_countries"])))
        for c in sorted(anyc):
            _bump(s["any_country"], c)
        if int(r["named_moe"]):
            s["named_moe"] += 1
            _bump(s["named_moe_verdict"], r["verdict"])
        by_doi[r["doi"].lower()] = r["verdict"]
        if r["verdict"] != "FOREIGN":
            continue
        _bump(s["foreign_by_publisher"], r["publisher"])
        _bump(s["foreign_by_year"], r["created"][:4])
        _bump(s["foreign_asserted_by"], r["asserted_by"] or "none")
        if r["created"].startswith("2026"):
            s["foreign_created_2026"] += 1
    for doi, want in SANITY.items():
        got = by_doi.get(doi)
        s["sanity"][doi] = {"expected": want, "found": got,
                            "ok": got == want}
    return s


def main(argv=None, fetch=http_get_json):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--funder", default=UAE)
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--mailto", default="")
    ap.add_argument("--max-pages", type=int, default=0)
    ap.add_argument("--pause", type=float, default=1.0)
    a = ap.parse_args(argv)
    target = a.funder if a.funder.startswith("10.13039/") else (
        "10.13039/" + a.funder)
    os.makedirs(a.out_dir, exist_ok=True)
    rows, total = [], 0
    for total, w in scan(target, fetch=fetch, mailto=a.mailto,
                         max_pages=a.max_pages, pause=a.pause):
        rows.append(classify_work(w, target))
    with open(os.path.join(a.out_dir, "mohesr-works.csv"), "w", newline="",
              encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=FIELDS)
        wr.writeheader()
        wr.writerows(rows)
    s = summarize(rows, total, target)
    with open(os.path.join(a.out_dir, "summary.json"), "w",
              encoding="utf-8") as f:
        json.dump(s, f, indent=1, sort_keys=True)
    print(json.dumps(s["verdict"], sort_keys=True), s["works_scanned"],
          "of", total)
    return s


if __name__ == "__main__":
    main()
