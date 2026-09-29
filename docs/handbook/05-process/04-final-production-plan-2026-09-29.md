**Final Production Plan Document**  
**Project:** Shift Management + HRMS Foundation (this hospital + Reusable Product)  
**Date:** 29 September 2026  
**Owner:** Venkat Narasimha  
**Last Updated:** 29 September 2026 22:55 IST (live verification integrated)  
**Target:** Full production readiness in 2–3 focused days (long hours acceptable) + reusable foundation  

---

### 1. Goal

Deliver **two things simultaneously**:

1. **this hospital** — a fully production-ready Shift + Attendance + Leave system that can be used daily by the hospital with correct Auto-Attendance, proper approvals, and safe permissions.
2. **Reusable Product** — a clean, generic custom app + Client Onboarding Playbook that can be used for any hospital, medical college, engineering college, or multi-shift organization.

**Success Definition (Definition of Done):**
- HRMS scheduler is firing nightly AND producing correct Attendance records from real check-ins.
- Formal Workflows exist for Leave Application and Shift Request.
- A tested Role × Permission matrix is implemented and documented.
- `leave_approver` populated for all employees with active department heads.
- Security review of roles and data isolation is completed.
- Disaster Recovery restore has been successfully tested once (against a temp container, see Phase D update).
- Custom app is self-contained (installable on a fresh site) and renamed/cleaned.
- A short Client Onboarding Playbook exists.
- An honest "What is live / What is still pending" status document exists.

---

### 2. Scope

**In Scope**
- Organization Management, Employee Lifecycle (basic), Shift Management, Attendance Management, Leave Management
- **HRMS scheduler diagnosis + repair** (added 2026-09-29 after live verification found it silently broken)
- Auto-Attendance activation and correctness
- Formal Workflows (Leave Application + Shift Request, created from scratch — none exist today)
- Complete RBAC / Role matrix + User Permissions + leave_approver bulk population
- Security review (permissions, password policy, data isolation)
- Disaster Recovery test (against temp container — no same-VPS target exists)
- Basic monitoring readiness
- Clean custom app + fixtures
- Client Onboarding Playbook
- Minimal hospital-domain readiness (correct holiday handling, on-call fields usable)

**Explicitly Out of Scope (for this 2–3 day push)**
- Payroll
- Wards, beds, OT, pharmacy, lab, billing
- Advanced NABH continuous-duty rules / complex nurse rotation algorithms
- Full automated test suite and performance load testing
- Real multi-week UAT with all hospital staff (can start immediately after this foundation)

---

### 3. Recommended Custom App Name

**`shift_hrms_foundation`**

- Generic and reusable
- Clearly describes the quantity
- Allows hospital-specific branding to live only in masters, letterheads, and the onboarding playbook

**Timing decision (2026-09-29 22:55):** Rename happens at **end of Phase C**, not start. Mid-plan rename is too disruptive — touches `installed_apps` on every site, `apps.txt`, fixture refs in `migrate_master_data.py`, GitHub repo name, local clones. Doing it at end of Phase C means the rename has the cleanest possible baseline to land on. The app stays as `haritha_hospital` (internal `haritta_hospital`) through Phase A and Phase B; rename is the last action of Phase C, just before fixtures + hooks are re-verified.

(Existing `haritha_hospital` is installed on `prod-env` per verification; rename runbook must handle the migration of `installed_apps` in `site_config.json` atomically with `bench get-app` + `bench install-app` on the new name.)

---

### 4. Role × Permission Matrix (Must Implement First)

| Role                  | Purpose                              | Typical Users                     | Status (2026-09-29) |
|-----------------------|--------------------------------------|-----------------------------------|---------------------|
| System Manager        | Full technical control               | You / technical admin             | ✅ Exists            |
| HR Manager            | Full HR + policy control             | Hospital HR Head                  | ✅ Exists            |
| HR User               | Day-to-day HR operations             | HR executives                     | ✅ Exists            |
| **Roster Manager**    | Create / edit / publish rosters      | Nursing Supervisor / Roster Planner | ❌ **Must CREATE** (not a stock HRMS role) |
| Leave Approver        | Approve leave for own scope          | Department Heads / In-charges     | ✅ Exists            |
| Employee              | Self-service only                    | All staff                         | ✅ Exists            |

