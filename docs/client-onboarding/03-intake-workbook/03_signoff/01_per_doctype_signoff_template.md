# Per-DocType Sign-off — Template

**Project:** ABC Healthcare ERPNext + HRMS
**Date:** YYYY-MM-DD
**Phase:** 3 — Validation & Dry-Run Migration

> **Usage:** Complete one copy of this template per DocType (15 DocTypes = 15 sign-offs).
> Reference the corresponding `01_master_data/XX_*.md` field docs and `02_master_validation_report.md`.

## DocType details

| Field | Value |
|---|---|
| **DocType** | (e.g., Department) |
| **Source CSV** | `01_master_data/XX_doctype.csv` |
| **Sheet imported on** | YYYY-MM-DD |
| **Imported by** | (Partner Tech Lead) |
| **Sandbox site** | (URL) |

## Import summary

| Metric | Value |
|---|---|
| **Total records in source CSV** | |
| **Records attempted** | |
| **Records succeeded** | |
| **Records failed** | |
| **Coverage %** | (succeeded / source × 100) |

## Validation checks

- [ ] **Required fields populated** for all records (no blank in mandatory columns)
- [ ] **Link fields resolved** — all FK references exist in target DocType (Department → Company, Employee → Department, etc.)
- [ ] **Unique constraints** — no duplicates in `name`, `department_name`, `designation_name`, `employee_number`, etc.
- [ ] **Select field values** — all values from CSV match allowed options (Gender: Male/Female/Other, Status: Active/Suspended/Left, etc.)
- [ ] **Date formats** — all dates in YYYY-MM-DD format and parseable
- [ ] **Numeric fields** — within valid ranges (salary ≥ 0, lat ∈ [-90, 90], etc.)
- [ ] **Booleans** — encoded as 0/1 (not Yes/No)
- [ ] **Custom fields** — healthcare fields (medical_council_reg_no, blood_group, emergency contact) populated where required
- [ ] **No orphan records** — every Department has Company; every Employee has Department; etc.

## Failed records (if any)

| # | Row # | Field | Error | Resolution |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## Sample verification

| Record | Spot-check confirmed by client | Comments |
|---|---|---|
| (first record) | | |
| (middle record) | | |
| (last record) | | |

## Sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Partner Tech Lead (imported + validated) | | | |
| Client HR Lead (data accuracy confirmed) | | | |
| Client Project Lead (overall sign-off) | | | |

## Comments

<!-- Capture any exceptions, accepted risks, deferred validations -->

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
