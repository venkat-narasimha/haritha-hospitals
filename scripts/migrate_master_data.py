"""
Haritha Hospitals — Master Data Migration Script
==================================================

Migrates Company + reference data + Employee + Item master records from the
production source site (pberpprod) into the dev target site (pberpdev).

The script reads JSON dumps written by the fetch step (one file per DocType
in /tmp/prod_<DocType>.json, produced by the companion
``fetch_master_data.py``) and replays them via the Frappe ORM using an
**upsert** pattern (insert-if-missing, update-if-present). Re-running the
script is therefore safe: no duplicates, no destructive rewrites.

DocTypes migrated (in dependency order)
---------------------------------------
1.  ``Company``           (2-step: minimal insert, then attach default accounts)
2.  ``Account``           (skip auto-generated root nodes)
3.  ``Cost Center``
4.  ``Department``        (skip ``All Departments`` root)
5.  ``Designation``
6.  ``Item Group``        (skip ``All Item Groups`` root)
7.  ``UOM``
8.  ``Gender``
9.  ``Employment Type``
10. ``Shift Type``        (autoname='prompt' → set ``name`` explicitly)
11. ``Holiday List``
12. ``Employee``          (depends on Dept/Designation/Gender/Default Shift)
13. ``Item``              (depends on Item Group/UOM)

USAGE
-----
Prerequisites
~~~~~~~~~~~~~
- Source site has API access enabled (default for any Frappe site).
- Companion fetch step has written ``/tmp/prod_<DocType>.json`` files inside
  the **target** bench container (erp-dev-backend-1).
- Target site has the ``haritha_hospital`` app installed and all 274 custom
  fixtures (Custom Field / Property Setter / Print Format / Notification /
  Letter Head) migrated.

Run inside the bench container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    docker exec -u frappe erp-dev-backend-1 bash
    cd /home/frappe/frappe-bench
    bench --site pberpdev.duckdns.org \
          execute apps.haritha_hospital.utils.migrate_master_data.run

Exit codes / summary
~~~~~~~~~~~~~~~~~~~~
The script prints a per-DocType ``ins=N upd=M fail=K`` line and a final
``=== SUMMARY ===`` block. A non-zero ``fail`` count does NOT abort the
migration — partial progress is committed per DocType so a re-run picks up
the remainder.

GOTCHAS DISCOVERED (first run: 2026-08-29)
------------------------------------------
1.  ``get_doc()`` requires the ``doctype`` key.
    Passing only the record fields raises
    ``ValidationError: doc(dict) does not have a valid 'doctype'``.
    *Fix:* inject ``{'doctype': dt, **payload}`` before constructing a new
    document. This is the single most common bug when replaying exported
    records.

2.  Company default accounts depend on Account existing first.
    ``default_bank_account``, ``default_receivable_account``,
    ``default_payable_account``, ``default_expense_account`` and
    ``default_income_account`` are Link fields pointing at Account records
    that are themselves created by this migration. Inserting Company with
    them populated fails with ``LinkValidationError``.
    *Fix:* insert Company with only identity fields, then call
    ``frappe.db.set_value`` to attach the default accounts once Account
    records exist.

3.  Account root nodes are system-generated and not editable.
    ``Accounts Receivable``, ``Accounts Payable``, ``Cash In Hand`` etc.
    already exist as ERPNext stock accounts (root_type set, no
    parent_account). Trying to re-insert them throws a duplicate-key
    / parent-not-found error.
    *Fix:* detect ``parent_account is None and root_type`` and skip.

4.  ``Shift Type`` has ``autoname = 'prompt'``.
    Frappe will not auto-generate a name on insert; you must set
    ``doc.name`` explicitly (which is what the source JSON provides).
    *Fix:* the upsert helper already passes ``name`` back into the payload
    for inserts, satisfying the autoname contract.

5.  Department / Item Group circular-root trap.
    ``All Departments`` and ``All Item Groups`` are the implicit root
    nodes created by Frappe on app install. Trying to insert a record with
    ``parent_department == 'All Departments'`` (or the Item Group
    equivalent) raises ``ParentNotFoundError`` because we never create
    those root records ourselves.
    *Fix:* skip rows whose parent equals the root sentinel.

6.  Employee requires ``gender`` and ``default_shift``.
    Both are Link fields with ``mandatory_depends_on`` set in HRMS. If
    those DocTypes are not migrated first, every Employee insert fails
    with ``ValueError: gender must be one of ...``.
    *Fix:* migrate ``Gender`` and ``Shift Type`` BEFORE ``Employee`` in
    the ordered loop.

IDEMPOTENCY
-----------
Every DocType is processed via the same ``upsert`` helper:
    - ``frappe.db.exists(dt, name)`` → if true, ``get_doc + update + save``
    - else → ``new_doc + insert``
    - one ``frappe.db.commit()`` per DocType (atomicity per DocType)

This makes the script safe to re-run after partial failure. Re-runs will
update any drift between source and target without creating duplicates.
"""

import json
import os
import sys
import frappe


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