**Action item from verification:** Create the `Roster Manager` role as a custom role during Phase A. Sub-decision: if creating it complicates the matrix, substitute with `HR Manager` for v1 and create `Roster Manager` later.

**`leave_approver` field status (2026-09-29):** Only 1 of 212 employees has it populated (Test User → Administrator). Phase A must bulk-populate from department heads before any leave workflow can route at scale.

**User Permissions status (2026-09-29):** Only 2 records exist for 212 employees × 39 departments. Row-level isolation is effectively off. Phase A must bulk-create User Permissions for department-level filtering.

**Core Permission Matrix** (R = Read, W = Write, C = Create, S = Submit, D = Delete, A = Approve)

| DocType / Area                | System Manager | HR Manager | HR User | Roster Manager | Leave Approver      | Employee          |
|-------------------------------|----------------|------------|---------|----------------|---------------------|-------------------|
| Employee                      | Full           | Full       | RWCS    | R              | R (own dept)        | R (own only)      |
| Department / Designation      | Full           | Full       | RW      | R              | R                   | —                 |
| Shift Type                    | Full           | Full       | RW      | RW             | R                   | R                 |
| Shift Assignment / Roster     | Full           | Full       | RWCS    | Full (scoped)  | R                   | R (own)           |
| Employee Checkin              | Full           | Full       | RWCS    | R              | R                   | C + R (own)       |
| Attendance                    | Full           | Full       | RWCS    | R              | R                   | R (own)           |
| Leave Type / Policy / Allocation | Full        | Full       | RWCS    | R              | R                   | R                 |
| Leave Application             | Full           | Full       | RWCS    | R              | Approve (scoped)    | C + R (own)       |
| Holiday List                  | Full           | Full       | RW      | R              | R                   | R                 |
| HR Settings                   | Full           | Full       | R       | —              | —                   | —                 |
| Key Reports                   | Full           | Full       | Full    | Full           | Own dept            | Own only          |

**Mandatory additional rules:**
- Enable "Apply User Permissions" for Employee role.
- Use User Permissions + Department filtering so Leave Approver and Roster Manager only see their scope.
- Create Role Profiles so new users get the correct role bundle automatically.

---

### 5. Detailed Execution Plan (Ordered)

#### Phase 0 — Pre-Flight Diagnostics (NEW, added 2026-09-29 after live verification)

**Must run BEFORE Phase A. If Phase 0 fails, Phase A/B are blocked.**

1. **HRMS scheduler diagnosis** — CRITICAL: all 7 HRMS scheduled cron jobs show `last_execution = 2026-08-28 16:02 IST` (32+ days stale), despite `scheduler.enable=true` and all jobs `stopped=0`. Diagnosis:
 - Check `bench schedule` worker is running on `prod-env-backend-1` (and `prod-env-scheduler-1`). Verify via `docker ps` + `docker logs prod-env-scheduler-1 --since 1h`.
 - If worker not running: identify why and restart. Common causes: crashed worker, not started after container restart, OOM, scheduler lock stuck.
 - Trigger one manual cron run for `process_auto_attendance_for_all_shifts` via `bench execute hrms.hr.doctype.shift_type.shift_type.process_auto_attendance_for_all_shifts` and confirm it completes + updates `last_execution`.
 - Wait one full scheduler tick (~1 hour for Hourly Long, ~24h for Daily Long) and confirm `last_execution` advances.
 - Document the root cause + fix in the daily log.
