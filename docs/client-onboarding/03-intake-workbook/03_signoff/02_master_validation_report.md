# Master Validation Report — Template

**Project:** Haritha Hospitals ERPNext + HRMS
**Date:** YYYY-MM-DD
**Phase:** 3 — Validation & Dry-Run Migration
**Sandbox site:** (URL)

> **Usage:** This is the *roll-up* report across all 15 DocTypes. Fill one row per DocType after dry-run import. Attach individual per-DocType sign-offs (`01_per_doctype_signoff_template.md`).

## Per-DocType summary

| # | DocType | Source CSV | Attempted | Succeeded | Failed | Coverage % | Per-Doctype Sign-off | Client Sign-off | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Department | `01_department.csv` | | | | | [ ] | [ ] | |
| 2 | Designation | `02_designation.csv` | | | | | [ ] | [ ] | |
| 3 | Employment Type | `03_employment_type.csv` | | | | | [ ] | [ ] | |
| 4 | Employee Grade | `04_employee_grade.csv` | | | | | [ ] | [ ] | |
| 5 | Branch | `05_branch.csv` | | | | | [ ] | [ ] | |
| 6 | Holiday List | `06_holiday_list.csv` | | | | | [ ] | [ ] | |
| 7 | Shift Type | `07_shift_type.csv` | | | | | [ ] | [ ] | |
| 8 | Shift Location | `08_shift_location.csv` | | | | | [ ] | [ ] | |
| 9 | Shift Schedule | `09_shift_schedule.csv` | | | | | [ ] | [ ] | |
| 10 | Employee | `10_employee.csv` | | | | | [ ] | [ ] | |
| 11 | Leave Type | `11_leave_type.csv` | | | | | [ ] | [ ] | |
| 12 | Leave Policy | `12_leave_policy.csv` | | | | | [ ] | [ ] | |
| 13 | Leave Period | `13_leave_period.csv` | | | | | [ ] | [ ] | |
| 14 | Leave Allocation | `14_leave_allocation.csv` | | | | | [ ] | [ ] | |
| 15 | Shift Assignment | `15_shift_assignment.csv` | | | | | [ ] | [ ] | |
| | **TOTAL** | | | | | | | | |

## Overall metrics

| Metric | Value |
|---|---|
| **Total source records** | |
| **Total records attempted** | |
| **Total records succeeded** | |
| **Total records failed** | |
| **Overall coverage %** | |
| **DocTypes at 100% coverage** | |
| **DocTypes with <100% coverage** | |

## Error classification

| Error type | Count | DocTypes affected | Resolution plan |
|---|---|---|---|
| Validation (format, range) | | | |
| Link FK missing | | | |
| Uniqueness violation | | | |
| Required field blank | | | |
| Custom field missing | | | |
| Other | | | |

## Healthcare-specific checks

- [ ] All doctors have `medical_council_reg_no` populated
- [ ] All clinical staff have `blood_group` populated
- [ ] All clinical staff have `emergency_contact_name` + `emergency_phone_number` populated
- [ ] Department codes populated for reporting (where applicable)
- [ ] Shift Locations have lat/long/radius from site survey
- [ ] Holiday Lists cover the go-live year fully

## Critical defects raised

| # | DocType | Issue | Severity (P1/P2/P3) | Owner | Status |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## Phase 3 exit criteria

- [ ] Overall coverage ≥ 95% (≥ 99% target)
- [ ] Zero P1 (critical) defects open
- [ ] <3 P2 (major) defects open per DocType
- [ ] All P3 (minor) defects logged for post-go-live
- [ ] All per-DocType sign-offs collected
- [ ] Client HR Lead signs off on this roll-up report

## Migration readiness decision

- [ ] **APPROVED** — Proceed to Phase 4 (Production Migration)
- [ ] **APPROVED with conditions** — proceed with named risks accepted by Client Sponsor
- [ ] **DEFERRED** — Hold until [specific issues] resolved; re-validate

## Comments / Risk acceptance

<!-- Capture: accepted risks, deferred validations, conditions for approval -->

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

## Sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Partner Tech Lead | | | |
| Client HR Lead | | | |
| Client Project Lead | | | |
