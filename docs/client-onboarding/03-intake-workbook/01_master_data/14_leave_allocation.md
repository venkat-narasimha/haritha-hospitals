# Leave Allocation — Intake Sheet

**DocType:** Leave Allocation (submittable)
**Module:** HR / Leaves
**Required fields:** 7 (`naming_series`, `employee`, `leave_type`, `from_date`, `to_date`, `total_leaves_allocated`, `company`)
**Optional fields:** 11+

A Leave Allocation grants a specific number of leaves of a specific Leave Type to a specific Employee over a specific date range. Submittable DocType — Data Import will create as draft (`docstatus=0`) and clients submit via web UI to trigger ledger entries.

> **Production note:** Single-site deployments typically have 0 Leave Allocations. Template exists for forward-compatibility when leave transactions begin.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| naming_series | Series | Select | Y | HR-LAL-.YYYY.- | HR-LAL-.YYYY.- | required stock field; submittable DocType |
| employee | Employee | Link→Employee | Y | HR-EMP-001 | must exist | required stock field |
| employee_name | Employee Name | Data | N | Employee A Sample | autogen if blank | autogen from Employee record |
| leave_type | Leave Type | Link→Leave Type | Y | Casual Leave | must exist | required stock field |
| from_date | From Date | Date | Y | 2026-09-01 | YYYY-MM-DD | allocation start (inclusive) |
| to_date | To Date | Date | Y | 2027-08-31 | YYYY-MM-DD; >= from_date | allocation end (inclusive) |
| new_leaves_allocated | New Leaves Allocated | Float | N | 12 | >= 0 | leaves granted this allocation |
| carry_forward | Add unused leaves from previous allocations | Check | N | 0 | 0/1 | 1 to roll forward unused leaves |
| unused_leaves | Unused leaves | Float | N | 0 | >= 0 | from previous period |
| total_leaves_allocated | Total Leaves Allocated | Float | Y | 12 | >= 0 | required stock field (sum of new + carried) |
| total_leaves_encashed | Total Leaves Encashed | Float | N | 0 | >= 0 | encashed portion (read-only on submit) |
| carry_forwarded_leaves_count | Carry Forwarded Leaves | Float | N | 0 | >= 0 | read-only; derived from carry_forward |
| leave_period | Leave Period | Link→Leave Period | N | Period A | must exist if set | optional link to Leave Period |
| leave_policy | Leave Policy | Link→Leave Policy | N | Standard Policy | must exist if set | optional link to Leave Policy |
| expired | Expired | Check | N | 0 | 0/1 | 1 once allocation window has closed |
| description | Description | Small Text | N |  | <= 140 chars | free-text note |
| company | Company | Link→Company | Y | Company A | must exist | required stock field |

## Migration notes (from research §7)

- **Gotcha #14 — leave module is configured but unpopulated:** 0 Leave Allocations at single-site deployments. Template exists for forward-compatibility.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Leave Allocation", ...}` before constructing the document.
- **Submittable DocType:** Data Import creates records at `docstatus=0` (draft). Clients must submit via web UI to trigger the Leave Ledger Entry creation that powers the leave balance calculations. CSV import alone does not generate ledger entries.
- Leave Allocation has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.

## Healthcare-specific fields

None. Leave Allocation has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Leave Allocation template? |
|---|---|
| Initial leave grant at start of period | YES — one row per (Employee × Leave Type) |
| Mid-year adjustment (additional grant) | YES — append row |
| Carry-forward from previous period | YES — set `carry_forward=1` + `unused_leaves` value |
| Encashment on exit | YES — set `total_leaves_encashed` and submit |

## Common client mistakes

- Setting `total_leaves_allocated` to a value different from `new_leaves_allocated + carry_forwarded_leaves_count` — validation error.
- Omitting `naming_series` — fails required check.
- Linking to an Employee that does not exist — fails LinkValidationError.
- Setting `from_date > to_date` — fails Date Range validation.
- Importing at `docstatus=0` and assuming the allocation is active — clients must submit via web UI for ledger entries to be created.
- Setting `carry_forward=1` but leaving `unused_leaves=0` — carry-forward is a no-op.
- Linking to a `Leave Period` / `Leave Policy` that does not exist — fails LinkValidationError.

## Related

- **Employee** template (must import first).
- **Leave Type** template (must import first).
- **Leave Period** / **Leave Policy** templates (optional imports).
- **Leave Application** consumes allocations; **Leave Ledger Entry** is system-generated on submit.
