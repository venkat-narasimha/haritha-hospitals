# Haritha Hospitals — Migration Guide

**Project:** haritha-hospitals
**Target:** pberpqa.duckdns.org (post 2026-08-21 rollback)
**Source data:** `masters/` (19 CSV files — canonical, idempotent)
**Git repo:** origin/main at `a0d1be9` (includes rollback event)
**Last updated:** 2026-08-21 11:40 IST
**Author:** Agent C (workflow+migration+audit subagent)

---

> 🔐 **Credentials notice:**
> All credentials in this guide are intentionally **placeholder** values.
> - `Administrator / <from site_config>` — your site's Administrator user (from `site_config.json`)
> - `<from ADMIN_PASSWORD env>` — ERPNext admin password from `.env` (`ADMIN_PASSWORD`)
> - `<from .env MYSQL_ROOT_PASSWORD>` — MariaDB root password from `.env` (`MYSQL_ROOT_PASSWORD`)
>
> **Never commit real credentials.** This repo uses placeholders throughout.

---

## 1. Goal

Redeploy Haritha Hospitals on pberpqa.duckdns.org (current env post-2026-08-21 rollback). The pberp.duckdns.org environment (9 containers) was destroyed at 10:11–10:18 IST. Company "Haritha Hospitals" was recreated on pberpqa at 10:59 IST. This guide covers the full redo of Phases 2-5 on the new environment.

---

## 2. Prerequisites

