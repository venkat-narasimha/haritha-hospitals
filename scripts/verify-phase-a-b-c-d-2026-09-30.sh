#!/bin/bash
# verify-phase-a-b-c-d-2026-09-30.sh
#
# Phase E deliverable 5: Sanity-check script for all Phase A + B + D outcomes.
#
# Usage:
#   bash scripts/verify-phase-a-b-c-d-2026-09-30.sh
#
# What it does:
#   1. SSHes to prod VPS
#   2. Runs `bench --site prod-env.duckdns.org console` with embedded Python
#   3. Python script does 13 checks against live MariaDB tables
#   4. Prints PASS/FAIL for each + summary
#
# Exit codes:
#   0 = all checks PASS
#   1 = one or more checks FAIL
#   2 = infrastructure error (SSH, container not running, etc.)
#
# Phase A outcomes verified:
#   - 6 Haritha Role Profiles present
#   - 6 Haritha Workspaces present (all public=0)
#   - 2 active workflows (Leave Application + Shift Request)
#   - 8+ Notifications (Haritha workflow notifications)
#   - 451+ User Permissions
#   - 211/211 Active employees with user_id
#   - 211/211 with leave_approver (Administrator fallback acceptable)
#   - Role.module_profile Custom Field exists
#
# Phase B outcomes verified:
#   - HRMS scheduler last execution < 2h ago
#   - HRMS Health Monitor Server Script enabled (disabled=0)
#   - HRMS Health Alert DocType exists
#
# Phase D outcomes verified:
#   - Password policy enabled (enable_password_policy=1)
#
# Author: Phase E subagent (depth 1/5)
# Sanitized per AGENTS.md rule

set -e

# --- Config (sanitized) ---
SSH_KEY="/root/.openclaw/ssh_key"
SSH_USER="<user>"
SSH_HOST="[redacted-IP]"
CONTAINER_BACKEND="prod-env-backend-1"
CONTAINER_DB="prod-env-db-1"
CONTAINER_SCHEDULER="prod-env-scheduler-1"
SITE_DOMAIN="prod-env.duckdns.org"
DB_NAME="[redacted-db-name]"
ENV_FILE="/home/<user>/erpnext/prod-env/.env"

# --- Helpers ---
red()    { printf '\033[0;31m%s\033[0m\n' "$*"; }
green()  { printf '\033[0;32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[0;33m%s\033[0m\n' "$*"; }
cyan()   { printf '\033[0;36m%s\033[0m\n' "$*"; }

# --- Pre-flight: SSH access ---
cyan "[preflight] Testing SSH + Docker access..."
if ! ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=10 \
    "$SSH_USER@$SSH_HOST" \
    "docker ps --filter name=$CONTAINER_SCHEDULER --format '{{.Names}}: {{.Status}}'" \
    >/dev/null 2>&1; then
  red "[FAIL] SSH or scheduler container unreachable"
  red "       check: $SSH_KEY, $SSH_USER@$SSH_HOST, container name"
  exit 2
fi
green "[preflight] OK"

