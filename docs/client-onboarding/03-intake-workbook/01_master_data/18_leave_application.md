# Leave Application — Intake Sheet

**DocType:** `Leave Application` (submittable)
**Module:** HR / Leave Management
**Required fields:** 7
**Optional fields:** 9+

> **Note:** Leave Application is the formal request document that drives the leave ledger. Submitted applications go through the approval workflow (Leave Approver → Approved / Rejected). Approved applications create matching Leave Ledger Entry records and Attendance records (status=On Leave).

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `employee` | Employee | Link → Employee | Y | "EMP-A001" | must exist | – |
| `employee_name` | Employee Name | Data | Y | "Employee A" | non-empty | Join key for prod → dev ID remap |
| `leave_type` | Leave Type | Link → Leave Type | Y | "Leave Type A" | must exist | – |
| `from_date` | From Date | Date | Y | "2025-09-01" | YYYY-MM-DD | – |
| `to_date` | To Date | Date | Y | "2025-09-03" | YYYY-MM-DD, ≥from_date | – |
| `half_day` | Half Day | Check | Y | 0 | 0/1 | – |
| `half_day_date` | Half Day Date | Date | N | "2025-09-01" | YYYY-MM-DD | Required if half_day=1 |
| `posting_date` | Posting Date | Date | Y | "2025-09-01" | YYYY-MM-DD | Date application was filed |
| `company` | Company | Link → Company | Y | "Company A" | must exist | Auto-fetched from employee |
| `department` | Department | Link → Department | N | "Department A" | must exist | Auto-fetched from employee |
| `leave_approver` | Leave Approver | Link → User | Y | "approver.a@example.com" | must exist | User.email |
| `leave_approver_name` | Leave Approver Name | Data | N | "Approver A" | non-empty | Auto-fetched |
| `reason` | Reason | Small Text | N | "Family event" | – | Description / context |
| `status` | Status | Select | N | "Approved" | Open / Approved / Rejected / Cancelled | Defaults to Open |
| `follow_via_email` | Follow Via Email | Check | N | 0 | 0/1 | Notify approver by email |
| `is_lwp` | Is Leave Without Pay | Check | N | 0 | 0/1 | Auto-set if over balance |
| `docstatus` | Document Status | Int | Y | 1 | 0=Draft, 1=Submitted, 2=Cancelled | Submit to apply leave |

## Healthcare-specific fields

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `medical_certificate_required` | Medical Certificate Required | Check | N | 0 | For Sick Leave > 2 days — enforce via Client Script |
| `cover_required` | Cover Required (clinical) | Check | N | 1 | Clinical staff — needs handover/cover arranged |

## Validation rules

- `to_date ≥ from_date`.
- `half_day_date` required if `half_day=1`.
- `leave_approver` must exist as a User and must be listed in the Employee's department approvers (mirrors GOTCHA #10 for Shift Request — same Department Approver pre-seed requirement).
- `status=Approved` requires `docstatus=1`.
- Negative balance check: if `Leave Type.allow_negative_balance=0` and the application exceeds the Employee's current leave balance, the application is rejected unless `Leave Type.is_leave_without_pay=1`.
- Overlapping Leave Applications for the same Employee + date range are rejected.

## Common client mistakes

- Forgetting `leave_approver` — submission fails because the validation hook requires an approver in the Employee's department approver list.
- Setting `half_day=1` without `half_day_date` — validation error.
- Filing Leave Application for a date that is in the past beyond the Leave Type's `applicable_after` working days.
- Approving a Leave Application that pushes the balance negative without setting `is_lwp=1`.
- Creating multiple Leave Applications for the same Employee on overlapping dates — validation error on submit.
- Cancelling (`docstatus=2`) a Leave Application instead of cancelling via the dedicated Cancel action — leaves orphan Leave Ledger Entries.
- Forgetting `posting_date` — defaults to `today()`, which is correct for new applications but wrong for backfills.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Employee self-service (ESS) leave request | **No** — use HRMS Leave Application form |
| Bulk backfill of historical leave (migration from legacy HRIS) | **Yes** — script-based import |
| Mid-month corrections | **Yes** — manual adjustment |
| Compensatory off grants | **No** — use Compensatory Leave Request |
| Maternity / paternity leave | **Yes** — manual filing (often > 7 days, ESS handles it but offline filing common) |

## Migration notes (post-go-live upload)

- **Employee ID remap by `employee_name`.** Same constraint as Attendance and Employee Checkin (GOTCHA #7). The upload script remaps `employee` using `employee_name` as the join key. Client CSV MUST supply both columns.
- **Leave Approver must exist as a User.** The Frappe controller calls `validate_approver()` on submit (mirrors GOTCHA #10 from Shift Request). If `leave_approver` does not reference an existing `tabUser.email`, the submission fails. Pre-create the User via template 10 (`employee.csv`) before this template.
- **`department` Approver pre-seed (GOTCHA #10).** For every department referenced in the Leave Application rows, ensure a `Department Approver` child row exists with `approver` matching the Leave Application's `leave_approver`. Otherwise `validate_approver()` fails even if the User exists. See `scripts/migrate_master_data.py` `_ensure_department_approvers()` for the pattern.
- **`docstatus=1` (Submitted) is mandatory.** Draft Leave Applications do NOT create Leave Ledger Entries and do NOT auto-mark Attendance as `On Leave`. For backfills of historical approved leave, set `docstatus=1, status="Approved"`.
- **Leave Ledger Entry auto-creation.** On Approved submission, HRMS creates one Leave Ledger Entry row per day with `transaction_type=Application`, `leaves_added=-<fraction>`. The upload script does NOT need to create matching Leave Ledger Entry rows — they are generated server-side. (See template 19 only if you need to inject MANUAL ledger adjustments.)
- **Overlap check is strict.** The upload script pre-checks for overlapping Leave Applications on the target site and skips duplicates. For corrections, cancel the existing record first then re-import.

## Related

- **DocType:** `Leave Application` — Frappe HR v16.5.0 stock controller
- **Upstream:** Employee self-service / HR admin
- **Downstream:** `tabLeave Ledger Entry` (auto-created on approval), `tabAttendance` (auto-marked On Leave)
- **Related template:** `11_leave_type.csv` (Leave Type master), `10_employee.csv` (Employee master, sets leave_approver)
- **File location:** `docs/client-onboarding/03-intake-workbook/01_master_data/18_leave_application.csv`
- **Upload script:** TBD — Wave 4 will add `scripts/upload_leave_application.py`
