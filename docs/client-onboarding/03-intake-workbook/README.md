# Intake Workbook — How to Fill

**Date:** 2026-09-15
**Status:** ✅ Complete (Phase 3 rebuilt from research §3.1 MIGRATION_ORDER + §7 gotcha index)
**Owner (client):** Client HR Lead + Client Project Lead
**Owner (partner):** Implementation Partner Tech Lead
**Phase:** 2 — Environment Provisioning + Master-Data Intake → 3 — Validation & Signoff

---

## What This Covers

Collects all master data needed to import a healthcare client into ERPNext + HRMS. 19 DocType templates (paired MD + CSV) drive Frappe Data Import for the partner's migration script. Generic placeholders only — no real client data.

---

## 1. Purpose + Audience

| Role | Owns |
|---|---|
| **Client HR Lead** | Fills the `client_value` column on each CSV with real org data |
| **Client Project Lead** | Approves final submission, signs off per DocType + master roll-up |
| **Client IT Lead** | Answers Link-target existence questions (which Department / Holiday List / Shift Type exists) |
| **Partner Tech Lead** | Imports CSVs via Frappe Data Import, runs validation, aggregates master report |

---

## 2. Workflow (4 steps)

```
1. Download  → grab CSV from 01_master_data/
2. Fill      → replace client_value placeholders with real data
3. Sign off  → per DocType: 03_signoff/01_per_doctype_signoff_template.md
4. Import    → partner runs Data Import on sandbox, then production
```

### Step-by-step

1. **Read** each template's `XX_*.md` first to understand:
   - Required (`Y`) vs optional (`N`) vs conditionally required (`Y*`)
   - Auto-name mode (autoname=field, autoname=prompt, autoname=Series)
   - Link-target existence assumptions
   - Gotchas relevant to that DocType
2. **Open** `XX_*.csv` in Excel / Google Sheets / LibreOffice.
3. **Fill** the `client_value` column. Replace example rows or append new rows.
4. **Save** as UTF-8 comma-separated CSV. Do NOT change column names or order — Data Import requires exact match.
5. **Repeat** for all 19 templates. Run validation checks in `03_signoff/02_master_validation_report.md` after each DocType submission.
6. **Sign off** per DocType using `03_signoff/01_per_doctype_signoff_template.md`.
7. **Hand off** filled CSVs to Partner Tech Lead for Data Import.

---

## 3. 19-Template Index

Templates are paired `.csv` + `.md`. CSV is the import target; MD is the field reference.

