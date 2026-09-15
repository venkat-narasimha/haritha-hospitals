# Per-DocType Signoff — Template

**Date:** 2026-09-15
**Status:** ✅ Complete (rebuilt Phase 3 — 19 DocType blocks, one per template)
**Phase:** 3 — Validation & Signoff

---

## What This Covers

One signoff block per DocType (19 total). Each block captures client attestation, reviewer attestation, validation checklist, and free-text notes. After all 19 blocks are signed, aggregate results in [`02_master_validation_report.md`](./02_master_validation_report.md).

---

## Roles

| Role | Responsibility |
|---|---|
| **Client HR Lead** | Confirms `client_value` column accuracy on every CSV row. Signs the Client attestation block. |
| **Client Project Lead** | Overall sign-off authority for the client. May co-sign Client attestation. |
| **Reviewer (Partner Tech Lead)** | Runs validation checks, confirms Link targets resolve, reviews gotchas. Signs the Reviewer attestation block. |
| **Importer (Partner Tech Lead or designate)** | Executes Data Import; populates Import verification cells. |

---

## Definitions

| Term | Meaning |
|---|---|
| **Records submitted** | Count of non-empty data rows in the CSV (excluding header). |
| **Required-marking fields** | CSV `required` column = `Y` or `Y*`. |
| **Link-target resolved** | Every Link field value points to an existing record in the target DocType (imported earlier per `README.md` §4). |
| **Gotchas reviewed** | Reviewer has read the relevant gotcha(s) from research §7 and confirmed the CSV avoids each one. |
| **Custom fields populated** | For DocTypes with custom fields (`haritha_hospital` app), every required custom field is filled. |
| **Y / N / A** | Yes / No / Not Applicable. |

---

## Universal Migration Note

⚠️ **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script that processes these templates must inject `{"doctype": "<DocType>", ...}` before constructing the document. Applies to every block below.

---

# Signoff Block 01 — Department

**DocType:** Department (stock, not submittable)
**Template file:** [`./01_master_data/01_department.csv`](./01_master_data/01_department.csv) + [`.md`](./01_master_data/01_department.md)
**Required fields:** 2 (`department_name`, `company`) + 5 optional
**Custom fields in scope:** `payroll_cost_center`, `leave_block_list` (both optional)

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Company, Parent Department, Cost Center, Leave Block List): Y / N
- [ ] Gotchas reviewed: **#5** (parent_department root trap), **#11** (name auto-suffix), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): Y / N / A

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 02 — Designation

**DocType:** Designation (stock, not submittable)
**Template file:** [`./01_master_data/02_designation.csv`](./01_master_data/02_designation.csv) + [`.md`](./01_master_data/02_designation.md)
**Required fields:** 1 (`designation_name`)
**Custom fields in scope:** `appraisal_template` (optional)

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Appraisal Template): Y / N / A
- [ ] Gotchas reviewed: **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): Y / N / A

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 03 — Employment Type

**DocType:** Employment Type (stock, not submittable)
**Template file:** [`./01_master_data/03_employment_type.csv`](./01_master_data/03_employment_type.csv) + [`.md`](./01_master_data/03_employment_type.md)
**Required fields:** 1 (`employee_type_name`)
**Custom fields in scope:** none

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved: N/A (no Link fields)
- [ ] Gotchas reviewed: **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 04 — Employee Grade

**DocType:** Employee Grade (stock, not submittable)
**Template file:** [`./01_master_data/04_employee_grade.csv`](./01_master_data/04_employee_grade.csv) + [`.md`](./01_master_data/04_employee_grade.md)
**Required fields:** 1 (`name` — see note below; autoname=prompt)
**Custom fields in scope:** none

> **Note on `name`:** This template uses `name` as the primary-key column because Employee Grade has `autoname=Prompt`. See gotcha #13 — DocType may be unused at single-site deployments.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Salary Structure, Currency): Y / N / A
- [ ] Gotchas reviewed: **#13** (unused at single-site), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 05 — Branch

**DocType:** Branch (stock, not submittable)
**Template file:** [`./01_master_data/05_branch.csv`](./01_master_data/05_branch.csv) + [`.md`](./01_master_data/05_branch.md)
**Required fields:** 1 (`branch`)
**Custom fields in scope:** none

> **Note:** See gotcha #12 — Branch is unused in single-site deployments. Include this block for completeness; mark records count as `0` if not used.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____ (expected 0 for single-site)
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved: N/A (no Link fields)
- [ ] Gotchas reviewed: **#12** (unused at single-site), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 06 — Holiday List

