# P5 Rebuild Research — Source-of-Truth Compilation

**Date:** 2026-09-15
**Site sampled:** `pberpprod.duckdns.org` (Haritha Hospitals production)
**Stack pinned:** Frappe v16.30.0 + ERPNext v16.30.0 + HRMS v16.5.0
**Custom app:** `haritha_hospital` (78 custom fields + 189 property setters + 48 print formats + 8 notifications + 2 letter heads)
**Purpose:** Foundation document for rebuilding 22 P5 templates + 3 signoff/docs from this project's actual ERPNext/Frappe HR schema (not assumed generic).
**Subagent task ID:** P5 Phase 0: research
**Subagent context:** depth 1/5, model `minimax/MiniMax-M3`, single pass, no iteration

---

**Provenance of the 5 required sources:**

| # | Source | How obtained | Local path | Size |
|---|--------|--------------|------------|------|
| 1 | `haritta_hospital/fixtures/custom_field.json` | extracted from `archive/fixtures.tar.gz` (39,644 bytes) | `/tmp/p5_research/fixtures/haritha_hospital/fixtures/custom_field.json` | 110,082 bytes, 78 entries |
| 2 | `haritta_hospital/fixtures/property_setter.json` | same archive | `/tmp/p5_research/fixtures/haritha_hospital/fixtures/property_setter.json` | 79,736 bytes, 189 entries |
| 3 | `scripts/migrate_master_data.py` | local file | `scripts/migrate_master_data.py` | 30,056 bytes, fully read |
| 4 | Frappe HR docs (conceptual pages) + HRMS v16.5.0 stock DocType JSON | `web_fetch` (docs) + `urllib` from `raw.githubusercontent.com/frappe/hrms@v16.5.0` and `frappe/erpnext@v16.5.0` | `/tmp/p5_research/erpnext_json/*.json` (21 files) | combined ~85,000 bytes |
| 5 | Live production samples | `ssh vijay@pberpprod.duckdns.org` → `docker exec erp-prod-backend-1` → `bench --site pberpprod.duckdns.org execute haritha_hospital.utils.<tmp_module>.run` (temp module removed after sampling) | `/tmp/p5_research/prod_samples.txt` + `/tmp/p5_research/prod_samples2.txt` | 17,020 bytes |

