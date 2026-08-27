#!/usr/bin/env python3
"""
Haritha Hospitals — idempotent recreate of Property Setters added during Phase 3 ingest.

Background (Rule #9 SOUL violation from Phase 3.6 bulk-submit, 2026-08-27):
  Phase 3 ingest used raw SQL bulk insert for Attendance. The CSV source
  uses 7 status values (Present, Absent, On Leave, Half Day, Work From Home,
  Holiday, Weekly Off) but HRMS Attendance.meta.get_field('status').options
  ships with only the first 5. A Property Setter
  `Attendance-status-options` was added at runtime to extend the meta options
  so raw SQL inserts with 'Holiday' / 'Weekly Off' were accepted at the
  meta level.

  `bench export-fixtures` writes fixtures to each app's `fixtures/`
  directory based on the `fixtures` list in that app's hooks.py. HRMS' hooks.py
  does NOT list 'Property Setter', so the export is silent (no output) and the
  PS only lives in the DB. Without a scripted recreate, the next env migration
  would silently lose the meta.options extension, breaking future CSV ingests.

This script:
  - Is idempotent (frappe.make_property_setter overwrites if exists).
  - Recreates the exact same Property Setter that the bulk-submit produced.
  - Can be invoked on any env (dev/qa/prod) with the same code path.
  - Logs before/after state for audit.

Usage:
  # Copy to container, then bench execute:
  docker cp recreate_property_setters.py erp-prod-backend-1:/tmp/
  docker exec erp-prod-backend-1 bash -c "cd /home/frappe/frappe-bench && \\
    bench --site pberpprod.duckdns.org execute /tmp/recreate_property_setters.py"

Why not Option 1 (custom app fixtures) or Option 3 (manual JSON):
  - PROD has no custom app on the bench (apps/ = {erpnext, frappe, hrms} only).
    Adding a new custom app just to host one fixture is overkill for this size.
  - apps/hrms/ is third-party custom code; SOUL NEVER rule #3 forbids editing
    it, including fixtures (would also fail on next `bench update`).
  - Manual JSON in workspace fixtures/ would require a parallel applier script
    anyway; this single script is cleaner.

Ref:
  - TRACKER.md Phase 3.6 (line 398-400 in current snapshot): "TODO before next
    env migration: bench --site pberpprod export-fixtures + commit Property Setter
    to fixtures."
  - LEARNINGS.md #104 (raw-SQL mandatory backfill), #105 (controller-level
    status check), #106 (3-run pattern).
"""
import json
import time
from datetime import datetime

import frappe


# Property Setter definition: (doctype, field_name, property, value)
#
# Source: Phase 3.6 bulk-submit, 2026-08-27 14:39 IST. Verified by inspecting
# tabProperty Setter on pberpprod: name='Attendance-status-options',
# value='\nPresent\nAbsent\nOn Leave\nHalf Day\nWork From Home\nHoliday\nWeekly Off'.
#
# Note: the value has a leading newline because Frappe stores select options
# newline-delimited and the original Property Setter was created with a
# newline prefix. We preserve that exact format to avoid spurious meta diffs.
PROPERTY_SETTERS = [
    {
        "doctype": "Attendance",
        "field_name": "status",
        "property": "options",
        "value": "\nPresent\nAbsent\nOn Leave\nHalf Day\nWork From Home\nHoliday\nWeekly Off",
        "property_type": "Text",
    },
]


def _existing_ps(doctype: str, field_name: str, property_name: str) -> dict | None:
    """Return the existing Property Setter (if any) for (doctype, field, property)."""
    return frappe.db.get_value(
        "Property Setter",
        {
            "doc_type": doctype,
            "field_name": field_name,
            "property": property_name,
        },
        ["name", "value"],
        as_dict=True,
    )