**DocType:** Holiday List (stock, not submittable)
**Template file:** [`./01_master_data/06_holiday_list.csv`](./01_master_data/06_holiday_list.csv) + [`.md`](./01_master_data/06_holiday_list.md)
**Required fields:** 3 (`holiday_list_name`, `from_date`, `to_date`)
**Custom fields in scope:** none

> **Note:** This template imports the parent Holiday List record only. Child `Holiday` rows (one per holiday date) are imported via a separate Data Import on the `Holiday` DocType. Track that import separately.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved: N/A (no Link fields on parent)
- [ ] Gotchas reviewed: **#17** (weekly_off string, not index), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)
- [ ] Child Holiday rows imported separately (count): ____

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 07 — Shift Type

**DocType:** Shift Type (stock, not submittable)
**Template file:** [`./01_master_data/07_shift_type.csv`](./01_master_data/07_shift_type.csv) + [`.md`](./01_master_data/07_shift_type.md)
**Required fields:** 3 (`name`, `start_time`, `end_time`)
**Custom fields in scope:** none

> **Note:** `name` is REQUIRED because Shift Type has `autoname=Prompt` (gotcha #4). Naming convention is client-defined (gotcha #16). `color` Select options extended to 9 colors by property setter.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Holiday List, Overtime Type): Y / N / A
- [ ] Gotchas reviewed: **#4** (autoname=prompt), **#16** (naming convention), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 08 — Shift Location

**DocType:** Shift Location (stock, not submittable)
**Template file:** [`./01_master_data/08_shift_location.csv`](./01_master_data/08_shift_location.csv) + [`.md`](./01_master_data/08_shift_location.md)
**Required fields:** 1 (`location_name`)
**Custom fields in scope:** none

> **Note:** See gotcha #15 — single-site deployments typically have 1 row (e.g. `Site A`). Multi-site chains have 1 row per physical site.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____ (1 typical for single-site)
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved: N/A (no Link fields)
- [ ] Gotchas reviewed: **#8** (autoname=field:location_name), **#15** (single-site = 1 row), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 09 — Shift Schedule

**DocType:** Shift Schedule (stock, not submittable)
**Template file:** [`./01_master_data/09_shift_schedule.csv`](./01_master_data/09_shift_schedule.csv) + [`.md`](./01_master_data/09_shift_schedule.md)
**Required fields:** 4 (`name`, `frequency`, `repeat_on_days`, `shift_type`)
**Custom fields in scope:** none

> **Note:** `name` is REQUIRED because Shift Schedule has `autoname=Prompt` (gotcha #8a). `repeat_on_days` is a Table field; child rows are imported separately via Data Import on `Assignment Rule Day` DocType. Plain `Link` field `amended_from` is one of the 6 known-accepted fields (see master report §4).

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Shift Type, Shift Schedule [amended_from]): Y / N
- [ ] Gotchas reviewed: **#8** (autoname=prompt + child-table docstatus mismatch), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)
- [ ] Child `repeat_on_days` rows imported separately (count): ____

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 10 — Employee

**DocType:** Employee (stock, not submittable)
**Template file:** [`./01_master_data/10_employee.csv`](./01_master_data/10_employee.csv) + [`.md`](./01_master_data/10_employee.md)
**Required fields:** 7 (`naming_series`, `first_name`, `company`, `status`, `gender`, `date_of_birth`, `date_of_joining`)
**Custom fields in scope:** 14+ (`default_shift`, `employment_type`, `grade`, health insurance, approvers, PAN/IFSC/MICR/PF)

> **CRITICAL gotchas:** #6 (gender + default_shift ordering — Gender + Shift Type masters MUST be imported first), #7 (Employee ID remap by `employee_name`), #12 (Branch unused at single-site), #13 (Grade unused at single-site). Plain `Link` fields `company` and `gender` are 2 of the 6 known-accepted (see master report §4).

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Company, Gender, Department, Designation, Employee [reports_to], Branch, Holiday List, Employment Type, Employee Grade, Shift Type, Employee Health Insurance, User [×3 approvers], Currency): Y / N
- [ ] Gotchas reviewed: **#6** (gender + default_shift ordering), **#7** (Employee ID remap), **#12** (Branch unused), **#13** (Grade unused), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): Y / N / A
- [ ] Gender + Shift Type masters verified as imported before Employee: Y / N

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 11 — Leave Type

