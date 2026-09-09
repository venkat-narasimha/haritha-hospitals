# Go-Live — Phase 6 Sign-off

**Project:** Haritha Hospitals ERPNext + HRMS
**Date:** YYYY-MM-DD
**Phase:** 6 — Cutover & Go-Live Day
**Frappe/HRMS version:** v16.30.0 / v16.5.0

## Signatories

| Role | Name | Signature | Date |
|---|---|---|---|
| Client Project Lead | | | |
| Client HR Lead | | | |
| Client IT Lead | | | |
| Client Department Manager rep. | | | |
| Client Sponsor / CFO | | | |
| Implementation Partner Lead | | | |
| Implementation Partner Tech Lead | | | |

## Cutover — sign-off checklist

- [ ] **Cutover plan executed** per Phase 4 schedule (typically weekend 18:00 Friday → 06:00 Monday)
- [ ] **Full database backup** taken before migration; backup verified restorable
- [ ] **Production migration completed** — all 15 DocTypes imported; integrity checks passed
- [ ] **Data integrity verified** — record counts match workbook, FK validity 100%, no orphans
- [ ] **Smoke tests passed** — login, view employee, assign shift, apply leave, mark attendance, generate report
- [ ] **Biometric devices reconfigured** — pointing at production URL, first punches processed correctly
- [ ] **User accounts created** for all active employees; password reset emails sent
- [ ] **User roles + permissions** configured per role matrix
- [ ] **Rollback plan documented and rehearsed** — trigger thresholds agreed (e.g., >5 P1 failures = rollback)
- [ ] **Communication sent** to all staff: "ERPNext is live; here's how to log in / reset password"
- [ ] **War-room staffed** for go-live day; Partner + Client IT + Client HR physically/digitally present
- [ ] **Hypercare rotation scheduled** — daily standups week 1, every-other-day week 2, weekly weeks 3–4

## Production metrics — Day 1 verification

| Metric | Target | Actual | Pass/Fail |
|---|---|---|---|
| Total Employees imported | = Workbook count | | |
| Departments | = Workbook count | | |
| Designations | = Workbook count | | |
| Shift Types | = Workbook count | | |
| Shift Locations | = Workbook count | | |
| Holiday Lists | = Workbook count | | |
| Successful biometric check-ins (first 24h) | ≥90% | | |
| Failed login attempts (first 24h) | <5% of users | | |
| Critical defects raised (first 24h) | 0 | | |

## Rollback decision

- [ ] **No rollback** — production stable, smoke tests passed, proceed to hypercare
- [ ] **Rollback executed** — triggers met; rollback log attached

## Comments / Deviations

<!-- Free text — capture cutover surprises, device reconfiguration delays, any early incidents -->

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

## Signatures

**Client Project Lead:** _________________________
Date: ___________

**Client Sponsor / CFO:** _________________________
Date: ___________

**Implementation Partner Lead:** _________________________
Date: ___________
