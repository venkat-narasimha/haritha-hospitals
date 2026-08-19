# Haritha Hospitals — Project Tracker

**Project:** Haritha Hospitals — Real hospital project (CMM Level 5 target)
**Scope:** Shift management + HRMS basics (employees, departments, shift types, attendance, leave)
**Deferred:** Wards, beds, OTs, pharmacy, lab, billing, full CoA, cost centers
**Owner:** Venkat (Processbricks)
**Started:** 2026-08-19
**Stack:** Frappe 16 / ERPNext 16 / HRMS 16.5.0 (pinned) / payments / custom app (TBD)

---

## Phase 0: Schema Planning (CURRENT)

**Goal:** Document schema for all master data entities needed for shift management system.

**Status:** Awaiting user review of `all_schemas.csv`.

**Deliverables:**
- [x] `all_schemas.csv` — 15 entities, schema-only (drafted 2026-08-19)
- [x] `TRACKER.md` — this file (created 2026-08-19)
- [x] `README.md` — project overview (created 2026-08-19)

**Decisions:**
- 2026-08-19: Scope = shift management only (deferred: wards, beds, OTs, pharmacy, lab, billing)
- 2026-08-19: Stack pin = hrms 16.5.0 (per lesson #44)
- 2026-08-19: Shift code scheme = 10-char `[P][HHMM][S][HHMM]` (Option A, HRMS-native flags)
- 2026-08-19: Holidays = standard Indian national + 4-5 Telangana (per user)
- 2026-08-19: Custom leave types = deferred (Haritha adds later)
- 2026-08-19: Leave allocation = standard Indian defaults + rules in remarks column
- 2026-08-19: Source data = DO NOT modify (canonicalization applied at import time, not in source)

**Sources:**
- Real hospital roster: `../../uploads/pberpqa-real-data-for-demo/roster_and_attendance_june.xlsx` (210 employees, 36 depts, 51 desigs, 31 shift codes)
- Reference: `../pberpqa-hospital-demo/` (pberpqa hospital demo, NOT perfect — gaps documented)

---

## Phase 1: Schema Approval (PENDING)

**Goal:** User reviews and approves the schema CSV.

**Deliverables:**
- [ ] User sign-off on all 15 entity schemas
- [ ] Source canonicalization confirmed (no changes to source data)
- [ ] Holiday List dates confirmed (Telangana 2025 + 2026 national holidays)

---

## Phase 2: Site Setup (PENDING)

**Goal:** Create Haritha Hospitals site on a fresh environment.

**Deliverables:**
- [ ] Site location TBD (pberpQA busy, pberpDEV Synvok legacy, dev-erp Processleap legacy — new env?)
- [ ] Apps installed: frappe, erpnext, hrms 16.5.0, payments
- [ ] Custom app: haritha_hospital (TBD if needed)
- [ ] Company "Haritha Hospitals" created
- [ ] Holidays loaded

---

## Phase 3: Data Import (PENDING)

**Goal:** Load all master data from CSV into the site.

**Deliverables:**
- [ ] L1 Foundation: Company, FY, Holiday List, Departments, Designations, Employment Type
- [ ] L2 Shift Management: Shift Types, Employees, Shift Assignments, Attendance, Leave Types
- [ ] Custom Fields fixtures (Rule #9 compliance from day 1)
- [ ] Data validation

---

## Phase 4: Shift Management Workflow (PENDING)

**Goal:** Test end-to-end shift management.

**Deliverables:**
- [ ] Shift Assignment creation
- [ ] Auto Attendance (cron)
- [ ] Manual Attendance
- [ ] Leave Application + Allocation
- [ ] Employee Checkin
- [ ] Reports (8-phase test playbook per lesson #48)

---

## Phase 5: Production Readiness (PENDING)

**Goal:** Audit and harden for production.

**Deliverables:**
- [ ] Backups (cron 4×/day like other envs)
- [ ] Pre-flight + post-flight process
- [ ] Disaster recovery tested
- [ ] User training
- [ ] Go-live

---

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-08-19 | Scope = shift management only | User clarified mid-session; defer hospital modules |
| 2026-08-19 | hrms 16.5.0 pin | Lesson #44 — v16.5.1+ breaks on `repost_allowed_types` |
| 2026-08-19 | Shift code = 10-char `[P][HHMM][S][HHMM]` | User-proposed scheme, Option A (lean) |
| 2026-08-19 | Holidays = standard Indian national + 4-5 Telangana | User confirmed |
| 2026-08-19 | Custom leave types = deferred | User said Haritha adds later |
| 2026-08-19 | Leave allocation = standard Indian defaults | User confirmed; rules in remarks column |
| 2026-08-19 | Source data = DO NOT modify | Canonicalization at import time only |

---

## Subagent Log

| Date | Task | Agent | Status |
|---|---|---|---|
| 2026-08-19 12:30 | pberpqa reference + scout analysis | pberpqa_ref_an | ✅ done |
| 2026-08-19 12:30 | Source data Excel analysis | source_data_an | ✅ done |
| 2026-08-19 12:30 | Tracker + docs scan | tracker_docs_an | ✅ done |
| 2026-08-19 14:00 | Week-off pattern analysis | pberpqa_week_off_an | ✅ done |

---

## Open Questions

1. Site location (which env for Haritha Hospitals)?
2. Custom app `haritha_hospital` — needed or just custom fields + fixtures?
3. Telangana 2025 + 2026 holiday list — official dates?
4. Hospital-specific holidays (founder day, anniversary)?

---

*Last updated: 2026-08-19 14:45 IST*