2. **Fresh backup before any changes** — `bash /home/<user>/scripts/prod-env_backup.sh`; verify tarball produced + offsite push succeeded. Keep the tarball as the rollback baseline for Phase A onwards.
3. **Audit-staleness probe** — verification found that shift types went from 25 → 26, enable_auto_attendance flipped 0 → 1 on all 26, process_attendance_after populated, holidays 12 → 14, departments 37 → 39, shift assignments 8118 → 7830 (288 pruned). Someone has been making changes. Confirm via git log on the project repo + daily memory: were these changes intentional? If not, identify who made them and whether to revert.
4. **Forward-dated Attendance investigation** — verification found `last_attendance_date = 2026-10-02` (3 days ahead of system date 2026-09-29). Investigate: which script/bulk operation created these? Should they be deleted?

**Exit criteria for Phase 0:**
- HRMS scheduler fires at least one cron successfully, with `last_execution` advancing.
- A fresh prod backup exists on local + offsite.
- Audit-staleness probe findings are documented and decision recorded (revert / keep / unrelated).
- Forward-dated Attendance is either explained or cleaned up.

---

#### Phase A — RBAC + Workflows + leave_approver + User Permissions + Per-Role Dashboards (Day 1 Morning – Highest Priority)

**Venkat's Phase A requirements (recorded 2026-09-29 23:08 IST):**

- **R1 — Plan roles, permissions, workflows in detail** (not just outline). Done at start of Phase A, before any change. Detailed design must be reviewed + signed off by Venkat before execution.
- **R2 — User dashboard for every role** with their respective permissions + access. 6 roles → 6 dashboards (Workspace + module visibility + custom cards). Not "Desk default" — built per role.
- **R3 — Derive roles / permissions / access from existing designations.** 39 departments × 49 designations exist in prod. Observe the data, cluster designations into role-candidates, assign per best practices + org structure.

**Phase A steps:**

A.0. **Analyze Designation + Department data (R3 pre-work).** Pull all 49 Designations + 39 Departments from prod. Cluster designations into role-candidates:
- e.g., "HR Head" / "HR Manager" designations → `HR Manager` role
- "Nursing Supervisor" / "Roster Planner" → `Roster Manager` role
- "Department Head" / "In-Charge" → `Leave Approver` role
- "Doctor" / "Nurse" / "Technician" / "Support Staff" → `Employee` role (self-service)
- "System Admin" / "Technical" → `System Manager` role
- "HR Executive" / "HR User" → `HR User` role

Document the designation → role mapping as the basis for permission grants + dashboard design. **This is the gate before role creation; nothing else in Phase A proceeds without this map.**

A.1. **Create the missing `Roster Manager` role** (custom role — does not exist). Configure per-role settings.

A.2. **Confirm the other 5 roles** (System Manager, HR Manager, HR User, Leave Approver, Employee already exist per verification).

A.3. **Create Role Profiles** for each of the 6 roles — bundle roles for new-user assignment.

A.4. **Configure Permission Manager** exactly per the matrix in §4. Apply designation-based role grants from A.0.

A.5. **Bulk-populate `leave_approver`** on all 212 Employee records — derive from department head mapping (from A.0). Department → Leave Approver (User). Verify by query after bulk update.

A.6. **Bulk-create User Permissions** for all 212 employees + dept-level filtering. Each employee gets a User Permission row for their Department. Each Leave Approver gets a User Permission for their department scope. Verify count goes from 2 → ~250+ records.

A.7. **Create 2 Workflows** from scratch (currently 0 exist):
- Leave Application: states Draft → Pending Approval → Approved / Rejected. Approver routing uses Employee.leave_approver.
- Shift Request: same pattern.

A.8. **Build user dashboard per role (R2).** Workspace + module visibility + cards for each role:
- **System Manager**: full Desk visibility, all modules, standard Workspace.
- **HR Manager**: HR + Shift + Leave modules + custom HR Dashboard (employee census, leave summary, attendance summary, open workflows).
- **HR User**: HR module (limited per Role Permission Manager) + custom HR-User Dashboard.
- **Roster Manager**: Shift-Management focused — Roster Workspace (today's roster, this week's roster, attendance summary per shift, pending shift requests).
- **Leave Approver**: Leave focused — Leave Approver Workspace (pending approvals queue, team leave calendar, attendance vs leave summary).
- **Employee**: Self-service — Employee Workspace (my profile, my attendance, my leave balance, my shifts, my requests).

