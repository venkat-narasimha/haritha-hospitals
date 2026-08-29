## Phase 3.9: Populate Attendance.department + employee_name (✅ DONE 2026-08-27 19:12 IST)

**Status:** ✅ Complete. Both columns now populated for all 6,300 Attendance rows.

**Why:** Phase 3 raw SQL bulk ingest skipped FK-derived fields. ORM `frappe.get_doc().insert()` would have auto-derived `employee_name` and `department` from the Employee FK; raw SQL does NOT. Result: Shift Attendance report's department column was empty for all 6,300 rows.

**Fix:** Single SQL UPDATE pass via INNER JOIN to `tabEmployee`. Both columns populated atomically in one query.

**Before → After:**

| Field | Before | After |
|---|---:|---:|
| department populated | 0 | 6,300 |
| employee_name populated | 0 | 6,300 |
| Orphan FK (attendance without Employee match) | 0 | 0 |
| docstatus=1 (Phase 3.6 preserved) | 6,300 | 6,300 |

**Backup:** `pberpprod_backup_20260827_191033/` — 4 files (database.sql.gz 1.8 MiB, files.tar, private-files.tar, site_config_backup.json) + sha256 byte-match local ↔ offsite (venkat@135.125.196.35). DB SHA256 first 16: `7a113f9c852e4c37`.

**Script:** `scripts/populate_attendance_meta.py` — idempotent (WHERE only matches empty rows). Re-run as sanity check returned 0 matches.

**Sample row (HR-ATT-20250526-00001):**
- attendance.employee_name = `'Manager-1001'` = employee.employee_name ✅
- attendance.department = `'Maintenance - HH'` = employee.department ✅

**Side effects:** None. Direct SQL UPDATE on Attendance; no controller hooks fired; docstatus=1 preserved on all rows; Phase 3.6/3.7/3.8 untouched. Property Setters (status options, Attendance-status-options) untouched.

**Lesson #112 (new):** Any FK-derived field (employee_name, department, etc.) needs to be explicitly included in raw SQL INSERT, OR populated post-ingest via INNER JOIN. ORM auto-derives; raw SQL doesn't. This is the same root cause as Phase 3.6 naming_series issue (Lesson #104) and Phase 3.8 linkage-fix (Lessons #110/#111) — all symptoms of bypassing ORM hooks. Future raw-SQL ingest scripts should enumerate derived/FK fields explicitly in their column list.

**Note on row-count extraction:** `frappe.db.sql("UPDATE ...")` returns `()` (empty tuple) in MariaDB — rowcount is not surfaced via the result tuple. The script computes "Estimated rows updated" by diffing the before/after counts instead of trusting the SQL result. Verified idempotent by re-running and confirming 0 matches.

---