- ✅ pberpqa.duckdns.org running, HRMS 16.5.0 installed (pinned per Lesson #44)
- ✅ pberp_hospital custom app installed (already done)
- ✅ Haritha Hospitals company created (already done 10:59 IST on pberpqa)
- ✅ CSV masters in `masters/` (19 files — canonical source, idempotent)
- ✅ Git history at `origin/main` (includes rollback event at `a0d1be9`)
- ✅ VPS access: vijay@144.217.163.228 (for backup cron deployment)
- ✅ Offsite backup target: venkat@135.125.196.35

---

## 3. Steps

### Step 1: Phase 2 Redo — Site Setup

**Target:** pberpqa.duckdns.org (already has HRMS 16.5.0 + pberp_hospital app + Company)

```bash
# On VPS (vijay@144.217.163.228) - if using pberpqa compose project
docker compose -p pberpqa ps  # Verify 9 containers running

# Verify site exists and apps installed
bench --site pberpqa.duckdns.org list-apps
# Should show: frappe, erpnext, hrms (v16.5.0), payments, pberp_hospital

# Verify Company exists
bench --site pberpqa.duckdns.org console
# >>> frappe.get_doc("Company", "Haritha Hospitals")
```

**If site needs recreation:**
```bash
bench new-site pberpqa.duckdns.org \
  --admin-password "<from ADMIN_PASSWORD env>" \
  --mariadb-root-password "<from MYSQL_ROOT_PASSWORD env>" \
  --no-mariadb-socket

bench --site pberpqa.duckdns.org install-app erpnext
bench --site pberpqa.duckdns.org install-app hrms  # v16.5.0 pinned
bench --site pberpqa.duckdns.org install-app payments
bench --site pberpqa.duckdns.org install-app pberp_hospital  # custom app
```

**Custom fields fixtures** (already in pberp_hospital app):
```bash
bench --site pberpqa.duckdns.org migrate
# Fixtures auto-applied on migrate
```

**Holiday List** (if not already loaded):
```bash
bench --site pberpqa.duckdns.org execute haritha.utils.load_holidays
```

### Step 2: Phase 3 Redo — Data Import

Import all 19 CSV masters from `masters/` in dependency order. The CSVs are idempotent — re-running is safe.

```bash
# 1. Foundation entities (L1)
bench --site pberpqa.duckdns.org execute haritha.import.departments
bench --site pberpqa.duckdns.org execute haritha.import.employment_types
bench --site pberpqa.duckdns.org execute haritha.import.leave_types
bench --site pberpqa.duckdns.org execute haritha.import.designations

# 2. Shift Types (L2)
bench --site pberpqa.duckdns.org execute haritha.import.shift_types

# 3. Employees (210 records)
bench --site pberpqa.duckdns.org execute haritha.import.employees

# 4. ERPNext defaults cleanup (H1.5 + H1.5b)
bench --site pberpqa.duckdns.org execute haritha.cleanup.defaults

# 5. Shift Assignments (5,317 records) - background jobs
bench --site pberpqa.duckdns.org execute haritha.import.shift_assignments

# 6. Attendance (6,300 records) - raw SQL bulk insert
bench --site pberpqa.duckdns.org execute haritha.import.attendance

# 7. Employee Checkins (12,562 records) - 25 batches
bench --site pberpqa.duckdns.org execute haritha.import.employee_checkins

# 8. DB cleanup - force delete 5 X-HH Department variants
bench --site pberpqa.duckdns.org execute haritha.cleanup.xhh_departments
```

**Validation** (run after each step):
```bash
bench --site pberpqa.duckdns.org execute haritha.validate.counts
# Should match: Dept=36, Desig=48, EmpType=6, LeaveType=7, ShiftType=25, Emp=210, ShiftAssign=5317, Att=6300, Checkin=12562
```

### Step 3: Phase 4 Redo — Workflow Testing

```bash
# J-1: nginx config already in place on pberpqa
# Verify websocket proxy
curl -I https://pberpqa.duckdns.org/socket.io/
# Should return HTTP 200/101 with Upgrade header

# J-2: Worker fix verification
docker compose -p pberpqa exec queue-short python -c "import hrms; import payments; print('OK')"

# K-1: Smoke + functional tests
bench --site pberpqa.duckdns.org run-tests --module haritha.tests.test_smoke

# K-2: CRUD + payroll integration
bench --site pberpqa.duckdns.org run-tests --module haritha.tests.test_crud_payroll

# K-3: HRMS integration
bench --site pberpqa.duckdns.org run-tests --module haritha.tests.test_hrms_integration
```

**Expected results (from rollback verification):**
- K-1: PASS (auth, CRUD, entity counts)
- K-2: PASS (Shift Assignment CRUD, payroll integration)
- K-3: PASS (shift/leave/holiday/process_attendance)

**UI Smoke Test (manual required):**
1. Open https://pberpqa.duckdns.org in real browser (Chrome/Firefox)
2. Login as Administrator
3. Verify Desk loads (not stuck on splash)
4. Navigate to Shift Assignment list — verify 5,317 records
5. Create test Shift Assignment via UI
6. Verify Employee Checkin list loads

### Step 4: Phase 5 Redo — Production Readiness

```bash
# On VPS (vijay@144.217.163.228)
# Deploy backup script
mkdir -p /home/vijay/scripts /home/vijay/logs /home/vijay/backups

cat > /home/vijay/scripts/pberp_backup.sh << 'EOF'
#!/bin/bash
set -euo pipefail
TIMEOUT=900
BACKUP_DIR="/home/vijay/backups"
OFFSITE_HOST="venkat@135.125.196.35"
OFFSITE_DIR="/home/venkat/pberp_backups"
SITE="pberpqa.duckdns.org"

mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="pberpqa_backup_${TIMESTAMP}.tar.gz"

timeout $TIMEOUT bench --site "$SITE" backup --with-files \
  --backup-path "$BACKUP_DIR/$BACKUP_FILE"
BACKUP_EXIT=${PIPESTATUS[0]}

if [ $BACKUP_EXIT -eq 0 ]; then
    scp "$BACKUP_DIR/$BACKUP_FILE" "$OFFSITE_HOST:$OFFSITE_DIR/"
    find "$BACKUP_DIR" -name "pberpqa_backup_*.tar.gz" -mtime +14 -delete
    ssh "$OFFSITE_HOST" "find $OFFSITE_DIR -name 'pberpqa_backup_*.tar.gz' -mtime +30 -delete"
    echo "✅ Backup complete: $BACKUP_FILE"
else
    echo "❌ Backup failed with exit code $BACKUP_EXIT"
    exit 1
fi
EOF

chmod +x /home/vijay/scripts/pberp_backup.sh

# Test run
/home/vijay/scripts/pberp_backup.sh

# Install cron (every 6 hours)
(crontab -l 2>/dev/null; echo "0 */6 * * * /home/vijay/scripts/pberp_backup.sh >> /home/vijay/logs/pberp_backup.log 2>&1") | crontab -

# Verify cron
crontab -l
```

**Pre-flight checklist:**
- [ ] Backup cron test run successful + offsite copy verified on venkat VPS
- [ ] SSL certificates valid (expiry > 30 days) — check `certbot certificates`
- [ ] All 9 containers healthy (`docker compose -p pberpqa ps`)
- [ ] Database restore test on staging env (if available)
- [ ] Monitoring: uptime, disk, memory alerts configured
- [ ] Rate limiting on nginx (login, API endpoints)
- [ ] Admin password rotated from default
- [ ] `setup_complete=1` in System Settings
- [ ] `desktop:home_page` cleared for Administrator (or set to Desk)

**Post-flight checklist:**
- [ ] First 24h: monitor error logs, slow queries, queue backlogs
- [ ] Verify offsite backup arrives on venkat VPS
- [ ] Confirm Auto Attendance cron processes correctly
- [ ] Validate shift/attendance reports with real data
- [ ] Document any new lessons learned in TRACKER.md

---

## 4. Rollback

If migration fails and you need to return to pre-migration state:

### Option A: Restore from backup (preferred)
```bash
# On VPS
cd /home/vijay/backups
# Find latest backup
LATEST=$(ls -t pberpqa_backup_*.tar.gz | head -1)
bench --site pberpqa.duckdns.org restore "$LATEST" --force

# Offsite backup
scp venkat@135.125.196.35:/home/venkat/pberp_backups/pberpqa_backup_*.tar.gz /home/vijay/backups/
bench --site pberpqa.duckdns.org restore /home/vijay/backups/pberpqa_backup_*.tar.gz --force
```

### Option B: Destroy and recreate site (nuclear)
```bash
bench drop-site pberpqa.duckdns.org --force
# Then re-run Step 1 (Phase 2) from scratch
```

### Option C: Git revert (code only)
```bash
git revert a0d1be9  # Reverts rollback event commit
# Note: This only reverts code, not database state
```

---

## 5. Lessons Applied

References to LEARNINGS.md and TRACKER.md Known Issues section:

| Lesson # | Issue | Applied In Migration |
|----------|-------|---------------------|
| 44 | HRMS v16.5.1+ broken by `repost_allowed_types` | Pin HRMS to v16.5.0 in Step 1 |
| 47 | Asset sync requires `docker cp` with `/.` syntax | nginx asset routing in Phase 4 |
| 79 | `bench backup --with-files` needs `timeout` + `${PIPESTATUS[0]}` | Backup script in Step 4 |
| 80 | `installed_apps` in TWO places | Verified in Step 1 migrate |
| NEW | WebSocket Redis `SocketClosedUnexpectedlyError` | Health check + auto-restart in compose |
| NEW | Frappe `ws` needs `Upgrade: websocket` header | nginx config in Phase 4 J-1 |
| NEW | Force-delete via direct DB DELETE | X-HH Department cleanup in Step 2 |
| NEW | Headless browser unreliable | Manual browser test in Step 3 |

---

## 6. Quick Reference

```bash
# Full redo (single command sequence)
# Step 1: Site setup
bench --site pberpqa.duckdns.org migrate

# Step 2: Data import
bench --site pberpqa.duckdns.org execute haritha.import.all

# Step 3: Tests
bench --site pberpqa.duckdns.org run-tests --module haritha.tests

# Step 4: Backup
/home/vijay/scripts/pberp_backup.sh

# Verify counts
bench --site pberpqa.duckdns.org execute haritha.validate.counts
```

---

## 7. Support Files in Repo

| File | Purpose |
|------|---------|
| `masters/*.csv` | 19 canonical CSV sources |
| `fixtures/custom_field.json` | 14 custom fields (Rule #9) |
| `scripts/import_*.py` | Import scripts per entity |
| `scripts/cleanup_*.py` | Defaults + X-HH cleanup |
| `scripts/validate_counts.py` | Validation script |
| `tests/test_smoke.py` | K-1 tests |
| `tests/test_crud_payroll.py` | K-2 tests |
| `tests/test_hrms_integration.py` | K-3 tests |
| `TRACKER.md` | Phase log + Known Issues |
| `DECISIONS.md` | Architecture decisions |
| `LEARNINGS.md` | Consolidated lessons |
| `WORKFLOW.md` | This workflow (Phase 2-5 runbooks) |

---

*Generated 2026-08-21 11:40 IST — Haritha Hospitals Migration Guide v1.0*