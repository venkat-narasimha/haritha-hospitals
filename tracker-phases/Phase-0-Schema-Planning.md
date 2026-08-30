# Phase 0 — Schema Planning & Approval

> **Consolidated file** — merged from `003-phase-0-schema-planning.md`, `004-phase-1-schema-approval.md`, `005-phase-1.5-csv-master-reverify.md` (chronological).

----

## Source: 003-phase-0-schema-planning.md (Phase 0: Schema Planning)

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



---

## Source: 004-phase-1-schema-approval.md (Phase 1: Schema Approval)

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



---

## Source: 005-phase-1.5-csv-master-reverify.md (Phase 1.5: CSV Master Re-Verification)

## Phase 1.5: CSV Master Re-Verification (2026-08-25 22:00 IST) ✅

**Goal:** Validate the 19 CSV masters before ingestion (catch data corruption + schema drift early).

**Status:** ✅ Complete. All 7 checks PASS. 0 FAILs, 0 WARNs. 24,758 rows across 19 entities.

**Deliverables:**
- [x] Reusable verify script: `scripts/verify_csvs.py` (also runs Phase 4 post-ingest count comparison)
- [x] Investigation script: `scripts/investigate_failures.py` (one-shot, captured findings)
- [x] JSON report: `reports/verify_pre_ingest_20260825_2200.json`
- [x] Human-readable report (printed to stdout)

**Checks performed (7):**
1. ✅ Row counts vs manifest — all 19 entities match
2. ✅ Designation collisions (3 known pairs resolved Aug 19) — 0 present
3. ✅ Shift duplicates (A4, B2, C1 resolved Aug 19) — 0 present
4. ✅ Shift code format — 25/25 valid
5. ✅ FK integrity Employee ↔ Shift Type ↔ Shift Assignment — 0 orphans (5,317 SAs checked)
6. ✅ Holiday completeness — 8 unique × 2 years = 14 rows (Haritha-selected Indian national)
7. ✅ FK holistic (no dupes across Dept/Company/Desig) — clean

**Findings (to MEMORY candidates):**

| # | Finding | Impact |
|---|---|---|
| A | Actual shift code format = `[GMAN]\d{4}[RS]\d{4}` (10-char) | MEMORY decision (Aug 19) was wrong — said `[P][HHMM][S][HHMM]`. Actual codes: G=General (12), M=Morning (7), A=Afternoon (3), N=Night (3); R=Regular end, S=Special end. |
| B | `employee.csv` has **NO `name` column** | Schema is `employee_name, employee_number, status, department, designation, employment_type, default_shift, date_of_joining, company, is_synthetic_data, branch, gender, date_of_birth, user_id, holiday_list, attendance_device_id`. Join key for `shift_assignment.employee` = `employee.attendance_device_id` (EMP-NNNN format). 210/210 match. |
| C | Verify script format assumption | `## Data` marker + header line + data rows. `csv.DictReader` needs the header in its input — pass `readlines()[header_idx:]` not `[data_start:]`. |

**Initial run had 2 false positives (regex too strict + wrong FK column) — fixed in same script, re-run PASS.**

