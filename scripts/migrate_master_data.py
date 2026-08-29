"""
Haritha Hospitals — Master Data Migration Script
==================================================

Migrates Company + reference data + Employee + Item master records +
HR scheduling masters (Shift Schedule / Shift Assignment / Shift Request)
from the production source site (pberpprod) into the dev target site
(pberpdev).

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
4.  ``Department``        (skip ``All Departments`` root; also pre-seeded with
                            ``Department Approver`` rows for the Shift Request
                            approver check — see GOTCHA #10)
5.  ``Designation``
6.  ``Item Group``        (skip ``All Item Groups`` root)
7.  ``UOM``
8.  ``Gender``
9.  ``Employment Type``
10. ``Shift Type``        (autoname='prompt' → set ``name`` explicitly)
11. ``Shift Location``    (created with autoname=field:location_name, name
                            pinned explicitly — see GOTCHA #8)
12. ``Holiday List``
13. ``Employee``          (depends on Dept/Designation/Gender/Default Shift)
14. ``Item``              (depends on Item Group/UOM)
15. ``Shift Request``     (must come before Shift Assignment because one
                            SA record links back to a Shift Request — see
                            GOTCHA #9. Employee ID is remapped by
                            ``employee_name`` because prod / dev employee
                            IDs differ — see GOTCHA #7)
16. ``Shift Schedule``    (autoname='prompt' + a ``repeat_on_days`` child
                            table that is dropped from ``fields=["*"]`` list
                            payloads; re-fetch each record individually if
                            the source JSON is empty — see GOTCHA #8)
17. ``Shift Assignment``  (remaps employee ID, NULLIFIES the
                            ``shift_schedule_assignment`` link because
                            the Shift Schedule Assignment DocType is out
                            of scope — see GOTCHA #9)

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

7.  Prod and dev Employee IDs do not align.
    Production Employee records use IDs starting ``HR-EMP-00211`` while
    the dev site (after the Employee migration) uses ``HR-EMP-00002`` ….
    The ``employee_name`` is preserved across sites, so Link fields
    (``employee``, ``approver`` user lookups) must be remapped by
    ``employee_name`` before insert/update.
    *Fix:* build ``DEV_EMP_BY_NAME = {e.employee_name: e.name}`` once
    inside ``run()`` and substitute the ``employee`` value of every
    Shift Assignment / Shift Request record with the dev ID before
    upserting.

8.  Shift Schedule needs ``repeat_on_days`` child table + an explicit
    ``name``.
    ``/api/resource/<DocType>?fields=["*"]`` returns child-table rows
    stripped out (Frappe list-view optimisation). Plain
    ``frappe.get_doc(payload).insert()`` then throws
    ``Please set the document name`` because the controller declares
    ``autoname = 'prompt'``.
    *Fix:* when listing Shift Schedule, fetch each record individually
    via ``/api/resource/Shift Schedule/<name>`` to pull the child rows
    in. On insert, set ``payload["name"] = rec["name"]`` so the prompt
    autoname contract is satisfied.

9.  Shift Assignment has two out-of-scope Link fields.
    Every SA references a ``Shift Location`` (``Hyderabad`` is the only
    one used in production) and a ``Shift Schedule Assignment`` (420
    unique SSA records). SSA records are deliberately NOT migrated in
    this script.
    *Fix:* pre-create ``Shift Location "Hyderabad"`` (autoname=field)
    and NULLIFY ``shift_schedule_assignment`` on every SA record before
    upsert. One SA (``HR-SHA-26-08-05318``) also links to a Shift
    Request — to keep that one green, ``Shift Request`` must be migrated
    BEFORE ``Shift Assignment`` in ``MIGRATION_ORDER``.

10. Shift Request ``validate_approver()`` is unconditional.
    ``ShiftRequest.validate()`` runs ``validate_approver()`` regardless
    of ``docstatus``. The check requires the record's ``approver`` to
    appear in the department's ``shift_request_approver`` list. The
    production records have ``approver="Administrator"`` but the dev
    site's Department Approver rows are empty, so a naive insert raises
    ``Only Approvers can Approve this Request.``.
    *Fix:* for every department referenced by the source JSON, add a
    ``Department Approver`` child row with ``approver="Administrator"``
    and ``parentfield="shift_request_approver"`` BEFORE inserting the
    Shift Request records. Then insert each SR with
    ``docstatus=0, status="Draft"`` (bypasses workflow) and use
    ``frappe.db.set_value(..., update_modified=False)`` to promote the
    record to its source ``docstatus``/``status`` without re-running
    ``validate()``.

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
PROMPT_AUTONAME_DOCTYPES = {"Shift Type", "Shift Location", "Shift Schedule"}

#: Fields never to replay — managed by Frappe / metadata-only.
SKIP_FIELDS = {
    "name", "creation", "modified", "owner", "modified_by", "idx",
    "docstatus", "_user_tags", "_comments", "_assign", "_liked_by", "_seen",
    # Tree bookkeeping fields — Frappe recomputes these from parent links.
    "lft", "rgt", "old_parent",
}

#: DocTypes handled by a dedicated migration function instead of the
#: default ``upsert`` path (see ``_migrate_shift_*`` below).
SHIFT_LINK_DOCTYPES = {"Shift Assignment", "Shift Request", "Shift Schedule"}

#: Migration order. Order matters: dependencies first, dependents last.
#: ``Shift Request`` is intentionally placed BEFORE ``Shift Assignment``
#: because one SA references an SR (GOTCHA #9).
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
    "Shift Location",
    "Holiday List",
    "Employee",
    "Item",
    "Shift Request",
    "Shift Schedule",
    "Shift Assignment",
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
# Shift scheduling migrations
# ---------------------------------------------------------------------------

def _ensure_shift_location(location_name):
    """Idempotently create the named ``Shift Location``.

    See GOTCHA #9 — every prod Shift Assignment carries
    ``shift_location="Hyderabad"`` and dev has no Shift Location records
    on a clean install.
    """
    if frappe.db.exists("Shift Location", location_name):
        return False
    doc = frappe.get_doc(
        {
            "doctype": "Shift Location",
            "name": location_name,
            "location_name": location_name,
        }
    )
    doc.insert(ignore_permissions=True)
    print(f"  created Shift Location: {location_name}", flush=True)
    return True


def _ensure_department_approvers(records):
    """Add a Department Approver row for every department referenced by
    ``records`` so Shift Request ``validate_approver()`` passes.

    See GOTCHA #10. Adds ``approver="Administrator"`` with
    ``parentfield="shift_request_approver"`` and is idempotent.
    """
    departments = {r.get("department") for r in records if r.get("department")}
    added = 0
    for dept in departments:
        if not frappe.db.exists(
            "Department Approver",
            {
                "parent": dept,
                "parentfield": "shift_request_approver",
                "approver": "Administrator",
            },
        ):
            frappe.get_doc(
                {
                    "doctype": "Department Approver",
                    "parent": dept,
                    "parenttype": "Department",
                    "parentfield": "shift_request_approver",
                    "approver": "Administrator",
                }
            ).insert(ignore_permissions=True)
            added += 1
    if added:
        print(f"  added {added} Department Approver rows", flush=True)


def _migrate_shift_schedule(rec):
    """Upsert a single Shift Schedule — see GOTCHA #8.

    Two implementation details matter here:

    1.  ``frappe.get_doc(payload).insert()`` silently drops child-table
        rows when the child rows carry ``docstatus=1`` while the parent
        is inserted at ``docstatus=0`` (the ORM filters child rows by
        parent docstatus).  We therefore **append the child rows
        programmatically** via ``doc.append()`` instead of relying on
        them being present in the constructor dict.
    2.  The controller declares ``autoname='prompt'`` so the parent
        ``name`` must be pinned on insert (handled by the upsert path).
    """
    name = rec["name"]
    child_rows = rec.get("repeat_on_days") or []

    if frappe.db.exists("Shift Schedule", name):
        doc = frappe.get_doc("Shift Schedule", name)
        # Wipe existing child rows so we don't accumulate duplicates on
        # re-runs.
        doc.set("repeat_on_days", [])
        for d in child_rows:
            doc.append(
                "repeat_on_days",
                {"day": d.get("day"), "idx": d.get("idx")},
            )
        doc.save()
        return "updated"

    new_payload = {"doctype": "Shift Schedule", "name": name}
    new_payload.update(_clean_payload("Shift Schedule", rec))
    new_payload["repeat_on_days"] = []
    doc = frappe.get_doc(new_payload)
    for d in child_rows:
        doc.append(
            "repeat_on_days",
            {"day": d.get("day"), "idx": d.get("idx")},
        )
    doc.insert()
    return "inserted"


def _migrate_shift_request(rec, dev_emp_by_name):
    """Upsert a single Shift Request — see GOTCHA #10.

    Inserts as ``docstatus=0, status="Draft"`` to skip
    ``validate_approver`` (the Department Approver pre-seed handles the
    actual approver lookup), then promotes the record to its source
    ``docstatus``/``status`` via ``frappe.db.set_value`` to bypass
    validation entirely.
    """
    name = rec["name"]
    rec = dict(rec)  # do not mutate caller's dict
    ename = rec.get("employee_name")
    if ename in dev_emp_by_name:
        rec["employee"] = dev_emp_by_name[ename]

    orig_docstatus = rec.pop("docstatus", 0)
    orig_status = rec.get("status")

    payload = _clean_payload("Shift Request", rec)
    payload["docstatus"] = 0
    payload["status"] = "Draft"

    if frappe.db.exists("Shift Request", name):
        doc = frappe.get_doc("Shift Request", name)
        doc.update(payload)
        doc.save()
    else:
        np = {"doctype": "Shift Request"}
        np.update(payload)
        np["name"] = name
        frappe.get_doc(np).insert()

    # Promote to the source's final state without re-running validate().
    frappe.db.set_value(
        "Shift Request",
        name,
        {"docstatus": orig_docstatus, "status": orig_status},
        update_modified=False,
    )
    return "inserted"


def _migrate_shift_assignment(rec, dev_emp_by_name):
    """Upsert a single Shift Assignment — see GOTCHAs #7 and #9.

    Remaps ``employee`` by ``employee_name`` (GOTCHA #7) and NULLIFIES
    the ``shift_schedule_assignment`` link (GOTCHA #9, SSA is out of
    scope).
    """
    name = rec["name"]
    rec = dict(rec)
    ename = rec.get("employee_name")
    if ename in dev_emp_by_name:
        rec["employee"] = dev_emp_by_name[ename]
    rec["shift_schedule_assignment"] = None  # GOTCHA #9

    payload = _clean_payload("Shift Assignment", rec)
    if frappe.db.exists("Shift Assignment", name):
        doc = frappe.get_doc("Shift Assignment", name)
        doc.update(payload)
        doc.save()
        return "updated"
    np = {"doctype": "Shift Assignment"}
    np.update(payload)
    frappe.get_doc(np).insert()
    return "inserted"


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

    # Build the dev employee_name → id map once (GOTCHA #7).
    dev_emp_by_name = {
        e.employee_name: e.name
        for e in frappe.get_all(
            "Employee",
            filters={"company": "Haritha Hospitals"},
            fields=["name", "employee_name"],
        )
        if e.employee_name
    }
    print(f"  indexed {len(dev_emp_by_name)} Haritha Hospitals employees", flush=True)

    # Pre-create Shift Location "Hyderabad" before processing any Shift
    # Assignment (GOTCHA #9).
    if "Shift Assignment" in MIGRATION_ORDER:
        _ensure_shift_location("Hyderabad")
        frappe.db.commit()

    results = {}

    for dt in MIGRATION_ORDER:
        print(f"\nPROCESSING {dt}", flush=True)
        records = _load_records(dt)
        if not records:
            results[dt] = {"inserted": 0, "updated": 0, "failed": 0, "errors_sample": []}
            continue
        print(f"  loaded {len(records)} records", flush=True)

        # Pre-seed Department Approver rows for Shift Request (GOTCHA #10).
        if dt == "Shift Request":
            _ensure_department_approvers(records)
            frappe.db.commit()

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
                elif dt == "Shift Schedule":
                    # GOTCHA #8 — autoname=prompt + repeat_on_days child
                    # table. Source JSON must already include the child rows.
                    outcome = _migrate_shift_schedule(rec)
                elif dt == "Shift Request":
                    # GOTCHA #10 — insert as Draft, then promote.
                    outcome = _migrate_shift_request(rec, dev_emp_by_name)
                elif dt == "Shift Assignment":
                    # GOTCHA #7 + #9 — remap employee, NULLIFY SSA link.
                    outcome = _migrate_shift_assignment(rec, dev_emp_by_name)
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
