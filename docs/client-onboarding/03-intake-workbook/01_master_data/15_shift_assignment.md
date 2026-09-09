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