# --- Pre-flight: DB credentials ---
cyan "[preflight] Fetching DB password..."
DB_PASS=$(ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$SSH_HOST" \
  "grep DB_PASSWORD $ENV_FILE | cut -d= -f2" 2>/dev/null)
if [ -z "$DB_PASS" ]; then
  red "[FAIL] Could not fetch DB_PASSWORD from $ENV_FILE"
  exit 2
fi
green "[preflight] DB password loaded (length ${#DB_PASS})"

# --- Write embedded Python verification script ---
TMP_SQL=$(mktemp)
trap 'rm -f "$TMP_SQL" /tmp/phase_e_verify.py' EXIT

cat > /tmp/phase_e_verify.py << 'PYEOF'
"""Phase A + B + D sanity-check script for this hospital.
Runs inside `bench console` context on prod site.
Prints PASS/FAIL per check + summary.
"""
import frappe
from datetime import datetime, timedelta

results = []  # list of (name, passed, detail)

def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    results.append((name, condition, detail))
    sym = "✅" if condition else "❌"
    print(f"{sym} {name}: {status}  {detail}")

print("=" * 78)
print(f"Phase A + B + D Verification — this hospital")
print(f"Run at: {frappe.utils.now()}")
print(f"Site: {frappe.local.site}")
print("=" * 78)
print()

# ============================================================================
# Phase A: RBAC + Workflows + Dashboards + User Provisioning
# ============================================================================
print("--- Phase A: RBAC + Workflows + Dashboards + User Provisioning ---")

# A.1 6 Haritha Role Profiles
rp_count = frappe.db.count("Role Profile", {"name": ["like", "Haritha:%"]})
check("A.1 6 Haritha Role Profiles",
      rp_count == 6,
      f"found={rp_count} (expected 6)")

# A.2 6 Haritha Workspaces (all public=0)
ws_count = frappe.db.count("Workspace", {"name": ["like", "Haritha:%"]})
ws_private = frappe.db.count("Workspace", {"name": ["like", "Haritha:%"], "public": 0})
check("A.2 6 Haritha Workspaces (all public=0)",
      ws_count == 6 and ws_private == 6,
      f"total={ws_count}, private={ws_private} (expected 6/6)")

# A.3 2 active workflows
wf_count = frappe.db.count("Workflow", {"is_active": 1,
                                          "document_type": ["in", ["Leave Application", "Shift Request"]]})
check("A.3 2 active workflows (Leave App + Shift Request)",
      wf_count == 2,
      f"found={wf_count} (expected 2)")

# A.4 8+ notifications (Haritha workflow notifications)
notif_count = frappe.db.count("Notification",
                                {"name": ["in", [
                                  "Leave Application: Pending Approval",
                                  "Leave Application: Approved",
                                  "Leave Application: Rejected",
                                  "Leave Application: Cancelled",
                                  "Shift Request: Pending Approval",
                                  "Shift Request: Approved",
                                  "Shift Request: Rejected",
                                  "Shift Request: Cancelled",
                                ]]})
check("A.4 8 Haritha Notifications",
      notif_count >= 8,
      f"found={notif_count} (expected >=8)")

# A.5 451+ User Permissions
up_count = frappe.db.count("User Permission")
check("A.5 451+ User Permissions",
      up_count >= 451,
      f"found={up_count} (expected >=451)")

# A.6 211/211 Active employees with user_id
emp_total = frappe.db.count("Employee", {"status": "Active"})
emp_with_user = frappe.db.sql("""
    SELECT COUNT(*) FROM tabEmployee
    WHERE status='Active' AND IFNULL(user_id,'') != ''
""")[0][0]
check("A.6 211/211 Active employees with user_id",
      emp_total == 211 and emp_with_user == 211,
      f"active={emp_total}, with_user_id={emp_with_user}")

# A.7 211/211 with leave_approver (Administrator fallback acceptable)
emp_with_approver = frappe.db.sql("""
    SELECT COUNT(*) FROM tabEmployee
    WHERE status='Active' AND IFNULL(leave_approver,'') != ''
""")[0][0]
check("A.7 211/211 with leave_approver",
      emp_with_approver == 211,
      f"with_approver={emp_with_approver} (expected 211)")

# A.8 Role.module_profile Custom Field exists
mf_exists = frappe.db.exists("Custom Field", {"dt": "Role", "fieldname": "module_profile"})
check("A.8 Role.module_profile Custom Field",
      bool(mf_exists),
      f"exists={bool(mf_exists)}")

print()

# ============================================================================
# Phase B: Auto-attendance activation
# ============================================================================
print("--- Phase B: Auto-attendance Activation ---")

# B.1 HRMS scheduler last execution < 2h ago
last_hrms = frappe.db.sql("""
    SELECT MAX(last_execution) FROM `tabScheduled Job Type`
    WHERE method LIKE '%hrms%' OR method LIKE 'hrms%'
""")[0][0]
if last_hrms:
    now = frappe.utils.now_datetime()
    last_dt = frappe.utils.get_datetime(last_hrms)
    seconds_ago = (now - last_dt).total_seconds()
    hours_ago = seconds_ago / 3600.0
    check("B.1 HRMS scheduler fired < 2h ago",
          seconds_ago < 7200,
          f"last={last_hrms}, {hours_ago:.2f}h ago")
else:
    check("B.1 HRMS scheduler fired < 2h ago",
          False,
          "no HRMS scheduler job found")

# B.2 HRMS Health Monitor Server Script enabled (disabled=0)
health_script = frappe.db.get_value("Server Script",
                                      "HRMS Health Monitor",
                                      ["disabled", "script_type", "event_frequency"],
                                      as_dict=True)
if health_script:
    check("B.2 HRMS Health Monitor Server Script enabled",
          health_script.disabled == 0,
          f"disabled={health_script.disabled}, type={health_script.script_type}, freq={health_script.event_frequency}")
else:
    check("B.2 HRMS Health Monitor Server Script enabled",
          False,
          "HRMS Health Monitor Server Script not found")

# B.3 HRMS Health Alert DocType exists
alert_exists = frappe.db.exists("DocType", "HRMS Health Alert")
check("B.3 HRMS Health Alert DocType",
      bool(alert_exists),
      f"exists={bool(alert_exists)}")

print()

# ============================================================================
# Phase D: Notifications + Scheduled Jobs + Monitoring
# ============================================================================
print("--- Phase D: Notifications + Scheduled Jobs + Monitoring ---")

# D.1 Password policy enabled (enable_password_policy=1)
pp_enabled = frappe.db.get_single_value("System Settings", "enable_password_policy")
check("D.1 Password policy enabled",
      pp_enabled == 1,
      f"enable_password_policy={pp_enabled}")

# D.2 (sanity) E2E Workflow Document States populated
state_count = frappe.db.sql("""
    SELECT COUNT(*) FROM `tabWorkflow Document State`
    WHERE parent IN ('Leave Application', 'Shift Request')
""")[0][0]
check("D.2 Workflow Document States (Leave + Shift Request)",
      state_count >= 10,
      f"states={state_count} (expected >=10)")

print()
print("=" * 78)

# Summary
passed = sum(1 for _, ok, _ in results if ok)
failed = sum(1 for _, ok, _ in results if not ok)
total = len(results)
print(f"SUMMARY: {passed}/{total} checks PASSED, {failed} FAILED")
print("=" * 78)

# Exit with proper code
import sys
sys.exit(0 if failed == 0 else 1)
PYEOF

# --- Push script + run ---
cyan "[exec] Pushing verify script to VPS..."
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no /tmp/phase_e_verify.py \
  "$SSH_USER@$SSH_HOST:/tmp/phase_e_verify.py"

cyan "[exec] Running verify script via bench console on $SITE_DOMAIN..."
echo

# Pipe the Python into bench console
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$SSH_HOST" \
  "docker exec -i $CONTAINER_BACKEND bash -c 'cd /home/frappe/frappe-bench && bench --site $SITE_DOMAIN console'" \
  < /tmp/phase_e_verify.py
VERIFY_EXIT=$?

echo
if [ "$VERIFY_EXIT" -eq 0 ]; then
  green "[done] All checks PASSED"
  exit 0
else
  yellow "[done] Some checks FAILED — review above output"
  exit 1
fi
