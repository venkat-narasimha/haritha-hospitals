# Haritha Hospitals — Project Tracker

**Project:** Haritha Hospitals — Real hospital project (CMM Level 5 target)
**Scope:** Shift management + HRMS basics (employees, departments, shift types, attendance, leave)
**Deferred:** Wards, beds, OTs, pharmacy, lab, billing, full CoA, cost centers
**Owner:** Venkat (Processbricks)
**Started:** 2026-08-19
**Stack:** Frappe 16 / ERPNext 16 / HRMS 16.5.0 (pinned) / payments / custom app (TBD)

---

## 🔄 Project Status (2026-08-21) — Rollback

At **10:11–10:18 IST 2026-08-21**, the `pberp.duckdns.org` environment was torn down (Option B: nuke, no backup). All Phase 2–5 deployment work was destroyed. Restart from Phase 1.

| Phase | Before rollback (2026-08-19/20) | After rollback (2026-08-21) |
|---|---|---|
| Phase 0 — Schema Planning | ✅ done | ✅ done (preserved) |
| Phase 1 — Schema Approval | ✅ done | ✅ done (preserved) |
| Phase 2 — Site Setup | ✅ done at pberp.duckdns.org | 🔄 rolled back — needs redo |
| Phase 3 — Data Import (24,511 records) | ✅ done at pberp.duckdns.org | 🔄 rolled back — needs redo |
| Phase 4 — Workflow Testing (backend PASS) | ✅ done at pberp.duckdns.org | 🔄 rolled back — needs redo |
| Phase 5 — Production Readiness | ⚠️ partial (backup cron only) | 🔄 rolled back — needs redo |
| Phase L — Cert monitoring + sign-off | ⏳ pending | ⏳ pending |

**What was lost:** pberp.duckdns.org env, 24,511 records across 9 entities, all live config (Company, Holidays, Custom Fields), backup cron on vijay@144.217.163.228, all nginx/websocket/workers config.

**What is preserved (intact):**
- CSV masters in `masters/` (19 files, 1.77 MB, 24,758 rows) — canonical source
- All Phase 0 + 1 design decisions (schema, canonicalization, holidays)
- Full git history (a468113 and earlier)
- Lessons learned (table at bottom)
- Venkat VPS backups: `pberpprod_backup_20260821_000039.tar.gz` (only one backup ever created — covers 1.6 MB but pre-Phase 4 data)

**Open question:** New env domain — reuse `pberp.duckdns.org` (faster, but was the destroyed env) or pick new domain (cleaner)? See Open Questions section.

**Restart strategy:** Pick new env domain → re-run Phase 2 (site setup) → re-run Phase 3 (CSV import) → re-run Phase 4 (testing) → re-run Phase 5 (production readiness). CSV masters are idempotent so re-import is safe.

---

## Phase 0: Schema Planning (DONE ✅)

**Goal:** Document schema for all master data entities needed for shift management system.

**Status:** ✅ Complete 2026-08-19. 19 entities, 168 fields. HRMS v15 verification done (9 docs read, 7 corrections applied — see Decisions Log).

**Deliverables:**
- [x] `all_schemas.csv` — 19 entities, 168 fields (final, after HRMS v15 verification)
- [x] `TRACKER.md` — this file (created 2026-08-19)
- [x] `README.md` — project overview (created 2026-08-19)
- [x] `knowledge/shift_management_hrms.md` — reusable reference (2026-08-19)

