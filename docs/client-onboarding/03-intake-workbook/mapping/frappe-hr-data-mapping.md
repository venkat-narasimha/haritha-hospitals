# Frappe HR Data Mapping — Client Intake to the Target Site

> **Purpose:** When a client provides Excel/CSV files, this document is the
> bridge between their column headers and the team's Frappe HR DocType fields.
> Each section maps one template (CSV file) to its destination DocType with
> field-by-field semantics and known gotchas.

> **Source-of-truth:** `scripts/migrate_master_data.py` (the actual code that
> writes records to the target site). This doc mirrors its field access
> patterns (`upsert()`, `_migrate_company()`, `_migrate_shift_schedule()`,
> `_migrate_shift_request()`, `_migrate_shift_assignment()`).

> **Template convention:** CSV files in
> `docs/client-onboarding/03-intake-workbook/01_master_data/` are numbered
> `NN_<doctype>.csv`. The corresponding `.md` next to each CSV explains
> column meanings and gotchas in prose.

> **Last updated:** 2026-09-15 (post-audit; gotchas #4–#10 surfaced)

---

## Conventions

- **Required fields:** Without these, `frappe.get_doc({...}).insert()` raises
  `ValidationError` or `LinkValidationError`. Marked **[R]** in each table.
- **Link fields:** Values must match an existing record's `name` in the linked
  DocType (case-sensitive on Linux MariaDB per Gotcha #6).
- **Date formats:** `YYYY-MM-DD` accepted; other formats require preprocessing.
- **Time formats:** `HH:MM:SS`, 24-hour clock.
- **Column → Frappe field mapping:** In almost every template the CSV
  `fieldname` column IS the Frappe fieldname. Where it differs (because the
  Frappe DocType uses `autoname = "field:<csv-column>"` so the document's
  primary `name` is populated from a different column), the table makes the
  remap explicit.
- **Generic examples:** All example values below are illustrative placeholders
  (e.g., `"Department A"`, `"EMP-XXXX"`, `"Site A"`); do not reference real
  client data.

---

## 1. Department → `tabDepartment`

Source CSV: `01_department.csv`

**Autoname:** `field:department_name` — the department's primary `name` is
populated from the CSV column `department_name`. The CSV does NOT include
separate `company`, `payroll_cost_center`, or `approvers` (child) columns;
those are configured per-Company or seeded by the migration script.

| CSV column          | Frappe HR field   | Type    | Required | Gotcha |
|---------------------|-------------------|---------|----------|--------|
| `department_name`   | `name`            | Data    | **[R]**  | Unique per Company. **Gotcha #5:** migration script SKIPS rows whose `parent_department` equals the literal sentinel `"All Departments"` (script line 305, `DEPARTMENT_ROOT` line 221). Skip root nodes silently — do not import the implicit Frappe root. |
| `company`           | `company`         | Link    | **[R]**  | Must reference existing `tabCompany.name`. Set per-site at run time; not auto-derived from CSV in single-tenant deploys. |
| `parent_department` | `parent_department` | Link  |          | Must reference existing `tabDepartment.name`. Empty = root. **Gotcha #5:** value `"All Departments"` will be dropped by the script. |
| `is_group`          | `is_group`        | Check   |          | `0`/`1`. Set to `1` for nodes that have children; Frappe then allows child Departments to point at it. |
| `leave_block_list`  | `leave_block_list` | Link   |          | Must reference existing `tabLeave Block List`. Single value (no multi-select). |
| `department_code`   | `department_code` | Data    |          | Short code for HR reports (e.g., `"CARD"`). Free-form. |
| `building`          | `building`        | Data    |          | Free-form text (e.g., `"Main Block - 2nd Floor"`). Drives signage / geofencing hints. |
| `hod`               | `hod`             | Link    |          | Must reference existing `tabEmployee.name`. Left empty if no HOD assigned yet. |

**Migration-script-driven additions (not in CSV):**

- `Department Approver` child rows are pre-seeded by
  `_ensure_department_approvers()` (script line 420) BEFORE `Shift Request`
  inserts run, so `ShiftRequest.validate_approver()` passes on the target
  site. See **Gotcha #10** in Appendix A.

---

## 2. Designation → `tabDesignation`

Source CSV: `02_designation.csv`

**Autoname:** `field:designation_name` — `name` is populated from the CSV
column `designation_name`.

| CSV column             | Frappe HR field            | Type    | Required | Gotcha |
|------------------------|----------------------------|---------|----------|--------|
| `designation_name`     | `name`                     | Data    | **[R]**  | Unique. Used as `tabEmployee.designation` Link value. |
| `description`          | `description`              | Text    |          | Plain text. |
| `clinical_role`        | `clinical_role`            | Select  |          | One of `Doctor` / `Nurse` / `Technician` / `Support` / `Admin`. Custom field — verify client has added it before import. |
| `requires_registration`| `requires_registration`    | Check   |          | `0`/`1`. When `1`, the script expects a medical registration number on the linked Employee (template 10 fields `medical_council_reg_no`, `reg_validity_date`). |
| `min_qualification`    | `min_qualification`        | Data    |          | Plain text (e.g., `"MBBS, MD"`). |
| `appraisal_template`   | `appraisal_template`       | Link    |          | Must reference existing `tabAppraisal Template` if set. |

> **Standard upsert path** (`scripts/migrate_master_data.py` `upsert()` line
> 314). No gotchas touch this DocType.

---

## 3. Employment Type → `tabEmployment Type`

Source CSV: `03_employment_type.csv`

**Autoname:** `field:name` — `name` column maps directly to Frappe `name`.

| CSV column     | Frappe HR field | Type    | Required | Gotcha |
|----------------|-----------------|---------|----------|--------|
| `name`         | `name`          | Data    | **[R]**  | Unique. Referenced by `tabEmployee.employment_type`. |
| `description`  | `description`   | Text    |          | Plain text. |

> **Standard upsert path.** No special handling.

---

## 4. Employee Grade → `tabEmployee Grade`

Source CSV: `04_employee_grade.csv`

**Autoname:** `field:grade_name` — `name` is populated from `grade_name`.

| CSV column        | Frappe HR field  | Type     | Required | Gotcha |
|-------------------|------------------|----------|----------|--------|
| `grade_name`      | `name`           | Data     | **[R]**  | Unique. Referenced by `tabEmployee.grade`. |
| `description`     | `description`    | Text     |          | Plain text. |
| `default_currency`| `default_currency`| Link    |          | Must reference existing `tabCurrency` (e.g., `"INR"`). |
| `min_salary`      | `min_salary`     | Currency |          | Numeric, ≥ 0. No currency symbol, no thousands separator. |
| `max_salary`      | `max_salary`     | Currency |          | Numeric, ≥ `min_salary`. |
| `pay_band`        | `pay_band`       | Data     |          | Free-form text for grouping (e.g., `"Clinical-Band-2"`). Drives Leave Policy mapping in the MD. |

> **Standard upsert path.** No special handling.

---

## 5. Branch → `tabBranch`

Source CSV: `05_branch.csv`

**Autoname:** `field:branch` — `name` is populated from the CSV column
`branch`.

| CSV column      | Frappe HR field | Type    | Required | Gotcha |
|-----------------|-----------------|---------|----------|--------|
| `branch`        | `name`          | Data    | **[R]**  | Unique. The Branch site's primary name. |
| `company`       | `company`       | Link    |          | Must reference existing `tabCompany`. |
| `branch_code`   | `branch_code`   | Data    |          | Short code (e.g., `"MAIN"`). |
| `branch_type`   | `branch_type`   | Select  |          | One of `Hospital` / `Clinic` / `Lab` / `Pharmacy` / `Office`. |
| `state`         | `state`         | Link    |          | Must reference existing `tabState` (drives default Holiday List). |
| `city`          | `city`          | Data    |          | Plain text. |
| `pincode`       | `pincode`       | Data    |          | 6-digit Indian pincode. |
| `latitude`      | `latitude`      | Float   |          | `-90` to `90`. |
| `longitude`     | `longitude`     | Float   |          | `-180` to `180`. |
| `bed_count`     | `bed_count`     | Int     |          | Non-negative integer. |

> **Standard upsert path.** The audit report (AUDIT-REPORT.md, template 05)
> mentions a custom `nabh_accredited` column that the script-handled
> payload supports; it is NOT a column in `05_branch.csv` on disk. Treat as
> optional custom field if the client has it.

---

## 6. Holiday List → `tabHoliday List` (+ child `tabHoliday`)

Source CSV: `06_holiday_list.csv`

**Autoname:** `field:holiday_list_name` — `name` from the CSV column
`holiday_list_name`. Child rows (rows 8–9 in the CSV header) become
`tabHoliday` records linked to the parent.

| CSV column          | Frappe HR field   | Type    | Required | Gotcha |
|---------------------|-------------------|---------|----------|--------|
| `holiday_list_name` | `name`            | Data    | **[R]**  | Unique. |
| `from_date`         | `from_date`       | Date    | **[R]**  | `YYYY-MM-DD`. |
| `to_date`           | `to_date`         | Date    | **[R]**  | `YYYY-MM-DD`. Must satisfy `to_date ≥ from_date`. |
| `country`           | `country`         | Link    |          | Must reference existing `tabCountry`. Auto-fills state list. |
| `subdivision`       | `subdivision`     | Link    |          | Must reference existing `tabState`/`tabProvince`. |
| `weekly_off`        | `weekly_off`      | Select  |          | One of `Sun`–`Sat`. |
| `holiday_date (child)` | `holiday_date` | Date    | **[R]** (per child row) | Must fall within the parent's `from_date`/`to_date`. |
| `description (child)`  | `description`  | Data    | **[R]** (per child row) | Plain text. |
| `applicable_to`     | `applicable_to`   | Select  |          | One of `All` / `Doctors` / `Nurses` / `Admin`. **Caveat (AUDIT §3):** this is a custom field — verify the client has added it to their Holiday List DocType, otherwise the column will be silently dropped by `_clean_payload()` (script line 320). |

> **Standard upsert path** for both parent (`tabHoliday List`) and the
> implicit `tabHoliday` child rows when the script processes the child table.

---

## 7. Shift Type → `tabShift Type`

Source CSV: `07_shift_type.csv`

**Autoname:** `prompt` — `name` is a free-form prompt column in the CSV. The
migration script **pins `name` explicitly** on every row (see
`PROMPT_AUTONAME_DOCTYPES` set, script line 227, and the `name`-pining branch
inside `upsert()`, line 314+).

| CSV column                              | Frappe HR field                     | Type   | Required | Gotcha |
|-----------------------------------------|-------------------------------------|--------|----------|--------|
| `name`                                  | `name`                              | Data   | **[R]**  | **Gotcha #4:** must be non-empty. Without it Frappe raises `ValidationError: Naming Series 'prompt' is invalid` on insert. |
| `start_time`                            | `start_time`                        | Time   | **[R]**  | `HH:MM:SS`, 24h. |
| `end_time`                              | `end_time`                          | Time   | **[R]**  | `HH:MM:SS`. `end_time < start_time` is allowed and means the shift spans midnight (night shift). |
| `color`                                 | `color`                             | Select |          | One of the named Frappe HR colors (e.g., `Blue`, `Cyan`, …). Drives roster-UI coloring. |
| `enable_auto_attendance`                | `enable_auto_attendance`            | Check  |          | `0`/`1`. Drives the scheduler. |
| `process_attendance_after`              | `process_attendance_after`          | Date   |          | `YYYY-MM-DD`. **Required if `enable_auto_attendance=1`** — leaving it blank when auto-attendance is on causes the attendance scheduler to fail silently. |
| `working_hours_threshold_for_half_day`  | `working_hours_threshold_for_half_day` | Float |        | Hours; `0` disables. |
| `working_hours_threshold_for_absent`    | `working_hours_threshold_for_absent`  | Float |        | Hours; `0` disables. |
| `enable_late_entry_marking`             | `enable_late_entry_marking`         | Check  |          | `0`/`1`. |
| `late_entry_grace_period`               | `late_entry_grace_period`           | Int    |          | Minutes. |
| `enable_early_exit_marking`             | `enable_early_exit_marking`         | Check  |          | `0`/`1`. |
| `early_exit_grace_period`               | `early_exit_grace_period`           | Int    |          | Minutes. |
| `allow_overtime`                        | `allow_overtime`                    | Check  |          | `0`/`1`. |

**Order dependency — Gotcha #6.** `Shift Type` is migrated BEFORE
`Holiday List`, `Employee`, and `Shift Assignment` (see `MIGRATION_ORDER`,
script line 244). Every Employee's `default_shift` Link must resolve against
an already-existing Shift Type when Employee inserts run.

> The 15-field CSV is the canonical list; this table mirrors it 1:1.

---

## 8. Shift Location → `tabShift Location`

Source CSV: `08_shift_location.csv`

**Autoname:** `field:location_name` — `name` is populated from
`location_name`. Although `field:`-autoname DocTypes generally don't need
explicit name pinning, `Shift Location` is included in
`PROMPT_AUTONAME_DOCTYPES` (line 227) so the migration script always pins
`name` explicitly on insert (defensive coding against schema drifts).

| CSV column                       | Frappe HR field            | Type   | Required | Gotcha |
|----------------------------------|----------------------------|--------|----------|--------|
| `location_name`                  | `name`                     | Data   | **[R]**  | Unique. |
| `latitude`                       | `latitude`                 | Float  | **[R]**  | `-90` to `90`. |
| `longitude`                      | `longitude`                | Float  | **[R]**  | `-180` to `180`. |
| `checkin_radius`                 | `checkin_radius`           | Int    |          | Meters; 50–200 typical indoors, 500+ for campus. |
| `address`                        | `address`                  | Text   |          | Plain text. |
| `zone_type`                      | `zone_type`                | Select |          | One of `ICU` / `OT` / `Ward` / `OPD` / `Casualty` / `Lab` / `Pharmacy` / `Admin`. |
| `floor`                          | `floor`                    | Data   |          | Free-form (e.g., `"2nd"`). |
| `requires_late_attendance_alert` | `requires_late_attendance_alert` | Check |     | `0`/`1`. |

**Gotcha #9 — pre-create requirement.** The migration script
**pre-creates** a single canonical Shift Location (via
`_ensure_shift_location()`, script line 399) before processing any Shift
Assignment. The current call hardcodes the canonical name; see Gotcha #9 in
Appendix A for what changes if the client uses a different location name.

---

## 9. Shift Schedule → `tabShift Schedule` (+ child `tabAssignment Rule Day` / `tabShift Assignment`)

Source CSV: `09_shift_schedule.csv`

**Autoname:** `prompt` — `name` is a free-form prompt column. The migration
script's `_migrate_shift_schedule()` (line 452) explicitly pins `name` on
insert (Gotcha #8 part A) AND re-appends `repeat_on_days` child rows via
`doc.append()` (Gotcha #8 part B), because the standard
`fields=["*"]` list-view payload strips child-table rows.

| CSV column                 | Frappe HR field         | Type   | Required | Gotcha |
|----------------------------|-------------------------|--------|----------|--------|
| `shift_type`               | `shift_type`            | Link   | **[R]**  | Must reference existing `tabShift Type`. |
| `from_date`                | `from_date`             | Date   | **[R]**  | `YYYY-MM-DD`. |
| `to_date`                  | `to_date`               | Date   | **[R]**  | `YYYY-MM-DD`. Must satisfy `to_date ≥ from_date`. |
| `frequency`                | `frequency`             | Select | **[R]**  | One of `Every 1 Week` / `Every 2 Weeks` / `Every 3 Weeks` / `Every 4 Weeks`. |
| `company`                  | `company`               | Link   |          | Must reference existing `tabCompany`. |
| `department`               | `department`            | Link   |          | Must reference existing `tabDepartment`. |
| `enable_auto_shift_schedule` | `enable_auto_shift_schedule` | Check |     | `0`/`1`. Setting to `1` enables the auto-create scheduler; it does **not** retroactively create historical assignments. |
| `day (child)`              | `day`                   | Select | **[R]** (at least one) | One of `Monday`–`Sunday`. Child rows are lost on `fields=["*"]` list payloads — `_migrate_shift_schedule()` re-appends them via `doc.append()` (script line 480). |
| `employee (child)`         | `employee`              | Link   | **[R]** (per row) | Must reference existing `tabEmployee`. |
| `shift_type (child)`       | `shift_type`            | Link   | **[R]** (per row) | Must reference existing `tabShift Type`. |
| `start_date (child)`       | `start_date`            | Date   | **[R]** (per row) | `YYYY-MM-DD`. |
| `end_date (child)`         | `end_date`              | Date   |          | `YYYY-MM-DD`. Blank = ongoing. |
| `shift_location (child)`   | `shift_location`        | Link   |          | Must reference existing `tabShift Location` if set. See Gotcha #9 — canonical name pre-created by `_ensure_shift_location()`. |
| `status (child)`           | `status`                | Select |          | `Active` / `Inactive`. |

---

## 10. Employee → `tabEmployee`

Source CSV: `10_employee.csv`

**Autoname:** Client-target dependent. The Employee `name` is the primary
identifier used as the Link value across `tabShift Assignment.employee`,
`tabLeave Allocation.employee`, etc. The CSV does **not** include a `name`
column — the script derives `name` from the per-site Employee ID convention
documented in `employee_number` (the human-readable badge) per the audit.
Client intake MUST include both `employee_name` (display name) and
`employee_number` (badge) so the dev-side ID remap works (see **Gotcha #7**).

| CSV column                 | Frappe HR field            | Type   | Required | Gotcha |
|----------------------------|----------------------------|--------|----------|--------|
| `employee_name`            | `employee_name`            | Data   | **[R]**  | Display name (e.g., `"Employee A"`). **Join key for prod → dev ID remap (Gotcha #7).** MUST be non-empty. |
| `employee_number`          | `employee_number`          | Data   | **[R]**  | Badge ID (e.g., `"EMP-XXXX"`). Unique. |
| `first_name`               | `first_name`               | Data   | **[R]**  | First name. |
| `last_name`                | `last_name`                | Data   |          | Last name. |
| `gender`                   | `gender`                   | Link   | **[R]**  | Must reference existing `tabGender` (**Gotcha #6** — Gender must migrate before Employee). |
| `date_of_birth`            | `date_of_birth`            | Date   | **[R]**  | `YYYY-MM-DD`. Must be ≤ today. |
| `date_of_joining`          | `date_of_joining`          | Date   | **[R]**  | `YYYY-MM-DD`. |
| `status`                   | `status`                   | Select | **[R]**  | One of `Active` / `Suspended` / `Left` / `Permanently Disabled`. |
| `company`                  | `company`                  | Link   | **[R]**  | Must reference existing `tabCompany`. |
| `department`               | `department`               | Link   |          | Must reference existing `tabDepartment`. |
| `designation`              | `designation`              | Link   |          | Must reference existing `tabDesignation`. |
| `employment_type`          | `employment_type`          | Link   |          | Must reference existing `tabEmployment Type`. |
| `branch`                   | `branch`                   | Link   |          | Must reference existing `tabBranch`. |
| `grade`                    | `grade`                    | Link   |          | Must reference existing `tabEmployee Grade`. |
| `reports_to`               | `reports_to`               | Link   |          | Must reference existing `tabEmployee.name` if set. |
| `leave_approver`           | `leave_approver`           | Link   |          | Must reference existing `tabUser.email` if set. |
| `default_shift`            | `default_shift`            | Link   |          | Must reference existing `tabShift Type`. **Gotcha #6** — Shift Type must migrate before Employee. |
| `attendance_device_id`     | `attendance_device_id`     | Data   |          | Unique biometric ID if set. |
| `holiday_list`             | `holiday_list`             | Link   |          | Must reference existing `tabHoliday List`. Defaults from Company. |
| `cell_number`              | `cell_number`              | Data   |          | E.164-style; `"+CC-NNNNNNNNNN"`. |
| `personal_email`           | `personal_email`           | Data   |          | Valid email. One of `personal_email` or `company_email` REQUIRED for User provisioning. |
| `company_email`            | `company_email`            | Data   |          | Valid email. One of `personal_email` or `company_email` REQUIRED for User provisioning. |
| `blood_group`              | `blood_group`              | Select |          | One of the standard groups (e.g., `O+`, `B+`). **REQUIRED for clinical staff** (Doctor/Nurse). |
| `medical_council_reg_no`    | `medical_council_reg_no`   | Data   |          | **REQUIRED for doctors** (linked to `Designation.requires_registration=1`). |
| `reg_validity_date`        | `reg_validity_date`        | Date   |          | `YYYY-MM-DD`. |
| `specialization`           | `specialization`           | Data   |          | Free-form text. |
| `emergency_contact_name`   | `emergency_contact_name`   | Data   |          | **REQUIRED for clinical staff**. |
| `emergency_phone_number`   | `emergency_phone_number`   | Data   |          | **REQUIRED for clinical staff**. |
| `next_of_kin`              | `next_of_kin`              | Data   |          | Free-form (e.g., `"Spouse"`). |

---

## 11. Leave Type → `tabLeave Type`

Source CSV: `11_leave_type.csv`

**Autoname:** `field:name` — `name` maps directly to Frappe `name`.

| CSV column                                | Frappe HR field                          | Type   | Required | Gotcha |
|-------------------------------------------|------------------------------------------|--------|----------|--------|
| `name`                                    | `name`                                   | Data   | **[R]**  | Unique. Referenced by `tabLeave Allocation.leave_type`. |
| `max_leave_allocation_allowed`            | `max_leave_allocation_allowed`           | Int    |          | ≥ 0. |
| `applicable_after`                        | `applicable_after`                       | Int    |          | Working days; ≥ 0. |
| `max_consecutive_leaves_allowed`          | `max_consecutive_leaves_allowed`         | Int    |          | ≥ 0. |
| `is_carry_forward`                        | `is_carry_forward`                       | Check  |          | `0`/`1`. |
| `carry_forward_leaves_limit`              | `carry_forward_leaves_limit`             | Int    |          | ≥ 0. |
| `earned_leave`                            | `earned_leave`                           | Check  |          | `0`/`1`. |
| `earned_leave_frequency`                  | `earned_leave_frequency`                 | Select |          | One of `Monthly` / `Quarterly` / `Half-Yearly` / `Yearly`. |
| `is_leave_without_pay`                    | `is_leave_without_pay`                   | Check  |          | `0`/`1`. Mutually exclusive with `is_partially_paid_leaves`. |
| `is_partially_paid_leaves`                | `is_partially_paid_leaves`               | Check  |          | `0`/`1`. Mutually exclusive with `is_leave_without_pay`. |
| `fraction_of_daily_salary_per_leave`      | `fraction_of_daily_salary_per_leave`     | Float  |          | `0.0` to `1.0`. |
| `is_optional_leaves`                      | `is_optional_leaves`                     | Check  |          | `0`/`1`. |
| `max_days_leave_allowed`                  | `max_days_leave_allowed`                 | Int    |          | ≥ 0. |
| `allow_negative_balance`                  | `allow_negative_balance`                 | Check  |          | `0`/`1`. |
| `allow_over_allocation`                   | `allow_over_allocation`                  | Check  |          | `0`/`1`. Does NOT override `max_leave_allocation_allowed`. |
| `include_holidays_within_leaves_as_leaves`| `include_holidays_within_leaves_as_leaves`| Check |          | `0`/`1`. |
| `is_compensatory`                         | `is_compensatory`                        | Check  |          | `0`/`1`. |
| `allow_encashment`                        | `allow_encashment`                       | Check  |          | `0`/`1`. |
| `requires_medical_certificate`            | `requires_medical_certificate`           | Check  |          | `0`/`1`. For Sick Leave > 2 days. |

> **Standard upsert path.** No gotchas touch this DocType.

---

## 12. Leave Policy → `tabLeave Policy` (+ child `tabLeave Policy Detail`)

Source CSV: `12_leave_policy.csv`

**Autoname:** `field:title` — `name` is populated from the CSV column `title`.

| CSV column              | Frappe HR field       | Type   | Required | Gotcha |
|-------------------------|-----------------------|--------|----------|--------|
| `title`                 | `name`                | Data   | **[R]**  | Unique. |
| `leave_type (child)`    | `leave_type`          | Link   | **[R]** (per child row) | Must reference existing `tabLeave Type`. |
| `annual_allocation (child)` | `annual_allocation`| Float  | **[R]** (per child row) | Days; ≥ 0. |

> **Standard upsert path.** No gotchas touch this DocType.

---

## 13. Leave Period → `tabLeave Period`

Source CSV: `13_leave_period.csv`

**Autoname:** Document name is derived from `from_date`/`to_date` (Frappe
default). The CSV does not include a separate `name` column.

| CSV column   | Frappe HR field | Type   | Required | Gotcha |
|--------------|-----------------|--------|----------|--------|
| `from_date`  | `from_date`     | Date   | **[R]**  | `YYYY-MM-DD`. |
| `to_date`    | `to_date`       | Date   | **[R]**  | `YYYY-MM-DD`. Must satisfy `to_date > from_date`. |
| `is_active`  | `is_active`     | Check  | **[R]**  | `0`/`1`. Only one active per Company. |
| `company`    | `company`       | Link   |          | Must reference existing `tabCompany`. |
| `fiscal_year`| `fiscal_year`   | Link   |          | Must reference existing `tabFiscal Year`. |

---

## 14. Leave Allocation → `tabLeave Allocation`

Source CSV: `14_leave_allocation.csv`

**Autoname:** Frappe default (naming series based). The CSV does not include
a separate `name` column.

| CSV column                | Frappe HR field        | Type   | Required | Gotcha |
|---------------------------|------------------------|--------|----------|--------|
| `employee`                | `employee`             | Link   | **[R]**  | Must reference existing `tabEmployee`. |
| `leave_type`              | `leave_type`           | Link   | **[R]**  | Must reference existing `tabLeave Type`. |
| `from_date`               | `from_date`            | Date   | **[R]**  | `YYYY-MM-DD`. |
| `to_date`                 | `to_date`              | Date   | **[R]**  | `YYYY-MM-DD`. Must satisfy `to_date > from_date`. |
| `new_leaves_allocated`    | `new_leaves_allocated` | Float  | **[R]**  | Days; ≥ 0. |
| `leave_period`            | `leave_period`         | Link   |          | Must reference existing `tabLeave Period`. |
| `leave_policy`            | `leave_policy`         | Link   |          | Must reference existing `tabLeave Policy`. |
| `carry_forward`           | `carry_forward`        | Check  |          | `0`/`1`. |
| `unused_leaves`           | `unused_leaves`        | Float  |          | Days; ≥ 0. |
| `notes`                   | `notes`                | Text   |          | Reason for manual allocation. |

> **Standard upsert path.** No gotchas touch this DocType.

---

## 15. Shift Assignment → `tabShift Assignment`

Source CSV: `15_shift_assignment.csv`

**Autoname:** `prompt` — `name` is a free-form prompt column. The migration
script preserves whatever `name` is in the CSV (line 580, `_migrate_shift_assignment()`).

| CSV column                       | Frappe HR field                | Type   | Required | Gotcha |
|----------------------------------|--------------------------------|--------|----------|--------|
| `name`                           | `name`                         | Data   | **[R]**  | **Gotcha #4 + #7:** autoname='prompt' — must be non-empty. Acts as upsert key — re-runs UPDATE existing SA rows in place. |
| `employee`                       | `employee`                     | Link   | **[R]**  | Must reference existing `tabEmployee`. **Gotcha #7:** the script REMAPS this from the prod ID to the dev ID using `employee_name` as the join key (script line 591). Client CSV MUST supply both `employee` (prod-side, will be overwritten) and `employee_name` (the join key). |
| `employee_name`                  | `employee_name`                | Data   | **[R]**  | **Join key for the prod → dev ID remap.** MUST match `employee_name` on the migrated Employee exactly (case-sensitive — Gotcha #6). |
| `shift_type`                     | `shift_type`                   | Link   | **[R]**  | Must reference existing `tabShift Type`. |
| `company`                        | `company`                      | Link   | **[R]**  | Must reference existing `tabCompany`. Auto-fetched from Employee but supplied explicitly for safety. |
| `start_date`                     | `start_date`                   | Date   | **[R]**  | `YYYY-MM-DD`. |
| `end_date`                       | `end_date`                     | Date   |          | `YYYY-MM-DD`. Blank = ongoing. |
| `status`                         | `status`                       | Select |          | `Active` / `Inactive`. |
| `shift_location`                 | `shift_location`               | Link   |          | Must reference existing `tabShift Location` if set. **Gotcha #9:** the script pre-creates a single canonical Shift Location (via `_ensure_shift_location()`, line 399) before any SA insert. If the client uses a different name, populate `08_shift_location.csv` AND change `_ensure_shift_location()` to match. |
| `overtime_type`                  | `overtime_type`                | Link   |          | Must reference existing `tabOvertime Type` if set. |
| `shift_request`                  | `shift_request`                | Link   |          | Must reference existing `tabShift Request` if set. **Gotcha:** `Shift Request` is migrated BEFORE `Shift Assignment` (see `MIGRATION_ORDER`, line 244). If the linked SR exists on the target site, the Link is preserved; if not, it is dropped silently (Frappe does not raise on missing optional Links at `docstatus=0`). |
| `shift_schedule_assignment`      | `shift_schedule_assignment`    | Link   |          | **Gotcha #9:** the script NULLIFIES this field (`rec["shift_schedule_assignment"] = None`, line 593). Leave the column blank in the CSV — any non-empty value is discarded. The `Shift Schedule Assignment` DocType is out of scope. |
| `docstatus`                      | `docstatus`                    | Int    | **[R]**  | `0` = Draft, `1` = Submitted, `2` = Cancelled. The script preserves the source value so cancelled SA records can be migrated alongside active ones (`docstatus=2` rows are valid). |

---

## Appendix A — Gotcha Index (cross-reference)

Source-of-truth: `scripts/migrate_master_data.py` module docstring ("GOTCHAS
DISCOVERED") and AUDIT-REPORT.md "Gotcha Coverage Matrix".

The numbering #1–#10 follows the migration script's docstring. Gotchas #1–#3
are script-internal (no client CSV column maps to them); #4–#10 are
client-visible.

| #   | Gotcha                                                                                                  | Affected templates            | Migration script behavior (line)                                                                                |
|-----|---------------------------------------------------------------------------------------------------------|-------------------------------|------------------------------------------------------------------------------------------------------------------|
| #4  | Shift Type / Shift Location / Shift Schedule / Shift Assignment declare `autoname='prompt'`. The script pins `name` explicitly on insert. | 07, 08, 09, 15                | `PROMPT_AUTONAME_DOCTYPES` set (line 227); `upsert()` pins `payload["name"]` (line 314+). |
| #5  | Department (and Item Group) root-skip — rows whose parent equals `"All Departments"` (`"All Item Groups"`) are skipped because Frappe creates those roots implicitly on app install. | 01                            | `_should_skip_root_tree_node()` (line 305); sentinel constant `DEPARTMENT_ROOT` (line 221). |
| #6  | `Employee.gender` and `Employee.default_shift` are Link fields; both source DocTypes must be migrated first. Also: Link field values are case-sensitive on Linux MariaDB. | 07, 10                        | `MIGRATION_ORDER` ensures `Gender` and `Shift Type` come BEFORE `Employee` (line 244). |
| #7  | Prod and dev Employee IDs do not align after migration. The script REMAPS the `employee` field on Shift Request and Shift Assignment records using `employee_name` as the join key. | 10, 15                        | `_migrate_shift_request()` (line 532); `_migrate_shift_assignment()` (line 580). Both consume `dev_emp_by_name`, built once in `run()` (line ~705). |
| #8  | Shift Schedule autoname='prompt' + `repeat_on_days` child table is dropped by `fields=["*"]` list payloads. Script re-appends child rows via `doc.append()`. | 09                            | `_migrate_shift_schedule()` (line 452); child rows restored via `doc.append()` (~line 480). |
| #9  | Shift Assignment has two out-of-scope Link fields: `shift_schedule_assignment` (NULLIF'd) and `shift_location` (pre-created single record). The pre-create uses a hardcoded canonical name. | 08, 15                        | `_ensure_shift_location()` (line 399); `_migrate_shift_assignment()` NULLIF (line 593); `MIGRATION_ORDER` migrates Shift Request BEFORE Shift Assignment (line 244). |
| #10 | Shift Request `validate_approver()` runs unconditionally + autoname series silently overrides an explicit `name`. Script pre-seeds `Department Approver` rows for every referenced dept, then inserts as `docstatus=0, status="Draft"`, then promotes via `frappe.db.set_value()`. Also bumps `tabSeries.current` before insert. | 01, 15 (effect; template source root cause is the schema in `tabShift Request`/`tabDepartment`) | `_ensure_department_approvers()` (line 420); `_pre_set_shift_request_series()` (line 495); `_migrate_shift_request()` draft-insert-then-promote (line 532). |

> **#1–#3 are script-internal** (no client CSV column triggers them):
> - #1: `get_doc()` requires `doctype` key — handled in-script by `upsert()`.
> - #2: Company default-account dependencies on Account — Company is configured
>   in ERPNext directly, not via a client CSV template.
> - #3: Account root nodes skipped — Account is not a workbook template (system-generated).

---

## Appendix B — Validation Rules (apply to every CSV)

- **All `[R]` columns must be non-empty.** Blank required fields cause
  `frappe.get_doc({...}).insert()` to raise `ValidationError`.
- **All Link fields must reference an existing record's `name`** (case-sensitive
  on Linux MariaDB — per Gotcha #6). The migration script does NOT pre-create
  Link targets unless explicitly named in the script (`_ensure_shift_location`
  is the only documented pre-create).
- **Dates:** `YYYY-MM-DD` only. Other formats (`DD/MM/YYYY`, `MM-DD-YYYY`,
  Excel serial numbers) require preprocessing before import.
- **Times:** `HH:MM:SS`, 24-hour clock. `end_time < start_time` is allowed
  and means the shift spans midnight.
- **Numerics:** Integers or floats. No thousands separators, no currency
  symbols, no leading/trailing whitespace.
- **Booleans:** `0` or `1` only (not `true`/`false`, not `yes`/`no`).
- **Header row:** Column order MUST match the CSV `fieldname` header in the
  files under `01_master_data/` — the migration script iterates by
  `fieldname`. Reordering columns does not break the upsert path (which uses
  dict keys), but downstream consumers (Excel validators, dashboards) often
  rely on column order.
- **Empty data rows:** Skipped silently by the upsert path — not an error.
- **Encoding:** UTF-8, no BOM. Frappe ORM rejects BOM-prefixed CSVs on load.
- **Re-runs are safe:** The upsert helper uses
  `frappe.db.exists(dt, name) → get_doc + update + save` else
  `new_doc + insert`. Re-running after partial failure resumes at the missing
  records; existing records are updated in place (NOT duplicated, NOT
  rewritten destructively).
- **Per-DocType transaction:** One `frappe.db.commit()` per DocType per run —
  partial progress persists across re-runs.
- **`employee_name` join key integrity (templates 10 + 15):** Every Employee
  row MUST have a unique, non-empty `employee_name`. Every Shift Assignment
  row MUST carry `employee_name` matching an Employee `employee_name`
  case-sensitively — otherwise the prod → dev ID remap fails and the SA row
  is dropped with `LinkValidationError`.