**DocType:** Leave Type (stock, not submittable)
**Template file:** [`./01_master_data/11_leave_type.csv`](./01_master_data/11_leave_type.csv) + [`.md`](./01_master_data/11_leave_type.md)
**Required fields:** 1 (`leave_type_name`)
**Custom fields in scope:** none

> **Note:** See gotcha #14 — Leave module is configured but transactions are created via App UI, not migration script. This template populates the master definitions (CL / SL / EL / LWP / etc.).

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Salary Component [earning_component]): Y / N / A
- [ ] Gotchas reviewed: **#14** (leave module), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 12 — Leave Policy

**DocType:** Leave Policy (stock, not submittable)
**Template file:** [`./01_master_data/12_leave_policy.csv`](./01_master_data/12_leave_policy.csv) + [`.md`](./01_master_data/12_leave_policy.md)
**Required fields:** 2 (`title`, `leave_policy_details`)
**Custom fields in scope:** none

> **Note:** `leave_policy_details` is a Table field; child Leave Policy Detail rows imported separately. Plain `Link` field `amended_from` is one of the 6 known-accepted (see master report §4). See gotcha #14.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Leave Policy [amended_from]): Y / N
- [ ] Gotchas reviewed: **#14** (leave module), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)
- [ ] Child `leave_policy_details` rows imported separately (count): ____

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 13 — Leave Period

**DocType:** Leave Period (stock, not submittable)
**Template file:** [`./01_master_data/13_leave_period.csv`](./01_master_data/13_leave_period.csv) + [`.md`](./01_master_data/13_leave_period.md)
**Required fields:** 3 (`from_date`, `to_date`, `company`)
**Custom fields in scope:** none

> **Note:** See gotcha #14 — Leave Period is configured via App UI. The template populates annual leave cycles (typically 1 record per year).

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Company, Holiday List [optional]): Y / N
- [ ] Gotchas reviewed: **#14** (leave module), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 14 — Leave Allocation

**DocType:** Leave Allocation (stock, submittable)
**Template file:** [`./01_master_data/14_leave_allocation.csv`](./01_master_data/14_leave_allocation.csv) + [`.md`](./01_master_data/14_leave_allocation.md)
**Required fields:** 7 (`naming_series`, `employee`, `leave_type`, `from_date`, `to_date`, `total_leaves_allocated`, `company`)
**Custom fields in scope:** none

> **Notes:** See gotcha #14 — typically created via App UI per employee per leave period. Gotcha #7 applies if Employees were imported via migration (employee_id remap). `description` is `Small Text` (≤140 chars) — not `Text`.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Employee, Leave Type, Leave Period, Leave Policy, Leave Policy Assignment, Company): Y / N
- [ ] Gotchas reviewed: **#14** (leave module), **#7** (Employee ID remap), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 15 — Shift Assignment

**DocType:** Shift Assignment (stock, submittable)
**Template file:** [`./01_master_data/15_shift_assignment.csv`](./01_master_data/15_shift_assignment.csv) + [`.md`](./01_master_data/15_shift_assignment.md)
**Required fields:** 6 (`name`, `employee`, `employee_name`, `shift_type`, `company`, `start_date`)
**Custom fields in scope:** none

> **CRITICAL gotchas:** #8 (`name` Series override — Frappe will overwrite unless Series counter pre-bumped), #7 (Employee remap by `employee_name`), #9 (`shift_schedule_assignment` field NULLIFIED by script — out of scope), #15 (Shift Location defaults to `Site A`). Plain `Link` fields `department` and `amended_from` are 2 of the 6 known-accepted (see master report §4). Data Import creates records at `docstatus=0` (draft) — submit via web UI to activate.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Employee, Shift Type, Company, Shift Request, Shift Location, Overtime Type, Department, Shift Assignment [amended_from]): Y / N
- [ ] Gotchas reviewed: **#8** (autoname=Series override), **#7** (Employee remap), **#9** (`shift_schedule_assignment` NULLIFIED), **#15** (Shift Location `Site A`), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)
- [ ] Submittable DocType — draft (docstatus=0) created; web UI submit step pending: Y / N

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 16 — Attendance

**DocType:** Attendance (stock, submittable)
**Template file:** [`./01_master_data/16_attendance.csv`](./01_master_data/16_attendance.csv) + [`.md`](./01_master_data/16_attendance.md)
**Required fields:** 5 (`naming_series`, `employee`, `status`, `attendance_date`, `company`)
**Custom fields in scope:** none

