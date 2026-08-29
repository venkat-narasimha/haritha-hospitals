# Haritha Hospitals — Workflow

**Project:** haritha-hospitals
**Target env:** pberp.duckdns.org (compose project `pberp` on main VPS vijay@144.217.163.228)
**Source data:** `masters/` (19 CSV files — canonical, idempotent)
**Git repo:** origin/main at `a0d1be9`
**Created:** 2026-08-21 11:40 IST
**Last updated:** 2026-08-21 11:40 IST

---

## Overview

This workflow describes the end-to-end process for deploying Haritha Hospitals on a fresh Frappe/ERPNext/HRMS environment. It is **document-first, git-tracked, gate-gated**: every phase produces a canonical artifact, every transition requires explicit operator approval, and the entire process is reproducible from this repo alone.

**Rollback context:** On 2026-08-21 10:11–10:18 IST, the pberp.duckdns.org environment (9 containers) was destroyed. All Phase 2-5 work was preserved in this repo (TRACKER.md, CSV masters, git history). The Company "Haritha Hospitals" was recreated at 10:59 IST on the new pberpqa env. This workflow covers re-execution of Phases 2-5 on the new environment.

---

## Phase 2 — Site Setup

> **Status: NEEDS REDO** — All Phase 2 work was destroyed in the 2026-08-21 rollback. Re-execute from scratch on new env.

### Goal
Create Haritha Hospitals site on a fresh environment with HRMS 16.5.0 pinned.

### Resolution (from TRACKER.md)
- ✅ **NEW dedicated env** (clean slate) — compose project `pberp` on main VPS (vijay@144.217.163.228)
- ✅ Skip custom app initially — use custom fields + fixtures for haritha-specific data
- ✅ Apps: frappe 16.x, erpnext 16.x, hrms 16.5.0 (pinned), payments

### Steps

