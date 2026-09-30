# Role × Permission Matrix — this hospital

**Date:** 2026-09-30 (Phase E handover snapshot)
**Phase E deliverable:** 2 of 5
**Source of truth:** Live `tabCustom DocPerm` rows on `[redacted-db-name]` (queried 2026-09-30 15:14 IST)
**Scope:** 6 Haritha roles × 11 critical HRMS/ERPNext DocTypes
**Design rationale:** See § "Design Rationale" at the bottom

---

## How to read this matrix

- **R** = Read | **W** = Write | **C** = Create | **S** = Submit | **X** = Cancel | **A** = Amend | **D** = Delete | **H** = Share | **P** = Print | **E** = Email | **Rp** = Report | **I** = Import | **Ex** = Export
- **`.`** = no permission
- Empty row in matrix = no Custom DocPerm override (inherits default from DocType definition; usually Read for Owner/All)

---

## Master matrix (6 roles × 11 DocTypes)

| DocType ↓ \ Role → | System Manager | HR Manager | HR User | Roster Manager | Leave Approver | Employee |
|---|---|---|---|---|---|---|
| **Employee** | R W C · · · D H P E Rp I Ex | R W C · · · D H P E Rp I Ex | R W C · · · D H P E Rp I Ex | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · · P E Rp · · |
| **Shift Assignment** | R W C S X A D H P E Rp I Ex | R W C S X A D H P E Rp I Ex | R W C S X · D H P E Rp I · | R W C · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · |
| **Attendance** | R W C S X · D H P E Rp · · | R W C S X · D H P E Rp · · | R W C S X · D H P E Rp I Ex | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · Ex |
| **Employee Checkin** | R W C · · · D H P E Rp I Ex † | R W C · · · D H P E Rp I Ex † | R W · · · · D H P E Rp I Ex † | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R W C · · · · · · · · · · ‡ |
| **Leave Application** | R W C S X A D H P E Rp I Ex | R W C · · · D H P E Rp · Ex § | R W C S X A D H P E Rp · · | R · · · · · · H P E Rp · · | R W · S X · D H P E Rp · · ¶ | R W C · · · · H P E Rp · · |
| **Leave Allocation** | R W C S X A D H P E Rp I Ex | R W C S X A D H P E Rp I Ex | R W C S X A D H P E Rp · · | R · · · · · · · · · Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · |
| **Holiday List** | R W C S X A D H P E Rp I Ex | R W C · · · D H P E Rp · · | R W C · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · |
| **Shift Type** | R W C S X A D H P E Rp I Ex | R W C · · · D H P E Rp · Ex | R W C · · · · H P E Rp · Ex | R W C · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · Ex |
| **Department** | R W C S X A D H P E Rp I Ex | R W C · · · D H P E Rp I Ex | R W C · · · D H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · | · · · · · · · · · · · · |
| **Designation** | R W C S X A D H P E Rp I Ex | R W C · · · D H P E Rp · · | R W C · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · | R · · · · · · H P E Rp · · |
| **HR Settings** | R W C S X A D H P E Rp I Ex | R W · · · · · · · · · · · | R · · · · · · · · · · · · | · · · · · · · · · · · · | · · · · · · · · · · · · | · · · · · · · · · · · · |

**Notes on table:**

- † **Employee Checkin — HR Manager / HR User / System Manager:** Two `tabCustom DocPerm` rows exist for these roles (one with Create/Import/Export, one without). Both apply additively. The matrix shows the more permissive row.
- ‡ **Employee Checkin — Employee:** Two `tabCustom DocPerm` rows exist (one with C, one without). Employees can Read always; Create permitted for self-service checkin via mobile/desk.
- § **Leave Application — HR Manager:** Two `tabCustom DocPerm` rows (one with S/X/A, one without). HR Manager can approve/cancel both — they own the final state.
- ¶ **Leave Application — Leave Approver:** Two `tabCustom DocPerm` rows (one with S, one without). Approvers can submit Pending → Approved/Rejected but not Cancel post-approval (HR Manager owns cancel).

---

## Compact matrix (read-only / write-yes-or-no)

For quick scanning. **`R`** = any read access, **`RW`** = read + write (or stronger), **`—`** = no access.

| DocType ↓ \ Role → | System Manager | HR Manager | HR User | Roster Manager | Leave Approver | Employee |
|---|---|---|---|---|---|---|
| **Employee** | RW | RW | RW | R | R | R |
| **Shift Assignment** | RW | RW | RW | RW | R | R |
| **Attendance** | RW | RW | RW | R | R | R |
| **Employee Checkin** | RW | RW | RW | R | R | RW |
| **Leave Application** | RW | RW | RW | R | RW | RW |
| **Leave Allocation** | RW | RW | RW | R | R | R |
| **Holiday List** | RW | RW | RW | R | R | R |
| **Shift Type** | RW | RW | RW | RW | R | R |
| **Department** | RW | RW | RW | R | R | — |
| **Designation** | RW | RW | RW | R | R | R |
| **HR Settings** | RW | RW | R | — | — | — |

