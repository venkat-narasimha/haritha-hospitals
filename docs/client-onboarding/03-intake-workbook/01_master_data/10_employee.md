# Employee — Intake Sheet

**DocType:** `Employee` (master)
**Module:** HR / People
**Autoname rule:** `naming_series (hidden but reqd=1 per Property Setter)`

**Required fields:** 11  |  **Optional fields:** 16

## Purpose

Master record for each person. Links to Department, Branch, Designation, Grade, Employment Type.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `naming_series` | Series | Select | **Y** | `HR-EMP-.YYYY.-` | must be one of the configured series |  |
| `employee_name` | Employee Name | Data | **Y** | `Employee A` | unique across employees |  |
| `first_name` | First Name | Data | **Y** | `FirstA` | non-empty |  |
| `last_name` | Last Name | Data | **Y** | `LastA` | non-empty |  |
| `gender` | Gender | Link→Gender | **Y** | `Gender A` | must exist in tabGender (auto-seeded by Frappe) |  |
| `date_of_birth` | Date of Birth | Date | **Y** | `1990-01-15` | YYYY-MM-DD |  |
| `date_of_joining` | Date of Joining | Date | **Y** | `2024-01-15` | YYYY-MM-DD |  |
| `status` | Status | Select | **Y** | `Active` | Active/Suspended/Left |  |
| `company` | Company | Link→Company | **Y** | `Company A` | must exist in tabCompany |  |
| `department` | Department | Link→Department | **Y** | `Department A` | must exist in tabDepartment |  |
| `designation` | Designation | Link→Designation | **Y** | `Designation A` | must exist in tabDesignation |  |
| `branch` | Branch | Link→Branch | **N** | `Site A` | must exist if set |  |
| `employment_type` | Employment Type | Link→Employment Type | **N** | `Full-time` | must exist if set |  |
| `grade` | Grade | Link→Employee Grade | **N** | `Grade A` | must exist if set |  |
| `default_shift` | Default Shift | Link→Shift Type | **N** | `Morning-8h` | must exist in tabShift Type |  |
| `holiday_list` | Holiday List | Link→Holiday List | **N** | `Holiday Calendar A` | must exist if set |  |
| `expense_approver` | Expense Approver | Link→User | **N** | `` | must exist in tabUser (login) |  |
| `leave_approver` | Leave Approver | Link→User | **N** | `` | must exist in tabUser |  |
| `shift_request_approver` | Shift Request Approver | Link→User | **N** | `` | must exist in tabUser |  |
| `payroll_cost_center` | Payroll Cost Center | Link→Cost Center | **N** | `Cost Center A` | must exist if set |  |
| `employee_advance_account` | Employee Advance Account | Link→Account | **N** | `Account A` | must exist if set |  |
| `ifsc_code` | IFSC Code | Data | **N** | `BANK0000123` | 11-char format |  |
| `pan_number` | PAN Number | Data | **N** | `ABCDE1234F` | 10-char format |  |
| `micr_code` | MICR Code | Data | **N** | `123456789` | 9-digit format |  |
| `provident_fund_account` | Provident Fund Account | Data | **N** | `PF-12345` | free-form |  |
| `health_insurance_no` | Health Insurance No | Data | **N** | `HI-001` | free-form |  |
| `health_insurance_provider` | Health Insurance Provider | Link→Employee Health Insurance | **N** | `` | must exist in tabEmployee Health Insurance |  |

## Migration notes

- GOTCHA #6: Gender + Shift Type + Department must migrate BEFORE Employee. Ensure those templates run before this one.
- GOTCHA #7: employee_name is the join key for prod→dev ID remap. After Employee imports, the script builds employee_name → name map and rewrites downstream Link values (Shift Assignment, Shift Request). All downstream templates MUST carry employee_name too.
- naming_series is HIDDEN by default BUT Property Setter flipped reqd=1. Fill it explicitly. Use 'HR-EMP-.YYYY.-' or similar.
- Custom fields (employment_type, grade, default_shift, all approver fields, payroll_cost_center, employee_advance_account, IFSC/PAN/MICR/PF, health_insurance_*) require the haritta_hospital app's custom-field fixtures to be loaded BEFORE this migration runs (typically via bench install-app).

## Healthcare-specific extensions (optional, India-context)

- Health insurance fields (health_insurance_no, health_insurance_provider) per India-style hospital staff policies.
- Indian tax/bank fields (PAN, IFSC, MICR, PF account) for payroll/tax filing.
- These can be left blank for non-Indian deployments.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment — bulk import | Yes — required |
| New hire | Yes — single-row insert |
| Promotion/transfer mid-employment | Use separate Employee Promotion / Employee Transfer docs |

## Common client mistakes

- Empty employee_name — must be unique and stable (this becomes the join key).
- Missing gender — fails ValidationError on insert.
- Setting approver fields to Employee.name instead of User.email — fails LinkValidationError.
- Missing department — fails ValidationError on insert.

## Related gotchas

This DocType touches gotcha(s): `##6, ##7` from `scripts/migrate_master_data.py`.
