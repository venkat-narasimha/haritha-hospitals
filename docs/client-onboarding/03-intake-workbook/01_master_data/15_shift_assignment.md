# Shift Assignment — Intake Sheet

**DocType:** Shift Assignment (submittable)
**Module:** HR / Shift Management
**Required fields:** 6 (`name`, `employee`, `employee_name`, `shift_type`, `company`, `start_date`)
**Optional fields:** 7+

A Shift Assignment is a per-employee, per-shift, per-date-range scheduling record. Submittable DocType — Data Import creates as draft (`docstatus=0`) and clients submit via web UI to activate.

> **CRITICAL:** `Shift Assignment` has `autoname='prompt'` — the CSV MUST include a `name` column populated with a client-defined assignment code. **Also requires `employee_name`** — Frappe does not autogen it during Data Import for this DocType.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| name | Shift Assignment Name | Data | Y | SA-001 | unique | REQUIRED because autoname=prompt - see gotcha #8; client-defined SA code |
| employee | Employee | Link | Y | HR-EMP-001 | must exist | required stock field; remap by employee_name (gotcha #7) |
| employee_name | Employee Name | Data | Y | Employee A Sample | non-empty | REQUIRED for Data Import to fill autogen display field |
| shift_type | Shift Type | Link | Y | T1 | must exist | required stock field |
| company | Company | Link | Y | Company A | must exist | required stock field |
| shift_request | Shift Request | Link | N |  | must exist if set | optional link to originating Shift Request |
| start_date | Start Date | Date | Y | 2026-09-01 | YYYY-MM-DD | required stock field |
| end_date | End Date | Date | N | 2026-09-15 | YYYY-MM-DD; >= start_date | optional; blank = open-ended assignment |
| status | Status | Select | N | Active | Active / Inactive | stock optional; defaults to Active |
| shift_location | Shift Location | Link | N | Site A | must exist if set | optional; pre-create Site A (gotcha #9, gotcha #15) |
| department | Department | Link | N | Department A | must exist if set | optional; derived from Employee |
| amended_from | Amended From | Link | N |  | must exist if set | for amendment workflow only |
| overtime_type | Overtime Type | Link | N |  | must exist if set | optional; only if shift allows overtime |

> **Field `shift_schedule_assignment` is intentionally OMITTED.** This field links to a DocType (`Shift Schedule Assignment`) that is out of P5 scope. The migration script NULLIFIES it on every SA before upsert. See research §8 Q5.

## Migration notes (from research §7)

- **Gotcha #8 — `autoname='prompt'`:** CSV MUST include a `name` column. Without it, every row fails with `Please set the document name`.
- **Gotcha #9 — two out-of-scope Link fields:** (a) `shift_location` defaults to `Site A` (single-site deployments). (b) `shift_schedule_assignment` is OMITTED from this template entirely (out of scope).
- **Gotcha #7 — Employee ID remap:** Prod and dev Employee IDs do not align. The migration script remaps the `employee` Link by `employee_name`. **Clients should fill `employee_name` exactly as it appears on the Employee record.**
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Shift Assignment", ...}` before constructing the document.
- **Submittable DocType:** Data Import creates records at `docstatus=0` (draft). Clients must submit via web UI to activate the assignment for roster display.
- Shift Assignment has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.

## Healthcare-specific fields

None. Shift Assignment has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Shift Assignment template? |
|---|---|
| Initial roster setup (every employee × every week) | YES — one row per assignment slot |
| Adding a one-off shift swap | YES — append row |
| Long-running weekly pattern | NO — use Shift Schedule template instead |
| Bulk retro-assignments (backfill last 6 months) | YES — one row per week |

## Common client mistakes

- Omitting the `name` column — **CRITICAL**: every row fails.
- Omitting `employee_name` — `name` is set but display field stays blank; many list views break.
- Setting `end_date < start_date` — fails Date Range validation.
- Linking to a `Shift Type` that does not exist — fails LinkValidationError. Import Shift Types first.
- Linking to a `Shift Location` that does not exist — fails LinkValidationError. Import Shift Locations first (or leave blank).
- Importing at `docstatus=0` and assuming the assignment is active — clients must submit via web UI.
- Setting `status = Inactive` on initial import — those rows are hidden from roster views.
- Putting `employee` as the employee's numeric ID without `employee_name` matching — LinkValidationError on remap.

## Related

- **Employee** template (must import first).
- **Shift Type** template (must import first).
- **Shift Location** template (must import first if `shift_location` is populated).
- **Shift Request** template (optional; `shift_request` Link is rare).
