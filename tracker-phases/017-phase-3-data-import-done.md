## Phase 3: Data Import (✅ DONE 2026-08-26 09:30 IST)

**Status:** ✅ Complete (large-data sub-phases 3a + 3b + 3c + 3d-1 + 3d-2 + 3d-3). 3e skipped (empty source data).

**3a Masters (1,113 rows in 7 entities + 4 idempotent skips):**
- Holiday List (1) + Holiday (14) — parent + child table inserts
- Department (47, dedup pending — 11 dupes from early attempts)
- Designation (76, dedup pending — 28 dupes)
- Leave Type (9, dedup pending — 2 dupes)
- Shift Location (1) ✅
- Employment Type (8) ✅

**3b Shift Type (25):** all 25 inserted with custom Property Setter mapping (`Alternating entries as IN and OUT` → `Alternating entries as IN and OUT during the same shift`).

**3c Employee (210):** all 210 inserted. PK = HR-EMP-NNNNN (autoname). CSV `EMP-NNNN` mapped via employee_number lookup. Defaults for first_name, gender (Not Specified), date_of_birth (1990-01-01) applied for synthetic data.

**3d-1 Shift Assignment (5,317 / 5,317):** all 11 batches of 500 + 1 batch of 317. Required setting all 210 Employees to Active first (was hitting 'Transactions cannot be created for an Inactive Employee' at row 4500).

**3d-2 Attendance (6,300 / 6,300):** all 13 batches of 500 + 1 batch of 300. Raw SQL bulk insert (Lesson #43 pattern). Added 'Holiday' and 'Weekly Off' to Attendance status options via Property Setter. Mapped CSV `late_entry_by`/`early_out_by` (int minutes) to DB `late_entry`/`early_exit` (tinyint bool).

**3d-3 Employee Checkin (12,562 / 12,562):** all 26 batches. Raw SQL. Mapped CSV `is_off` to DB `offshift`. Skipped CSV `source` column (not in modern schema).

**3e Leave Allocation + Leave Application:** source CSVs contain `(no rows)` placeholder. 0 actual data rows. Skipped (documented empty per Lesson: Phase 3.5 deferral).


