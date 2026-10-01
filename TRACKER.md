# this hospital — Project Tracker (Index)

**Project:** this hospital — Real hospital project (CMM Level 5 target)
**Scope:** Shift management + HRMS basics (employees, departments, shift types, attendance, leave)
**Deferred:** Wards, beds, OTs, pharmacy, lab, billing, full CoA, cost centers
**Owner:** Venkat (Processbricks)
**Started:** 2026-08-19
**Stack:** Frappe 16 / ERPNext 16 / HRMS 16.5.0 (pinned) / payments / custom app (TBD)

---

## 📌 Recent Activity (Sep 17–21, 2026) — Demo Readiness Push

5-day intensive push to bring the system to demo-ready state and resolve all sign-off transactions. See [`archive/docs/manager-briefing-2026-09-21.md`](archive/docs/manager-briefing-2026-09-21.md) for the full manager-review briefing.

| Date | Event |
|---|---|
| 2026-09-17 | Demo readiness audit + 1 prod fix (Company.default_holiday_list on this hospital) |
| 2026-09-18 | Manual transaction testing (60 transactions, 6 modules) + Streams 1–5 + sign-off commit (51 PASS) |
| 2026-09-19 | Stream 5 Maximum effort (4 prerequisites + 3 write-tests) + sign-off updated to 58 PASS; Sample Leave Application HR-LAP-2026-00001 submitted end-to-end with Leave Ledger Entry; Fiscal Year fix (2025-2026 + 2026-2027) |
| 2026-09-21 | 211 Holiday List Assignments batch-submitted + renumbering (T-001 to T-079, +19 new transactions); 8 client template items (5 new master templates + 3 template updates); 2 hotfix scrubs (sanitization) |

**Demo readiness verdict (current):** ✅ READY (full, no caveats). Custom Fields 78/78, Property Setters 189/189, Leave Engine (Approver, 211 Holiday List Assignments, Leave Period 2026-2027, 3 Leave Allocations, notification template), HR Settings configured. Test Company kept per operator decision (manual testing sandbox); 0 Branches = single-site per repo Gotcha #12.

**Sign-off state (post-renumber):** 77 ✅ PASS / 0 ⬜ DEFERRED / 1 ❌ NOT DONE / 1 🚫 REMOVED = 78 sign-off rows. Total defined = 79 (1 removed from sign-off but documented as out-of-scope).

---

**Master tracker split:** this file is now a slim index. Full phase detail lives under [`tracker-phases/`](tracker-phases/).

A full backup of the original 1492-line TRACKER.md is preserved at [`tracker-phases/000-FULL-TRACKER-backup.md`](tracker-phases/000-FULL-TRACKER-backup.md).

---

## 📌 Recent Activity (Sep 30 PM, 2026) — Phase B + D + E + Custom App + Leave Approver Attempt

