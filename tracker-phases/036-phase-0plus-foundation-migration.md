## Phase 0+ — Foundation & Migration (2026-08-28 to 2026-08-29)

> New top-level phase added today: custom app build + master data migration + outage recovery. Distinct from the existing Phase 0 (schema planning) — this is "Phase 0.5 / Schema-Portability Layer".

### Custom App Build (2026-08-28)
- ✅ GitHub repo `venkat-narasimha/haritha_hospital` created (private)
- ✅ `bench new-app` skeleton committed + pushed (commit `4023ccd`)
- ✅ Re-tagged 192 customizations in pberpprod (189 Property Setter + 3 Print Format, plus 78 Custom Field + 2 Notification + 2 Letter Head already tagged from earlier)
- ✅ Configured `hooks.py` with `fixtures = [...]` block (5 fixture types)
- ✅ Exported **274 customizations** as JSON fixtures (5 files in `apps/haritha_hospital/haritha_hospital/fixtures/`)
- ✅ Committed fixtures + pushed (commit `93e8c48`)

### Install + Verify (2026-08-28)
- ✅ Installed on **pberpdev** (fresh) — all 274 customizations loaded
- ✅ Installed on **pberpprod** (idempotent) — already in `installed_apps`
- ✅ Both envs verified at **78 CF + 189 PS + 3 PF + 2 N + 2 LH = 274 rows**
- ✅ Per-environment DB counts match (78/189/3/2/2 on both)

### 🔴 Incident: Both envs 500'd (2026-08-29 03:06 IST)
- **Root cause:** gunicorn `--preload` froze sys.path at container start (dev=9d old, prod=2d old) — today's `.pth` file not seen by gunicorn
- **Symptom:** every request returned `ModuleNotFoundError: No module named 'haritha_hospital'` → HTTP 500 in ~35ms
- **Fix:** `docker restart erp-{dev,prod}-backend-1` (~30-60s downtime each)
- **Volume verify (Lesson #72):** all critical paths on **named Docker volumes** (`erp-{dev,prod}_sites`, `erp-{dev,prod}_db-data`); writable layer `<nil>` — zero data loss risk
- **Recovery:** dev=200, prod=200 on `/`; dev login 200 (admin/admin123); **prod login 401** ⚠️ — DB password drifted from MEMORY
- **Action items:** MEMORY DB pwd correction (done), prod admin pwd recovery (pending), gunicorn preload lesson added (#153)

### Master Data Migration (prod → dev) (2026-08-29)
- ✅ Company: 1 (Haritha Hospitals)
- ✅ Employee: 210
- ✅ Department: 37, Designation: 48
- ✅ Account: 89 (5 root accounts skipped)
- ✅ Cost Center: 2
- ✅ Item Group: 6, UOM: 239
- ✅ Shift Type: 25, Holiday List: 1
- ✅ Gender: 1 new (Not Specified), Employment Type: 6
- ✅ Shift Schedule: 5, Shift Assignment: 7,829 (1 rejected — data conflict)
- ✅ Shift Request: 7/8 (1 HRMS validation conflict)
- ✅ All 8,118 Shift Assignments on dev bulk-submitted (docstatus=1)
- ✅ Migration script saved to `scripts/migrate_master_data.py` (idempotent, 16 DocTypes, 10 gotchas documented — see LEARNINGS #157)
- ✅ Roster on dev verified rendering data (Phase 4.11 fix held)

### Phase 5: SKIPPED per Venkat 2026-08-28
DR test, error monitoring, security audit, SSL audit, UAT, perf baseline — all deferred.

### Phase 6: TBD
- HRMS version-check in `haritha_hospital/__init__.py` (deferred — should add before Phase 6)
- MEMORY.md DB password audit (DONE today 2026-08-29)
- Phase 5 items still skipped (DR, security audit, etc.)
- ISO/CMM L5 docs (per Venkat 2026-08-25)

### New Lessons Documented (LEARNINGS.md)
- #151 — `bench export-fixtures` requires `fixtures = [...]` in hooks.py
- #152 — Frappe v16 uses `module` column, not `app`
- #153 — Gunicorn `--preload` + new app = backend restart required (root cause of P1 outage)
- #154 — `docker restart` ≠ `docker-compose down` (volume preservation)
- #155 — Letter Head table has no `module` column
- #156 — Print Format/Notification `module IS NULL` = old stock seeds
- #157 — Master data migration pattern (upsert + 10 gotchas)

### Comprehensive Guide
See: `docs/HARITHA_HOSPITALS_GUIDE.md` (400-600 line end-to-end reference for the project, including architecture, tech stack, customizations catalog, migration playbook, and operational runbook).


---

