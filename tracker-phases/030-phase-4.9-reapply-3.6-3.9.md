## Phase 4.9: Re-apply Phase 3.6 + 3.9 (✅ DONE 2026-08-28 15:18 IST)

**Status:** ✅ Complete. Re-applied Phase 3.6 (bulk submit) + Phase 3.9 (department + employee_name) + re-created Property Setter (was reverted by Phase 4.8 restore).

**Discovery:** At script-run time (15:18 IST), pre-state check showed **all 4 metrics already at target** (Holiday=14, Attendance=6300, dept=6300, name=6300). The HRMS subagent 356050a3 (running in parallel, working on in_time/out_time/late_entry/early_exit) had also re-submitted the records as a side effect of populating the HRMS-computed fields. Property Setter for `Attendance.status.options` was empty (reverted by restore), and was re-created using `scripts/recreate_property_setters.py`.

**Before → After:**
- Holiday docstatus=1: 14 → 14 (already at target via HRMS subagent)
- Attendance docstatus=1: 6,300 → 6,300 (already at target via HRMS subagent)
- Attendance with dept: 6,300 → 6,300 (already at target via HRMS subagent)
- Attendance with employee_name: 6,300 → 6,300 (already at target via HRMS subagent)
- Property Setter Attendance-status-options: missing → recreated

**HRMS-computed fields (also populated, separate work):**
- Attendance with in_time: 4,270 / 6,300
- Attendance with out_time: 4,270 / 6,300
- Attendance with late_entry=1: 973 / 6,300
- Attendance with early_exit=1: 1,397 / 6,300

**Reapply script result (idempotent, 0 records affected):**
- Holiday submitted: 0 / 14 (no drafts)
- Attendance submitted: 0 / 6,300 (no drafts)
- naming_series backfilled: 0 (already populated)
- dept/name updated: 0 (already populated)

**Backup:** `pberpprod_backup_20260828_151719.tar.gz` (2.0 MB) — SHA256 `212282ba19eb697554443446fd373cec3bb4ec3248173a0ef1636c287980bf0e`. Offsite rsync OK to venkat@135.125.196.35.

**Scripts:**
- `scripts/reapply_phases_3_6_3_9.py` — idempotent (filters docstatus=0 only, dept/name only).
- `scripts/recreate_property_setters.py` — idempotent PS recreate (re-used).

**Lesson applied:** #79 (pre-mutation backup with SHA256 + offsite rsync), #72 (pre/post-state verify with same query set), #105 (controller-level status check monkey-patch), #106 (SQL fallback when doc.submit() raises), #119-#123 (use `bench console < script.py` not `bench console -c "..."`; for bench execute use module method paths; for full-script execution in console use `exec(open(...).read())` or `importlib.util.spec_from_file_location()`).

**User decision (2026-08-28 15:16 IST):** Full re-apply (vs Selective or HRMS-only).

**Note:** Phase 4.6-4.7 (SSA Option B), Phase 4.1-4.5 (end_time + color + Location + SS submit) all preserved through restore (those changes were in scripts/deployment, not direct SQL on these tables).

