# Shift Assignment — Intake Sheet

**DocType:** `Shift Assignment` (submittable)
**Module:** HR / Shift Management
**Required fields:** 4
**Optional fields:** 5+

> **Note:** Shift Assignment is typically auto-generated from Shift Schedule via "Create Shift Assignments" button. This sheet is for **bulk backfill of historical assignments** or **manual ad-hoc adjustments**.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `employee` | Employee | Link → Employee | Y | "EMP-0001" | must exist | – |
| `shift_type` | Shift Type | Link → Shift Type | Y | "Morning-8h" | must exist | – |
| `company` | Company | Link → Company | Y | "Haritha Hospitals Pvt Ltd" | auto-fetched from employee | Required even if auto-fetched |
| `start_date` | Start Date | Date | Y | "2026-09-01" | YYYY-MM-DD | Assignment start |
| `end_date` | End Date | Date | N | "2026-09-30" | YYYY-MM-DD, ≥start_date; blank = ongoing | Optional |
| `status` | Status | Select | N | "Active" | Active / Inactive | – |
| `shift_location` | Shift Location | Link → Shift Location | N | "Main Hospital - ICU" | must exist if set | – |
| `overtime_type` | Overtime Type | Link → Overtime Type | N | "" | must exist if set | For OT calculation |
| `shift_request` | Shift Request | Link → Shift Request | N | "" | must exist if set | Auto-linked when created from request |
| `shift_schedule_assignment` | Shift Schedule Assignment | Link | N | "" | must exist if set | When created from schedule |
| `docstatus` | Document Status | Int | Y | 1 | 0=Draft, 1=Submitted, 2=Cancelled | Submit to make active |

## Healthcare-specific fields

None required — Shift Location's `zone_type` (custom) provides healthcare context.

## Validation rules

- `end_date ≥ start_date` (or blank for ongoing).
- `status=Active` requires `docstatus=1` (submitted).
- Cannot overlap with another Active Shift Assignment for the same employee (Frappe validates on submit).

## Common client mistakes

- Leaving `docstatus=0` (Draft) — assignment won't activate auto-attendance.
- Overlapping assignments for the same employee — validation error on submit.
- Not specifying `company` — auto-fetch should work, but explicit is safer for Data Import.
- Importing without `status=Active` — assignments won't drive attendance.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Backfill historical rotations for payroll | **Yes** — import last 6–12 months for accurate OT calculations |
| Set up monthly rosters going forward | **No** — use Shift Schedule + auto-generation |
| Manual swap (A covers B's shift tomorrow) | **Yes** — one-off ad-hoc assignment |
| Bulk roster re-import after policy change | **Yes** — cancel old + import new |

## Backfill example

For a nurse (EMP-0001) who worked 8h-rotating in August 2026:
- 10 Morning shifts (1st–10th, every other day)
- 10 Evening shifts
- 11 Night shifts (incl. Sundays)

→ 31 separate Shift Assignment rows, alternating between Morning-8h / Evening-8h / Night-8h Shift Types.

> Tip: For large backfills (>500 rows), use a script that generates rows from a rotation pattern rather than manual CSV entry. See `haritha_hospital.scripts.generate_shift_assignments`.

## Migration notes (see `scripts/migrate_master_data.py`)

- **Employee ID remap by `employee_name` — GOTCHA #7.** The migration script builds `DEV_EMP_BY_NAME` once at the top of `run()` from the already-migrated dev-side Employees, then walks every Shift Assignment record and remaps `employee` from the prod ID to the dev ID using `employee_name` as the join key. Client-side: every row in your CSV MUST have a non-empty `employee_name` column — if blank, the script cannot resolve the dev-side `employee` and the row fails with `LinkValidationError`.
- **`shift_schedule_assignment` is NULLIFIED — GOTCHA #9.** Every Shift Assignment has a `shift_schedule_assignment` Link field pointing at the `Shift Schedule Assignment` DocType, which is OUT OF SCOPE for this migration. The script explicitly sets `rec["shift_schedule_assignment"] = None` before insert. Client-side: leave the `shift_schedule_assignment` column blank in your CSV; any non-empty value will be discarded by the script.
- **`shift_request` Link is preserved.** The migration script migrates `Shift Request` BEFORE `Shift Assignment` (see `MIGRATION_ORDER`). As long as the source SR exists on the target site, the SR link is preserved. If the SR does NOT exist on the target site, the Link is dropped silently on insert (Frappe does not fail on missing optional Links at insert time for `docstatus=0` records).
- **`Shift Location` must exist — GOTCHA #9.** The migration script calls `_ensure_shift_location("Hyderabad")` once before processing any Shift Assignment record. This pre-creates a single canonical Shift Location with that name (production only uses one location). If your client uses a different canonical name, add that row to the `08_shift_location.csv` sheet AND edit `_ensure_shift_location()` in the script to match — otherwise every SA insert fails with `LinkValidationError: Shift Location "Hyderabad" not found`.
- **`docstatus` is set from source JSON.** The migration script preserves the source `docstatus` value (0 = Draft, 1 = Submitted, 2 = Cancelled). To migrate cancelled SA records alongside active ones, include them with `docstatus=2`.
- **Upsert by `name`.** The script upserts by document `name` (e.g., `HR-SHA-26-08-05318`). Re-runs UPDATE existing SA rows in place — date overlaps and Shift Type changes overwrite the live record, which immediately affects attendance.