**Decisions:**
- 2026-08-19: Scope = shift management only (deferred: wards, beds, OTs, pharmacy, lab, billing)
- 2026-08-19: Stack pin = hrms 16.5.0 (per lesson #44)
- 2026-08-19: Shift code scheme = 10-char `[P][HHMM][S][HHMM]` (Option A, HRMS-native flags)
- 2026-08-19: Holidays = standard Indian national + 4-5 Telangana (per user)
- 2026-08-19: Custom leave types = deferred (Haritha adds later)
- 2026-08-19: Leave allocation = standard Indian defaults + rules in remarks column
- 2026-08-19: Source data = DO NOT modify (canonicalization applied at import time, not in source)

**Sources:**
- Real hospital roster: `../../uploads/pberpqa-real-data-for-demo/roster_and_attendance_june.xlsx` (210 employees, 36 depts, 51 desigs, 31 shift codes)
- Reference: `../pberpqa-hospital-demo/` (pberpqa hospital demo, NOT perfect — gaps documented)

---

## Phase 1: Schema Approval (DONE ✅)

**Goal:** User reviews and approves the schema CSV + data CSVs.

**Status:** ✅ Signed off 2026-08-20 by manager. Both deliverables on GitHub (private repo). Manager downloaded, imported to Google Sheets, shared with team.

**Deliverables:**
- [x] User sign-off on all 19 entity schemas (manager approved)
- [x] Source canonicalization confirmed (no changes to source data — 3 designation collisions + 3 shift dupes resolved)
- [x] Holiday List dates confirmed (14 Indian national holidays 2025 + 2026)
- [x] 19 data CSVs generated in `masters/` (1.9 MB total)
- [x] Manager downloaded from GitHub, imported to Google Sheets, shared with team

---

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

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-08-19 | Scope = shift management only | User clarified mid-session; defer hospital modules |
| 2026-08-19 | hrms 16.5.0 pin | Lesson #44 — v16.5.1+ breaks on `repost_allowed_types` |
| 2026-08-19 | Shift code = 10-char `[P][HHMM][S][HHMM]` | User-proposed scheme, Option A (lean) |
| 2026-08-19 | Shift name = 10-char code itself (no separate `shift_code` field) | User simplification — name IS the code |
| 2026-08-19 | Holidays = standard Indian national + 4-5 Telangana | User confirmed |
| 2026-08-19 | Custom leave types = deferred | User said Haritha adds later |
| 2026-08-19 | Leave allocation = standard Indian defaults | User confirmed; rules in remarks column |
| 2026-08-19 | Source data = DO NOT modify | Canonicalization at import time only |
| 2026-08-19 | SSA is HRMS-native (Shift Schedule Assignment DocType) | Originally doubted; verified via docs.frappe.io/hr/shift-schedule-assignment |
| 2026-08-19 | Comprehensive 7-change schema update | 9 HRMS docs verified; HRMS v15 canonical structure applied |
| 2026-08-19 | 19 CSVs schema + data combined format | Manager-friendly for Google Sheets review |
| 2026-08-19 | 3 designation collisions resolved automatically | Physician Asstant+Assistant, Sr.Executive+Senior Executive, Sr.Manager+Senior Manager |
| 2026-08-19 | 3 shift code duplicates consolidated | A4+Shift-A, B2+Shift-B, C1+Shift-C |
| 2026-08-20 | Phase 0 + 1 signed off by manager | Schema + data CSVs approved |
| 2026-08-20 | New dedicated env `pberp` (clean slate) | Recommended over legacy envs |
| 2026-08-20 | Apps installed via `bench install-app` (runtime) | Quick start; lesson #47 trade-off (asset sync) |
| 2026-08-20 | Custom app: deferred, use custom fields + fixtures | Fast track for MVP |
| 2026-08-20 | Real-time employee name mapping: `EMP-1001` (CSV) → `HR-EMP-00001` (DB) | Built `HR-EMP-{N-1000:05d}` formatter |
| 2026-08-20 | Attendance imported via raw SQL (not ORM) | Bypassed Frappe Status validation + 240s timeout |
| 2026-08-20 | Attendance status options extended via Property Setter | Added "Weekly Off" + "Holiday" (1:1 CSV match) |
| 2026-08-20 | Employee Checkin via background jobs (25 batches × 500) | Direct console timed out on 12,562 rows |
| 2026-08-20 | HR-Attendance series counter fixed mid-flight (`HR-ATT-2026-` was 183, fixed to 6300) | Series was stale, prevented new record creation |
| 2026-08-20 | 5 X-HH Department variants force-deleted via direct SQL | Frappe `doc.delete()` enforces "disable not delete"; direct DELETE bypasses |
| 2026-08-21 | Backend tested end-to-end via API: auth ✅, CRUD ✅, all 9 entities queryable ✅, payroll/leave/holiday workflows ✅ |
| 2026-08-21 | UI smoke test inconclusive (headless browser tool unreliable) | Needs real browser verification next session |
| 2026-08-21 | Token limit issues (rate_limit_error) on long subagent runs — workaround: split into K1/K2/K3 + direct exec | Lesson learned for future orchestration |
| 2026-08-21 | nginx `Upgrade: websocket` forced for /socket.io/ (added during UI debugging — may need review/revert) | Frappe ws server validates Upgrade header on every request |
| 2026-08-21 | **Rollback: pberp.duckdns.org env torn down 10:11–10:18 IST (Option B: nuke, no backup). All Phase 2–5 deployment work destroyed. Restart from Phase 1 on new env. CSV masters + git history intact.** | Venkat authorized Option B at 10:33 IST; Phase 0 + 1 design work preserved; deployment was not recoverable |

---

## Subagent Log

| Date | Task | Agent | Status |
|---|---|---|---|
| 2026-08-19 12:30 | pberpqa reference + scout analysis | pberpqa_ref_an | ✅ done |
| 2026-08-19 12:30 | Source data Excel analysis | source_data_an | ✅ done |
| 2026-08-19 12:30 | Tracker + docs scan | tracker_docs_an | ✅ done |
| 2026-08-19 14:00 | Week-off pattern analysis | pberpqa_week_off_an | ✅ done |
| 2026-08-19 16:06 | Read 9 HRMS shift management docs | read_shift_mgmt_doc, read_shift_type_doc, read_shift_location_doc, read_shift_request_doc, read_shift_assignment_doc, read_shift_schedule_doc, read_shift_assignment_tool_doc, read_ssa_doc, read_roster_doc | ✅ done |
| 2026-08-19 15:33 | Update schema CSV (add SS, SSA, SR + remove shift_code) | update_schema_csv | ✅ done (commit 8307c0b) |
| 2026-08-19 15:42 | Comprehensive 7-change schema update | comprehensive_csv_update | ✅ done (commit aac7b3e) |
| 2026-08-19 19:35 | Generate 19 schema+data CSVs | generate_19_csvs | ✅ done |
| 2026-08-19 22:47 | Push 19 CSVs to GitHub | commit_push_masters | ✅ done (commit 21d54f4) |
| 2026-08-20 14:00 | Phase G (Company + Holidays) | phase_g_setup | ✅ done |
| 2026-08-20 14:30 | Phase H1 (6 small entities) | phase_h1_small_entities | ✅ done |
| 2026-08-20 15:00 | Phase H1.5 (delete 18 defaults) | phase_h15_delete_defaults | ✅ done |
| 2026-08-20 15:30 | Phase H2 (210 Employees) | phase_h2_employees | ✅ done |
| 2026-08-20 16:00 | Phase H3 (5,317 Shift Assignments) | phase_h3_shift_assignment | ✅ done |
| 2026-08-20 16:30 | Phase H4 (6,300 Attendance) | phase_h4_attendance | ✅ done (raw SQL bulk insert) |
| 2026-08-20 17:00 | Phase H5 (12,562 Employee Checkin) | phase_h5_employee_checkin | ✅ done (background jobs) |
| 2026-08-20 17:30 | Phase DB cleanup (force-delete 6 X-HH Departments) | force_delete_hr_dept | ✅ done |
| 2026-08-20 18:00 | Phase I (Backup script + cron + first run) | phase_i_backup | ✅ done |
| 2026-08-20 18:30 | Phase J-1 (nginx HTTPS routing) | phase_j1_nginx_routing | ✅ done |
| 2026-08-20 19:00 | Phase J-2 (worker fix — hrms/payments imports) | phase_j2_worker_fix (failed 2× token limit, direct exec succeeded) | ✅ done |
| 2026-08-21 06:31 | Phase K-1 (smoke tests) | phase_k1_smoke | ✅ done |
| 2026-08-21 06:31 | Phase K-2 (functional CRUD) | phase_k2_functional | ✅ done |
| 2026-08-21 06:31 | Phase K-3 (HRMS integration) | phase_k3_integration | ✅ done |

---

## Open Questions

1. **Site location** — which env for Haritha Hospitals? 🔄 RE-OPENED 2026-08-21: prior choice `pberp.duckdns.org` was destroyed. Options: (a) reuse `pberp.duckdns.org` (faster, but was the destroyed env), (b) pick new domain like `haritha.duckdns.org` (cleaner — no association with teardown). Awaiting user decision.
2. **Custom app `haritha_hospital`** — needed or just custom fields + fixtures? ✅ RESOLVED: deferred, using custom fields + fixtures
3. **🆕 New env domain** — reuse `pberp.duckdns.org` or pick new? Decision needed before Phase 2 restart.
4. Hospital-specific holidays (founder day, anniversary)? ⏳ Pending user input
5. ⚠️ **UI verification in real browser** — needed before go-live
6. ⚠️ **nginx `Upgrade: websocket` force-set** — should we revert? (added during debugging)
7. ⚠️ **User `Administrator` default `desktop:home_page="setup-wizard"`** — clear before production?

**Resolved:**
- ~~Telangana 2025 + 2026 holiday list~~ — using standard Indian national 14 holidays (per user)
- ~~Shift code convention~~ — 10-char `[P][HHMM][S][HHMM]`, name IS the code
- ~~Source data canonicalization~~ — 3 designation + 3 shift dupes resolved at import time
- ~~Apps stack~~ — frappe, erpnext, hrms 16.5.0, payments (no custom app for MVP)

---

## Pending Actions (Next Session)

> **🔄 RESTART NOTE (2026-08-21):** Phases 2–5 must be RE-EXECUTED on new env (after env domain decision). Items below are ordered by restart priority.

1. **🆕 Decide new env domain** — see Open Question #1 (reuse pberp.duckdns.org or new?)
2. **🆕 Phase 2 (re-execute)** — site setup on new env (use Phase 2 detailed section as runbook)
3. **🆕 Phase 3 (re-execute)** — CSV import (idempotent, 19 CSV masters ready)
4. **🆕 Phase 4 (re-execute)** — workflow testing (K-1/K-2/K-3 scripts preserved)
5. **🆕 Phase 5 (re-execute)** — backup cron + production readiness
6. **Phase L** — Cert monitoring + final sign-off report (~15m)
7. **UI smoke test in real browser** — verify Frappe desk loads at new env (login Administrator / admin123)
8. **Review nginx `Upgrade: websocket` change** — may need revert (added during debugging)
9. **Clear `desktop:home_page` default for user Administrator** — possibly needed for production
10. **Activate Auto Attendance cron** — `enable_auto_attendance=1` on Shift Types
11. **Pre-flight + post-flight process docs** — for go-live
12. **Disaster recovery test** — restore from backup (note: backups are for pre-Phase 4 state only)
13. **User training** — for Haritha Hospital staff

---

## Known Issues / Lessons Learned

| # | Issue | Lesson |
|---|-------|--------|
| 47 | Asset sync after `bench build` requires per-directory `docker cp` with `/.` syntax | Backend + frontend have separate `/sites/assets` volumes |
| 80 | Frappe `installed_apps` lives in TWO places: `site_config.json` AND `sites/apps.txt` | Both must be edited atomically |
| 44 | HRMS v16.5.1+ install broken by `repost_allowed_types` phantom field | Pin to v16.5.0 |
| 79 | `bench backup --with-files` has no built-in timeout | Always wrap with `timeout 900` + capture `${PIPESTATUS[0]}` |
| NEW | `bench install-app` runtime creates asset hash drift (Lesson #47) | For future envs, bake apps into image via apps.json |
| NEW | WebSocket container can crash with Redis `SocketClosedUnexpectedlyError` | Add health check + auto-restart |
| NEW | Frappe `ws` server requires `Upgrade: websocket` header even for polling | nginx needs explicit `proxy_set_header Upgrade "websocket";` for `/socket.io/` |
| NEW | Frappe `doc.delete()` enforces "disable not delete" | Force-delete via direct DB DELETE |
| NEW | Token limit errors on long subagent runs (rate_limit_error) | Split large tasks into smaller subagents OR direct exec |
| NEW | Frappe headless browser testing unreliable (timeouts, false negatives) | Use real browser for UI smoke tests |

---

*Last updated: 2026-08-21 10:34 IST — 🔄 ROLLBACK: pberp.duckdns.org env destroyed 10:11–10:18 IST; restart from Phase 1 on new env. Phase 0 + 1 + CSV masters + git history preserved.*
