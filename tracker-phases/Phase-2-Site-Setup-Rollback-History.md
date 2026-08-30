# Phase 2 — Site Setup, Restart & Rollback History

> **Consolidated file** — merged from `006-phase-2-restart-pberpprod.md`, `016-phase-2-step-a1-a5-backup.md`, `007-phase-2-site-setup-rolledback.md`, `008-phase-3-data-import-rolledback.md`, `009-phase-4-shift-mgmt-rolledback.md`, `010-phase-5-prod-readiness-rolledback.md`.

> Preserves the full history of the Aug 21 10:11–10:18 IST rollback at `pberp.duckdns.org`, the Aug 25 21:43 IST Option B wipe + restart on `pberpprod.duckdns.org`, and the pre-flight backup.

----

## Source: 006-phase-2-restart-pberpprod.md (Phase 2 Restart #2 — pberpprod.duckdns.org)

## Phase 2 (Restart #2 — pberpprod.duckdns.org) (2026-08-25 22:00 IST) 🔄 IN PROGRESS

> Resumption context: Aug 21 10:11–10:18 IST rollback destroyed prior `pberp.duckdns.org` env. After considering options, Venkat chose **Option B (wipe + reinit) on `pberpprod.duckdns.org`** at 21:43 IST 2026-08-25. pberpprod was created but never loaded with real data — treated as QA/dev for wipe purposes.

**Goal:** Spin up Haritha Hospitals on `pberpprod.duckdns.org` with clean state.

**Plan (gated, no auto-progression):**

```
Step A1: bench --site prod backup --with-files (mandatory pre-flight)
Step A2: copy backup to /home/vijay/backups/prod/ (local)
Step A3: copy backup to venkat@135.125.196.35:/home/vijay/backups/prod/ (offsite)
Step A4: verify backup integrity (tar tzf + smoke-restore in dev)
Step A5: SHA256 backup, store checksum
  ↓ user ✅ on backup integrity
Step B1: stop site traffic (maintenance mode or DNS pause)
Step B2: drop database _<dbname>
Step B3: bench new-site pberpprod.duckdns.org
Step B4: install apps: frappe → erpnext → hrms 16.5.0 → payments
Step B5: configure domain + DuckDNS + cert (same URL, but cert may need refresh)
Step B6: 4×/day cron backup (per Lesson #79 hardening)
  ↓ user ✅ on env live
Phase 3: ingest in sub-phases (3a masters → 3b shift_assignments → 3c attendance/checkin/leave)
```

**Runbook reuse:** Aug 20 Phase 2 execution at `pberp.duckdns.org` is preserved in git history — sub-agents should reference commit history for exact commands, container names, MySQL grant patterns.

**Subagent model:** OX Alpha free (1M ctx, code-writing specialty, structured output).

**Lessons to apply (cumulative):**
- #44: pin hrms 16.5.0 (NOT 16.5.1+)
- #46: restart backend + workers after install-app
- #47: asset sync per-directory via host-staged `docker cp`
- #66: verify `sites/apps.txt` after install-app
- #79: wrap `bench backup` with `timeout 900` + `${PIPESTATUS[0]}` capture
- #80: edit `site_config.json` AND `sites/apps.txt` atomically



---

## Source: 016-phase-2-step-a1-a5-backup.md (Phase 2: Step A1-A5 Pre-flight Backup)

## Phase 2: Step A1-A5 Pre-flight Backup (2026-08-25 22:27 IST) ✅