def _apply_ps(spec: dict) -> dict:
    """Apply a single Property Setter spec. Returns a result dict.

    `frappe.make_property_setter` is idempotent — it overwrites if exists,
    creating a new row keyed by (doctype, field, property).
    """
    before = _existing_ps(spec["doctype"], spec["field_name"], spec["property"])

    # frappe.make_property_setter signature (positional + keyword):
    #   make_property_setter(args, ignore_validate=False, validate_fields_for_doctype=True,
    #                        is_system_generated=True, *, module=None)
    # where `args` is a dict-like with keys: doctype, fieldname, property, value,
    # property_type, doctype_or_field (optional: defaults to "DocField" for field-level).
    # We use validate_fields_for_doctype=False to skip meta-validation since
    # Attendance.status is a real field but the validation can spuriously fail
    # during raw-SQL-insert workflows where the meta cache is stale.
    ps = frappe.make_property_setter(
        {
            "doctype": spec["doctype"],
            "fieldname": spec["field_name"],
            "property": spec["property"],
            "value": spec["value"],
            "property_type": spec.get("property_type", "Text"),
            "doctype_or_field": "DocField",  # field-level PS, not doctype-level
        },
        validate_fields_for_doctype=False,
    )

    after = _existing_ps(spec["doctype"], spec["field_name"], spec["property"])

    return {
        "doctype": spec["doctype"],
        "field_name": spec["field_name"],
        "property": spec["property"],
        "before": before,
        "after": after,
        "ps_doc": ps.name if ps else None,
    }


def run(dry_run: bool = False):
    """Apply all Property Setters. Idempotent — safe to run multiple times.

    Args:
        dry_run: If True, print what would be applied without writing.

    Returns:
        Structured result dict with per-PS before/after state.
    """
    started = time.time()
    print(f"=== recreate_property_setters.run started {datetime.utcnow().isoformat()}Z ===")
    print(f"dry_run = {dry_run}")
    print(f"site = {frappe.local.site}")
    print(f"app set = {frappe.get_installed_apps()}")
    print(f"property setters to apply: {len(PROPERTY_SETTERS)}")

    results = []

    for spec in PROPERTY_SETTERS:
        before = _existing_ps(spec["doctype"], spec["field_name"], spec["property"])
        print(
            f"\n[{spec['doctype']}.{spec['field_name']}.{spec['property']}] "
            f"before: {before}"
        )

        if dry_run:
            results.append({
                "spec": spec,
                "before": before,
                "after": "(dry-run skipped)",
                "would_change": before is None or before.get("value") != spec["value"],
            })
            continue

        try:
            result = _apply_ps(spec)
            print(f"  applied: name={result['ps_doc']}, after={result['after']}")
            results.append(result)
        except Exception as exc:
            err_str = f"{type(exc).__name__}: {exc}"
            print(f"  FAIL: {err_str}")
            results.append({"spec": spec, "error": err_str})

    if not dry_run:
        try:
            frappe.db.commit()
            print("\nDB commit OK")
        except Exception as exc:
            print(f"\nWARN: commit failed: {exc}")

    elapsed = time.time() - started
    print(f"\n=== recreate_property_setters.run complete in {elapsed:.2f}s ===")

    # Verify meta actually reflects the new options
    print("\nMeta verification:")
    for spec in PROPERTY_SETTERS:
        mf = frappe.get_meta(spec["doctype"]).get_field(spec["field_name"])
        print(f"  {spec['doctype']}.{spec['field_name']}.options = {mf.options!r}")

    return {
        "site": frappe.local.site,
        "dry_run": dry_run,
        "applied": len([r for r in results if "error" not in r]),
        "failed": len([r for r in results if "error" in r]),
        "results": results,
        "elapsed_sec": round(elapsed, 2),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    # Allow `python recreate_property_setters.py` direct execution (not via bench execute)
    # by treating no-arg as a default dry_run=False.
    import sys
    dry = "--dry-run" in sys.argv
    print(json.dumps(run(dry_run=dry), indent=2, default=str))
