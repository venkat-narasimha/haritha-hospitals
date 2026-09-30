# Phase A Execution — this hospital

**Date:** 2026-09-30
**Status:** ✅ COMPLETE on prod (`prod-env.duckdns.org`)
**Wall time:** ~3.5 hours (10:07 → 11:55 IST)
**Owner:** Venkat Narasimha

---

## TL;DR

All 10 steps (A.1–A.10) + 6 sub-steps in A.11 complete on prod. Sign-off commit `fdc8c0c` in this repo. Custom app commit `0a423db` in `haritta_hospital` repo (with author fix to `venkat-narasimha <srivenkatnarasimha@gmail.com>`).

## Execution steps

1. **A.1** — Created Roster Manager role (52→53 roles)
2. **A.2** — Confirmed 5 expected roles present (System Mgr, HR Mgr, HR User, Leave Approver, Employee)
3. **A.3** — Created 6 Haritha Role Profiles (System Mgr / HR Mgr / HR User / Roster Mgr / Leave Approver / Employee)
4. **A.4** — Configured Permission Manager (858 perm values across 11 DocTypes × 6 roles)
5. **A.5** — Bulk-populated `leave_approver` on 211/211 Active employees (initial pass; re-run in A.11.5)
6. **A.6** — Created User Permissions (initial pass; re-run in A.11.6)
7. **A.7** — Created 2 Workflows (Leave App 5 states/8 transitions + Shift Request 5 states/9 transitions) + 8 notifications
8. **A.8** — Created 6 Haritha workspaces (SysMgr/HRMgr/HRUser/RosterMgr/LeaveApprover/Employee)
9. **A.11** — User Provisioning Server Script installed + 211/211 Employee Users provisioned + 6 Module Profiles + `leave_approver` re-run (169 dept-head + 42 fallback) + User Permissions re-run (29 new) + Password Policy (min_score=3, no 2FA)
10. **A.9** — 6 test users created (test.sm/hrmgr/hruser/rm/la/emp) + E2E permission checks 6/6 pass
11. **A.10** — Fresh backup (2.6 MB tarball, SHA `56c86341...`) + 3 docs updated + Phase A officially closed

## End state (prod at 2026-09-30 11:55 IST)

- **219 enabled Users** (3 admin + 211 employees + 5 test users)
- **211/211 Active employees** with `user_id` (100%) + `leave_approver` (100%, 27 distinct approvers)
- **53 roles** + **6 Haritha role profiles**
- **2 active workflows** (Leave App + Shift Request) + **16 notifications**
- **6 Haritha workspaces** + **6 module profiles**
- **451 User Permissions** + **11 Roster Manager DocPerms**
- HRMS scheduler firing normally (Fix B from Phase 0 still working)

## Phase D backlog (do NOT block sign-off)

1. **SMTP not configured** (Decision 1)
2. **`User.role_profile_name` persistence issue** (workaround used via `tabHas Role` force-insert)
3. **`Role.module_profile` not a valid Frappe v16 Role field** (need Custom Field)
4. **2 Server Scripts use `from datetime`** (RestrictedPython) — rewrite sandbox-safe before prod traffic
5. **12 small depts `leave_approver` fallback to Administrator** (HR Mgr to manually assign)
6. **Image version drift** `frappe/erpnext:v16.31.1` vs plan baseline `v16.30.0` (confirm intentional)

## Commits made during Phase A

- `0fef62a` — design doc + 13 decisions locked (plan + notes + DECISIONS + design)
- `fdc8c0c` — Phase A sign-off (DECISIONS + plan + design updates)
- `0a423db` — `haritta_hospital` custom app commit (16 A.11 fixtures/scripts, force-pushed with author fix)

## Related documentation

- `docs/handbook/05-process/04-final-production-plan-2026-09-29.md` — final production plan
- `docs/handbook/05-process/05-phase-a-planning-notes-2026-09-29.md` — Phase A planning notes
- `docs/handbook/05-process/06-phase-a-design-2026-09-30.md` — Phase A design (112 KB, 18,388 words, 1,650 lines)
- `docs/DECISIONS.md` — decisions log
- `/root/.openclaw/workspace/memory/2026-09-29.md` — full session recap
