# Phase 6 — Process & Maturity Documentation

> **Consolidated file** — merged from `037-phase-6-process-maturity.md`. Covers the 34 docs / ~14,030 lines of process and maturity documentation produced 2026-08-29.

----

## Phase 6 — Process & Maturity Documentation (2026-08-29)

**Status:** COMPLETE ✅ (34 docs, ~14,030 lines)

### Custom App Build (Phase 0+ foundation)
- ✅ GitHub repo `venkat-narasimha/haritha_hospital` (singular) created
- ✅ `bench new-app haritha_hospital` skeleton committed + pushed (commit 4023ccd)
- ✅ Re-tagged 192 customizations in pberpprod (189 PS + 3 PF)
- ✅ Configured `hooks.py` with `fixtures = [...]` block
- ✅ Exported 274 customizations as JSON fixtures
- ✅ Committed fixtures + pushed (commit 93e8c48)

### Install + Verify
- ✅ Installed on pberpdev (fresh) — 274 customizations loaded
- ✅ Installed on pberpprod (idempotent) — already in installed_apps
- ✅ Both envs verified at 78 CF + 189 PS + 3 PF + 2 N + 2 LH = ~274 rows

### Critical Incident: Both envs 500'd (2026-08-29 03:06 IST)
- 🔴 Root cause: gunicorn `--preload` froze sys.path at container start
- ✅ Fix: `docker restart erp-{dev,prod}-backend-1`
- ✅ Volume verify confirmed data persistence
- See LEARNINGS #153, #154, #157

### Master Data Migration (prod → dev)
- ✅ 16 DocTypes migrated (Company, Employee 210, Item, Shift Assignment 7,829, etc.)
- ✅ 8,118 Shift Assignments bulk-submitted
- ✅ Script: `scripts/migrate_master_data.py` (idempotent, documented gotchas)

### Phase 6 Documentation (34 docs, ~14,030 lines)
- ✅ Tier 0: Foundations (2 docs)
- ✅ Tier 1: Schema (2 docs)
- ✅ Tier 2: Workflow (2 docs)
- ✅ Tier 3: Client Presentation (3 docs)
- ✅ Tier 4: Runbooks (4 docs)
- ✅ Tier 5: Process (2 docs)
- ✅ Tier 6: Compliance/Maturity (12 docs — ISO 27001 + CMM L5)
- ✅ Tier 7: User Manuals (3 docs)
- ✅ Tier 8: Testing (3 docs)
- ✅ `docs/HARITHA_HOSPITALS_GUIDE.md` (543 lines)
- All pushed to `github.com/venkat-narasimha/haritha-hospitals` (dash, docs repo)
- Commits: `e8b04ca`, `6b9cf3d`, `890fee4`, `d1c76ce`, `6fa8deb`, `4cb85c7`, `facf8d5`, `8017c49`, `63caa2b`

### Phase 5 Status
SKIPPED per Venkat (DR test, security audit, SSL audit, UAT, perf baseline — deferred)

### Open items (deferred)
- [x] Update MEMORY.md / LEARNINGS.md — DONE 2026-08-29
- [ ] Quarterly DB password audit
- [ ] Quarterly DR drill (run 04.3 procedure)
- [ ] Run 8-phase regression test (08.3) on pberpdev
- [ ] Update pberpqa env to v16 (skipped today — might want to revisit)
- [ ] Phase 5 items if revisited
- [ ] Real audit-grade Tier 6 docs if pursuing certification
- [ ] HRMS version-check in `haritha_hospital/__init__.py` (deferred)

### Phase 6 — Documentation Index
See `docs/phase6/README.md` for the full index. Tier 6 (compliance/maturity) lives under `docs/phase6/09-compliance/` despite the tier numbering — the folder was named that way in Tier 6 Batch 1 to distinguish from process-level docs (Tier 5). Renaming deferred.