| Date | Event |
|---|---|
| 2026-09-30 12:25–12:30 IST | **Phase B execution batch** — B.1 fixed `working_hours_threshold_for_absent` 0.0 → 2.0 on all 26 Shift Types + fixed Morning-8h `last_sync_of_checkin` (Lesson #42); B.2 changed Holiday List `weekly_off` Sunday → None; B.3 reconciled attendance vs checkin (12,612 → 21,921, +9,309); B.4 took fresh backup + created `Phase-B-Activation.md`. **Phase B closed** (commit `3ab688e`). |
| 2026-09-30 13:30 IST | **Custom app push** — Per Venkat's "dont rename" instruction, rebased + force-pushed local A.11 commit `ec1aa7b` to `github.com/venkat-narasimha/haritha_hospital` with author fix to venkat-narasimha (commit `0a423db`). |
| 2026-09-30 13:48 IST | **Phase D execution batch** (SMTP-less per Venkat choice) — D.1 HRMS heartbeat installed (`HRMS Health Alert` DocType + `HRMS Health Monitor` Server Script, Hourly cadence, sandbox-safe); D.2 12 small depts audit (27 employees on Administrator, 4 with senior candidates, 8 need external); D.2b auto-attendance backfill (same 12,612 → 21,921); D.3a `Role.module_profile` Custom Field + 6/6 roles assigned; D.3b rewrote `Enforce 90-Day Password Expiry` Server Script (datetime import removed); D.3c `User.role_profile_name` root cause = `doc.save()` strips it, `db.set_value()` persists it; D.4 security audit (219 users, 3 admin-like, 451 User Permissions); D.6 image version = Frappe 16.30.0 (matches) + ERPNext 16.31.1 (minor drift). DR test deferred per scope. SMTP deferred per Venkat. |
| 2026-09-30 15:35 IST | **Phase E execution batch** — E.1 project status refreshed (187 lines), E.2 Role × Permission matrix doc (66 cells 11×6), E.3 Client Onboarding Playbook (15 steps), E.4 DECISIONS.md updated (Known Limitations), E.5 verification script (13 checks, executable). **Phase E+1 Org Chart**: 171/211 Employee.reports_to populated + Org Chart card added to HR Manager + Roster Manager Workspaces. **Committed `8be58c7`** to haritha-hospitals repo. |
| 2026-09-30 16:14–17:45 IST | **Sign-off + leave_approver gap attempt** — Venkat chose sign-off + manual CSV fix. Mapped 32 employees on Administrator approver to `medicalsuperdinet1194404@harithahospitals.com`. CSV upload blocked by `ModuleNotFoundError: No module named 'hrms'` in Data Import Tool. Diagnosed: gunicorn workers use system Python, not venv. `sitecustomize.py` fix partially worked. Discovered real startup script is `/usr/local/bin/start.sh` inside container (writable image layer, not bind-mounted). 3 duplicate subagents dispatched by mistake. Found typo (`/frappe/` segment missing on gunicorn path). Fix applied in main session: wrote corrected start.sh, docker cp'd in, docker restart issued. **Verify timed out** — backend status unknown (Venkat to test via browser). 8 known gaps still open for Phase D backlog. |

**Engagement sign-off status:** Phase A + B + D + E closed; Phase C cancelled. 8 known gaps in Phase D/E backlog (SMTP, DR test, Server Scripts sandbox-safe rewrite, 12 small depts leave_approver fallback, image version drift, etc.). All committed to `github.com/venkat-narasimha/haritha-hospitals` + custom app to `github.com/venkat-narasimha/haritha_hospital`.

**Custom app state:** Python module `haritta_hospital` (historical double-t typo), repo URL `haritha_hospital` (correct). Both Phase A + A.11 fixtures committed.

---

## 📌 Recent Activity (Sep 30 PM, 2026) — HRMS Module Not Found Fix

| Date | Event |
|---|---|
| 2026-09-30 ~18:00 IST | **HRMS Module Not Found fix saga begins** — Venkat tried importing 30-row CSV to assign `leave_approver` to the 32 employees still on Administrator fallback. Data Import Tool threw `ModuleNotFoundError: No module named 'hrms'`. Root cause: gunicorn workers (system Python) didn't have hrms in `sys.path` because HRMS was installed via `bench install-app` at runtime, not baked into the image. |
| 2026-09-30 ~18:10 IST | **Fix attempt 1 — sitecustomize.py:** Created `/usr/local/lib/python3.14/site-packages/sitecustomize.py` adding venv site-packages to `sys.path`. Verified `import hrms` works in fresh Python, but **did not fully fix it** because gunicorn workers (preforked with stale sys.path) still failed. |
| 2026-09-30 ~18:20 IST | **Fix attempt 2 — start.sh source venv:** Modified `/home/<user>/scripts/start.sh`. **Discovered stale file** — actual active file is `/home/<user>/erpnext/erp-prod/compose.yaml`. |
| 2026-09-30 ~18:35 IST | **Backend crash loop (typo):** Patched correct file `/usr/local/bin/start.sh` inside container with gunicorn path missing `/frappe/` segment → container exit-126 crash loop. Fixed via main session. |
| 2026-09-30 ~18:40 IST | **Read-only audit (subagent)** — Confirmed active compose = `compose.yaml` (not pwd.yml), image = `frappe/erpnext:v16.31.1` (PUBLIC, no HRMS baked in). Compose template supports `${CUSTOM_IMAGE:-frappe/erpnext}:${CUSTOM_TAG:-...}` env vars. Builder dir: `/home/<user>/erpnext/erp-prod/` (frappe_docker clone with `images/layered/Containerfile`). Data preserved via named volumes. |
| 2026-09-30 ~19:00–22:40 IST | **4× rebuild attempts via subagent failed** because Gateway restarts killed the long-running subagent sessions (build takes 10–15 min). |
| 2026-09-30 ~22:30 IST | **Manual build by Venkat — SUCCESS.** Created `apps.json` (only `[frappe/hrms v16.5.0, venkat-nasimha/haritha_hospital main]` — frappe/erpnext baked into layered base image). Built via `docker buildx build --build-arg FRAPPE_BRANCH=version-16 --build-arg APPS_JSON_BASE64="$(base64 -w0 apps.json)" -t frappe/custom_apps:version-16 -f images/layered/Containerfile .`. Image created (3.47 GB) with all 4 apps. |
| 2026-09-30 ~22:40 IST | **Deployed** via `docker compose up -d` (~5 min downtime, all volumes preserved). All 7+ containers on `frappe/custom_apps:version-16`. |
| 2026-09-30 ~22:40 IST | **Verified `import hrms` works** via `docker exec erp-prod-backend-1 /home/<user>/frappe-bench/env/bin/python -c "import hrms"`. Scheduler still firing (last HRMS execution at 22:34:07). Backend HTTP 200. |
| 2026-09-30 ~22:45 IST | **Server Script fix (subagent) — NEW bug surfaced during CSV retry:** `Provision User on Employee Activate` Server Script had underscore-prefixed helper names (`_gen_pwd`, `_slug`, `_email_from`) that RestrictedPython's `safe_exec` rejected. Subagent renamed to `gen_pwd`, `slug`, `email_from` (plus `local_slug` for shadow-avoidance). Saved via `frappe.db.set_value`. `Employee.doc.save()` now works. |
| 2026-09-30 ~23:00 IST | **CSV import SUCCESS** — All 30 rows now have `leave_approver = medicalsuperdinet1194404@harithahospitals.com`. |

**Final state at 23:03 IST:** Full hrms journey closed. `frappe/custom_apps:version-16` running on prod. HRMS baked into image. Server Script sandbox-safe. CSV import working. 8 known Phase D backlog items still open (SMTP, `User.role_profile_name` persistence fix, `Role.module_profile` Custom Field, 2nd Server Script rewrite, 12 small-dept leave_approver fallback, image version drift, DR test, quarterly drills).

---

## 📌 Recent Activity (Oct 1, 2026) — Phase D Backlog: D1 (User Role Profile Migration) + D2 (test.emp Employee Role) RESOLVED

**Audit findings (RBAC verification subagent 2026-10-01 08:43 IST):**
- 219 enabled users, 0 currently assigned to any Haritha Role Profile
- **D1 (CRITICAL):** All 219 users had `role_profile_name = NULL` — RPs + Workspaces existed but unused
- **D2 (HIGH):** `test.emp@harithahospitals.com` had zero roles in `tabHas Role`
- Drift: Custom DocPerm = 379 (handover said 858), Notifications = 16 (handover said 8), Admin-like users = 5 (handover said 3)

**D1 fix applied (2026-10-01 09:26 IST):**
- Snapshot CSV: `/root/.openclaw/workspace/audit/d1-dry-run-snapshot-2026-10-01.csv` (219 rows)
- Backup: `pberpprod_backup_20261001_091507.tar.gz` (5.0 MB, local + offsite verified)
- Mapped 219 users to 6 Haritha Role Profiles via priority cascade (System Manager → HR Manager → HR User → Roster Manager → Leave Approver → Employee default)
- Administrator exception: `Haritha: System Manager` (Option a — preserves Administrator's 46-role `tabHas Role` history)
- All updates via `frappe.db.set_value` (NOT `doc.save()` per Lesson #177)
- 218 of 219 non-Guest users on Haritha RPs; 1 Guest system user has NULL (expected, `user_type='Website User'`)

**D2 fix applied:**
- Granted `Employee` role to `test.emp@harithahospitals.com` via direct `tabHas Role` INSERT
- test.emp now lands on `Haritha: Employee` RP

**Final distribution (218 Haritha users):**

| Haritha Role Profile | Count |
|---|---:|
| Haritha: Employee | 179 |
| Haritha: Leave Approver | 28 |
| Haritha: Roster Manager | 5 |
| Haritha: HR Manager | 3 |
| Haritha: System Manager | 2 (Administrator + test.sm) |
| Haritha: HR User | 1 |

**Verification (9 checks):**
- V1 Distribution: ✓ PASS
- V2 NULL count: 1 (Guest only, expected)
- V3 Non-Haritha count: ✓ 0
- V4 Total on Haritha RPs: ✓ 218
- V5 Administrator: ✓ `Haritha: System Manager`
- V6 test.emp roles: ✓ `['Employee']`
- V7 test.emp RP: ✓ `Haritha: Employee`
- V8 RP coverage: ✓ All 6 RPs ≥1 user
- V9 Test user spot-checks: ✓ All 7 match (Administrator + 6 test users)

**Lessons:**
- Lesson (new, ~#183): Always exclude `name='Guest'` AND `user_type='Website User'` from "no NULL role_profile_name" checks — Guest is a built-in system user with NULL by design.
- Lesson (extended): D1 fix demonstrates `frappe.db.set_value` works reliably for User doc writes (Lesson #177 pattern extended from Server Scripts to User docs).

**Status:** Phase D backlog items D1 + D2 RESOLVED. 6 backlog items remain (SMTP, image version drift, DR drill, regression test, pberpqa update, leave_approver fallback for 10 remaining small depts).

---

## 2026-10-01 (10:21 → 10:32 IST) — Phase D Item 5 (leave_approver) RESOLVED + D3/D4/D5 drift investigated

### Phase D Item 5 — leave_approver cleanup FULLY RESOLVED

**Pre-state (handover claim):** 12 employees on Administrator fallback (HR-EMP-00415/00399 in CSSD, HR-EMP-00242/00275/00305 in Internal Audit, HR-EMP-00234/00324 in OT, HR-EMP-00248 in Finance, HR-EMP-00339 in HR, HR-EMP-00390 in IP Ops, plus 2 in `depts without senior candidates`).

**Actual pre-state (verified 2026-10-01 09:55 IST):** 10 employees on Administrator fallback (handover's 12 was outdated; 2 had been closed by HR since handover).

**Fix applied (10:21 → 10:27 IST):** 10 of 10 employees mapped via `frappe.db.set_value` (Lesson #177 safe_exec pattern):

| Emp ID | Dept | Approver Email |
|---|---|---|
| HR-EMP-00234 | Operation Theatre | srtechnician1052262@harithahospitals.com |
| HR-EMP-00242 | Internal Audit | seniorexecutive1053263@harithahospitals.com |
| HR-EMP-00248 | Finance & Accounts | assistantmanager1026236@harithahospitals.com ⚠️ inverted (closes 3 ghost delegations) |
| HR-EMP-00275 | Internal Audit | seniorexecutive1053263@harithahospitals.com |
| HR-EMP-00305 | Internal Audit | seniorexecutive1053263@harithahospitals.com |
| HR-EMP-00324 | Operation Theatre | srtechnician1052262@harithahospitals.com |
| HR-EMP-00390 | IP Operations | seniorexecutive1042252@harithahospitals.com ⚠️ inverted (closes 3 ghost delegations) |
| HR-EMP-00399 | CSSD | srtechnician1011221@harithahospitals.com |
| HR-EMP-00415 | CSSD | srtechnician1011221@harithahospitals.com |
| HR-EMP-00339 | HR | seniorvicepresident1115325@harithahospitals.com (VP-level, top of hierarchy) |

**Post-state:** **0 employees on Administrator fallback** ✓ — Phase D item 5 FULLY RESOLVED.

**Side benefits:**
- 6 ghost delegations closed (3 each from Finance Mgr + IP Ops Mgr — they were approving leave for 3 others while their own approver was Administrator; now both have a proper superior in their chain)
- All 7 handover-noted dept-head candidates verified (CSSD HR-EMP-00221, Internal Audit HR-EMP-00263, Medical Records HR-EMP-00282, OT HR-EMP-00262 — all active, with User accounts)

### Drift Investigation — D3/D4/D5 (all non-issues)

| Item | Handover | Verified | Verdict | Action |
|---|---|---|---|---|
| D3 Custom DocPerm | 858 | 379 | 858 was design target (33 roles × 26 doctypes grid); 379 is actual scoped count covering all Haritha-critical HRMS surface | Accept + add design-vs-actual note |
| D4 Notifications | 8 | 16 | Handover undercounted: 6 stock framework (Email, 2017-2021) + 8 workflow-generated (auto-created 2026-09-30 10:49:25 when Leave App + Shift Request workflows defined) + 2 disabled | Update handover doc to 16 = 6+8+2 |
| D5 Admin-like users | 3 | 5 | 2 "extras" are false positives: `coordinator*@harithahospitals.com` users have only Employee role + Haritha: Employee profile. Audit filter `LIKE '%coo%'` matched "coordinator" substring | Tighten audit filter; document as Employee-role |

### Session Summary (10:32 IST)

**6 of 10 Phase D backlog items CLOSED in this session:**

| # | Item | Status | Closed |
|---|---|---|---|
| D1 | User RP migration (218 users → Haritha RPs) | ✅ RESOLVED | 09:26 |
| D2 | test.emp Employee role | ✅ RESOLVED | 09:26 |
| D3 (audit) | Role.module_profile CF verify | ✅ verified | 09:00 |
| D4 (audit) | Enforce 90-Day Password Expiry rewrite | ✅ enabled + working | 09:00 |
| D5 | Small dept leave_approver (was 12) | ✅ FULLY RESOLVED | 10:27 |
| D3/D4/D5 (drift) | Custom DocPerm / Notifications / Admin-like | ✅ investigated — non-issues | 10:29 |

**4 Phase D items still OPEN:** SMTP (deferred per Venkat), Image version drift (accepted minor), DR drill (needs dedicated session), 8-phase regression on pberpdev.

**Lessons captured:**
- Lesson #183: Built-in Guest user has `role_profile_name = NULL` by design (`user_type='Website User'`). Always exclude from "no NULL role_profile_name" verification queries.
- Lesson #184: Audit filter for admin-like users should use `role_profile_name LIKE '%System Manager%' OR email LIKE '%@admin%'`, NOT `email LIKE '%coo%'` (matches "coordinator"/"cooper" substrings → false positives).
- Lesson #185: Workflow auto-creates 4 notifications per workflow with 4 states (System Notification channel, Value Change event, `is_standard=0`). Verify workflow count × 4 when investigating notification drift.

---

## 2026-10-01 (08:13 → 20:44 IST) — RBAC Audit + Workspace + Permissions Day

**Theme:** Phase D backlog burn-down (D1/D2/D3/D4/D5) + workspace visibility/content fixes + permission deep-dive + RBAC URL redirect attempt (rolled back).

**Net results:**
- **6 of 10 Phase D backlog items CLOSED:** D1 (User RP migration, 218 users), D2 (test.emp Employee role), D3 (Role.module_profile CF verified), D4 (Enforce 90-Day Password Expiry enabled+working), D5 (leave_approver cleanup 12→10→1→0), Drift D3/D4/D5 (Custom DocPerm 379, Notifications 16, Admin-like 5 — all non-issues)
- **6 Haritha workspaces** made visible (public=1, is_hidden=0, for_user='') + content JSON regenerated with proper `card_name` / `shortcut_name` / `chart_name` references
- **HR Manager content cleanup:** 6 duplicate Link cards collapsed to 1, broken `/app/organizational-chart` URL block removed
- **Round 2 fixes:** HR User / Employee / Leave Approver / Roster Manager workspaces verified + duplicated card cleanup
- **218 User.default_workspace assignments** via `frappe.db.set_value` (role-specific Haritha workspace per user)
- **Page DocPerm fix:** Desk User role now has read=1 on Page (fixes "No permission for Page" on report URLs)
- **Report.roles fix:** Leave Ledger + Monthly Attendance Sheet Report.roles corrected (5 reports total)
- **RBAC redirect attempt (Option A URL redirect + Option C sidebar filter):** ROLLED BACK due to regression (54-min stuck subagent + slug comparison bug); code preserved at `/tmp/rollback_backup/` for retry
- **medicalsuperdinet1194404** workspace routing recovered (had `role_profile_name=NULL` → db.set_value to `Haritha: HR Manager`)

### Phase D backlog status (post 2026-10-01)

| # | Item | Status | Closed |
|---|---|---|---|
| D1 | User RP migration (218 users → Haritha RPs) | ✅ RESOLVED | 09:26 |
| D2 | test.emp Employee role | ✅ RESOLVED | 09:26 |
| D3 (audit) | Role.module_profile CF verify | ✅ RESOLVED (verified) | 09:09 |
| D4 (audit) | Enforce 90-Day Password Expiry rewrite | ✅ RESOLVED (enabled+working) | 09:09 |
| D5 | leave_approver cleanup (was 12) | ✅ FULLY RESOLVED | 10:27 |
| Drift D3/D4/D5 | Custom DocPerm / Notif / Admin-like | ✅ RESOLVED (all non-issues) | 10:29 |
| D6 | SMTP setup | ⏳ OPEN — Venkat deferred | — |
| D7 | Image version drift (Frappe 16.30.0 vs ERPNext 16.31.1) | ⏳ OPEN — accepted minor | — |
| D8 | Quarterly DR drill | ⏳ OPEN — needs dedicated session | — |
| D9 | 8-phase regression test on pberpdev | ⏳ OPEN | — |
| D10 | pberpqa v16 update | ⏳ OPEN | — |

**6 of 10 Phase D backlog items CLOSED in this session.**

### Commits pushed today

| Hash | What |
|---|---|
| `651536f` | D1 + D2 (User RP migration + test.emp Employee role) — morning commit |
| `1211249` | D5 + drift (leave_approver cleanup + D3/D4/D5 drift investigation) — mid-session commit |

### 2026-10-01 Open Issues (for next session)

- 🔴 **HR Manager workspace "Page not found" — bootinfo filter excludes 5 of 6 Haritha workspaces for non-admin users.** Administrator sees all 6 in `bootinfo.workspaces.pages`; HR Manager only sees `Haritha: System Manager`. Workspace IS in `tabWorkspace` with `public=1, is_hidden=0` but bootinfo module/app filter blocks it. **Suggested fix:** `frappe.modules.reload_doc('HR', 'Workspace', 'Haritha: HR Manager')` + clear bootinfo cache, OR investigate why System Manager workspace passes filter but HR Manager (same config) doesn't. 3 test users affected: `assistantgeneralmanager1002212`, `manager1001211`, `nursingsupervisor1045255` see all 6 Haritha in bootinfo but only `System Manager` is callable.
- 🔴 **`medicalsuperdinet1194404` (real HR Manager)** direct URL verification pending — RP fixed but needs browser walkthrough to confirm full RBAC works for real production user (not just test users).
- ⚠️ **Workspace Sidebar DocType missing parent column** — design constraint that limits sidebar hierarchy options.
- ⚠️ **URL redirect hook (Option A)** and **sidebar filter (Option C)** NOT deployed — rolled back due to regression. Code preserved at `/tmp/rollback_backup/` on VPS for next session to retry with safer pattern.
- ⚠️ **rbac_sidebar.py** Python `__pycache__` may still reference deleted module until explicitly cleared.
- ⚠️ **`medicalsuperdinet1194404` had `role_profile_name=NULL`** (the only Haritha user in that state) — fixed via db.set_value but root cause of why this user alone fell out of the cascade is unknown.

### Lessons captured (5 new)

- **Lesson #183:** Built-in Guest user has `role_profile_name = NULL` by design (`user_type='Website User'`). Always exclude from "no NULL role_profile_name" verification queries.
- **Lesson #184:** Audit filter for admin-like users should use `role_profile_name LIKE '%System Manager%' OR email LIKE '%@admin%'`, NOT `email LIKE '%coo%'` (matches "coordinator"/"cooper" substrings → false positives).
- **Lesson #185:** Frappe Workflow auto-spawns 1 notification per state (System Notification channel, Value Change event, `is_standard=0`). Expect N×states workflow notifications.
- **Lesson #186 (NEW):** Frappe v16's `User.on_update` hook reconciles `role_profile_name` field with `User Role Profile` child table. If child table is empty, `doc.save()` SILENTLY NULLs `role_profile_name`. Use `frappe.db.set_value` OR populate child table first. Lesson #177 was right — `doc.save()` is hazardous for User docs in v16.
- **Lesson #187 (NEW):** For RBAC workspace routing, Frappe uses `bootinfo.workspaces.pages` (bootinfo cache) NOT `tabWorkspace` table directly. A workspace can exist in DB with `public=1, is_hidden=0` and still not render if missing from bootinfo pages — typically a caching/module-tag issue, not a permission issue.

---

## Phase Index

> **Consolidated 2026-08-30:** 38 numbered phase files merged into 9 logical phase documents (preserving all content). The numbered filenames referenced in the right-column summaries (e.g. `003+004+005`) point to the original files, which are preserved in git history.

| # | File | Summary |
|---|------|---------|
| 000 | [000-FULL-TRACKER-backup.md](tracker-phases/000-FULL-TRACKER-backup.md) | Full 1492-line backup of the original monolithic TRACKER.md (historical reference) |
| S   | [Status-Wrapups.md](tracker-phases/Status-Wrapups.md) | End-of-day status wrap-ups (2026-08-27) + historical rollback status (2026-08-21) |
| L   | [Decisions-Lessons-Learned.md](tracker-phases/Decisions-Lessons-Learned.md) | Decisions log + Known Issues / Lessons Learned |
| Q   | [Subagent-Questions-Pending.md](tracker-phases/Subagent-Questions-Pending.md) | Subagent log, Open Questions, Pending Actions (Next Session) |
| 0   | [Phase-0-Schema-Planning.md](tracker-phases/Phase-0-Schema-Planning.md) | **Phase 0 → 1.5** — Schema Planning, Approval, CSV Master Re-Verification (003+004+005) |
| 2   | [Phase-2-Site-Setup-Rollback-History.md](tracker-phases/Phase-2-Site-Setup-Rollback-History.md) | **Phase 2** — Site Setup, Restart #2 on prod-env, Pre-flight Backup, all rollback history (006+016+007+008+009+010) |
| 3   | [Phase-3-Data-Import.md](tracker-phases/Phase-3-Data-Import.md) | **Phase 3 → 3.10** — Data Import, Reconcile, Bulk Submit, Property Setter, Attendance Link/Backfill, Backup Bundle Fix (017+018+012+019+021+022+023) |
| 4   | [Phase-4-Shift-Management-Roster-Crash-Fix.md](tracker-phases/Phase-4-Shift-Management-Roster-Crash-Fix.md) | **Phase 4.1 → 4.12** — Shift Type end_time+color, Location backfill, SS submit, SSA create_shifts, Option B 1-SSA-per-employee, Attendance HRMS-recompute, Tailwind color normalization, Roster crash root cause (026+024+025+027+028+029+034+030+033+032+035+031) |
| 0+  | [Phase-0plus-Foundation-Migration.md](tracker-phases/Phase-0plus-Foundation-Migration.md) | **Phase 0+** — Custom app build + Master Data Migration (prod → dev) (036) |
| 3+  | [Phase-3plus-Client-Onboarding-Data-Templates.md](tracker-phases/Phase-3plus-Client-Onboarding-Data-Templates.md) | **Phase 3+** — P5 rebuild: 22 data templates + 3 intake-workbook docs (README + signoff + master validation); 11/11 SCs PASS; tag `v1.0-p5-templates-production-ready` |
| 6   | [Phase-6-Process-Maturity.md](tracker-phases/Phase-6-Process-Maturity.md) | **Phase 6** — Process & Maturity Documentation, 34 docs / ~14,030 lines (037) |
| A   | [Phase-A-Execution.md](tracker-phases/Phase-A-Execution.md) | **Phase A** — RBAC + Workflows + Dashboards + User Provisioning (2026-09-30) |
| B   | [Phase-B-Activation.md](tracker-phases/Phase-B-Activation.md) | **Phase B** — Auto-Attendance Activation (2026-09-30 PM) — config fixes (threshold 2.0, weekly_off=None, backfill +9,309 records) |
| D   | (in-flight tracker file) | **Phase D** — Production Hardening (2026-09-30 PM, SMTP-less per Venkat) — HRMS heartbeat, Module Profile, Server Script rewrite, security audit |
| F   | [HRMS-Module-Fix-Epic.md](tracker-phases/HRMS-Module-Fix-Epic.md) | **HRMS Module Fix** — custom image build with HRMS baked in + Server Script sandbox-safe rewrite (2026-09-30 PM) |
| E   | (in-flight tracker file) | **Phase E** — Handover Package + Phase E+1 Org Chart (2026-09-30 PM) — 5 docs + org chart setup |
| C   | n/a | **Phase C** — Custom App Rename CANCELLED per Venkat "dont rename" instruction (2026-09-30) |

> **Note (Sep 30 PM):** Phase D + Phase E tracker files are in-flight (will be added in a follow-up commit alongside other Phase B/D/E companion docs). Phase C was cancelled per Venkat's instruction and has no tracker file.

## Quick Stats

- Environments: pberpdev, prod-env (pberpqa skipped)
- Active env (2026-09-30 23:03 IST): prod-env.duckdns.org (Phase A + B + D + E closed + HRMS Module Fix closed; Phase C cancelled; custom app pushed to haritha_hospital repo; 32 employees leave_approver updated via CSV import after HRMS module-not-found fix; running on custom image `frappe/custom_apps:version-16` with HRMS baked in)
- See per-phase files for commit counts, customizations captured, and run logs.

## See Also

- [README.md](README.md)
- [docs/](docs/)
- [docs/handbook/README.md](docs/handbook/README.md)
