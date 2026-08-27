#!/usr/bin/env python3
"""
Haritha Hospitals — bulk-submit draft documents.

Phase 3 ingest used frappe.get_doc().insert() which creates docstatus=0 (Draft).
User observed list views showing "all Draft" — submittable docs need docstatus=1.

Submittable doctypes in Haritha Phase 3 data:
  - Holiday (child of Holiday List; parent is NOT submittable)
  - Shift Assignment (per-employee per-date rows)
  - Attendance (per-employee per-day rows)

This script is idempotent: only docs at docstatus=0 are processed.
Already-submitted docs (docstatus=1) are skipped.

Usage:
  # Dry run — prints expected counts without submitting:
  docker exec erp-prod-backend-1 bash -c "cd /home/frappe/frappe-bench && \
    bench --site pberpprod.duckdns.org execute bulk_submit.run --kwargs '{\"dry_run\": True}'"

  # Live run:
  docker exec erp-prod-backend-1 bash -c "cd /home/frappe/frappe-bench && \
    bench --site pberpprod.duckdns.org execute bulk_submit.run"

Notes:
  - Loaded via bench execute, NOT via custom app module (haritha_hospitals doesn't exist yet).
  - Script must be copied to /home/frappe/frappe-bench/sites/<site>/ or run via
    docker cp + execute.
  - Run with `frappe.flags.in_bulk_submit = True` to skip non-essential hooks
    (per Frappe production migration docs).
"""
import json
import sys
import time
import traceback
from collections import defaultdict
from datetime import datetime

import frappe

# Submittable doctypes in Haritha Phase 3 data, in safe order
# (parents first if any — Holiday is child of Holiday List, but Holiday List
# itself is not submittable so we just process Holiday rows directly.)
SUBMITTABLE_DOCTYPES = [
    ("Holiday", 200),
    ("Shift Assignment", 200),
    ("Attendance", 200),
]


def _get_draft_docnames(doctype: str) -> list[str]:
    """Return all docstatus=0 names for the doctype, ordered by creation."""
    return frappe.get_all(
        doctype,
        filters={"docstatus": 0},
        pluck="name",
        order_by="creation asc",
    )


def _flush_failure(failures: list[dict]):
    """Write failures JSON incrementally so we don't lose data on crash."""
    if not hasattr(_flush_failure, "path"):
        return
    with open(_flush_failure.path, "w") as f:
        json.dump(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "failures": failures,
            },
            f,
            indent=2,
            default=str,
        )


def submit_doctype(
    doctype: str,
    batch_size: int = 200,
    dry_run: bool = False,
    failures: list[dict] | None = None,
) -> dict:
    """Bulk-submit all draft docs of a doctype in batches.

    Returns a summary dict:
      {doctype, total, submitted, failed, skipped, elapsed_sec, batches}
    """
    started = time.time()
    if failures is None:
        failures = []

    # Allow disabling of hooks for performance (per Frappe docs)
    frappe.flags.in_bulk_submit = True

    draft_names = _get_draft_docnames(doctype)
    total = len(draft_names)
    submitted = 0
    skipped = 0

    print(f"\n[{doctype}] found {total} draft docs (dry_run={dry_run})")

    if total == 0:
        return {
            "doctype": doctype,
            "total": 0,
            "submitted": 0,
            "failed": 0,
            "skipped": 0,
            "elapsed_sec": 0,
            "batches": 0,
        }

    if dry_run:
        # Show first 5 names as a sample
        sample = draft_names[:5]
        print(f"  sample names: {sample}")
        batches = (total + batch_size - 1) // batch_size
        return {
            "doctype": doctype,
            "total": total,
            "submitted": 0,
            "failed": 0,
            "skipped": 0,
            "elapsed_sec": 0,
            "batches": batches,
            "dry_run": True,
        }

    batches = 0
    for batch_start in range(0, total, batch_size):
        batch = draft_names[batch_start : batch_start + batch_size]
        batches += 1
        batch_num = batches
        total_batches = (total + batch_size - 1) // batch_size

        print(
            f"  batch {batch_num}/{total_batches}: "
            f"submitting {len(batch)} docs ({submitted + len(batch)}/{total})"
        )

        for name in batch:
            try:
                doc = frappe.get_doc(doctype, name)
                # Double-check docstatus (in case it changed since the initial query)
                if doc.docstatus != 0:
                    skipped += 1
                    continue
                doc.submit()
                submitted += 1
            except Exception as exc:
                err_str = f"{type(exc).__name__}: {exc}"
                failures.append(
                    {
                        "doctype": doctype,
                        "name": name,
                        "error": err_str,
                        "traceback": traceback.format_exc(limit=5),
                    }
                )
                # Print concise error so we can see what's failing without flooding the log
                if len(failures) <= 10 or len(failures) % 100 == 0:
                    print(f"  FAIL {doctype} {name}: {err_str}")
                # continue processing other docs

        # Commit per batch — keeps the txn window small
        try:
            frappe.db.commit()
        except Exception as exc:
            err_str = f"{type(exc).__name__}: {exc}"
            print(f"  WARN commit failed after batch {batch_num}: {err_str}")

    elapsed = time.time() - started
    print(
        f"  done: submitted={submitted} skipped={skipped} failed={len(failures)} "
        f"in {elapsed:.1f}s ({batches} batches)"
    )

    return {
        "doctype": doctype,
        "total": total,
        "submitted": submitted,
        "failed": len(failures),
        "skipped": skipped,
        "elapsed_sec": round(elapsed, 1),
        "batches": batches,
    }


