# Haritha Hospitals — Comprehensive Guide

> **Audience:** Processbricks team (Venkat + downstream devs) and any operator touching the Haritha Hospitals ERPNext stack.
> **Scope:** End-to-end reference for the Haritha Hospitals deployment — architecture, customizations, migration, ops, and lessons.
> **Last updated:** 2026-08-29 (post custom-app build + master data migration + P1 outage recovery).

---

## Table of Contents

1. [Overview](#1-overview)
2. [Tech Stack](#2-tech-stack)
3. [Architecture](#3-architecture)
4. [Phase History](#4-phase-history)
5. [Customizations Catalog (274)](#5-customizations-catalog-274)
6. [Migration Guide](#6-migration-guide-how-to-replicate)
7. [Operational Runbook](#7-operational-runbook)
8. [Open Issues / Phase 6 Backlog](#8-open-issues--phase-6-backlog)
9. [References](#9-references)
10. [Appendix A — Master Data State](#appendix-a--master-data-state-as-of-2026-08-29)
11. [Appendix B — Incident Timeline (2026-08-29)](#appendix-b--incident-timeline-p1-outage-2026-08-29)

---

## 1. Overview

| Field | Value |
|---|---|
| Project | Haritha Hospitals ERPNext deployment |
| Company | Haritha Hospitals (healthcare / hospital group) |
| Industry | Hospital shift management + HRMS |
| Owner | Venkat Narasimha (Processbricks) |
| Started | 2026-04-01 (concept); project on this repo: 2026-08-19 |
| Stack | Frappe 16 / ERPNext 16 / HRMS 16.5.0 (pinned) / custom app `haritha_hospital` |
| Sites | `pberpprod.duckdns.org` (prod), `pberpdev.duckdns.org` (dev), `dev-erp.duckdns.org` (Venkat VPS for prototyping) |
| Last major milestone | 2026-08-29 — custom app build + master data migration + P1 outage recovery |

**Goal:** Stand up Haritha Hospitals as a real hospital shift-management system backed by ERPNext + HRMS, capturing all customizations as a portable Frappe custom app so any env can be reproduced with `bench install-app haritha_hospital`.

**Out of scope (deferred):** Wards, beds, OTs, pharmacy, lab, billing, full Chart of Accounts, cost centers beyond the 2 already created. Haritha adds these modules incrementally once shift + HRMS is validated.

---

## 2. Tech Stack

### Core Apps (4)
| App | Version | Notes |
|---|---|---|
| Frappe | v16.30.0 (pinned per compose) | Foundation framework |
| ERPNext | v16.30.0 | Accounting, inventory, selling, buying |
| HRMS | v16.5.0 (pinned, see LEARNINGS #44) | HR, payroll, shift, attendance, leave. **v16.5.1+ breaks on `repost_allowed_types`** — never upgrade without testing on dev first. |
| Custom app | `haritha_hospital` (0.0.1) | Owns 274 customizations as fixtures |

### Infrastructure
- **MariaDB** 10.x via Docker named volumes
- **Docker Compose** (compose-based deployment; `erp-{env}-*` containers on main VPS, `erpdev-*` on Venkat VPS)
- **Redis** (cache + queue broker) + **Socket.IO** for realtime desk
- **nginx-proxy** reverse proxy with TLS termination (DuckDNS + Let's Encrypt / self-signed fallback)
- **Custom Python 3.11** (Frappe v16 baseline)

### Custom App: `haritha_hospital`
- **Repo:** `git@github.com:venkat-narasimha/haritha_hospital.git`
- **Branch:** `main`
- **Layout:** Standard Frappe app — git-root with inner Python module dir (`apps/haritha_hospital/haritha_hospital/`)
- **Captures:** 274 customizations as JSON fixtures (78 Custom Field + 189 Property Setter + 3 Print Format + 2 Notification + 2 Letter Head)
- **Hooks:** `fixtures = [...]` block lists 5 DocTypes (see [HARITHA_HOSPITALS_GUIDE §5](#5-customizations-catalog-274))

### Source Repos
- **App:** https://github.com/venkat-narasimha/haritha_hospital
- **Workspace / docs / scripts:** https://github.com/venkat-narasimha/haritha_hospitals (this repo)
- **Memory / lessons (separate, not in this repo):** `/root/.openclaw/workspace/MEMORY.md` + `/root/.openclaw/workspace/.learnings/LEARNINGS.md`

---

## 3. Architecture

### 3.1 Environment Layout

| Env | URL | Compose Project | Containers | DB Name | Purpose |
|---|---|---|---|---|---|
| **pberpprod** | `https://pberpprod.duckdns.org/` | `erp-prod` | 9 (backend, frontend, scheduler, queue-short, queue-long, websocket, redis-cache, redis-queue, db) | `_b80f05e76a0dcaad` | Production. Customizations + 8,118 Shift Assignments. |
| **pberpdev** | `https://pberpdev.duckdns.org/` | `erp-dev` | 9 (same layout) | `_0c0679ad719b9491` | Development. Mirror of prod customizations + master data. |
| **dev-erp** | `https://dev-erp.duckdns.org/` | `erpdev` | 9 (different prefix `erpdev-*`) | `_f042e7eabf48bf86` | Venkat VPS prototyping. v15 HRMS, separate stack. |

QA env (`pberpqa.duckdns.org`) exists but **skipped for Haritha** per Venkat 2026-08-28 — direct dev → prod promotion with custom-app fixtures as the safety net.

### 3.2 Customization Capture

```
┌──────────────────────────────────────────────────────────────┐
│ pberpprod DB                                                 │
│  - 274 customizations (CF + PS + PF + N + LH)                │
│  - 8,118 Shift Assignments + 6,300 Attendance                │
│  - 210 Employees + 25 Shift Types + ...                      │
└──────────────────────────────────────────────────────────────┘
                          │
                          │ bench export-fixtures
                          │ (requires fixtures = [...] in hooks.py)
                          ▼
┌──────────────────────────────────────────────────────────────┐
│ haritha_hospital app                                         │
│  apps/haritha_hospital/haritha_hospital/                     │
│    fixtures/                                                 │
│      custom_field.json (78 rows)                             │
│      property_setter.json (189 rows)                         │
│      print_format.json (3 rows)                              │
│      notification.json (2 rows)                              │
│      letter_head.json (2 rows)                               │
│    hooks.py ← fixtures = [...] declaration                   │
└──────────────────────────────────────────────────────────────┘
                          │
                          │ git push → GitHub
                          │ bench install-app haritha_hospital
                          │ bench --site <env> migrate
                          ▼
┌──────────────────────────────────────────────────────────────┐
│ Any new env                                                  │
│  Same 274 customizations, env-portable, idempotent           │
└──────────────────────────────────────────────────────────────┘
```

### 3.3 Master Data Layer

Master data (Company, Employee, Department, Shift Type, etc.) is **NOT in fixtures**. Rationale:
- Master data is environment-specific (test fixtures would clutter prod)
- Master data drifts frequently (new hires, terminations) — fixtures would force re-export churn
- Migration is a one-shot operation per env, not a continuous sync

Master data lives in the DB; CSV sources in `projects/haritha-hospitals/masters/` (19 files, ~1.77 MB) act as the canonical reference. Migration script: `scripts/migrate_master_data.py` (idempotent).

### 3.4 Persistence Model

| Volume | Container | Content | Recovery on `restart` |
|---|---|---|---|
| `erp-{env}_sites` | backend, frontend, scheduler, workers | `/home/frappe/frappe-bench/sites/` (site_config.json, apps.txt, assets, private files) | ✅ preserved |
| `erp-{env}_db-data` | db only | `/var/lib/mysql/` (MariaDB data dir) | ✅ preserved |
| `erp-{env}_redis-cache-data` | redis-cache | cache snapshots | ✅ preserved |
| `erp-{env}_redis-queue-data` | redis-queue | background job queue | ✅ preserved |
| Anonymous (writable layer) | any | runtime writes (logs, tmp) | ⚠️ ephemeral |

**Rule of thumb:** anything in `/home/frappe/frappe-bench/` is on a named volume. `docker restart` is 100% safe; `docker-compose down -v` is data loss.

---

## 4. Phase History

### Phase 0 — Schema Planning (2026-04-01 to 2026-08-19)
**Goal:** Document schema for all master data entities needed for shift management.

**Status:** ✅ Complete. 19 entities, 168 fields. HRMS v15 verification done (9 docs read, 7 corrections applied).

**Deliverables:**
- `all_schemas.csv` — 19 entities, 168 fields
- `TRACKER.md` — this repo's tracker
- `README.md` — project overview
- `knowledge/shift_management_hrms.md` — reusable reference

**Decisions:**
- 2026-04-01: Scope = shift management only (defer wards, beds, OTs, pharmacy, lab, billing)
- 2026-04-15: HRMS v16.5.0 pin (Lesson #44)
- 2026-08-19: Shift code = 10-char `[P][HHMM][S][HHMM]` (HRMS-native flags)
- 2026-08-19: Holidays = standard Indian national + 4-5 Telangana

### Phase 1 — Schema Approval (2026-08-20)
**Goal:** Manager sign-off on schema + 19 data CSVs.

**Status:** ✅ Done. Both deliverables on GitHub (private repo). Manager downloaded, imported to Google Sheets, shared with team.

### Phase 1.5 — CSV Master Re-Verification (2026-08-25)
**Goal:** Validate 19 CSV masters before ingestion.

**Status:** ✅ Complete. All 7 checks PASS. 0 FAILs, 0 WARNs. 24,758 rows across 19 entities.

**Findings (MEMORY candidates):**
- Actual shift code format = `[GMAN]\d{4}[RS]\d{4}` (10-char) — MEMORY decision was wrong (said `[P][HHMM][S][HHMM]`)
- `employee.csv` has NO `name` column — FK join key = `attendance_device_id` (EMP-NNNN)
- Verify script format assumption: `## Data` marker + header + data rows; use `csv.DictReader` on header slice

### Phase 2 — Site Setup (2026-08-25, after 2026-08-21 rollback)
**Goal:** Spin up Haritha Hospitals on `pberpprod.duckdns.org` with clean state.

**Status:** ✅ Done. Pre-flight backup + wipe + reinit executed.

**Apps installed:** frappe, erpnext, hrms 16.5.0 (pinned), payments. Custom app **deferred** initially.

### Phase 3 — Data Import (2026-08-26)
**Goal:** Load 19 CSV masters into prod.

**Final tally:** 24,511 records across 9 entities (Company, Holiday, Department, Designation, Employment Type, Shift Type, Employee, Shift Assignment, Attendance, Employee Checkin).

**Key gotchas:**
- Employee PK = `HR-EMP-NNNNN` (autoname), not CSV `EMP-NNNN`. Map via `employee_number`.
- Attendance status extended with 'Holiday' + 'Weekly Off' via Property Setter
- Synthetic data: defaults for gender (Not Specified), date_of_birth (1990-01-01), first_name (split from employee_name)
- 5 X-HH Department variants force-deleted via direct SQL (Frappe `doc.delete()` enforces disable-not-delete)
- HR-Attendance series counter fixed mid-flight (was 183, fixed to 6300)

### Phase 3.5 — Reconcile + SS/SSA/SR Synthesis (2026-08-26)
**Status:** ✅ Done. All 11 entities match CSV targets after dedup + re-ingest.

- Department: 47 → 37 (36 CSV + 'All Departments' root)
- Designation: 76 → 48
- Leave Type: 9 → 7
- Employment Type: 8 → 6 (merged CSV-added with 3 defaults)
- Holiday: 28 → 14
- Shift Location: 1 → 0 (deleted bogus '(no rows)' literal)
- SS/SSA/SR synthesized to fill Phase 3 deferral gap

### Phase 3.6 — Bulk Submit (2026-08-27)
**Status:** ✅ Done. 6,314 docs at docstatus=0 now docstatus=1.

3 runs needed due to 3-layer Frappe framework barriers (LEARNINGS #106):
1. Naming series backfill (raw SQL ingest missed `naming_series`)
2. Property Setter for Attendance status options (added 'Holiday' + 'Weekly Off')
3. Monkey-patch controller-level status check (HRMS Attendance.validate() has hardcoded 5-value list)

### Phase 3.7 — Property Setter Recreate Script (2026-08-27)
**Status:** ✅ Done. `scripts/recreate_property_setters.py` is idempotent.

Pattern: scripted recreate (Option 2) instead of fixtures, because HRMS' `hooks.py` doesn't list 'Property Setter' as a fixture (LEARNINGS #151). Mirrors `bulk_submit.py`'s `importlib.util.spec_from_file_location()` pattern.

### Phase 4 — Roster Crash Fix (2026-08-28)
**Issue:** HRMS Roster page returned 500 on pberpprod.

**Root cause:** CapitalCase color keys ('Blue') vs lowercase Tailwind palette ('blue') in `apps/hrms/roster/src/components/MonthViewTable.vue`. TypeScript color type was lowercase but data had CapitalCase.

**Fix:** Property Setters for Shift Type color options + default + lowercase color values across all 25 Shift Types (78 → 25 visible colors actually stored; 50 missing shifts regenerated with defaults).

**Lesson:** "Worked before" + "Works on other site" = data bug, not framework.

### Phase 4.10/4.11 — Roster Real Root Cause + Verification (2026-08-28)
Deep-dive verification via headless Chromium with auth cookie injection (CDP Network.setCookie). Confirmed Phase 4.10 was the correct fix; no new code change needed, just documentation + idempotent verification script.

**Lessons:** #147-#150 (minified Vue column positions, numeric vs string keys, CDP HttpOnly cookies, verification scripts).

### Custom App Build (2026-08-28)
**Goal:** Capture all customizations as Frappe fixtures for env portability.

Built `haritha_hospital` app, configured `hooks.py`, exported 274 customizations, installed on both pberpdev (fresh) + pberpprod (idempotent).

**Schema gotchas caught:**
- `module` column vs legacy `app` (LEARNINGS #152)
- `fixtures = [...]` declaration required (LEARNINGS #151)
- Letter Head has no `module` column (LEARNINGS #155)
- Stock Print Formats have `module=NULL` (LEARNINGS #156)

### Master Data Migration (2026-08-29)
16 DocTypes migrated from prod to dev. 8,118 Shift Assignments on dev (7,829 from prod + 289 pre-existing).

Migration script: `scripts/migrate_master_data.py` (idempotent, 16 DocTypes, 10 gotchas documented — LEARNINGS #157).

### P1 Outage — Both envs 500'd (2026-08-29 03:06 IST)
**Root cause:** Gunicorn `--preload` froze sys.path at container startup; today's haritha_hospital install added `.pth` but gunicorn didn't see it.

**Fix:** `docker restart erp-{dev,prod}-backend-1` after volume verify (Lesson #72). ~30-60s downtime each, zero data loss.

**Lesson:** Always restart backend container after `bench install-app` (LEARNINGS #153).

### Phase 5 — DEFERRED (2026-08-28, per Venkat)
DR test, error monitoring, security audit, SSL audit, UAT, perf baseline — all skipped.

### Phase 6 — TBD
ISO/CMM L5 docs originally planned after Phase 5. Awaiting Venkat.

---

## 5. Customizations Catalog (274)

### 5.1 Custom Fields (78)
Major DocTypes with new fields:

| DocType | New Fields |
|---|---|
| **Employee** | PAN, IFSC, bank account, Health Insurance Number, approvers (Leave Approver, Expense Approver, Shift Request Approver) |
| **Company** | Payroll cost center, default leave policy |
| **Attendance** | HRMS-specific status extensions, late entry/early exit flags |
| **Shift Type** | Color (Tailwind palette), HRMS workflow flags |
| **Shift Assignment** | Department link, custom status |
| **Leave Application** | Approval workflow tweaks |
| **Holiday List** | Telangana regional holidays |
| ... | (full list in `apps/haritha_hospital/haritha_hospital/fixtures/custom_field.json`) |

### 5.2 Property Setters (189)
Largest category. Dominant DocTypes:

| DocType | PS Count | Purpose |
|---|---|---|
| **HRMS** (Attendance, Shift Type, Shift Assignment, Employee, Leave Application) | ~120 | Status options, default values, mandatory toggles, field order |
| **ERPNext** (Company, Item, Customer, Supplier) | ~50 | Custom field visibility, validation rules |
| **Frappe core** (User, File, Communication) | ~19 | UI behavior tweaks |

### 5.3 Print Formats (3)
- Haritha Hospitals Payslip
- Haritha Hospitals Shift Card
- Haritha Hospitals Leave Application

### 5.4 Notifications (2)
- **DISABLED:** Shift assignment change notification
- **DISABLED:** Leave approval pending notification

### 5.5 Letter Heads (2)
- Haritha Hospitals (default for all docs)
- Haritha Hospitals - Confidential (for HR/Payroll)

### 5.6 Total = 78 + 189 + 3 + 2 + 2 = **274** ✅

---

## 6. Migration Guide (How to Replicate)

### 6.1 Setup New Env with Customizations

```bash
# 1. Spin up the env (compose-based)
cd /path/to/frappe_docker
docker compose -p erp-newenv up -d

# 2. Create site
docker exec erp-newenv-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench new-site newsitename --admin-password admin123 --mariadb-root-password <root>"

# 3. Install base apps
docker exec erp-newenv-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench --site newsitename install-app erpnext"
docker exec erp-newenv-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench --site newsitename install-app hrms --branch version-16"

# 4. Get haritha_hospital custom app
docker exec erp-newenv-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench get-app https://github.com/venkat-narasimha/haritha_hospital"

# 5. Install + restart (CRITICAL — see LEARNINGS #153)
docker exec erp-newenv-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench --site newsitename install-app haritha_hospital"
docker restart erp-newenv-backend-1

# 6. Verify count
docker exec erp-newenv-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench --site newsitename console < /tmp/verify_haritha.py"
# Expect: 78 CF + 189 PS + 3 PF + 2 N + 2 LH = 274
```

### 6.2 Migrate Master Data

Use `scripts/migrate_master_data.py` (idempotent, 16 DocTypes):

```bash
docker cp scripts/migrate_master_data.py erp-newenv-backend-1:/tmp/
docker exec erp-newenv-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench --site newsitename console < /tmp/run_migrate.py"
# where run_migrate.py imports + calls migrate_all()
```

### 6.3 Migration Gotchas (LEARNINGS #157)

1. `frappe.get_doc()` requires `doctype` key in payload
2. Company default accounts depend on Account existing first → 2-step insert + update
3. Account root nodes (`Accounts Receivable`, etc.) are system-managed → skip
4. Shift Type `autoname='prompt'` → set name explicitly
5. Department/Item Group root (`All Departments`) → skip
6. Employee missing Gender/Default Shift → migrate lookup data first
7. Employee ID remapping — prod IDs differ from dev IDs, look up by `employee_name`
8. Child tables stripped by REST API `fields=["*"]` — need explicit fetch
9. HRMS `validate_approver` for Shift Request → Department Approver must exist
10. `autoname='field.######'` requires Series pre-bump or Frappe renames

### 6.4 Pre-Flight Checklist Before Any Migration

```
[ ] Backup taken (4 files: DB, config, public, private)
[ ] Backup SHA256 verified
[ ] Source env custom app count = 274
[ ] Target env custom app count = 274 (after install-app)
[ ] Backend container restarted after install-app (LEARNINGS #153)
[ ] All named volumes intact (Lesson #72 verify)
[ ] Migration script dry-run passes
[ ] Reversal plan documented (drop + restore from backup)
```

---

## 7. Operational Runbook

### 7.1 Daily
- [ ] Verify cron backup slot (4×/day per env) — check offsite rsync success
- [ ] Read backup log tail (NOT just exit code — Lesson #114)
- [ ] Spot-check container health (`docker ps | grep erp-`)
- [ ] Monitor token burn (HEARTBEAT.md §7)

### 7.2 Weekly
- [ ] Verify all envs healthy (`/` returns 200 on prod + dev)
- [ ] Check git repo sync (`git status` clean + `origin/main` reachable)
- [ ] Review open lessons in `.learnings/` for new patterns

### 7.3 Monthly
- [ ] **Re-verify DB passwords against container env** (LEARNINGS #154):
      `for env in dev prod qa; do docker exec erp-${env}-db-1 printenv MYSQL_ROOT_PASSWORD; done`
- [ ] Audit MEMORY.md for stale hardcoded values
- [ ] Audit LEARNINGS.md for stale entries
- [ ] Test restore from backup (3-2-1 rule, Lesson #4)
- [ ] Review cron logs for partial failures

### 7.4 Per Change (Customization, Migration, Update)
- [ ] **Pre-flight checklist** (§6.4 above)
- [ ] Apply on dev first, verify, then prod
- [ ] After `bench install-app`: **`docker restart erp-{env}-backend-1`** (LEARNINGS #153)
- [ ] After any DB write: backup before + verify after (Lesson #72)
- [ ] Export new customizations to fixtures + commit + push (Rule #9)
- [ ] Update TRACKER.md + this guide

### 7.5 Incident Response: HTTP 500 on All Requests

If both/all envs suddenly return HTTP 500:

```
1. Check if recent `bench install-app` ran → likely gunicorn --preload issue (LEARNINGS #153)
2. Verify container uptime vs last install-app time
3. Volume verify (Lesson #72): docker inspect <container> | grep Mounts
4. If volume verify passes → docker restart erp-<env>-backend-1
5. If volume verify fails → STOP, do not restart, escalate
```

---

## 8. Open Issues / Phase 6 Backlog

### 8.1 Deferred from Today (2026-08-29)
- **Prod admin password recovery** — pberpprod login returned 401 post-restart; need to retrieve actual `ADMIN_PASSWORD` from container `.env` (MEMORY's `PUNJD5HMp5B0uWBkRqeo` literal also drifted)
- **HRMS version-check** in `haritha_hospital/__init__.py` — should enforce `hrms == 16.5.0` to prevent accidental upgrades
- **MEMORY.md / LEARNINGS.md audit** — Lesson #114 silent cron failure root cause still has 3 dropped backup lines from a previous regression

### 8.2 Phase 5 Items Still Skipped (per Venkat 2026-08-28)
- Disaster recovery test (restore from backup)
- Error monitoring (Sentry / Rollbar integration)
- Security audit (HTTPS headers, RBAC review, password policy)
- SSL audit (cert expiry monitoring)
- UAT (user acceptance testing with Haritha Hospital staff)
- Performance baseline (load test, response time SLAs)

### 8.3 Phase 6 Candidates (TBD with Venkat)
- ISO 9001 + 27001 documentation
- SOPs + process maps
- Audit trail configuration
- Manager walkthrough deck
- Customer pilot (Haritha Hospital staff training)

### 8.4 Out-of-Scope Reminder
Wards, beds, OTs, pharmacy, lab, billing, full Chart of Accounts — deferred per Phase 0 decision. Add incrementally after shift + HRMS validated end-to-end.

---

## 9. References

### Repos
- **App:** https://github.com/venkat-narasimha/haritha_hospital
- **Workspace / docs / scripts:** https://github.com/venkat-narasimha/haritha_hospitals (this repo)
- **OpenClaw workspace memory:** `git@github.com:venkat-narasimha/erpclaw.git`

### Frappe / ERPNext
- **ERPNext docs:** https://docs.frappe.io/
- **HRMS docs:** https://docs.frappe.io/hr/
- **Frappe framework:** https://frappeframework.com/docs/
- **Custom app tutorial:** https://frappeframework.com/docs/v14/user/en/tutorial

### Internal
- **MEMORY.md:** `/root/.openclaw/workspace/MEMORY.md` (workspace root, separate repo)
- **LEARNINGS.md:** `/root/.openclaw/workspace/.learnings/LEARNINGS.md` (workspace root, separate repo)
- **Daily logs:** `/root/.openclaw/workspace/memory/YYYY-MM-DD.md`
- **Tracker:** `TRACKER.md` (in this repo)
- **Decisions log:** `DECISIONS.md` (in this repo)
- **Master data CSVs:** `masters/` (19 files, 1.77 MB)
- **Migration script:** `scripts/migrate_master_data.py`
- **Property Setter recreate script:** `scripts/recreate_property_setters.py`
- **Tracker update script:** `scripts/update_tracker.py`
- **CSV verification script:** `scripts/verify_csvs.py`

### External
- **DuckDNS:** https://www.duckdns.org/ (dynamic DNS for `*.duckdns.org` subdomains)
- **Docker Compose:** https://docs.docker.com/compose/
- **MariaDB:** https://mariadb.com/kb/en/documentation/

---

## Appendix A — Master Data State (as of 2026-08-29)

| DocType | pberpprod count | pberpdev count | Source CSV |
|---|---|---|---|
| Company | 1 | 1 | `masters/company.csv` |
| Employee | 210 | 210 | `masters/employee.csv` |
| Department | 37 | 37 | `masters/department.csv` |
| Designation | 48 | 48 | `masters/designation.csv` |
| Account | 89 | 89 | (system defaults + 5 roots skipped) |
| Cost Center | 2 | 2 | (system + Haritha Hospitals) |
| Item Group | 6 | 6 | (system + Haritha) |
| UOM | 239 | 239 | (system + Haritha units) |
| Shift Type | 25 | 25 | `masters/shift_type.csv` |
| Holiday List | 1 | 1 | `masters/holiday_list.csv` |
| Holiday | 14 | 14 | `masters/holiday.csv` |
| Employment Type | 6 | 6 | `masters/employment_type.csv` |
| Gender | 1 (Not Specified) | 1 | (system) |
| Shift Schedule | 5 | 5 | (synthesized) |
| Shift Assignment | 5,318 | 8,118 | `masters/shift_assignment.csv` + migration script |
| Shift Request | 8 | 7 | (synthesized + 1 migration conflict) |
| Leave Type | 7 | 7 | `masters/leave_type.csv` |
| Attendance | 6,300 | 6,300 | `masters/attendance.csv` |
| Employee Checkin | 12,562 | 12,562 | `masters/employee_checkin.csv` |

---

## Appendix B — Incident Timeline (P1 Outage, 2026-08-29)

| Time (IST) | Event |
|---|---|
| ~03:00 | haritha_hospital install-app completed on both envs |
| 03:06 | Venkat reports: "both pberpdev and pberpprod are down - internal server error" |
| 03:07 | `haritha-diag-500` subagent spawned (premium Minimax) |
| 03:09 | Root cause confirmed: gunicorn `--preload` sys.path freeze |
| 03:11 | Venkat asks "will restart clear the data?" |
| 03:12 | `haritha-verify-volumes` subagent spawned |
| 03:18 | Volume verify PASSES — all data on named volumes, zero risk |
| 03:20 | Venkat confirms YES → restart sequence spawned |
| 03:21 | `docker restart erp-dev-backend-1` (30s) |
| 03:22 | dev curl verify: HTTP 200 ✅, login 200 ✅ |
| 03:23 | `docker restart erp-prod-backend-1` (30s) |
| 03:24 | prod curl verify: HTTP 200 ✅, login 401 ⚠️ (DB password drifted) |
| 03:30 | Incident closed; MEMORY.md DB password audit kicked off |
| 04:00 | All action items documented in `memory/2026-08-29.md` |

**Total downtime:** ~18 min (both envs combined).

**Total data loss:** zero.

**Root cause documented in:** LEARNINGS.md #153 (gunicorn preload), #154 (restart vs down).

**Action items completed today:** MEMORY.md DB password correction, LEARNINGS #151-#157 added, this guide created.

**Action items still open:** prod admin password recovery (401 incident), HRMS version-check in `haritha_hospital/__init__.py`, Phase 5 items (deferred per Venkat).

---

*Last updated: 2026-08-29 09:21 IST (post Phase 0+ — Foundation & Migration).*

*Generated as part of comprehensive doc update subagent task (2026-08-29). See `TRACKER.md` Phase 0+ section for chronological build-out.*
