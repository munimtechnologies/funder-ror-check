# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. Made with AI agents working in the name of MV2, Munim, Inc.
"""PREREG-FUNDER-1 census: (a) ROR affiliation-matcher probe for 26 provincial science
departments x 3 name forms; (b) funder_ror_check --ror scan of every Crossref work
carrying each of the 26 department ROR IDs. Writes probe.csv, scan.csv, summary.json."""
import csv
import json
import os
import sys
import time

import funder_ror_check as frc
import ror_matcher_probe as rmp

SUSPECT = set(frc.SUSPECT)


def write_csv(path, fields, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    probe_rows = rmp.probe(rmp.http_get, sorted(rmp.DEPARTMENTS), list(rmp.TEMPLATES), pause=0.3)
    write_csv(os.path.join(out_dir, "probe.csv"), rmp.FIELDS, probe_rows)
    by_template = {}
    for t in rmp.TEMPLATES:
        rows = [r for r in probe_rows if r["query"] == t.replace("{p}", r["province"])]
        by_template[t] = rmp.counts(rows)
        by_template[t]["wrong_provinces"] = sorted(
            "%s->%s" % (r["province"], r["chosen_ror"]) for r in rows if r["verdict"] == "wrong")

    ck = frc.Checker(pause=0.2)
    scan_rows, works, errors = [], {}, {}
    for prov in sorted(rmp.DEPARTMENTS):
        rid = rmp.DEPARTMENTS[prov]
        try:
            got, n = ck.scan_ror(rid)
        except Exception as ex:
            got, n = [], -1
            errors[rid] = str(ex)[:300]
        works[prov] = n
        for r in got:
            r = dict(r)
            r["scanned_province"] = prov
            scan_rows.append(r)
        sys.stderr.write("%s %s: %d works, %d rows\n" % (prov, rid, n, len(got)))
    write_csv(os.path.join(out_dir, "scan.csv"), ["scanned_province"] + frc.FIELDS, scan_rows)

    verdicts = {}
    for r in scan_rows:
        k = "%s|%s" % (r["verdict"], r["asserted_by"] or "?")
        verdicts[k] = verdicts.get(k, 0) + 1
    sus_cr = sorted(set(r["doi"].lower() for r in scan_rows
                        if r["verdict"] in SUSPECT and r["asserted_by"] == "crossref"))
    sus_pub = sorted(set(r["doi"].lower() for r in scan_rows
                         if r["verdict"] in SUSPECT and r["asserted_by"] == "publisher"))
    per_target = {}
    for r in scan_rows:
        if r["verdict"] in SUSPECT and r["asserted_by"] == "crossref":
            per_target[r["scanned_province"]] = per_target.get(r["scanned_province"], 0) + 1
    summary = {
        "started": started,
        "finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "probe_by_template": by_template,
        "works_scanned_per_province": works,
        "scan_errors": errors,
        "scan_rows": len(scan_rows),
        "verdict_by_asserted_by": verdicts,
        "suspect_crossref_dois": len(sus_cr),
        "suspect_publisher_dois": len(sus_pub),
        "suspect_crossref_rows_per_scanned_record": per_target,
    }
    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, sort_keys=True)
    with open(os.path.join(out_dir, "suspect_crossref_dois.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sus_cr) + "\n")
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "/out"))
