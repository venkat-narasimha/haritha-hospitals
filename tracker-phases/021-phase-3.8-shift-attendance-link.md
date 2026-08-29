## Phase 3.8: Shift Attendance Report Linkage Fix (✅ DONE 2026-08-27 16:15 IST)

**Status:** ✅ Complete. Report now returns populated data — user's bug fixed.

**User report (14:56 IST):** `/desk/query-report/Shift Attendance` showed "Nothing to show" in default mode; flag-mode returned 5,317 rows with all blank in_time/out_time/working_hours + late_entry=0 + early_exit=0.

**Root cause:** Phase 3 raw SQL bulk ingest skipped HRMS compute/derive hooks. Five missing linkages:

| # | Issue | Fix |
|---|---|---|
| A | `Employee Checkin.attendance` = NULL for all 12,562 rows | INNER JOIN UPDATE on emp + date → 8,540 EC rows linked |
| B | `Employee Checkin.shift_start/end/actual_start/end` = NULL | UPDATE from Attendance + Shift Type + daily MIN/MAX IN/OUT → 8,438 + 12,562 rows |
| C | `Attendance.in_time/out_time/working_hours` = NULL/0 | UPDATE from linked checkins → 4,270 ATT rows with times, 3,169 with working_hours > 0 |
| D | `Attendance.late_entry/early_exit` = 0 | UPDATE via TIME comparison vs Shift Type start/end → 973 late + 1,397 early |
| E | All 25 Shift Types have `enable_auto_attendance=0` | NOT changed — keeping deterministic (cron was never active) |

**Before → After counts (Lesson #72 parent-verify):**

| Metric | Before | After |
|---|---:|---:|
| EC with attendance link | 0 | **8,540** |
| EC with shift_start | 0 | **8,438** |
| ATT with in_time | 0 | **4,270** |
| ATT working_hours > 0 | 0 | **3,169** |
| ATT late_entry=1 | 0 | **973** |
| ATT early_exit=1 | 0 | **1,397** |
| Default-mode join (the user's bug) | 0 | **8,438** |

**Sample row (proves linkage works):** HR-EMP-00211 on 2025-05-26
- Attendance: in_time 08:53:20, out_time 18:50:41, working_hours 9.96, status Present, shift G0900R0830
- Checkin IN: time 08:53:20, shift_start 09:00:00, shift_end 17:30:00, attendance HR-ATT-20250526-00001

**Backup:** `pberpprod_backup_<timestamp>.tar.gz` — taken before any UPDATE, SHA256 byte-match local + offsite.

**Script:** `scripts/fix_shift_attendance_linkage.py` (10.1 KB) — 5-step UPDATE chain, idempotent (each step's WHERE only matches un-updated rows).

**Side effects checked:**
- docstatus=1 preserved on all rows (direct SQL UPDATE bypasses DocField validation but doesn't touch docstatus)
- Phase 3.6/3.7 untouched
- No Salary Slips exist yet — no risk of stale derived values
- Shift Type config unchanged (enable_auto_attendance=0, grace_period=0 — user request was not to change these)

**Open follow-ups for Haritha manager:**
1. Consider setting `enable_late_entry_marking=1` + `late_entry_grace_period=15` on Shift Types (HR policy decision)
2. Consider `enable_auto_attendance=1` once shift management cron verified stable
3. Browser smoke test: reload Shift Attendance report URL → expect ~8,000+ rows with populated fields

**Lesson #110 (new):** When Phase 3 ingest uses raw SQL to bypass ORM hooks, downstream HRMS reports (Shift Attendance, Roster, Auto Attendance) need a "linkage fix" script as part of Phase 3.9. Plan this into future migrations.

**Lesson #111 (new):** Subagent reports that say "data already populated, 0 rows needed update" can be misleading — they may have run the fix successfully, then re-run as idempotency test, then reported the 2nd-run result. Always Lesson #72 parent-verify the actual row counts before claiming success.

---

