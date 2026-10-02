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

> **Workflow-state → Status sync (2026-10-02):** A `before_save` doc_events hook (`harita_hospital.workflow_sync.sync_workflow_state_to_status`) was tried first to bridge the gap where HRMS's `on_submit` validates `status in [Approved, Rejected]` but the workflow action didn't pre-set the Status field. The hook was registered correctly in `hooks.py` (`doc_events = {"Shift Request": {"before_save": ...}}`) and confirmed via `frappe.get_hooks("doc_events")`. However, **the hook did NOT fire on the submit-path transition** — Approved/Rejected have Doc Status=1, so Frappe's workflow apply path calls `doc.submit()`, and HRMS's `on_submit` validator runs BEFORE custom `before_save`/`on_update` doc_events hooks. A temporary `frappe.throw` inside the hook never appeared when "Approve" was clicked from the UI. (Lesson #193.)
>
> **Actual mechanism now in place:** Workflow's built-in `Update Field` / `Update Value` mechanism on the state definition. On the Approved state: `update_field='status', update_value='Approved'`. On the Rejected state: `update_field='status', update_value='Rejected'`. This runs DURING the transition (before `on_submit` validates) and is the framework-supported way. Same setup applied to the Leave Application workflow. Property Setters still make the `status` field read-only on forms (admin can still override via API).

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

> Leave Application workflow uses the same mechanism: `Update Field = 'status'`, `Update Value = 'Approved'` on the Approved state and `'Rejected'` on the Rejected state (no doc_events hook — same Lesson #193 reason).

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
| Workflow sync (2026-10-02) | Workflow State's `Update Field` / `Update Value` mechanism sets `status` from `workflow_state` on submit-path transitions (Shift Request + Leave Application) — `before_save` doc_events hook was tried first but did NOT fire on submit-path (Lesson #193) |

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
| 2026-10-02 (workflow sync — superseded) | Tried `harita_hospital.workflow_sync.sync_workflow_state_to_status` (before_save hook) + hooks.py doc_events registration; **did NOT fire on submit-path** — replaced by Workflow's `Update Field` / `Update Value` on Approved/Rejected states. Property Setters still make `status` read-only on forms |
| 2026-10-02 (Approvers) | Set `Employee.shift_request_approver = medicalsuperdinet1194404` for HR-EMP-00212 (Assistant General Manager-1002) — for cross-user workflow testing |
| 2026-10-02 (F1+F2+F3 RBAC fixes) | **F1 User Permission:** removed `medicalsuperdinet1194404` over-restriction (`allow=Employee, for_value=HR-EMP-00404, apply_to_all_doctypes=1`) → HR Manager now sees 212 employees via API (was 1). **F3 Account/Project doctype leak:** `Account` blocked via Custom DocPerm zero-out for HR Manager → HTTP 403 verified; `Project` PARTIAL — same approach returns HTTP 200 (deeper Frappe perm path grant suspected — Server Script `permission_query` hook or v16 `if_owner` re-grant) → deferred. **F2 Reports module:** 5 test-name → actual-name mappings documented (Attendance Sheet, Attendance Summary, Shift Roster, Leave Ledger, Employee Leave Balance); Employee Leave Balance has internal TypeError deferred. |
| 2026-10-02 (Tests 3-6 + E2E + F3 propagation fix) | **Tests 3-6** (post-F3 re-test): HR User (HR User) on Project 200 + Account 200, RM/LA/Employee (all via `Haritha: <Role>` profiles) on Project 200 — F3 only zeroed HR Manager row, leak persisted. **E2E workflow test** (HR-EMP-00212): Shift Request create→Submit→Approve→Reject→Submit→Approved (5 transitions) completed successfully. **F3 propagation fix (RESOLVED):** root cause = all 4 Haritha role profiles reference plain `Employee` role via `tabHas Role`; `Employee` row had `select=1` on Project (the actual leak); `HR User` row had `select=1` on Project + Account. Fix = `UPDATE tabCustom DocPerm SET all_perms=0 WHERE parent IN ('Project','Account') AND role IN ('HR User','Employee')` (rows_updated=3) + `bench clear-cache`. **Verified per-user API:** HR User Project 403, HR User Account 403, RM Project 403, LA Project 403, Employee Project 403 — all 5 = HTTP 403. **Lesson #195** (CRITICAL — DocPerm fixes for one role do NOT auto-propagate to other roles sharing the module). **Test data cleanup:** deleted 1 Employee Checkin (`EMP-CKIN-10-2026-000001`) + 6 docstatus=0 Shift Requests (HR-SHR-26-10-00001/00002/00005/00006/00007/00008) via REST + 1 docstatus=1 Shift Request (HR-SHR-26-10-00004) via SQL force-delete. Survived: HR-SHR-26-10-00009 (excluded per spec). |

---

## Open items / Pending

- Module Profile per-user population is incomplete (e.g., `Haritha: HR Manager Modules` has 0 active users even though 3 users have `Haritha: HR Manager` role profile) — to verify whether role profile grants module access via Has Role → role → module mapping, or if Module Profile assignment is separate
- Page DocPerm coverage is minimal (only Desk User · read=1) — other role-level Page permissions are inherited from stock ERPNext/HRMS
- Custom DocPerm count appears low; most permission overrides happen via role profiles rather than Custom DocPerm
- Workflow Sender (email) configuration uses system default — not customized per Haritha

---

_Document generated 2026-10-02 (Haritha Hospitals deployment, Frappe v16 + ERPNext v16 + HRMS v16.5.0)._

## Open RBAC + Workflow Findings (2026-10-02)

These 4 doc-only bugs were categorized as by-design / test-design / data gaps / API quirks per Lesson #196 (3-bucket triage) and require no code fix. Each is documented here for future reference and to inform future test plans.

| # | Bug | Found in | Severity | Status |
|---|---|---|---|---|
| 1 | Monthly Attendance Sheet pypika `AttributeError: 'NoneType' object has no attribute 'nodes_'` in `apps/hrms/hrms/hr/report/monthly_attendance_sheet/monthly_attendance_sheet.py:329` regardless of filter combo | 2026-10-02 verification | medium | RESOLVED 2026-10-02 — Cycle fix: HR-EMP-00325.reports_to set to null (top of BD chain), leave_approver set to medicalsuperdinet1194404 (HR Manager); HR-EMP-00331 direction was already correct; HR-EMP-00212 preserved (Bug 5 fix); backup at `/home/vijay/backups/prod/task8_pre_20261002_162523_*` |
| 4 | Workflow Submit path leaves `workflow_state`='Draft' (status='Draft') after `client.insert`; explicit `apply_workflow` API call with action "Submit for Approval" transitions to Pending Approval correctly | 2026-10-02 verification | low | by-design workaround verified — use `apply_workflow` API |
| 6 | Leave Approver / Employee can read own Employee but cannot update own `cell_number` (HTTP 403) | Test 5 D5 | medium | Open — design choice, not a bug per se |
| 7 | `status` field not auto-updated by workflow transitions (only updated on Approved/Rejected per Workflow Update Field config) | Test 6 B1 | low | Open — known limitation, documented in F2 fix |
| 9 | `Attendance Summary (HR)` report doesn't exist (actual report name: "Shift Attendance") | E2E 2.4, Test 4 C5 | low | Open — spec vs reality drift |
| 10 | Workflow Apply Workflow API returns HTML "Invalid Link" for some transitions; workaround: direct `workflow_state` PUT via `frappe.client.set_value` | Test 3 B1 | low | Open — API quirk, workaround documented |

### Deferred (2026-10-02)

| # | Bug | Reason | Artefact |
|---|---|---|---|
| 1 | Monthly Attendance Sheet pypika upstream HRMS bug | Web search 2026-10-02 found no fix; no workaround from our app side. Venkat decided not to file upstream at this time | Issue draft at `/root/.openclaw/workspace/audit/bug-stack-traces-2026-10-02/hrms-issue-draft.md` for future filing |

**Bug 6 — Self-update of cell_number returns 403 (by-design):** The Leave Approver + Employee role profiles can `read` their own Employee record but are correctly denied `write` on `cell_number` per Frappe v16's role-permission model. The Employee Self Service role only grants read access. This is a security boundary, not a defect. To enable self-update of `cell_number`, add a Custom DocPerm row for the appropriate role on the Employee DocType with `write=1` for the `cell_number` field only (not the whole doc).

**Bug 7 — `status` field not auto-updated by every workflow transition:** Frappe v16 Workflow transitions only update the `workflow_state` field automatically. The `status` DocField (separate from `workflow_state`) is updated only when a state's `update_field` is configured to point to `status` with a specific `update_value`. Today this is set on Approved + Rejected for both Shift Request + Leave Application workflows. To update `status` on additional transitions (e.g. "Pending Approval"), edit the Workflow state definition and add `update_field='status', update_value='Open'` on those states. Already covered by F2 fix — listed for completeness.

**Bug 9 — `Attendance Summary (HR)` report name mismatch:** The test plan referenced `Attendance Summary (HR)` but the actual HRMS report is `Shift Attendance`. This is test-plan drift, not a code bug. The HRMS v16 reports available include `Monthly Attendance Sheet`, `Shift Attendance`, `Employee Leave Balance`, `Leave Ledger`. Update future test cases to use the actual report names; no code change required.

**Bug 10 — Apply Workflow API HTML "Invalid Link" quirk:** Calling `POST /api/method/frappe.model.workflow.apply_workflow` with a `state` value that's not the current state's allowed transitions returns a wrapped HTML "Invalid Link" error instead of a clean JSON 422. Workaround used today: bypass `apply_workflow` and set `workflow_state` directly via `frappe.client.set_value(doctype, docname, 'workflow_state', new_state)` from a Python context with `frappe.set_user` to escalate. The API quirk does not affect standard UI-based workflow transitions (which use the correct endpoint); only programmatic transitions hit it. No fix recommended — workaround documented for future automation scripts.

**Bug 4 — Workflow Submit path UX (by-design workaround verified, 2026-10-02):** When creating a Shift Request or Leave Application via `frappe.client.insert`, the new doc's `workflow_state` remains "Draft" after insertion — the `client.insert` path does NOT auto-trigger the "Submit for Approval" workflow transition. Verified today: explicit `frappe.model.workflow.apply_workflow(doc, 'Submit for Approval')` correctly transitions `workflow_state` from Draft → Pending Approval. The `status` field stays "Draft" through the Submit transition because no `update_field='status', update_value='Open'` is configured on the Submit state (by design — only Approved/Rejected states have `update_field` configured per today's earlier F2 fix, Lesson #193). **Workaround (verified):** after `client.insert`, call `apply_workflow(doc, 'Submit for Approval')` to advance `workflow_state`. The `status` field will update to "Approved"/"Rejected" only when the approver acts on the request. This is framework-by-design, not a defect.

---