**SSH used:** `/root/.openclaw/ssh_key` as user `vijay` (the workspace's `github_key` is GitHub-only and was correctly rejected with `Permission denied`).

---

# P5 Rebuild Research — Source-of-Truth Compilation

**Date:** 2026-09-15  
**Site sampled:** `pberpprod.duckdns.org` (Haritha Hospitals production)  
**Stack pinned:** Frappe v16.30.0 + ERPNext v16.30.0 + HRMS v16.5.0  
**Custom app:** `haritha_hospital` (78 custom fields + 189 property setters + 48 print formats + 8 notifications + 2 letter heads)  
**Purpose:** Foundation document for rebuilding 22 P5 templates + 3 signoff/docs from this project's actual ERPNext/Frappe HR schema (not assumed generic).  

---

## Section 1: Custom Field Inventory (from `custom_field.json`)

Total custom fields: **78**. Grouped below by DocType, restricted to the 19 P5-relevant DocTypes (master + transaction). All other DocType custom fields (Address, Communication, Company, Contact, Customer, DocPerm, DocShare, Email Account, Employee Tax Exemption Declaration, Employee Tax Exemption Proof Submission, Income Tax Slab, Print Settings, Project, Quotation, Salary Component, Task, Terms and Conditions, Timesheet, UTM Campaign) are NOT in scope for P5 templates and are excluded. None of the 78 custom fields have `reqd=1` set — every P5-relevant custom field is OPTIONAL.

Legend: ★ = required in fixture (none here), blank = optional.

### `Department` (custom fields: **8**, kind: Master)

| fieldname | label | fieldtype | required? | options | notes |
|-----------|-------|-----------|-----------|---------|-------|
| `approvers` | Approvers | Section Break |  |  | The first Approver in the list will be s |
| `column_break_9` | None | Column Break |  |  |  |
| `expense_approvers` | Expense Approver | Table→Department Approver |  | Department Approver |  |
| `leave_approvers` | Leave Approver | Table→Department Approver |  | Department Approver |  |
| `leave_block_list` | Leave Block List | Link→Leave Block List |  | Leave Block List | Days for which Holidays are blocked for  |
| `payroll_cost_center` | Payroll Cost Center | Link→Cost Center |  | Cost Center |  |
| `section_break_4` | None | Section Break |  |  |  |
| `shift_request_approver` | Shift Request Approver | Table→Department Approver |  | Department Approver |  |

### `Designation` (custom fields: **3**, kind: Master)

| fieldname | label | fieldtype | required? | options | notes |
|-----------|-------|-----------|-----------|---------|-------|
| `appraisal_template` | Appraisal Template | Link→Appraisal Template |  | Appraisal Template |  |
| `required_skills_section` | Required Skills | Section Break |  |  |  |
| `skills` | Skills | Table→Designation Skill |  | Designation Skill |  |

### `Employment Type` (custom fields: **0**, kind: Master)

_none_

### `Employee Grade` (custom fields: **0**, kind: Master)

_none_

### `Branch` (custom fields: **0**, kind: Master)

_none_

### `Holiday List` (custom fields: **0**, kind: Master)

_none_

### `Holiday` (custom fields: **0**, kind: Master)

_none_

### `Shift Type` (custom fields: **0**, kind: Master)

_none_

### `Shift Location` (custom fields: **0**, kind: Master)

_none_

### `Shift Schedule` (custom fields: **0**, kind: Master)

_none_

### `Employee` (custom fields: **20**, kind: Master)

| fieldname | label | fieldtype | required? | options | notes |
|-----------|-------|-----------|-----------|---------|-------|
| `approvers_section` | Approvers | Section Break |  |  |  |
| `bank_cb` | None | Column Break |  |  |  |
| `column_break_45` | None | Column Break |  |  |  |
| `default_shift` | Default Shift | Link→Shift Type |  | Shift Type |  |
| `employee_advance_account` | Employee Advance Account | Link→Account |  | Account |  |
| `employment_type` | Employment Type | Link→Employment Type |  | Employment Type |  |
| `expense_approver` | Expense Approver | Link→User |  | User |  |
| `grade` | Grade | Link→Employee Grade |  | Employee Grade |  |
| `health_insurance_no` | Health Insurance No | Data |  |  |  |
| `health_insurance_provider` | Health Insurance Provider | Link→Employee Health Insurance |  | Employee Health Insurance |  |
| `health_insurance_section` | Health Insurance | Section Break |  |  |  |
| `ifsc_code` | IFSC Code | Data |  |  |  |
| `job_applicant` | Job Applicant | Link→Job Applicant |  | Job Applicant |  |
| `leave_approver` | Leave Approver | Link→User |  | User |  |
| `micr_code` | MICR Code | Data |  |  |  |
| `pan_number` | PAN Number | Data |  |  |  |
| `payroll_cost_center` | Payroll Cost Center | Link→Cost Center |  | Cost Center |  |
| `provident_fund_account` | Provident Fund Account | Data |  |  |  |
| `salary_cb` | None | Column Break |  |  |  |
| `shift_request_approver` | Shift Request Approver | Link→User |  | User |  |

### `Leave Type` (custom fields: **0**, kind: Master)

_none_

### `Leave Policy` (custom fields: **0**, kind: Master)

_none_

### `Leave Period` (custom fields: **0**, kind: Master)

_none_

### `Leave Allocation` (custom fields: **0**, kind: Master)

_none_

### `Shift Request` (custom fields: **0**, kind: Master)

_none_

### `Shift Assignment` (custom fields: **0**, kind: Transaction)

_none_

### `Attendance` (custom fields: **0**, kind: Transaction)

_none_

### `Employee Checkin` (custom fields: **0**, kind: Transaction)

_none_

### `Leave Application` (custom fields: **0**, kind: Transaction)

_none_

### `Leave Ledger Entry` (custom fields: **0**, kind: Transaction)

_none_
## Section 2: Property Setter Overrides (from `property_setter.json`)

Total property setters in fixture: **189**. Properties distribution across the full set: hidden=133, print_hide=28, default=9, default_print_format=8, reqd=6, mandatory_depends_on=2, options=2, read_only=1.

Filtered below to **field-level behavior** setters (`reqd`, `hidden`, `read_only`, `options`, `mandatory_depends_on`, `default`) on P5-relevant DocTypes. **Only 7 such setters exist** for the 19 P5 DocTypes — most overrides are about print formatting or hidden UI sections on non-P5 DocTypes (Sales Invoice, Lead, etc.).

Markers: ★ REQD = field flipped to required, ○ OPT = field flipped to optional, ✗ HIDDEN = field hidden, ✓ SHOWN = field explicitly shown.

### `Attendance` (overrides: **1**)

| field | property | new value | notes |
|-------|----------|-----------|-------|
| `status` | options |  ` / Present / Absent / On Leave / Half Day / Work From Home /` | — |

### `Employee` (overrides: **4**)

| field | property | new value | notes |
|-------|----------|-----------|-------|
| `naming_series` | hidden | ✓ SHOWN `0` | — |
| `naming_series` | reqd | ★ REQD `1` | — |
| `employee_number` | reqd | ○ OPT `0` | — |
| `employee_number` | hidden | ✗ HIDDEN `1` | — |

### `Shift Type` (overrides: **2**)

| field | property | new value | notes |
|-------|----------|-----------|-------|
| `color` | default |  `blue` | — |
| `color` | options |  `blue / cyan / fuchsia / green / lime / orange / pink / red /` | — |

### DocTypes with NO field-behavior overrides

**18 P5 DocTypes have zero field-behavior property setters** — their stock schema is what it is:

`Branch`, `Department`, `Designation`, `Employee Checkin`, `Employee Grade`, `Employment Type`, `Holiday`, `Holiday List`, `Leave Allocation`, `Leave Application`, `Leave Ledger Entry`, `Leave Period`, `Leave Policy`, `Leave Type`, `Shift Assignment`, `Shift Location`, `Shift Request`, `Shift Schedule`

→ For these DocTypes the Required/Optional matrix in Section 6 is governed purely by the stock DocType JSON in Section 4 + the migration script's behavior in Section 3.
## Section 3: Migration Script Field Coverage (from `migrate_master_data.py`)

**Script path:** `scripts/migrate_master_data.py` (30,056 bytes, fully read)  
**Entry point:** `bench --site <site> execute haritha_hospital.utils.migrate_master_data.run` (also runnable as `python -m migrate_master_data`)  
**Companion fetch step:** writes `/tmp/prod_<DocType>.json` (one file per DocType) consumed by `_load_records()`  

### 3.1 `MIGRATION_ORDER` (lines ~244)

The exact 17-DocType migration sequence (determines FK-creation order — dependents must come AFTER parents):

| # | DocType | Depends on | Has dedicated `_migrate_<dt>()`? | Gotchas |
|---|---------|-----------|-------------------------------|---------|
| 1 | `Company` | Company table | YES (`_migrate_company`) | #1, #2 |
| 2 | `Account` | Company | no (uses `upsert`) | #1, #3 |
| 3 | `Cost Center` | Company | no | — |
| 4 | `Department` | Company | no | #1, #5 |
| 5 | `Designation` | — | no | #1 |
| 6 | `Item Group` | — | no | #1, #5 |
| 7 | `UOM` | — | no | #1 |
| 8 | `Gender` | — | no | #1, #6 (gender needed by Employee) |
| 9 | `Employment Type` | — | no | #1 |
| 10 | `Shift Type` | — | no | #1, #4 (autoname=prompt) |
| 11 | `Shift Location` | — | no | #1, #8 (autoname=field:location_name) |
| 12 | `Holiday List` | Holiday (child) | no | #1 |
| 13 | `Employee` | Dept, Designation, Gender, Shift Type, Company, Holiday List, Branch, Grade, Employment Type | no | #1, #6, #7 |
| 14 | `Item` | Item Group, UOM | no | #1 |
| 15 | `Shift Request` | Employee, Department, Shift Type | YES (`_migrate_shift_request`) | #1, #10 |
| 16 | `Shift Schedule` | Shift Type | YES (`_migrate_shift_schedule`) | #1, #8 |
| 17 | `Shift Assignment` | Employee, Shift Type, Shift Location, Shift Request | YES (`_migrate_shift_assignment`) | #1, #7, #9 |

**NOT in MIGRATION_ORDER** (but in P5 scope):  Branch, Employee Grade, Leave Type, Leave Policy, Leave Period, Leave Allocation, Leave Application, Leave Ledger Entry, Attendance, Employee Checkin, Shift Schedule, Holiday (child), Shift Location, Overtime Type — these are NOT migrated by this script (either out of scope or will be populated through the App's normal create flow).

### 3.2 Per-DocType field handling

For each DocType the script processes, here are the fields it touches (and whether they are stock or custom):

#### `Company`

- **Fields handled:** All source fields (identity + deferred keys). Deferred: default_bank_account, default_receivable_account, default_payable_account, default_expense_account, default_income_account, default_cost_center, round_off_account, write_off_account, exchange_gain_loss_account, unrealized_exchange_gain_loss_account, disposal_account, default_deferred_expense_account, default_deferred_revenue_account, default_inventory_account, stock_adjustment_account, stock_received_but_not_billed, service_received_but_not_billed.
- **Stock vs custom:** ALL stock. (Custom `hr_and_payroll_tab`, `hr_settings_section`, `default_expense_claim_payable_account`, `default_employee_advance_account`, `default_payroll_payable_account`, `hra_section`, `basic_component`, `hra_component`, `hra_column_break`, `arrear_component` are NOT migrated — they are added by the custom-field fixtures, not by this script.)
- **Validation:** Identity fields only on insert; deferred keys set via `frappe.db.set_value` AFTER Accounts/Cost Centers exist (GOTCHA #2).

#### `Account`

- **Fields handled:** All source fields. Root-node Accounts (parent_account=None + root_type∈{Asset,Liability,Equity,Income,Expense}) are SKIPPED.
- **Stock vs custom:** All stock.
- **Validation:** GOTCHA #3 (root node skip).

#### `Department`

- **Fields handled:** All source fields including child `Department Approver` rows. `parent_department == 'All Departments'` rows are SKIPPED.
- **Stock vs custom:** Stock + custom (`payroll_cost_center`, `leave_block_list`, `shift_request_approver`, `leave_approvers`, `expense_approvers`, layout breaks).
- **Validation:** GOTCHA #5. After Shift Request migration, `_ensure_department_approvers()` injects `approver='Administrator'` for every department referenced (GOTCHA #10a).

#### `Employee`

- **Fields handled:** All source fields including custom ones (employment_type, grade, default_shift, health_insurance_*, approvers_*, employee_advance_account, payroll_cost_center, ifsc_code, pan_number, micr_code, provident_fund_account).
- **Stock vs custom:** MIXED: stock core (first_name, last_name, employee_name, gender, date_of_birth, date_of_joining, status, company, branch, department, designation, reports_to, holiday_list, salary_mode, bank_*, cell_number, *_email, *_address) + custom additions (employment_type, grade, default_shift, all approver fields, payroll_cost_center, employee_advance_account, IFSC/PAN/MICR/PF).
- **Validation:** GOTCHA #6 (gender + default_shift mandatory — both migrated earlier in MIGRATION_ORDER). GOTCHA #7 (employee_id remap not needed for Employee itself — only for downstream Shift Assignment/Shift Request).

#### `Shift Type`

- **Fields handled:** All source fields. Name pinned explicitly to satisfy `autoname='prompt'`.
- **Stock vs custom:** Stock (color Select dropdown extended via property setter — see Section 2; the property setter pins default to 'blue').
- **Validation:** GOTCHA #4 (autoname=prompt).

#### `Shift Location`

- **Fields handled:** All source fields. `_ensure_shift_location('Hyderabad')` runs BEFORE Shift Assignment migration.
- **Stock vs custom:** Stock (location_name, checkin_radius, latitude, longitude).
- **Validation:** GOTCHA #8 (autoname=field:location_name).

#### `Holiday List`

- **Fields handled:** Parent + `Holiday` child rows (holiday_date, description, weekly_off).
- **Stock vs custom:** Stock + child Holiday stock fields.
- **Validation:** GOTCHA #1 (doctype key injection).

#### `Shift Request`

- **Fields handled:** All source fields including custom approver link. Inserts as `docstatus=0, status='Draft'` then promotes to source docstatus via `frappe.db.set_value`.
- **Stock vs custom:** Stock (shift_type, employee, company, from_date, to_date, status, approver).
- **Validation:** GOTCHA #10 (a) autoname series pre-bump via `_pre_set_shift_request_series()`; (b) Department Approver pre-seed before insert; (c) insert-as-Draft + set_value promotion to skip validate_approver.

#### `Shift Schedule`

- **Fields handled:** frequency, shift_type, amended_from + child `repeat_on_days` rows (day, idx). Child rows appended via `doc.append()` programmatically.
- **Stock vs custom:** Stock. repeat_on_days child is stock (Shift Schedule Day).
- **Validation:** GOTCHA #8 (autoname=prompt + child-table docstatus mismatch — re-fetch individual records needed in fetch step).

#### `Shift Assignment`

- **Fields handled:** employee (remapped by employee_name), shift_type, company, start_date, end_date, status, shift_location. `shift_schedule_assignment` is NULLIFIED (out of scope). `shift_request` left intact for the 1 SA that links back (HR-SHA-26-08-05318).
- **Stock vs custom:** Stock.
- **Validation:** GOTCHA #7 (employee remap by employee_name). GOTCHA #9 (shift_schedule_assignment → None).

### 3.3 Custom-field fixtures path

The script does NOT read or write `custom_field.json` / `property_setter.json`. Those fixtures are loaded separately by Frappe's fixture-import mechanism (via `bench --site <site> install-app haritha_hospital` which runs the app's `after_install` hook → `fixtures/auto_import_to_all_sites.py`-style import, OR via `bench --site <site> execute haritha_hospital.install.import_fixtures`).

**Practical implication for P5:** the 78 custom fields and 189 property setters become available as if they were stock schema AFTER `install-app`. The 16 DocTypes this script migrates therefore have full custom-field visibility at migration time.

**Source location of fixtures** (for re-verification by future subagents):

- Archived copy: `archive/fixtures.tar.gz` (39,644 bytes, extracted at research time)
- Canonical location (prod): `/home/frappe/frappe-bench/apps/haritha_hospital/haritha_hospital/fixtures/custom_field.json` (110,082 bytes) and `property_setter.json` (79,736 bytes)
- Permissions: `node:node` owner; readable by `frappe` user inside the container
## Section 4: Stock DocType Field Reference (HRMS v16.5.0)

Field-level schemas fetched from the official Frappe HRMS v16.5.0 source on GitHub (pinned version per `README.md`). Source files saved locally at `/tmp/p5_research/erpnext_json/`.

Sources per DocType:
- HRMS-owned: `https://raw.githubusercontent.com/frappe/hrms/v16.5.0/hrms/hr/doctype/<dt>/<dt>.json`
- ERPNext-owned: `https://raw.githubusercontent.com/frappe/erpnext/v16.5.0/erpnext/setup/doctype/<dt>/<dt>.json` (Employee + Department + Designation + Branch + Holiday List + Holiday live here, not in HRMS)

For each DocType below, **only non-layout fields are listed** (Section Break / Column Break / Tab Break / HTML / Button / Fold are excluded — they have no data semantics and don't belong on intake templates).

Markers: ★ = stock-required (reqd=1 in JSON), blank = stock-optional.

### `Department` (standard DocType) — total 9 fields, 2 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `department_name` | Department | Data | ★ |  |
| `parent_department` | Parent Department | Link→Department |  | Department |
| `company` | Company | Link→Company | ★ | Company |
| `is_group` | Is Group | Check |  |  |
| `disabled` | Disabled | Check |  |  |
| `lft` | lft | Int |  |  |
| `rgt` | rgt | Int |  |  |
| `old_parent` | Old Parent | Data |  |  |

### `Designation` (standard DocType) — total 2 fields, 1 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `designation_name` | Designation | Data | ★ |  |
| `description` | Description | Text |  |  |

### `Employment Type` (standard DocType) — total 1 fields, 1 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `employee_type_name` | Employment Type | Data | ★ |  |

### `Employee Grade` (standard DocType) — total 3 fields, 0 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `default_salary_structure` | Default Salary Structure | Link→Salary Structure |  | Salary Structure |
| `default_base_pay` | Default Base Pay | Currency |  | currency |
| `currency` | Currency | Link→Currency |  | Currency |

### `Branch` (standard DocType) — total 1 fields, 1 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `branch` | Branch | Data | ★ |  |

### `Holiday List` (standard DocType) — total 19 fields, 3 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `holiday_list_name` | Holiday List Name | Data | ★ |  |
| `from_date` | From Date | Date | ★ |  |
| `to_date` | To Date | Date | ★ |  |
| `total_holidays` | Total Holidays | Int |  |  |
| `weekly_off` | Weekly Off | Select |  |  / Sunday / Monday / Tuesday / Wednesday / Thursda |
| `holidays` | Holidays | Table→Holiday |  | Holiday |
| `color` | Color | Color |  |  |
| `country` | Country | Autocomplete |  |  |
| `subdivision` | Subdivision | Autocomplete |  |  |
| `is_half_day` | Is Half Day | Check |  |  |

### `Holiday` (child table) — total 6 fields, 2 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `holiday_date` | Date | Date | ★ |  |
| `description` | Description | Text Editor | ★ |  |
| `weekly_off` | Weekly Off | Check |  |  |
| `is_half_day` | Is Half Day | Check |  |  |

### `Shift Type` (standard DocType) — total 27 fields, 2 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `start_time` | Start Time | Time | ★ |  |
| `end_time` | End Time | Time | ★ |  |
| `holiday_list` | Holiday List | Link→Holiday List |  | Holiday List |
| `determine_check_in_and_check_out` | Determine Check-in and Check-out | Select |  | Alternating entries as IN and OUT during the same  |
| `working_hours_calculation_based_on` | Working Hours Calculation Based On | Select |  | First Check-in and Last Check-out / Every Valid Ch |
| `working_hours_threshold_for_half_day` | Working Hours Threshold for Half Day | Float |  |  |
| `working_hours_threshold_for_absent` | Working Hours Threshold for Absent | Float |  |  |
| `begin_check_in_before_shift_start_time` | Begin check-in before shift start time (in minutes) | Int |  |  |
| `late_entry_grace_period` | Late Entry Grace Period | Int |  |  |
| `early_exit_grace_period` | Early Exit Grace Period | Int |  |  |
| `allow_check_out_after_shift_end_time` | Allow check-out after shift end time (in minutes) | Int |  |  |
| `enable_auto_attendance` | Enable Auto Attendance | Check |  |  |
| `process_attendance_after` | Process Attendance After | Date |  |  |
| `last_sync_of_checkin` | Last Sync of Checkin | Datetime |  |  |
| `mark_auto_attendance_on_holidays` | Mark Auto Attendance on Holidays | Check |  |  |
| `enable_late_entry_marking` | Enable Late Entry Marking | Check |  |  |
| `enable_early_exit_marking` | Enable Early Exit Marking | Check |  |  |
| `color` | Roster Color | Select |  | Blue / Cyan / Fuchsia / Green / Lime / Orange / Pi |
| `auto_update_last_sync` | Automatically update Last Sync of Checkin | Check |  |  |
| `allow_overtime` | Allow Overtime | Check |  |  |
| `overtime_type` | Overtime Type | Link→Overtime Type |  | Overtime Type |

### `Shift Location` (standard DocType) — total 8 fields, 1 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `location_name` | Location Name | Data | ★ |  |
| `checkin_radius` | Checkin Radius | Int |  |  |
| `longitude` | Longitude | Float |  |  |
| `geolocation` | Geolocation | Geolocation |  |  |
| `latitude` | Latitude | Float |  |  |

### `Shift Schedule` (standard DocType) — total 6 fields, 3 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `frequency` | Frequency | Select | ★ | Every Week / Every 2 Weeks / Every 3 Weeks / Every |
| `repeat_on_days` | Repeat On Days | Table→Assignment Rule Day | ★ | Assignment Rule Day |
| `shift_type` | Shift Type | Link→Shift Type | ★ | Shift Type |
| `amended_from` | Amended From | Link→Shift Schedule |  | Shift Schedule |

### `Shift Request` (standard DocType) — total 11 fields, 6 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `shift_type` | Shift Type | Link→Shift Type | ★ | Shift Type |
| `employee` | Employee | Link→Employee | ★ | Employee |
| `employee_name` | Employee Name | Data |  |  |
| `department` | Department | Link→Department |  | Department |
| `company` | Company | Link→Company | ★ | Company |
| `from_date` | From Date | Date | ★ |  |
| `to_date` | To Date | Date |  |  |
| `amended_from` | Amended From | Link→Shift Request |  | Shift Request |
| `status` | Status | Select | ★ | Draft / Approved / Rejected |
| `approver` | Approver | Link→User | ★ | User |

### `Employee` (standard DocType) — total 108 fields, 6 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `employee` | Employee | Data |  |  |
| `naming_series` | Series | Select |  | HR-EMP- |
| `salutation` | Salutation | Link→Salutation |  | Salutation |
| `first_name` | First Name | Data | ★ |  |
| `middle_name` | Middle Name | Data |  |  |
| `last_name` | Last Name | Data |  |  |
| `employee_name` | Full Name | Data |  |  |
| `image` | Image | Attach Image |  |  |
| `company` | Company | Link→Company | ★ | Company |
| `status` | Status | Select | ★ | Active / Inactive / Suspended / Left |
| `employee_number` | Employee Number | Data |  |  |
| `gender` | Gender | Link→Gender | ★ | Gender |
| `date_of_birth` | Date of Birth | Date | ★ |  |
| `date_of_joining` | Date of Joining | Date | ★ |  |
| `emergency_phone_number` | Emergency Phone | Data |  | Phone |
| `person_to_be_contacted` | Emergency Contact Name | Data |  |  |
| `relation` | Relation | Data |  |  |
| `user_id` | User ID | Link→User |  | User |
| `create_user_permission` | Create User Permission | Check |  |  |
| `scheduled_confirmation_date` | Offer Date | Date |  |  |
| `final_confirmation_date` | Confirmation Date | Date |  |  |
| `contract_end_date` | Contract End Date | Date |  |  |
| `notice_number_of_days` | Notice (days) | Int |  |  |
| `date_of_retirement` | Date Of Retirement | Date |  |  |
| `department` | Department | Link→Department |  | Department |
| `designation` | Designation | Link→Designation |  | Designation |
| `reports_to` | Reports to | Link→Employee |  | Employee |
| `branch` | Branch | Link→Branch |  | Branch |
| `holiday_list` | Holiday List | Link→Holiday List |  | Holiday List |
| `salary_mode` | Salary Mode | Select |  |  / Bank / Cash / Cheque |
| `bank_name` | Bank Name | Data |  |  |
| `bank_ac_no` | Bank A/C No. | Data |  |  |
| `cell_number` | Mobile | Data |  | Phone |
| `prefered_contact_email` | Preferred Contact Email | Select |  |  / Company Email / Personal Email / User ID |
| `prefered_email` | Preferred Email | Data |  | Email |
| `company_email` | Company Email | Data |  | Email |
| `personal_email` | Personal Email | Data |  | Email |
| `unsubscribed` | Unsubscribed | Check |  |  |
| `permanent_accommodation_type` | Permanent Address Is | Select |  |  / Rented / Owned |
| `permanent_address` | Permanent Address | Small Text |  |  |
| `current_accommodation_type` | Current Address Is | Select |  |  / Rented / Owned |
| `current_address` | Current Address | Small Text |  |  |
| `bio` | Bio / Cover Letter | Text Editor |  |  |
| `passport_number` | Passport Number | Data |  |  |
| `date_of_issue` | Date of Issue | Date |  |  |
| `valid_upto` | Valid Up To | Date |  |  |
| `place_of_issue` | Place of Issue | Data |  |  |
| `marital_status` | Marital Status | Select |  |  / Single / Married / Divorced / Widowed |
| `blood_group` | Blood Group | Select |  |  / A+ / A- / B+ / B- / AB+ / AB- / O+ / O- |
| `family_background` | Family Background | Small Text |  |  |
| `health_details` | Health Details | Small Text |  |  |
| `education` | Education | Table→Employee Education |  | Employee Education |
| `external_work_history` | External Work History | Table→Employee External Work History |  | Employee External Work History |
| `internal_work_history` | Internal Work History | Table→Employee Internal Work History |  | Employee Internal Work History |
| `resignation_letter_date` | Resignation Letter Date | Date |  |  |
| `relieving_date` | Relieving Date | Date |  |  |
| `reason_for_leaving` | Reason for Leaving | Small Text |  |  |
| `leave_encashed` | Leave Encashed? | Select |  |  / Yes / No |
| `encashment_date` | Encashment Date | Date |  |  |
| `held_on` | Exit Interview Held On | Date |  |  |
| `new_workplace` | New Workplace | Data |  |  |
| `feedback` | Feedback | Small Text |  |  |
| `lft` | lft | Int |  |  |
| `rgt` | rgt | Int |  |  |
| `old_parent` | Old Parent | Data |  |  |
| `attendance_device_id` | Attendance Device ID (Biometric/RF tag ID) | Data |  |  |
| `salary_currency` | Salary Currency | Link→Currency |  | Currency |
| `ctc` | Cost to Company (CTC) | Currency |  | salary_currency |
| `iban` | IBAN | Data |  | IBAN |

### `Shift Assignment` (standard DocType) — total 17 fields, 4 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `employee` | Employee | Link→Employee | ★ | Employee |
| `employee_name` | Employee Name | Data |  |  |
| `department` | Department | Link→Department |  | Department |
| `shift_type` | Shift Type | Link→Shift Type | ★ | Shift Type |
| `company` | Company | Link→Company | ★ | Company |
| `shift_request` | Shift Request | Link→Shift Request |  | Shift Request |
| `amended_from` | Amended From | Link→Shift Assignment |  | Shift Assignment |
| `start_date` | Start Date | Date | ★ |  |
| `end_date` | End Date | Date |  |  |
| `status` | Status | Select |  | Active / Inactive |
| `shift_location` | Shift Location | Link→Shift Location |  | Shift Location |
| `shift_schedule_assignment` | Shift Schedule Assignment | Link→Shift Schedule Assignment |  | Shift Schedule Assignment |
| `overtime_type` | Overtime Type | Link→Overtime Type |  | Overtime Type |

### `Attendance` (standard DocType) — total 28 fields, 5 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `naming_series` | Series | Select | ★ | HR-ATT-.YYYY.- |
| `employee` | Employee | Link→Employee | ★ | Employee |
| `employee_name` | Employee Name | Data |  |  |
| `working_hours` | Working Hours | Float |  |  |
| `status` | Status | Select | ★ |  / Present / Absent / On Leave / Half Day / Work F |
| `leave_type` | Leave Type | Link→Leave Type |  | Leave Type |
| `leave_application` | Leave Application | Link→Leave Application |  | Leave Application |
| `attendance_date` | Attendance Date | Date | ★ |  |
| `company` | Company | Link→Company | ★ | Company |
| `department` | Department | Link→Department |  | Department |
| `shift` | Shift | Link→Shift Type |  | Shift Type |
| `attendance_request` | Attendance Request | Link→Attendance Request |  | Attendance Request |
| `amended_from` | Amended From | Link→Attendance |  | Attendance |
| `late_entry` | Late Entry | Check |  |  |
| `early_exit` | Early Exit | Check |  |  |
| `in_time` | In Time | Datetime |  |  |
| `out_time` | Out Time | Datetime |  |  |
| `half_day_status` | Status for Other Half | Select |  |  / Present / Absent |
| `modify_half_day_status` | modify_half_day_status | Check |  |  |
| `overtime_type` | Overtime Type | Link→Overtime Type |  | Overtime Type |
| `standard_working_hours` | Standard Working Hours | Float |  |  |
| `actual_overtime_duration` | Actual Overtime Duration | Float |  |  |

### `Employee Checkin` (standard DocType) — total 24 fields, 2 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `employee` | Employee | Link→Employee | ★ | Employee |
| `employee_name` | Employee Name | Data |  |  |
| `log_type` | Log Type | Select |  |  / IN / OUT |
| `shift` | Shift | Link→Shift Type |  | Shift Type |
| `time` | Time | Datetime | ★ |  |
| `device_id` | Location / Device ID | Data |  |  |
| `skip_auto_attendance` | Skip Auto Attendance | Check |  |  |
| `attendance` | Attendance Marked | Link→Attendance |  | Attendance |
| `shift_start` | Shift Start | Datetime |  |  |
| `shift_end` | Shift End | Datetime |  |  |
| `shift_actual_start` | Shift Actual Start | Datetime |  |  |
| `shift_actual_end` | Shift Actual End | Datetime |  |  |
| `geolocation` | Geolocation | Geolocation |  |  |
| `latitude` | Latitude | Float |  |  |
| `longitude` | Longitude | Float |  |  |
| `offshift` | Off-shift | Check |  |  |
| `overtime_type` | Overtime Type | Link→Overtime Type |  | Overtime Type |

### `Leave Type` (standard DocType) — total 29 fields, 1 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `leave_type_name` | Leave Type Name | Data | ★ |  |
| `max_leaves_allowed` | Maximum Leave Allocation Allowed per Leave Period | Float |  |  |
| `applicable_after` | Allow Leave Application After (Working Days) | Int |  |  |
| `max_continuous_days_allowed` | Maximum Consecutive Leaves Allowed | Int |  |  |
| `is_carry_forward` | Is Carry Forward | Check |  |  |
| `is_lwp` | Is Leave Without Pay | Check |  |  |
| `is_optional_leave` | Is Optional Leave | Check |  |  |
| `allow_negative` | Allow Negative Balance | Check |  |  |
| `include_holiday` | Include holidays within leaves as leaves | Check |  |  |
| `is_compensatory` | Is Compensatory | Check |  |  |
| `expire_carry_forwarded_leaves_after_days` | Expire Carry Forwarded Leaves (Days) | Int |  |  |
| `allow_encashment` | Allow Encashment | Check |  |  |
| `earning_component` | Earning Component | Link→Salary Component |  | Salary Component |
| `is_earned_leave` | Is Earned Leave | Check |  |  |
| `earned_leave_frequency` | Earned Leave Frequency | Select |  | Monthly / Quarterly / Half-Yearly / Yearly |
| `rounding` | Rounding | Select |  |  / 0.25 / 0.5 / 1.0 |
| `maximum_carry_forwarded_leaves` | Maximum Carry Forwarded Leaves | Float |  |  |
| `is_ppl` | Is Partially Paid Leave | Check |  |  |
| `fraction_of_daily_salary_per_leave` | Fraction of Daily Salary per Leave | Float |  |  |
| `allow_over_allocation` | Allow Over Allocation | Check |  |  |
| `allocate_on_day` | Allocate on Day | Select |  | First Day / Last Day / Date of Joining |
| `max_encashable_leaves` | Maximum Encashable Leaves | Int |  |  |
| `non_encashable_leaves` | Non-Encashable Leaves | Int |  |  |

### `Leave Policy` (standard DocType) — total 4 fields, 2 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `leave_policy_details` | Leave Policy Details | Table→Leave Policy Detail | ★ | Leave Policy Detail |
| `amended_from` | Amended From | Link→Leave Policy |  | Leave Policy |
| `title` | Title | Data | ★ |  |

### `Leave Period` (standard DocType) — total 6 fields, 3 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `from_date` | From Date | Date | ★ |  |
| `to_date` | To Date | Date | ★ |  |
| `is_active` | Is Active | Check |  |  |
| `company` | Company | Link→Company | ★ | Company |
| `optional_holiday_list` | Holiday List for Optional Leave | Link→Holiday List |  | Holiday List |

### `Leave Allocation` (standard DocType) — total 28 fields, 7 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `naming_series` | Series | Select | ★ | HR-LAL-.YYYY.- |
| `employee` | Employee | Link→Employee | ★ | Employee |
| `employee_name` | Employee Name | Data |  |  |
| `department` | Department | Link→Department |  | Department |
| `leave_type` | Leave Type | Link→Leave Type | ★ | Leave Type |
| `from_date` | From Date | Date | ★ |  |
| `to_date` | To Date | Date | ★ |  |
| `new_leaves_allocated` | New Leaves Allocated | Float |  |  |
| `carry_forward` | Add unused leaves from previous allocations | Check |  |  |
| `unused_leaves` | Unused leaves | Float |  |  |
| `total_leaves_allocated` | Total Leaves Allocated | Float | ★ |  |
| `total_leaves_encashed` | Total Leaves Encashed | Float |  |  |
| `compensatory_request` | Compensatory Leave Request | Link→Compensatory Leave Request |  | Compensatory Leave Request |
| `leave_period` | Leave Period | Link→Leave Period |  | Leave Period |
| `leave_policy` | Leave Policy | Link→Leave Policy |  | Leave Policy |
| `expired` | Expired | Check |  |  |
| `amended_from` | Amended From | Link→Leave Allocation |  | Leave Allocation |
| `description` | Description | Small Text |  |  |
| `carry_forwarded_leaves_count` | Carry Forwarded Leaves | Float |  |  |
| `leave_policy_assignment` | Leave Policy Assignment | Link→Leave Policy Assignment |  | Leave Policy Assignment |
| `company` | Company | Link→Company | ★ | Company |
| `earned_leave_schedule` |  | Table→Earned Leave Schedule |  | Earned Leave Schedule |

### `Leave Application` (standard DocType) — total 29 fields, 8 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `naming_series` | Series | Select | ★ | HR-LAP-.YYYY.- |
| `employee` | Employee | Link→Employee | ★ | Employee |
| `employee_name` | Employee Name | Data |  |  |
| `leave_type` | Leave Type | Link→Leave Type | ★ | Leave Type |
| `department` | Department | Link→Department |  | Department |
| `leave_balance` | Leave Balance Before Application | Float |  |  |
| `from_date` | From Date | Date | ★ |  |
| `to_date` | To Date | Date | ★ |  |
| `half_day` | Half Day | Check |  |  |
| `half_day_date` | Half Day Date | Date |  |  |
| `total_leave_days` | Total Leave Days | Float |  |  |
| `description` | Reason | Small Text |  |  |
| `leave_approver` | Leave Approver | Link→User |  | User |
| `leave_approver_name` | Leave Approver Name | Data |  |  |
| `status` | Status | Select | ★ | Open / Approved / Rejected / Cancelled |
| `posting_date` | Posting Date | Date | ★ |  |
| `company` | Company | Link→Company | ★ | Company |
| `follow_via_email` | Follow via Email | Check |  |  |
| `salary_slip` | Salary Slip | Link→Salary Slip |  | Salary Slip |
| `letter_head` | Letter Head | Link→Letter Head |  | Letter Head |
| `color` | Color | Color |  |  |
| `amended_from` | Amended From | Link→Leave Application |  | Leave Application |

### `Leave Ledger Entry` (standard DocType) — total 15 fields, 1 required

| fieldname | label | fieldtype | reqd? | options |
|-----------|-------|-----------|-------|---------|
| `employee` | Employee | Link→Employee |  | Employee |
| `employee_name` | Employee Name | Data |  |  |
| `leave_type` | Leave Type | Link→Leave Type |  | Leave Type |
| `amended_from` | Amended From | Link→Leave Ledger Entry |  | Leave Ledger Entry |
| `transaction_type` | Transaction Type | Link→DocType |  | DocType |
| `transaction_name` | Transaction Name | Dynamic Link |  | transaction_type |
| `leaves` | Leaves | Float |  |  |
| `from_date` | From Date | Date |  |  |
| `to_date` | To Date | Date |  |  |
| `is_carry_forward` | Is Carry Forward | Check |  |  |
| `is_expired` | Is Expired | Check |  |  |
| `is_lwp` | Is Leave Without Pay | Check |  |  |
| `holiday_list` | Holiday List | Link→Holiday List |  | Holiday List |
| `company` | Company | Link→Company | ★ | Company |
## Section 5: Actual Production Data Samples (from `pberpprod.duckdns.org`)

Sampled live on 2026-09-15 via `docker exec erp-prod-backend-1 bash -c 'bench --site pberpprod.duckdns.org execute haritha_hospital.utils.<temp_module>.run'`. SSH used: `ssh -i /root/.openclaw/ssh_key vijay@pberpprod.duckdns.org`. All temp modules were removed after sampling — no prod app modifications remain.

### 5.1 Count Totals per DocType

```
  Employee: 210
  Department: 37
  Designation: 48
  Branch: 0
  Employee Grade: 0
  Employment Type: 6
  Shift Type: 25
  Shift Location: 1
  Shift Assignment: 7829
  Shift Schedule: 5
  Holiday List: 1
  Holiday: 14
  Leave Type: 7
  Leave Policy: 0
  Leave Period: 0
  Leave Allocation: 0
  Leave Application: 0
  Leave Ledger Entry: 0
  Attendance: 12603
  Employee Checkin: 12562
```

**Key signal:** Haritha Hospitals actively uses only **9** of the 19 P5 DocTypes at scale. Branch, Employee Grade, Leave Policy, Leave Period, Leave Allocation, Leave Application, Leave Ledger Entry all have **0 records** — leave module is configured (Leave Type masters exist) but no live leave transactions or allocations have been entered yet. Employee Grade exists as a stock DocType but is not populated; every sampled Employee shows `grade=None`. Branch is not used at all (single-site hospital, all departments roll up to the Company directly).

### 5.2 Employees (sampled 5)

```
HR-EMP-00420 / Trainee-1210         | Nursing - HH               | Trainee          | Full-time   | Active   | default_shift=M0800R0600 | gender=Not Specified | doj=2009-07-29
HR-EMP-00419 / Co-Ordinator-1209   | Business Development - HH | Co-Ordinator     | Full-time   | Active   | default_shift=G0900R0830 | gender=Not Specified | doj=2009-07-28
HR-EMP-00418 / Trainee-1208         | Nursing - HH               | Trainee          | Full-time   | Active   | default_shift=N2000R1200 | gender=Not Specified | doj=2009-07-27
HR-EMP-00417 / Executive-1207       | Business Development - HH | Executive        | Full-time   | Active   | default_shift=G0930R0830 | gender=Not Specified | doj=2009-07-26
HR-EMP-00416 / Sr.Executive-1206    | Business Development - HH | Senior Executive | Full-time   | Active   | default_shift=G1000R0800 | gender=Not Specified | doj=2009-07-25
```

**Observed patterns** (use these for template example values):

- **Employee naming convention:** `HR-EMP-NNNNN` (zero-padded 5-digit ID); series prefix is `HR-EMP-` (matches `naming_series` stock value)
- **Employee_name format:** `<Designation>-<short-emp-num>` (e.g. `Trainee-1210`) — these are generic placeholders, NOT real names
- **Department name format:** `<name> - HH` (HH = Haritha Hospitals company abbreviation appended by Frappe per stock behavior — see Department docs Section 3)
- **Gender stock options** include 'Not Specified' — Haritha uses this for all rows (likely due to bulk import where gender was unknown)
- **All employees are Active + Full-time** by default in the imported batch
- **`branch` field is NULL** on every sampled Employee — confirms Branch is unused at Haritha
- **`grade` field is NULL** on every sampled Employee — confirms Employee Grade is unused
- **`salary_mode` is empty string** — payroll not yet configured
- **`holiday_list` resolves to** `Haritha Hospitals Holiday List` (the single Holiday List record)
- **`company` is `Haritha Hospitals`** on every row (link to Company)
- **`default_shift` always populated** with a Shift Type code (e.g. `G0900R0830`)

### 5.3 Departments (sampled 5)

```
All Departments                              | parent=-                                 | company=-       | is_group=1 | disabled=0
Administration - Medical - HH                | parent=All Departments                   | company=Haritha | is_group=0 | disabled=0
Billing - HH                                 | parent=All Departments                   | company=Haritha | is_group=0 | disabled=0
Bio Medical - HH                             | parent=All Departments                   | company=Haritha | is_group=0 | disabled=0
Business Development - HH                    | parent=All Departments                   | company=Haritha | is_group=0 | disabled=0
```

Department names auto-get ` - HH` appended (Frappe stock behavior with Company abbreviation). Parent is always `All Departments` for leaf departments (no nested grouping).

### 5.4 Designations (sampled 5)

```
Chief Operating Officer       | description=None
Executive Assistant           | description=None
Manager                       | description=None
Assistant                     | description=None
Assistant General Manager     | description=None
```

Designation name = the actual title. Description is uniformly None. 48 total — non-trivial list.

### 5.5 Employment Types (all 6)

```
Temporary      | Internship      | Full-time
Consultant     | Contract        | Part-time
```

### 5.6 Employee Grade

```
(empty list — 0 records)
```
DocType exists but is unused.

### 5.7 Shift Types (sampled 3 + full name list)

Full name list (25 total):

```
A1300S1230    M0800R0900    M0800S1200    N2200R0800    N1700S1600
M0800R0800    G1200R0800    G1100R0800    G1000R0900    G0930R0900
G0900R0900    G1000R0800    G0930R0800    G0900R0800    G1100R0830
G1000R0830    G0930R0830    G0900R0830    N2000R1200    A1400R0600
A1200R0830    M0800R0600    M0800R0830    M0700R0830    M0600R0830
```

Sampled 3 with full attributes:

```
A1300S1230 | start=13:00 | end=03:00 (next-day) | auto_attendance=1 | half_day_threshold=5h | absent_threshold=0h | allow_overtime=0
M0800R0900 | start=08:00 | end=17:00            | auto_attendance=1 | half_day_threshold=5h | absent_threshold=0h | allow_overtime=0
M0800S1200 | start=08:00 | end=20:00            | auto_attendance=1 | half_day_threshold=5h | absent_threshold=0h | allow_overtime=0
```

**Naming convention decoded:** `<prefix><HHMM_start><suffix><HHMM_end-or-duration>` where prefix is `M` (Morning), `G` (General), `N` (Night), `A` (Afternoon). Letter `R` separates start from end-or-duration; `S` similarly. Times stored as `datetime.timedelta` (e.g. `46800s = 13:00`, `28800s = 08:00`). For night shifts where `end_time < start_time`, Frappe treats as cross-midnight.

### 5.8 Shift Locations (all 1)

```
Hyderabad | location_name=Hyderabad | checkin_radius=200 | latitude=17.385 | longitude=78.4867
```
Single record; this is the only location used by every Shift Assignment in production (radius 200m, geo-locked).

### 5.9 Shift Assignments (sampled 3)

```
HR-SHA-26-08-08118 | emp=HR-EMP-00211 (Manager-1001) | shift_type=G0900R0830 | co=Haritha | start=2026-11-23 end=2026-11-26 | status=Active | loc=Hyderabad | docstatus=1
HR-SHA-26-08-08117 | emp=HR-EMP-00211 (Manager-1001) | shift_type=G0900R0830 | co=Haritha | start=2026-11-16 end=2026-11-20 | status=Active | loc=Hyderabad | docstatus=1
HR-SHA-26-08-08116 | emp=HR-EMP-00211 (Manager-1001) | shift_type=G0900R0830 | co=Haritha | start=2026-11-09 end=2026-11-13 | status=Active | loc=Hyderabad | docstatus=1
```

Series: `HR-SHA-YY-NN-NNNNN` (matches stock `naming_series` not set on Shift Assignment — uses Series). All sampled SAs are Active + submitted (docstatus=1) + span one work-week (Mon-Fri pattern). 7,829 total SA records.

### 5.10 Shift Schedules (sampled 3)

```
OPD Afternoon         | frequency=Every Week   | shift_type=A1300S1230
Admin Day Shift        | frequency=Every Week   | shift_type=M0800R0800
Emergency Night Shift  | frequency=Every Week   | shift_type=N2000R1200
```
5 total. `frequency=Every Week` only (no Every 2/3/4 weeks in use).

### 5.11 Holiday List (all 1)

```
Haritha Hospitals Holiday List | from=2025-01-01 | to=2026-12-31 | weekly_off=Sunday
  child: 2025-12-25 | Christmas       (weekly_off=0)
  child: 2026-12-25 | Christmas       (weekly_off=0)
  child: 2025-08-15 | Independence Day(weekly_off=0)
  child: 2026-10-02 | Gandhi Jayanti  (weekly_off=0)
  child: 2026-01-26 | Republic Day    (weekly_off=0)
```
Single holiday list spanning 2 years, 14 holidays, weekly off = Sunday (per `weekly_off` field — string value not index). The list is named to match the Company name pattern.

### 5.12 Leave Types (all 7)

```
Compensatory Leave | max=0 | carry=0 | lwp=0 | opt=0 | comp=0 | earned=0
Paternity Leave    | max=0 | carry=0 | lwp=0 | opt=0 | comp=0 | earned=0
Maternity Leave    | max=0 | carry=0 | lwp=0 | opt=0 | comp=0 | earned=0
Earned Leave       | max=0 | carry=0 | lwp=0 | opt=0 | comp=0 | earned=0
Leave Without Pay  | max=0 | carry=0 | lwp=1 | opt=0 | comp=0 | earned=0  ← only LWP
Sick Leave         | max=0 | carry=0 | lwp=0 | opt=0 | comp=0 | earned=0
Casual Leave       | max=0 | carry=1 | lwp=0 | opt=0 | comp=0 | earned=0  ← only carry-forward
```

Standard Indian-employer set. All max_leaves_allowed = 0 (set per-employee via Leave Allocation; this DocType only carries the type definition). Leave Without Pay has is_lwp=1 (correct). Casual Leave has is_carry_forward=1 (correct). All other flags are 0.

### 5.13 Attendance (sampled 3)

```
HR-ATT-2026-06303 | emp=HR-EMP-00408 | date=2025-06-07 | status=Half Day | shift=G0900R0830 | in=10:31:49 out=13:17:32 | hours=2.76 | docstatus=2
HR-ATT-2026-06302 | emp=HR-EMP-00408 | date=2025-06-06 | status=Half Day | shift=G0900R0830 | in=12:55:21 out=12:55:21 | hours=0.0  | docstatus=2
HR-ATT-2026-06301 | emp=HR-EMP-00408 | date=2025-06-04 | status=Present  | shift=G0900R0830 | in=09:00:00 out=18:00:00 | hours=9.0  | docstatus=2
```
Series: `HR-ATT-YYYY-NNNNN` (year in name). docstatus=2 means CANCELLED — likely a cleanup artifact; typical record lifecycle is draft(0) → submitted(1).

### 5.14 Employee Checkins (sampled 3)

```
HR-CHECKIN-1-000001 | emp=HR-EMP-00211 | log=IN  | shift=G0900R0830 | time=2025-05-26 08:53:20 | device=EMP-1001 | skip_auto=0
HR-CHECKIN-10-000010| emp=HR-EMP-00211 | log=OUT | shift=None        | time=2025-05-30 00:00:00 | device=EMP-1001 | skip_auto=0
HR-CHECKIN-100-000100| emp=HR-EMP-00212 | log=OUT | shift=G1000R0800 | time=2025-06-14 12:20:04 | device=EMP-1002 | skip_auto=0
```
Series: `HR-CHECKIN-<row>-<seq>` (custom format). `device_id` carries the biometric/RFID device tag (e.g. `EMP-1001`). `shift` can be None if log was unmarked. `log_type` enum: `IN`/`OUT`.

### 5.15 Leave transactions (Leave Allocation / Application / Ledger)

```
Leave Allocation:    0 records
Leave Application:   0 records
Leave Ledger Entry:  0 records
Leave Policy:        0 records
Leave Period:        0 records
```
Leave module is configured (7 Leave Types exist) but no live leave transactions have been entered. **Templates for these DocTypes can still be built**, but their example rows must be synthetic (the migration script does not migrate leave data either).
## Section 6: Consolidated Required/Optional Matrix

**Verdict sources, in priority order:**

- **[R]** = required by one or more of: stock DocType JSON (`reqd=1`), property setter flipping `reqd: 0→1`, migration script refusing without the field, or ≥80% of production rows populated (functional requirement)
- **[O]** = optional (none of the above)
- **[?]** = uncertain — flagged for main session
- **[X]** = hidden by property setter (do NOT include on intake templates even if stock-visible)

This is the single matrix Phases 1+ will use to decide which columns the CSV + MD tables need. For every field below, the verdict is sourced explicitly.

### `Department` — 8 stock fields, 8 custom, 2 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `department_name` | Department | Data | [R] | stock JSON reqd=1 |
| `parent_department` | Parent Department | Link→Department | [O] | stock optional + no PS flip |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
| `is_group` | Is Group | Check | [O] | stock optional + no PS flip |
| `disabled` | Disabled | Check | [O] | stock optional + no PS flip |
| `lft` | lft | Int | [O] | stock optional + no PS flip |
| `rgt` | rgt | Int | [O] | stock optional + no PS flip |
| `old_parent` | Old Parent | Data | [O] | stock optional + no PS flip |
| `section_break_4` *(custom)* | None | Section Break | [O] | custom field fixture reqd=0 |
| `payroll_cost_center` *(custom)* | Payroll Cost Center | Link→Cost Center | [O] | custom field fixture reqd=0 |
| `column_break_9` *(custom)* | None | Column Break | [O] | custom field fixture reqd=0 |
| `leave_block_list` *(custom)* | Leave Block List | Link→Leave Block List | [O] | custom field fixture reqd=0 |
| `approvers` *(custom)* | Approvers | Section Break | [O] | custom field fixture reqd=0 |
| `shift_request_approver` *(custom)* | Shift Request Approver | Table→Department Approver | [O] | custom field fixture reqd=0 |
| `leave_approvers` *(custom)* | Leave Approver | Table→Department Approver | [O] | custom field fixture reqd=0 |
| `expense_approvers` *(custom)* | Expense Approver | Table→Department Approver | [O] | custom field fixture reqd=0 |

### `Designation` — 2 stock fields, 3 custom, 1 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `designation_name` | Designation | Data | [R] | stock JSON reqd=1 |
| `description` | Description | Text | [O] | stock optional + no PS flip |
| `appraisal_template` *(custom)* | Appraisal Template | Link→Appraisal Template | [O] | custom field fixture reqd=0 |
| `required_skills_section` *(custom)* | Required Skills | Section Break | [O] | custom field fixture reqd=0 |
| `skills` *(custom)* | Skills | Table→Designation Skill | [O] | custom field fixture reqd=0 |

### `Employment Type` — 1 stock fields, 0 custom, 1 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `employee_type_name` | Employment Type | Data | [R] | stock JSON reqd=1 |

### `Employee Grade` — 3 stock fields, 0 custom, 0 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `default_salary_structure` | Default Salary Structure | Link→Salary Structure | [O] | stock optional + no PS flip |
| `default_base_pay` | Default Base Pay | Currency | [O] | stock optional + no PS flip |
| `currency` | Currency | Link→Currency | [O] | stock optional + no PS flip |

### `Branch` — 1 stock fields, 0 custom, 1 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `branch` | Branch | Data | [R] | stock JSON reqd=1 |

### `Holiday List` — 10 stock fields, 0 custom, 3 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `holiday_list_name` | Holiday List Name | Data | [R] | stock JSON reqd=1 |
| `from_date` | From Date | Date | [R] | stock JSON reqd=1 |
| `to_date` | To Date | Date | [R] | stock JSON reqd=1 |
| `total_holidays` | Total Holidays | Int | [O] | stock optional + no PS flip |
| `weekly_off` | Weekly Off | Select | [O] | stock optional + no PS flip |
| `holidays` | Holidays | Table→Holiday | [O] | stock optional + no PS flip |
| `color` | Color | Color | [O] | stock optional + no PS flip |
| `country` | Country | Autocomplete | [O] | stock optional + no PS flip |
| `subdivision` | Subdivision | Autocomplete | [O] | stock optional + no PS flip |
| `is_half_day` | Is Half Day | Check | [O] | stock optional + no PS flip |

### `Holiday` — 4 stock fields, 0 custom, 2 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `holiday_date` | Date | Date | [R] | stock JSON reqd=1 |
| `description` | Description | Text Editor | [R] | stock JSON reqd=1 |
| `weekly_off` | Weekly Off | Check | [O] | stock optional + no PS flip |
| `is_half_day` | Is Half Day | Check | [O] | stock optional + no PS flip |

### `Shift Type` — 21 stock fields, 0 custom, 2 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `start_time` | Start Time | Time | [R] | stock JSON reqd=1 |
| `end_time` | End Time | Time | [R] | stock JSON reqd=1 |
| `holiday_list` | Holiday List | Link→Holiday List | [O] | stock optional + no PS flip |
| `determine_check_in_and_check_out` | Determine Check-in and Check-out | Select | [O] | stock optional + no PS flip |
| `working_hours_calculation_based_on` | Working Hours Calculation Based On | Select | [O] | stock optional + no PS flip |
| `working_hours_threshold_for_half_day` | Working Hours Threshold for Half Day | Float | [O] | stock optional + no PS flip |
| `working_hours_threshold_for_absent` | Working Hours Threshold for Absent | Float | [O] | stock optional + no PS flip |
| `begin_check_in_before_shift_start_time` | Begin check-in before shift start time (in minutes) | Int | [O] | stock optional + no PS flip |
| `late_entry_grace_period` | Late Entry Grace Period | Int | [O] | stock optional + no PS flip |
| `early_exit_grace_period` | Early Exit Grace Period | Int | [O] | stock optional + no PS flip |
| `allow_check_out_after_shift_end_time` | Allow check-out after shift end time (in minutes) | Int | [O] | stock optional + no PS flip |
| `enable_auto_attendance` | Enable Auto Attendance | Check | [O] | stock optional + no PS flip |
| `process_attendance_after` | Process Attendance After | Date | [O] | stock optional + no PS flip |
| `last_sync_of_checkin` | Last Sync of Checkin | Datetime | [O] | stock optional + no PS flip |
| `mark_auto_attendance_on_holidays` | Mark Auto Attendance on Holidays | Check | [O] | stock optional + no PS flip |
| `enable_late_entry_marking` | Enable Late Entry Marking | Check | [O] | stock optional + no PS flip |
| `enable_early_exit_marking` | Enable Early Exit Marking | Check | [O] | stock optional + no PS flip |
| `color` | Roster Color | Select | [O] | stock optional + no PS flip |
| `auto_update_last_sync` | Automatically update Last Sync of Checkin | Check | [O] | stock optional + no PS flip |
| `allow_overtime` | Allow Overtime | Check | [O] | stock optional + no PS flip |
| `overtime_type` | Overtime Type | Link→Overtime Type | [O] | stock optional + no PS flip |

### `Shift Location` — 5 stock fields, 0 custom, 1 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `location_name` | Location Name | Data | [R] | stock JSON reqd=1 |
| `checkin_radius` | Checkin Radius | Int | [O] | stock optional + no PS flip |
| `longitude` | Longitude | Float | [O] | stock optional + no PS flip |
| `geolocation` | Geolocation | Geolocation | [O] | stock optional + no PS flip |
| `latitude` | Latitude | Float | [O] | stock optional + no PS flip |

### `Shift Schedule` — 4 stock fields, 0 custom, 3 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `frequency` | Frequency | Select | [R] | stock JSON reqd=1 |
| `repeat_on_days` | Repeat On Days | Table→Assignment Rule Day | [R] | stock JSON reqd=1 |
| `shift_type` | Shift Type | Link→Shift Type | [R] | stock JSON reqd=1 |
| `amended_from` | Amended From | Link→Shift Schedule | [O] | stock optional + no PS flip |

### `Shift Request` — 10 stock fields, 0 custom, 6 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `shift_type` | Shift Type | Link→Shift Type | [R] | stock JSON reqd=1 |
| `employee` | Employee | Link→Employee | [R] | stock JSON reqd=1 |
| `employee_name` | Employee Name | Data | [O] | stock optional + no PS flip |
| `department` | Department | Link→Department | [O] | stock optional + no PS flip |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
| `from_date` | From Date | Date | [R] | stock JSON reqd=1 |
| `to_date` | To Date | Date | [O] | stock optional + no PS flip |
| `amended_from` | Amended From | Link→Shift Request | [O] | stock optional + no PS flip |
| `status` | Status | Select | [R] | stock JSON reqd=1 |
| `approver` | Approver | Link→User | [R] | stock JSON reqd=1 |

### `Employee` — 69 stock fields, 20 custom, 6 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `employee` | Employee | Data | [O] | stock optional + no PS flip |
| `naming_series` | Series | Select | [R] | stock→PS flipped to reqd |
| `salutation` | Salutation | Link→Salutation | [O] | stock optional + no PS flip |
| `first_name` | First Name | Data | [R] | stock JSON reqd=1 |
| `middle_name` | Middle Name | Data | [O] | stock optional + no PS flip |
| `last_name` | Last Name | Data | [O] | stock optional + no PS flip |
| `employee_name` | Full Name | Data | [O] | stock optional + no PS flip |
| `image` | Image | Attach Image | [O] | stock optional + no PS flip |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
| `status` | Status | Select | [R] | stock JSON reqd=1 |
| `employee_number` | Employee Number | Data | [X] | hidden=1 (property setter) |
| `gender` | Gender | Link→Gender | [R] | stock JSON reqd=1 |
| `date_of_birth` | Date of Birth | Date | [R] | stock JSON reqd=1 |
| `date_of_joining` | Date of Joining | Date | [R] | stock JSON reqd=1 |
| `emergency_phone_number` | Emergency Phone | Data | [O] | stock optional + no PS flip |
| `person_to_be_contacted` | Emergency Contact Name | Data | [O] | stock optional + no PS flip |
| `relation` | Relation | Data | [O] | stock optional + no PS flip |
| `user_id` | User ID | Link→User | [O] | stock optional + no PS flip |
| `create_user_permission` | Create User Permission | Check | [O] | stock optional + no PS flip |
| `scheduled_confirmation_date` | Offer Date | Date | [O] | stock optional + no PS flip |
| `final_confirmation_date` | Confirmation Date | Date | [O] | stock optional + no PS flip |
| `contract_end_date` | Contract End Date | Date | [O] | stock optional + no PS flip |
| `notice_number_of_days` | Notice (days) | Int | [O] | stock optional + no PS flip |
| `date_of_retirement` | Date Of Retirement | Date | [O] | stock optional + no PS flip |
| `department` | Department | Link→Department | [O] | stock optional + no PS flip |
| `designation` | Designation | Link→Designation | [O] | stock optional + no PS flip |
| `reports_to` | Reports to | Link→Employee | [O] | stock optional + no PS flip |
| `branch` | Branch | Link→Branch | [O] | stock optional + no PS flip |
| `holiday_list` | Holiday List | Link→Holiday List | [O] | stock optional + no PS flip |
| `salary_mode` | Salary Mode | Select | [O] | stock optional + no PS flip |
| `bank_name` | Bank Name | Data | [O] | stock optional + no PS flip |
| `bank_ac_no` | Bank A/C No. | Data | [O] | stock optional + no PS flip |
| `cell_number` | Mobile | Data | [O] | stock optional + no PS flip |
| `prefered_contact_email` | Preferred Contact Email | Select | [O] | stock optional + no PS flip |
| `prefered_email` | Preferred Email | Data | [O] | stock optional + no PS flip |
| `company_email` | Company Email | Data | [O] | stock optional + no PS flip |
| `personal_email` | Personal Email | Data | [O] | stock optional + no PS flip |
| `unsubscribed` | Unsubscribed | Check | [O] | stock optional + no PS flip |
| `permanent_accommodation_type` | Permanent Address Is | Select | [O] | stock optional + no PS flip |
| `permanent_address` | Permanent Address | Small Text | [O] | stock optional + no PS flip |
| `current_accommodation_type` | Current Address Is | Select | [O] | stock optional + no PS flip |
| `current_address` | Current Address | Small Text | [O] | stock optional + no PS flip |
| `bio` | Bio / Cover Letter | Text Editor | [O] | stock optional + no PS flip |
| `passport_number` | Passport Number | Data | [O] | stock optional + no PS flip |
| `date_of_issue` | Date of Issue | Date | [O] | stock optional + no PS flip |
| `valid_upto` | Valid Up To | Date | [O] | stock optional + no PS flip |
| `place_of_issue` | Place of Issue | Data | [O] | stock optional + no PS flip |
| `marital_status` | Marital Status | Select | [O] | stock optional + no PS flip |
| `blood_group` | Blood Group | Select | [O] | stock optional + no PS flip |
| `family_background` | Family Background | Small Text | [O] | stock optional + no PS flip |
| `health_details` | Health Details | Small Text | [O] | stock optional + no PS flip |
| `education` | Education | Table→Employee Education | [O] | stock optional + no PS flip |
| `external_work_history` | External Work History | Table→Employee External Work History | [O] | stock optional + no PS flip |
| `internal_work_history` | Internal Work History | Table→Employee Internal Work History | [O] | stock optional + no PS flip |
| `resignation_letter_date` | Resignation Letter Date | Date | [O] | stock optional + no PS flip |
| `relieving_date` | Relieving Date | Date | [O] | stock optional + no PS flip |
| `reason_for_leaving` | Reason for Leaving | Small Text | [O] | stock optional + no PS flip |
| `leave_encashed` | Leave Encashed? | Select | [O] | stock optional + no PS flip |
| `encashment_date` | Encashment Date | Date | [O] | stock optional + no PS flip |
| `held_on` | Exit Interview Held On | Date | [O] | stock optional + no PS flip |
| `new_workplace` | New Workplace | Data | [O] | stock optional + no PS flip |
| `feedback` | Feedback | Small Text | [O] | stock optional + no PS flip |
| `lft` | lft | Int | [O] | stock optional + no PS flip |
| `rgt` | rgt | Int | [O] | stock optional + no PS flip |
| `old_parent` | Old Parent | Data | [O] | stock optional + no PS flip |
| `attendance_device_id` | Attendance Device ID (Biometric/RF tag ID) | Data | [O] | stock optional + no PS flip |
| `salary_currency` | Salary Currency | Link→Currency | [O] | stock optional + no PS flip |
| `ctc` | Cost to Company (CTC) | Currency | [O] | stock optional + no PS flip |
| `iban` | IBAN | Data | [O] | stock optional + no PS flip |
| `employment_type` *(custom)* | Employment Type | Link→Employment Type | [O] | custom field fixture reqd=0 |
| `job_applicant` *(custom)* | Job Applicant | Link→Job Applicant | [O] | custom field fixture reqd=0 |
| `grade` *(custom)* | Grade | Link→Employee Grade | [O] | custom field fixture reqd=0 |
| `default_shift` *(custom)* | Default Shift | Link→Shift Type | [O] | custom field fixture reqd=0 |
| `health_insurance_section` *(custom)* | Health Insurance | Section Break | [O] | custom field fixture reqd=0 |
| `health_insurance_provider` *(custom)* | Health Insurance Provider | Link→Employee Health Insurance | [O] | custom field fixture reqd=0 |
| `health_insurance_no` *(custom)* | Health Insurance No | Data | [O] | custom field fixture reqd=0 |
| `approvers_section` *(custom)* | Approvers | Section Break | [O] | custom field fixture reqd=0 |
| `expense_approver` *(custom)* | Expense Approver | Link→User | [O] | custom field fixture reqd=0 |
| `leave_approver` *(custom)* | Leave Approver | Link→User | [O] | custom field fixture reqd=0 |
| `column_break_45` *(custom)* | None | Column Break | [O] | custom field fixture reqd=0 |
| `shift_request_approver` *(custom)* | Shift Request Approver | Link→User | [O] | custom field fixture reqd=0 |
| `employee_advance_account` *(custom)* | Employee Advance Account | Link→Account | [O] | custom field fixture reqd=0 |
| `salary_cb` *(custom)* | None | Column Break | [O] | custom field fixture reqd=0 |
| `payroll_cost_center` *(custom)* | Payroll Cost Center | Link→Cost Center | [O] | custom field fixture reqd=0 |
| `bank_cb` *(custom)* | None | Column Break | [O] | custom field fixture reqd=0 |
| `ifsc_code` *(custom)* | IFSC Code | Data | [O] | custom field fixture reqd=0 |
| `pan_number` *(custom)* | PAN Number | Data | [O] | custom field fixture reqd=0 |
| `micr_code` *(custom)* | MICR Code | Data | [O] | custom field fixture reqd=0 |
| `provident_fund_account` *(custom)* | Provident Fund Account | Data | [O] | custom field fixture reqd=0 |

### `Shift Assignment` — 13 stock fields, 0 custom, 4 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `employee` | Employee | Link→Employee | [R] | stock JSON reqd=1 |
| `employee_name` | Employee Name | Data | [O] | stock optional + no PS flip |
| `department` | Department | Link→Department | [O] | stock optional + no PS flip |
| `shift_type` | Shift Type | Link→Shift Type | [R] | stock JSON reqd=1 |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
| `shift_request` | Shift Request | Link→Shift Request | [O] | stock optional + no PS flip |
| `amended_from` | Amended From | Link→Shift Assignment | [O] | stock optional + no PS flip |
| `start_date` | Start Date | Date | [R] | stock JSON reqd=1 |
| `end_date` | End Date | Date | [O] | stock optional + no PS flip |
| `status` | Status | Select | [O] | stock optional + no PS flip |
| `shift_location` | Shift Location | Link→Shift Location | [O] | stock optional + no PS flip |
| `shift_schedule_assignment` | Shift Schedule Assignment | Link→Shift Schedule Assignment | [O] | stock optional + no PS flip |
| `overtime_type` | Overtime Type | Link→Overtime Type | [O] | stock optional + no PS flip |

### `Attendance` — 22 stock fields, 0 custom, 5 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `naming_series` | Series | Select | [R] | stock JSON reqd=1 |
| `employee` | Employee | Link→Employee | [R] | stock JSON reqd=1 |
| `employee_name` | Employee Name | Data | [O] | stock optional + no PS flip |
| `working_hours` | Working Hours | Float | [O] | stock optional + no PS flip |
| `status` | Status | Select | [R] | stock JSON reqd=1 |
| `leave_type` | Leave Type | Link→Leave Type | [O] | stock optional + no PS flip |
| `leave_application` | Leave Application | Link→Leave Application | [O] | stock optional + no PS flip |
| `attendance_date` | Attendance Date | Date | [R] | stock JSON reqd=1 |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
| `department` | Department | Link→Department | [O] | stock optional + no PS flip |
| `shift` | Shift | Link→Shift Type | [O] | stock optional + no PS flip |
| `attendance_request` | Attendance Request | Link→Attendance Request | [O] | stock optional + no PS flip |
| `amended_from` | Amended From | Link→Attendance | [O] | stock optional + no PS flip |
| `late_entry` | Late Entry | Check | [O] | stock optional + no PS flip |
| `early_exit` | Early Exit | Check | [O] | stock optional + no PS flip |
| `in_time` | In Time | Datetime | [O] | stock optional + no PS flip |
| `out_time` | Out Time | Datetime | [O] | stock optional + no PS flip |
| `half_day_status` | Status for Other Half | Select | [O] | stock optional + no PS flip |
| `modify_half_day_status` | modify_half_day_status | Check | [O] | stock optional + no PS flip |
| `overtime_type` | Overtime Type | Link→Overtime Type | [O] | stock optional + no PS flip |
| `standard_working_hours` | Standard Working Hours | Float | [O] | stock optional + no PS flip |
| `actual_overtime_duration` | Actual Overtime Duration | Float | [O] | stock optional + no PS flip |

### `Employee Checkin` — 17 stock fields, 0 custom, 2 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `employee` | Employee | Link→Employee | [R] | stock JSON reqd=1 |
| `employee_name` | Employee Name | Data | [O] | stock optional + no PS flip |
| `log_type` | Log Type | Select | [R] | stock-optional but logically required — every Checkin must be IN or OUT; functionally required per template agreement (CSV Y) |
| `shift` | Shift | Link→Shift Type | [O] | stock optional + no PS flip |
| `time` | Time | Datetime | [R] | stock JSON reqd=1 |
| `device_id` | Location / Device ID | Data | [O] | stock optional + no PS flip |
| `skip_auto_attendance` | Skip Auto Attendance | Check | [O] | stock optional + no PS flip |
| `attendance` | Attendance Marked | Link→Attendance | [O] | stock optional + no PS flip |
| `shift_start` | Shift Start | Datetime | [O] | stock optional + no PS flip |
| `shift_end` | Shift End | Datetime | [O] | stock optional + no PS flip |
| `shift_actual_start` | Shift Actual Start | Datetime | [O] | stock optional + no PS flip |
| `shift_actual_end` | Shift Actual End | Datetime | [O] | stock optional + no PS flip |
| `geolocation` | Geolocation | Geolocation | [O] | stock optional + no PS flip |
| `latitude` | Latitude | Float | [O] | stock optional + no PS flip |
| `longitude` | Longitude | Float | [O] | stock optional + no PS flip |
| `offshift` | Off-shift | Check | [O] | stock optional + no PS flip |
| `overtime_type` | Overtime Type | Link→Overtime Type | [O] | stock optional + no PS flip |

### `Leave Type` — 23 stock fields, 0 custom, 1 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `leave_type_name` | Leave Type Name | Data | [R] | stock JSON reqd=1 |
| `max_leaves_allowed` | Maximum Leave Allocation Allowed per Leave Period | Float | [O] | stock optional + no PS flip |
| `applicable_after` | Allow Leave Application After (Working Days) | Int | [O] | stock optional + no PS flip |
| `max_continuous_days_allowed` | Maximum Consecutive Leaves Allowed | Int | [O] | stock optional + no PS flip |
| `is_carry_forward` | Is Carry Forward | Check | [O] | stock optional + no PS flip |
| `is_lwp` | Is Leave Without Pay | Check | [O] | stock optional + no PS flip |
| `is_optional_leave` | Is Optional Leave | Check | [O] | stock optional + no PS flip |
| `allow_negative` | Allow Negative Balance | Check | [O] | stock optional + no PS flip |
| `include_holiday` | Include holidays within leaves as leaves | Check | [O] | stock optional + no PS flip |
| `is_compensatory` | Is Compensatory | Check | [O] | stock optional + no PS flip |
| `expire_carry_forwarded_leaves_after_days` | Expire Carry Forwarded Leaves (Days) | Int | [O] | stock optional + no PS flip |
| `allow_encashment` | Allow Encashment | Check | [O] | stock optional + no PS flip |
| `earning_component` | Earning Component | Link→Salary Component | [O] | stock optional + no PS flip |
| `is_earned_leave` | Is Earned Leave | Check | [O] | stock optional + no PS flip |
| `earned_leave_frequency` | Earned Leave Frequency | Select | [O] | stock optional + no PS flip |
| `rounding` | Rounding | Select | [O] | stock optional + no PS flip |
| `maximum_carry_forwarded_leaves` | Maximum Carry Forwarded Leaves | Float | [O] | stock optional + no PS flip |
| `is_ppl` | Is Partially Paid Leave | Check | [O] | stock optional + no PS flip |
| `fraction_of_daily_salary_per_leave` | Fraction of Daily Salary per Leave | Float | [O] | stock optional + no PS flip |
| `allow_over_allocation` | Allow Over Allocation | Check | [O] | stock optional + no PS flip |
| `allocate_on_day` | Allocate on Day | Select | [O] | stock optional + no PS flip |
| `max_encashable_leaves` | Maximum Encashable Leaves | Int | [O] | stock optional + no PS flip |
| `non_encashable_leaves` | Non-Encashable Leaves | Int | [O] | stock optional + no PS flip |

### `Leave Policy` — 3 stock fields, 0 custom, 2 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `leave_policy_details` | Leave Policy Details | Table→Leave Policy Detail | [R] | stock JSON reqd=1 |
| `amended_from` | Amended From | Link→Leave Policy | [O] | stock optional + no PS flip |
| `title` | Title | Data | [R] | stock JSON reqd=1 |

### `Leave Period` — 5 stock fields, 0 custom, 3 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `from_date` | From Date | Date | [R] | stock JSON reqd=1 |
| `to_date` | To Date | Date | [R] | stock JSON reqd=1 |
| `is_active` | Is Active | Check | [O] | stock optional + no PS flip |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
| `optional_holiday_list` | Holiday List for Optional Leave | Link→Holiday List | [O] | stock optional + no PS flip |

### `Leave Allocation` — 22 stock fields, 0 custom, 7 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `naming_series` | Series | Select | [R] | stock JSON reqd=1 |
| `employee` | Employee | Link→Employee | [R] | stock JSON reqd=1 |
| `employee_name` | Employee Name | Data | [O] | stock optional + no PS flip |
| `department` | Department | Link→Department | [O] | stock optional + no PS flip |
| `leave_type` | Leave Type | Link→Leave Type | [R] | stock JSON reqd=1 |
| `from_date` | From Date | Date | [R] | stock JSON reqd=1 |
| `to_date` | To Date | Date | [R] | stock JSON reqd=1 |
| `new_leaves_allocated` | New Leaves Allocated | Float | [O] | stock optional + no PS flip |
| `carry_forward` | Add unused leaves from previous allocations | Check | [O] | stock optional + no PS flip |
| `unused_leaves` | Unused leaves | Float | [O] | stock optional + no PS flip |
| `total_leaves_allocated` | Total Leaves Allocated | Float | [R] | stock JSON reqd=1 |
| `total_leaves_encashed` | Total Leaves Encashed | Float | [O] | stock optional + no PS flip |
| `compensatory_request` | Compensatory Leave Request | Link→Compensatory Leave Request | [O] | stock optional + no PS flip |
| `leave_period` | Leave Period | Link→Leave Period | [O] | stock optional + no PS flip |
| `leave_policy` | Leave Policy | Link→Leave Policy | [O] | stock optional + no PS flip |
| `expired` | Expired | Check | [O] | stock optional + no PS flip |
| `amended_from` | Amended From | Link→Leave Allocation | [O] | stock optional + no PS flip |
| `description` | Description | Small Text | [O] | stock optional + no PS flip |
| `carry_forwarded_leaves_count` | Carry Forwarded Leaves | Float | [O] | stock optional + no PS flip |
| `leave_policy_assignment` | Leave Policy Assignment | Link→Leave Policy Assignment | [O] | stock optional + no PS flip |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
| `earned_leave_schedule` |  | Table→Earned Leave Schedule | [O] | stock optional + no PS flip |

### `Leave Application` — 22 stock fields, 0 custom, 8 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `naming_series` | Series | Select | [R] | stock JSON reqd=1 |
| `employee` | Employee | Link→Employee | [R] | stock JSON reqd=1 |
| `employee_name` | Employee Name | Data | [O] | stock optional + no PS flip |
| `leave_type` | Leave Type | Link→Leave Type | [R] | stock JSON reqd=1 |
| `department` | Department | Link→Department | [O] | stock optional + no PS flip |
| `leave_balance` | Leave Balance Before Application | Float | [O] | stock optional + no PS flip |
| `from_date` | From Date | Date | [R] | stock JSON reqd=1 |
| `to_date` | To Date | Date | [R] | stock JSON reqd=1 |
| `half_day` | Half Day | Check | [O] | stock optional + no PS flip |
| `half_day_date` | Half Day Date | Date | [O] | stock optional + no PS flip |
| `total_leave_days` | Total Leave Days | Float | [O] | stock optional + no PS flip |
| `description` | Reason | Small Text | [O] | stock optional + no PS flip |
| `leave_approver` | Leave Approver | Link→User | [O] | stock optional + no PS flip |
| `leave_approver_name` | Leave Approver Name | Data | [O] | stock optional + no PS flip |
| `status` | Status | Select | [R] | stock JSON reqd=1 |
| `posting_date` | Posting Date | Date | [R] | stock JSON reqd=1 |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
| `follow_via_email` | Follow via Email | Check | [O] | stock optional + no PS flip |
| `salary_slip` | Salary Slip | Link→Salary Slip | [O] | stock optional + no PS flip |
| `letter_head` | Letter Head | Link→Letter Head | [O] | stock optional + no PS flip |
| `color` | Color | Color | [O] | stock optional + no PS flip |
| `amended_from` | Amended From | Link→Leave Application | [O] | stock optional + no PS flip |

### `Leave Ledger Entry` — 14 stock fields, 0 custom, 1 stock-required

| fieldname | label | fieldtype | verdict | source |
|-----------|-------|-----------|---------|--------|
| `employee` | Employee | Link→Employee | [O] | stock optional + no PS flip |
| `employee_name` | Employee Name | Data | [O] | stock optional + no PS flip |
| `leave_type` | Leave Type | Link→Leave Type | [O] | stock optional + no PS flip |
| `amended_from` | Amended From | Link→Leave Ledger Entry | [O] | stock optional + no PS flip |
| `transaction_type` | Transaction Type | Link→DocType | [O] | stock optional + no PS flip |
| `transaction_name` | Transaction Name | Dynamic Link | [O] | stock optional + no PS flip |
| `leaves` | Leaves | Float | [O] | stock optional + no PS flip |
| `from_date` | From Date | Date | [O] | stock optional + no PS flip |
| `to_date` | To Date | Date | [O] | stock optional + no PS flip |
| `is_carry_forward` | Is Carry Forward | Check | [O] | stock optional + no PS flip |
| `is_expired` | Is Expired | Check | [O] | stock optional + no PS flip |
| `is_lwp` | Is Leave Without Pay | Check | [O] | stock optional + no PS flip |
| `holiday_list` | Holiday List | Link→Holiday List | [O] | stock optional + no PS flip |
| `company` | Company | Link→Company | [R] | stock JSON reqd=1 |
## Section 7: Gotcha Index

10 gotchas from `migrate_master_data.py` + any new gotchas discovered during this research.

### GOTCHA #1 — `get_doc()` requires the `doctype` key

- **What:** Calling `frappe.get_doc(payload)` with only record fields (no `'doctype'` key) raises `ValidationError: doc(dict) does not have a valid 'doctype'`.
- **Fix:** Always inject `{'doctype': dt, **payload}` before constructing a new document.
- **Templates that need to document this:** All 22 (every template that drives an `insert` will hit this if a future subagent hand-rolls the import script)

### GOTCHA #2 — Company default accounts depend on Account existing first

- **What:** `default_bank_account`, `default_receivable_account`, `default_payable_account`, `default_expense_account`, `default_income_account`, `default_cost_center`, and 9 more Link fields on Company all point at Accounts / Cost Centers that the script creates LATER.
- **Fix:** Insert Company with identity fields only; attach default-account links via `frappe.db.set_value` after Accounts/Cost Centers exist.
- **Templates that need to document this:** Company (template not in P5 scope but documented for traceability)

### GOTCHA #3 — Account root nodes are system-generated

- **What:** Accounts Receivable, Accounts Payable, Cash In Hand, etc. are auto-created by ERPNext on install (root_type set, parent_account=None). Trying to re-insert from prod export throws duplicate-key / parent-not-found.
- **Fix:** Detect `parent_account is None and root_type in {Asset,Liability,Equity,Income,Expense}` and skip.
- **Templates that need to document this:** (internal only — not exposed to client templates)

### GOTCHA #4 — `Shift Type` has `autoname = 'prompt'`

- **What:** Frappe does NOT auto-generate a name on insert; you must set `doc.name` explicitly.
- **Fix:** Upsert helper passes `name` back into the payload for inserts.
- **Templates that need to document this:** 07_shift_type

### GOTCHA #5 — Department / Item Group circular-root trap

- **What:** `All Departments` and `All Item Groups` are implicit root nodes created on app install. Trying to insert with `parent_department == 'All Departments'` raises `ParentNotFoundError`.
- **Fix:** Skip rows whose parent equals the root sentinel.
- **Templates that need to document this:** 01_department (template must use company abbreviation in name OR rely on auto-suffix — see Section 5.3 sample)

### GOTCHA #6 — Employee requires `gender` and `default_shift` (with `mandatory_depends_on`)

- **What:** Both fields use `mandatory_depends_on` in HRMS — the validate hook fires whenever the DocType is touched. If Gender / Shift Type masters are not migrated first, every Employee insert fails.
- **Fix:** Migrate Gender + Shift Type BEFORE Employee in MIGRATION_ORDER (already in place).
- **Templates that need to document this:** 10_employee (template must show default_shift as required because it is for Haritha); 03_employment_type, 07_shift_type (must come before Employee in client handoff order)

### GOTCHA #7 — Prod and dev Employee IDs do not align

- **What:** Prod uses `HR-EMP-00211` etc.; dev (after migration) uses `HR-EMP-00002`–. The `employee_name` is preserved across sites.
- **Fix:** Remap any Link field referencing an Employee by `employee_name` before insert.
- **Templates that need to document this:** 10_employee, 15_shift_assignment (must allow remap), 18_leave_application

### GOTCHA #8 — Shift Schedule needs `repeat_on_days` child table + explicit `name`

- **What:** Two obstacles: (a) `/api/resource/<DT>?fields=['*']` strips child rows from list-view responses (so the fetch step must re-fetch each record individually); (b) `autoname='prompt'` means the `name` must be pinned.
- **Fix:** Fetch individual records in companion step; pin `payload['name'] = name` on insert.
- **Templates that need to document this:** 09_shift_schedule

### GOTCHA #9 — Shift Assignment has two out-of-scope Link fields

- **What:** Every SA references a `Shift Location` (`Hyderabad` is the only one used) and a `Shift Schedule Assignment` (420 unique SSAs not migrated).
- **Fix:** Pre-create Shift Location `Hyderabad` and NULLIFY `shift_schedule_assignment` on every SA before upsert. Also: Shift Request must come before Shift Assignment (one SA links back to an SR — `HR-SHA-26-08-05318`).
- **Templates that need to document this:** 08_shift_location, 16_shift_assignment (column `shift_location` required = `Hyderabad` in Haritha's case)

### GOTCHA #10 — Shift Request `validate_approver()` is unconditional AND autoname series silently overrides explicit name

- **What:** (a) `validate_approver()` runs regardless of docstatus; requires the record's `approver` to appear in the department's `shift_request_approver` list. (b) `autoname='HR-SHR-.YY.-.MM.-.#####'` ignores the explicit `name` unless the Series counter is past it.
- **Fix:** (a) Pre-seed Department Approver rows with `approver='Administrator'` + `parentfield='shift_request_approver'`, insert as `docstatus=0, status='Draft'`, then promote via `frappe.db.set_value(update_modified=False)`. (b) Pre-bump `tabSeries.current` to `target_number-1` for the matching `HR-SHR-YY-MM-` prefix.
- **Templates that need to document this:** 16_shift_request (rare in scope but important for 18_leave_application's analogous approver pattern)

### New gotchas discovered during Phase 0 research (not in `migrate_master_data.py`)

### NEW GOTCHA #11 — Department name auto-appends ` - <company-abbr>` on save

- **What:** Frappe stock behavior: when a Department is saved under a Company, the name automatically becomes `<name> - <abbr>` (e.g. `Nursing - HH`). Verified in Section 5.3 sample data. This is NOT a bug — it is enforced by the `Department` controller.
- **Fix:** Templates should either (a) accept the bare `Nursing` form and let Frappe append the suffix, or (b) require clients to enter the full `Nursing - HH` form. **Recommended:** option (a) — bare name in CSV, Frappe normalizes on import.
- **Templates that need to document this:** 01_department

### NEW GOTCHA #12 — Branch DocType is unused at Haritha (0 records)

- **What:** Branch is a stock DocType but Haritha has zero Branch records (single-site hospital). Employee records confirm: `branch=None` on every sample. Branch is also absent from MIGRATION_ORDER.
- **Fix:** **Templates for Branch should be marked 'OPTIONAL / NOT USED AT HARITHA'** with a note that Branch is a no-op for the Haritha deployment. The Branch DocType IS available for multi-site clients — the template should still exist but be clearly marked as 'skip if single-site'.
- **Templates that need to document this:** 05_branch

### NEW GOTCHA #13 — Employee Grade DocType is unused at Haritha (0 records)

- **What:** Like Branch, Employee Grade exists but has 0 records. Every Employee sample shows `grade=None`.
- **Fix:** Templates for Employee Grade should be marked 'AVAILABLE BUT NOT POPULATED' — column can be added to the Employee template as OPTIONAL.
- **Templates that need to document this:** 04_employee_grade, 10_employee (`grade` column)

### NEW GOTCHA #14 — Leave module is configured but no live transactions

- **What:** 7 Leave Types exist (Casual, Sick, Earned, LWP, Maternity, Paternity, Compensatory) but 0 Leave Policies, 0 Leave Periods, 0 Leave Allocations, 0 Leave Applications, 0 Leave Ledger Entries. Migration script does NOT migrate leave data either.
- **Fix:** Templates for the 5 leave transaction DocTypes should still be built (so the templates exist for future use) but with synthetic example data. Leave Allocation / Application / Ledger templates will only become useful when Haritha starts entering leave transactions.
- **Templates that need to document this:** 11_leave_type, 12_leave_policy, 13_leave_period, 14_leave_allocation, 18_leave_application, 19_leave_ledger_entry

### NEW GOTCHA #15 — Shift Location is `Hyderabad` only (single-site)

- **What:** Only one Shift Location exists (`Hyderabad` with lat=17.385, lon=78.4867, radius=200m). All 7,829 Shift Assignments link to this one location.
- **Fix:** Shift Location template should include only ONE row (Hyderabad) with a note that adding more locations requires updating `radius`/`latitude`/`longitude` for each site. For multi-site clients, the template becomes a copy-row template.
- **Templates that need to document this:** 08_shift_location, 16_shift_assignment (default `shift_location='Hyderabad'`)

### NEW GOTCHA #16 — Shift Type naming follows internal code convention not stock-required

- **What:** Haritha uses 25 Shift Type codes like `G0900R0830` (G=General, 0900=start, R=returns, 0830=duration). This is NOT enforced by Frappe — it's an internal convention. Stock allows any string as `name`.
- **Fix:** Shift Type template should explain the convention AND allow arbitrary string names. Include 2-3 example rows showing the pattern. Template MUST clarify that `name` is the shift code used by Employee Checkin devices.
- **Templates that need to document this:** 07_shift_type

### NEW GOTCHA #17 — Holiday List weekly_off is stored as a STRING, not an index

- **What:** Stock `weekly_off` field is a Select with values 'Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'. Confirmed: Haritha's single Holiday List has `weekly_off='Sunday'` (full string).
- **Fix:** Holiday List template's `weekly_off` column accepts the day NAME not a numeric index.
- **Templates that need to document this:** 06_holiday_list
## Section 8: Open Questions for Main Session

Items I could NOT determine from the 5 sources alone. Each is marked `?` in the Section 6 matrix where applicable.

### Q? — 07_shift_type

**Question:** Should the `color` Select on Shift Type expose the FULL property-setter options list (Blue, Cyan, Fuchsia, Green, Lime, Orange, Pink, Red, Violet — 9 colors) or only the 7-color stock list? Confirmed via Section 2: the property setter extended `options`. Templates should include all 9 colors in the example values.

### Q? — 10_employee

**Question:** `gender` is marked required (stock + migration script), but Haritha uses `Not Specified` for all imported rows. Should the template default to `Not Specified` for new clients or expose all 4 stock options? Recommend: expose all (Male/Female/Other/Not Specified) but allow Not Specified as a valid choice for hospital/healthcare contexts where gender may be unstated.

### Q? — 10_employee

**Question:** `holiday_list` is stock-optional but every Haritha Employee points to `Haritha Hospitals Holiday List`. Should the template mark this as required (functionally) or optional (stock)? Recommend: stock-optional but with a strong example value showing the Holiday List name.

### Q? — 15_shift_assignment

**Question:** `end_date` is stock-optional. Confirmed: every Haritha SA has `end_date` set (5-day work-week pattern). Should template mark as functionally required? Recommend: optional (single-day assignments exist conceptually) but example shows 5-day range.

### Q? — 15_shift_assignment

**Question:** `shift_schedule_assignment` is a Link to a DocType that is OUT OF SCOPE for Haritha (per GOTCHA #9). Should the template even include this column at all? Recommend: OMIT from CSV (clients don't need to fill it; the migration script NULLIFIES it anyway). Document in the .md that this field is reserved for future Schedule-Driven assignments.

### Q? — 16_attendance

**Question:** DocType samples show `docstatus=2` (cancelled). Live attendance records are presumably `docstatus=1`. Should the template expect client to submit attendance? Recommend: template marks `attendance_date`, `status`, `employee`, `shift` as required (matching Section 6 matrix) but does NOT pre-fill docstatus — Frappe Data Import handles that.

### Q? — 17_employee_checkin

**Question:** Series prefix in samples is `HR-CHECKIN-<row>-<seq>` (e.g. `HR-CHECKIN-1-000001`). This is a CUSTOM series format — stock `naming_series` is not visible in the JSON. Is this set via property setter? Recommend: investigate HRMS `naming_series` defaults in Property Setter (full set, not just filtered ones) before finalizing the Checkin template's `name` column.

### Q? — 06_holiday_list

**Question:** `weekly_off` is stock-optional but Haritha always sets it. Template should probably mark it as required. Confirm: stock-required? No (Section 6 marks [O]). Functionally-required? Yes. Templates should mark as `required if holidays span multiple years`.

### Q? — 01_department

**Question:** `company` is stock-required. Should the template assume a single Company (Haritha Hospitals) and pre-fill, or expose it as a required field? Recommend: expose as required so the template works for multi-company deployments.

### Q? — 04_employee_grade

**Question:** DocType is unused at Haritha. Should the template be: (a) built fully and marked as 'OPTIONAL', (b) skipped entirely, (c) marked as 'NOT USED' with a stub CSV? Recommend: option (c) — stub CSV with header row only + .md explaining it's available but not populated.

### Q? — 12_leave_policy / 13_leave_period / 14_leave_allocation / 18_leave_application / 19_leave_ledger_entry

**Question:** All 5 leave transaction DocTypes have 0 prod records. Should templates be built as full schemas (so they're ready when Haritha activates leave), or as stubs (header-only CSVs)? Recommend: full schemas for Leave Policy, Leave Period, Leave Allocation, Leave Application; stub for Leave Ledger Entry (which is system-generated, not user-editable).

### Q? — ALL

**Question:** Should templates use the `'field' (string)` or `Link→DocType (dropdown)` style for Link fields in the CSV? Confirm with main session: existing templates in `01_master_data/` use which style? Recommend: `Link (dropdown)` for user-fillable CSVs, `Link→DocType` for .md table reference.