A.9. **Test with one user per role** (6 users). For each: log in, verify dashboard renders, verify role-based visibility, exercise the role's typical workflow end-to-end.

A.10. **Take a backup** at end of Phase A before Phase B begins.

---

#### Phase B — Auto-Attendance Activation (Day 1 Afternoon)

**Pre-condition:** Phase 0 confirmed HRMS scheduler is firing. If not, STOP and re-run Phase 0.

1. **Verify Shift Type flags are correctly set** — verification already shows `enable_auto_attendance=1` on all 26 (good). Confirm on each shift.
2. **Fix `working_hours_threshold_for_absent`** — verification shows `0.0` on all 26 shifts (absent detection effectively disabled). Set to **2.0** hours (sensible default). Apply to all shift types via bulk script.
3. **Fix Holiday List `weekly_off`** — currently `Sunday` on the only Holiday List (14 entries). For a hospital where Sundays ARE working days in OPD/IPD, this misclassifies ~52 work-days/year. Options:
 - (a) Remove `weekly_off` entirely (no auto weekly off; per-shift Sunday work).
 - (b) Keep Sunday as weekly off for non-clinical departments only, set per-department shift policy.
 - (c) Set `weekly_off` to a department-specific value via custom field.
 - **Recommended for v1:** option (a) — remove weekly off, rely on holiday-list entries for actual holidays. Validate against 1 week of Sunday attendance after the change.
4. **Verify `process_attendance_after`** — verification shows it populated on all 26 (good). Confirm cutoff dates are reasonable (not in the future).
5. **Trigger one manual Auto-Attendance run** — `bench execute hrms.hr.doctype.shift_type.shift_type.process_auto_attendance_for_all_shifts` and verify Attendance records update correctly (count delta vs yesterday).
6. **Reconcile** Attendance count vs Employee Checkin count for the last 7 days. Document any gaps.
7. **Take a backup** at end of Phase B.

**Note from verification:** shift_assignment_count went from 8118 → 7830 (288 pruned) between audit and now. Investigate whether 288 were legitimately expired (use `mark_expired_shift_assignments_as_inactive` cron output) or were bulk-deleted. Either way, document.

---

#### Phase C — Custom App Hardening & Reusability (Day 2)

1. **Clean up scripts directory** — archive all old `_v1`, `_v2`, `fix_*` versions (per audit: 12 superseded ingest scripts, 14 fix-scripts).
2. **Complete fixtures export** — audit confirmed only 5 of 274 Haritha customizations are in fixtures. Verify each Custom Field, Property Setter, Notification, Letter Head, Print Format is in the custom app fixtures, OR in an env-init script that runs during install.
3. **Make `hooks.py` useful** — verification shows all sections except `fixtures` are commented out. At minimum populate:
 - `scheduler_events` (if HRMS-scheduled jobs need to be registered here)
 - any required `doc_events` for the workflows created in Phase A
4. **Rename custom app** at **end of Phase C** (per §3 timing decision). Rename runbook:
 - `bench uninstall-app haritha_hospital --site prod-env` (after backup)
 - Update `apps.txt` (remove `haritha_hospital` line)
 - Rename GitHub repo from `haritha_hospital` → `shift_hrms_foundation`
 - `bench get-app https://github.com/venkat-narasimha/shift_hrms_foundation.git`
 - Update module paths in code: `haritta_hospital` → `shift_hrms_foundation`
 - `bench install-app shift_hrms_foundation --site prod-env`
 - Verify site loads + login works
 - Update local clone to new repo URL
5. **Verify install on a fresh site** — run the new app's `migrate_master_data` on a temp container or restored site; confirm all 274 customizations apply cleanly.
6. **Write the Client Onboarding Playbook** (short, step-by-step):
 - New site creation
 - Install custom app
 - Load masters
 - Configure Shift Types / Holiday Lists / Leave Policies
 - Set up Roles & Permissions
 - Activate Auto-Attendance
 - UAT checklist
 - Variants for Hospital / Medical College / Engineering College / Factory

