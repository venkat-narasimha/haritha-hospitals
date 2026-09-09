# Client Onboarding Kit — Haritha Hospitals ERPNext + HRMS

**Version:** 1.0
**Date:** 2026-09-09
**Scope:** HRMS + Shift Management (extendable to other modules)
**Target Frappe/ERPNext/HRMS versions:** v16.30.0 / v16.30.0 / v16.5.0

This kit collects master data and tracks client sign-offs for ERPNext + HRMS implementation, focused on shift management. Synthesised from:
- Frappe's official implementation guidance (`frappe.io/partner/implementation`)
- Frappe partner SOP templates (`frappe.io/partner-sop/implementation-templates`)
- Industry methodology comparison (Frappe, NestorBird, Ksolves, Oracle AIM, SAP Activate)
- Healthcare-specific patterns (Nestorbird RYK Hospital case study)
- Frappe's Data Import DocType templates (per-DocType CSV columns)

## How to use this kit

### For the implementation partner (us)
1. **Read** `01-process.md` first to understand the 6 phases
2. **Share** the workbook files with the client during Phase 2 (Master-Data Intake)
3. **Use** the 6 sign-off templates at each phase boundary
4. **Track** sign-offs in `03-intake-workbook/03_signoff/`

### For the client
1. **Open** each `XX_doctype.csv` file in Excel/Google Sheets
2. **Fill** the `client_value` column (or replace example row with real data)
3. **Follow** any instructions in the corresponding `.md` file
4. **Sign off** per DocType using the validation report

## File structure

- **`README.md`** (this file) — entry point
- **`01-process.md`** — 6-phase onboarding process
- **`02-templates/`** — 6 sign-off templates (project planning, steering, training, UAT, go-live, post-impl)
- **`03-intake-workbook/`** — master data collection workbook
  - **`README.md`** — how to fill the workbook
  - **`01_master_data/`** — 15 DocType sheets (paired MD + CSV)
  - **`02_settings_checklists/`** — HR / Payroll / Auto-Attendance settings
  - **`03_signoff/`** — per-DocType sign-off + validation report

## Key conventions

- **CSV columns** = ERPNext fieldnames (not labels). Field names must match Frappe schema exactly for Data Import to work.
- **Required fields** are marked `Y` in the `.md` files; optional marked `N`.
- **Healthcare-specific fields** are documented per DocType (medical council reg no, license validity, blood group, emergency contact).
- **Validation rules** (formats, ranges, lookups) are in the `.md` files — not in CSV (Excel can't show notes per cell).

## How to regenerate fields

If your Frappe/HRMS version differs from v16.30.0 / v16.5.0, regenerate the .md field docs by running:

```bash
bench --site pberpprod.duckdns.org execute \
  haritha_hospital.scripts.extract_doctype_fields --args "[\"Department\", \"Designation\"]"
```

(Implementation not yet built — see `scripts/extract_doctype_fields.py` in the haritha_hospital app to add this. For now, fields are based on Frappe docs + research.)
