#!/usr/bin/env python3
"""
ingest_employee_checkin.py — Ingest Employee Checkin from CSV via background jobs.

Usage:
  /home/frappe/frappe-bench/env/bin/python ingest_employee_checkin.py

Why background jobs (not direct console):
  Lesson: 12,562 rows hit Frappe's 240s timeout when run via direct bench console.
  Solution: enqueue batches via Frappe background jobs (RQ). Same pattern used
  successfully in prior pberp demo (25 batches × 500 = 12,500).

Reusable / idempotent:
  - Skips already-ingested rows (compares CSV count vs DB count)
  - Each background job processes 500 rows
  - Polls for job completion before continuing
  - Halts on count mismatch

Commits-ready: parameterized via constants at top.
"""
import csv
import sys
import time
from pathlib import Path

# ---- Config ----
CSV_PATH = Path("/root/.openclaw/workspace/projects/haritha-hospitals/masters/employee_checkin.csv")
SITE = "pberpprod.duckdns.org"
BATCH_SIZE = 500
ENTITY = "Employee Checkin"
JOB_TIMEOUT = 600  # seconds to wait for each batch's background job

# ---- Init Frappe ----
import os
# Ensure CWD is bench dir so frappe.init() can find sites/
BENCH_DIR = "/home/frappe/frappe-bench"
if os.getcwd() != BENCH_DIR:
    os.chdir(BENCH_DIR)

import frappe

frappe.init(site=SITE)
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

# ---- Submit batches via background jobs ----
start_idx = db_count
total_enqueued = 0

for batch_end in range(start_idx + BATCH_SIZE, csv_count + BATCH_SIZE, BATCH_SIZE):
    batch_end = min(batch_end, csv_count)
    batch = all_rows[start_idx:batch_end]
    if not batch:
        break

    print(f"  batch {start_idx}-{batch_end} ({len(batch)} rows)...", end=" ", flush=True)

    try:
        # Enqueue as background job
        job = frappe.enqueue(
            "scripts.ingest_employee_checkin_worker.insert_batch",
            queue="long",
            batch=batch,
            start_idx=start_idx,
            enqueue_after_commit=True,
        )
        # Wait for completion
        if job:
            waited = 0
            while job.get_status() in ("queued", "started") and waited < JOB_TIMEOUT:
                time.sleep(2)
                waited += 2
            if job.get_status() != "finished":
                print(f"FAIL: job status={job.get_status()} after {waited}s")
                sys.exit(1)
        total_enqueued += len(batch)
    except Exception as e:
        print(f"ERROR enqueueing: {e}")
        sys.exit(1)

    # Verify count
    new_count = frappe.db.count(ENTITY)
    expected = batch_end
    if new_count < expected:
        print(f"FAIL (DB={new_count} < expected={expected})")
        sys.exit(1)

    print(f"OK (DB total={new_count})")
    start_idx = batch_end

print(f"\n=== complete ===")
print(f"  CSV: {csv_count} rows")
print(f"  Enqueued: {total_enqueued}")
print(f"  DB final: {frappe.db.count(ENTITY)}")
sys.exit(0)