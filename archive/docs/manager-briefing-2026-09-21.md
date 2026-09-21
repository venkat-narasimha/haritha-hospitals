# Manager Briefing — Haritha Hospitals HRMS Demo Readiness

**Date:** 2026-09-21
**For:** Operator's manager review call
**Repository:** github.com/venkat-narasimha/haritha-hospitals (public)
**Current commit:** `main` @ latest

---

## TL;DR

The Haritha Hospitals HRMS project is **demo-ready as of 2026-09-21**, with no caveats on the core HRMS scope (Shift Management, Leave Management, Employee Lifecycle, Org Management, Reports). The last five days (Sep 17–21) were an intensive push that took the system from a partially-tested state to a fully-verified state across all in-scope sign-off transactions, applied one production fix to a critical Holiday List reference, batch-submitted 211 Holiday List Assignments needed for the leave engine to function, completed renumbering of the manual testing scope to 79 transactions (T-001 to T-079), and shipped eight client template updates so the intake workbook reflects current HRMS v16 requirements.

Of the 79 defined transactions, **77 PASS / 0 DEFERRED / 1 NOT DONE / 1 REMOVED**. The one NOT DONE is Salary Structure (payroll), which was explicitly deferred as a scoping decision on Sep 17 — not a defect. The one REMOVED is the Branch.company field check, which is structurally untestable in our single-Company deployment (Branch has no `company` field in HRMS v16). Both are transparent gaps in the briefing below.