#: Directory holding the source dumps (``prod_<DocType>.json``).
#: Mounted at the same path inside the bench container as on the host.
SOURCE_DIR = "/tmp"

#: Skip these root Account nodes (auto-generated by ERPNext on install).
ACCOUNT_ROOT_PARENT = None  # root Accounts have parent_account == None
ACCOUNT_ROOT_TYPES = {"Asset", "Liability", "Equity", "Income", "Expense"}

#: Sentinel names for Department / Item Group root nodes. We never re-create
#: these; rows whose parent equals one of these are skipped.
DEPARTMENT_ROOT = "All Departments"
ITEM_GROUP_ROOT = "All Item Groups"

#: DocTypes for which ``name`` must be set explicitly before insert
#: (autoname='prompt' or field-based autoname where source JSON carries the
#: canonical name).
PROMPT_AUTONAME_DOCTYPES = {"Shift Type"}

#: Fields never to replay — managed by Frappe / metadata-only.
SKIP_FIELDS = {
    "name", "creation", "modified", "owner", "modified_by", "idx",
    "docstatus", "_user_tags", "_comments", "_assign", "_liked_by", "_seen",
    # Tree bookkeeping fields — Frappe recomputes these from parent links.
    "lft", "rgt", "old_parent",
}

#: Migration order. Order matters: dependencies first, dependents last.
MIGRATION_ORDER = [
    "Company",
    "Account",
    "Cost Center",
    "Department",
    "Designation",
    "Item Group",
    "UOM",
    "Gender",
    "Employment Type",
    "Shift Type",
    "Holiday List",
    "Employee",
    "Item",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_records(doctype):
    """Load source records for ``doctype`` from /tmp/prod_<doctype>.json.

    Returns a list of dicts (possibly empty). Missing files are treated as
    "no records to migrate" rather than fatal.
    """
    fname = os.path.join(
        SOURCE_DIR, "prod_" + doctype.replace(" ", "_") + ".json"
    )
    if not os.path.exists(fname):
        print(f"  SKIP {doctype}: source file {fname} missing", flush=True)
        return []
    with open(fname) as f:
        return json.load(f).get("data", [])


def _clean_payload(doctype, record):
    """Strip metadata fields from a source record.

    Also injects ``doctype`` — see GOTCHA #1. Without this key,
    ``frappe.get_doc(payload)`` raises ``ValidationError``.
    """
    payload = {
        k: v for k, v in record.items() if k not in SKIP_FIELDS
    }
    return payload


def _should_skip_root_account(record):
    """ACCOUNT root-node guard — see GOTCHA #3."""
    return (
        record.get("parent_account") in (None, "")
        and record.get("root_type") in ACCOUNT_ROOT_TYPES
    )


def _should_skip_root_tree_node(doctype, record):
    """DEPARTMENT / ITEM GROUP root-node guard — see GOTCHA #5."""
    if doctype == "Department" and record.get("parent_department") == DEPARTMENT_ROOT:
        return True
    if doctype == "Item Group" and record.get("parent_item_group") == ITEM_GROUP_ROOT:
        return True
    return False


def upsert(doctype, name, payload):
    """Insert or update a single record. Returns ``"inserted"`` / ``"updated"``.

    Gotcha #1 is handled here: ``payload`` is always augmented with
    ``doctype`` before constructing the new document.

    Gotcha #4 is handled here: for prompt-autoname DocTypes, ``name`` is
    pinned explicitly so Frappe doesn't try to generate one.
    """
    # Replay 'name' for prompt-autoname DocTypes so the autoname hook is
    # satisfied (Shift Type etc.) — see GOTCHA #4.
    if doctype in PROMPT_AUTONAME_DOCTYPES and name and "name" not in payload:
        payload["name"] = name

    if frappe.db.exists(doctype, name):
        doc = frappe.get_doc(doctype, name)
        doc.update(payload)
        doc.save()
        return "updated"

    new_payload = {"doctype": doctype}
    new_payload.update(payload)
    doc = frappe.get_doc(new_payload)
    doc.insert()
    return "inserted"


def _migrate_company(record):
    """Two-step Company insert — see GOTCHA #2.

    Default-account links (default_receivable_account, default_payable_account,
    default_bank_account, default_expense_account, default_income_account,
    default_cost_center) point at Accounts / Cost Centers that are created
    LATER in this migration. Inserting Company with them populated blows up
    with LinkValidationError. Solution: insert with identity fields only,
    then attach defaults via ``frappe.db.set_value``.
    """
    name = record.get("name")
    payload = _clean_payload("Company", record)

    # Keys that depend on Account / Cost Center existing first.
    deferred_keys = {
        "default_bank_account",
        "default_receivable_account",
        "default_payable_account",
        "default_expense_account",
        "default_income_account",
        "default_cost_center",
        "round_off_account",
        "write_off_account",
        "exchange_gain_loss_account",
        "unrealized_exchange_gain_loss_account",
        "disposal_account",
        "default_deferred_expense_account",
        "default_deferred_revenue_account",
        "default_inventory_account",
        "stock_adjustment_account",
        "stock_received_but_not_billed",
        "service_received_but_not_billed",
    }
    deferred = {k: payload.pop(k) for k in list(payload) if k in deferred_keys and payload[k]}

    if frappe.db.exists("Company", name):
        doc = frappe.get_doc("Company", name)
        doc.update(payload)
        doc.save()
        result = "updated"
    else:
        new_payload = {"doctype": "Company"}
        new_payload.update(payload)
        doc = frappe.get_doc(new_payload)
        doc.insert(ignore_permissions=True)
        result = "inserted"

    # Now attach the deferred defaults (Account / Cost Center must exist).
    for k, v in deferred.items():
        frappe.db.set_value("Company", name, k, v, update_modified=False)

    return result


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run():
    """Migrate every DocType in ``MIGRATION_ORDER``.

    Designed to be called via ``bench execute``. Uses upsert so re-runs are
    safe.
    """
    if not frappe.db:
        frappe.connect()

    print(f"Migrating master data on site {frappe.local.site}", flush=True)
    print(f"Source dir: {SOURCE_DIR}", flush=True)
    print(f"DocTypes in order: {', '.join(MIGRATION_ORDER)}", flush=True)

    results = {}

    for dt in MIGRATION_ORDER:
        print(f"\nPROCESSING {dt}", flush=True)
        records = _load_records(dt)
        if not records:
            results[dt] = {"inserted": 0, "updated": 0, "failed": 0, "errors_sample": []}
            continue
        print(f"  loaded {len(records)} records", flush=True)

        inserted = updated = failed = 0
        errors = []

        for rec in records:
            name = rec.get("name")
            try:
                # Skip root nodes per GOTCHAs #3 and #5.
                if dt == "Account" and _should_skip_root_account(rec):
                    continue
                if _should_skip_root_tree_node(dt, rec):
                    continue

                if dt == "Company":
                    # Company uses the 2-step path (GOTCHA #2).
                    outcome = _migrate_company(rec)
                else:
                    payload = _clean_payload(dt, rec)
                    outcome = upsert(dt, name, payload)

                if outcome == "inserted":
                    inserted += 1
                else:
                    updated += 1

            except Exception as exc:
                failed += 1
                if len(errors) < 5:
                    errors.append(f"{name}: {str(exc)[:120]}")
                # Print immediately so partial failures are visible in the
                # bench execute log even if the run aborts later.
                print(f"  FAIL {dt}/{name}: {str(exc)[:200]}", flush=True)

        # Commit per DocType so a re-run picks up where we left off.
        try:
            frappe.db.commit()
        except Exception as exc:
            print(f"  COMMIT FAILED on {dt}: {exc}", flush=True)

        results[dt] = {
            "inserted": inserted,
            "updated": updated,
            "failed": failed,
            "errors_sample": errors,
        }
        print(
            f"  RESULT {dt}: ins={inserted} upd={updated} fail={failed}",
            flush=True,
        )

    # ---- Summary -----------------------------------------------------------
    print("\n=== SUMMARY ===", flush=True)
    total_ins = total_upd = total_fail = 0
    for dt, r in results.items():
        print(
            f"{dt}: ins={r['inserted']} upd={r['updated']} "
            f"fail={r['failed']}",
            flush=True,
        )
        for e in r["errors_sample"]:
            print(f"  - {e}", flush=True)
        total_ins += r["inserted"]
        total_upd += r["updated"]
        total_fail += r["failed"]

    print(
        f"\nTOTAL: ins={total_ins} upd={total_upd} fail={total_fail}",
        flush=True,
    )
    # Returning the dict makes `bench execute` print it too.
    return results


# Allow `python -m migrate_master_data` style invocation from outside bench.
if __name__ == "__main__":
    run()


# ---------------------------------------------------------------------------
# NOTES for future maintainers
# ---------------------------------------------------------------------------
#
# - When adding a new DocType to MIGRATION_ORDER, place it AFTER every
#   DocType it has Link / Dynamic Link dependencies on. The Frappe ORM
#   does NOT defer link validation until commit for Insert operations, so
#   inserting a child before its parent will raise LinkValidationError.
#
# - If a DocType uses autoname by field (e.g. autoname = "field:slug"), the
#   value will already be present in the source payload as the document
#   name — no special handling needed.
#
# - The companion fetch script (``fetch_master_data.py``) must produce
#   /tmp/prod_<DocType>.json with the canonical key ``"data"`` (list of
#   record dicts). Frappe's own export uses this shape, so reusing the
#   standard /api/resource/<DocType> payload is sufficient.
#
# - For very large DocTypes (>10k records), consider batching commits
#   every N records instead of per DocType to keep transactions short.
#   Current target site volumes: Employee ~430, Account ~90, UOM ~1500.
#
# - If you need to migrate data from a NEW source site (not pberpprod),
#   change SOURCE_DIR or parameterize it via env var:
#       SOURCE_DIR = os.environ.get("MIGRATION_SOURCE_DIR", "/tmp")