---

#### Phase D — Production Hardening (Day 2 Evening + Day 3)

1. **DR test against a temporary target** — verification found **NO DR target exists** (no `qa-env`, no `dev-env` on this VPS). Options:
 - (a) Spin up a temporary `prod-env-dr-test` site in a new container, restore last backup into it, verify functionality, tear down. Heavy but real.
 - (b) Restore last backup into a docker volume + spin up a one-off MariaDB + bench + nginx stack on a non-standard port. Same as (a) but cleaner isolation.
 - (c) Skip DR test for this push and explicitly defer.
 - **Recommended for v1:** (a) or (b). The plan originally assumed a same-VPS target — that assumption is wrong; adapt.
2. **Basic security review checklist:**
 - No overly broad permissions (Phase A matrix should already address most)
 - Password policy reviewed
 - Employee data isolation confirmed (post Phase A User Permissions)
3. **Enable and test critical Notifications** (Leave approval, Shift assignment change). Verification confirmed `send_leave_notification=1` + template `Leave Approval Notification` already set. Test end-to-end.
4. **Create a short "Production Status & Known Limitations" document** reflecting the final state after Phase A/B/C/D.
5. **Final end-to-end verification** under the new roles:
 - Check-in → Auto Attendance → Leave Application → Approval → Roster visibility
 - One full flow per role, on the real (non-test) data

---

#### Phase E — Handover Package (End of Day 3)

Deliverables to be produced:
- Updated honest Project Status
- Role × Permission matrix document (with verification screenshots)
- Client Onboarding Playbook
- Known Limitations list
- Clean custom app ready for reuse (renamed `shift_hrms_foundation`)
- Short demo / verification script

---

### 6. What is Explicitly Deferred (After This Plan)

- Advanced NABH continuous-duty and mandatory rest rules
- Complex nurse rotation pattern engine
- Full automated test suite + CI
- Performance load testing report
- Long multi-week UAT with all hospital departments
- Monitoring stack (Sentry, uptime, slow-query alerts) beyond basic readiness
- Upgrade playbook for future HRMS versions
- **NEW (2026-09-29):** Same-VPS DR test target (no `qa-env`/`dev-env` exists; using a temp container for Phase D is sufficient)

These items will be placed in a clear backlog after the foundation is production-ready.

---

### 7. Execution Instructions for OpenClaw / AI Agent

When handing this plan to your AI agent, use this instruction:

> "Execute the Final Production Plan dated 29 September 2026 (updated 22:55 IST with live verification).  
> Start strictly with **Phase 0 (Pre-Flight Diagnostics)** — DO NOT skip to Phase A until Phase 0 exit criteria are met (HRMS scheduler firing + fresh backup + audit-staleness decisions recorded + forward-dated Attendance resolved).  
> Then Phase A (Roles + Workflows + leave_approver + User Permissions).  
> Phase A depends on Phase 0 succeeding (scheduler must fire before any attendance work).  
> Phase B depends on Phase A (auto-attendance + threshold + weekly_off fixes).  
> Phase C (app hardening + rename at end) depends on Phase B.  
> Phase D (DR test + security + e2e) depends on Phase C.  
> Phase E (handover) depends on Phase D.  
> Report status after every major step.  
> Do not skip to later phases until the previous phase is verified.  
> Keep all changes in the custom app or version-controlled scripts.  
> After each phase, produce a short status summary of what was completed and any blockers."

---

### 8. Final Notes

