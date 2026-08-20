# Haritha Hospitals — Project Tracker

**Project:** Haritha Hospitals — Real hospital project (CMM Level 5 target)
**Scope:** Shift management + HRMS basics (employees, departments, shift types, attendance, leave)
**Deferred:** Wards, beds, OTs, pharmacy, lab, billing, full CoA, cost centers
**Owner:** Venkat (Processbricks)
**Started:** 2026-08-19
**Stack:** Frappe 16 / ERPNext 16 / HRMS 16.5.0 (pinned) / payments / custom app (TBD)

---

## Phase 0: Schema Planning (DONE ✅)

**Goal:** Document schema for all master data entities needed for shift management system.

**Status:** ✅ Complete 2026-08-19. 19 entities, 168 fields. HRMS v15 verification done (9 docs read, 7 corrections applied — see Decisions Log).

**Deliverables:**
- [x] `all_schemas.csv` — 19 entities, 168 fields (final, after HRMS v15 verification)
- [x] `TRACKER.md` — this file (created 2026-08-19)
- [x] `README.md` — project overview (created 2026-08-19)
- [x] `knowledge/shift_management_hrms.md` — reusable reference (2026-08-19)

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

## Phase 1: Schema Approval (DONE ✅)

**Goal:** User reviews and approves the schema CSV + data CSVs.

**Status:** ✅ Signed off 2026-08-20 by manager. Both deliverables on GitHub (private repo). Manager downloaded, imported to Google Sheets, shared with team.

**Deliverables:**
- [x] User sign-off on all 19 entity schemas (manager approved)
- [x] Source canonicalization confirmed (no changes to source data — 3 designation collisions + 3 shift dupes resolved)
- [x] Holiday List dates confirmed (14 Indian national holidays 2025 + 2026)
- [x] 19 data CSVs generated in `masters/` (1.9 MB total)
- [x] Manager downloaded from GitHub, imported to Google Sheets, shared with team

---

## Phase 2: Site Setup (PENDING)

**Goal:** Create Haritha Hospitals site on a fresh environment.

**Prerequisites (open):**
- ❓ Site location (which env?):
  - pberpqa busy (has pberpqa hospital demo)
  - pberpDEV Synvok legacy
  - dev-erp Processleap legacy
  - **NEW env** (recommended for clean slate)
- ❓ Custom app `haritha_hospital` — needed OR just custom fields + fixtures?

**Plan (recommended):**
1. Create new dedicated env for Haritha Hospitals (clean slate)
2. Apps: frappe 16.x, erpnext 16.x, hrms 16.5.0 (pinned), payments
3. Skip custom app initially — use custom fields + fixtures for haritha-specific data
4. Create Company "Haritha Hospitals" with currency=INR, country=India, FY Apr-Mar
5. Load Holiday List (14 national holidays 2025+2026)

**Deliverables:**
- [ ] Site location decided (NEW env?)
- [ ] Apps installed: frappe, erpnext, hrms 16.5.0, payments
- [ ] Custom app: TBD (use custom fields + fixtures for now)
- [ ] Company "Haritha Hospitals" created
- [ ] Holidays loaded
- [ ] Pre-flight backup (per backup script pattern, 4×/day cron)

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
| 2026-08-19 | Shift name = 10-char code itself (no separate `shift_code` field) | User simplification — name IS the code |
| 2026-08-19 | Holidays = standard Indian national + 4-5 Telangana | User confirmed |
| 2026-08-19 | Custom leave types = deferred | User said Haritha adds later |
| 2026-08-19 | Leave allocation = standard Indian defaults | User confirmed; rules in remarks column |
| 2026-08-19 | Source data = DO NOT modify | Canonicalization at import time only |
| 2026-08-19 | SSA is HRMS-native (Shift Schedule Assignment DocType) | Originally doubted; verified via docs.frappe.io/hr/shift-schedule-assignment |
| 2026-08-19 | Comprehensive 7-change schema update | 9 HRMS docs verified; HRMS v15 canonical structure applied |
| 2026-08-19 | 19 CSVs schema + data combined format | Manager-friendly for Google Sheets review |
| 2026-08-19 | 3 designation collisions resolved automatically | Physician Asstant+Assistant, Sr.Executive+Senior Executive, Sr.Manager+Senior Manager |
| 2026-08-19 | 3 shift code duplicates consolidated | A4+Shift-A, B2+Shift-B, C1+Shift-C |
| 2026-08-20 | Phase 0 + 1 signed off by manager | Schema + data CSVs approved |

---

## Subagent Log

| Date | Task | Agent | Status |
|---|---|---|---|
| 2026-08-19 12:30 | pberpqa reference + scout analysis | pberpqa_ref_an | ✅ done |
| 2026-08-19 12:30 | Source data Excel analysis | source_data_an | ✅ done |
| 2026-08-19 12:30 | Tracker + docs scan | tracker_docs_an | ✅ done |
| 2026-08-19 14:00 | Week-off pattern analysis | pberpqa_week_off_an | ✅ done |
| 2026-08-19 16:06 | Read 9 HRMS shift management docs | read_shift_mgmt_doc, read_shift_type_doc, read_shift_location_doc, read_shift_request_doc, read_shift_assignment_doc, read_shift_schedule_doc, read_shift_assignment_tool_doc, read_ssa_doc, read_roster_doc | ✅ done |
| 2026-08-19 15:33 | Update schema CSV (add SS, SSA, SR + remove shift_code) | update_schema_csv | ✅ done (commit 8307c0b) |
| 2026-08-19 15:42 | Comprehensive 7-change schema update | comprehensive_csv_update | ✅ done (commit aac7b3e) |
| 2026-08-19 19:35 | Generate 19 schema+data CSVs | generate_19_csvs | ✅ done |
| 2026-08-19 22:47 | Push 19 CSVs to GitHub | commit_push_masters | ✅ done (commit 21d54f4) |

---

## Open Questions

1. **Site location** — which env for Haritha Hospitals? (NEW env recommended)
2. **Custom app `haritha_hospital`** — needed or just custom fields + fixtures?
3. Hospital-specific holidays (founder day, anniversary)?

**Resolved:**
- ~~Telangana 2025 + 2026 holiday list~~ — using standard Indian national 14 holidays (per user)
- ~~Shift code convention~~ — 10-char `[P][HHMM][S][HHMM]`, name IS the code
- ~~Source data canonicalization~~ — 3 designation + 3 shift dupes resolved at import time

---

*Last updated: 2026-08-20 10:12 IST — Phase 1 signed off*
