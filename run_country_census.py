# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. Made with AI agents working in the name of MV2, Munim, Inc.
"""PREREG-COUNTRY-1 census: run country_swap_scan over every target ROR ID in
country_swap_scan.TARGETS. Writes rows.csv, summary.json, foreign_dois.txt to the out dir."""
import csv
import json
import os
import sys
import time

import country_swap_scan as c

CAPS = {"027s68j25": 30000}
DEFAULT_CAP = 60000


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    all_rows, per_target = [], {}
    for rid in c.TARGETS:
        cap = CAPS.get(rid, DEFAULT_CAP)
        try:
            rows, total, seen = c.scan(c.http_get, rid, max_works=cap)
            err = ""
        except Exception as ex:
            rows, total, seen, err = [], -1, 0, str(ex)[:300]
        s = c.summarise(rows)
        pubs = {}
        for r in rows:
            if r["klass"] == "foreign":
                pubs[r["publisher"]] = pubs.get(r["publisher"], 0) + 1
        foreign_with_fdoi = sum(1 for r in rows if r["klass"] == "foreign" and r["funder_doi"])
        s.update({"country": c.TARGETS[rid][0], "total_results": total, "works_seen": seen,
                  "capped": bool(total and total > seen), "error": err,
                  "foreign_rows_by_publisher": pubs,
                  "foreign_rows_with_funder_doi": foreign_with_fdoi,
                  "foreign_funder_dois": sorted(set(r["funder_doi"] for r in rows
                                                    if r["klass"] == "foreign" and r["funder_doi"]))})
        per_target[rid] = s
        all_rows.extend(rows)
        sys.stderr.write("%s: total %s seen %s rows %d foreign DOIs %d %s\n" % (
            rid, total, seen, len(rows), s["foreign_dois"], err))
    with open(os.path.join(out_dir, "rows.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, c.FIELDS, lineterminator="\n")
        w.writeheader()
        for r in all_rows:
            w.writerow(r)
    foreign = sorted(set("%s %s" % (r["target"], r["doi"]) for r in all_rows if r["klass"] == "foreign"))
    with open(os.path.join(out_dir, "foreign_dois.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(foreign) + "\n")
    summary = {"version": c.__version__, "started": started,
               "finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "targets": per_target}
    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "/out"))