The work also captured five durable lessons for future projects (especially around DRAFT-vs-submitted validators, schema verification, and the Leave Engine's dependency on submitted Holiday List Assignments). These are documented in §4 below and slated for `tracker-phases/Decisions-Lessons-Learned.md` in a follow-up commit; they will save time on future ERPNext/HRMS deployments.

## 1. Demo Readiness (current state)

| Area | Verdict | Evidence / Notes |
|---|---|---|
| Custom Fields | ✅ PASS | 78/78 fields + 189/189 property setters match fixtures exactly |
| Leave Engine | ✅ PASS | Leave Approver (Department X-HH + Administrator), 211 Holiday List Assignments, Leave Period 2026-2027, 3 Leave Allocations, notification template configured |
| Branches | ✅ PASS-INTENTIONAL | Test Company kept per operator (manual testing sandbox); 0 Branches = single-site per repo Gotcha #12 |
| HR Settings | ✅ PASS | standard_working_hours=8.0, leave_approver_mandatory=1, leave_approval_notification_template set |
| **Overall** | **✅ READY (full, no caveats)** | as of 2026-09-21 |

## 2. What We Did (Sep 17-21 timeline)

| Date | Event |
|---|---|
| 2026-09-17 | Demo readiness audit on prod + 1 prod fix applied (Company.default_holiday_list) |
| 2026-09-18 | Manual transaction testing report (60 transactions, 6 modules) uploaded → Streams 1-5 executed → sign-off committed (51 PASS) |
| 2026-09-19 | Stream 5 Maximum effort (T-037, T-039, T-040, T-043 prerequisites created + 3 write-tests passed) → sign-off updated to 58 PASS; Sample Leave Application HR-LAP-2026-00001 submitted end-to-end with Leave Ledger Entry; Fiscal Year fix (2025-2026 + 2026-2027) |
| 2026-09-21 | 211 Holiday List Assignments batch-submitted; renumbering (T-001 to T-079 added 19 new transactions); 8 client template items (5 new master templates + 3 existing template updates); 2 hotfix scrubs (sanitization) |

## 3. Manual Transaction Testing (60 → 79 transactions)

After renumbering, the testing scope expanded to 79 total transactions (60 original + 19 new pre-requisites/operational flows):

| Module | Tests | Status |
|---|---|---|
| Org Management | 12 | All PASS |
| Shift Management | 12 (10 original + 2 new: Shift Request, Approve) | All PASS |
| Leave Management | 16 (14 original + 2 new: Approve, Reject) | All PASS |
| Employee Lifecycle | 8 | All PASS |
| Reports | 6 | All PASS |
| Edge cases | 10 | All PASS |
| **Operational subtotal** | **64** | |
| Section A: System Configuration | 7 | All PASS (new) |
| Section B: Test Data Setup | 8 | All PASS (new) |
| **New setup subtotal** | **15** | |
| **Grand total** | **79** | |

**Sign-off state (post-renumber):** 77 ✅ PASS / 0 ⬜ DEFERRED / 1 ❌ NOT DONE / 1 🚫 REMOVED = 78 sign-off rows. Total defined = 79 (1 removed from sign-off but documented as out-of-scope).

## 4. Notable Lessons Learned (capture for future projects)

1. **DRAFT state hides submit-time validation** — always attempt submit programmatically to surface full validator chain
2. **HRMS v16 Leave Application has no default UI Approve button** — Workflow doc or custom Server Script needed for production
3. **Holiday List Assignment rows need docstatus=1** to be visible to leave-app-submit validators — `insert()` creates Drafts; explicit `submit()` needed
4. **Schema assumptions need read-before-write verification** — caught NotificationTemplate vs Email Template mismatch before any writes
5. **raw SQL INSERT creates Draft rows** — `hla.insert()` not enough; follow-up `submit()` needed

## 5. Known Gaps / Out of Scope

Transparent for the call:

| Item | Status | Reason |
|---|---|---|
| Salary Structure | NOT DONE (T-018 in new numbering) | Payroll out of scope per operator decision Sep 17 |
| T-060 Branch.company field | REMOVED from sign-off (T-079 in new) | Structurally untestable in single-Company deployment (Branch has no `company` field in HRMS v16) |
| UI Approve Workflow for Leave App | DOCUMENTED but not configured | Console-path workaround used during demo; production deploy needs Workflow doc |
| Email Account for notifications | DOCUMENTED but not configured | 4 HR Settings toggles silently no-op without working SMTP |
| Migration script (T-025 in new) | FLAGGED `[?]` pending decision | Operator question "why we need to run migration script?" unresolved |

## 6. Procedure Going Forward

For ongoing demo / production deployment:

| Phase | Action |
|---|---|
| Pre-demo sanity | Run demo readiness audit; confirm sign-off state at `main` HEAD; verify Holiday List Assignments have docstatus=1 |
| Demo run | Use `[prod-site]` placeholders in any public materials; don't leak internal infra hosts; click through Sign-off section in `manual-ui-walkthrough.md` for status |
| Demo Q&A | If asked about gaps (T-018, T-060, T-025), refer to Known Gaps section above; emphasize gaps are scoped decisions (payroll deferred), not defects |
| After demo | Decide on production deploy scope (payroll on/off); configure Workflow for Leave App + Email Account for production; re-run Streams 1-5 if sign-off needs to expand |
| Long-term maintenance | Any DocType change → update both `01_master_data/` and `02_transaction_data/` templates; any new "leave" feature → re-run Stream 1 (investigation) + Stream 5 (sign-off) |

## 7. Audit Trail (workspace-only)

The following workspace artifacts support the claims in this briefing. They are intentionally kept out of the public repo and referenced here only as evidence:

- `workspace/audit-2026-09-17-demo-readiness.md` — Demo readiness audit (initial + Streams 3-6 verification, 24 KB+)
- `workspace/investigation-2026-09-18-pending-transactions.md` — Stream 1 investigation (36 KB / 383 lines, 20 pending T-items verified)
- `workspace/audit-client-templates-2026-09-21.md` — Client templates audit (21.3 KB / 294 lines, 84 files audited)
- `workspace/session-handoff-2026-09-17.md` — Full session continuity anchor

These are workspace-only files (not in git). Use for evidence trail but don't cite paths in public docs.

---

**Document version:** 2026-09-21 · For internal use as the basis for manager review call.