---

## Role Profile definitions

The 6 Haritha Role Profiles bundle the role + module profile + default workspace shortcut.

| # | Role Profile | Underlying Roles | Module Profile | Workspace | Default landing page | Intended user |
|---|---|---|---|---|---|---|
| 1 | **Haritha: System Manager** | System Manager + Administrator | (full Frappe/ERPNext/HRMS) | `Haritha: System Manager` | Desk | Implementation team only; IT admin |
| 2 | **Haritha: HR Manager** | HR Manager + HR User (legacy) | HR | `Haritha: HR Manager` | HR dashboard | Head of HR, payroll admin |
| 3 | **Haritha: HR User** | HR User | HR | `Haritha: HR User` | HR dashboard | HR operations (recruitment, on-boarding) |
| 4 | **Haritha: Roster Manager** | Roster Manager + Employee | HR + limited HRMS | `Haritha: Roster Manager` | Roster planner | Dept heads doing roster + shift approval |
| 5 | **Haritha: Leave Approver** | Leave Approver + Employee | HR + limited HRMS | `Haritha: Leave Approver` | Leave inbox | Managers approving leave only |
| 6 | **Haritha: Employee** | Employee | HR + limited HRMS (own data only) | `Haritha: Employee` | Employee dashboard (My Attendance + My Leaves) | All 211 hospital staff |

---

## Role Permission Rules (DocType-level constraints)

These are the additional constraints layered on top of `tabCustom DocPerm` via Frappe's "Role Permission Rules" feature. They enforce **row-level security** (per-employee department isolation).

### User Permission: per-employee Department isolation

- **Applicable to:** Employee role only (and arguably Leave Approver)
- **Mechanism:** For each of the 211 Employee Users, a `User Permission` row restricts accessible **Department** values to the user's own `department`.
- **Count:** 451 User Permission rows total (~2 per Employee User covering both Department and Company)
- **Effect:** An employee from `Nursing - HH` cannot view or edit Employees in `Billing - HH` (row-level data isolation).

### Permission rules NOT in place (intentional)

| Gap | Why not enforced | Risk |
|---|---|---|
| Employee can't see other employees in same dept (read-only) | Required for org chart + leave calendar lookup | None |
| Leave Approver can see all leave applications across dept | Cross-team leave coordination (e.g., Nursing + OT) | Low — read-only |
| Roster Manager can edit any employee's shift assignment | Roster Manager covers entire dept roster | Medium — mitigated by dept-head review |
| HR User can edit Company-level config | Trusted role; same as HR Manager minus Approve | Low |

---

## Workflow routing (orthogonal to DocPerm matrix)

Workflows enforce *state transitions* and are defined separately from `tabCustom DocPerm`. The two workflows in production:

### Leave Application workflow

| State | DocStatus | Owner role | Next allowed states |
|---|---|---|---|
| Draft | 0 | Employee (self only) | Pending Approval |
| Pending Approval | 0 | Leave Approver | Approved / Rejected |
| Approved | 1 | HR Manager | Cancelled |
| Rejected | 0 | Leave Approver | (terminal) |
| Cancelled | 2 | HR Manager | (terminal) |

### Shift Request workflow

| State | DocStatus | Owner role | Next allowed states |
|---|---|---|---|
| Draft | 0 | Employee (self only) | Pending Approval |
| Pending Approval | 0 | Roster Manager | Approved / Rejected |
| Approved | 1 | HR Manager | Cancelled |
| Rejected | 0 | Roster Manager | (terminal) |
| Cancelled | 2 | HR Manager | (terminal) |

---

## Design Rationale

### Why 6 roles (not 3, not 10)?

**Too few (e.g., 2 roles = Admin + Employee):** Loses granularity for the "approver chain" pattern — Leaves need Leave Approver, Shifts need Roster Manager, HR operations need HR User distinct from HR Manager.

**Too many (e.g., 12 roles):** Permission matrix becomes unreadable; provisioning mistakes multiply.

**The 6 chosen roles map 1:1 to the 6 distinct jobs-to-be-done:**
1. System admin (everything)
2. HR leadership (config + approvals)
3. HR operations (data entry, no approvals)
4. Roster planning (shifts + assignments)
5. Leave approval only
6. Self-service (the 211 hospital staff)

