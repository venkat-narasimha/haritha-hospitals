# Haritha Hospitals — RBAC + Workflow Report

**Date:** 2026-10-02
**Site:** pberpprod.duckdns.org
**Database:** `_b80f05e76a0dcaad`
**Status:** Post-Phase A + Phase D hardening (D1-D5 closed; D6-D10 open)

---

## 1. Roles (Haritha Custom + standard HRMS)

### 1.1 Haritha Custom Roles — Active user count per role

| Role | Active Users |
|---|---|
| `Haritha: System Manager` | 2 (Administrator + test.sm) |
| `Haritha: HR Manager` | 3 |
| `Haritha: HR User` | 1 |
| `Haritha: Roster Manager` | 5 |
| `Haritha: Leave Approver` | 28 |
| `Haritha: Employee` | 179 |
| **Total via Haritha Roles** | **218** |

### 1.2 Standard HRMS / Frappe Roles in use

| Role | Active Users |
|---|---|
| `Employee` | (used by Haritha: Employee) |
| `Leave Approver` | (used by Haritha: Leave Approver) |
| `Roster Manager` | (used by Haritha: Roster Manager) |
| `HR Manager` | (used by Haritha: HR Manager) |
| `HR User` | (used by Haritha: HR User) |
| `System Manager` | (used by Haritha: System Manager) |
| `Desk User` | (likely assigned to all users) |

> Note: Haritha custom roles are layered on top of standard roles. Total active users: 218-219.

---

## 2. Role Profiles

### 2.1 Active users per Role Profile

| Role Profile | Active Users |
|---|---|
| `Haritha: System Manager` | 2 |
| `Haritha: HR Manager` | 3 |
| `Haritha: HR User` | 1 |
| `Haritha: Roster Manager` | 5 |
| `Haritha: Leave Approver` | 28 |
| `Haritha: Employee` | 179 |
| **Total via Role Profile** | **218** |

> All 218 active Haritha users are assigned a role profile. The remaining users (1-2) are either Administrator without a profile or guest/inactive.

---

## 3. User Permissions (`tabUser Permission`)

- **Total User Permission records:** 451
- These enforce department-level + leave-approver + shift-approver + custom DocType access scoping
- Sample entries (latest 10):

| User | DocType Allowed | Value | Applicable For |
|---|---|---|---|
| (various users) | (various DocTypes) | (department / role / user values) | (Link/Department) |

> Specific user-permission details vary per user; the system is enforcing department isolation + approver scoping for all 218 active users.

---

## 4. Custom DocPerms (DocType-level RBAC overrides)

- **Total Custom DocPerm rows:** small set (added during Phase A + D1)
- Includes the Page DocPerm (Desk User · read=1) added during the workspace visibility fix

### Known Custom DocPerms applied during Phase A/D:

| DocType | Role | read | write | create | delete | submit | cancel | amend |
|---|---|---|---|---|---|---|---|---|
| `Page` | `Desk User` | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

> Other Custom DocPerms follow Frappe HRMS stock patterns for Employee, Leave Application, Shift Request, Attendance, etc., customized via the role profiles.

---

## 5. Workflows (`tabWorkflow` DocType)

**Total Workflow DocType records:** 2

### 5.1 Workflow: Shift Request

- **DocType:** `Shift Request`
- **Active:** Yes
- **Send email on transition:** Yes
- **Purpose:** Approve shift swap/change requests

**States:**

| State | doc_status | allow_edit |
|---|---|---|
| `Draft` | 0 | 1 |
| `Pending` | 1 | 0 |
| `Approved` | 1 | 0 |
| `Rejected` | 1 | 0 |

**Transitions:**

| Action | From State | To State | Allowed |
|---|---|---|---|
| `Submit` | Draft | Pending | Haritha: Employee, Haritha: Roster Manager, Haritha: Leave Approver, Haritha: HR User, Haritha: HR Manager, Haritha: System Manager, System Manager, HR Manager, HR User, Roster Manager, Leave Approver, Employee, Desk User |
| `Approve` | Pending | Approved | (configured approvers) |
| `Approve (HR)` | Pending | Approved | (HR Manager override) |
| `Reject` | Pending | Rejected | (configured approvers) |
| `Reject (HR)` | Pending | Rejected | (HR Manager override) |

> **Recent fix (2026-10-02):** Custom `before_save` server hook in `harita_hospital.workflow_sync` bridges the gap where HRMS's `on_submit` validates `status in [Approved, Rejected]` but the workflow action didn't pre-set the Status field. The hook now mirrors `workflow_state` → `status` before save. Also added Property Setters making `status` field read-only in form (admin can still override via API).

### 5.2 Workflow: Leave Application

- **DocType:** `Leave Application`
- **Active:** Yes
- **Send email on transition:** Yes
- **Purpose:** Approve leave requests

**States:**

| State | doc_status | allow_edit |
|---|---|---|
| `Draft` | 0 | 1 |
| `Pending` | 1 | 0 |
| `Approved` | 1 | 0 |
| `Rejected` | 1 | 0 |

**Transitions:**

| Action | From State | To State | Allowed |
|---|---|---|---|
| `Submit` | Draft | Pending | (employees) |
| `Approve` | Pending | Approved | (managers) |
| `Reject` | Pending | Rejected | (managers) |

> Same `harita_hospital.workflow_sync` hook applies — Leave Application also benefits from the workflow_state → status sync.

---

## 6. Workspaces (Haritha Custom + Per-User)

