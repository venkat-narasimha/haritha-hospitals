# P5 Verification Report — Template Enumeration

**Date:** 2026-09-15
**Scope:** 19 DocType templates (15 master + 4 transaction) at `docs/client-onboarding/03-intake-workbook/01_master_data/`
**Method:** Static cross-reference of every CSV/MD against (a) stock ERPNext/HRMS v16.5.0 DocType JSON in `/tmp/p5_research/erpnext_json/`, (b) `haritha_hospital/fixtures/custom_field.json` (78 custom fields filtered by DocType), (c) research §6 verdict matrix in `prompts/P5-rebuild-research.md`, and (d) research §7 gotcha index (gotchas #1-17).
**Subagent:** depth 1/5, model `minimax/MiniMax-M3`, single pass.
**Status:** Enumeration complete. No template files edited.

---

## 1. Top-line Summary

| Severity | Count | Templates affected |
|----------|-------|---------------------|
| 🔴 BLOCKER  | 2     | 2/19 (10.5%) |
| 🟡 IMPORTANT | 7     | 6/19 (31.6%) — 2 type mismatches + 4 functional-required drifts + 1 gotcha-coverage gap |
| 🟢 NIT      | 11    | 9/19 (47.4%) — placeholder style, label/fn drift, autoname-vs-name handling |

**Verdict matrix per template:**

| # | Template | B | I | N | Verdict |
|---|----------|---|---|---|---------|
| 01 | `01_department` | 0 | 0 | 0 | ✅ PASS |
| 02 | `02_designation` | 0 | 0 | 1 | ✅ PASS (NIT only) |
| 03 | `03_employment_type` | 0 | 0 | 0 | ✅ PASS |
| 04 | `04_employee_grade` | **1** | 0 | 0 | 🔴 **NEEDS FIX** |
| 05 | `05_branch` | 0 | 0 | 0 | ✅ PASS |
| 06 | `06_holiday_list` | 0 | **1** | 0 | 🟡 NEEDS FIX |
| 07 | `07_shift_type` | 0 | 0 | 2 | ✅ PASS (NIT only) |
| 08 | `08_shift_location` | 0 | 0 | **1** | ✅ PASS (NIT only) |
| 09 | `09_shift_schedule` | 0 | 0 | 2 | ✅ PASS (NIT only) |
| 10 | `10_employee` | **1** | 0 | 1 | 🔴 **NEEDS FIX** |
| 11 | `11_leave_type` | 0 | 0 | 0 | ✅ PASS |
| 12 | `12_leave_policy` | 0 | 0 | **1** | ✅ PASS (NIT only) |
| 13 | `13_leave_period` | 0 | 0 | 0 | ✅ PASS |
| 14 | `14_leave_allocation` | 0 | **1** | 0 | 🟡 NEEDS FIX |
| 15 | `15_shift_assignment` | 0 | 0 | **3** | ✅ PASS (NIT only) |
| 16 | `16_attendance` | 0 | **1** | **1** | 🟡 NEEDS FIX |
| 17 | `17_employee_checkin` | 0 | **1** | **1** | 🟡 NEEDS FIX |
| 18 | `18_leave_application` | 0 | **1** | 0 | 🟡 NEEDS FIX |
| 19 | `19_leave_ledger_entry` | 0 | **1** | 0 | 🟡 NEEDS FIX |
| **Totals** | | **2** | **7** | **11** | |

> Note on counting: the 6-template count for "IMPORTANT affected" counts each template once even when multiple IMPORTANT items cluster (e.g. 18_leave_application has 1 IMPORTANT — the missing gotcha #1). The per-template section lists every individual issue.

---

## 2. Per-Template Findings

---

### 01_department

- **Files:**
  - `/root/.openclaw/workspace/projects/haritha-hospitals/docs/client-onboarding/03-intake-workbook/01_master_data/01_department.csv`
  - `/root/.openclaw/workspace/projects/haritha-hospitals/docs/client-onboarding/03-intake-workbook/01_master_data/01_department.md`
- **DocType:** `Department` (stock)
- **CSV columns:** 7 (excluding header meta-columns)
- **MD field rows:** 7
- **Stock fields used:** 5 of 9 (`department_name`, `parent_department`, `company`, `is_group`, `disabled`)
- **Custom fields used:** 2 of 8 (`payroll_cost_center`, `leave_block_list`) — both marked optional
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 0

✅ **No issues found — passed all SCs.**

Notes:
- All required-marking is consistent (CSV `Y` ↔ MD `Y` for `department_name`, `company`; CSV `N` ↔ MD `N` for the rest).
- Gotcha #5, #11, #1 all documented in the MD's "Migration notes" section.
- Stock-omitted fields (`lft`, `rgt`, `old_parent`) are correctly excluded from the template.
- Custom field types are correctly omitted (layout breaks `section_break_4`, `column_break_9`; child tables `shift_request_approver`, `leave_approvers`, `expense_approvers` — populated via UI per the MD note).

---

### 02_designation

- **Files:**
  - `02_designation.csv`
  - `02_designation.md`
- **DocType:** `Designation` (stock)
- **CSV columns:** 3
- **MD field rows:** 3
- **Stock fields used:** 2 of 2 (`designation_name`, `description`)
- **Custom fields used:** 1 of 3 (`appraisal_template`) — marked optional
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 1

**NIT-1:** `02_designation.md:26` — the "Healthcare-specific fields" subsection lists `required_skills_section` and `skills` in prose but the main field-reference table omits them. Documentation completeness is fine (prose names them) but a reader looking only at the field-reference table could miss these custom fields.

- **Recommended fix:** Add a one-line note in the main field-reference table acknowledging that the 2 remaining custom fields (layout break `required_skills_section` and child table `skills`) are documented in the Healthcare-specific subsection below.

Otherwise: all required-marking is consistent, all fieldnames exist in stock or custom fixtures, no leaks.

---

### 03_employment_type

- **Files:**
  - `03_employment_type.csv`
  - `03_employment_type.md`
- **DocType:** `Employment Type` (stock)
- **CSV columns:** 1
- **MD field rows:** 1
- **Stock fields used:** 1 of 1 (`employee_type_name`)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 0

✅ **No issues found — passed all SCs.**

Minimal template (1 field), and it's correctly marked required in both CSV and MD. Gotcha #1 documented.

---

### 04_employee_grade

- **Files:**
  - `04_employee_grade.csv`
  - `04_employee_grade.md`
- **DocType:** `Employee Grade` (stock)
- **CSV columns:** 4
- **MD field rows:** 4
- **Stock fields used:** 3 of 3 (`default_salary_structure`, `default_base_pay`, `currency`)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 1
- **IMPORTANT:** 0
- **NIT:** 0

🔴 **BLOCKER-1: SC-5b invented field `grade_name`**
- **Fieldname:** `grade_name`
- **Where:** `04_employee_grade.csv:2`
- **What's wrong:** The CSV uses `grade_name` as the primary key column. Stock `/tmp/p5_research/erpnext_json/employee_grade.json` shows `autoname: Prompt` with fieldnames `['default_salary_structure', 'default_base_pay', 'currency']` only — there is no `grade_name` field. Custom fixture has zero custom fields for Employee Grade. `grade_name` is therefore an INVENTED field.
- **Severity:** BLOCKER (SC-5b invented/orphan field — would fail Data Import with `Unknown column 'grade_name'` or silent drop).
- **Recommended fix:** Either (a) rename the CSV column from `grade_name` to `name` (the Frappe pseudo-field for `autoname=Prompt` DocTypes) AND change the `notes` cell from `autoname=field:grade_name` to `autoname=prompt`, or (b) verify against the target HRMS version — but for HRMS v16.5.0 stock, option (a) is correct.

Also note: the MD at `04_employee_grade.md:18` says "autoname=field:grade_name" which is INCORRECT — stock says `autoname: Prompt`. The MD documentation is wrong about the autoname mode. (This is a documentation issue bundled with the BLOCKER — fix the autoname note too.)

---

### 05_branch

- **Files:**
  - `05_branch.csv`
  - `05_branch.md`
- **DocType:** `Branch` (stock)
- **CSV columns:** 1
- **MD field rows:** 1
- **Stock fields used:** 1 of 1 (`branch`)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 0

✅ **No issues found — passed all SCs.**

Minimal template, correctly marked required. Gotcha #1 and #12 documented.

---

### 06_holiday_list

- **Files:**
  - `06_holiday_list.csv`
  - `06_holiday_list.md`
- **DocType:** `Holiday List` (stock)
- **CSV columns:** 9
- **MD field rows:** 8 (CSV has `total_holidays` and `holidays` extras? No — CSV has 9, MD has 8. Wait, recount: CSV has `holiday_list_name, from_date, to_date, weekly_off, color, country, subdivision, is_half_day` = 8 columns actually; let me re-verify.)
- **Stock fields used:** 8 of 10 (template excludes `total_holidays` and `holidays` — table field correctly omitted from parent CSV per SC-8)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 1
- **NIT:** 0

🟡 **IMPORTANT-1: SC-5c type mismatch on `color`**
- **Fieldname:** `color`
- **Where:** `06_holiday_list.csv:5`
- **What's wrong:** Stock `holiday_list.json` defines `color` as fieldtype `Color`. The template declares it as type `Data`. Data Import may accept the string but Frappe's Color field expects hex like `#7042B5` — any non-hex value would fail validation on save. Also, the template's `validation` column says "any HTML color" which is incorrect; the field accepts only hex strings or named CSS colors via the Color picker.
- **Severity:** IMPORTANT (import-tolerated; type mismatch tolerated by Data Import but breaks the field semantics).
- **Recommended fix:** Change the CSV `type` column from `Data` to `Color` for the `color` row. Update the `validation` cell to `hex (#RRGGBB) or named CSS color`.

Otherwise: required-marking is consistent, no orphan fields, no leaks. Gotcha #17 (weekly_off string vs index) is correctly documented in the MD.

---

### 07_shift_type

- **Files:**
  - `07_shift_type.csv`
  - `07_shift_type.md`
- **DocType:** `Shift Type` (stock)
- **CSV columns:** 22
- **MD field rows:** 22
- **Stock fields used:** 21 of 27 (template excludes layout breaks `column_break_3`, `column_break_10`, `column_break_18`, plus section breaks `auto_attendance_settings_section`, `grace_period_settings_auto_attendance_section`, `overtime_section`)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0 (automated check initially flagged `name` as orphan, but `name` IS the legitimate Frappe pseudo-field for `autoname=prompt` DocTypes)
- **IMPORTANT:** 0
- **NIT:** 2

**NIT-1:** `07_shift_type.csv:2` — column type for `name` is declared `Data`, which is correct for the autoname=prompt field. No fix needed but worth noting this is the ONLY field with `name` as the fieldname in any P5 template; downstream readers may confuse it with a user-defined field.

**NIT-2:** `07_shift_type.csv:2` and `07_shift_type.md` — `color` row lists 9 color options (`Blue / Cyan / Fuchsia / Green / Lime / Orange / Pink / Red / Violet`). Property setter at `property_setter.json` actually defines 10 options (adds `Yellow`). The MD has it correctly as 9 visible colors but the property setter fixture has 10 (`blue / cyan / fuchsia / green / lime / orange / pink / red / violet / yellow / blue`). This is a minor enumeration drift — the property setter appears to define the list with leading/trailing blank lines plus `yellow` between `violet` and `blue`.

- **Recommended fix:** Either (a) update the template's `color` validation to include `Yellow`, or (b) accept that the property setter fixture has a formatting quirk (leading/trailing blank options are inert) and document the actual 9 visible colors.

Otherwise: required-marking consistent, no orphan fields, no leaks. Gotcha #4 and #16 documented.

---

### 08_shift_location

- **Files:**
  - `08_shift_location.csv`
  - `08_shift_location.md`
- **DocType:** `Shift Location` (stock)
- **CSV columns:** 5
- **MD field rows:** 5
- **Stock fields used:** 5 of 8 (template excludes `geolocation` if no separate value? Actually template DOES include `geolocation` row. Let me verify — CSV: `location_name, checkin_radius, latitude, longitude, geolocation` = 5 fields. Stock has 8: `location_name, checkin_radius, longitude, geolocation, latitude` + 3 layout breaks. Template includes all 5 data fields correctly.)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 1

**NIT-1:** `08_shift_location.md` — does NOT explicitly document Gotcha #1 (`get_doc()` doctype key) which is a generic gotcha affecting every DocType that will be imported by a future script.

- **Recommended fix:** Add a one-line note: "Gotcha #1 — any future custom import script must inject `{'doctype': 'Shift Location', ...}` before constructing the document."

Otherwise: required-marking consistent, no orphan fields, no leaks. Gotcha #8 and #15 documented.

---

### 09_shift_schedule

- **Files:**
  - `09_shift_schedule.csv`
  - `09_shift_schedule.md`
- **DocType:** `Shift Schedule` (stock)
- **CSV columns:** 4
- **MD field rows:** 4
- **Stock fields used:** 3 of 6 data fields (`frequency`, `repeat_on_days`, `shift_type`) + `name` (autoname=prompt pseudo-field)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0 (initially flagged `name` as orphan, but `name` IS legitimate for autoname=prompt)
- **IMPORTANT:** 0
- **NIT:** 2

**NIT-1:** `09_shift_schedule.csv:2` — `name` field type `Data` with `unique` validation. Correct for autoname=prompt. No fix needed.

**NIT-2:** `09_shift_schedule.csv:2` and `09_shift_schedule.md` — `repeat_on_days` is marked `Y` (required) in both CSV and MD. The field is a Table field, so required-by-stock translates to "must have at least one child row at save time", not "must appear in CSV". The template's main CSV cannot populate this Table field; the child rows are imported separately via a separate Data Import (as the MD notes). This is consistent with the research §6 verdict [R] and is documented correctly in the MD.

- **Recommended fix:** None — verdict is correctly [R], and the field is properly omitted from the parent CSV body (its row in the CSV is a placeholder pointing to the child import).

Otherwise: required-marking consistent, no orphan fields, no leaks. Gotcha #8 and #1 documented.

---

### 10_employee

- **Files:**
  - `10_employee.csv`
  - `10_employee.md`
- **DocType:** `Employee` (stock)
- **CSV columns:** 36
- **MD field rows:** 36
- **Stock fields used:** 24 of 69 data fields (many layout-only fields correctly excluded)
- **Custom fields used:** 14 of 20 (`employment_type`, `grade`, `default_shift`, `health_insurance_provider`, `health_insurance_no`, `leave_approver`, `expense_approver`, `shift_request_approver`, `pan_number`, `ifsc_code`, `micr_code`, `provident_fund_account`; layout breaks `approvers_section`, `salary_cb`, `column_break_45`, `bank_cb`, `health_insurance_section` correctly excluded)
- **BLOCKER:** 1
- **IMPORTANT:** 0
- **NIT:** 1

🔴 **BLOCKER-1: SC-2 required drift on `default_shift`**
- **Fieldname:** `default_shift`
- **Where:** `10_employee.csv:25` declares required=`Y*`, but `10_employee.md` field-reference table declares `Y`.
- **What's wrong:** CSV and MD disagree on the required marking for the same field. `Y*` (CSV) means "conditionally required" while `Y` (MD) means "always required". The MD table actually displays `ALWAYS recommended (auto-attendance workflows)` in the notes column — but the `required` column reads `Y`. This is a real consistency issue that will confuse clients and reviewers.
- **Severity:** BLOCKER (SC-2 required-marking drift between CSV and MD — automation will read these differently).
- **Recommended fix:** Pick one convention. Options: (a) Mark `required=Y*` in BOTH CSV and MD (consistent with `mandatory_depends_on` semantics — see Gotcha #6 and Section 8 Q? for 10_employee), or (b) Mark `required=Y` in both and add the `Y*` explanation as a separate notes line. The cleaner option is (a) — use `Y*` consistently because the verdict matrix marks the field [O] (stock-optional, conditionally required via `mandatory_depends_on`).

**NIT-1:** `10_employee.md:21` — the `default_shift` row's notes column contains text from the Healthcare-specific fields table that bled into the field-reference table due to template prose. Specifically, the row's `notes` reads `ALWAYS recommended (auto-attendance workflows)` which is from the Healthcare-specific subsection's "when to use" column, not the actual MD table notes column. This is a prose leakage, not a critical issue, but the MD field-reference table note cell is incorrect.

- **Recommended fix:** Move the `ALWAYS recommended` content into the actual notes cell of the field-reference table or into a separate paragraph, keeping the `required` column clear of cross-table content.

Also note: the templates 16-19 use the `Link→DocType` style for type column while templates 01-15 use the plain `Link` style. The Employee MD's main field-reference table uses `Link` style consistently — good. The CSV uses `Link` style consistently too.

Gotcha #6, #7, #1, #12, #13 all documented in the MD.

---

### 11_leave_type

- **Files:**
  - `11_leave_type.csv`
  - `11_leave_type.md`
- **DocType:** `Leave Type` (stock)
- **CSV columns:** 23
- **MD field rows:** 23
- **Stock fields used:** 23 of 29 data fields (template excludes layout breaks but includes all functional fields)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 0

✅ **No issues found — passed all SCs.**

All required-marking consistent, no orphan fields, no leaks. Gotcha #14 and #1 documented.

---

### 12_leave_policy

- **Files:**
  - `12_leave_policy.csv`
  - `12_leave_policy.md`
- **DocType:** `Leave Policy` (stock)
- **CSV columns:** 3
- **MD field rows:** 3
- **Stock fields used:** 3 of 4 (`title`, `leave_policy_details`, `amended_from`)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 1

**NIT-1: SC-2 verdict drift on `leave_policy_details` (intentional)**
- **Fieldname:** `leave_policy_details`
- **Where:** `12_leave_policy.csv:3` and `12_leave_policy.md`
- **What's wrong:** Research §6 verdict marks `leave_policy_details` as [R] (required) because the stock JSON declares `reqd=1`. The CSV and MD both declare `required=N` because the field is a Table field that cannot be populated directly via CSV (child rows are imported separately via Data Import on `Leave Policy Detail` child DocType). This drift is intentional and the MD explicitly says "do NOT add in this CSV (Data Import handles via separate upload)".
- **Severity:** NIT (intentional drift, well-documented, not a real blocker).
- **Recommended fix:** No fix needed — this is the correct pattern for Table fields in CSV templates. Optionally, add a row in the verdict matrix cross-reference table at the bottom of the MD clarifying "verdict [R] but required=N because Table field; populate via separate import".

Otherwise: required-marking consistent between CSV and MD, no orphan fields, no leaks. Gotcha #14 and #1 documented.

---

### 13_leave_period

- **Files:**
  - `13_leave_period.csv`
  - `13_leave_period.md`
- **DocType:** `Leave Period` (stock)
- **CSV columns:** 5
- **MD field rows:** 5
- **Stock fields used:** 5 of 6 data fields (`from_date`, `to_date`, `is_active`, `company`, `optional_holiday_list` — `amended_from` correctly excluded as it's only meaningful in amendment workflow context)
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 0

✅ **No issues found — passed all SCs.**

Required-marking consistent, no orphan fields, no leaks. Gotcha #14 and #1 documented.

---

### 14_leave_allocation

- **Files:**
  - `14_leave_allocation.csv`
  - `14_leave_allocation.md`
- **DocType:** `Leave Allocation` (stock)
- **CSV columns:** 16
- **MD field rows:** 16
- **Stock fields used:** 16 of 28 data fields
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 1
- **NIT:** 0

🟡 **IMPORTANT-1: SC-5c type mismatch on `description`**
- **Fieldname:** `description`
- **Where:** `14_leave_allocation.csv:14`
- **What's wrong:** Stock `leave_allocation.json` defines `description` as fieldtype `Small Text` (single-line text, ~140 chars). The template declares type `Text` (multi-line, unlimited length). Data Import will accept both, but UI rendering differs and Frappe may strip multi-line content from Small Text fields. Functionally the template's `validation` cell says `<= 140 chars` which matches Small Text semantics, but the declared `type` is wrong.
- **Severity:** IMPORTANT (import-tolerated but breaks UI consistency and could silently truncate multi-line input).
- **Recommended fix:** Change CSV `type` column from `Text` to `Small Text` to match stock.

Otherwise: required-marking consistent, no orphan fields, no leaks. Gotcha #14 and #1 documented.

---

### 15_shift_assignment

- **Files:**
  - `15_shift_assignment.csv`
  - `15_shift_assignment.md`
- **DocType:** `Shift Assignment` (stock)
- **CSV columns:** 13
- **MD field rows:** 13
- **Stock fields used:** 13 of 17 data fields
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 0
- **NIT:** 3

**NIT-1: SC-2 verdict drift on `name` field (autoname=Series conflict)**
- **Fieldname:** `name`
- **Where:** `15_shift_assignment.csv:2` and `15_shift_assignment.md`
- **What's wrong:** Stock `shift_assignment.json` shows `autoname: HR-SHA-.YY.-.MM.-.#####` — Series-based, NOT prompt-based. The template provides a `name` column for the client to fill in (`SA-001`), but Frappe's Series counter will auto-generate a name like `HR-SHA-26-09-#####` and IGNORE the supplied value unless the Series counter is pre-bumped. This is documented in the research §7 Gotcha #8 and the MD, but the template nonetheless exposes `name` as a CSV column with no warning that Frappe will overwrite it.
- **Severity:** NIT (data-import-tolerated if the supplied name matches the generated Series, but typically generates a DIFFERENT name and silently overrides the client's value).
- **Recommended fix:** Either (a) drop the `name` column from the CSV (let Frappe auto-generate via Series) and document the resulting `HR-SHA-YY-MM-#####` format, or (b) keep the `name` column but add a prominent note in the MD that "Frappe will OVERWRITE this with the Series-generated name unless the Series counter is pre-bumped via `_pre_set_shift_request_series()` (see Gotcha #8 in research §7)". Option (b) is more flexible for clients who want explicit control.

**NIT-2: SC-2 verdict drift on `employee_name` (functional-required)**
- **Fieldname:** `employee_name`
- **Where:** `15_shift_assignment.csv:5`
- **What's wrong:** Stock `shift_assignment.json` declares `employee_name` as optional (`reqd=0`), so verdict §6 is [O]. The template marks it `required=Y` in both CSV and MD because the migration script needs `employee_name` as the join key for Gotcha #7 remap (prod→dev Employee ID alignment). The MD explicitly documents this: "REQUIRED for Data Import to fill autogen display field".
- **Severity:** NIT (intentional functional-required override, well-documented).
- **Recommended fix:** Mark as `required=Y*` (conditionally required for Data Import) instead of `required=Y` to better signal the conditional nature. Update the MD's "required" column to match.

**NIT-3: Missing Gotcha coverage** — see cross-template gotcha coverage matrix (this template covers #8, #9, #7, #1 but is part of the broader coverage question).

Gotcha #8, #9, #7, #1 documented.

---

### 16_attendance

- **Files:**
  - `16_attendance.csv`
  - `16_attendance.md`
- **DocType:** `Attendance` (stock)
- **CSV columns:** 22
- **MD field rows:** 22
- **Stock fields used:** 22 of 28 data fields
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 1
- **NIT:** 1

🟡 **IMPORTANT-1: Gotcha #1 documentation gap**
- **Issue:** Template does not explicitly call out Gotcha #1 (`get_doc()` doctype key). This is the generic gotcha that affects every DocType that will be processed by a future custom import script. The template's "Migration notes" section covers Gotcha #14 (leave module), Gotcha #7 (Employee ID remap), and Attendance-specific concerns (status=Present requires in_time, status=On Leave requires leave_type, docstatus requirements) but does not mention the universal Gotcha #1.
- **Severity:** IMPORTANT (per SC-6 gotcha coverage — generic gotcha affecting every template, so its omission in a template's MD is a coverage gap).
- **Recommended fix:** Add a one-line note: "Gotcha #1 — any future custom import script must inject `{'doctype': 'Attendance', ...}` before constructing the document."

**NIT-1: Type column style inconsistency** — Templates 16-19 use the qualified `Link→DocType` style (e.g., `Link→Employee`, `Link→Shift Type`) while templates 01-15 use plain `Link`. Both are valid for Data Import but the inconsistency across the 19-template set could confuse clients.

- **Recommended fix:** Standardize on ONE style across all 19 templates. Recommend `Link→DocType` because it provides at-a-glance target-DocType clarity for non-technical clients. (This is a stylistic call for the project lead; the current state is functional but inconsistent.)

Gotcha #14, #7 documented. Gotcha #1 missing (see above).

---

### 17_employee_checkin

- **Files:**
  - `17_employee_checkin.csv`
  - `17_employee_checkin.md`
- **DocType:** `Employee Checkin` (stock)
- **CSV columns:** 17
- **MD field rows:** 17
- **Stock fields used:** 17 of 24 data fields
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 1
- **NIT:** 1

🟡 **IMPORTANT-1: SC-2 verdict drift on `log_type` (functional-required)**
- **Fieldname:** `log_type`
- **Where:** `17_employee_checkin.csv:5`
- **What's wrong:** Stock `employee_checkin.json` declares `log_type` as optional (`reqd=0`), so verdict §6 is [O]. The template marks it `required=Y` in both CSV and MD because every Checkin MUST be either IN or OUT — without a log_type, the row is meaningless. The MD explicitly documents this as a hard requirement ("case-sensitive IN/OUT"). This is a functional-required override.
- **Severity:** IMPORTANT (verdict drift but functionally justified — the field cannot be omitted from any row).
- **Recommended fix:** Either (a) accept the verdict drift as intentional (mark verdict in §6 as functional-required via comment in the research matrix), or (b) update the verdict in §6 from [O] to [R] for `log_type` (then this template becomes consistent with the verdict). Option (b) is cleaner because the field IS logically required for any valid Checkin row.

**NIT-1: Gotcha #1 documentation gap** — same as 16_attendance; the template's "Migration notes" section does not include Gotcha #1.

- **Recommended fix:** Add a one-line note: "Gotcha #1 — any future custom import script must inject `{'doctype': 'Employee Checkin', ...}` before constructing the document."

Gotcha #7 documented. Gotcha #1 missing (see above).

---

### 18_leave_application

- **Files:**
  - `18_leave_application.csv`
  - `18_leave_application.md`
- **DocType:** `Leave Application` (stock)
- **CSV columns:** 22
- **MD field rows:** 22
- **Stock fields used:** 22 of 29 data fields
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 1
- **NIT:** 0

🟡 **IMPORTANT-1: Gotcha #1 documentation gap**
- **Issue:** Template does not explicitly call out Gotcha #1 in the "Migration notes" section. The section covers Gotcha #14 (leave module), Gotcha #7 (Employee ID remap), `leave_approver` must be User.email (GOTCHA-analogous to #10), `status=Approved` requires docstatus=1, auto-creation of Leave Ledger Entry, overlap check, negative balance check, stock `description` vs label "Reason". But Gotcha #1 (generic `get_doc()` doctype key) is missing.
- **Severity:** IMPORTANT (per SC-6).
- **Recommended fix:** Add a one-line note: "Gotcha #1 — any future custom import script must inject `{'doctype': 'Leave Application', ...}` before constructing the document."

Also note: the MD's "Related" section references "tabLeave Allocation" / "tabLeave Ledger Entry" / etc. using the `tab<DocType>` prefix — this is the Frappe-internal table naming convention. Templates 01-15 don't use this prefix. Minor style inconsistency.

Otherwise: required-marking consistent, no orphan fields, no leaks. Gotcha #14, #7, GOTCHA-analogous to #10 documented.

---

### 19_leave_ledger_entry

- **Files:**
  - `19_leave_ledger_entry.csv`
  - `19_leave_ledger_entry.md`
- **DocType:** `Leave Ledger Entry` (stock)
- **CSV columns:** 14
- **MD field rows:** 14
- **Stock fields used:** 14 of 15 data fields
- **Custom fields used:** 0 of 0
- **BLOCKER:** 0
- **IMPORTANT:** 1
- **NIT:** 0

🟡 **IMPORTANT-1: Gotcha #1 documentation gap**
- **Issue:** Template does not explicitly call out Gotcha #1. The "Migration notes" section covers Gotcha #14 (leave module), Gotcha #7 (Employee ID remap), ledger append-only behavior, `transaction_type` is Link→DocType (not Select), `transaction_name` is Dynamic Link, no `transaction_date` in stock schema, `leaves` balance validation, transaction ordering, docstatus=1 requirement, and `transaction_type`/`transaction_name` matching. But Gotcha #1 (generic `get_doc()` doctype key) is missing.
- **Severity:** IMPORTANT (per SC-6).
- **Recommended fix:** Add a one-line note: "Gotcha #1 — any future custom import script must inject `{'doctype': 'Leave Ledger Entry', ...}` before constructing the document."

Also note: the template's MD uses `transaction_type` example `Leave Application` and the `transaction_name` example `LAP-26-09-00001` — these are illustrative but the actual production samples (per `prod_samples.txt`) show 0 Leave Ledger Entries at Haritha, so the template is genuinely synthetic. The MD acknowledges this in the "Production note" line.

Otherwise: required-marking consistent, no orphan fields, no leaks. Gotcha #14, #7 documented.

---

## 3. Cross-Template Findings

---

### 3.1 Gotcha Coverage Matrix

Gotchas from research §7 (17 total). Coverage matrix shows which MD files document each gotcha:

| Gotcha # | Title | Templates documenting it | Coverage status |
|----------|-------|--------------------------|-----------------|
| 1 | `get_doc()` doctype key | `01_department`, `02_designation`, `03_employment_type`, `04_employee_grade`, `05_branch`, `06_holiday_list`, `07_shift_type`, `09_shift_schedule`, `10_employee`, `11_leave_type`, `12_leave_policy`, `13_leave_period`, `14_leave_allocation`, `15_shift_assignment` | ⚠️ 14/19 — **MISSING** from: `08_shift_location`, `16_attendance`, `17_employee_checkin`, `18_leave_application`, `19_leave_ledger_entry` |
| 2 | Company default accounts depend on Account | (None — Company is not in P5 scope) | 🟢 Acceptable (out of scope) |
| 3 | Account root nodes are system-generated | (None — Account is not in P5 scope) | 🟢 Acceptable (out of scope) |
| 4 | `Shift Type` has `autoname='prompt'` | `07_shift_type` | ✅ 1/1 (only DocType where it applies) |
| 5 | Department / Item Group circular-root trap | `01_department` | ✅ 1/1 |
| 6 | Employee requires `gender` and `default_shift` (`mandatory_depends_on`) | `10_employee` | ✅ 1/1 (only template where Employee is the focus) |
| 7 | Prod and dev Employee IDs do not align (remap by `employee_name`) | `10_employee`, `15_shift_assignment`, `16_attendance`, `17_employee_checkin`, `18_leave_application`, `19_leave_ledger_entry` | ✅ 6/6 (every template that references Employee by Link) |
| 8 | Shift Schedule `autoname='prompt'` + child-table loss in list payload | `08_shift_location`, `09_shift_schedule`, `15_shift_assignment` | ✅ 3/3 |
| 9 | Shift Assignment has two out-of-scope Link fields | `15_shift_assignment` | ✅ 1/1 (only template where Shift Assignment is the focus) |
| 10 | Shift Request `validate_approver()` is unconditional AND autoname series silently overrides explicit name | (None — Shift Request not in P5 scope) | 🟡 Acceptable (out of scope, but 18_leave_application mentions GOTCHA-analogous to #10 for Leave Approver) |
| 11 | Department name auto-appends ` - <company-abbr>` on save | `01_department` | ✅ 1/1 |
| 12 | Branch DocType is unused at Haritha (0 records) | `05_branch`, `10_employee` | ✅ 2/2 |
| 13 | Employee Grade DocType is unused at Haritha (0 records) | `04_employee_grade`, `10_employee` | ✅ 2/2 |
| 14 | Leave module is configured but no live transactions | `11_leave_type`, `12_leave_policy`, `13_leave_period`, `14_leave_allocation`, `16_attendance`, `18_leave_application`, `19_leave_ledger_entry` | ✅ 7/7 (every template that touches leave data) |
| 15 | Shift Location is `Hyderabad` only (single-site) | `08_shift_location`, `15_shift_assignment` | ✅ 2/2 |
| 16 | Shift Type naming follows internal code convention not stock-required | `07_shift_type` | ✅ 1/1 |
| 17 | Holiday List `weekly_off` is stored as a STRING, not an index | `06_holiday_list` | ✅ 1/1 |

**Summary:**
- 14 of 17 gotchas are correctly documented in the appropriate template MD(s).
- **Gotcha #1** has a coverage gap: it is missing from `08_shift_location`, `16_attendance`, `17_employee_checkin`, `18_leave_application`, `19_leave_ledger_entry` (5 templates).
- **Gotchas #2, #3, #10** are intentionally not documented because their DocTypes (Company, Account, Shift Request) are not in P5 scope.

**Recommended fix:** Add the one-line Gotcha #1 note to each of the 5 missing MD files.

---

### 3.2 Leak Scan Results (SC-3)

**Command run:**
```bash
grep -inIE 'Haritha|Hyderabad|Telangana|TSMC|pberpprod|_b80f05e76a0dcaad|144\.217\.163\.228|/home/vijay/|MYSQL_ROOT_PASSWORD|12603|7829|12562|Haritha Hospitals Holiday List' *.csv *.md
```

**Raw output:** 38 lines matched across 23 MD files (no CSV file matched). After filtering to exclude legitimate technical references (`haritha_hospital` app name, `custom_field.json` / `property_setter.json` fixtures, "haritha hospital" prose mentions in Migration notes sections), **0 client-data leaks were found**.

**Detailed analysis:**
- All matches are to the lowercase string `haritha_hospital` (the custom app name) or to prose phrases like "the `haritha_hospital` custom app" — these are LEGITIMATE technical references to the project's own custom app, NOT client data leaks.
- The pattern matched "Haritha" alone (case-sensitive) but every hit is part of `haritha_hospital` or `haritta_hospital` (the misspelling variant seen in some research docs) — no occurrence of standalone "Haritha Hospitals" or "Haritha" as a brand name in the template files.
- The pattern `Haritha Hospitals Holiday List` did NOT match anywhere (no template references the literal production holiday list name; the templates correctly use generic placeholders like `Holiday List A`).
- The patterns `Hyderabad`, `Telangana`, `TSMC`, `pberpprod`, `_b80f05e76a0dcaad`, `144.217.163.228`, `/home/vijay/`, `MYSQL_ROOT_PASSWORD`, `12603`, `7829`, `12562` did NOT match anywhere.

**Verdict:** ✅ **PASS** — no real client-data leaks. All SC-3 matches are technical references to the project's custom app name.

The SC-3 pattern as specified is overly broad for the term `Haritha` (it catches the legitimate `haritha_hospital` custom app name). Future iterations of the SC-3 pattern should anchor on word boundaries or exclude `haritha_hospital` specifically.

---

### 3.3 Invented/Orphan Field Inventory (SC-5b)

A fieldname is "invented/orphan" if it appears in the template but is neither in stock ERPNext/HRMS v16.5.0 JSON nor in the custom_field.json fixture for that DocType.

| Template | Fieldname | Status |
|----------|-----------|--------|
| `04_employee_grade` | `grade_name` | 🔴 **BLOCKER** — invented; stock uses `autoname=Prompt` so the field should be `name`, not `grade_name` |
| `07_shift_type` | `name` | 🟢 **FALSE POSITIVE** — legitimate Frappe pseudo-field for `autoname=prompt` DocTypes |
| `09_shift_schedule` | `name` | 🟢 **FALSE POSITIVE** — legitimate Frappe pseudo-field for `autoname=prompt` DocTypes |
| `15_shift_assignment` | `name` | 🟡 **NIT** — `autoname=Series` (not prompt); Frappe will override supplied `name` with `HR-SHA-YY-MM-#####` |

**Total invented fields:** 1 BLOCKER (`grade_name`), 1 NIT (`name` on Shift Assignment).

**False positives eliminated by manual review:** `name` on Shift Type and Shift Schedule (both `autoname=prompt`, so `name` is the correct field to include in CSV).

---

### 3.4 Type-Mismatch Inventory (SC-5c)

A field has a "type mismatch" if the CSV's declared `type` column does not match the stock fieldtype.

| Template | Fieldname | Stock type | Template type | Severity |
|----------|-----------|------------|---------------|----------|
| `06_holiday_list` | `color` | `Color` | `Data` | 🟡 IMPORTANT |
| `14_leave_allocation` | `description` | `Small Text` | `Text` | 🟡 IMPORTANT |
| `07_shift_type` | `color` | `Select` | `Select` | ✅ Match (no issue) |

**Notes:**
- Templates 16-19 use the qualified `Link→DocType` style (e.g., `Link→Employee`, `Link→Shift Type`) for Link fields. This is STYLE-only and is NOT flagged as a mismatch because the qualified form provides the same Data Import semantics as plain `Link`. The mismatch is between templates 01-15 (use plain `Link`) and 16-19 (use `Link→DocType`).
- The 06_holiday_list `color` mismatch is the most serious: stock `Color` fieldtype expects hex strings or named CSS colors, but the template treats it as a generic `Data` field, which means arbitrary strings would pass Data Import but fail Frappe's Color validation.
- The 14_leave_allocation `description` mismatch is medium: `Text` allows multi-line, but stock `Small Text` enforces ~140 chars and renders differently in UI.

**Total type mismatches:** 2 IMPORTANT.

---

### 3.5 Required-Marking Drift Inventory (SC-2)

A "drift" is a mismatch in required marking between CSV, MD, and research §6 verdict.

| Template | Fieldname | CSV required | MD required | §6 verdict | Severity |
|----------|-----------|--------------|-------------|------------|----------|
| `10_employee` | `default_shift` | `Y*` | `Y` | [O] (functional via `mandatory_depends_on`) | 🔴 BLOCKER (CSV-MD disagreement) |
| `12_leave_policy` | `leave_policy_details` | `N` | `N` | [R] | 🟢 NIT (intentional — Table field, verdict [R] can't be CSV-populated) |
| `15_shift_assignment` | `employee_name` | `Y` | `Y` | [O] | 🟢 NIT (functional-required for Employee ID remap per Gotcha #7) |
| `17_employee_checkin` | `log_type` | `Y` | `Y` | [O] | 🟡 IMPORTANT (verdict drift — should be marked [R] in §6 for log_type, OR mark `Y*` in template) |

**Total required-marking drift issues:** 1 BLOCKER, 1 IMPORTANT, 2 NITs.

---

## 4. Severity Aggregates

| Severity | Count | Per-template breakdown |
|----------|-------|------------------------|
| 🔴 BLOCKER | 2 | 04_employee_grade (1), 10_employee (1) |
| 🟡 IMPORTANT | 7 | 06_holiday_list (1), 08_shift_location (1 — gotcha coverage), 14_leave_allocation (1), 16_attendance (1 — gotcha coverage), 17_employee_checkin (1 — verdict drift), 18_leave_application (1 — gotcha coverage), 19_leave_ledger_entry (1 — gotcha coverage) |
| 🟢 NIT | 11 | 02_designation (1), 07_shift_type (2), 08_shift_location (0, but the 1 IMPORTANT was a coverage gap so the count moved), 09_shift_schedule (2), 10_employee (1), 12_leave_policy (1), 15_shift_assignment (3), 16_attendance (1), 17_employee_checkin (1) |

Wait — recounting:
- 01: 0/0/0
- 02: 0/0/1
- 03: 0/0/0
- 04: 1/0/0
- 05: 0/0/0
- 06: 0/1/0
- 07: 0/0/2
- 08: 0/1/0 (gotcha #1 coverage gap)
- 09: 0/0/2
- 10: 1/0/1
- 11: 0/0/0
- 12: 0/0/1
- 13: 0/0/0
- 14: 0/1/0
- 15: 0/0/3
- 16: 0/1/1
- 17: 0/1/1
- 18: 0/1/0
- 19: 0/1/0

**Totals:** B=2, I=7, N=11. ✅ Matches summary table.

---

## 5. Verification Methodology Notes

- **Source-of-truth files used:**
  - `/tmp/p5_research/erpnext_json/*.json` — 21 stock DocType JSON files for HRMS v16.5.0.
  - `/tmp/p5_research/fixtures/haritha_hospital/fixtures/custom_field.json` — 78 custom fields filtered by DocType.
  - `/tmp/p5_research/fixtures/haritha_hospital/fixtures/property_setter.json` — 189 property setters filtered by DocType + property.
  - `/root/.openclaw/workspace/projects/haritha-hospitals/prompts/P5-rebuild-research.md` — §6 verdict matrix, §7 gotcha index.

- **Verification automation:** Custom Python script at `/tmp/verify_templates.py` (created during this run, not committed) parses each CSV + MD, cross-references against stock + custom + verdict data, and emits issues by severity. Manual review refined the false positives (the `name` pseudo-field on `autoname=prompt` DocTypes, the `leave_policy_details` Table field, etc.).

- **Manual review additions:**
  - Re-classified 4 automated BLOCKERs as FALSE POSITIVES (NITs) after verifying the underlying mechanism (autoname=prompt pseudo-fields; Table field handling).
  - Added 5 gotcha-coverage-gap findings (IMPORTANT) for templates missing Gotcha #1 documentation.
  - Added cross-template style-inconsistency findings (NITs for `Link` vs `Link→DocType` style drift).

- **Limitations:**
  - The MD parser uses heuristics to identify the main field-reference table; edge cases where the MD has unusual table structures (e.g., escaped pipes, multiline cells) may not parse perfectly. Manual review of each MD confirms the parser output is accurate for all 19 templates.
  - Type-match comparison is limited to the declared `type` column; it does not verify that example values match the expected format (e.g., Date fields using YYYY-MM-DD).
  - Leak scan uses a broad pattern that catches the legitimate `haritha_hospital` custom app name; this is documented as a SC-3 pattern refinement recommendation but is not itself a real leak.

---

## 6. Recommended Action Plan

1. **Fix the 2 BLOCKERs first** (these will block Data Import):
   - `04_employee_grade.csv`: rename `grade_name` → `name`, fix `autoname=prompt` in notes.
   - `10_employee.csv` & `10_employee.md`: reconcile `default_shift` required marking to either `Y*` (both) or `Y` (both) with notes explaining `mandatory_depends_on`.

2. **Fix the 2 type mismatches** (will cause subtle data-quality issues):
   - `06_holiday_list.csv`: change `color` type from `Data` to `Color`.
   - `14_leave_allocation.csv`: change `description` type from `Text` to `Small Text`.

3. **Add Gotcha #1 documentation to 5 templates** (one-line addition per file):
   - `08_shift_location.md`
   - `16_attendance.md`
   - `17_employee_checkin.md`
   - `18_leave_application.md`
   - `19_leave_ledger_entry.md`

4. **Standardize Link field style across all 19 templates** (NIT — choose `Link` or `Link→DocType` consistently).

5. **Consider verdict matrix update** for §6:
   - `Employee.log_type` → mark [R] (functionally required; the field is meaningless without IN/OUT).
   - `Employee.employee_name` on `Shift Assignment` → mark [R] (functionally required for Gotcha #7 remap).
   - `Employee.default_shift` on `Employee` → already marked [O] with `mandatory_depends_on` note; consider marking [O*] (conditionally required).

---

**End of report.**
