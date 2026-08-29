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

