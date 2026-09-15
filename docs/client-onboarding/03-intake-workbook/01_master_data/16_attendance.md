# Attendance — Intake Sheet

**DocType:** `Attendance` (submittable)
**Module:** HR / Attendance
**Autoname rule:** `naming_series` (Series: `HR-ATT-.YYYY.-`)
**Stock-required fields:** 5 (`naming_series`, `employee`, `status`, `attendance_date`, `company`)
**Stock-optional fields:** 17+
**Custom fields:** 0 (per `haritha_hospital/fixtures/custom_field.json` Section 1)

> **Note:** Attendance is typically auto-generated from Employee Checkin via the HRMS Attendance scheduler. This sheet is for **manual entry**, **corrections**, and **bulk backfill of historical records** (e.g., when integrating with a legacy biometric system that pre-dates the target site's go-live).

## Purpose

Records per-employee, per-day attendance status with optional time-stamp detail. Drives payroll (working hours), leave linkage (status=On Leave), and exception tracking (late_entry, early_exit). Submittable DocType — Data Import creates at `docstatus=0` and clients submit via web UI to make the record count toward payroll.

The `status` field's options are extended via a Property Setter on this DocType to add a leading blank option (Section 2): ` / Present / Absent / On Leave / Half Day / Work From Home /`.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `naming_series` | Series | Select | Y | `HR-ATT-.YYYY.-` | one of `HR-ATT-.YYYY.-` | required stock field; autoname series prefix (per Section 4) |
| `employee` | Employee | Link→Employee | Y | `EMP-A001` | must exist in tabEmployee | required stock field (per Section 4) |
| `employee_name` | Employee Name | Data | N | `Employee A` | non-empty | STOCK-optional; RECOMMENDED as join key for prod→dev ID remap (GOTCHA #7) |
| `attendance_date` | Attendance Date | Date | Y | `2025-09-01` | YYYY-MM-DD | required stock field; one record per (employee, attendance_date) |
| `status` | Status | Select | Y | `Present` | Present / Absent / On Leave / Half Day / Work From Home | required stock field; options EXTENDED via Property Setter (per Section 2: leading blank option included) |
| `company` | Company | Link→Company | Y | `Company A` | must exist in tabCompany | required stock field |
| `department` | Department | Link→Department | N | `Department A` | must exist if set | stock-optional; auto-fetched from Employee record |
| `shift` | Shift | Link→Shift Type | N | `Shift Type A` | must exist if set | stock-optional; defaults from Employee.default_shift (per Section 4) |
| `leave_type` | Leave Type | Link→Leave Type | N | `Leave Type A` | must exist if status=On Leave | Y* — required when status=On Leave |
| `leave_application` | Leave Application | Link→Leave Application | N | `LAP-26-09-00001` | must exist if set | stock-optional; back-link to the originating Leave Application (traceability) |
| `attendance_request` | Attendance Request | Link→Attendance Request | N | `AR-26-09-00001` | must exist if set | stock-optional; back-link when employee self-corrects via Attendance Request workflow |
| `amended_from` | Amended From | Link→Attendance | N | `HR-ATT-26-09-00001` | must exist if set | stock-optional; for amendment workflow only |
| `in_time` | In Time | Datetime | N | `2025-09-01 09:00:00` | YYYY-MM-DD HH:MM:SS | stock-optional; Y* effectively for status=Present with shift-bound employee |
| `out_time` | Out Time | Datetime | N | `2025-09-01 18:00:00` | YYYY-MM-DD HH:MM:SS | stock-optional; Y* effectively for status=Present with shift-bound employee |
| `working_hours` | Working Hours | Float | N | `9.0` | ≥0 | stock-optional; auto-computed from in_time/out_time on submit |
| `late_entry` | Late Entry | Check | N | `0` | 0/1 | stock-optional; derived from shift grace period (Shift Type.enable_late_entry_marking) |
| `early_exit` | Early Exit | Check | N | `0` | 0/1 | stock-optional; derived from shift grace period (Shift Type.enable_early_exit_marking) |
| `half_day_status` | Status for Other Half | Select | N | `Present` | /Present/Absent | stock-optional; only used when status=Half Day (e.g. first half Absent, second half Present) |
| `modify_half_day_status` | Modify Half Day Status | Check | N | `0` | 0/1 | stock-optional; UI flag to confirm the user intends to override the other-half status |
| `standard_working_hours` | Standard Working Hours | Float | N | `8.0` | ≥0 | stock-optional; defaults to Shift Type.working_hours_calculation_based_on basis |
| `overtime_type` | Overtime Type | Link→Overtime Type | N | `Overtime Type A` | must exist if set | stock-optional; required only if Shift Type.allow_overtime=1 and overtime > 0 |
| `actual_overtime_duration` | Actual Overtime Duration | Float | N | `0.0` | ≥0 | stock-optional; computed when overtime_type populated (hours) |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Attendance", ...}` before constructing the document.
- **Gotcha #14 — leave module unpopulated at go-live.** Single-site deployments typically have 0 Leave Applications and 0 Leave Allocations. Attendance records with `status=On Leave` will fail validation if a matching `Leave Application` does not exist. Import Leave Applications first, then Attendance.
- **Gotcha #7 — Employee ID remap by `employee_name`.** Production and dev Employee IDs do NOT align post-migration. The upload script remaps the `employee` field on every Attendance record using `employee_name` as the join key. Client CSV MUST supply both `employee` (original, will be remapped) and `employee_name` (the join key), even though `employee_name` is stock-optional.
- **`status=Present` requires `in_time`/`out_time` for shift-bound employees.** When the employee has a Shift Type with `enable_auto_attendance=1`, leaving `in_time` blank triggers a `ValidationError` on submit. Either populate `in_time`/`out_time` OR set `status=On Leave` / `Absent` for the day.
- **`status=On Leave` requires `leave_type`.** Frappe validates the Attendance record against the Leave Type on submit. If no matching Leave Application exists on the target site, the Attendance record will still create but the Leave Ledger Entry linkage will be missing — breaks traceability.
- **`docstatus=1` (Submitted) is mandatory for payroll.** Draft Attendance records do NOT contribute to Salary Slip generation. Confirm all bulk-imported rows have `docstatus=1` before the next payroll run. (Note: `docstatus` is intentionally OMITTED from this template — Data Import handles it via the standard Import File contract.)
- **Property Setter on `status` (Section 2).** The Property Setter extends `status.options` to include a leading blank choice. Templates show the effective enum: `Present / Absent / On Leave / Half Day / Work From Home`.
- **Duplicate guard.** The upload script silently skips Attendance rows whose (employee, attendance_date) already exists on the target site (Frappe unique constraint). For corrections, cancel the existing record first then re-import with the new values.
- **Attendance has zero custom fields.** This template contains only stock fields (per Section 1: 0 custom fields). The `medical_certificate_required` and `cover_required` concepts that may appear in older intake sheets are NOT stock fields — they would have to be added as new Custom Fields if a future client requires them.

## Healthcare-specific extensions

None required as standard. Hospital-specific context is captured at the **Shift Type** level (e.g., `Shift Type.color` distinguishes ICU / OT / Ward shifts) and the **Shift Location** level (e.g., `Shift Location.location_name` = `Main Campus`, `Branch Clinic`). For staff who work across multiple departments in a single day, the optional `Shift Assignment` override at import time carries the per-shift context — Attendance inherits department from Employee, not from the assignment.

If a client requires clinical-staff handover flags (e.g., "cover_required_for_clinical_staff"), these must be added as new Custom Fields to `Attendance` (this project's `haritha_hospital` app does NOT define them per Section 1).

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Daily biometric-driven auto-attendance | **No** — use Employee Checkin + HRMS Attendance scheduler |
| Manual entry for missed punches | **Yes** — one-off correction |
| Backfill historical attendance from legacy system | **Yes** — bulk import for payroll integrity |
| Bulk marking (e.g., all-staff WFH day) | **Yes** — script-based mass update |
| Re-import after attendance policy change | **Yes** — cancel old + re-import new |
| Single-day half-day correction | **Yes** — set `status=Half Day`, populate `half_day_status` |

## Common client mistakes

- Leaving `docstatus=0` (Draft) — Attendance won't drive payroll or the leave ledger.
- Setting `status=Present` without `in_time` for shift-bound employees — validation error on submit.
- Setting `status=On Leave` without `leave_type` — validation error on submit.
- Setting `status=Half Day` without `half_day_status` — silently treated as full day.
- Creating Attendance for an employee on a Holiday List date — should be skipped (auto-handled by the scheduler when `process_attendance_after` is set on the Shift Type).
- Backfilling Attendance that overlaps with approved Leave Application records — leads to duplicate Leave Ledger Entry rows on submit.
- Forgetting `company` — auto-fetch should work via Employee, but explicit is safer for Data Import.
- Setting `working_hours` manually that contradicts `in_time`/`out_time` — Frappe recomputes on save and overwrites.
- Importing with `attendance_date` in the future — Frappe allows but flags it; check `attendance_date ≤ today`.
- Setting `attendance_date` for a non-existent or past-dated `Leave Application` link — link drops silently at submit (no `LinkValidationError` for optional Links at insert time).

## Related

- **DocType:** `Attendance` — Frappe HR v16.5.0 stock controller (submittable)
- **Upstream:** `tabEmployee Checkin` (auto-attendance scheduler) + manual entry
- **Downstream:** `tabLeave Ledger Entry` (creates Application row when status=On Leave) + `tabSalary Slip` (counts working_hours)
- **Related template:** `10_employee.csv` (Employee master, sets default_shift), `07_shift_type.csv` (Shift Type master, sets enable_auto_attendance and grace periods)
- **File location:** `docs/client-onboarding/03-intake-workbook/01_master_data/16_attendance.csv`
- **Upload script:** TBD — Wave 4 will add `scripts/upload_attendance.py`
