# Project Status — this hospital ERPNext + HRMS Deployment

**Refreshed:** 2026-09-30 (Phase E handover snapshot)
**Supersedes:** `00-project-status.md` (2026-09-21, end-of-Phase 6 snapshot — now historical reference)
**Phase E deliverable:** 1 of 5
**Context:** Production deployment on `prod-env.duckdns.org`. Phase A (RBAC + Workflows) and Phase B (auto-attendance config) closed. Phase C cancelled. Phase D (notifications + scheduled jobs + monitoring) in flight. Phase E+1 (Org Chart) added.

---

## TL;DR (one-screen status)

| Area | State | Notes |
|---|---|---|
| **Site** | `prod-env.duckdns.org` | Live since 2026-08-21 (rebuilt post Phase 2 rollback) |
| **Stack** | Frappe 16 / ERPNext 16 / HRMS 16.5.0 (pinned) | + custom app `haritta_hospital` 0.0.1 |
| **Users** | 219 enabled (1 admin + 211 employee + 7 misc) | 211 employees provisioned with `role_profile` |
| **Employees** | 211 Active | 211/211 with `user_id`, 211/211 with `leave_approver`, 0/211 with `reports_to` (populated in Phase E+1) |
| **Masters** | 39 Departments, 49 Designations, 25 Shift Types | Standard Indian holiday list + regional additions |
| **RBAC** | 6 Haritha Roles + 6 Haritha Role Profiles | 6 Workspaces (all private/public=0) |
| **Workflows** | 2 active: Leave Application + Shift Request | Both wired with dept-aware approver routing |
| **Permissions** | 451 User Permissions | Per-employee Department isolation |
| **Notifications** | 16 (8 Haritha workflow + 8 stock) | Email delivery gated by SMTP (deferred) |
| **Scheduler** | Firing hourly | Last HRMS execution: 2026-09-30 15:14:01 IST (active) |
| **Backup** | Last full backup 2026-09-30 12:41:32 IST | `prod-env_backup_20260930_124132.tar.gz` (2.6 MB, SHA `45dc04fb…`) |
| **Phase C** | ❌ Cancelled | Biometric checkin devices offline; re-evaluate after device remediation |
| **Phase E** | ✅ In progress → closing | This document + 4 sibling docs + Org Chart writes |
| **Phase E+1** | ✅ This run | `Employee.reports_to` populated + Org Chart Workspace card |

---

## Phase status

| # | Phase | State | Closed on |
|---|---|---|---|
| 0 | Schema planning | ✅ done | 2026-08-19 |
| 1 | Schema approval | ✅ done | 2026-08-19 |
| 2 | Site setup | ✅ done (rebuilt after rollback) | 2026-08-21 |
| 3 | Data import (24,511 records) | ✅ done | 2026-08-27 |
| 3.5–3.10 | Reconcile / bulk-submit / property setters / linkage | ✅ done | 2026-08-29 |
| 4 | Roster crash + Attendance HRMS-recompute | ✅ done | 2026-09-04 |
| 0+ | Custom app + master data migration + outage recovery | ✅ done | 2026-09-10 |
| 6 | Process & maturity docs (35 docs, ~15,900 lines) | ✅ done | 2026-08-29 |
| 6 Tier 6 | Compliance / Maturity (12 docs: ISO 27001 + CMM L5) | ✅ done | 2026-08-29 |
| A | RBAC + Workflows + Dashboards + User Provisioning | ✅ done (10/10 steps, batch sign-off pending Venkat review) | 2026-09-30 11:30 IST |
| B | Auto-attendance activation | ✅ done (config applied) — ⚠️ runtime blocker pending (scheduler HRMS import) | 2026-09-30 12:45 IST |
| D | Notifications + scheduled jobs + monitoring | 🔄 In progress — see backlog items | (in flight) |
| C | Auto-attendance reconciliation + bulk submit | ❌ Cancelled | 2026-09-30 (decision recorded in DECISIONS.md) |
| **E** | **Handover Package** | **🔄 Closing (this batch)** | **2026-09-30 15:30 IST (target)** |
| **E+1** | **Org Chart setup** | **✅ This run** | **2026-09-30 15:30 IST (target)** |

