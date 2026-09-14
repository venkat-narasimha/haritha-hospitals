# Attendance — Intake Sheet

**DocType:** `Attendance` (submittable)
**Module:** HR / Attendance
**Required fields:** 5
**Optional fields:** 10+

> **Note:** Attendance is typically auto-generated from Employee Checkin via the HRMS Attendance scheduler. This sheet is for **manual entry**, **corrections**, and **bulk backfill of historical records** (e.g., when integrating with a legacy biometric system that pre-dates the target site's go-live).

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `employee` | Employee | Link → Employee | Y | "EMP-A001" | must exist | – |
| `employee_name` | Employee Name | Data | Y | "Employee A" | non-empty | Join key for prod → dev ID remap |
| `attendance_date` | Attendance Date | Date | Y | "2025-09-01" | YYYY-MM-DD | One record per employee per day |
| `status` | Status | Select | Y | "Present" | Present / Absent / Half Day / On Leave / Work From Home | – |
| `company` | Company | Link → Company | Y | "Company A" | must exist | – |
| `department` | Department | Link → Department | N | "Department A" | must exist if set | Auto-fetched from Employee |
| `shift` | Shift | Link → Shift Type | N | "Shift Type A" | must exist if set | Defaults from Employee.default_shift |
| `leave_type` | Leave Type | Link → Leave Type | N | "Leave Type A" | must exist if status=On Leave | Required when status=On Leave |
| `leave_application` | Leave Application | Link → Leave Application | N | "LAP-26-09-00001" | must exist if set | Traceability link to the originating request |
| `in_time` | In Time | Datetime | N | "2025-09-01 09:00:00" | YYYY-MM-DD HH:MM:SS | 24h clock |
| `out_time` | Out Time | Datetime | N | "2025-09-01 18:00:00" | YYYY-MM-DD HH:MM:SS | 24h clock |
| `working_hours` | Working Hours | Float | N | 9.0 | ≥0 | Auto-computed from in_time/out_time |
| `late_entry` | Late Entry | Check | N | 0 | 0/1 | Derived from shift grace period |
| `early_exit` | Early Exit | Check | N | 0 | 0/1 | Derived from shift grace period |
| `docstatus` | Document Status | Int | Y | 1 | 0=Draft, 1=Submitted, 2=Cancelled | Submit to drive payroll |

## Healthcare-specific fields

None required — Shift Type and Shift Location provide hospital context (e.g., `zone_type="ICU"` for clinical staff).

## Validation rules

- One Attendance record per (employee, attendance_date) tuple — Frappe rejects duplicates.
- `status=Present` requires `in_time` populated for shift-bound employees (Frappe validates per Shift Type settings).
- `status=On Leave` requires `leave_type` populated.
- `status=Half Day` requires either `in_time`/`out_time` populated or `working_hours < shift.working_hours_threshold_for_half_day`.
- `docstatus=1` (Submitted) is required for the record to count toward payroll and the leave ledger.

## Common client mistakes

- Leaving `docstatus=0` (Draft) — Attendance won't drive payroll or the leave ledger.
- Setting `status=Present` without `in_time` for shift-bound employees — validation error on submit.
- Setting `status=On Leave` without `leave_type` — validation error.
- Creating Attendance for an employee on a Holiday List date — should be skipped (auto-handled by the scheduler).
- Backfilling Attendance that overlaps with approved Leave Application records — leads to duplicate leave ledger entries.
- Forgetting `company` — auto-fetch should work, but explicit is safer for Data Import.
- Setting `working_hours` manually that contradicts `in_time`/`out_time` — Frappe recomputes on save.
- Importing with a date in the future — Frappe allows but flags it; check `attendance_date ≤ today`.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Daily biometric-driven auto-attendance | **No** — use Employee Checkin + HRMS Attendance scheduler |
| Manual entry for missed punches | **Yes** — one-off correction |
| Backfill historical attendance from legacy system | **Yes** — bulk import for payroll integrity |
| Bulk marking (e.g., all-staff WFH day) | **Yes** — script-based mass update |
| Re-import after attendance policy change | **Yes** — cancel old + re-import new |

## Migration notes (post-go-live upload)

- **Employee ID remap by `employee_name`.** Production and dev Employee IDs do NOT align post-migration. The upload script remaps the `employee` field on every Attendance record using `employee_name` as the join key (mirrors GOTCHA #7 from `scripts/migrate_master_data.py`). Client CSV MUST supply both `employee` (original, will be remapped) and `employee_name` (the join key).
- **`status=Present` requires `in_time` for shift-bound employees.** When the employee has a Shift Type with `enable_auto_attendance=1`, leaving `in_time` blank triggers `ValidationError` on submit. Either populate `in_time`/`out_time` OR set `status=On Leave` / `Absent` for the day.
- **`status=On Leave` requires `leave_type`.** The Attendance scheduler links the Attendance record back to the Leave Application via `leave_application`. If `leave_application` is not set, the leave ledger entry will still create — but the link to the originating leave request is lost, breaking traceability.
- **`docstatus=1` is mandatory for payroll.** Draft (`docstatus=0`) Attendance records do NOT contribute to Salary Slip generation. Confirm all bulk-imported rows have `docstatus=1` before the next payroll run.
- **Duplicate guard.** The upload script silently skips Attendance rows whose (employee, attendance_date) already exists on the target site (Frappe unique constraint). For corrections, cancel the existing record first then re-import with the new values.

## Related

- **DocType:** `Attendance` — Frappe HR v16.5.0 stock controller
- **Upstream:** `tabEmployee Checkin` (auto-attendance scheduler)
- **Downstream:** `tabLeave Ledger Entry` (creates Application row on status=On Leave)
- **Related template:** `10_employee.csv` (Employee master), `15_shift_assignment.csv` (Shift Assignment master)
- **File location:** `docs/client-onboarding/03-intake-workbook/01_master_data/16_attendance.csv`
- **Upload script:** TBD — Wave 4 will add `scripts/upload_attendance.py`