| Workspace | Title | Module | App | Public? | Hidden? | For User |
|---|---|---|---|---|---|---|
| `Haritha: System Manager` | Haritha: System Manager | Core | frappe | ✓ | | (public) |
| `Haritha: HR Manager` | Haritha: HR Manager | HR | hrms | ✓ | | (public) |
| `Haritha: HR User` | Haritha: HR User | HR | hrms | ✓ | | (public) |
| `Haritha: Roster Manager` | Haritha: Roster Manager | HR | hrms | ✓ | | (public) |
| `Haritha: Leave Approver` | Haritha: Leave Approver | HR | hrms | ✓ | | (public) |
| `Haritha: Employee` | Haritha: Employee | HR | hrms | ✓ | | (public) |

> All 6 Haritha custom workspaces are public (visible to all users) with `for_user=''` and `is_hidden=0`. The Home button routes to user's default_workspace (set in `User.default_workspace` per role-profile provisioning).

---

## 7. Module Profiles (DocType-level module restrictions)

| Module Profile | Active Users |
|---|---|
| `Haritha: Employee Modules` | 211 |
| `Haritha: System Manager Modules` | (low — admin only) |
| `Haritha: Leave Approver Modules` | (low — dept heads) |
| `Haritha: HR Manager Modules` | (low — HR managers) |
| `Haritha: HR User Modules` | (low — HR users) |
| `Haritha: Roster Manager Modules` | (low — nursing supervisors) |

> Total ~211 employees blocked from HR module access (D1 fix: deleted per-user `tabBlock Module` rows). Other role profiles grant the corresponding module access.

---

## 8. User Distribution Summary

**Total enabled users:** 218 (during Phase D audit) → 219 (post-test-user addition)

### Distribution by Role Profile

| Role Profile | Active Users |
|---|---|
| `Haritha: System Manager` | 2 |
| `Haritha: HR Manager` | 3 |
| `Haritha: HR User` | 1 |
| `Haritha: Roster Manager` | 5 |
| `Haritha: Leave Approver` | 28 |
| `Haritha: Employee` | 179 |
| **TOTAL** | **218** |

---

## 9. Role Profile → Role Mapping (which Roles each Profile grants)

### 9.1 `Haritha: System Manager` → 2 role(s)
- `Haritha: System Manager`

### 9.2 `Haritha: HR Manager` → 1 role(s)
- `Haritha: HR Manager`

### 9.3 `Haritha: HR User` → 1 role(s)
- `Haritha: HR User`

### 9.4 `Haritha: Roster Manager` → 1 role(s)
- `Haritha: Roster Manager`

### 9.5 `Haritha: Leave Approver` → 2 role(s)
- `Haritha: Leave Approver`
- `Leave Approver`

### 9.6 `Haritha: Employee` → 2 role(s)
- `Haritha: Employee`
- `Employee`

> Each Haritha role profile grants the matching Haritha custom role, plus in some cases the equivalent standard HRMS role (e.g., `Haritha: Employee` also grants `Employee`).

---

## Summary

| Category | Count |
|---|---|
| Total active Haritha users | 218 |
| Haritha custom role profiles | 6 |
| Haritha custom workspaces | 6 (all public) |
| Module profiles | 6 (211 users blocked from HR via `Haritha: Employee Modules`) |
| Workflow DocType records | 2 (Shift Request, Leave Application) |
| User Permission records | 451 |
| Custom DocPerms (custom additions) | 1 (Page · Desk User · read=1) |
| Workflow state transitions | Submit / Approve / Approve (HR) / Reject / Reject (HR) |
| Recent fix (2026-10-02) | `harita_hospital.workflow_sync` hook syncs workflow_state → status before save |

---

## Recent RBAC + Workflow changes (Phase A through 2026-10-02)

| Date | Change |
|---|---|
| 2026-09-30 (Phase A) | Created 6 Haritha role profiles + 6 Haritha workspaces + 2 workflows + 5 dashboard charts + 3 number cards + Server Script provisioning (211 users) |
| 2026-09-30 (Phase A.11) | Server Script auto-creates User + Role Profile for 211 employees |
| 2026-10-01 (D1 fix) | Migrated 218 users to Haritha role profiles; Administrator exception → Haritha: System Manager; 0 leave_approver fallbacks to Administrator |
| 2026-10-01 (bootinfo fix) | Deleted 211 per-user `tabBlock Module` rows for `HR` module (was blocking bootinfo; now role profiles grant HR access) |
| 2026-10-01 (test users) | `medicalsuperdinet1194404` role_profile fixed (was NULL) |
| 2026-10-01 (Page DocPerm) | Added Custom DocPerm: `Page` · `Desk User` · read=1 (fixes "No permission for Page" on report URLs) |
| 2026-10-02 (workflow sync) | Added `harita_hospital.workflow_sync.sync_workflow_state_to_status` (before_save hook) + hooks.py doc_events registration; Property Setters make `status` read-only on Shift Request + Leave Application forms |
| 2026-10-02 (Approvers) | Set `Employee.shift_request_approver = medicalsuperdinet1194404` for HR-EMP-00212 (Assistant General Manager-1002) — for cross-user workflow testing |

---

## Open items / Pending

- Module Profile per-user population is incomplete (e.g., `Haritha: HR Manager Modules` has 0 active users even though 3 users have `Haritha: HR Manager` role profile) — to verify whether role profile grants module access via Has Role → role → module mapping, or if Module Profile assignment is separate
- Page DocPerm coverage is minimal (only Desk User · read=1) — other role-level Page permissions are inherited from stock ERPNext/HRMS
- Custom DocPerm count appears low; most permission overrides happen via role profiles rather than Custom DocPerm
- Workflow Sender (email) configuration uses system default — not customized per Haritha

---

_Document generated 2026-10-02 (Haritha Hospitals deployment, Frappe v16 + ERPNext v16 + HRMS v16.5.0)._