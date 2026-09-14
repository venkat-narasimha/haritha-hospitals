# Intake Workbook — How to fill

**Owner (client side):** Client HR Lead + Client Project Lead
**Owner (partner side):** Implementation Partner Tech Lead
**Phase:** 2 — Environment Provisioning + Master-Data Intake

This workbook collects all master data needed to import ABC Healthcare into ERPNext + HRMS. It is organised into three sub-folders:

- `01_master_data/` — 15 DocType sheets (paired MD + CSV)
- `02_settings_checklists/` — HR / Payroll / Auto-Attendance settings (Phase 5)
- `03_signoff/` — per-DocType sign-off + master validation report (Phase 3)

## Step-by-step for the client

1. **Read** `../01-process.md` to understand the 6-phase methodology and where this workbook fits.
2. **Open** each `01_master_data/XX_*.csv` file in Excel or Google Sheets.
3. For each sheet, read the corresponding `XX_*.md` file first to understand:
   - Which fields are required (marked `Y`) vs optional (`N`)
   - Validation rules (formats, length constraints, FK lookups)
   - Healthcare-specific custom fields (e.g., medical_council_reg_no for Employees)
   - Common client mistakes to avoid
4. **Fill** the `client_value` column with the real data:
   - Replace the example row, or
   - Add new rows (one per record)
5. **Save** the CSV (UTF-8, comma-separated). Do not change column names or order — Data Import expects exact match.
6. **Repeat** for all 15 DocTypes.
7. **Run** settings checklists in `02_settings_checklists/` during Phase 5.
8. **Sign off** per DocType using `03_signoff/01_per_doctype_signoff_template.md`.
9. **Track validation** results in `03_signoff/02_master_validation_report.md`.

## Import order (dependency-aware)

```
Company (configured in ERPNext, not in workbook)
  ↓
Holiday List (06)
  ↓
Department (01) ←── Designation (02), Employment Type (03), Employee Grade (04), Branch (05)
  ↓
Shift Type (07), Shift Location (08), Shift Schedule (09)
  ↓
Employee (10)
  ↓
Leave Type (11), Leave Policy (12), Leave Period (13)
  ↓
Leave Allocation (14), Shift Assignment (15)
```

## Tips

- **Required fields first** — populate them all before attempting any optional fields. Data Import will fail on missing required fields.
- **Link fields** (Department, Designation, Branch) must match an existing record's `name` exactly. Use the canonical `name` from ERPNext, not a label.
- **Select fields** (Gender, Status, Frequency) must use the exact option text. See the `.md` for the full options list.
- **Date fields** use `YYYY-MM-DD` format. Excel may auto-convert to local date format — use Format → Cells → Text first.
- **Booleans** (Check fields) use `1` or `0` in CSV, not `Yes`/`No`.
- **Bulk data** (>1000 rows): split into multiple CSVs of ~500 rows each; Data Import handles each separately.

## When you get stuck

| Issue | Contact |
|---|---|
| Field validation error | Implementation Partner Tech Lead |
| Healthcare-specific field not in sheet | Check `.md` file's "Healthcare-specific fields" section — custom field may need adding via Customize Form first |
| Link field can't find target | Verify the target DocType has been imported already |
| Date format issues | Save as text or use Format → Cells → Date (ISO 8601) |
| File encoding | Save as UTF-8 (Notepad: Encoding → UTF-8; Excel: CSV UTF-8) |