#### A: Pre-flight checks + certificate fix
- Verify VPS connectivity (vijay@144.217.163.228)
- Ensure Docker + Docker Compose installed
- Fix SSL certificates for pberp.duckdns.org (Let's Encrypt / existing certs)
- Verify ports 80, 443, 9000 (websocket) accessible

#### B: Compose up — 9 containers
```bash
# On VPS: start the compose project
docker compose -p pberp up -d
```
Containers: backend, frontend, scheduler, queue-short, queue-long, websocket, redis-cache, redis-queue, db

#### C: Site creation — `pberp.duckdns.org`
```bash
bench new-site pberp.duckdns.org \
  --admin-password "<from ADMIN_PASSWORD env>" \
  --mariadb-root-password "<from MYSQL_ROOT_PASSWORD env>" \
  --no-mariadb-socket
```

#### D: Apps install
```bash
bench --site pberp.duckdns.org install-app erpnext
bench --site pberp.duckdns.org install-app hrms  # v16.5.0 pinned
bench --site pberp.duckdns.org install-app payments
```
**Critical:** Pin HRMS to v16.5.0 (Lesson #44: v16.5.1+ broken by `repost_allowed_types` phantom field)

#### E: Custom fields fixtures
- Apply haritha-specific custom fields via fixtures (not custom app)
- Fields target: Employee, Attendance, Shift Type, Department
- See `fixtures/custom_field.json` in repo

#### F: MySQL grants (db user permissions for scheduler IP)
```sql
GRANT ALL PRIVILEGES ON `pberp_duckdns_org`.* TO 'pberp_user'@'%';
FLUSH PRIVILEGES;
```
Ensure scheduler container IP can connect to MariaDB.

#### G: Company "Haritha Hospitals" + Holiday List
```bash
# Via bench console or UI
bench --site pberp.duckdns.org console
```
Create Company: "Haritha Hospitals" (INR, India, FY: Apr-Mar)
Load Holiday List for 2026 (India holidays + hospital-specific)

### Deliverables
- [ ] Site location: NEW env `pberp.duckdns.org` (compose project `pberp`)
- [ ] Apps installed: frappe, erpnext, hrms 16.5.0, payments
- [ ] Custom app: deferred (use custom fields + fixtures)
- [ ] Company "Haritha Hospitals" created (INR, India)
- [ ] Holidays loaded
- [ ] Pre-flight backup cron added (Phase I)

---

## Phase 3 — Data Import

> **Status: NEEDS REDO** — All 24,511 records imported into pberp.duckdns.org were destroyed in the env teardown. The 19 CSV masters in `masters/` are intact and idempotent — re-run Phase 3 on new env to recover.

### Goal
Load all master data from CSV into the site.

### Steps

#### H1: 6 small entities imported (124 records)
Import order (dependency-aware):
1. Department (36 records)
2. Employment Type (6 records)
3. Leave Type (7 records)
4. Designation (48 records)
5. Shift Type (25 records)
6. Employee (210 records: HR-EMP-00001 to HR-EMP-00210)

Use `bench --site pberp.duckdns.org execute` with import scripts or Data Import Tool.

#### H1.5 + H1.5b: ERPNext defaults cleanup
- Delete 18 ERPNext default records (leaves 10 → 5 X-HH variants remaining)
- Target: default Departments, Designations, Leave Types, etc.
- Use `bench --site pberp.duckdns.org execute` with cleanup script

#### H2: 210 Employees imported
CSV: `masters/employees.csv` → Employee doctype
Verify: 210 records (HR-EMP-00001 to HR-EMP-00210)

#### H3: 5,317 Shift Assignments imported
CSV: `masters/shift_assignments.csv` → Shift Assignment doctype
Formula: 210 employees × 25 shift types × 29 days = 5,317 (approx)
Background jobs recommended

#### H4: 6,300 Attendance records imported
CSV: `masters/attendance.csv` → Attendance doctype
Method: Raw SQL bulk insert (1:1 CSV match for performance)
```sql
-- Example pattern
INSERT INTO `tabAttendance` (...) VALUES (...), (...), ...;
```

#### H5: 12,562 Employee Checkin records imported
CSV: `masters/employee_checkins.csv` → Employee Checkin doctype
Method: Background jobs, 25 batches of ~500 records each
Use `enqueue` with queue-long worker

#### DB cleanup: 5 X-HH Department variants force-deleted
```sql
DELETE FROM `tabDepartment` WHERE name LIKE 'X-HH-%';
```
Direct SQL required (Frappe `doc.delete()` enforces "disable not delete" — Lesson learned)

### Deliverables
- [ ] L1 Foundation: Company ✅, FY ✅, Holiday List ✅, Departments ✅ (36), Designations ✅ (48), Employment Type ✅ (6)
- [ ] L2 Shift Management: Shift Types ✅ (25), Employees ✅ (210), Shift Assignments ✅ (5,317), Attendance ✅ (6,300), Leave Types ✅ (7)
- [ ] Custom Fields fixtures (Rule #9 compliance)
- [ ] Data validation (all 9 entities match CSV counts exactly)

**Final tally: 24,511 records across 9 entities.**

---

## Phase 4 — Workflow Testing

> **Status: NEEDS REDO** — All backend API testing (K-1, K-2, K-3 — PASS), nginx config, worker fixes, and websocket routing were destroyed with pberp.duckdns.org. Backend tests were PASS (verified via API) — scripts can be re-run on new env. UI smoke test was already inconclusive (headless browser unreliable).

### Goal
Test end-to-end shift management workflow.

### Steps

#### J-1: nginx HTTPS + security headers + routing config
- Configure TLSv1.2/1.3
- HSTS, CSP, rate limiting
- Route `/socket.io/` to websocket container (pberp-websocket-1:9000)
- Force `Upgrade: websocket` header for `/socket.io/` (Lesson: Frappe `ws` server requires it even for polling)

```nginx
# Key nginx config snippet
location /socket.io/ {
    proxy_pass http://pberp-websocket-1:9000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade "websocket";
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
}
```

#### J-2: Worker fix (hrms/payments/frappe/erpnext imports in queue workers)
- Ensure all apps' tasks are importable in queue workers
- Fix: install hrms, payments in worker containers or symlink apps
- Verify queue-short and queue-long process jobs without import errors

#### K-1: Smoke + functional tests (auth, CRUD, entity counts) — **PASS (re-runnable)**
```bash
# API test script pattern
bench --site pberp.duckdns.org run-tests --module haritha.tests.test_smoke
```
Tests: Authentication, CRUD on all 9 entities, entity count validation

#### K-2: Functional CRUD + payroll integration — **PASS (re-runnable)**
- Shift Assignment create/read/update/delete
- Payroll entry creation for test employees
- Salary slip generation validation

#### K-3: HRMS integration (shift/leave/holiday/process_attendance) — **PASS (re-runnable)**
- Shift Assignment workflow ✅
- Auto Attendance (cron ready, needs activation) ✅
- Manual Attendance ✅
- Leave Application + Allocation ✅
- Employee Checkin ✅
- Holiday List ✅

### UI Smoke Test (previously inconclusive)
- Site loads at https://pberp.duckdns.org ✅ (HTTP 200)
- Login form loads, API auth works ✅
- All asset bundles serve HTTP 200 ✅
- Socket.io proxy works ✅
- System Settings `setup_complete=1` set ✅
- **Issue:** Vue.js SPA mounts but stays on loading splash in headless browser
- **Action needed:** Manual browser verification (Lesson: headless browser unreliable)

### Outstanding Issues (from rollback)
- [ ] Auto Attendance cron activation — pending
- [ ] UI smoke test in real browser — pending
- [ ] nginx `Upgrade: websocket` header — verify if still needed
- [ ] User `Administrator` default `desktop:home_page=setup-wizard` — clear for production

### Deliverables
- [ ] Shift Assignment creation (via API) ✅
- [ ] Manual Attendance ✅
- [ ] Leave Application + Allocation ✅
- [ ] Employee Checkin ✅
- [ ] Reports (API tested, UI untested)
- [ ] Auto Attendance cron activation — pending
- [ ] UI smoke test in real browser — pending

---

## Phase 5 — Production Readiness

> **Status: NEEDS REDO** — Backup cron on vijay@144.217.163.228 (`/home/vijay/scripts/pberp_backup.sh`) was destroyed along with the env. The cron schedule (`0 */6 * * *`) and offsite push to venkat@135.125.196.35 will need to be recreated on new env. One backup file (`pberpprod_backup_20260821_000039.tar.gz`, 1.6 MB) exists on venkat VPS — covers pre-Phase 4 state.

### Goal
Audit and harden for production.

### Steps

#### I: Backup cron + first run + offsite to venkat VPS
```bash
# On VPS (vijay@144.217.163.228)
mkdir -p /home/vijay/scripts
cat > /home/vijay/scripts/pberp_backup.sh << 'EOF'
#!/bin/bash
set -euo pipefail
# Hardened backup script per Lesson #79
TIMEOUT=900
BACKUP_DIR="/home/vijay/backups"
OFFSITE_HOST="venkat@135.125.196.35"
OFFSITE_DIR="/home/venkat/pberp_backups"
SITE="pberp.duckdns.org"

mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="pberpprod_backup_${TIMESTAMP}.tar.gz"

# Run backup with timeout and capture exit code
timeout $TIMEOUT bench --site "$SITE" backup --with-files \
  --backup-path "$BACKUP_DIR/$BACKUP_FILE"
BACKUP_EXIT=${PIPESTATUS[0]}

if [ $BACKUP_EXIT -eq 0 ]; then
    # Offsite copy
    scp "$BACKUP_DIR/$BACKUP_FILE" "$OFFSITE_HOST:$OFFSITE_DIR/"
    # Retention: keep last 14 days locally, 30 days offsite
    find "$BACKUP_DIR" -name "pberpprod_backup_*.tar.gz" -mtime +14 -delete
    ssh "$OFFSITE_HOST" "find $OFFSITE_DIR -name 'pberpprod_backup_*.tar.gz' -mtime +30 -delete"
    echo "✅ Backup complete: $BACKUP_FILE"
else
    echo "❌ Backup failed with exit code $BACKUP_EXIT"
    exit 1
fi
EOF
chmod +x /home/vijay/scripts/pberp_backup.sh
```

#### Cron schedule
```bash
# Every 6 hours
0 */6 * * * /home/vijay/scripts/pberp_backup.sh >> /home/vijay/logs/pberp_backup.log 2>&1
```

#### Pre-flight checklist (before production traffic)
- [ ] Backup cron running and verified (test run + offsite copy confirmed)
- [ ] SSL certificates valid (expiry > 30 days)
- [ ] All 9 containers healthy (`docker compose -p pberp ps`)
- [ ] Database backups verified (restore test on staging)
- [ ] Monitoring: uptime, disk, memory alerts configured
- [ ] Rate limiting on nginx (login, API endpoints)
- [ ] Admin password rotated from default
- [ ] `setup_complete=1` in System Settings
- [ ] `desktop:home_page` cleared for Administrator

#### Post-flight checklist (after production traffic starts)
- [ ] First 24h: monitor error logs, slow queries, queue backlogs
- [ ] Verify offsite backup arrives on venkat VPS
- [ ] Confirm Auto Attendance cron processes correctly
- [ ] Validate shift/attendance reports with real data
- [ ] Document any new lessons learned

### Deliverables
- [ ] Backup script deployed and executable
- [ ] Cron scheduled (0 */6 * * *)
- [ ] First backup run successful + offsite copy verified
- [ ] Pre-flight checklist complete
- [ ] Post-flight monitoring active

---

## Gate Criteria

| Phase | Gate | Criteria |
|-------|------|----------|
| 2 → 3 | Site ready | Site accessible, apps installed, company created, holidays loaded |
| 3 → 4 | Data imported | All 24,511 records match CSV counts exactly |
| 4 → 5 | Tests pass | K-1, K-2, K-3 all PASS; Auto Attendance cron ready |
| 5 → PROD | Hardened | Backup cron running, offsite verified, pre-flight ✅ |

---

## Lessons Learned Applied (from TRACKER.md)

| # | Lesson | Applied In |
|---|--------|------------|
| 44 | Pin HRMS to v16.5.0 | Phase 2 Step D |
| 47 | Asset sync requires `docker cp` with `/.` syntax | Phase 4 J-1 (nginx asset routing) |
| 79 | `bench backup --with-files` needs `timeout` + `${PIPESTATUS[0]}` | Phase 5 Step I |
| 80 | `installed_apps` in TWO places: `site_config.json` AND `sites/apps.txt` | Phase 2 Step C/D |
| NEW | WebSocket Redis `SocketClosedUnexpectedlyError` | Phase 4 J-1 (health check + restart) |
| NEW | Frappe `ws` needs `Upgrade: websocket` header | Phase 4 J-1 (nginx config) |
| NEW | Force-delete via direct DB DELETE | Phase 3 DB cleanup |
| NEW | Headless browser unreliable for UI tests | Phase 4 (manual browser verification) |

---

## Quick Reference Commands

```bash
# Site console
bench --site pberp.duckdns.org console

# Run backup manually
/home/vijay/scripts/pberp_backup.sh

# Check container health
docker compose -p pberp ps

# View logs
docker compose -p pberp logs -f backend
docker compose -p pberp logs -f websocket

# Queue status
bench --site pberp.duckdns.org doctor
bench --site pberp.duckdns.org show-config
```