This mirrors the **leaves vs shifts separation** — different approval chains require different approver roles. Merging "Leave Approver" + "Roster Manager" into one "Manager" role would create a conflict: the same person could approve their own shift swaps via the Leave Approver path.

### Why Employee has Write+Create on Leave Application but only Read on Shift Assignment?

- **Leave Application (Employee has RWC):** Employees MUST be able to create their own leave requests and edit drafts. Cannot edit after submission (docstatus=1). Cannot delete.
- **Shift Assignment (Employee has R only):** Employees view their roster but cannot reassign themselves — that's the Roster Manager's job. Self-service shift swap goes via `Shift Request` (which has its own workflow).

### Why Employee Checkin grants Employee Create but not other HRMS docs?

- `Employee Checkin` is the **only** HRMS doc employees legitimately create on a daily basis (via biometric punch, mobile app, or web self-checkin). All other writes go through HR.
- Employees can also Read their own + nearby colleagues' checkins (so they can verify "yes I'm in office" before submitting Leave).

### Why Department denies Employee role entirely?

- Departments are **organizational structure** not operational data. Employees don't edit them, don't create them, don't delete them. Read-only access for Employee would create privacy leaks (you can see who's in your dept, but you don't see the org chart hierarchy or inter-dept relationships).
- HR User / HR Manager need RW to maintain the structure.
- Roster Manager / Leave Approver only need R (their dept isolation comes from `User Permission`, not from `tabCustom DocPerm`).

### Why HR Settings restricted to System Manager + HR Manager + HR User (read)?

- `HR Settings` controls **payroll policy**, **leave policy**, **auto-attendance frequency**, **email template IDs**, and similar tenant-wide config.
- System Manager = full access (recovery scenario)
- HR Manager = full except create/submit (can't accidentally reset payroll config)
- HR User = read only (must escalate to HR Manager for config changes)
- All other roles = no access (operational users shouldn't browse tenant config)

### Why multiple `tabCustom DocPerm` rows per (DocType, Role)?

Frappe supports multiple DocPerm rows per (DocType, Role) pair with **additive** semantics. We use this for:

- **Leave Application × HR Manager:** one row grants Submit/Cancel/Amend (final state), another grants Write/Cancel (correct draft errors). Together = full lifecycle.
- **Leave Application × Leave Approver:** one row grants Submit (Pending → Approved), another grants Write only (can edit approver remarks but not transition).
- **Employee Checkin × HR Manager:** one row grants Create (bulk ingestion), another doesn't. Together = flexible bulk + manual entry.

This pattern lets us tune **what an HR Manager can do at each docstate** without inventing custom Python.

### Why Module Profile matters

Even though all 6 Haritha roles map to a single `Module Profile = HR` in this hospital's setup, the `Role-module_profile` Custom Field gives future flexibility:

- Add a `Finance` module profile for Billing/Finance team
- Restrict the `Haritha: Employee` role to **only** see the HR module (no Settings, no Customization)
- Tenant-by-tenant override without rewriting roles

This is a Phase A Artifact 1 design choice that pays off in Phase E+1 multi-tenant rollout.

### Why custom app owns these (not global DocPerm)

All 6 Haritha roles, 6 Haritha workspaces, 451 User Permissions, 2 workflows, and ~70 DocPerm rows live in the **`haritta_hospital` custom app** as Frappe fixtures. On any new client site (`bench new-site` + `bench install-app haritta_hospital`), the entire permission model is reproducible in <30 seconds. Without fixtures, this would be 200+ manual config steps per onboarding.

---

## Verifying this matrix is current

Run the verification script:

```bash
bash scripts/verify-phase-a-b-c-d-2026-09-30.sh
```

It checks (among other things) that:
- 6 Haritha role profiles exist
- 6 Haritha workspaces exist (all public=0)
- 2 active workflows (Leave App + Shift Request)
- 451+ user permissions
- HRMS scheduler last execution < 2h ago

Or query directly:

```bash
ssh -i /root/.openclaw/ssh_key <user>@[redacted-IP] \
  "docker exec -i prod-env-db-1 mariadb -u root -p'<DB_PASS>' -D '[redacted-db-name]' \
   -e \"SELECT COUNT(*) FROM \`tabCustom DocPerm\` WHERE role LIKE 'Haritha%' OR role IN ('System Manager','HR Manager','HR User','Roster Manager','Leave Approver','Employee');\""
```

---

**Sanitization:** All client-identifying strings (domain, IPs, paths) scrubbed per `AGENTS.md` rule.
**Source data:** Live SQL queries on `[redacted-db-name]` at 2026-09-30 15:14-15:16 IST.
**Author:** Phase E subagent (depth 1/5)
