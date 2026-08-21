# INDEX — Haritha Hospitals

**Project code:** `haritha-hospitals`
**Owner:** Venkat (Processbricks) | **Builder:** ERPClaw + subagents
**Started:** 2026-08-19
**Last updated:** 2026-08-21 11:55 IST
**Status:** 🔄 **RESTART FROM PHASE 1** — Phase 2 deployment (`pberp.duckdns.org`) destroyed in 2026-08-21 10:11–10:18 IST teardown (Option B: nuke, no backup). 24,511 records + deployment artifacts lost. Phase 0 + 1 design preserved (CSV masters + git history intact). Phases 2–5 need redo on new env.
**Target environment:** TBD — see Open Question #1 / #3 (new domain pending user decision)
**Source data:** 19 CSV masters in `masters/` (1.77 MB, 24,758 rows) — canonical, read-only

---

## 1. Project Title + Status

**Haritha Hospitals** is a real hospital project (CMM Level 5 target) running on Frappe 16.x + ERPNext 16.x + HRMS 16.5.0. The MVP scope is **shift management + HRMS basics** (employees, departments, shift types, attendance, leave, checkin). Wards, beds, OTs, pharmacy, lab, billing, full CoA, and cost centers are **deferred**.

All work is **document-first, git-tracked, gate-gated**: every phase produces a canonical artifact, every transition requires explicit human approval, and the entire process is reproducible from this repo alone.

## 2. Table of Contents

| # | Doc | Purpose | Lines |
|---|---|---|---|
| 1 | `README.md` | Project overview, stack, file map | ~30 |
| 2 | `TRACKER.md` | Canonical project tracker (status, phases, decisions, subagent log) | master |
| 3 | `INDEX.md` | **This file** — entry point linking all docs | this |
| 4 | `DECISIONS.md` | All 28 decisions extracted from TRACKER.md Decisions Log | full |
| 5 | `WORKFLOW.md` | Phase 2–5 runbooks (site setup, import, testing, prod) | committed by Agent C (cb546db) |
| 6 | `MIGRATION-GUIDE.md` | End-to-end redeploy guide post-rollback | committed by Agent C (fe33f31) |
| 7 | `PRODUCTION-READINESS-AUDIT-2026-08-21.md` | Current prod readiness state (post-rollback) | this set |
| 8 | `knowledge/` | Domain knowledge notes (TBD) | empty |
| 9 | `masters/` | 19 CSV masters (canonical source, idempotent re-import safe) | 1.77 MB / 24,758 rows |
| 10 | `all_schemas.csv` | Schema definitions for 15 master entities (schema-only) | committed |

## 3. Status Snapshot (effective 2026-08-21 11:55 IST)

| Phase | State | Notes |
|---|---|---|
| Phase 0 — Schema Planning | ✅ done | preserved |
| Phase 1 — Schema Approval | ✅ done | preserved (manager signed off 2026-08-20) |
| Phase 2 — Site Setup | 🔄 rolled back | needs redo on new env |
| Phase 3 — Data Import (24,511 records) | 🔄 rolled back | needs redo |
| Phase 4 — Workflow Testing (backend PASS) | 🔄 rolled back | needs redo |
| Phase 5 — Production Readiness | 🔄 rolled back | needs redo |
| Phase L — Cert monitoring + sign-off | ⏳ pending | never reached |

**Preserved:** CSV masters in `masters/` (19 files, 1.77 MB, 24,758 rows), Phase 0 + 1 design decisions, full git history (back to a468113 + earlier), Venkat VPS backups (`pberpprod_backup_20260821_000039.tar.gz` — covers 1.6 MB but pre-Phase 4 data).

**Lost:** pberp.duckdns.org env, 24,511 records across 9 entities, all live config (Company, Holidays, Custom Fields), backup cron on vijay@144.217.163.228, all nginx/websocket/workers config.

**Restart strategy:** Pick new env domain → re-run Phase 2 → re-run Phase 3 → re-run Phase 4 → re-run Phase 5. CSV masters are idempotent so re-import is safe.

## 4. Quick Navigation

| If you want to … | Read |
|---|---|
| Get a 30-second overview of the project | `README.md` |
| Check current status + what changed today | `TRACKER.md` (Project Status section) |
| Understand why each decision was made | `DECISIONS.md` (28 entries chronological) |
| Run a phase end-to-end | `WORKFLOW.md` (Phases 2–5 runbooks) |
| Reproduce the deployment from scratch | `MIGRATION-GUIDE.md` |
| Audit production readiness (post-rollback) | `PRODUCTION-READINESS-AUDIT-2026-08-21.md` |
| Inspect or modify canonical data | `masters/` (19 CSV files, read-only) |
| Verify schema definitions | `all_schemas.csv` (15 entities, schema-only) |

## 5. Recent Activity (last 5 commits)

```
fe33f31 docs(migration): add MIGRATION-GUIDE.md for pberpqa redeploy post-rollback  (Agent C)
cb546db docs(workflow): add WORKFLOW.md with Phase 2-5 runbooks                     (Agent C)
a0d1be9 docs(tracker): rollback event 2026-08-21 — pberp teardown, restart from Phase 1
a468113 docs(tracker): update Phases 2-5 — site setup, data import (24,511 records), nginx + workers, backup cron
7efaf6f docs(plan): add Phase 2 setup plan for pberp.duckdns.org (Haritha Hospitals)
```

## 6. Stack

- **Frappe:** 16.x
- **ERPNext:** 16.x
- **HRMS:** 16.5.0 (pinned per lesson #44 — v16.5.1+ breaks on `repost_allowed_types`)
- **Payments:** (optional, per project plan)
- **Custom app:** TBD (deferred for MVP — using custom fields + fixtures; pberp_hospital patterns as reference)

## 7. Open Questions (top 3, full list in `TRACKER.md`)

1. **New env domain** — reuse `pberp.duckdns.org` (faster, but was the destroyed env) or pick new domain like `haritha.duckdns.org` (cleaner — no association with teardown)? **Decision needed before Phase 2 restart.**
2. **UI verification in real browser** — needed before go-live; headless browser tool unreliable during Phase 4 testing.
3. **nginx `Upgrade: websocket` force-set** — added during Phase 4 UI debugging; should we revert for new env?

## 8. References

- `README.md` — project overview
- `TRACKER.md` — master tracker
- `DECISIONS.md` — decision log (this set)
- `WORKFLOW.md` — phase runbooks (Agent C)
- `MIGRATION-GUIDE.md` — end-to-end guide (Agent C)
- `PRODUCTION-READINESS-AUDIT-2026-08-21.md` — current prod state (this set)
- `masters/` — 19 CSV source files
- `all_schemas.csv` — 15-entity schema definitions

---

**Doc set assembled:** INDEX + DECISIONS + AUDIT (this batch, 3 commits by venkat-narasimha) on top of WORKFLOW + MIGRATION-GUIDE (2 commits by Agent C). Total: 5 canonical docs aligned to pberpqa-hospital-demo structure.
