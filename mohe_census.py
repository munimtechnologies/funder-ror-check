# SPDX-License-Identifier: Apache-2.0
# mohe_census.py - count Malaysian (and Egyptian) signals on every Crossref
# work that carries Egypt's bare-named Funder ID "Ministry of Higher
# Education" (10.13039/501100002385).
# Made with AI agents working in the name of MV2, Munim, Inc.
"""Scripted census for PREREG-MOHE-1 (funder-ror-check).

Standard library only.

    python mohe_census.py --out-dir out --mailto you@example.org [--max-pages N]

Signals, read from each work's funder entries:
  award_my        an award on the Egyptian entry in a Malaysian format
                  (FRGS/LRGS/PRGS/ERGS/TRGS/RAGS, or a UTM vote code such as
                  R.J130000.7845.4L669)
  name_my_strict  the Egyptian entry's own name contains "Malaysia"
  name_my         the Egyptian entry's name has any Malaysian word
  cof_my          another entry is Malaysian (name, Malaysia's Funder ID
                  10.13039/501100003093, or a Malaysian award format)
  name_eg/cof_eg  the Egyptian entry or another entry names Egypt, an
                  Egyptian university or programme
Verdict: MY (Malaysian signal only), EG (Egyptian only), BOTH, NONE.
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
EGYPT = "10.13039/501100002385"
MALAYSIA = "10.13039/501100003093"

# Malaysian Ministry of Higher Education grant schemes, and Universiti
# Teknologi Malaysia vote codes. Applied to upper-cased award strings.
_MY_AWARD = re.compile(r"(?:FRGS|LRGS|PRGS|ERGS|TRGS|RAGS)"
                       r"|(?:^|[^A-Z0-9])[RQ]\.[JK]\d{6}\.\d{4}\.")
# Malaysian words in funder names (upper-cased). "Universiti" is Malay;
# Brunei's university is excluded in is_my_name().
_MY_NAME = re.compile(r"MALAYSIA|\bMALAYA\b|\bUNIVERSITI\b|\bIIUM\b"
                      r"|(?:FUNDAMENTAL|LONG[- ]?TERM|PROTOTYPE|EXPLORATORY"
                      r"|TRANS[- ]?DISCIPLINARY) RESEARCH GRANT SCHEME")
# Egyptian words in funder names (upper-cased).
_EG_NAME = re.compile(r"EGYPT|\bCAIRO\b|\bKAIRO\b|\bE-?JUST\b|\bASSIUT\b"
                      r"|\bASYUT\b|\bMANSOURA\b|\bZAGAZIG\b"
                      r"|\bALEXANDRIA UNIVERSITY\b|\bAIN SHAMS\b|\bTANTA\b"
                      r"|\bBENHA\b|\bHELWAN\b|\bMINIA\b|\bSOHAG\b"
                      r"|\bKAFRELSHEIKH\b|\bKAFR EL[- ]?SHEIKH\b|\bMENOUFIA\b"
                      r"|\bSUEZ CANAL\b|\bASWAN\b|\bDAMIETTA\b|\bBENI[- ]SUEF\b"
                      r"|\bACADEMY OF SCIENTIFIC RESEARCH\b|\bMOSHARAFA\b")
# Egypt's Science and Technology Development Fund; Macau's fund has the
# same English name, so it counts only when no Macau funder is on the work.
_STDF = re.compile(r"SCIENCE AND TECHNOLOGY DEVELOPMENT FUND|\bSTDF\b")
_MACAU = re.compile(r"MACAU|MACAO|\bFDCT\b")

# Known rows from the hand sample (FINDINGS-MOHE-1), checked in every run.
SANITY = {
    "10.1021/acsomega.6c06914": "MY",
    "10.1109/icocet63343.2024.10730485": "MY",
    "10.1016/j.cie.2021.107300": "EG",
}


def up(text):
    return str(text or "").upper()


def is_my_award(award):
    return bool(_MY_AWARD.search(up(award)))


def is_my_name(name):
    u = up(name)
    return bool(_MY_NAME.search(u)) and "BRUNEI" not in u


def is_eg_name(name, macau=False):
    u = up(name)
    if _EG_NAME.search(u):
        return True
    return (not macau) and bool(_STDF.search(u))


def entry_doi(entry):
    return str(entry.get("DOI") or "").strip().lower()


def classify_work(work, target=EGYPT):
    """Row with the signals and verdict for one work."""
    t = target.lower()
    entries = work.get("funder") or []
    tgt = [e for e in entries if entry_doi(e) == t]
    others = [e for e in entries if entry_doi(e) != t]
    macau = any(_MACAU.search(up(e.get("name"))) for e in entries)
    tgt_names = [str(e.get("name") or "") for e in tgt]
    tgt_awards = [str(a) for e in tgt for a in (e.get("award") or [])]
    oth_awards = [str(a) for e in others for a in (e.get("award") or [])]

    name_my_strict = any("MALAYSIA" in up(n) for n in tgt_names)
    name_my = any(is_my_name(n) for n in tgt_names)
    award_my = any(is_my_award(a) for a in tgt_awards)
    cof_my = (any(is_my_name(e.get("name")) or entry_doi(e) == MALAYSIA
                  for e in others)
              or any(is_my_award(a) for a in oth_awards))
    name_eg = any(is_eg_name(n, macau) for n in tgt_names)
    cof_eg = any(is_eg_name(e.get("name"), macau) for e in others)

    my = name_my or award_my or cof_my
    eg = name_eg or cof_eg
    if my and eg:
        verdict = "BOTH"
    elif my:
        verdict = "MY"
    elif eg:
        verdict = "EG"
    else:
        verdict = "NONE"
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
        "name_my_strict": int(name_my_strict),
        "name_my": int(name_my),
        "award_my": int(award_my),
        "cof_my": int(cof_my),
        "name_eg": int(name_eg),
        "cof_eg": int(cof_eg),
        "asserted_by": ",".join(asserted),
        "verdict": verdict,
    }


FIELDS = ["doi", "publisher", "created", "n_target", "target_names",
          "target_awards", "other_names", "name_my_strict", "name_my",
          "award_my", "cof_my", "name_eg", "cof_eg", "asserted_by",
          "verdict"]
TIERS = ["name_my_strict", "name_my", "award_my", "cof_my", "name_eg",
         "cof_eg"]


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
                url, headers={"User-Agent": "mohe-census/" + __version__})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as exc:  # network errors and 429s: back off
            last = exc
            time.sleep(5 * (i + 1))
    raise RuntimeError("failed: %s (%s)" % (url, last))


def scan(target=EGYPT, fetch=http_get_json, rows=1000, mailto="",
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


def summarize(rows, total, target=EGYPT):
    s = {"funder": target, "total_results": total, "works_scanned": 0,
         "verdict": {}, "tiers": {k: 0 for k in TIERS},
         "my_by_publisher": {}, "my_by_year": {}, "my_asserted_by": {},
         "my_created_2026": 0, "sanity": {}, "version": __version__}
    by_doi = {}
    for r in rows:
        s["works_scanned"] += 1
        _bump(s["verdict"], r["verdict"])
        for k in TIERS:
            s["tiers"][k] += int(r[k])
        by_doi[r["doi"].lower()] = r["verdict"]
        if r["verdict"] != "MY":
            continue
        _bump(s["my_by_publisher"], r["publisher"])
        _bump(s["my_by_year"], r["created"][:4])
        _bump(s["my_asserted_by"], r["asserted_by"] or "none")
        if r["created"].startswith("2026"):
            s["my_created_2026"] += 1
    for doi, want in SANITY.items():
        got = by_doi.get(doi)
        s["sanity"][doi] = {"expected": want, "found": got,
                            "ok": got == want}
    return s


def main(argv=None, fetch=http_get_json):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--funder", default=EGYPT)
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
    with open(os.path.join(a.out_dir, "mohe-works.csv"), "w", newline="",
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