| # | DocType | Template File | Brief | MIGRATION_ORDER rank |
|---|---|---|---|---|
| 01 | Department | [`01_department.csv`](./01_master_data/01_department.csv) + [.md](./01_master_data/01_department.md) | Org chart units; rolls up to Company | **#4** |
| 02 | Designation | [`02_designation.csv`](./01_master_data/02_designation.csv) + [.md](./01_master_data/02_designation.md) | Job titles | **#5** |
| 03 | Employment Type | [`03_employment_type.csv`](./01_master_data/03_employment_type.csv) + [.md](./01_master_data/03_employment_type.md) | Full-time / Part-time / Contract / etc. | **#9** |
| 04 | Employee Grade | [`04_employee_grade.csv`](./01_master_data/04_employee_grade.csv) + [.md](./01_master_data/04_employee_grade.md) | Pay-band masters (optional; see gotcha #13) | — (App create) |
| 05 | Branch | [`05_branch.csv`](./01_master_data/05_branch.csv) + [.md](./01_master_data/05_branch.md) | Multi-site offices (optional; see gotcha #12) | — (App create) |
| 06 | Holiday List | [`06_holiday_list.csv`](./01_master_data/06_holiday_list.csv) + [.md](./01_master_data/06_holiday_list.md) | Public holidays + weekly off (parent) | **#12** |
| 06a | Holiday (child) | See [06_holiday_list.md §Child table](./01_master_data/06_holiday_list.md) | Per-date holiday entries (separate Data Import) | — (child of #12) |
| 07 | Shift Type | [`07_shift_type.csv`](./01_master_data/07_shift_type.csv) + [.md](./01_master_data/07_shift_type.md) | Shift patterns (Morning / Night / General) | **#10** |
| 08 | Shift Location | [`08_shift_location.csv`](./01_master_data/08_shift_location.csv) + [.md](./01_master_data/08_shift_location.md) | Geofenced sites | **#11** |
| 09 | Shift Schedule | [`09_shift_schedule.csv`](./01_master_data/09_shift_schedule.csv) + [.md](./01_master_data/09_shift_schedule.md) | Recurring weekly patterns | **#16** |
| 10 | Employee | [`10_employee.csv`](./01_master_data/10_employee.csv) + [.md](./01_master_data/10_employee.md) | Central HR master | **#13** |
| 11 | Leave Type | [`11_leave_type.csv`](./01_master_data/11_leave_type.csv) + [.md](./01_master_data/11_leave_type.md) | CL / SL / EL / LWP / etc. | — (App create) |
| 12 | Leave Policy | [`12_leave_policy.csv`](./01_master_data/12_leave_policy.csv) + [.md](./01_master_data/12_leave_policy.md) | Leave-type bundles per role | — (App create) |
| 13 | Leave Period | [`13_leave_period.csv`](./01_master_data/13_leave_period.csv) + [.md](./01_master_data/13_leave_period.md) | Annual leave cycles | — (App create) |
| 14 | Leave Allocation | [`14_leave_allocation.csv`](./01_master_data/14_leave_allocation.csv) + [.md](./01_master_data/14_leave_allocation.md) | Per-employee leave balances | — (App create) |
| 15 | Shift Assignment | [`15_shift_assignment.csv`](./01_master_data/15_shift_assignment.csv) + [.md](./01_master_data/15_shift_assignment.md) | Roster rows | **#17** |
| 16 | Attendance | [`16_attendance.csv`](./01_master_data/16_attendance.csv) + [.md](./01_master_data/16_attendance.md) | Daily attendance (auto-created from Checkins) | — (App create) |
| 17 | Employee Checkin | [`17_employee_checkin.csv`](./01_master_data/17_employee_checkin.csv) + [.md](./01_master_data/17_employee_checkin.md) | Biometric/RFID log rows | — (device import) |
| 18 | Leave Application | [`18_leave_application.csv`](./01_master_data/18_leave_application.csv) + [.md](./01_master_data/18_leave_application.md) | Leave requests (UI-submitted) | — (App create) |
| 19 | Leave Ledger Entry | [`19_leave_ledger_entry.csv`](./01_master_data/19_leave_ledger_entry.csv) + [.md](./01_master_data/19_leave_ledger_entry.md) | System-generated ledger (not user-editable) | — (system-generated) |

**Reading the table:** `MIGRATION_ORDER rank` comes from research §3.1. Templates marked `— (App create)` are populated through the App's normal create flow (UI / Data Import standalone / device auto-import / system generation) — not by the partner's master-data migration script.

> **See also:** [`02_settings_checklists/`](./02_settings_checklists/) — Phase 5 configuration checklists for HR Settings, Payroll Settings, and auto-attendance policies. These are out of the master-data CSV import flow but must be completed before UAT. Start with [`01_hr_settings.md`](./02_settings_checklists/01_hr_settings.md) (added Sep 21: **Workflow for Leave Application** + **Email Account** sections).

---

## 4. Import Order + Dependencies

### 4.1 The 9 templates in MIGRATION_ORDER

Per research §3.1, the partner's migration script processes these 9 DocTypes in this order. Each depends on its parent:

```
Company (configured in ERPNext, NOT in workbook)
  ↓
Department          (01)  ←── Designation (02), Employment Type (03)
  ↓
Shift Type          (07), Shift Location (08)
  ↓
Holiday List        (06)
  ↓
Employee            (10)  ←── Branch (05), Employee Grade (04) optional
  ↓
Shift Schedule      (09)
  ↓
Shift Assignment    (15)
```

**Strict rule:** Import parents before children. Example: `Department` (#4) MUST land before `Employee` (#13) because Employee.department is a Link to Department.

### 4.2 The 10 templates NOT in MIGRATION_ORDER

These DocTypes exist in the workbook but are populated through the App's normal create flow, not the migration script:

| # | DocType | Why NOT in MIGRATION_ORDER |
|---|---|---|
| 04 | Employee Grade | DocType exists but unused in single-site deployments (gotcha #13). Add via web UI or standalone Data Import. |
| 05 | Branch | DocType exists but unused in single-site deployments (gotcha #12). Add via web UI or standalone Data Import. |
| 11 | Leave Type | Standalone Data Import; no FK dependencies beyond Company. |
| 12 | Leave Policy | App UI create; child Leave Policy Detail rows added in same form. |
| 13 | Leave Period | App UI create; references Company + Holiday List (already imported). |
| 14 | Leave Allocation | App UI create; requires Employee + Leave Type + Leave Period + Leave Policy. |
| 16 | Attendance | Auto-created from Employee Checkin via auto-attendance job. Rarely imported directly. |
| 17 | Employee Checkin | Created by biometric/RFID device sync (HRMS Device API or custom middleware). |
| 18 | Leave Application | Submitted by employees via web UI. Pre-seeding only via direct Data Import. |
| 19 | Leave Ledger Entry | System-generated when Leave Allocation / Leave Application is created. NOT user-editable. |

> **Task-spec note:** The task brief listed "13 of 19 are populated through App's normal create flow". That count includes Holiday (child) + Shift Location + Overtime Type — none of which are standalone P5 templates (Holiday is a child of 06_holiday_list; Shift Location IS in MIGRATION_ORDER #11; Overtime Type is out of P5 scope). Counting only standalone P5 DocType templates: **10 of 19 are NOT in MIGRATION_ORDER**.

---

## 5. Top 5 Client-Facing Gotchas

These are the gotchas most likely to bite clients filling templates. Full gotcha index: research §7.

| # | DocType | Gotcha | One-liner |
|---|---|---|---|
| #5 | 01_department | Department root trap | Leave `parent_department` blank for top-level rows. Setting `= "All Departments"` raises `ParentNotFoundError`. → [01_department.md](./01_master_data/01_department.md) |
| #6 | 10_employee | Employee `gender` / `default_shift` ordering | Gender + Shift Type masters MUST be imported first. Both fields use `mandatory_depends_on` — insert fails if masters missing. → [10_employee.md](./01_master_data/10_employee.md) |
| #11 | 01_department | Department name auto-suffix | Enter the bare name (`Nursing`), NOT `Nursing - HH`. Frappe appends the company abbreviation on save. Typing it twice → `Nursing - HH - HH`. → [01_department.md](./01_master_data/01_department.md) |
| #17 | 06_holiday_list | `weekly_off` is a STRING | Use day name (`Sunday`), NOT numeric index (`0`). Stock Select stores full string. → [06_holiday_list.md](./01_master_data/06_holiday_list.md) |
| #7 | 10_employee + 15_shift_assignment | Employee ID remap | Fill `employee_name` exactly as on the Employee record. Prod and dev Employee IDs (`HR-EMP-00211` vs `HR-EMP-00002`) differ; remap joins on `employee_name`. → [10_employee.md](./01_master_data/10_employee.md), [15_shift_assignment.md](./01_master_data/15_shift_assignment.md) |

Gotcha #1 (`get_doc()` doctype key injection) affects every DocType and is documented in every template's MD. Other in-scope gotchas (#4, #8, #9, #12, #13, #14, #15, #16) are covered in their respective template MDs.

---

## 6. Signoff Process

After all 19 templates are filled, run per-DocType signoff:

→ **[`03_signoff/01_per_doctype_signoff_template.md`](./03_signoff/01_per_doctype_signoff_template.md)**

Each DocType gets one signoff block containing:

- Client attestation (organization + contact + date + signature)
- Reviewer attestation (partner tech lead)
- Validation checklist (records count, required-marking OK, Link targets resolved, gotchas reviewed, custom fields populated)
- Free-text notes / exceptions

After all 19 blocks are signed, run the master roll-up:

→ **[`03_signoff/02_master_validation_report.md`](./03_signoff/02_master_validation_report.md)**

The master report aggregates all 19 DocType summaries, captures cross-template import verification logs, lists the 6 known-accepted plain `Link` fields, and provides the final signoff chain (Client → Reviewer → Importer).

---

## 7. Master Validation Report

→ **[`03_signoff/02_master_validation_report.md`](./03_signoff/02_master_validation_report.md)**

Captures:

- Per-template summary table (19 rows + TOTAL)
- Aggregate stats (total templates, total records, required-marking coverage %, gotcha coverage)
- Import verification log (per import run: date, site, importer, records imported, errors)
- Known-accepted items (6 plain `Link` fields remaining — see §8 below)
- Open issues (typically none post-Phase 2.7)
- Signoff chain

### 7.1 Known-accepted plain `Link` fields (6 fields)

Per commit `31243cf`, the following 6 fields remain as plain `Link` (not `Link→DocType`):

| Template | Field | Target DocType |
|---|---|---|
| 09_shift_schedule | `amended_from` | Shift Schedule |
| 10_employee | `company` | Company |
| 10_employee | `gender` | Gender |
| 12_leave_policy | `amended_from` | Leave Policy |
| 15_shift_assignment | `department` | Department |
| 15_shift_assignment | `amended_from` | Shift Assignment |

These are accepted as-is — Data Import resolves them correctly. Cosmetic `Link→DocType` upgrade is deferred to a future pass.

---

## 8. File Location Map

```directory
docs/client-onboarding/03-intake-workbook/
├── README.md                                    (this file — rebuilt Phase 3)
├── AUDIT-REPORT.md                              (Phase 2.5 baseline, untouched)
├── 01_master_data/
│   ├── 01_department.{csv,md}                   (rebuilt Phase 1)
│   ├── 02_designation.{csv,md}
│   ├── 03_employment_type.{csv,md}
│   ├── 04_employee_grade.{csv,md}
│   ├── 05_branch.{csv,md}
│   ├── 06_holiday_list.{csv,md}
│   ├── 07_shift_type.{csv,md}
│   ├── 08_shift_location.{csv,md}
│   ├── 09_shift_schedule.{csv,md}
│   ├── 10_employee.{csv,md}
│   ├── 11_leave_type.{csv,md}
│   ├── 12_leave_policy.{csv,md}
│   ├── 13_leave_period.{csv,md}
│   ├── 14_leave_allocation.{csv,md}
│   ├── 15_shift_assignment.{csv,md}
│   ├── 16_attendance.{csv,md}                   (rebuilt Phase 2)
│   ├── 17_employee_checkin.{csv,md}
│   ├── 18_leave_application.{csv,md}
│   └── 19_leave_ledger_entry.{csv,md}
├── 02_settings_checklists/                      ([HR Settings](./02_settings_checklists/01_hr_settings.md) · [Payroll Settings](./02_settings_checklists/02_payroll_settings.md) · [Auto-Attendance Policies](./02_settings_checklists/03_auto_attendance_policies.md) — Phase 5)
├── 03_signoff/
│   ├── 01_per_doctype_signoff_template.md       (rebuilt Phase 3 — this file)
│   └── 02_master_validation_report.md           (rebuilt Phase 3 — this file)
├── mapping/                                     (Phase 4 reconciliation, untouched)
└── reconciliation/                              (Phase 4 reconciliation, untouched)
```

---

## 9. Tips for Filling Templates

| Tip | Why |
|---|---|
| **Required fields first** | Data Import fails on missing required fields. Fill all `Y` / `Y*` columns before touching `N` columns. |
| **Link fields use canonical `name`** | Link values must match the target DocType's `name` exactly. Use the primary key, not the label. |
| **Select fields use exact option text** | `Sunday` not `sunday`; `Active` not `active`. Case-sensitive. |
| **Date fields use `YYYY-MM-DD`** | Excel may auto-convert. Format → Cells → Text first, or use ISO 8601 format. |
| **Booleans use `0` / `1`** | Not `Yes` / `No`. Data Import parses Check fields strictly. |
| **Bulk data (>1000 rows)** | Split into multiple CSVs of ~500 rows each. Data Import handles each separately. |
| **UTF-8 only** | Save as UTF-8 (Notepad: Encoding → UTF-8; Excel: CSV UTF-8). |

---

## 10. When You Get Stuck

| Issue | Contact |
|---|---|
| Field validation error | Partner Tech Lead |
| Healthcare-specific field missing | Check MD's "Healthcare-specific fields" subsection; custom field may need adding via Customize Form |
| Link target can't be found | Verify the parent DocType was imported first (see §4) |
| Date format issues | Save as text or use Format → Cells → Date (ISO 8601) |
| File encoding | Save as UTF-8 |
| Auto-attendance / biometric integration | Partner Tech Lead (out of workbook scope; covered in `02_settings_checklists/`) |

---

## Related

- [`02_settings_checklists/01_hr_settings.md`](./02_settings_checklists/01_hr_settings.md) — HR Settings configuration checklist (HRMS v16 Workflow for Leave Application + Email Account sections, Sep 21)
- [`02_settings_checklists/02_payroll_settings.md`](./02_settings_checklists/02_payroll_settings.md) — Payroll Settings configuration checklist
- [`02_settings_checklists/03_auto_attendance_policies.md`](./02_settings_checklists/03_auto_attendance_policies.md) — Auto-attendance policy checklist (Shift Location geofence, grace periods, biometric integration)
- [`prompts/P5-rebuild-research.md`](../../../prompts/P5-rebuild-research.md) — Source-of-truth compilation (custom-field inventory, stock DocType JSON, MIGRATION_ORDER, gotcha index)
- [`prompts/P5-rebuild-plan.md`](../../../prompts/P5-rebuild-plan.md) — 8-SC verification protocol
- [`reports/p5/P5-reverify-report.md`](../../../reports/p5/P5-reverify-report.md) — Phase 2.7 verdict (22/22 fixes + 11/11 SCs PASS)
- [`reports/p5/P5-fix-summary.md`](../../../reports/p5/P5-fix-summary.md) — Phase 2.6 diff stats + per-fix list
- [`03_signoff/01_per_doctype_signoff_template.md`](./03_signoff/01_per_doctype_signoff_template.md) — 19 signoff blocks
- [`03_signoff/02_master_validation_report.md`](./03_signoff/02_master_validation_report.md) — Master roll-up

---

**End of README.**
