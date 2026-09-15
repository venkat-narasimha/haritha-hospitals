# Leave Application — Intake Sheet

**DocType:** `Leave Application` (submittable)
**Module:** HR / Leave Management
**Autoname rule:** `naming_series` (Series: `HR-LAP-.YYYY.-`)
**Stock-required fields:** 8 (`naming_series`, `employee`, `leave_type`, `from_date`, `to_date`, `status`, `posting_date`, `company`)
**Stock-optional fields:** 14+
**Custom fields:** 0 (per `haritha_hospital/fixtures/custom_field.json` Section 1)

> **Note:** Leave Application is the formal request document that drives the Leave Ledger. Submitted applications go through the approval workflow (Leave Approver → Approved / Rejected). Approved applications create matching Leave Ledger Entry records (transaction_type=`Leave Application`, leaves negative) and Attendance records (status=`On Leave`).

## Purpose

Per-employee, per-Leave-Type, date-bounded leave request. Drives the leave-balance accounting via the Leave Ledger (auto-populated on Approved submit) and the daily Attendance rows marked `On Leave` for the application period. Submittable DocType — Data Import creates at `docstatus=0` and clients submit via web UI (or the upload script can set `docstatus=1` for backfills of historical approved leave).

The `status` field has 4 fixed values (per Section 4): `Open / Approved / Rejected / Cancelled`. Setting `status=Approved` directly at insert time is the common pattern for bulk backfills of legacy approved leave.

