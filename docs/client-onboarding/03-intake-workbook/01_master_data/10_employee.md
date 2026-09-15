# Employee — Intake Sheet

**DocType:** Employee (not submittable)
**Module:** HR / Employee
**Required fields:** 7 (`naming_series`, `first_name`, `company`, `status`, `gender`, `date_of_birth`, `date_of_joining`)
**Optional fields:** 27+ (incl. 14+ custom fields for healthcare/payroll)

Employee is the central HR master. It references Department, Designation, Branch, Holiday List, Shift Type (custom), Employment Type (custom), Employee Grade (custom), and User (for approvers). It has 5 child tables (Education, External Work History, Internal Work History, External Work History, Internal Work History) — populated via web UI, not Data Import.

> **CRITICAL:** Two Link fields use `mandatory_depends_on` in HRMS — `gender` and `default_shift` (custom). The Gender and Shift Type masters MUST be imported **before** Employee. See Gotcha #6.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| naming_series | Series | Select | Y | HR-EMP- | HR-EMP- | required by property setter (reqd=1) - see gotcha #6; client may keep default prefix |
| first_name | First Name | Data | Y | Employee A | non-empty | required stock field |
| middle_name | Middle Name | Data | N |  | <= 80 chars | stock optional |
| last_name | Last Name | Data | N | Sample | <= 80 chars | stock optional |
| employee_name | Full Name | Data | N | Employee A Sample | non-empty if set | autogen if blank |
| company | Company | Link | Y | Company A | must exist | required stock field |
| status | Status | Select | Y | Active | Active / Inactive / Suspended / Left | required stock field |
| gender | Gender | Link | Y | Not Specified | must exist | required stock field; import Gender master first (gotcha #6) |
| date_of_birth | Date of Birth | Date | Y | 1990-01-01 | YYYY-MM-DD | required stock field |
| date_of_joining | Date of Joining | Date | Y | 2026-09-01 | YYYY-MM-DD | required stock field |
| department | Department | Link→Department | N | Department A | must exist if set | stock optional |
| designation | Designation | Link→Designation | N | Designation A | must exist if set | stock optional |
| reports_to | Reports to | Link→Employee | N | HR-EMP-002 | must exist if set | self-link to another Employee |
| branch | Branch | Link→Branch | N | Branch A | must exist if set | stock optional; unused at single-site (gotcha #12) |
| holiday_list | Holiday List | Link→Holiday List | N | Holiday List A | must exist if set | stock optional but functionally required |
| salary_mode | Salary Mode | Select | N |  | Bank / Cash / Cheque | stock optional |
| bank_name | Bank Name | Data | N |  | <= 100 chars | stock optional |
| bank_ac_no | Bank A/C No. | Data | N |  | <= 30 chars | stock optional |
| cell_number | Mobile | Data | N | +91-9999999999 | phone format | stock optional |
| personal_email | Personal Email | Data | N | employee.a@example.com | email format | stock optional |
| company_email | Company Email | Data | N |  | email format | stock optional |
| employment_type | Employment Type | Link→Employment Type | N | Full-time | must exist if set | custom field; link to Employment Type master |
| grade | Grade | Link→Employee Grade | N | Grade A | must exist if set | custom field; unused at single-site (gotcha #13) |
| default_shift | Default Shift | Link→Shift Type | Y* | T1 | must exist | custom field; required if auto-attendance enabled (gotcha #6) |
| health_insurance_provider | Health Insurance Provider | Link→Employee Health Insurance | N |  | must exist if set | custom field |
| health_insurance_no | Health Insurance No | Data | N |  | <= 50 chars | custom field |
| leave_approver | Leave Approver | Link→User | N | Administrator | must exist if set | custom field; link to User |
| expense_approver | Expense Approver | Link→User | N | Administrator | must exist if set | custom field; link to User |
| shift_request_approver | Shift Request Approver | Link→User | N | Administrator | must exist if set | custom field; link to User |
| pan_number | PAN Number | Data | N | ABCDE1234F | regex if India | custom field; India tax identifier |
| ifsc_code | IFSC Code | Data | N |  | 11 chars | custom field; India bank branch code |
| micr_code | MICR Code | Data | N |  | 9 chars | custom field; India bank MICR |
| provident_fund_account | Provident Fund Account | Data | N |  | <= 30 chars | custom field; PF account number |
| salary_currency | Salary Currency | Link→Currency | N |  | must exist if set | stock optional |
| attendance_device_id | Attendance Device ID (Biometric/RF tag ID) | Data | N | EMP-001 | unique if set | stock optional; links Checkin to employee |
| ctc | Cost to Company (CTC) | Currency | N | 0 | >= 0 | stock optional |

> **Y\* explanation for `default_shift`:** Required by `mandatory_depends_on` if you have set `enable_auto_attendance = 1` on any Shift Type. For deployments without auto-attendance, this is functionally optional.

## Migration notes (from research §7)

- **Gotcha #6 — `gender` and `default_shift` mandatory_depends_on:** Both fields use `mandatory_depends_on` in HRMS. If Gender / Shift Type masters are not imported first, every Employee insert fails. **Import order: Gender → Shift Type → Employee.**
- **Gotcha #7 — Prod / dev Employee ID remap:** Prod uses `HR-EMP-00211` style; dev (after migration) uses `HR-EMP-00002`+. The `employee_name` is preserved. Link fields referencing an Employee must be remapped by `employee_name` before insert.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Employee", ...}` before constructing the document.
- **Property setter on `naming_series`:** `haritha_hospital/fixtures/property_setter.json` flips `naming_series` to reqd=1 (and `employee_number` to hidden=1). The `naming_series` column is REQUIRED.
- **Property setter on `employee_number`:** `employee_number` is hidden by property setter. **Do not include this column in the CSV** — Frappe will reject it.

## Healthcare-specific fields

The `haritha_hospital` custom app adds 20 custom fields to Employee. The most useful for hospital clients:

| fieldname | label | type | when to use |
|---|---|---|---|
| `default_shift` | Default Shift | Link→Shift Type | ALWAYS recommended (auto-attendance workflows) |
| `employment_type` | Employment Type | Link→Employment Type | differentiate Full-time / Contract / etc. |
| `health_insurance_no` | Health Insurance No | Data | hospital staff insurance ID |
| `health_insurance_provider` | Health Insurance Provider | Link | optional provider reference |
| `leave_approver` / `expense_approver` / `shift_request_approver` | Approvers | Link→User | workflow routing |
| `pan_number` / `ifsc_code` / `micr_code` / `provident_fund_account` | Tax/Banking | Data | India payroll compliance |

Skip `job_applicant` (workflow tracking) and `employee_advance_account` / `payroll_cost_center` (out-of-P5-scope advanced payroll).

## When to use this sheet

| Scenario | Use Employee template? |
|---|---|
| Bulk onboarding 50+ employees | YES — one row per employee |
| Adding a single new hire | YES — append row |
| Migrating from legacy HRIS | YES — preserve legacy IDs in `attendance_device_id` |
| Auto-attendance deployment | YES — `default_shift` is required |

## Common client mistakes

- Importing Employees before Gender + Shift Type masters — fails LinkValidationError on `gender` / `default_shift`.
- Omitting `naming_series` — fails on the property-setter-enforced required check.
- Including `employee_number` (hidden by property setter) — Data Import silently drops it.
- Setting `date_of_birth` in DD/MM/YYYY format — fails Date validation. Use YYYY-MM-DD.
- Using non-existent Users in `leave_approver` / `expense_approver` / `shift_request_approver` — fails LinkValidationError.
- Setting `attendance_device_id` to duplicate values across employees — biometric device can resolve to two employees.
- Forgetting to set `company` — required Link; fails import.
- Setting `status = Left` on initial import — those rows are excluded from active lists; use only for past employees.

## Related

- **Department**, **Designation**, **Branch**, **Holiday List**, **Shift Type**, **Employment Type**, **Employee Grade**, **Gender** — all imported BEFORE Employee.
- **Shift Assignment** template references Employee by `employee` (Link) + `employee_name` (Data).
- **Leave Allocation** template references Employee by `employee` (Link).
- **Attendance** / **Employee Checkin** template references Employee by `employee` (Link).