- This plan deliberately puts **HRMS scheduler diagnosis first (Phase 0)** because without it, Phase B's auto-attendance work is a black box. Verification on 2026-09-29 found the scheduler silently broken (32+ days stale) — this is the highest-priority blocker.
- Phase A (RBAC + Workflows) is next because without it the system is not safe for real users.
- Auto-Attendance (Phase B) is the third priority because that's the core value proposition.
- Everything else (app cleanliness, playbook, DR test) turns the current Haritha deployment into a real product.
- **Audit caveat:** the 2026-09-29 audit (`docs/handbook/05-process/03-project-go-live-audit-2026-09-29.md`) is already partially stale relative to live prod (shift types 25→26, auto-attendance flags flipped, holidays 12→14, dept 37→39, shift assignments 8118→7830). Treat the audit as a snapshot; re-run key checks after any major change rather than trusting the audit row counts blindly.

---

### 9. Pre-Execution Findings (Live Verification 2026-09-29 22:49 IST)

This section captures the live state of `prod-env` at the time the plan was updated. Treat as the baseline against which Phase 0–E progress should be measured.

**Access method:** SSH `<user>@[redacted-IP]` → `docker exec prod-env-backend-1 ... bench --site prod-env console` (read-only).

**Phase A baseline:**
- 52 total roles; 5 of 6 plan roles present (`Roster Manager` missing — must create)
- 0 Workflows
- 2 User Permission records
- 1/212 employees with `leave_approver` populated (Test User only)
- HR Settings: `leave_approver_mandatory_in_leave_application=1`, `prevent_self_leave_approval=0`, `standard_working_hours=8.0`

**Phase B baseline:**
- 26 Shift Types (audit said 25 — `Morning-8h` is new)
- All 26 have `enable_auto_attendance=1` (audit said 0 — someone toggled these)
- All 26 have `process_attendance_after` populated (audit said empty)
- All 26 have `working_hours_threshold_for_absent=0.0` (BLOCKER — set to 2.0)
- 1 Holiday List ("this hospital Holiday List") with `weekly_off=Sunday` and 14 entries (audit said 12)
- 7830 Shift Assignments (audit said 8118 — 288 pruned)
- 0 Scheduler Events (Frappe v16 uses Scheduled Job Type)
- 98 Scheduled Job Types, 1 HRMS attendance job found: `process_auto_attendance_for_all_shifts`
- **All HRMS cron jobs `last_execution = 2026-08-28 16:02 IST` — silently broken**

**Custom app baseline:**
- `installed_apps = ["frappe", "erpnext", "hrms", "haritha_hospital"]`
- `haritta_hospital` present, no `__version__` attribute
- Hooks: only `fixtures` populated (5 fixtures: custom_field, property_setter, letter_head, notification, print_format). All other sections commented out.

**Preconditions baseline:**
- Backup script: `/home/<user>/scripts/prod-env_backup.sh` (4248 bytes) exists, cron `0 */6 * * *` registered, latest log `prod-env_backup_20260929_180001.log` (5h old at verify time) — healthy
- DR target: **NONE** (no `qa-env` site, no `dev-env` site)
- Site config: `db_name=[redacted-db-name]`, `db_type=mariadb`, `db_host=prod-env-db-1`

**Audit discrepancies (between 2026-09-29 audit commit and 2026-09-29 22:49 verification):**
- Shift types count: 25 → 26 (new "Morning-8h")
- Shift types `enable_auto_attendance`: all 0 → all 1
- Shift types `process_attendance_after`: empty → populated
- Holiday List entries: 12 → 14
- Departments: 37 → 39
- Shift Assignments: 8118 → 7830 (−288)
- **No git log explanation** found for these changes; this needs Phase 0 audit-staleness probe.

**New findings not in audit:**
- HRMS scheduler silent failure (32+ days stale)
- `leave_approver` sparse (1/212)
- User Permissions sparse (2 records)
- `last_attendance_date = 2026-10-02` (forward-dated by 3 days)
- Only 4 user accounts for 212 employees (OK for HRMS where Employees ≠ Users, but worth noting)

---

*Plan updated by main session on 2026-09-29 22:55 IST based on subagent verification report (`haritha-prod-verify-v2`, run `debbeee7-5a6b-4109-9663-578c65028173`). Read-only verification — no prod writes, no migrations, no commits. Next action: Phase 0 (scheduler diagnosis) on Venkat's YES.*