The stock fieldname is **`description`** but the UI label is **`Reason`** (per Section 4 — both client and server use the same DocType field, only the displayed label differs).

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `naming_series` | Series | Select | Y | `HR-LAP-.YYYY.-` | one of `HR-LAP-.YYYY.-` | required stock field; autoname series prefix (per Section 4) |
| `employee` | Employee | Link→Employee | Y | `EMP-A001` | must exist in tabEmployee | required stock field (per Section 4) |
| `employee_name` | Employee Name | Data | N | `Employee A` | non-empty | STOCK-optional; RECOMMENDED as join key for prod→dev ID remap (GOTCHA #7) |
| `leave_type` | Leave Type | Link→Leave Type | Y | `Leave Type A` | must exist in tabLeave Type | required stock field (per Section 4) |
| `department` | Department | Link→Department | N | `Department A` | must exist if set | stock-optional; auto-fetched from Employee record |
| `leave_balance` | Leave Balance Before Application | Float | N | `12.0` | can be negative | stock-optional; Y* if Leave Type.allow_negative_balance=0 (pre-check) |
| `from_date` | From Date | Date | Y | `2025-09-01` | YYYY-MM-DD | required stock field |
| `to_date` | To Date | Date | Y | `2025-09-03` | YYYY-MM-DD; >= from_date | required stock field |
| `half_day` | Half Day | Check | N | `0` | 0/1 | stock-optional; Y* effectively — controls whether half_day_date is required |
| `half_day_date` | Half Day Date | Date | N | `2025-09-01` | YYYY-MM-DD | stock-optional; Y* — required if half_day=1 |
| `total_leave_days` | Total Leave Days | Float | N | `3.0` | ≥0 | stock-optional; auto-computed from from_date/to_date/half_day on submit |
| `description` | Reason | Small Text | N | `Family event` | – | stock-optional; label is Reason per Section 4; free-text context |
| `leave_approver` | Leave Approver | Link→User | N | `approver.a@example.com` | must exist in tabUser | stock-optional BUT must be a User.email; required for validate_approver on submit (GOTCHA-analogous) |
| `leave_approver_name` | Leave Approver Name | Data | N | `Approver A` | non-empty | stock-optional; auto-fetched from leave_approver (User.full_name) |
| `status` | Status | Select | Y | `Approved` | Open/Approved/Rejected/Cancelled | required stock field; options per Section 4 |
| `posting_date` | Posting Date | Date | Y | `2025-09-01` | YYYY-MM-DD | required stock field; date application was filed |
| `company` | Company | Link→Company | Y | `Company A` | must exist in tabCompany | required stock field |
| `follow_via_email` | Follow Via Email | Check | N | `0` | 0/1 | stock-optional; 1 to email the approver |
| `salary_slip` | Salary Slip | Link→Salary Slip | N | `SS-26-09-00001` | must exist if set | stock-optional; back-link when leave spans payroll period |
| `letter_head` | Letter Head | Link→Letter Head | N | `Letter Head A` | must exist if set | stock-optional; print letterhead for printed leave form |
| `color` | Color | Color | N | `#7042B5` | hex string | stock-optional; UI color tag (used in calendar views) |
| `amended_from` | Amended From | Link→Leave Application | N | `LAP-26-09-00001` | must exist if set | stock-optional; for amendment workflow only |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Leave Application", ...}` before constructing the document.
- **Gotcha #14 — leave module unpopulated at go-live.** Single-site deployments typically have 0 Leave Applications at go-live. Template exists for forward-compatibility AND for any backfill from a legacy HRIS.
- **Gotcha #7 — Employee ID remap by `employee_name`.** Same constraint as Attendance and Employee Checkin. The upload script remaps the `employee` field using `employee_name` as the join key. Client CSV MUST supply both `employee` (original) and `employee_name` (the join key), even though `employee_name` is stock-optional.
- **`leave_approver` must be a User.email, not an Employee.name** (GOTCHA-analogous to #10 for Shift Request). The stock `leave_approver` field is `Link→User`. If the field references an Employee name (e.g., `EMP-A001`), the submit-time `validate_approver()` hook fails with `LinkValidationError`. Pre-create the User records (template `10_employee.csv` triggers `create_user_permission` if set) before importing Leave Applications.
- **Department Approver pre-seed (GOTCHA-analogous to #10 for Shift Request).** `validate_approver()` requires the Leave Approver to appear in the Employee's `Department Approver` child table (`leave_approvers` per Section 1). If the approver is not pre-seeded, submit fails even if the User exists. The upload script handles this via the same `_ensure_department_approvers()` pattern used by `migrate_master_data.py`.
- **`status=Approved` requires `docstatus=1`.** Draft (`docstatus=0`) Leave Applications do NOT create Leave Ledger Entries and do NOT auto-mark Attendance as `On Leave`. For backfills of historical approved leave, set `status="Approved"` AND `docstatus=1`.
- **Leave Ledger Entry auto-creation.** On Approved submission, HRMS creates one Leave Ledger Entry row per day with `transaction_type=Leave Application`, `leaves=-<fraction>`. The upload script does NOT need to create matching Leave Ledger Entry rows — they are generated server-side. (See template 19 only if you need to inject MANUAL ledger adjustments.)
- **Overlap check is strict.** The upload script pre-checks for overlapping Leave Applications on the target site and skips duplicates. For corrections, cancel the existing record first then re-import.
- **Negative balance check.** If `Leave Type.allow_negative_balance=0` and the application exceeds the Employee's current leave balance, the application is rejected on submit unless `Leave Type.is_lwp=1`. Pre-check the balance before bulk import.
- **Stock `description` fieldname, "Reason" label.** The CSV uses `description` as the fieldname (per Section 4). The Data Import contract matches the fieldname, NOT the label — uploading a `reason` column will be silently dropped.
- **No custom `is_lwp` field on Leave Application.** Note: the verdict matrix confirms there is NO `is_lwp` field on Leave Application itself — `is_lwp` is a property of the **Leave Type**, not the application. Forcing `is_lwp` onto a Leave Application row will fail at insert.

## Healthcare-specific extensions

None required as standard (per Section 1: 0 custom fields on `Leave Application` in `haritha_hospital`). Hospital context comes from the Employee's department and the Leave Type's properties.

If a client requires clinical-staff specific flags (e.g., `medical_certificate_required` for Sick Leave > 2 days, `cover_required` for clinical handover), these must be added as **new Custom Fields** to `Leave Application` (the `haritha_hospital` app does NOT define them per Section 1). These would attach to every Leave Application and could be enforced via Client Script on the web form.

Common hospital-specific policies to consider:
- **Sick Leave > 2 consecutive days** → require `medical_certificate_required` (would be a Custom Field).
- **Clinical staff (nurses, doctors)** → require `cover_required` indicating handover arranged (would be a Custom Field).
- **Maternity / paternity leave** → typically filed manually rather than via ESS for documentation trail.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Employee self-service (ESS) leave request | **No** — use HRMS Leave Application form |
| Bulk backfill of historical leave (migration from legacy HRIS) | **Yes** — script-based import |
| Mid-month corrections | **Yes** — manual adjustment |
| Compensatory off grants | **No** — use Compensatory Leave Request |
| Maternity / paternity leave | **Yes** — manual filing (often > 7 days, ESS handles it but offline filing common) |
| Cancellation of approved leave (rare) | **Yes** — set `status=Cancelled` and submit (creates compensating Leave Ledger Entry) |

## Common client mistakes

- Forgetting `leave_approver` — submission fails because the validation hook requires an approver in the Employee's department approver list.
- Setting `half_day=1` without `half_day_date` — validation error on submit.
- Filing Leave Application for a date in the past beyond the Leave Type's `applicable_after` working days — rejected on submit.
- Approving a Leave Application that pushes the balance negative without setting `is_lwp=1` on the Leave Type.
- Creating multiple Leave Applications for the same Employee on overlapping dates — validation error on submit.
- Cancelling (`docstatus=2`) a Leave Application instead of cancelling via the dedicated Cancel action — leaves orphan Leave Ledger Entries.
- Using `reason` as the column header instead of `description` — column is silently dropped by Data Import (the stock fieldname is `description`).
- Setting `leave_approver` to an Employee name (e.g., `EMP-A001`) instead of a User email — `LinkValidationError` on submit.
- Forgetting `posting_date` — defaults to `today()`, which is correct for new applications but wrong for backfills.
- Forgetting `naming_series` — fails required check.

## Related

- **DocType:** `Leave Application` — Frappe HR v16.5.0 stock controller (submittable)
- **Upstream:** Employee self-service / HR admin
- **Downstream:** `tabLeave Ledger Entry` (auto-created on approval), `tabAttendance` (auto-marked On Leave for each date in from_date–to_date)
- **Related template:** `11_leave_type.csv` (Leave Type master), `10_employee.csv` (Employee master), `14_leave_allocation.csv` (Leave Allocation master), `19_leave_ledger_entry.csv` (auto-created audit trail)
- **File location:** `docs/client-onboarding/03-intake-workbook/01_master_data/18_leave_application.csv`
- **Upload script:** TBD — Wave 4 will add `scripts/upload_leave_application.py`
