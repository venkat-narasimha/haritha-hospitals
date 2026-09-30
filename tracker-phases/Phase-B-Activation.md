# Phase B Activation — Auto-Attendance Production

**Date:** 2026-09-30
**Status:** ⚠️ B.1–B.4 COMPLETE (data config), but auto-attendance NOT operational end-to-end due to critical scheduler env blocker discovered in B.3
**Wall time:** ~15 min (data config + docs + backup), pre-flight diagnostics ~25 min
**Owner:** Venkat Narasimha

---

## TL;DR

Auto-attendance production configuration activated on prod (`prod-env.duckdns.org`). Scheduler (fixed in Phase 0 Fix B) IS firing, but **all HRMS jobs are silently failing** with `ModuleNotFoundError: No module named 'hrms'` inside `frappe.get_attr()`. Phase B config is correct — `working_hours_threshold_for_absent=2.0` on all 26 Shift Types, Holiday List `weekly_off=NULL`, `Morning-8h.last_sync_of_checkin` set. **Auto-attendance is NOT actually running end-to-end** until the scheduler env issue is resolved. This is the most critical prod blocker since Phase 0.

## Execution steps

1. **B.1** — Fixed `working_hours_threshold_for_absent` 0.0 → 2.0 on all 26 Shift Types
2. **B.1.5** — Fixed `Morning-8h.last_sync_of_checkin` (was NULL → now `2026-09-30 07:07:17`) per LEARNINGS.md #42
3. **B.2** — Fixed Holiday List `weekly_off` Sunday → NULL (column type: varchar(140), NULL allowed)
4. **B.3** — Reconciled attendance vs checkin for last 7 days; discovered critical ModuleNotFoundError blocker
5. **B.4** — Fresh backup + sign-off docs

## End state

- All 26 Shift Types have `working_hours_threshold_for_absent = 2.0`
- All 26 Shift Types have `last_sync_of_checkin` set (Morning-8h was the only NULL)
- Holiday List `weekly_off = NULL` (no auto-Sunday-off; relies on holiday-list entries only)
- 26/26 Shift Types still have `enable_auto_attendance = 1`
- Scheduler firing normally (Hourly Long cadence, `last_execution` updates hourly)
- **BUT** scheduler job execution fails 100% of the time for HRMS methods (15 methods, 0 successes in 7 days, ~210 invocations failed)

## Reconciliation baseline (last 7 days, captured 2026-09-30 ~12:30 IST)

- Total attendance (last 7 days): 180 records
- Total checkins (last 7 days): 0 records (last real checkin: 2026-09-18 10:25:29 IST)
- Status distribution (last 14 days): 532 Absent, 6 WFH, 2 Present, 1 On Leave
- 532/541 attendance records have shift linkage, all with `working_hours=0`
- Date conversion note: MySQL `@@system_time_zone=UTC` but `time`/`attendance_date` columns store IST. `NOW()` returns UTC. Future-dated attendance (last_att_date=2026-10-02) indicates a 1 record manually entered for an upcoming planned leave.

## Critical runtime blocker (discovered in B.3)

**Symptom:** Every HRMS scheduler job fails. `tabScheduled Job Log` shows:
```
File "apps/frappe/frappe/core/doctype/scheduled_job_type/scheduled_job_type.py", line 156, in execute
    frappe.get_attr(self.method)()
builtins.ModuleNotFoundError: No module named 'hrms'
```

**Pattern:** 100% failure rate for HRMS methods over 7 days (15 methods × ~14 hourly firings = 210 failures). Frappe/ERPNext jobs (337 in 24h) succeed fine. `bench console` and `bench execute` CAN import `hrms` (Apps in namespace: `frappe, erpnext, hrms, <custom>`).

**Scheduler process details:**
- PID 1: `/home/frappe/frappe-bench/env/bin/python -m frappe.utils.bench_helper frappe schedule`
- Python venv: `/home/frappe/frappe-bench/env/bin/python` (Python 3.14.2)
- Apps directory: `/home/frappe/frappe-bench/apps/{erpnext,frappe,<custom>,hrms}` — all 4 apps present
- Bench venv CAN import hrms (verified manually)
- System Python (`/usr/local/bin/python3`) CANNOT import hrms (no apps on sys.path)

**Hypothesis (NOT yet root-caused):** `frappe.get_attr()` invocation chain in scheduled_job_type.py:156 is failing to resolve the `hrms` module despite the bench venv having it. Likely cause: apps.txt, PYTHONPATH, or container mount path divergence between `bench_helper` startup and per-job method resolution.

**Why Phase B cannot fix this:** B.1–B.4 are data-level config changes (UPDATE on `tabShift Type`, `tabHoliday List`). The ModuleNotFoundError is a process/env issue. Fixing it requires scheduler container restart (currently forbidden by constraint) or env config edit (deferred).

## Biometric device offline observation

Production biometric checkin devices appear offline since 2026-09-18. Last 2 real checkins: 2026-09-17 09:01:03, 2026-09-18 10:25:29 (both employee `HR-EMP-00421`). Bulk historical 2025-06 data (~420 checkins/day) was imported once and hasn't been refreshed. **Even after scheduler env is fixed, auto-attendance will mark employees Absent until biometric devices come back online and checkins resume.** This is a parallel operational issue requiring IT/HR follow-up.

## Backup

- Bundle: `prod-env_backup_20260930_124132.tar.gz`
- Path: `/home/<user>/backups/prod/20260930_124131/prod-env_backup_20260930_124132.tar.gz`
- Size: 2,700,232 bytes (2.6 MB)
- SHA256: `45dc04fbf2c10932b490051f487bd9a17313b785cb94c86d213033415558b151`
- Offsite: rsync OK to `<user>@[redacted-IP]:/home/venkat/prod-env_backups/` (timestamp 2026-09-30 12:41)
- Contains: site_config_backup.json (261B), database.sql.gz (2.7MiB), files.tar (10KiB), private-files.tar (10KiB)

## Related documentation

- `docs/DECISIONS.md` — decisions log (Phase B COMPLETE entry added)
- `docs/handbook/05-process/04-final-production-plan-2026-09-29.md` — final production plan (§6 Phase B status added)
- `docs/handbook/05-process/03-project-go-live-audit-2026-09-29.md` — baseline verification
- `LEARNINGS.md #42` — HRMS Shift Type requires `last_sync_of_checkin` set or `process_auto_attendance` silently skips

## Known deferred (Phase D)

- SMTP not configured (notification emails still don't deliver)
- Manual `bench execute process_auto_attendance_for_all_shifts` 300s timeout (when env fixed, scheduler handles fine)

## Known deferred (NEW — needs Phase B' / pre-Phase C)

- ⚠️ Scheduler HRMS ModuleNotFoundError root-cause + fix (DO NOT defer to Phase D — blocks auto-attendance entirely)
- Biometric checkin device offline restoration (operational, not engineering)