def _patch_status_validation():
    """Monkey-patch erpnext's validate_status to accept Holiday + Weekly Off.

    HRMS Attendance.validate() calls validate_status() with a hardcoded
    5-value list (Present/Absent/On Leave/Half Day/Work From Home). The CSV
    Phase 3 ingest includes 'Holiday' and 'Weekly Off' rows, which the
    property setter lets through the meta-level select check but are
    rejected by this hardcoded validate_status(). See LEARNINGS #X (new).

    This patch wraps validate_status() to silently accept the two extra
    statuses before falling back to the original implementation for other
    values.
    """
    try:
        import erpnext.controllers.status_updater as su
    except ImportError:
        print("WARN: erpnext.controllers.status_updater not importable — skip patch")
        return

    if getattr(su.validate_status, "_haritha_patched", False):
        return  # already patched

    orig = su.validate_status

    def patched(status, options):
        if status in ("Holiday", "Weekly Off"):
            return
        return orig(status, options)

    patched._haritha_patched = True
    su.validate_status = patched
    print("Patched validate_status to accept Holiday + Weekly Off")


def run(dry_run=False):
    """Main entry point for `bench execute bulk_submit.run`."""
    overall_start = time.time()
    failures: list[dict] = []
    results = []

    print(f"=== bulk_submit.run started at {datetime.utcnow().isoformat()}Z ===")
    print(f"dry_run = {dry_run}")
    print(f"site = {frappe.local.site}")
    print(f"frappe.flags.in_bulk_submit = True (set per doctype loop)")

    if not dry_run:
        _patch_status_validation()

    for doctype, batch_size in SUBMITTABLE_DOCTYPES:
        try:
            result = submit_doctype(
                doctype,
                batch_size=batch_size,
                dry_run=dry_run,
                failures=failures,
            )
            results.append(result)
        except Exception as exc:
            err_str = f"{type(exc).__name__}: {exc}"
            print(f"FATAL [{doctype}]: {err_str}")
            print(traceback.format_exc())
            results.append(
                {
                    "doctype": doctype,
                    "fatal": err_str,
                }
            )

    elapsed = time.time() - overall_start
    totals = {
        "submitted": sum(r.get("submitted", 0) for r in results),
        "failed": sum(r.get("failed", 0) for r in results),
        "skipped": sum(r.get("skipped", 0) for r in results),
        "total": sum(r.get("total", 0) for r in results),
    }

    print(f"\n=== bulk_submit.run complete in {elapsed:.1f}s ===")
    print(f"  submitted: {totals['submitted']}")
    print(f"  failed:    {totals['failed']}")
    print(f"  skipped:   {totals['skipped']}")
    print(f"  total:     {totals['total']}")

    print("\nPer-doctype results:")
    for r in results:
        if "fatal" in r:
            print(f"  {r['doctype']}: FATAL {r['fatal']}")
        else:
            print(
                f"  {r['doctype']}: total={r['total']} submitted={r['submitted']} "
                f"failed={r['failed']} skipped={r['skipped']} "
                f"elapsed={r.get('elapsed_sec', 0)}s batches={r.get('batches', 0)}"
            )

    if failures:
        # Persist failures JSON to a known path
        failures_file = (
            f"/home/frappe/frappe-bench/bulk_submit_failures_"
            f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        )
        try:
            with open(failures_file, "w") as f:
                json.dump(
                    {
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "site": frappe.local.site,
                        "totals": totals,
                        "failures": failures,
                    },
                    f,
                    indent=2,
                    default=str,
                )
            print(f"\nFailures written to {failures_file}")
            print(f"  count: {len(failures)}")
        except Exception as exc:
            print(f"\nWARN: could not write failures file: {exc}")
            # Print failures to stdout instead
            print(json.dumps(failures, indent=2, default=str))

    # Return structured result so caller can inspect
    return {
        "totals": totals,
        "per_doctype": results,
        "elapsed_sec": round(elapsed, 1),
        "dry_run": dry_run,
        "site": frappe.local.site,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }