#!/usr/bin/env python3
"""
ingest_shift_assignment.py — Ingest Shift Assignment from CSV to Frappe site.

Usage:
  /home/frappe/frappe-bench/env/bin/python ingest_shift_assignment.py

Reusable / idempotent:
  - Skips already-ingested rows (compares CSV count vs DB count)
  - Halts on any batch mismatch
  - Batched insert (default 500 rows/batch) to avoid 240s timeout

Commits-ready: parameterized via constants at top.
"""
import csv
import sys
from pathlib import Path

# ---- Config (override via constants or env vars) ----
CSV_PATH = Path("/root/.openclaw/workspace/projects/haritha-hospitals/masters/shift_assignment.csv")
SITE = "pberpprod.duckdns.org"
BATCH_SIZE = 500
ENTITY = "Shift Assignment"

# ---- Init Frappe ----
import os
# Ensure CWD is bench dir so frappe.init() can find sites/
BENCH_DIR = "/home/frappe/frappe-bench"
if os.getcwd() != BENCH_DIR:
    os.chdir(BENCH_DIR)

import frappe

frappe.init(site=SITE, sites_path="/home/frappe/frappe-bench/sites")
frappe.connect()

# ---- Read CSV (skip comment + ## Data + header rows) ----
def find_data_start(path: Path) -> int:
    with open(path) as f:
        for i, line in enumerate(f):
            if line.strip() == "## Data":
                return i + 1  # next line = header
    return -1

data_start = find_data_start(CSV_PATH)
if data_start < 0:
    print("ERROR: no '## Data' marker found in CSV", file=sys.stderr)
    sys.exit(1)

with open(CSV_PATH) as f:
    lines = f.readlines()[data_start:]
reader = csv.DictReader(lines)
all_rows = [r for r in reader if any(v.strip() for v in r.values())]
csv_count = len(all_rows)
print(f"CSV rows: {csv_count}")

# ---- Current DB count (idempotency) ----
db_count = frappe.db.count(ENTITY)
print(f"DB rows: {db_count}")
if db_count >= csv_count:
    print(f"Already ingested ({db_count} >= {csv_count}). Exiting.")
    sys.exit(0)

# ---- Insert in batches ----
start_idx = db_count  # resume from current count
inserted = 0
errors = []

for batch_end in range(start_idx + BATCH_SIZE, csv_count + BATCH_SIZE, BATCH_SIZE):
    batch_end = min(batch_end, csv_count)
    batch = all_rows[start_idx:batch_end]
    if not batch:
        break

    print(f"  batch {start_idx}-{batch_end} ({len(batch)} rows)...", end=" ", flush=True)

    try:
        for row in batch:
            doc = frappe.new_doc(ENTITY)
            doc.employee = row.get("employee", "").strip()
            doc.shift_type = row.get("shift_type", "").strip()
            doc.start_date = row.get("start_date", "").strip()
            doc.end_date = row.get("end_date", "").strip() or None
            doc.status = row.get("status", "Active").strip()
            doc.docstatus = int(row.get("docstatus", 0))
            doc.company = row.get("company", "").strip()
            doc.shift_location = row.get("shift_location", "").strip() or None
            doc.insert()
            inserted += 1
        frappe.db.commit()
    except Exception as e:
        frappe.db.rollback()
        errors.append((start_idx, batch_end, str(e)))
        print(f"ERROR: {e}")
        print("HALTING — fix and re-run (idempotent, resumes from current count)")
        sys.exit(1)

    # Verify count
    new_count = frappe.db.count(ENTITY)
    expected = batch_end
    if new_count < expected:
        print(f"FAIL (DB={new_count} < expected={expected})")
        print("HALTING — fix and re-run")
        sys.exit(1)

    print(f"OK (DB total={new_count})")
    start_idx = batch_end

print(f"\n=== complete ===")
print(f"  CSV: {csv_count} rows")
print(f"  Inserted: {inserted}")
print(f"  DB final: {frappe.db.count(ENTITY)}")
if errors:
    print(f"  Errors: {len(errors)}")
    for e in errors:
        print(f"    {e}")
    sys.exit(1)
sys.exit(0)