> **Notes:** See gotcha #14 — typically auto-created from Employee Checkin via auto-attendance job. Direct Data Import is rare. Gotcha #7 (Employee ID remap) applies. Status options overridden by property setter: `Present / Absent / On Leave / Half Day / Work From Home`.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Employee, Leave Type, Leave Application, Company, Department, Shift Type, Attendance Request, Attendance [amended_from], Overtime Type): Y / N
- [ ] Gotchas reviewed: **#14** (leave module), **#7** (Employee ID remap), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 17 — Employee Checkin

**DocType:** Employee Checkin (stock, submittable)
**Template file:** [`./01_master_data/17_employee_checkin.csv`](./01_master_data/17_employee_checkin.csv) + [`.md`](./01_master_data/17_employee_checkin.md)
**Required fields:** 3 (`employee`, `log_type`, `time`)
**Custom fields in scope:** none

> **Notes:** `log_type` is functionally required (must be `IN` or `OUT`) — stock-optional but verdict is `[R]` per research §6. Gotcha #7 (Employee ID remap) applies. Typically created by biometric/RFID device sync, not direct Data Import.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Employee, Shift Type, Attendance, Overtime Type): Y / N
- [ ] Gotchas reviewed: **#7** (Employee ID remap), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 18 — Leave Application

**DocType:** Leave Application (stock, submittable)
**Template file:** [`./01_master_data/18_leave_application.csv`](./01_master_data/18_leave_application.csv) + [`.md`](./01_master_data/18_leave_application.md)
**Required fields:** 8 (`naming_series`, `employee`, `leave_type`, `from_date`, `to_date`, `status`, `posting_date`, `company`)
**Custom fields in scope:** none

> **Notes:** See gotcha #14 — typically submitted via App UI. Pre-seeding via Data Import is rare. Gotcha #7 (Employee ID remap) applies. `description` label = "Reason". Auto-creates Leave Ledger Entry on submit. `leave_approver` must be a real `User.email` (GOTCHA-analogous to #10).

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Employee, Leave Type, Department, Company, User [leave_approver], Leave Application [amended_from]): Y / N
- [ ] Gotchas reviewed: **#14** (leave module), **#7** (Employee ID remap), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)
- [ ] `leave_approver` confirmed as a real `User.email`: Y / N

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

# Signoff Block 19 — Leave Ledger Entry

**DocType:** Leave Ledger Entry (stock, submittable)
**Template file:** [`./01_master_data/19_leave_ledger_entry.csv`](./01_master_data/19_leave_ledger_entry.csv) + [`.md`](./01_master_data/19_leave_ledger_entry.md)
**Required fields:** 1 (`company`)
**Custom fields in scope:** none

> **Notes:** Leave Ledger Entry is **system-generated** (auto-created when Leave Allocation / Leave Application is processed). Direct Data Import is rarely used. See gotcha #14. `transaction_type` is `Link→DocType` (not Select); `transaction_name` is `Dynamic Link`. Gotcha #7 (Employee ID remap) applies if Employees were imported via migration.

## Client attestation

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Contact person + email | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Reviewer attestation

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Date | YYYY-MM-DD |
| Signature | ________________________________ |

## Validation checklist

- [ ] Records submitted (count): ____ (typically 0 — system-generated)
- [ ] All required-marking fields populated: Y / N — if N, list fields: ________________
- [ ] Cross-template references resolved (Links → Employee, Leave Type, DocType [transaction_type], Leave Ledger Entry [amended_from], Holiday List, Company): Y / N / A
- [ ] Gotchas reviewed: **#14** (leave module), **#7** (Employee ID remap), **#1** (get_doc doctype key)
- [ ] Custom fields populated (if any): N/A (no custom fields)

## Notes / exceptions

_______________________________________________________________
_______________________________________________________________

---

## Changelog

| Date | Changes |
|------|---------|
| 2026-09-15 | Initial version (Phase 3 rebuild) — 19 DocType signoff blocks |

---

## Related

- [`02_master_validation_report.md`](./02_master_validation_report.md) — Aggregate roll-up after all 19 blocks are signed
- [`../README.md`](../README.md) — Workbook index, 19-template table, MIGRATION_ORDER
- [`../../../prompts/P5-rebuild-research.md`](../../../prompts/P5-rebuild-research.md) — §7 gotcha index (17 gotchas)

---

**End of per-DocType signoff template.**
