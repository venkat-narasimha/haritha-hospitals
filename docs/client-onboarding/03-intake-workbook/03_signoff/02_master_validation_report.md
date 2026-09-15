# Master Validation Report — Template

**Date:** 2026-09-15
**Status:** ✅ Complete (rebuilt Phase 3 — per-template summary + aggregate stats + 6 known-accepted items + signoff chain)
**Phase:** 3 — Validation & Signoff

---

## What This Covers

Roll-up report across all 19 DocTypes. Aggregates per-template signoffs from [`01_per_doctype_signoff_template.md`](./01_per_doctype_signoff_template.md), captures import verification logs, documents the 6 known-accepted plain `Link` fields, and provides the final signoff chain.

---

## Header — Project Info

| Field | Value |
|---|---|
| **Client name** | ________________________________ |
| **Intake date** | YYYY-MM-DD |
| **Reviewer (Partner Tech Lead)** | ________________________________ |
| **Importer (Partner Tech Lead or designate)** | ________________________________ |
| **Sandbox site** | ________________________________ |
| **Production site** | ________________________________ |

---

## 1. Per-Template Summary

| # | DocType | Template File | Records | Required-marking OK | Gotcha Coverage | Validation Status |
|---|---|---|---|---|---|---|
| 01 | Department | [`01_department.csv`](../01_master_data/01_department.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #5, #11 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 02 | Designation | [`02_designation.csv`](../01_master_data/02_designation.csv) | ____ | ✅ / ⚠️ / ❌ | #1 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 03 | Employment Type | [`03_employment_type.csv`](../01_master_data/03_employment_type.csv) | ____ | ✅ / ⚠️ / ❌ | #1 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 04 | Employee Grade | [`04_employee_grade.csv`](../01_master_data/04_employee_grade.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #13 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 05 | Branch | [`05_branch.csv`](../01_master_data/05_branch.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #12 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 06 | Holiday List | [`06_holiday_list.csv`](../01_master_data/06_holiday_list.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #17 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 07 | Shift Type | [`07_shift_type.csv`](../01_master_data/07_shift_type.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #4, #16 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 08 | Shift Location | [`08_shift_location.csv`](../01_master_data/08_shift_location.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #8, #15 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 09 | Shift Schedule | [`09_shift_schedule.csv`](../01_master_data/09_shift_schedule.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #8 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 10 | Employee | [`10_employee.csv`](../01_master_data/10_employee.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #6, #7, #12, #13 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 11 | Leave Type | [`11_leave_type.csv`](../01_master_data/11_leave_type.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #14 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 12 | Leave Policy | [`12_leave_policy.csv`](../01_master_data/12_leave_policy.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #14 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 13 | Leave Period | [`13_leave_period.csv`](../01_master_data/13_leave_period.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #14 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 14 | Leave Allocation | [`14_leave_allocation.csv`](../01_master_data/14_leave_allocation.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #7, #14 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 15 | Shift Assignment | [`15_shift_assignment.csv`](../01_master_data/15_shift_assignment.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #7, #8, #9, #15 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 16 | Attendance | [`16_attendance.csv`](../01_master_data/16_attendance.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #7, #14 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 17 | Employee Checkin | [`17_employee_checkin.csv`](../01_master_data/17_employee_checkin.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #7 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 18 | Leave Application | [`18_leave_application.csv`](../01_master_data/18_leave_application.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #7, #14 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| 19 | Leave Ledger Entry | [`19_leave_ledger_entry.csv`](../01_master_data/19_leave_ledger_entry.csv) | ____ | ✅ / ⚠️ / ❌ | #1, #7, #14 ✅ | ✅ PASS / ⚠️ PARTIAL / ❌ FAIL |
| | **TOTAL** | | ____ | | | |

**Status legend:** ✅ PASS = all checks green. ⚠️ PARTIAL = known-accepted deviations (see §4 below) or minor issues. ❌ FAIL = blockers requiring fix before production.

---

## 2. Aggregate Stats

| Metric | Value |
|---|---|
| **Total templates** | 19 |
| **Templates in MIGRATION_ORDER** (research §3.1) | 9 (01, 02, 03, 06, 07, 08, 09, 10, 15) |
| **Templates NOT in MIGRATION_ORDER** (App create flow) | 10 (04, 05, 11, 12, 13, 14, 16, 17, 18, 19) |
| **Total records** | ____ |
| **Required-marking coverage** | ____ % (target ≥ 95%) |
| **Gotcha coverage** | ____ / 17 in-scope gotchas referenced (target 17/17) |
| **Custom-field coverage** | ____ % of applicable templates (10_employee has 14+ custom fields) |
| **DocTypes at 100% required-marking coverage** | ____ |
| **DocTypes with <100% required-marking coverage** | ____ |
| **Per-DocType signoffs collected** | ____ / 19 (target 19/19) |
| **Open issues (see §5)** | ____ |

---

## 3. Import Verification Log

One row per Data Import run. Sandbox-first, then production.

| Import # | Date | Site | Importer | Records Imported | Errors | Notes |
|---|---|---|---|---|---|---|
| 1 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | e.g. first dry-run on Department |
| 2 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| 3 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| 4 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| 5 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| 6 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| 7 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| 8 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| 9 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| 10 | YYYY-MM-DD | Sandbox | ________________ | ____ | ____ | |
| ... | | | | | | |
| ____ | YYYY-MM-DD | Production | ________________ | ____ | ____ | First production import |

**Recommended import sequence (from research §3.1 MIGRATION_ORDER):**

```
1. Company (configured in ERPNext, NOT in workbook)
2. Department      (01)
3. Designation     (02)
4. Employment Type (03)
5. Shift Type      (07)
6. Shift Location  (08)
7. Holiday List    (06)
8. Employee        (10)
9. Shift Schedule  (09)
10. Shift Assignment (15)
```

After MIGRATION_ORDER completes, run separate Data Imports for the 10 "App create" DocTypes per client preference (UI or standalone Data Import).

---

## 4. Known-Accepted Items

Per commit `31243cf` and the Phase 2.6 fix-summary, the following **6 plain `Link` fields** remain as `Link` (not `Link→DocType`). All resolve correctly via Data Import. Cosmetic `Link→DocType` upgrade is deferred to a future pass.

| # | Template | Field | Target DocType | Reason for accepting plain `Link` |
|---|---|---|---|---|
| 1 | 10_employee | `company` | Company | Outside D-7 to D-11 task enumeration; cosmetic only |
| 2 | 10_employee | `gender` | Gender | Outside D-7 to D-11 task enumeration; cosmetic only |
| 3 | 09_shift_schedule | `amended_from` | Shift Schedule | Amendment workflow only; rarely populated |
| 4 | 12_leave_policy | `amended_from` | Leave Policy | Amendment workflow only; rarely populated |
| 5 | 15_shift_assignment | `department` | Department | Optional Link auto-derived from Employee; cosmetic only |
| 6 | 15_shift_assignment | `amended_from` | Shift Assignment | Amendment workflow only; rarely populated |

**Total:** 6 plain `Link` fields. None of these block Data Import. All resolve correctly.

---

## 5. Open Issues

Expected: **None** post-Phase 2.7 (22/22 fixes confirmed + 11/11 SCs PASS per `P5-reverify-report.md`).

If any issues are open, document them below:

| # | Issue ID | DocType | Severity | Description | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

---

## 6. Signoff Chain

Final sign-off runs after all 19 per-DocType blocks are signed (see [`01_per_doctype_signoff_template.md`](./01_per_doctype_signoff_template.md)).

### 6.1 Client sign-off

| Field | Value |
|---|---|
| Organization name | ________________________________ |
| Client HR Lead (name + signature) | ________________________________ |
| Client Project Lead (name + signature) | ________________________________ |
| Date | YYYY-MM-DD |

> I confirm the `client_value` column on every CSV is accurate and complete for our organization's data.

### 6.2 Reviewer sign-off

| Field | Value |
|---|---|
| Reviewer name + role | ________________________________ |
| Signature | ________________________________ |
| Date | YYYY-MM-DD |

> I confirm all 19 templates passed validation, Link targets resolve, and gotchas were reviewed.

### 6.3 Importer sign-off

| Field | Value |
|---|---|
| Importer name + role | ________________________________ |
| Signature | ________________________________ |
| Date | YYYY-MM-DD |

> I confirm the records were imported via Frappe Data Import on the sites listed in §3 with no critical errors.

---

## 7. Migration Readiness Decision

Mark **one**:

- [ ] **APPROVED** — Proceed to Phase 4 (Production Migration)
- [ ] **APPROVED with conditions** — proceed with named risks accepted by Client Sponsor
- [ ] **DEFERRED** — Hold until specific issues resolved; re-validate

**Conditions (if APPROVED with conditions):**

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

**Deferral reasons (if DEFERRED):**

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

---

## 8. Comments / Risk Acceptance

Capture accepted risks, deferred validations, and conditions for approval:

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

---

## Changelog

| Date | Changes |
|------|---------|
| 2026-09-15 | Initial version (Phase 3 rebuild) — per-template summary + 6 known-accepted items + 3-party signoff chain |

---

## Related

- [`01_per_doctype_signoff_template.md`](./01_per_doctype_signoff_template.md) — 19 per-DocType signoff blocks
- [`../README.md`](../README.md) — Workbook index, MIGRATION_ORDER, top 5 client-facing gotchas
- [`../../../prompts/P5-rebuild-research.md`](../../../prompts/P5-rebuild-research.md) — §3.1 MIGRATION_ORDER, §6 verdict matrix, §7 gotcha index
- [`../../../reports/p5/P5-reverify-report.md`](../../../reports/p5/P5-reverify-report.md) — Phase 2.7 verdict (22/22 fixes + 11/11 SCs PASS)

---

**End of master validation report.**