**Goal:** Mandatory backup before any destructive wipe (Aug 19 lesson #79 + user safety rule).

**Status:** ✅ Complete + verified. SHA256 byte-match between local + offsite.

**Subagent:** OX Alpha free (1M ctx, code-writing specialty, run mode, lightContext=true). 1 fix applied: direct gateway→venkat `scp` invalid (files on vijay VPS). Subagent swapped to vijay→venkat SSH tar-pipe. Worked.

**Deliverables:**
- [x] Site name verified: `pberpprod.duckdns.org` (db `_b80f05e76a0dcaad`)
- [x] Local backup: `/home/vijay/backups/prod/20260825_222729/` (6 files, 1.23 MB master + 4 components + sha256)
- [x] Offsite backup: `venkat@135.125.196.35:/home/venkat/pberpprod_backups/20260825_222729/` (6 files, identical SHA256)
- [x] Master archive: `pberpprod_phase2_20260825_222729.tar.gz` (1,229,164 B)
- [x] gzip integrity test: OK on both sides
- [x] SHA256: `37ff656efa89ac04dfe9a93539dce24b8807de5f3149ae641731e47d71b39007` (matches local + offsite)
- [x] Disk after backup: 14G free / 81% used (stable)
- [x] Reusable script: `/tmp/phase2_backup.sh` on vijay VPS (idempotent, re-runnable)

**Pre-flight checks completed:**
- Container `erp-prod-backend-1` Up
- Site name from container (not assumed)
- Disk space >500MB free before backup
- Existing backups preserved (not deleted)

**Parent verification (Lesson #72):** Independent SHA256 + gzip integrity check via inline SSH after subagent completion. Both local + offsite verified byte-identical.

**Push to origin:** ✅ Done (inline fallback — Nemotron subagent hit FailoverError). 3 commits pushed: `219978d..7e95049`. Remote HEAD matches local.




---

## Source: 007-phase-2-site-setup-rolledback.md (Phase 2 Site Setup — ROLLED BACK 2026-08-21)

## Phase 2: Site Setup (🔄 ROLLED BACK 2026-08-21 — work preserved, env destroyed)

> **Rollback 2026-08-21:** All Phase 2 deployment work (pberp.duckdns.org site, 9 containers, apps, custom fields, MySQL grants, Company, Holidays) was destroyed when pberp env was torn down at 10:11–10:18 IST. Details below kept as historical record of what was planned and executed. Re-execute from scratch on new env.

**Goal:** Create Haritha Hospitals site on a fresh environment.

**Resolution:**
- ✅ **NEW dedicated env** (clean slate) — compose project `pberp` on main VPS (vijay@144.217.163.228)
- ✅ Skip custom app initially — use custom fields + fixtures for haritha-specific data
- ✅ Apps: frappe 16.x, erpnext 16.x, hrms 16.5.0 (pinned), payments

**Phases executed:**
- A: Pre-flight checks + certificate fix
- B: Compose up — 9 containers (backend, frontend, scheduler, queue-short, queue-long, websocket, redis-cache, redis-queue, db)
- C: Site creation — `pberp.duckdns.org`
- D: Apps install — frappe, erpnext, hrms 16.5.0, payments
- E: Custom fields fixtures
- F: MySQL grants (db user permissions for scheduler IP)
- G: Company "Haritha Hospitals" + Holiday List

**Deliverables:**
- [x] Site location: NEW env `pberp.duckdns.org` (compose project `pberp`)
- [x] Apps installed: frappe, erpnext, hrms 16.5.0, payments
- [x] Custom app: deferred (use custom fields + fixtures)
- [x] Company "Haritha Hospitals" created (INR, India)
- [x] Holidays loaded
- [x] Pre-flight backup (cron added in Phase I)

---



---

## Source: 008-phase-3-data-import-rolledback.md (Phase 3 Data Import — ROLLED BACK 2026-08-21)

## Phase 3: Data Import (🔄 ROLLED BACK 2026-08-21 — work preserved, env destroyed)

> **Rollback 2026-08-21:** All 24,511 records imported into pberp.duckdns.org were destroyed in the env teardown. The 19 CSV masters in `masters/` are intact and idempotent — re-run Phase 3 on new env to recover.

**Goal:** Load all master data from CSV into the site.

**Phases executed:**
- H1: 6 small entities imported (124 records: Dept/ET/LT/Designation/Shift Type)
- H1.5 + H1.5b: 18 ERPNext defaults deleted (10 left → 5 X-HH variants remaining)
- H2: 210 Employees imported (HR-EMP-00001 to HR-EMP-00210)
- H3: 5,317 Shift Assignments imported (210 employees × 25 shift types × 29 days)
- H4: 6,300 Attendance records imported (raw SQL bulk insert, 1:1 CSV match)
- H5: 12,562 Employee Checkin records imported (background jobs, 25 batches of ~500)
- DB cleanup: 5 X-HH Department variants force-deleted via direct SQL

**Deliverables:**
- [x] L1 Foundation: Company ✅, FY ✅, Holiday List ✅, Departments ✅ (36), Designations ✅ (48), Employment Type ✅ (6)
- [x] L2 Shift Management: Shift Types ✅ (25), Employees ✅ (210), Shift Assignments ✅ (5,317), Attendance ✅ (6,300), Leave Types ✅ (7)
- [x] Custom Fields fixtures (Rule #9 compliance)
- [x] Data validation (all 9 entities match CSV counts exactly)

**Final tally: 24,511 records across 9 entities.**

---



---

## Source: 009-phase-4-shift-mgmt-rolledback.md (Phase 4 Shift Management — ROLLED BACK 2026-08-21)

## Phase 4: Shift Management Workflow Testing (🔄 ROLLED BACK 2026-08-21 — work preserved, env destroyed)

> **Rollback 2026-08-21:** All backend API testing (K-1, K-2, K-3 — PASS), nginx config, worker fixes, and websocket routing were destroyed with pberp.duckdns.org. Backend tests were PASS (verified via API) — scripts can be re-run on new env. UI smoke test was already inconclusive (headless browser unreliable).

**Goal:** Test end-to-end shift management.

**Phases executed:**
- J-1: nginx HTTPS + security headers + routing config (TLSv1.2/1.3, HSTS, CSP, rate limiting)
- J-2: Worker fix (hrms/payments/frappe/erpnext imports in queue workers)
- K-1: Smoke + functional tests (auth, CRUD, entity counts) — **PASS**
- K-2: Functional CRUD + payroll integration — **PASS**
- K-3: HRMS integration (shift/leave/holiday/process_attendance) — **PASS**

**Backend tests PASS** for:
- Shift Assignment workflow ✅
- Auto Attendance (cron ready, needs activation) ✅
- Manual Attendance ✅
- Leave Application + Allocation ✅
- Employee Checkin ✅
- Holiday List ✅

**UI Smoke Test (08:00–09:40 IST 2026-08-21):**
- Site loads at https://pberp.duckdns.org ✅ (HTTP 200)
- Login form loads, API auth works ✅
- All asset bundles serve HTTP 200 (frappe/erpnext/hrms/payments dist/css/js) ✅
- Socket.io proxy added (nginx → pberp-websocket-1:9000) ✅
- System Settings `setup_complete=1` set ✅
- WebSocket container crashed with Redis `SocketClosedUnexpectedlyError` — restarted ✅
- Frappe desk bootstrap IS running (confirmed via browser console stack trace: `desk.js:34 startup`, `sidebar.js:30 prepare`, `notifications.js:476 make`)
- Vue.js SPA mounted but stays on loading splash — **inconclusive** due to headless browser tool unreliability (timeouts, false-negative evaluations)
- **No reliable UI smoke test result** — needs manual browser verification

**Issues encountered (resolved):**
- nginx upstream port: `:80` → `:8080` (frontend listens on 8080)
- Installed Application `is_setup_complete=1` (4 apps)
- System Settings `setup_complete=1`
- Custom app migration path not used (apps installed at runtime, not via apps.json)
- Asset hash sync required (Lesson #47): frontend assets rebuilt + synced via host-staged `docker cp`
- WebSocket container restart loop (Redis connection transient error)

**Issues outstanding (UI):**
- Desk JS mount hangs in headless browser — needs real browser test
- nginx `Upgrade: websocket` header force-set (added during debugging — may need revert if not needed)
- User `Administrator` default `desktop:home_page=setup-wizard` — may need clearing for production

**Deliverables:**
- [x] Shift Assignment creation (via API) ✅
- [x] Manual Attendance ✅
- [x] Leave Application + Allocation ✅
- [x] Employee Checkin ✅
- [x] Reports (API tested, UI untested)
- [ ] ⚠️ Auto Attendance cron activation — pending
- [ ] ⚠️ UI smoke test in real browser — pending

---



---

## Source: 010-phase-5-prod-readiness-rolledback.md (Phase 5 Prod Readiness — ROLLED BACK 2026-08-21)

## Phase 5: Production Readiness (🔄 ROLLED BACK 2026-08-21 — work partially preserved)

> **Rollback 2026-08-21:** Backup cron on vijay@144.217.163.228 (`/home/vijay/scripts/pberp_backup.sh`) is destroyed along with the env. The cron schedule (`0 */6 * * *`) and offsite push to venkat@135.125.196.35 will need to be recreated on new env. One backup file (`pberpprod_backup_20260821_000039.tar.gz`, 1.6 MB) exists on venkat VPS — covers pre-Phase 4 state.

**Goal:** Audit and harden for production.

**Phases executed:**
- I: Backup cron + first run + offsite to venkat VPS ✅
  - Script: `/home/vijay/scripts/pberp_backup.sh` (139 lines, hardened per Lesson #79)
  - Cron: `0 */6 * * *` (00:00, 06:00, 12:00, 18:00 IST)
  - Local retention: 7 days at `/home/vijay/backups/pberp/`
  - Offsite: forever at `venkat@135.125.196.35:/home/venkat/pberp_backups/`
  - First run: `pberpprod_backup_20260821_000039.tar.gz` (1.6 MB) ✅

**Deliverables:**
- [x] Backups (cron 4×/day, 7d local + forever offsite) ✅
- [ ] ⚠️ Pre-flight + post-flight process documentation — pending
- [ ] ⚠️ Disaster recovery tested — pending
- [ ] ⚠️ UI smoke test (real browser) — pending
- [ ] ⚠️ User training — pending
- [ ] ⚠️ Go-live — pending

**Remaining phase:**
- L: Cert monitoring + final sign-off report — **PENDING (next session)**

---

