# Manager Call Cheatsheet — Haritha Hospitals HRMS Demo Readiness

**Date:** 2026-09-21
**For:** Manager review call
**Current HEAD:** `6fb1e7e` on `main`

---

## 1. Headline

- **1.1** Demo status: **READY (full)** as of 2026-09-21
- **1.2** Sign-off: **77 ✅ / 0 ⬜ / 1 ❌ / 1 🚫** = 78 rows
- **1.3** Timeline: **5 days** (Sep 17–21), all issues resolved

---

## 2. Demo Readiness by Area

- **2.1** Custom Fields — ✅ PASS (78/78 + 189/189 fixtures match)
- **2.2** Leave Engine — ✅ PASS (Approver + 211 HLAs + Leave Period + Allocations + Notifications)
- **2.3** Branches — ✅ PASS-INTENTIONAL (Test Company kept as sandbox)
- **2.4** HR Settings — ✅ PASS (standard_working_hours=8.0 + notification template)
- **2.5** **Overall verdict: ✅ READY (full, no caveats)**

---

## 3. Timeline (Sep 17–21)

- **3.1** Sep 17 — Demo readiness audit + 1 prod fix (Company.default_holiday_list)
- **3.2** Sep 18 — Manual test 60 transactions + Streams 1-5 fixes
- **3.3** Sep 19 — Sample Leave App end-to-end submit + Fiscal Year fix (2025-26 + 2026-27)
- **3.4** Sep 21 — 211 HLAs batch + renumbering + 8 client templates + 2 sanitization hotfix scrubs

---

## 4. Manual Transaction Testing

- **4.1** Total transactions: **79** (60 original + 19 new pre-reqs/operational flows)
- **4.2** By module:
  - **4.2.1** Org Management — 12 (all PASS)
  - **4.2.2** Shift Management — 12 (10 original + 2 new: Shift Request, Approve)
  - **4.2.3** Leave Management — 16 (14 original + 2 new: Approve, Reject)
  - **4.2.4** Lifecycle — 8 (all PASS)
  - **4.2.5** Reports — 6 (all PASS)
  - **4.2.6** Edge cases — 10 (all PASS)
  - **4.2.7** Section A (System Configuration, new) — 7 (all PASS)
  - **4.2.8** Section B (Test Data Setup, new) — 8 (all PASS)
- **4.3** Sign-off: **77 ✅ / 0 ⬜ / 1 ❌ / 1 🚫** = 78 rows

---

## 5. Notable Lessons Learned

- **5.1** DRAFT state hides submit-time validation errors — always attempt programmatic submit
- **5.2** HRMS v16 Leave Application has no default UI Approve button — Workflow doc or custom Server Script needed
- **5.3** Holiday List Assignment rows need `docstatus=1` — raw `insert()` creates Drafts; explicit `submit()` needed
- **5.4** Schema assumptions need read-before-write verification — caught NotificationTemplate vs Email Template mismatch
- **5.5** Raw SQL `INSERT` creates Draft rows — `insert()` not enough; follow-up `submit()` needed

---

## 6. Known Gaps / Out of Scope

- **6.1** Salary Structure (T-018) — NOT DONE; payroll deferred per operator decision
- **6.2** T-079 (originally T-060) Branch.company — REMOVED; HRMS v16 has no `company` field; structurally untestable
- **6.3** UI Approve Workflow for Leave App — DOCUMENTED but not configured (console-path workaround used during demo)
- **6.4** Email Account for notifications — DOCUMENTED but not configured (4 HR Settings toggles silently no-op without working SMTP)
- **6.5** Migration script (T-025) — FLAGGED `[?]` pending decision

---

## 7. Procedure Going Forward

- **7.1** Pre-demo sanity — run demo readiness audit; verify Holiday List Assignments have docstatus=1
- **7.2** Demo run — use `[prod-site]` placeholders; click through Sign-off section in test docs
- **7.3** Demo Q&A — refer to Known Gaps section; emphasize gaps are scoped decisions, not defects
- **7.4** Post-demo — decide on production deploy scope; configure Workflow for Leave App + Email Account
- **7.5** Long-term maintenance — any DocType change → update both `01_master_data/` and `02_transaction_data/` templates

---

## 8. Audit Trail (workspace-only)

- **8.1** `workspace/audit-2026-09-17-demo-readiness.md` — initial audit + Streams 3-6 verification
- **8.2** `workspace/investigation-2026-09-18-pending-transactions.md` — Stream 1 investigation
- **8.3** `workspace/audit-client-templates-2026-09-21.md` — 84 client files audited
- **8.4** `workspace/session-handoff-2026-09-17.md` — session continuity anchor

---

**Version:** 2026-09-21 · Hierarchical-numbered call reference.
**Companion to:** `manager-briefing-2026-09-21.md` (7-section detail version).