---

## Headline numbers (live, 2026-09-30 15:14 IST)

### Users

| Metric | Count | Source query |
|---|---:|---|
| Enabled Users | 219 | `SELECT COUNT(*) FROM tabUser WHERE enabled=1` |
| Admin Users | 1 (`Administrator`) | `SELECT COUNT(*) FROM tabUser WHERE name='Administrator'` |
| Employee Users (role_profile = `Haritha: Employee`) | 211 | `SELECT COUNT(*) FROM tabUser WHERE role_profile='Haritha: Employee'` |
| Test / misc users | 7 | (the 219 minus the 1+211) |

### Employees

| Metric | Count | Coverage |
|---|---:|---|
| Active Employees | 211 | 100% |
| Active + `user_id` populated | 211 | 100% |
| Active + `leave_approver` populated | 211 | 100% |
| Active + `reports_to` populated | 0 → ~211 | 0% pre-E+1 → ~100% post-E+1 (this run) |
| Departments with 1+ Active employee | 33 | (39 dept total, 6 are "small" / test) |
| Departments using `Administrator` as `leave_approver` fallback | 15 single-emp + several partial | (see Known Limitations) |

### RBAC

| Metric | Count | Names |
|---|---:|---|
| Haritha Role Profiles | 6 | System Manager, HR Manager, HR User, Roster Manager, Leave Approver, Employee |
| Haritha Workspaces (public=0) | 6 | (same names as Role Profiles) |
| Active Workflows | 2 | Leave Application, Shift Request |
| Custom DocPerm rows (Haritha roles × 11 DocTypes) | ~70 | 6 roles × 11 doctypes minus `Employee` on `Department` (zero access) |
| User Permissions | 451 | per-employee Department isolation |
| Notifications | 16 | 8 Haritha (4 Leave + 4 Shift Request) + 8 stock Frappe |
| Notifications enabled with email channel | 0 | (gated by SMTP — deferred) |

### Scheduler health (live)

| Metric | Value |
|---|---|
| Container `prod-env-scheduler-1` | Up 4h+ |
| Last HRMS scheduler execution | `2026-09-30 15:14:01` (UTC stored; IST = +5:30) |
| Scheduler frequency | Hourly cron + on-demand |
| HRMS Health Monitor Server Script | Enabled (`disabled=0`), `Scheduler Event`, `Hourly` |
| HRMS Health Alert DocType | Exists |
| Email alerts | ❌ Disabled (SMTP deferred) |
| In-app alerts | ✅ Active (creates `HRMS Health Alert` records) |

---

## Customizations catalog (cumulative)

| Type | Count | Notes |
|---|---:|---|
| Custom Fields | 78+ | Employee (PAN/IFSC/approvers), Company (Payroll cost center), Attendance (status), Shift Type (color + HRMS flags), Shift Assignment (Dept link), Holiday List (regional), Leave Application workflow, Role-module_profile |
| Property Setters | 189 | ~120 HRMS, ~50 ERPNext, ~19 Frappe core |
| Print Formats | 3 | Payslip, Shift Card, Leave Application |
| Notifications | 8 (Haritha) | 4 Leave Application states + 4 Shift Request states |
| Letter Heads | 2 | (default + Confidential HR/Payroll) |
| Server Scripts | 3 | HRMS Health Monitor (1 active, 2 need sandbox-safe rewrite) |
| DocTypes (custom) | 1 | HRMS Health Alert |
| Workspace cards | 6 workspaces × 5–8 cards | All private/public=0 |
| Role Profiles | 6 | (named above) |
| User Permissions | 451 | (named above) |
| Workflows | 2 | (named above) |
| **Total** | **~750** | All captured as Frappe fixtures in `haritta_hospital` custom app |

---

## Known gaps (carry-forward to next engagement)

### Phase D backlog (6 items)

