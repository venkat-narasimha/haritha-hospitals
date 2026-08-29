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

