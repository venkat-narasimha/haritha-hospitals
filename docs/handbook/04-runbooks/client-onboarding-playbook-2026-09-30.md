# Client Onboarding Playbook (templated for any new org)

**Date:** 2026-09-30 (Phase E handover snapshot)
**Phase E deliverable:** 3 of 5
**Purpose:** Step-by-step playbook for onboarding a new client (hospital, college, factory, retail chain, etc.) onto a Frappe/ERPNext/HRMS instance with the `haritta_hospital` custom app.
**Audience:** Implementation team (subagents, IT staff, Processbricks consultants).
**Templated for:** Any new tenant. Domain/industry-agnostic. Hospital, college, factory patterns are noted where applicable.

---

## Pre-flight checklist (run before starting)

| # | Task | Owner | Verification |
|---|---|---|---|
| 0.1 | Provision VPS / k8s namespace | IT | Docker Compose running, ports 80/443 open |
| 0.2 | Reserve domain + DuckDNS / Cloudflare | IT | DNS resolves to VPS |
| 0.3 | Set up SMTP relay (SendGrid, Mailgun, self-hosted) | IT | `bench execute frappe.sendmail.sendmail` delivers |
| 0.4 | Acquire TLS cert (Let's Encrypt or self-signed fallback) | IT | `https://<domain>/` serves 200 with valid cert |
| 0.5 | Backup credentials (DB root, admin password) to 1Password | IT | All 3 creds present |
| 0.6 | Define client "go-live target date" | PM | Locked with client sponsor |

**Time estimate:** 1-2 days wall time (mostly SMTP + DNS + cert waiting).

---

## Step 1 — Provision infra

```bash
# On VPS, as user
mkdir -p /home/<user>/<client-name>/
cd /home/<user>/<client-name>/

# Clone compose stack
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker

# Customise compose for this client
cp compose.yaml compose.yaml.bak
# Edit: change site domain, container prefix, volume paths, port mappings
```

**Domain convention:** `<client>-prod.duckdns.org` (e.g., `acme-prod.duckdns.org`).
**Container convention:** `<client>-prod-backend-1`, `<client>-prod-db-1`, `<client>-prod-scheduler-1`.

---

## Step 2 — Create new Frappe site + install custom app

```bash
# On VPS
ssh <user>@[redacted-IP]

cd /home/<user>/erpnext/<client>-prod/

# Bring up containers
docker compose up -d

# Create site
docker exec -it <client>-prod-backend-1 bash -c "
  cd /home/frappe/frappe-bench &&
  bench new-site <client>-prod.duckdns.org \\
    --mariadb-root-password '<DB_ROOT_PASS>' \\
    --admin-password '<ADMIN_PASS>' \\
    --install-app erpnext &&
  bench --site <client>-prod.duckdns.org install-app hrms &&
  bench --site <client>-prod.duckdns.org install-app haritta_hospital
"

# Set site in production
docker exec -it <client>-prod-backend-1 bash -c "
  cd /home/frappe/frappe-bench &&
  bench --site <client>-prod.duckdns.org set-config developer_mode 0 &&
  bench --site <client>-prod.duckdns.org enable-scheduler
"
```

**Verification:** Visit `https://<client>-prod.duckdns.org/`, log in as Administrator, see HRMS module.

---

## Step 3 — Configure Company

| Field | Template value |
|---|---|
| Company Name | `<Client Legal Name>` |
| Abbreviation | 3-6 char code (e.g., `ACME`) |
| Default Currency | INR (or USD/EUR/AED as per client) |
| Country | India (or as per client) |
| Default Holiday List | `<Client Name> Holiday List` (created in Step 6) |
| Default Financial Year | April-March (or calendar-year override) |
| Payroll Cost Center | `<Client Name>` |
| Chart of Accounts | Standard India (or regional) |

```bash
docker exec -it <client>-prod-backend-1 bench --site <client>-prod.duckdns.org console << 'PY'
import frappe
co = frappe.new_doc("Company")
co.company_name = "<Client Legal Name>"
co.abbr = "ACME"
co.default_currency = "INR"
co.country = "India"
co.default_holiday_list = "<Client Name> Holiday List"
co.save()
frappe.db.commit()
PY
```

**Verification:** `bench --site <client>-prod.duckdns.org execute frappe.db.get_single_value('Company', 'name')` returns the company name.

---

## Step 4 — Define Departments + Designations + Department Heads

### Department template (one row per dept)

| Department | Parent Department | Leave Approver (User) |
|---|---|---|
| Administration | (root) | admin@<client-domain> |
| Finance & Accounts | Administration | cfo@<client-domain> |
| Human Resources | Administration | hr.head@<client-domain> |
| Operations | Administration | ops.head@<client-domain> |
| Information Technology | Administration | it.head@<client-domain> |
| Nursing | Operations | (assigned post hire) |
| Pharmacy | Operations | (assigned post hire) |
| ... | ... | ... |

### Designation template

| Designation | Seniority (1-10) |
|---|---|
| CEO / COO | 10 |
| Vice President | 9 |
| Senior Manager | 8 |
| Manager | 7 |
| Assistant Manager | 6 |
| Senior Executive | 5 |
| Executive | 4 |
| Senior Officer | 3 |
| Officer | 2 |
| Trainee | 1 |

### Department Heads

For each dept with ≥3 employees, assign one **Department Head** (must be a User with `HR Manager` or custom `Department Head` role). Stored on `Department.leave_approver`.

```python
import frappe
import openpyxl

wb = openpyxl.load_workbook("/home/<user>/intake/<client>-departments.xlsx")
for row in wb.active.iter_rows(min_row=2, values_only=True):
    name, parent, approver_email = row
    d = frappe.new_doc("Department")
    d.department_name = name
    d.parent_department = parent
    d.leave_approver = approver_email
    d.save()
frappe.db.commit()
```

**Verification:** `SELECT COUNT(*) FROM tabDepartment` matches the intake spreadsheet.

---

## Step 5 — Define Shift Types

### Shift Type template

| Shift Code (10-char) | Start Time | End Time | Duration | Color | enable_auto_attendance |
|---|---|---|---|---|---|
| `P0800S1700` | 08:00:00 | 17:00:00 | 9h | `#28a745` (green) | 1 |
| `P0900S1800` | 09:00:00 | 18:00:00 | 9h | `#007bff` (blue) | 1 |
| `P0900S1400` | 09:00:00 | 14:00:00 | 5h | `#ffc107` (amber) | 1 |
| `P1400S2200` | 14:00:00 | 22:00:00 | 8h | `#17a2b8` (cyan) | 1 |
| `P2200S0700` | 22:00:00 | 07:00:00 | 9h | `#6f42c1` (purple) | 1 |
| `P0000S0800` | 00:00:00 | 08:00:00 | 8h | `#dc3545` (red) | 1 |
| `P0700S1500` | 07:00:00 | 15:00:00 | 8h | `#fd7e14` (orange) | 1 |

### Bulk create via fixture

The `haritta_hospital` custom app ships Shift Type fixtures. On a clean install:

```bash
docker exec -it <client>-prod-backend-1 bench --site <client>-prod.duckdns.org console << 'PY'
import frappe
# Migrate Shift Types from custom app fixtures
frappe.reload_doc("hr", "doctype", "shift_type")
frappe.db.commit()
PY
```

Then upload client-specific shifts via:

```python
import openpyxl
wb = openpyxl.load_workbook("/home/<user>/intake/<client>-shifts.xlsx")
for row in wb.active.iter_rows(min_row=2, values_only=True):
    code, start, end, color, auto = row
    st = frappe.new_doc("Shift Type")
    st.name = code  # name IS the code (per design decision)
    st.start_time = start
    st.end_time = end
    st.color = color
    st.enable_auto_attendance = auto
    st.save()
frappe.db.commit()
```

**Verification:** `SELECT COUNT(*) FROM tabShift Type` matches expected.

---

## Step 6 — Configure Holiday List

### Holiday List template

```python
holidays = [
    ("2026-01-26", "Republic Day"),
    ("2026-03-25", "Holi"),
    ("2026-04-03", "Good Friday"),
    ("2026-08-15", "Independence Day"),
    ("2026-10-02", "Gandhi Jayanti"),
    ("2026-11-08", "Diwali"),
    ("2026-12-25", "Christmas"),
    # ... + regional state-specific
]

hl = frappe.new_doc("Holiday List")
hl.name = "<Client Name> Holiday List"
hl.from_date = "2026-01-01"
hl.to_date = "2026-12-31"
hl.weekly_off = None  # client works Sundays? set to "Sunday" if not
for date_str, label in holidays:
    row = hl.append("holidays", {})
    row.holiday_date = date_str
    row.description = label
hl.save()
```

**Verification:** Visit `/app/holiday-list/<name>`, see all holidays.

---

## Step 7 — Create Roles + Role Profiles (6 standard)

The 6 standard Haritha roles and Role Profiles ship as fixtures in the custom app. After install:

```bash
docker exec -it <client>-prod-backend-1 bench --site <client>-prod.duckdns.org console << 'PY'
import frappe
# Role Profiles are fixtures — auto-loaded on install-app
# Verify
profiles = frappe.get_all("Role Profile", filters={"name": ["like", "Haritha:%"]})
print(f"Found {len(profiles)} Haritha role profiles")
PY
```

Expected: 6 (System Manager, HR Manager, HR User, Roster Manager, Leave Approver, Employee).

**If a tenant needs custom roles** (e.g., "Lab Manager" not in the 6 standard), create them and assign appropriate `tabCustom DocPerm`. See `06-reference/role-permission-matrix-2026-09-30.md` for the standard matrix to clone.

---

## Step 8 — Create Workspaces (6 standard per role)

Same as Role Profiles — workspaces ship as fixtures. On install:

```bash
# Workspaces auto-load via fixtures. Verify:
docker exec -it <client>-prod-backend-1 bench --site <client>-prod.duckdns.org console << 'PY'
import frappe
ws = frappe.get_all("Workspace", filters={"name": ["like", "Haritha:%"], "public": 0})
print(f"Found {len(ws)} private Haritha workspaces")
PY
```

Expected: 6, all `public=0` (private — visible only via Role Profile landing page).

**Customize cards:** Each Workspace has 5-8 shortcut cards (links to Dashboard, My Attendance, My Leaves, Roster Planner, etc.). Customise per tenant needs.

---

## Step 9 — Define Workflows (Leave Application + Shift Request with dept-specific routing)

The 2 standard workflows ship as fixtures. Configure dept-specific routing by:

```python
import frappe

# For each department, set leave_approver (Dept-level default)
for dept_name, approver_email in [
    ("Nursing", "nursing.hod@<client-domain>"),
    ("Pharmacy", "pharmacy.hod@<client-domain>"),
    ("Finance & Accounts", "cfo@<client-domain>"),
    # ...
]:
    d = frappe.get_doc("Department", dept_name)
    d.leave_approver = approver_email
    d.save()

frappe.db.commit()
```

**Workflow states (Leave Application):**

```
Draft (Employee) ──submit──> Pending Approval (Leave Approver)
                                  │
                          ┌───────┴───────┐
                          ▼               ▼
                     Approved        Rejected
                     (HR Manager)    (Leave Approver)
                          │
                          ▼
                     Cancelled (HR Manager)
```

**Workflow states (Shift Request):**

```
Draft (Employee) ──submit──> Pending Approval (Roster Manager)
                                  │
                          ┌───────┴───────┐
                          ▼               ▼
                     Approved        Rejected
                     (HR Manager)    (Roster Manager)
                          │
                          ▼
                     Cancelled (HR Manager)
```

---

## Step 10 — Bulk-provision Employee Users + assign Role Profiles

### Intake template (Excel)

| Employee ID | Full Name | Personal Email | Department | Designation | Date of Joining | Mobile |
|---|---|---|---|---|---|---|
| HR-EMP-00001 | Anil Kumar | anil.k@<client-domain> | Finance & Accounts | Senior Manager | 2020-03-15 | +91-9876543210 |
| HR-EMP-00002 | Priya Sharma | priya.s@<client-domain> | Human Resources | Manager | 2021-06-01 | +91-9876543211 |
| ... | ... | ... | ... | ... | ... | ... |

### Bulk provision script

```python
import frappe
import openpyxl
import re

wb = openpyxl.load_workbook("/home/<user>/intake/<client>-employees.xlsx")

for row in wb.active.iter_rows(min_row=2, values_only=True):
    emp_id, name, email, dept, desig, doj, mobile = row
    if not email:
        continue
    
    # Create User
    u = frappe.new_doc("User")
    u.email = email
    u.first_name = name.split()[0]
    u.last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ""
    u.send_welcome_email = 0  # SMTP will handle separately
    u.role_profile_name = "Haritha: Employee"
    u.insert(ignore_permissions=True)
    
    # Create Employee
    e = frappe.new_doc("Employee")
    e.employee_name = name
    e.first_name = u.first_name
    e.last_name = u.last_name
    e.employee_number = emp_id
    e.user_id = email
    e.company = "<Client Legal Name>"
    e.department = dept
    e.designation = desig
    e.date_of_joining = doj
    e.cell_number = mobile
    e.status = "Active"
    e.save(ignore_permissions=True)

frappe.db.commit()
```

**Verification:** `SELECT COUNT(*) FROM tabUser WHERE role_profile='Haritha: Employee'` matches intake count.

---

## Step 11 — Populate `leave_approver` based on dept heads

```python
import frappe

# For each Employee, set leave_approver = Department's leave_approver
for emp in frappe.get_all("Employee", filters={"status": "Active"}, fields=["name", "department"]):
    if not emp.department:
        continue
    approver = frappe.db.get_value("Department", emp.department, "leave_approver")
    if approver:
        e = frappe.get_doc("Employee", emp.name)
        e.leave_approver = approver
        e.save(ignore_permissions=True)

frappe.db.commit()
```

**Verification:** `SELECT COUNT(*) FROM tabEmployee WHERE status='Active' AND IFNULL(leave_approver,'')=''` should return 0 (or only known exceptions).

---

## Step 12 — Configure User Permissions (dept isolation)

### For Employee role: per-employee Department isolation

```python
import frappe

for emp in frappe.get_all("Employee", filters={"status": "Active"}, fields=["name", "user_id", "department"]):
    if not emp.user_id or not emp.department:
        continue
    # User Permission: this user can only see records for their department
    up = frappe.new_doc("User Permission")
    up.user = emp.user_id
    up.allow = "Department"
    up.for_value = emp.department
    up.insert(ignore_permissions=True)
    
    # User Permission: same for Company
    up2 = frappe.new_doc("User Permission")
    up2.user = emp.user_id
    up2.allow = "Company"
    up2.for_value = "<Client Legal Name>"
    up2.insert(ignore_permissions=True)

frappe.db.commit()
```

**Verification:** `SELECT COUNT(*) FROM tabUser Permission` should be ~2× employee count.

---

## Step 13 — Activate auto-attendance cron

```python
import frappe

# Enable auto-attendance on all Shift Types
frappe.db.sql("""
    UPDATE `tabShift Type`
    SET enable_auto_attendance = 1,
        working_hours_threshold_for_absent = 2.0,
        process_attendance_after = '2025-01-01'
    WHERE name NOT LIKE 'X-%'  -- exclude test shifts
""")

frappe.db.commit()
```

**Verification:** `SELECT COUNT(*) FROM tabShift Type WHERE enable_auto_attendance=1` matches non-test shift count.

---

## Step 14 — Run E2E test with sample users

### Test scenarios (6 minimum)

| # | Scenario | Expected result |
|---|---|---|
| T1 | Employee submits Leave Application → Leave Approver approves → HR Manager sees in dashboard | Leave approved, HRMS notification created |
| T2 | Employee submits Shift Request → Roster Manager approves → HR Manager finalizes | Shift swap approved |
| T3 | Employee checks in via mobile (or mock checkin) → Attendance auto-created | Attendance marked Present (if working_hours >= 2) |
| T4 | Employee tries to view Employee record in different dept | Permission denied |
| T5 | HR User creates new Employee | New Employee visible in HR User's dept list |
| T6 | HR Manager edits HR Settings | Save succeeds; HR User sees updated config |

```python
# Run all 6 tests
import subprocess
result = subprocess.run([
    "bench", "--site", "<client>-prod.duckdns.org",
    "execute", "haritta_hospital.scripts.verify_e2e_six"
], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
```

**Verification:** All 6 tests pass.

---

## Step 15 — Hand over + train

| Task | Owner | Duration |
|---|---|---|
| Walkthrough demo with client HR Manager (90 min) | Implementation lead | 1.5h |
| Train 3 power users (HR Manager + 2 HR Users) on role-specific workflows (4h) | Implementation lead | 4h |
| Train all 211 employees on Employee self-service (leave, attendance view) — 30-min sessions × 11 batches | Implementation lead + HR | 6h |
| Hand over credentials + runbook (this doc + 04.1-deployment.md + 04.2-daily-ops.md + 04.4-incident-response.md) | Implementation lead | 30 min |
| Schedule first DR drill (30 days post go-live) | IT + Implementation lead | (calendar item) |

**Acceptance criteria for go-live:**
- All 211 employees can log in via personal email
- All 6 E2E tests pass
- 2-week shadow run (parallel with old system) shows zero discrepancies
- Client HR Manager signs sign-off doc

---

## Sign-off template

```markdown
## Client Onboarding Sign-off

**Client:** <Client Legal Name>
**Domain:** <client>-prod.duckdns.org
**Go-live date:** YYYY-MM-DD
**Implementation team:** <names>
**Total employees provisioned:** <count>

**Verification:**
- [ ] 6 Haritha Role Profiles present
- [ ] 6 Haritha Workspaces present (all private)
- [ ] 2 active workflows (Leave App + Shift Request)
- [ ] 451+ User Permissions (or count matching N employees × 2)
- [ ] All employees can log in
- [ ] All 6 E2E tests pass
- [ ] SMTP delivers test email
- [ ] Backup runs successfully
- [ ] HR Manager signs below

**Signatures:**

Client HR Manager: ___________________________ Date: __________

Implementation Lead: ___________________________ Date: __________

IT/Infra Lead: ___________________________ Date: __________
```

---

## Variations by industry

| Industry | Key differences | Reference |
|---|---|---|
| **Hospital** (this hospital model) | 24×7 shifts, dept-specific weekly_off override, biometric checkin integration | this hospital project (current site) |
| **College / University** | Academic calendar (July-June), semester-based Holiday List, faculty + staff roles | TBD — adapt Steps 5-9 |
| **Factory / Manufacturing** | Production-line shift rotation, Overtime calculation, contract labour | TBD — adapt Step 5 (3-shift rotation) |
| **Retail chain** | Multi-store, store-level departments, weekly_off varies by store | TBD — adapt Steps 4 + 9 |
| **IT services** | WFH-friendly shifts, leave-heavy, project-based costing | TBD — adapt Step 5 (shorter shifts, more leave types) |

---

## See also

- `00-foundations/00-project-status-2026-09-30.md` — current state
- `06-reference/role-permission-matrix-2026-09-30.md` — role × DocType matrix
- `04.1-deployment.md` — environment provisioning
- `04.2-daily-ops.md` — daily operations runbook
- `04.3-disaster-recovery.md` — DR procedure (run quarterly)
- `04.4-incident-response.md` — incident handling

---

**Sanitization:** All client-identifying strings scrubbed per `AGENTS.md` rule.
**Author:** Phase E subagent (depth 1/5)
**Audience:** Any Processbricks implementation team member picking up a new HRMS engagement.