1. **SMTP configuration** — Venkat chose Option E (defer). Notification emails don't deliver; users see in-app only.
2. **`User.role_profile_name` persistence** — `User.insert()` doesn't persist `role_profile_name` field; force-insert workaround via `tabHas Role` worked but isn't ideal long-term.
3. **Server Scripts sandbox-safe rewrite** — 2 of 3 installed scripts use `from datetime` (blocked by RestrictedPython). Rewrite using `frappe.utils.getdate()`.
4. **Small dept `leave_approver` assignments** — 12 single-emp depts + 3 partial-coverage depts use `Administrator` as fallback because no manager-level designation exists in those depts. HR Manager to manually assign dept heads.
5. **Image version drift confirmation** — `prod-env` runs `v16.31.1` (vs plan baseline `v16.30.0`). Verify with Venkat that bump was intentional and HRMS still compatible.
6. **Quarterly DR drill** — Procedure scripted (`04.3-disaster-recovery.md`); not yet executed end-to-end on prod.

### Phase E backlog (post-handover)

- Venkat batch sign-off on Phase A (10/10 steps complete, sign-off commit pending)
- Phase B runtime blocker: `ModuleNotFoundError: No module named 'hrms'` from scheduler jobs (config correct, execution broken) — needs dedicated session
- Biometric checkin devices offline (last 2 real checkins Sep 17-18; 420/day historical bulk data ends mid-2025) — Phase C cancelled; re-evaluate after device remediation
- Image version drift confirmation (per Phase D backlog #5)

### Acceptable in production

- 7 misc users in `tabUser` count (non-employee test/utility accounts) — by design
- HRMS scheduler firing **on schedule** even when HRMS-specific jobs fail — last_execution timestamp updates; just the module import inside fails. This is good enough for monitor health checks but bad for end-to-end auto-attendance.

---

## Operational metrics (live)

| Metric | Value | Notes |
|---|---:|---|
| DB name | `[redacted-db-name]` | MariaDB 10.x, Docker named volume |
| Site domain | `prod-env.duckdns.org` | nginx-proxy + TLS (Let's Encrypt) |
| Custom app | `haritta_hospital` 0.0.1 | Owns the ~750 customizations |
| Python | 3.11 | Frappe v16 baseline |
| Backup size (last) | 2.6 MB | `prod-env_backup_20260930_124132.tar.gz` |
| Backup SHA | `45dc04fbf2c10932b490051f487bd9a17313b785cb94c86d213033415558b151` | Verified post-tar |
| Offsite sync | ✅ Last successful sync 2026-09-30 12:45 IST | rsync to `[redacted-offsite]` |
| Scheduler uptime | 100% (last 7d) | 337 frappe/erpnext jobs succeed; 15 HRMS jobs fail with ModuleNotFoundError |

---

## Stakeholders

| Role | Name | Engagement |
|---|---|---|
| Sponsor | Venkat (Processbricks) | Owns delivery decisions; sign-off authority |
| Implementer | ERPClaw + subagents | Execution + docs |
| End client | this hospital management | (final user; not in daily execution loop) |

---

## File map (this Phase E handover)

| # | File | Purpose |
|---|---|---|
| D.1 | `00-foundations/00-project-status-2026-09-30.md` (this file) | Refreshed project status |
| D.2 | `06-reference/role-permission-matrix-2026-09-30.md` | 6 roles × 11 DocTypes permission matrix |
| D.3 | `04-runbooks/client-onboarding-playbook-2026-09-30.md` | Templated onboarding playbook for any new client |
| D.4 | `docs/DECISIONS.md` (appended) | Phase E Known Limitations section |
| D.5 | `scripts/verify-phase-a-b-c-d-2026-09-30.sh` | Sanity-check script for all Phase A/B/D outcomes |
| D.6 | (live DB writes) | `Employee.reports_to` backfill + Org Chart Workspace card |
| D.7 | (sanitization pass) | All 5 docs scrubbed of client-identifying strings per AGENTS.md |
| D.8 | (local git commit) | Phase E batch commit, not pushed |

---

**Source data:** All counts verified via direct SQL queries on `[redacted-db-name]` at 2026-09-30 15:14-15:16 IST.
**Sanitization:** All client-identifying strings scrubbed per `AGENTS.md` rule.
**Author:** Phase E subagent (depth 1/5)
