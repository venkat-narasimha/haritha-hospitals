#!/usr/bin/env python3
"""
ingest_attendance.py — Ingest Attendance from CSV to Frappe site via raw SQL bulk insert.

Usage:
  /home/frappe/frappe-bench/env/bin/python ingest_attendance.py

Why raw SQL (not ORM):
  Lesson #43: ORM insert on 12K+ Attendance rows hit 240s Frappe timeout.
  Raw bulk INSERT bypasses validation + timeout. Validates via COUNT after.

Reusable / idempotent:
  - Skips already-ingested rows (compares CSV count vs DB count)
  - Halts on any batch mismatch
  - Batched (default 500 rows/batch)

Commits-ready: parameterized via constants at top.
"""
import csv
import sys
from pathlib import Path

# ---- Config ----
CSV_PATH = Path("/root/.openclaw/workspace/projects/haritha-hospitals/masters/attendance.csv")
SITE = "pberpprod.duckdns.org"
BATCH_SIZE = 500
ENTITY = "Attendance"

# ---- Init Frappe ----
import os
# Ensure CWD is bench dir so frappe.init() can find sites/
BENCH_DIR = "/home/frappe/frappe-bench"
if os.getcwd() != BENCH_DIR:
    os.chdir(BENCH_DIR)

import frappe

frappe.init(site=SITE, sites_path="/home/frappe/frappe-bench/sites")
frappe.connect()

# ---- Read CSV ----
def find_data_start(path: Path) -> int:
    with open(path) as f:
        for i, line in enumerate(f):
            if line.strip() == "## Data":
                return i + 1
    return -1

data_start = find_data_start(CSV_PATH)
if data_start < 0:
    print("ERROR: no '## Data' marker found", file=sys.stderr)
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

# ---- Build bulk INSERT statement ----
# Table: tabAttendance; columns match CSV order
COLUMNS = [
    "name", "employee", "attendance_date", "status", "shift", "leave_type",
    "leave_application", "late_entry_by", "early_out_by", "is_wfh",
    "company", "docstatus", "creation", "modified", "modified_by", "owner"
]

def escape_sql(value):
    """Escape value for SQL literal."""
    if value is None or value == "":
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    # string - escape single quotes and wrap
    return "'" + str(value).replace("\\", "\\\\").replace("'", "''") + "'"

def build_insert(rows, start_name_idx):
    """Build single bulk INSERT for a batch of rows."""
    parts = []
    for i, row in enumerate(rows):
        idx = start_name_idx + i
        # Construct NAME field (Attendance naming pattern: EMP-NNNN-DATE)
        emp = row.get("employee", "").strip()
        date = row.get("attendance_date", "").strip()
        # Frappe default Attendance name = HR-ATT-YYYY-NNNNN or HR-EMP-NNNN-DATE
        # Use a counter-based naming to avoid collisions
        name = f"HR-ATT-{date.replace('-', '')}-{idx:05d}"

        values = [
            escape_sql(name),
            escape_sql(emp),
            escape_sql(date),
            escape_sql(row.get("status", "Present").strip()),
            escape_sql(row.get("shift", "").strip() or None),
            escape_sql(row.get("leave_type", "").strip() or None),
            escape_sql(row.get("leave_application", "").strip() or None),
            escape_sql(int(row.get("late_entry_by", 0) or 0)),
            escape_sql(int(row.get("early_out_by", 0) or 0)),
            escape_sql(int(row.get("is_wfh", 0) or 0)),
            escape_sql(row.get("company", "").strip()),
            "0",  # docstatus
            "NOW()",
            "NOW()",
            "'Administrator'",
            "'Administrator'",
        ]
        parts.append(f"({','.join(values)})")
    cols = ",".join(COLUMNS)
    return f"INSERT INTO `tabAttendance` ({cols}) VALUES " + ",".join(parts)

# ---- Insert in batches ----
start_idx = db_count
total_inserted = 0

for batch_end in range(start_idx + BATCH_SIZE, csv_count + BATCH_SIZE, BATCH_SIZE):
    batch_end = min(batch_end, csv_count)
    batch = all_rows[start_idx:batch_end]
    if not batch:
        break

    print(f"  batch {start_idx}-{batch_end} ({len(batch)} rows)...", end=" ", flush=True)

    try:
        sql = build_insert(batch, start_idx)
        frappe.db.sql(sql)
        frappe.db.commit()
        total_inserted += len(batch)
    except Exception as e:
        frappe.db.rollback()
        print(f"ERROR: {e}")
        print("HALTING — fix and re-run (idempotent, resumes from current count)")
        sys.exit(1)

    # Verify count
    new_count = frappe.db.count(ENTITY)
    expected = batch_end
    if new_count < expected:
        print(f"FAIL (DB={new_count} < expected={expected})")
        print("HALTING")
        sys.exit(1)

    print(f"OK (DB total={new_count})")
    start_idx = batch_end

print(f"\n=== complete ===")
print(f"  CSV: {csv_count} rows")
print(f"  Inserted: {total_inserted}")
print(f"  DB final: {frappe.db.count(ENTITY)}")
sys.exit(0)