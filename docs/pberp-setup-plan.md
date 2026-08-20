# Phase 2 Setup Plan: pberp.duckdns.org for Haritha Hospitals

**Created:** 2026-08-20 14:46 IST (revised 15:46 IST per user decision)
**Owner:** Venkat (Processbricks)
**Target:** New Frappe site at `pberp.duckdns.org`
**Compose project name:** `pberp`
**Stack:** Frappe 16.x + ERPNext 16.x + HRMS **16.5.0 pinned** (Lesson #44) + payments
**Estimated time:** 5-7 hours total (simplified from custom image build approach)

---

## Approach: Vanilla image + runtime app install (per user preference)

User chose NOT to build a custom Docker image. Use the vanilla `frappe/erpnext:v16` image. Install apps at runtime via `bench get-app` + `bench install-app`.

**Workflow:**
1. Use vanilla image: `frappe/erpnext:v16` (or specific version)
2. Create site (no app install)
3. `bench get-app` + `bench install-app` for each app

**Trade-off:** Simpler setup (no docker build), but apps are installed at runtime rather than baked into the image. For production, custom image builds are preferred (frappe_docker canonical). For this project, vanilla image is acceptable per user.

**HRMS pin:** Use `--branch version-15` per Lesson #44 (v16.5.0). Even on vanilla image, this pin is enforced.

---

## Summary

| Phase | What | Time | Status |
|-------|------|------|--------|
| A | Pre-flight (DNS, SSL, dirs) | 30m | pending |
| B | Compose up (vanilla image) | 30m | pending |
| C | Site creation (no app install) | 15m | pending |
| D | Get apps + install + restart workers | 30m | pending |
| E | Custom fields fixtures (7 fields) | 30m | pending |
| F | MySQL grants for scheduler (Lesson #87) | 5m | pending |
| G | Company + Holiday List | 15m | pending |
| H | Data import (19 CSVs) | 60m | pending |
| I | Backup setup (hardened prod_backup.sh pattern) | 30m | pending |
| J | nginx routing (real path fix) | 30m | pending |
| K | Test + Sign-off (100% green + delete + report) | 3-4h | pending |
| L | Cert expiry monitoring | 15m | pending |

---

## 7 User Decisions (FINAL)

1. Compose project name: **`pberp`**
2. HRMS pin: **16.5.0** (Lesson #44 — `--branch version-15` enforced even on vanilla image)
3. Ports: NO host ports published (match existing erp-dev/qa/prod convention; Docker DNS only)
4. Leave Allocation (1,470 rows): DEFER — HRMS auto-allocates on first Leave Application
5. nginx config: REAL path is `/home/vijay/nginx-erp.conf` (single-file bind-mount to container `/etc/nginx/conf.d/erp.conf`)
6. Backup: match existing (cron `0 */6 * * *`, `KEEP_DAYS=7` local, offsite to `venkat@135.125.196.35` retains forever)
7. Test gating: 100% green vendor tests REQUIRED for sign-off → delete all test data → generate sign-off report

## 7 Custom Fields (Rule #9: must be in fixtures, NEVER dialog-added)

| Entity | Field | Type |
|---|---|---|
| Shift Type | is_oncall | Check |
| Shift Type | is_emergency | Check |
| Employee | is_synthetic_data | Check |
| Attendance | late_entry_by | Int |
| Attendance | early_out_by | Int |
| Attendance | is_wfh | Check |
| Employee Checkin | is_off | Check |

## Probe + Research Findings (embedded)

- **frappe-only** compose project: REMOVED at 11:42 IST Aug 20 (3 containers gone)
- **Port convention:** No existing env publishes host ports. Match this.
- **nginx config:** Real served file = `/home/vijay/nginx-erp.conf`
- **SSL certs:** Located at `/home/vijay/erpnext/ssl-certs/<subdomain>/{fullchain,privkey}.pem`. **Existing certs expire 2026-10-25.** No auto-renewal script found.
- **Stale config flag:** Dead `pberpfrappe.duckdns.org` block in nginx config — REMOVE during Phase J
- **Backup scripts:** `/home/vijay/scripts/prod_backup.sh` (158 lines, hardened 2026-08-18 with `set -euo pipefail` + `timeout 900` + `PIPESTATUS[0]`) — use as template
- **Cron schedule:** `0 */6 * * *` for envs; erpclaw at `0 3 * * *`
- **DuckDNS config:** Token at `/home/vijay/erpnext/ssl-certs/duckdns-credentials.ini`

## Prerequisites

- DNS: `pberp.duckdns.org` resolves to nginx-proxy IP
- SSL cert at `/home/vijay/erpnext/ssl-certs/pberp/`
- Workspace files ready at `/root/.openclaw/workspace/projects/haritha-hospitals/`
- `frappe-only` removed (11:42 IST Aug 20)
- Pre-existing compose projects intact: erp-dev, erp-qa, erp-prod, erp_custom_apps, frappeclaw, nginx-proxy

---

## Phase A: Pre-flight (~30 min)

**Goal:** DNS verified, SSL cert provisioned, site folder created

```bash
# 1. DNS verify
dig +short pberp.duckdns.org

# 2. SSL cert directory
ssh vijay@144.217.163.228 "sudo mkdir -p /home/vijay/erpnext/ssl-certs/pberp"

# 3. Provision cert (follow duckdns-credentials.ini pattern from pberpqa)
ssh vijay@144.217.163.228 "ls /home/vijay/erpnext/ssl-certs/"

# 4. Site folder
ssh vijay@144.217.163.228 "sudo mkdir -p /home/vijay/erp-pberp"
```

**Verify:** `dig +short pberp.duckdns.org` returns nginx-proxy IP; SSL cert files exist; site folder ready.

---

## Phase B: Compose up (vanilla image) (~30 min)

**Goal:** 9 containers Up using vanilla `frappe/erpnext:v16` image (NO custom build)

```bash
# 1. Copy template from erp-qa
ssh vijay@144.217.163.228 "cd /home/vijay/erp-qa && sudo tar cf - --exclude=.git --exclude=*.sock . | (cd /home/vijay/erp-pberp && sudo tar xf -)"

# 2. Rename compose project + containers
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && sudo sed -i 's/name: erp-qa/name: pberp/' docker-compose.yml"
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && sudo sed -i 's/erp-qa-/erp-pberp-/g' docker-compose.yml"

# 3. Disable custom image (comment out CUSTOM_IMAGE + CUSTOM_TAG to use vanilla)
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && \
  sudo sed -i 's|^CUSTOM_IMAGE=.*|# CUSTOM_IMAGE=|' .env && \
  sudo sed -i 's|^CUSTOM_TAG=.*|# CUSTOM_TAG=|' .env"

# 4. Verify docker-compose.yml uses vanilla image (look for `image:` field)
ssh vijay@144.217.163.228 "grep '^[[:space:]]*image:' /home/vijay/erp-pberp/docker-compose.yml | head -5"
# Should show: image: frappe/erpnext:v16 (or similar)

# 5. Update SITE_NAME in .env
ssh vijay@144.217.163.228 "sudo sed -i 's/SITE_NAME=.*/SITE_NAME=pberp.duckdns.org/' /home/vijay/erp-pberp/.env"

# 6. Start containers (NO host ports per convention)
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && sudo docker compose -p pberp --env-file .env up -d"

# 7. Wait + verify
sleep 60
ssh vijay@144.217.163.228 "docker ps | grep pberp"  # Should show 9 containers
ssh vijay@144.217.163.228 "docker inspect --format '{{.State.Health.Status}}' erp-pberp-backend-1"  # healthy
```

**Verify:** 9 containers Up, backend healthy, image is `frappe/erpnext:v16` (vanilla).

---

## Phase C: Site creation (~15 min)

```bash
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && \
  docker exec -u frappe erp-pberp-backend-1 bash -c '
    cd /home/frappe/frappe-bench
    bench new-site pberp.duckdns.org \
      --mariadb-root-password <ROOT_PWD> \
      --admin-password <ADMIN_PWD>
  '"
```

**DO NOT install any app here** — apps installed in Phase D via `bench get-app` + `bench install-app`.

**Verify:** UI login works at `http://pberp.duckdns.org:8000`. Only `frappe` is installed.

---

## Phase D: Get apps + install + restart workers (~30 min)

**Goal:** Install payments + erpnext + hrms (16.5.0 pinned) on the site + restart workers per Lesson #46

```bash
# 1. Get apps (via runtime installation per user preference)
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && \
  docker exec -u frappe erp-pberp-backend-1 bash -c '
    cd /home/frappe/frappe-bench
    bench get-app payments
    bench get-app erpnext --branch version-16
    bench get-app hrms --branch version-15  # PINNED — Lesson #44
  '"

# 2. Install apps on site
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && \
  docker exec -u frappe erp-pberp-backend-1 bash -c '
    cd /home/frappe/frappe-bench
    bench --site pberp.duckdns.org install-app erpnext hrms payments
  '"

# 3. Verify apps installed (Lesson #80 — both DB and filesystem must match)
ssh vijay@144.217.163.228 "cat /home/vijay/erp-pberp/sites/apps.txt"
# Should show 4 lines: frappe, erpnext, hrms, payments

ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && \
  docker exec -u frappe erp-pberp-backend-1 bash -c '
    cd /home/frappe/frappe-bench
    bench --site pberp.duckdns.org console -c \"import frappe; print(frappe.get_installed_apps())\"
  '"
# Should show: ['frappe', 'erpnext', 'hrms', 'payments']

# 4. Restart workers (Lesson #46)
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && sudo docker compose -p pberp restart"
sleep 30
```

**Verify:** All 4 apps visible. Workers restarted. UI works.

---

## Phase E: Custom fields fixtures (~30 min)

```bash
# Pre-author fixture JSON
ssh vijay@144.217.163.228 "cat > /home/vijay/erp-pberp/masters/pberp_custom_fields.json << 'EOF'
[
  {\"doctype\":\"Custom Field\",\"name\":\"is_oncall\",\"dt\":\"Shift Type\",\"fieldname\":\"is_oncall\",\"label\":\"Is On-Call Shift\",\"fieldtype\":\"Check\",\"insert_after\":\"is_past_end_time\",\"default\":\"0\"},
  {\"doctype\":\"Custom Field\",\"name\":\"is_emergency\",\"dt\":\"Shift Type\",\"fieldname\":\"is_emergency\",\"label\":\"Is Emergency Shift\",\"fieldtype\":\"Check\",\"insert_after\":\"is_oncall\",\"default\":\"0\"},
  {\"doctype\":\"Custom Field\",\"name\":\"is_synthetic_data\",\"dt\":\"Employee\",\"fieldname\":\"is_synthetic_data\",\"label\":\"Is Synthetic Data\",\"fieldtype\":\"Check\",\"insert_after\":\"branch\",\"default\":\"0\"},
  {\"doctype\":\"Custom Field\",\"name\":\"late_entry_by\",\"dt\":\"Attendance\",\"fieldname\":\"late_entry_by\",\"label\":\"Late Entry By (minutes)\",\"fieldtype\":\"Int\",\"insert_after\":\"shift\",\"default\":\"0\"},
  {\"doctype\":\"Custom Field\",\"name\":\"early_out_by\",\"dt\":\"Attendance\",\"fieldname\":\"early_out_by\",\"label\":\"Early Out By (minutes)\",\"fieldtype\":\"Int\",\"insert_after\":\"late_entry_by\",\"default\":\"0\"},
  {\"doctype\":\"Custom Field\",\"name\":\"is_wfh\",\"dt\":\"Attendance\",\"fieldname\":\"is_wfh\",\"label\":\"Work From Home\",\"fieldtype\":\"Check\",\"insert_after\":\"early_out_by\",\"default\":\"0\"},
  {\"doctype\":\"Custom Field\",\"name\":\"is_off\",\"dt\":\"Employee Checkin\",\"fieldname\":\"is_off\",\"label\":\"Off-Shift Check-in\",\"fieldtype\":\"Check\",\"insert_after\":\"source\",\"default\":\"0\"}
]
EOF
"

# Apply via console
ssh vijay@144.217.163.228 "docker exec -u frappe erp-pberp-backend-1 bash -c '
    cd /home/frappe/frappe-bench
    bench --site pberp.duckdns.org console <<\"PYTHON\"
import frappe, json
frappe.flags.mute_emails = True
data = json.load(open(\"/home/vijay/erp-pberp/masters/pberp_custom_fields.json\"))
for item in data:
    frappe.get_doc(dict(item)).insert(ignore_permissions=True)
frappe.db.commit()
print(f\"Inserted {len(data)} custom fields\")
PYTHON
'"
```

**Verify:**
- `frappe.get_meta("Shift Type").custom_fields` length = 2
- `frappe.get_meta("Attendance").custom_fields` length = 3
- `frappe.get_meta("Employee").custom_fields` length = 1
- `frappe.get_meta("Employee Checkin").custom_fields` length = 1

---

## Phase F: MySQL grants (Lesson #87) — ~5 min

**Critical:** Run BEFORE scheduler wakes up (within ~30s of Phase B)

```bash
# Find scheduler IP
ssh vijay@144.217.163.228 "docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' erp-pberp-scheduler-1"

# Get DB credentials
ssh vijay@144.217.163.228 "grep -E 'MYSQL|DB_' /home/vijay/erp-pberp/.env"

# Pre-create grant
ssh vijay@144.217.163.228 "docker exec erp-pberp-db-1 mariadb -u root -p<ROOT_PWD> -e \"
  GRANT ALL ON pberp_db.* TO 'pberp_user'@'<SCHEDULER_IP>' IDENTIFIED BY '<DB_PWD>';
  FLUSH PRIVILEGES;
\""

# Verify no 1045 errors after 5 min
sleep 300
ssh vijay@144.217.163.228 "docker logs erp-pberp-scheduler-1 --since 5m | grep -c 1045"  # should be 0
```

**Verify:** Zero 1045 errors in scheduler logs.

---

## Phase G: Company + Holiday List (~15 min)

```bash
# Copy CSVs into container workspace
ssh vijay@144.217.163.228 "docker cp /home/vijay/erp-pberp/masters/company.csv erp-pberp-backend-1:/tmp/"
ssh vijay@144.217.163.228 "docker cp /home/vijay/erp-pberp/masters/holiday_list.csv erp-pberp-backend-1:/tmp/"
ssh vijay@144.217.163.228 "docker cp /home/vijay/erp-pberp/masters/holiday.csv erp-pberp-backend-1:/tmp/"

# Import via Data Import tool (UI) or console
# (See all_schemas.csv for field names)
```

**Verify:** UI shows Haritha Hospitals company + 14 holidays.

---

## Phase H: Data import (~60 min)

**Order (smallest first):**
1. Department, Designation, Employment Type, Shift Type, Leave Type (small)
2. Employee (210)
3. ~~Leave Allocation~~ DEFER (Decision #4) — HRMS auto-allocates
4. Shift Assignment (5,317), Attendance (6,300), Employee Checkin (12,562) — large

```bash
# Per entity (template):
ssh vijay@144.217.163.228 "docker cp /home/vijay/erp-pberp/masters/<entity>.csv erp-pberp-backend-1:/tmp/"
ssh vijay@144.217.163.228 "docker exec -u frappe erp-pberp-backend-1 bash -c '
    cd /home/frappe/frappe-bench
    bench --site pberp.duckdns.org console <<\"PYTHON\"
import frappe, csv
rows = list(csv.DictReader(open(\"/tmp/<entity>.csv\")))
for r in rows:
    frappe.get_doc(dict({\"doctype\": \"<DocType>\", **r})).insert(ignore_permissions=True)
frappe.db.commit()
print(f\"Imported {len(rows)} <DocType>\")
PYTHON
'"

# Verify after each
ssh vijay@144.217.163.228 "docker exec -u frappe erp-pberp-backend-1 bench --site pberp.duckdns.org console -c 'import frappe; print(frappe.db.count(\"<DocType>\"))'"
```

**Expected counts:**
| Entity | Count |
|---|---|
| Department | 36 |
| Designation | 48 |
| Employment Type | 6 |
| Shift Type | 25 |
| Leave Type | 7 |
| Employee | 210 (194 Active, 16 Inactive) |
| Shift Assignment | 5,317 |
| Attendance | 6,300 |
| Employee Checkin | 12,562 |

---

## Phase I: Backup setup (HARDENED pattern) (~30 min)

**Use `prod_backup.sh` (158 lines) as template** — has `set -euo pipefail` + `timeout 900` + `PIPESTATUS[0]` (Lesson #79).

```bash
# 1. Copy template
ssh vijay@144.217.163.228 "sudo cp /home/vijay/scripts/prod_backup.sh /home/vijay/scripts/pberp_backup.sh"

# 2. Edit variables
ssh vijay@144.217.163.228 "sudo sed -i 's/SITE_NAME=.*/SITE_NAME=pberp.duckdns.org/' /home/vijay/scripts/pberp_backup.sh"
ssh vijay@144.217.163.228 "sudo sed -i 's/BACKUP_CONTAINER=.*/BACKUP_CONTAINER=erp-pberp-backend-1/' /home/vijay/scripts/pberp_backup.sh"
ssh vijay@144.217.163.228 "sudo sed -i 's|LOCAL_BACKUP_DIR=.*|LOCAL_BACKUP_DIR=/home/vijay/backups/pberp|' /home/vijay/scripts/pberp_backup.sh"
ssh vijay@144.217.163.228 "sudo sed -i 's|OFFSITE_TARGET=.*|OFFSITE_TARGET=venkat@135.125.196.35:/home/venkat/pberp_backups|' /home/vijay/scripts/pberp_backup.sh"

# 3. Syntax check + chmod
ssh vijay@144.217.163.228 "bash -n /home/vijay/scripts/pberp_backup.sh && chmod +x /home/vijay/scripts/pberp_backup.sh"

# 4. Add to cron (heredoc + atomic per Lesson #77)
ssh vijay@144.217.163.228 "crontab -l > /tmp/cron.bak && \
  echo '0 */6 * * * /home/vijay/scripts/pberp_backup.sh >> /home/vijay/backups/logs/pberp_backup.log 2>&1' >> /tmp/cron.bak && \
  crontab /tmp/cron.bak && rm /tmp/cron.bak"

# 5. First run (sanity)
ssh vijay@144.217.163.228 "sudo /home/vijay/scripts/pberp_backup.sh"
```

**Verify:** `crontab -l` shows pberp backup line. First run produces valid backup file.

---

## Phase J: nginx routing (~30 min)

**REAL path:** `/home/vijay/nginx-erp.conf` (NOT `conf.d/`)

```bash
# 1. Backup current config
ssh vijay@144.217.163.228 "sudo cp /home/vijay/nginx-erp.conf /home/vijay/nginx-erp.conf.bak-\$(date +%Y%m%d)"

# 2. Edit /home/vijay/nginx-erp.conf — add pberp.duckdns.org server block
# Use pberpqa block as template; upstream: erp-pberp-frontend-1:8080

# 3. CLEANUP: remove dead pberpfrappe.duckdns.org block

# 4. Test + reload
ssh vijay@144.217.163.228 "docker exec nginx-proxy nginx -t"
ssh vijay@144.217.163.228 "docker exec nginx-proxy nginx -s reload"

# 5. Verify
curl -I https://pberp.duckdns.org/  # 200/302
```

**Verify:** `nginx -t` syntax OK; `curl -I https://pberp.duckdns.org/` returns 200/302; UI accessible.

---

## Phase K: Test + Sign-off (~3-4 hr)

### K1: Vendor tests (100% green REQUIRED)

```bash
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && \
  docker exec -u frappe erp-pberp-backend-1 bash -c '
    cd /home/frappe/frappe-bench
    CI=1 bench --site pberp.duckdns.org run-tests --app hrms
  '"
```

**Must be 100% green. If failures, investigate before proceeding.**

### K2-K7: Standard 8-phase (per Lesson #48)
- K2: Smoke (login + view pages)
- K3: Schema (all 19 entities exist)
- K4: CRUD (test records)
- K5: Workflow (Shift Schedule → SSA → cron → Shift Assignment creation)
- K6: Integration (Leave → Attendance status)
- K7: Regression (existing critical workflows)

### K8: Delete ALL test data (per Decision #7)

```bash
ssh vijay@144.217.163.228 "cd /home/vijay/erp-pberp && \
  docker exec -u frappe erp-pberp-backend-1 bench --site pberp.duckdns.org console <<\"PYTHON\"
import frappe
frappe.db.sql(\"DELETE FROM tabShift Assignment WHERE docstatus=0\")
frappe.db.sql(\"DELETE FROM tabEmployee WHERE employee_number LIKE 'TEST-%'\")
frappe.db.sql(\"DELETE FROM tabAttendance WHERE status='Test'\")
frappe.db.commit()
print('Test data deleted')
PYTHON
"
```

### K9: Generate sign-off report

```bash
ssh vijay@144.217.163.228 "cat > /home/vijay/erp-pberp/sites/sign-off-report.md << 'EOF'
# Haritha Hospitals — Phase 2 Sign-off Report
**Date:** $(date)
**Site:** pberp.duckdns.org
**Compose project:** pberp
**Approach:** Vanilla frappe/erpnext:v16 + runtime app install (per user preference)

## Test Results
### Vendor Tests (K1)
- HRMS: <PASS/FAIL> (X/Y tests, Z failures)

### Data Import Counts (K3)
| Entity | Expected | Actual |
|--------|----------|--------|
| Department | 36 | ? |
| Designation | 48 | ? |
| Employee | 210 | ? |
| Shift Type | 25 | ? |
| Shift Assignment | 5,317 | ? |
| Attendance | 6,300 | ? |
| Employee Checkin | 12,562 | ? |

## Custom Fields Applied (Rule #9)
- 7 custom fields verified

## Backup Verified
- First run: <timestamp>

## nginx Verified
- https://pberp.duckdns.org/ returns 200/302

## Sign-off
- [ ] All tests 100% green
- [ ] Counts verified
- [ ] Test data deleted
- [ ] User approves

**Signed off by:** ________________
**Date:** ____________
EOF
"
```

---

## Phase L: Cert expiry monitoring (~15 min)

**CRITICAL:** Existing certs expire 2026-10-25. No auto-renewal script found.

```bash
# 1. Check expiry of all certs
ssh vijay@144.217.163.228 "for cert in /home/vijay/erpnext/ssl-certs/*/fullchain.pem; do echo \"\$cert: \$(openssl x509 -enddate -noout -in \$cert | cut -d= -f2)\"; done"

# 2. Write cert-expiry-check.sh script
ssh vijay@144.217.163.228 "cat > /home/vijay/scripts/cert_expiry_check.sh << 'EOF'
#!/bin/bash
set -euo pipefail
EXPIRY=\$(openssl x509 -enddate -noout -in /home/vijay/erpnext/ssl-certs/pberp/fullchain.pem | cut -d= -f2)
EXPIRY_EPOCH=\$(date -d \"\$EXPIRY\" +%s)
NOW_EPOCH=\$(date +%s)
DAYS_LEFT=\$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
if [ \$DAYS_LEFT -lt 30 ]; then
  echo \"WARNING: pberp cert expires in \$DAYS_LEFT days (\$EXPIRY)\"
fi
EOF
chmod +x /home/vijay/scripts/cert_expiry_check.sh"

# 3. Add daily check to cron
ssh vijay@144.217.163.228 "crontab -l > /tmp/cron.bak && \
  echo '0 8 * * * /home/vijay/scripts/cert_expiry_check.sh >> /home/vijay/scripts/cert_expiry.log 2>&1' >> /tmp/cron.bak && \
  crontab /tmp/cron.bak && rm /tmp/cron.bak"

# 4. Calendar reminder (manual) — renew 25 days before expiry
echo "Set calendar reminder for 2026-10-01 to renew pberp cert"
```

**Verify:** `crontab -l` shows daily cert check. First run produces no warning (cert valid).

---

## Open Questions / Decisions

All 7 decisions captured. No remaining open questions.

## Sign-off Checklist

Before Phase 2 closure:

- [ ] A: DNS + SSL + dir ready
- [ ] B: 9 containers Up + backend healthy (vanilla image)
- [ ] C: Site created + admin password set (no app install)
- [ ] D: All 4 apps installed + workers restarted
- [ ] E: 7 custom fields verified
- [ ] F: Zero 1045 errors (Lesson #87 prevented)
- [ ] G: Company + Holidays in UI
- [ ] H: All 19 entities imported + counts match
- [ ] I: Backup cron + first run success (hardened pattern)
- [ ] J: nginx serving pberp.duckdns.org
- [ ] K1: Vendor tests 100% GREEN
- [ ] K2-K7: Manual tests all PASS
- [ ] K8: Test data deleted
- [ ] K9: Sign-off report generated
- [ ] L: Cert expiry monitoring set up
- [ ] Manager approval

---

**Total estimated time:** 5-7 hours (down from 7-10 due to simplified approach)
**Sign-off requires:** All checklist items + 100% green vendor tests
