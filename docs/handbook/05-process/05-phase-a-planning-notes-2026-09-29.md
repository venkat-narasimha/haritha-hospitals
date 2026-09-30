# Phase A Planning Notes

**Captured:** 2026-09-29 23:08 IST  
**Project:** this hospital + reusable foundation  
**Trigger:** Venkat's directive to remember 3 Phase A requirements

---

## Venkat's 3 Phase A Requirements (verbatim)

1. **Plan roles, permissions, workflows accordingly** — detailed planning (not just outline), done at start of Phase A before any change.
2. **User dashboard for every role** with their respective permissions and access. 6 roles → 6 dashboards.
3. **Based on the designations we have, we derive the roles and permissions and access.** Observe the data, assign per best practices + org structure.

---

## Where this context lives

| Artifact | Path |
|---|---|
| Plan doc §5 Phase A (expanded with the 3 requirements) | `/root/.openclaw/workspace/FINAL-PRODUCTION-PLAN-2026-09-29.md` |
| Plan doc §4 Role × Permission Matrix (outline) | same file |
| Plan doc §9 Pre-Execution Findings (live baseline) | same file |
| Live verification report | subagent run `debbeee7-5a6b-4109-9663-578c65028173` |
| Audit (partially stale — 26 shift types, 14 holidays, etc.) | `projects/haritha-hospitals/docs/handbook/05-process/03-project-go-live-audit-2026-09-29.md` |

---

## Designation → Role starting mapping (Phase A.0 will refine)

This is the **starting point** for R3. Phase A.0 must pull all 49 Designations + 39 Departments from prod and cluster them into role-candidates.

| Existing designation cluster | → Target role | Role exists? |
|---|---|---|
| HR Head, HR Manager | → HR Manager | ✅ exists |
| Nursing Supervisor, Roster Planner, Ward In-Charge | → Roster Manager | ❌ must CREATE |
| Department Head, In-Charge, Senior Doctor | → Leave Approver | ✅ exists |
| Doctor, Nurse, Technician, Pharmacist, Lab Tech, Support Staff | → Employee (self-service) | ✅ exists |
| System Admin, Technical, IT | → System Manager | ✅ exists |
| HR Executive, HR User, HR Assistant | → HR User | ✅ exists |

**Cluster edge cases** (to resolve in Phase A.0):
- What about "Senior Doctor" — does it become Leave Approver for their unit, or Employee (and a separate designation acts as approver)?
- What about "Administrator" or "Owner" designation — what role?
- What about employees with no designation (212 employees — are all assigned?).

---

## Per-role dashboard sketch (R2)

| Role | Workspace name | Key cards / visibility |
|---|---|---|
| System Manager | Full Desk (default) | All modules, all reports, all workspaces |
| HR Manager | HR Workspace | Employee census, leave summary, attendance summary, open workflows, payroll-readiness (out of scope but visible) |
| HR User | HR-User Workspace | Limited per Role Permission Manager; HR module only |
| Roster Manager | Roster Workspace | Today's roster, this week's roster, attendance summary per shift, pending shift requests |
| Leave Approver | Leave-Approver Workspace | Pending approvals queue, team leave calendar, attendance-vs-leave summary |
| Employee | Employee Workspace | My profile, my attendance, my leave balance, my shifts, my requests |

**Implementation notes:**
- Each Workspace is a DocType in Frappe (`tabWorkspace`) with module visibility + cards.
- Dashboards are Frappe Dashboard DocType with charts sourced from reports.
- Module visibility per role configured via Role Permission Manager (not Workspace — Workspace handles cards but module sidebar visibility is per-role).
- For role-based module sidebar: edit "Show/Hide Cards" + module visibility per role in `tabUser` + `tabRole`.

---

## Phase A gate

**Phase 0 (Pre-Flight Diagnostics) must run first** — HRMS scheduler silently broken (32+ days stale), audit is stale relative to live prod (shift types 25→26, auto-attendance flipped, etc.). Phase A cannot begin until Phase 0 exit criteria are met.

---

## When Phase A starts

Read this file + the plan doc §5 Phase A + §9 baseline. Then design:

1. Detailed Role Permission Manager entries (perm levels per role × DocType × perm type)
2. Role Profile bundles
3. User Permission rules (department → user mapping, dept-isolation rules)
4. Workflow state machines (Leave App + Shift Request: states, transitions, approver routing)
5. Workspace definitions + module visibility per role
6. Dashboard cards + chart sources

**Gate before execution:** All 6 above must be reviewed + signed off by Venkat before any Role/Permission/Workflow change is pushed.

---

## Venkat Decisions Locked (2026-09-30 09:38 IST)

All 13 Phase A design decisions are locked. The detailed design doc is at `docs/handbook/05-process/06-phase-a-design-2026-09-30.md`.

| # | Decision | Value |
|---|---|---|
| 1 | SMTP | Defer to Phase D (option c) |
| 2 | COO role | System Manager |
| 3 | Manager / GM cluster | Default Employee + per-dept overrides |
| 4 | Roster Manager count | 4 (3 Nursing Supervisors + 1 Nursing Superintendent) |
| 5 | HR Mgr / HR User boundary | 1 HR Manager + 2 HR Users |
| 6 | Branches | Add now |
| 7 | 2FA | None |
| 8 | Password policy | Adopt as-is (min 12, score 3, 90-day expiry, history 5) |
| 9 | Notifications | tabNotification, System channel initially, Email in Phase D |
| 10 | testuser role | Employee |
| 11 | Leave Approver routing | via Employee.leave_approver field |
| 12 | Workflow approver routing | Leave App: leave_approver; Shift Request: dept's Roster Manager (fallback HR Manager) |
| 13 | Cross-functional Sr Manager | approve only own dept |

**Architectural decisions status:** All 3 architectural decisions (A: Branches — Add now; B: 2FA — None; C: Password policy — Adopt as-is) have been resolved.

**Execution impact:** Decision 6 (Branches) brings Branch DocType + Employee.branch Custom Field + 3D User Permissions into scope. Revised Phase A total: ~7-8h wall time (was 5.5h).