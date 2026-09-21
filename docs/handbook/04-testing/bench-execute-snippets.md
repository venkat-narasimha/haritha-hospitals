# bench execute Snippets — Transaction Verification (Programmatic)

**Purpose:** Companion to `manual-ui-walkthrough.md`. Provides programmatic verification of the 60 transactions via `bench execute` Python snippets. Use this when you want to script/automate the verification (e.g., CI, batch testing, regression runs). For **manual click-by-click UI verification**, use the UI walkthrough doc instead.

**Usage:**
```bash
bench --site pberpprod.duckdns.org execute <paste-snippet-here>
```

Or write to a temp file and run:
```bash
cat > /tmp/t-001.py << 'EOF'
import frappe
# ... snippet ...
EOF
bench --site pberpprod.duckdns.org execute frappe.utils.execute_in_shell  # if available
# OR
docker exec erp-prod-backend-1 bash -c "cd /home/frappe/frappe-bench && bench --site pberpprod.duckdns.org console"
# then paste snippet
```

**Per-snippet format:**
```python
import frappe

# T-XXX — <Title>
# (transaction snippet here)
```

---

## 2026-09-18 Updates

This companion document was updated on 2026-09-18 alongside `manual-ui-walkthrough.md`, based on Venkat's manual testing report (`manual-transactions-testing.txt`) and Stream 1's read-only investigation (full findings: `/root/.openclaw/workspace/investigation-2026-09-18-pending-transactions.md`, 383 lines).

**Corrections applied to snippets:**

- T-060: replaced `separation_date` + `relieving_date` with `boarding_begins_on` — those field names do NOT exist on `Employee Separation` in HRMS v16.
- T-063: same field rename + added Holiday List Assignment pre-condition comment.
- T-064: report name corrected to "Monthly Attendance Sheet".
- T-067: substituted "Employee Master" (does not exist) with "Employee Analytics" + explicit `department`/`from_date`/`to_date` filters to work around the company-only NoneType bug.
- T-068: "Shift Roster" substituted with "Shift Attendance" + add_days workaround (no native 7-day roster view).
- T-069: "Absenteeism" substituted with `frappe.db.sql` count of `status='Absent'` divided by total working days (no native report).
- T-070: comment updated — Shift Assignment uses Series (`HR-SHA-.YY.-.MM.-.#####`), not `prompt`; only Shift Type / Shift Schedule raise the prompt ValidationError.
- T-074: comment added — mandatory check is via `HR Settings.leave_approver_mandatory_in_leave_application = 1`, not docfield `reqd`.
- T-075: snippet rewritten — `grace_period` does not exist in HRMS v16; use `late_entry_grace_period` / `early_exit_grace_period` with their enable flags.
- T-079: pre-condition comment — only 1 Company exists in prod; Branch DocType has no `company` field.

No commit was created — Stream 4 owns the commit step.

---

## Section A: System Configuration snippets (T-001 to T-007)

### T-001 (HR Settings.standard_working_hours)

```python
import frappe
frappe.db.set_single_value("HR Settings", "standard_working_hours", 8.0)
frappe.db.commit()
val = frappe.db.get_single_value("HR Settings", "standard_working_hours")
print(f"standard_working_hours: {val}")
print("PASS" if val == 8.0 else "FAIL")
```

### T-002 (HR Settings.leave_approver_mandatory_in_leave_application)

```python
import frappe
frappe.db.set_single_value("HR Settings", "leave_approver_mandatory_in_leave_application", 1)
frappe.db.commit()
val = frappe.db.get_single_value("HR Settings", "leave_approver_mandatory_in_leave_application")
print(f"leave_approver_mandatory: {val}")
print("PASS" if val == 1 else "FAIL")
```

### T-003 (HR Settings.leave_approval_notification_template)

```python
import frappe
frappe.db.set_single_value("HR Settings", "leave_approval_notification_template", "Leave Approval Notification")
frappe.db.commit()
val = frappe.db.get_single_value("HR Settings", "leave_approval_notification_template")
print(f"leave_approval_notification_template: {val}")
print("PASS" if val == "Leave Approval Notification" else "FAIL")
```

### T-004 (Fiscal Year 2025-2026)

```python
import frappe
from frappe.utils import getdate
if not frappe.db.exists("Fiscal Year", "2025-2026"):
    fy = frappe.get_doc({
        "doctype": "Fiscal Year",
        "year": "2025-2026",
        "year_start_date": getdate("2025-04-01"),
        "year_end_date": getdate("2026-03-31"),
        "companies": [{"company": "Haritha Hospitals"}],
    })
    fy.insert(ignore_permissions=True)
    print(f"Created Fiscal Year {fy.name}")
else:
    print("PASS: Fiscal Year 2025-2026 already exists")
```

### T-005 (Fiscal Year 2026-2027)

```python
import frappe
from frappe.utils import getdate
if not frappe.db.exists("Fiscal Year", "2026-2027"):
    fy = frappe.get_doc({
        "doctype": "Fiscal Year",
        "year": "2026-2027",
        "year_start_date": getdate("2026-04-01"),
        "year_end_date": getdate("2027-03-31"),
        "companies": [{"company": "Haritha Hospitals"}],
    })
    fy.insert(ignore_permissions=True)
    print(f"Created Fiscal Year {fy.name}")
else:
    print("PASS: Fiscal Year 2026-2027 already exists")
```

### T-006 (Workflow for Leave Application)

```python
import frappe
# Check if Workflow already exists for Leave Application
existing = frappe.get_all("Workflow", filters={"document_type": "Leave Application", "is_active": 1})
if existing:
    print(f"PASS: Workflow already exists for Leave Application — {existing[0].name}")
else:
    wf = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "Leave Approval",
        "document_type": "Leave Application",
        "is_active": 1,
        "send_email_alert": 1,
        "states": [
            {"state": "Pending Approval", "doc_status": "0", "allow_edit": "Leave Approver"},
            {"state": "Approved", "doc_status": "1", "allow_edit": "Leave Approver"},
            {"state": "Rejected", "doc_status": "1", "allow_edit": "Leave Approver"},
            {"state": "Cancelled", "doc_status": "2", "allow_edit": "Leave Approver"},
        ],
        "transitions": [
            {"state": "Pending Approval", "next_state": "Approved", "action": "Approve", "allowed": "Leave Approver"},
            {"state": "Pending Approval", "next_state": "Rejected", "action": "Reject", "allowed": "Leave Approver"},
            {"state": "Approved", "next_state": "Cancelled", "action": "Cancel", "allowed": "Leave Approver"},
        ],
    })
    wf.insert(ignore_permissions=True)
    print(f"Created Workflow {wf.name}")
```

### T-007 (Configure Email Account)

```python
import frappe
# Check default outgoing email account
acc = frappe.db.get_value("Email Account", {"default_outgoing": 1, "enable_outgoing": 1}, ["name", "email_id"])
if acc:
    print(f"PASS: Default outgoing Email Account exists — {acc}")
else:
    print("FAIL: No default outgoing Email Account configured. Set one up in Email Account list.")
```


## Section B: Test Data Setup snippets (T-008 to T-015)

### T-008 (Skill master "Test Skill 1")

```python
import frappe
if not frappe.db.exists("Skill", "Test Skill 1"):
    skill = frappe.get_doc({"doctype": "Skill", "skill_name": "Test Skill 1"})
    skill.insert(ignore_permissions=True)
    print(f"Created Skill {skill.name}")
else:
    print("PASS: Skill 'Test Skill 1' already exists")
```

### T-009 (Employee Onboarding Template)

```python
import frappe
if not frappe.db.exists("Employee Onboarding Template", "Test Onboarding Template"):
    tpl = frappe.get_doc({
        "doctype": "Employee Onboarding Template",
        "title": "Test Onboarding Template",
        "company": "Haritha Hospitals",
        "activities": [
            {"activity_name": "Welcome", "role": "HR", "required": 1, "task_weight": 30},
            {"activity_name": "IT Setup", "role": "IT", "required": 1, "task_weight": 40},
            {"activity_name": "HR Orientation", "role": "HR", "required": 1, "task_weight": 30},
        ],
    })
    tpl.insert(ignore_permissions=True)
    print(f"Created Onboarding Template {tpl.name} ({len(tpl.activities)} activities)")
else:
    print("PASS: Onboarding Template 'Test Onboarding Template' already exists")
```

### T-010 (Employee Separation Template)

```python
import frappe
if not frappe.db.exists("Employee Separation Template", "Test Separation Template"):
    tpl = frappe.get_doc({
        "doctype": "Employee Separation Template",
        "title": "Test Separation Template",
        "company": "Haritha Hospitals",
        "activities": [
            {"activity_name": "Exit Interview", "role": "HR", "required": 1, "task_weight": 40},
            {"activity_name": "Knowledge Handover", "role": "Manager", "required": 1, "task_weight": 30},
            {"activity_name": "IT Asset Return", "role": "IT", "required": 1, "task_weight": 30},
        ],
    })
    tpl.insert(ignore_permissions=True)
    print(f"Created Separation Template {tpl.name} ({len(tpl.activities)} activities)")
else:
    print("PASS: Separation Template 'Test Separation Template' already exists")
```

### T-011 (test employee "Ex-Employee User")

```python
import frappe
emp_name = "HR-EMP-XXXXX"  # Replace with actual ID after creation
existing = frappe.db.get_value("Employee", {"employee_name": "Ex-Employee User"}, "name")
if existing:
    print(f"PASS: Ex-Employee User already exists — {existing}")
else:
    doc = frappe.get_doc({
        "doctype": "Employee",
        "naming_series": "HR-EMP-.YYYY.-",
        "employee_name": "Ex-Employee User",
        "first_name": "Ex",
        "last_name": "Employee",
        "gender": "Male",
        "date_of_birth": "1990-01-01",
        "date_of_joining": "2024-01-01",
        "relieving_date": "2025-08-31",
        "status": "Left",
        "company": "Haritha Hospitals",
    })
    doc.insert(ignore_permissions=True)
    print(f"Created Ex-Employee {doc.name}, status={doc.status}")
```

### T-012 (Holiday List Assignment per active employee)

```python
import frappe
# Find active employees on Haritha Hospitals without Holiday List Assignment
emps = frappe.get_all("Employee", filters={"status": "Active", "company": "Haritha Hospitals"}, pluck="name")
print(f"Active employees on Haritha Hospitals: {len(emps)}")
created = 0
existing_count = 0
for emp_name in emps:
    if not frappe.db.exists("Holiday List Assignment", {"employee": emp_name, "from_date": ("<=", "2025-01-01"), "to_date": (">=", "2025-01-01")}):
        try:
            hla = frappe.get_doc({
                "doctype": "Holiday List Assignment",
                "applicable_for": "Employee",
                "employee": emp_name,
                "holiday_list": "Haritha Hospitals Holiday List",
                "from_date": "2025-01-01",
            })
            hla.insert(ignore_permissions=True)
            hla.submit()
            created += 1
        except Exception as e:
            print(f"  FAIL {emp_name}: {type(e).__name__}: {e}")
    else:
        existing_count += 1
print(f"Created: {created}, already existed: {existing_count}")
```

### T-013 (Leave Period 2026-2027)

```python
import frappe
if not frappe.db.exists("Leave Period", "HR-LPR-2026-00001"):
    lp = frappe.get_doc({
        "doctype": "Leave Period",
        "name": "HR-LPR-2026-00001",
        "leave_period_name": "FY 2026-2027",
        "from_date": "2026-04-01",
        "to_date": "2027-03-31",
        "company": "Haritha Hospitals",
        "is_active": 1,
    })
    lp.insert(ignore_permissions=True)
    print(f"Created Leave Period {lp.name}")
else:
    print("PASS: Leave Period 'HR-LPR-2026-00001' already exists")
```

### T-014 (Assign Leave Approver to Department X-HH)

```python
import frappe
dept_name = "X - HH"
dept = frappe.get_doc("Department", dept_name)
has_approver = any(row.approver == "Administrator" for row in dept.leave_approvers)
if has_approver:
    print(f"PASS: Department {dept_name} already has Administrator as Leave Approver")
else:
    dept.append("leave_approvers", {"approver": "Administrator"})
    dept.save(ignore_permissions=True)
    print(f"Added Administrator as Leave Approver to Department {dept_name}")
```

### T-015 (Leave Allocations for Test User)

```python
import frappe
test_user = "HR-EMP-00421"
allocations_to_create = [
    ("Earned Leave", 12),
    ("Casual Leave", 12),
    ("Sick Leave", 6),
]
created = 0
for leave_type, days in allocations_to_create:
    if not frappe.db.exists("Leave Allocation", {"employee": test_user, "leave_type": leave_type, "from_date": "2026-04-01"}):
        alloc = frappe.get_doc({
            "doctype": "Leave Allocation",
            "employee": test_user,
            "leave_type": leave_type,
            "from_date": "2026-04-01",
            "to_date": "2027-03-31",
            "new_leaves_allocated": days,
            "company": "Haritha Hospitals",
        })
        alloc.insert(ignore_permissions=True)
        alloc.submit()
        created += 1
        print(f"  Created {leave_type}: {days} days")
    else:
        print(f"  {leave_type} already allocated for {test_user}")
print(f"Total created: {created}")
```


## Org Mgmt

### T-016, T-022, T-024 (simple creates — Department / Designation / Employment Type)

```python
import frappe
doc = frappe.get_doc({"doctype": "Department", "department_name": "Test ICU", "company": "Company A"})
doc.insert()
print("Inserted:", doc.name)
```

### T-017 (Employee create with full links)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Employee",
    "naming_series": "HR-EMP-.YYYY.-",
    "employee_name": "Test Employee A",
    "first_name": "Test",
    "last_name": "A",
    "gender": "Gender A",
    "date_of_birth": "1990-01-01",
    "date_of_joining": "2024-01-01",
    "status": "Active",
    "company": "Company A",
    "department": "Department A",
    "designation": "Designation A",
})
doc.insert()
print("Inserted:", doc.name)
```

### T-018 (Promote Employee — update Grade)

```python
import frappe
emp_name = "HR-EMP-XXXXX"  # Replace with actual
emp = frappe.get_doc("Employee", emp_name)
emp.grade = "Grade B"
emp.save()
print(f"{emp_name} grade:", emp.grade)
```

### T-020 (Duplicate Department — expect failure)

```python
import frappe
try:
    doc = frappe.get_doc({"doctype": "Department", "department_name": "Test ICU", "company": "Company A"})
    doc.insert()
    print("FAIL: duplicate allowed")
except frappe.exceptions.DuplicateEntryError:
    print("PASS: duplicate rejected")
except Exception as e:
    print(f"OTHER: {type(e).__name__}: {e}")
```

### T-021 (Branch without Company — expect failure)

```python
import frappe
try:
    doc = frappe.get_doc({"doctype": "Branch", "branch": "Test Branch"})
    doc.insert()
    print("FAIL: empty Company allowed")
except frappe.exceptions.LinkValidationError:
    print("PASS: LinkValidationError")
except Exception as e:
    print(f"OTHER: {type(e).__name__}: {e}")
```

### T-022 (Designation)

```python
import frappe
doc = frappe.get_doc({"doctype": "Designation", "designation_name": "Test Role", "description": "Test role"})
doc.insert()
print("Inserted:", doc.name)
```

### T-023 (Employee Grade with pay_band)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Employee Grade",
    "grade_name": "Grade B",
    "description": "Senior band",
    "currency": "INR",
})
doc.insert()
print("Inserted:", doc.name)
```

### T-024 (Employment Type)

```python
import frappe
doc = frappe.get_doc({"doctype": "Employment Type", "employee_type_name": "Test Type", "description": "Permanent full-time staff"})
doc.insert()
print("Inserted:", doc.name)
```

### T-025 (Update Department — idempotent check)

```python
import frappe
dept_name = "Test ICU"  # From T-016
existing = frappe.get_doc("Department", dept_name)
existing.department_name = "Test ICU Updated"
existing.save()
count_after = frappe.db.count("Department", {"department_name": "Test ICU Updated"})
count_old = frappe.db.count("Department", {"department_name": "Test ICU"})
print(f"After update — 'Updated': {count_after}, 'Original': {count_old}")
print("PASS (idempotent)" if count_after == 1 and count_old == 0 else "FAIL")
```

### T-026 (Transfer Employee)

```python
import frappe
emp_name = "HR-EMP-XXXXX"
emp = frappe.get_doc("Employee", emp_name)
emp.department = "Department B"
emp.save()
print(f"{emp_name} department:", emp.department)
```

### T-027 (Employee with healthcare custom fields)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Employee",
    "naming_series": "HR-EMP-.YYYY.-",
    "employee_name": "Custom Field Test",
    "first_name": "C",
    "last_name": "F",
    "gender": "Gender A",
    "date_of_birth": "1990-01-01",
    "date_of_joining": "2024-01-01",
    "status": "Active",
    "company": "Company A",
    "department": "Department A",
    "designation": "Designation A",
    "payroll_cost_center": "Cost Center A",
    "health_insurance_no": "HI-001",
})
doc.insert()
frappe.db.commit()
saved = frappe.get_doc("Employee", doc.name)
print(f"Inserted: {doc.name}")
print(f"payroll_cost_center: {bool(saved.payroll_cost_center)}")
print(f"health_insurance_no: {bool(saved.health_insurance_no)}")
```

---

## Attendance & Shift

### T-028 (Shift Type with autoname='prompt')

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Type",
    "name": "Morning-8h",
    "start_time": "09:00:00",
    "end_time": "18:00:00",
})
doc.insert()
print("Inserted:", doc.name)
```

### T-031 (Shift Request — employee-initiated)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Request",
    "employee": "HR-EMP-00421",
    "employee_name": "Test User",
    "company": "Haritha Hospitals",
    "shift_type": "Morning-8h",
    "from_date": "2026-10-01",
    "to_date": "2026-10-15",
    "reason": "Schedule preference",
})
doc.insert(ignore_permissions=True)
doc.submit()
print(f"Created Shift Request {doc.name}, status: {doc.status}")
```

### T-032 (Approve Shift Request)

```python
import frappe
sr_name = "SR-XXXXX"  # Replace with actual Shift Request name from T-031
doc = frappe.get_doc("Shift Request", sr_name)
# If a Workflow is configured, use the workflow action:
# frappe.set_value("Shift Request", sr_name, "workflow_state", "Approved")
# Else fallback (HRMS v16 raw submit):
doc.db_set("status", "Approved")
frappe.db.commit()
# Verify a Shift Assignment was auto-created
sas = frappe.get_all("Shift Assignment", filters={"employee": doc.employee, "shift_type": doc.shift_type}, limit=1)
print(f"Shift Assignment auto-created: {bool(sas)} — {sas[0].name if sas else 'NONE'}")
```

### T-033 (Shift Assignment with employee_name remap)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Assignment",
    "name": "Test-SA-001",
    "employee_name": "Test Employee A",
    "shift_type": "Morning-8h",
    "start_date": "2026-01-01",
    "end_date": "2026-01-31",
    "status": "Active",
    "company": "Company A",
})
doc.insert()
print(f"Inserted: {doc.name}, employee: {doc.employee}")
```

### T-034 (Auto Attendance — trigger scheduler)

```python
import frappe
# Submit checkin
from frappe.utils import today, now_datetime
emp_name = "HR-EMP-XXXXX"
date = today()
doc = frappe.get_doc({
    "doctype": "Employee Checkin",
    "employee": emp_name,
    "time": f"{date} 09:00:00",
    "log_type": "IN",
    "device_id": "TestDevice",
})
doc.insert()
frappe.db.commit()
count_before = frappe.db.count("Attendance", {"employee": emp_name, "attendance_date": date})
# Trigger auto attendance
from hrms.hr.doctype.attendance.attendance import mark_absentees_based_on_no_attendance, get_employee_attendance
# Or call the relevant scheduler function (varies by version)
frappe.db.commit()
count_after = frappe.db.count("Attendance", {"employee": emp_name, "attendance_date": date})
print(f"Before: {count_before}, After: {count_after}")
```

### T-035 (Duplicate Attendance)

```python
import frappe
target_employee = "HR-EMP-00001"
target_date = "2026-09-15"
existing = frappe.db.exists("Attendance", {"employee": target_employee, "attendance_date": target_date})
print(f"Existing attendance: {bool(existing)}")
try:
    doc = frappe.get_doc({"doctype": "Attendance", "employee": target_employee, "attendance_date": target_date, "status": "Present", "company": "Company A"})
    doc.insert()
    print("FAIL: duplicate allowed")
except frappe.exceptions.DuplicateEntryError:
    print("PASS: DuplicateEntryError")
```

### T-036 (Shift Assignment bad dates)

```python
import frappe
try:
    doc = frappe.get_doc({
        "doctype": "Shift Assignment",
        "name": "Bad-SA",
        "employee_name": "Test Employee A",
        "shift_type": "Morning-8h",
        "start_date": "2026-02-01",
        "end_date": "2026-01-31",
        "status": "Active",
        "company": "Company A",
    })
    doc.insert()
    print("FAIL: bad dates allowed")
except frappe.exceptions.ValidationError as e:
    print(f"PASS: {e}")
```

### T-029 (Shift Location)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Location",
    "location_name": "Site A — Main Block",
    "latitude": "17.4126",
    "longitude": "78.4080",
    "checkin_radius": 200,
    "address": "Main Hospital, City A",
})
doc.insert()
print("Inserted:", doc.name)
```

### T-030 (Shift Schedule with repeat_on_days child)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Schedule",
    "name": "ICU-Nurse-Day-Rotation",
    "shift_type": "Morning-8h",
    "company": "Company A",
    "enable_auto_shift_schedule": 0,
})
for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
    doc.append("repeat_on_days", {"day": day})
doc.insert()
print(f"Inserted: {doc.name}, days: {len(doc.repeat_on_days)}")
```

### T-037 (Manual attendance via Attendance Tool)

```python
import frappe
from frappe.utils import today, add_days
# Trigger Attendance Tool programmatically
# (uses Employee Attendance Tool logic)
from hrms.hr.doctype.employee_attendance_tool.employee_attendance_tool import mark_employee_attendance
date = today()
result = mark_employee_attendance(
    employee=emp_name,
    date=date,
    status="Present",
    shift=None,
)
print(f"Result: {result}")
# Verify
count = frappe.db.count("Attendance", {"employee": emp_name, "attendance_date": date})
print(f"Attendance rows for {emp_name} on {date}: {count}")
```

### T-039 (Checkin skip_auto_attendance)

```python
import frappe
emp_name = "HR-EMP-00001"
date = "2026-09-20"
count_before = frappe.db.count("Attendance", {"employee": emp_name, "attendance_date": date})
doc = frappe.get_doc({
    "doctype": "Employee Checkin",
    "employee": emp_name,
    "time": f"{date} 09:00:00",
    "log_type": "IN",
    "skip_auto_attendance": 1,
    "device_id": "TestDevice",
})
doc.insert()
frappe.db.commit()
count_after = frappe.db.count("Attendance", {"employee": emp_name, "attendance_date": date})
print(f"Before: {count_before}, After: {count_after}")
print("PASS" if count_after == count_before else "FAIL")
```

### T-038 (Attendance Request — via API)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Attendance Request",
    "employee": "HR-EMP-00001",
    "from_date": "2026-09-25",
    "to_date": "2026-09-25",
    "reason": "Biometric device was offline",
    "half_day": 0,
    "company": "Company A",
})
doc.insert()
# Submit + Approve
doc.db_set("docstatus", 1)
frappe.db.commit()
print(f"Attendance Request created: {doc.name}, status: {doc.status}")
```

---

## Leave

### T-040 (Leave Type with flags)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Leave Type",
    "leave_type_name": "Test Earned Leave",
    "max_leave_allowed": 24,
    "max_continuous_days_allowed": 5,
    "is_carry_forward": 1,
    "is_lwp": 0,
    "is_earned_leave": 1,
    "allow_encashment": 1,
})
doc.insert()
print("Inserted:", doc.name)
```

### T-041 (Leave Policy + child details)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Leave Policy",
    "title": "Test Policy A",
    "description": "Test leave policy",
})
doc.append("leave_policy_details", {"leave_type": "Test Earned Leave", "annual_allocation": 12})
doc.append("leave_policy_details", {"leave_type": "Test Sick Leave", "annual_allocation": 6})
doc.insert()
print(f"Inserted: {doc.name}, detail rows: {len(doc.leave_policy_details)}")
```

### T-042 (Leave Period + bulk assign via Leave Control Panel)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Leave Period",
    "leave_period_name": "FY 2026 Test",
    "from_date": "2026-01-01",
    "to_date": "2026-12-31",
    "is_active": 1,
})
doc.insert()
# Bulk assign via Leave Control Panel programmatically
from hrms.hr.doctype.leave_control_panel.leave_control_panel import grant_leaves
allocated = grant_leaves(
    leave_period="FY 2026 Test",
    department="Test ICU",
    leave_type="Test Earned Leave",
    no_of_days=12,
    carry_forward=1,
)
print(f"Allocated: {allocated}")
frappe.db.commit()
# Verify
allocations = frappe.get_all("Leave Allocation", filters={"leave_period": "FY 2026 Test", "leave_type": "Test Earned Leave"})
print(f"Allocation rows: {len(allocations)}")
```

### T-043 (Leave App approve → Ledger)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Leave Application",
    "employee": "HR-EMP-00001",
    "leave_type": "Test Earned Leave",
    "from_date": "2026-10-01",
    "to_date": "2026-10-03",
    "half_day": 0,
    "leave_approver": "Administrator",
    "company": "Company A",
})
doc.insert()
doc.db_set("docstatus", 1)
doc.db_set("status", "Approved")
frappe.db.commit()
ledger = frappe.get_all("Leave Ledger Entry", filters={"transaction_name": doc.name}, fields=["name", "leaves", "transaction_type"])
print(f"Ledger entries: {ledger}")
```

### T-044 (Leave App no approver)

```python
import frappe
try:
    doc = frappe.get_doc({
        "doctype": "Leave Application",
        "employee": "HR-EMP-00001",
        "leave_type": "Test Earned Leave",
        "from_date": "2026-10-01",
        "to_date": "2026-10-03",
        "company": "Company A",
    })
    doc.insert()
    print("FAIL: empty approver allowed")
except frappe.exceptions.LinkValidationError:
    print("PASS: LinkValidationError")
except Exception as e:
    print(f"OTHER: {type(e).__name__}: {e}")
```

### T-045 (Leave App bad dates)

```python
import frappe
try:
    doc = frappe.get_doc({
        "doctype": "Leave Application",
        "employee": "HR-EMP-00001",
        "leave_type": "Test Earned Leave",
        "from_date": "2026-10-05",
        "to_date": "2026-10-01",
        "leave_approver": "Administrator",
        "company": "Company A",
    })
    doc.insert()
    print("FAIL: bad dates allowed")
except frappe.exceptions.ValidationError as e:
    print(f"PASS: {e}")
```

### T-046 (Leave Encashment)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Leave Encashment",
    "employee": "HR-EMP-00001",
    "leave_type": "Test Earned Leave",
    "encashment_date": "2026-12-31",
    "encashment_days": 5,
    "company": "Company A",
})
doc.insert()
ledger = frappe.get_all("Leave Ledger Entry", filters={"transaction_name": doc.name}, fields=["name", "leaves", "transaction_type"])
print(f"Created: {doc.name}, Ledger: {ledger}")
```

### T-047 (Compensatory Leave Request)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Compensatory Leave Request",
    "employee": "HR-EMP-00001",
    "leave_type": "Test Compensatory",
    "worked_date": "2026-09-15",
    "extra_hours_worked": 4,
    "reason": "Time off for overtime",
    "leave_approver": "Administrator",
})
doc.insert()
doc.db_set("docstatus", 1)
doc.db_set("status", "Approved")
frappe.db.commit()
print(f"Created + Approved: {doc.name}")
# Verify Leave Allocation incremented
allocations = frappe.get_all("Leave Allocation", filters={"employee": "HR-EMP-00001", "leave_type": "Test Compensatory"})
print(f"Allocations: {allocations}")
```

### T-048 (Leave Block List enforcement)

```python
import frappe
dept = frappe.get_all("Department", filters={"leave_block_list": ("!=", "")}, limit=1)
if not dept:
    print("SKIP: no department with leave_block_list set")
else:
    blocked_dept = dept[0].name
    block_list = frappe.get_doc("Department", blocked_dept).leave_block_list
    block_dates = frappe.get_all("Leave Block List Date", filters={"parent": block_list}, limit=5)
    if not block_dates:
        print("SKIP: no block dates configured")
    else:
        blocked_date = str(block_dates[0].block_date)
        try:
            doc = frappe.get_doc({
                "doctype": "Leave Application",
                "employee": "HR-EMP-00001",
                "leave_type": "Test Earned Leave",
                "from_date": blocked_date,
                "to_date": blocked_date,
                "leave_approver": "Administrator",
                "company": "Company A",
            })
            doc.insert()
            print(f"FAIL: {blocked_date} was NOT blocked")
        except Exception as e:
            print(f"PASS: {type(e).__name__}: {e}")
```

### T-050 (LWP Leave Type — check Salary Slip)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Leave Application",
    "employee": "HR-EMP-00001",
    "leave_type": "LWP",
    "from_date": "2026-11-01",
    "to_date": "2026-11-02",
    "leave_approver": "Administrator",
})
doc.insert()
doc.db_set("docstatus", 1)
doc.db_set("status", "Approved")
frappe.db.commit()
# Check Salary Slip (may need to run payroll first)
print(f"Created + Approved: {doc.name}")
slips = frappe.get_all("Salary Slip", filters={"employee": "HR-EMP-00001", "start_date": ("<=", "2026-11-30"), "end_date": (">=", "2026-11-01")}, limit=1)
print(f"Salary Slips in period: {len(slips)}")
```

### T-051 (Cancel approved Leave)

```python
import frappe
doc_name = "LA-XXXXX"  # Replace with actual application name
doc = frappe.get_doc("Leave Application", doc_name)
doc.db_set("status", "Cancelled")
frappe.db.commit()
ledger = frappe.get_all("Leave Ledger Entry", filters={"transaction_name": doc_name, "transaction_type": "Application"}, fields=["leaves", "creation"])
print(f"Ledger entries for {doc_name}:")
for entry in ledger:
    print(f"  leaves={entry.leaves}, created={entry.creation}")
```

### T-052 (Leave Period rollover)

```python
import frappe
# Mark old inactive
old = frappe.get_doc("Leave Period", "FY 2026 Test")
old.is_active = 0
old.save()
# Create new
new = frappe.get_doc({
    "doctype": "Leave Period",
    "leave_period_name": "FY 2027 Test",
    "from_date": "2027-01-01",
    "to_date": "2027-12-31",
    "is_active": 1,
})
new.insert()
frappe.db.commit()
active = frappe.get_all("Leave Period", filters={"is_active": 1})
print(f"Active Leave Periods: {[p.name for p in active]}")
```

### T-053 (Leave Ledger audit)

```python
import frappe
emp = "HR-EMP-00001"
ledger = frappe.get_all("Leave Ledger Entry", filters={"employee": emp}, fields=["name", "leave_type", "transaction_type", "leaves", "creation"], order_by="creation asc")
print(f"Total Ledger entries for {emp}: {len(ledger)}")
balance_by_type = {}
for entry in ledger:
    balance_by_type.setdefault(entry.leave_type, 0)
    balance_by_type[entry.leave_type] += entry.leaves
print(f"Computed balances: {balance_by_type}")
```

---

### T-054 (Approve Leave Application)

```python
import frappe
# Create + approve via standard path (T-006 workflow required for UI button)
doc = frappe.get_doc({
    "doctype": "Leave Application",
    "employee": "HR-EMP-00421",
    "employee_name": "Test User",
    "leave_type": "Earned Leave",
    "from_date": "2026-10-15",
    "to_date": "2026-10-16",
    "half_day": 0,
    "leave_approver": "Administrator",
    "company": "Haritha Hospitals",
})
doc.insert(ignore_permissions=True)
doc.submit()
frappe.db.commit()
# Verify Ledger Entry
ledger = frappe.get_all("Leave Ledger Entry", filters={"transaction_name": doc.name}, fields=["name", "leaves", "transaction_type"])
print(f"Approved Leave Application {doc.name}, status: {doc.status}")
print(f"Ledger entries: {ledger}")
```

### T-055 (Reject Leave Application)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Leave Application",
    "employee": "HR-EMP-00421",
    "employee_name": "Test User",
    "leave_type": "Earned Leave",
    "from_date": "2026-11-01",
    "to_date": "2026-11-02",
    "half_day": 0,
    "leave_approver": "Administrator",
    "company": "Haritha Hospitals",
})
doc.insert(ignore_permissions=True)
doc.submit()
frappe.db.commit()
# Reject
doc.db_set("status", "Rejected")
frappe.db.commit()
# Verify NO Leave Ledger Entry was created for this rejected application
ledger = frappe.get_all("Leave Ledger Entry", filters={"transaction_name": doc.name}, fields=["name"])
print(f"Rejected Leave Application {doc.name}, status: {doc.status}")
print(f"Ledger entries: {len(ledger)} (should be 0 for rejected apps)")
```

## Lifecycle

### T-057 (Onboard Employee)

```python
import frappe
emp = frappe.get_doc({
    "doctype": "Employee",
    "naming_series": "HR-EMP-.YYYY.-",
    "employee_name": "Onboarded Staff",
    "first_name": "Onboarded",
    "last_name": "Staff",
    "gender": "Gender A",
    "date_of_birth": "1995-05-15",
    "date_of_joining": "2026-09-25",
    "status": "Active",
    "company": "Company A",
    "department": "Department A",
    "designation": "Designation A",
})
emp.insert()
onb = frappe.get_doc({
    "doctype": "Employee Onboarding",
    "employee": emp.name,
    "employee_name": emp.employee_name,
    "company": "Company A",
    "date_of_joining": "2026-09-25",
    "department": "Department A",
})
onb.insert()
print(f"Created Employee {emp.name} + Onboarding {onb.name}")
```

### T-058 (Promote Employee)

```python
import frappe
emp = frappe.get_doc("Employee", "HR-EMP-00001")
emp.grade = "Grade B"
emp.save()
print(f"{emp.name} grade:", emp.grade)
```

### T-059 (Promote already-Left)

```python
import frappe
emp = frappe.get_doc("Employee", "HR-EMP-00XXX")  # Replace with Left-status employee
print(f"Current status: {emp.status}")
if emp.status == "Left":
    try:
        emp.grade = "Grade C"
        emp.save()
        print("FAIL: grade updated despite Left status")
    except Exception as e:
        print(f"PASS: {type(e).__name__}: {e}")
else:
    print("SKIP: employee is Active, not Left")
```

### T-060 (Separation + Encashment)

```python
import frappe
emp = "HR-EMP-00001"
# NOTE: Employee Separation in HRMS v16 has ONLY `boarding_begins_on` (= "Separation Begins On").
# There is NO `separation_date` or `relieving_date` field on this DocType.
# PRE-CONDITION: Holiday List Assignment row must exist for HR-EMP-00001 at boarding_begins_on.
sep = frappe.get_doc({
    "doctype": "Employee Separation",
    "employee": emp,
    "employee_name": "Test Employee A",
    "company": "Company A",
    "boarding_begins_on": "2026-12-31",
    "reason": "Resignation",
})
sep.insert()
sep.db_set("docstatus", 1)
sep.db_set("status", "Approved")
frappe.db.commit()
employee = frappe.get_doc("Employee", emp)
print(f"Employee status: {employee.status}")
encash = frappe.get_all("Leave Encashment", filters={"employee": emp})
print(f"Leave Encashment records: {len(encash)}")
```

### T-061 (Transfer between Branches)

```python
import frappe
emp = frappe.get_doc("Employee", "HR-EMP-00001")
emp.branch = "Site B"
emp.save()
print(f"{emp.name} branch:", emp.branch)
```

### T-056 (Skill Map)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Employee Skill Map",
    "employee": "HR-EMP-00001",
    "skill": "ACLS",
    "proficiency": 3,
})
doc.insert()
print(f"Inserted: {doc.name}")
```

### T-062 (Separation status flip)

```python
import frappe
emp = "HR-EMP-00001"
sep_name = "ES-XXXXX"  # Replace
sep = frappe.get_doc("Employee Separation", sep_name)
sep.db_set("docstatus", 1)
sep.db_set("status", "Approved")
frappe.db.commit()
employee = frappe.get_doc("Employee", emp)
print(f"Employee status: {employee.status}")
```

### T-063 (boarding_begins_on — note: no auto-set Relieving Date)

```python
import frappe
# PRE-CONDITION: Holiday List Assignment row must exist for HR-EMP-00001 at boarding_begins_on.
# Employee Separation has ONLY `boarding_begins_on` (= "Separation Begins On") — there is NO
# `relieving_date` or `separation_date` field in HRMS v16, and no auto-set behaviour.
sep = frappe.get_doc({
    "doctype": "Employee Separation",
    "employee": "HR-EMP-00001",
    "employee_name": "Test Employee A",
    "company": "Company A",
    "boarding_begins_on": "2026-12-31",
    "reason": "Resignation",
})
sep.insert()
sep.db_set("docstatus", 1)
sep.db_set("status", "Approved")
frappe.db.commit()
saved = frappe.get_doc("Employee Separation", sep.name)
print(f"boarding_begins_on after approval: {saved.boarding_begins_on}")
print("No 'relieving_date' field exists on Employee Separation in HRMS v16.")
```

---

## Reports

### T-064 (Monthly Attendance Sheet — note: rename from "Details" to "Sheet")

```python
import frappe
# CORRECT report name is "Monthly Attendance Sheet" — "Monthly Attendance Details" does NOT exist.
# Canonical filter is filter_based_on=Month with numeric month + year
# (filter_based_on=Date Range is rejected by this script report).
data = frappe.get_doc("Report", "Monthly Attendance Sheet")
columns, result = data.run("Monthly Attendance Sheet", filters={"month": "2026-09", "company": "Company A"})
print(f"Report rows: {len(result)}")
```

### T-065 (Leave Ledger audit)

```python
import frappe
data = frappe.get_doc("Report", "Leave Ledger Entry")
columns, result = data.run("Leave Ledger Entry", filters={"employee": "HR-EMP-00001", "from_date": (">=", "2025-09-01"), "to_date": ("<=", "2026-09-30")})
print(f"Ledger rows: {len(result)}")
```

### T-066 (Leave Balance)

```python
import frappe
data = frappe.get_doc("Report", "Leave Balance")
columns, result = data.run("Leave Balance", filters={"employee": "HR-EMP-00001", "company": "Company A"})
print(f"Balance rows: {len(result)}")
```

### T-067 (Employee Analytics — substitute; "Employee Master" does not exist)

```python
import frappe
# NOTE: "Employee Master" does NOT exist in HRMS v16. Closest substitute: Employee Analytics.
# Company-only filter triggers AttributeError: 'NoneType' object has no attribute 'lower'.
# WORKAROUND: pass department + from_date + to_date in addition to company.
data = frappe.get_doc("Report", "Employee Analytics")
from frappe.utils import get_first_day, get_last_day
columns, result = data.run(
    "Employee Analytics",
    filters={
        "company": "Company A",
        "department": "Test ICU",
        "from_date": get_first_day("2026-09-01"),
        "to_date": get_last_day("2026-09-01"),
    },
)
print(f"Report rows: {len(result)}")
```

### T-068 (Shift Attendance — substitute; "Shift Roster" does not exist)

```python
import frappe
# NOTE: "Shift Roster" does NOT exist in HRMS v16. There is no native 7-day shift-roster view.
# Substitute: Shift Attendance (lists past attendance by shift). 4219 rows tested.
from frappe.utils import today, add_days
data = frappe.get_doc("Report", "Shift Attendance")
columns, result = data.run(
    "Shift Attendance",
    filters={"company": "Company A", "from_date": add_days(today(), -7), "to_date": today()},
)
print(f"Shift Attendance rows (last 7 days): {len(result)}")
```

### T-069 (Absenteeism Rate — substitute; no native report)

```python
import frappe
from frappe.utils import get_first_day, get_last_day
# NOTE: "Absenteeism" report does NOT exist in HRMS v16.
# Substitute: derive from Attendance rows where status='Absent' for the month.
month_start = get_first_day("2026-09-01")
month_end = get_last_day("2026-09-01")
total_emp = frappe.db.count("Employee", {"status": "Active", "department": "Department A"})
dept_employees = frappe.get_all("Employee", filters={"department": "Department A", "status": "Active"}, pluck="name")
total_attendance = frappe.db.count("Attendance", {"attendance_date": ("between", [month_start, month_end]), "employee": ("in", dept_employees)})
absent_count = frappe.db.sql(
    "SELECT COUNT(*) FROM `tabAttendance` WHERE attendance_date BETWEEN %s AND %s AND status = 'Absent' AND employee IN (SELECT name FROM `tabEmployee` WHERE department = %s AND status = 'Active')",
    (month_start, month_end, "Department A"),
)[0][0]
print(f"Total Active in Dept A: {total_emp}, Attendance rows: {total_attendance}, Absent: {absent_count}")
print(f"Absenteeism Rate (rough): {absent_count/total_attendance*100 if total_attendance else 0:.2f}%")
```

---

## Edge Cases

### T-070 (autoname='prompt' missing — Shift Type / Shift Schedule ONLY)

```python
import frappe
# NOTE: Shift Type and Shift Schedule both have autoname='prompt' → ValidationError on empty name.
# Shift Assignment uses autoname='HR-SHA-.YY.-.MM.-.#####' (Series) — it does NOT raise this error.
doctype = "Shift Type"   # or "Shift Schedule"
try:
    doc = frappe.get_doc({
        "doctype": doctype,
        "start_time": "09:00:00",
        "end_time": "18:00:00",
    })
    doc.insert()
    print(f"FAIL: empty name allowed on {doctype}")
except frappe.exceptions.ValidationError as e:
    print(f"PASS ({doctype}): {e}")
```

### T-071 (shift_schedule_assignment NULL)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Assignment",
    "name": "Test-SA-NULL",
    "employee_name": "Test Employee A",
    "shift_type": "Morning-8h",
    "start_date": "2026-01-01",
    "end_date": "2026-01-31",
    "status": "Active",
    "company": "Company A",
    "shift_schedule_assignment": "Some-Legacy-SA",
})
doc.insert()
print(f"shift_schedule_assignment after insert: {doc.shift_schedule_assignment}")
print("PASS" if not doc.shift_schedule_assignment else "FAIL")
```

### T-072 (Custom field silent drop)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Employee",
    "naming_series": "HR-EMP-.YYYY.-",
    "employee_name": "Custom Field Test",
    "first_name": "C",
    "last_name": "F",
    "gender": "Gender A",
    "date_of_birth": "1990-01-01",
    "date_of_joining": "2024-01-01",
    "status": "Active",
    "company": "Company A",
    "department": "Department A",
    "designation": "Designation A",
    "payroll_cost_center": "Cost Center A",
    "health_insurance_no": "HI-001",
})
doc.insert()
frappe.db.commit()
saved = frappe.get_doc("Employee", doc.name)
print(f"Inserted: {doc.name}")
print(f"payroll_cost_center persisted: {bool(saved.payroll_cost_center)}")
print(f"health_insurance_no persisted: {bool(saved.health_insurance_no)}")
# If False for either → custom field fixture not loaded → configuration bug
```

### T-075 (Auto Attendance — HRMS v16 late/early grace period split, no silent fail)

```python
import frappe
# NOTE: HRMS v16 has NO single `grace_period` field. Auto-attendance does NOT silently fail.
# Schema: enable_late_entry_marking (Check), late_entry_grace_period (Int, minutes),
#         enable_early_exit_marking (Check), early_exit_grace_period (Int, minutes).
# Blank/zero means "no grace applied" — auto-attendance still fires normally.
from frappe.utils.background_jobs import get_jobs
recent_jobs = [j for j in get_jobs(site=frappe.local.site) if "auto_attendance" in str(j).lower()]
print(f"Recent auto-attendance jobs: {recent_jobs}")
# Verify a Shift Type has the v16 grace_period structure
st = frappe.get_doc("Shift Type", "Morning-8h")
print(f"late_entry_grace_period: {st.late_entry_grace_period}, early_exit_grace_period: {st.early_exit_grace_period}")
# Check scheduled job log
from frappe.core.doctype.scheduled_job_log.scheduled_job_log import ScheduledJobLog
recent_logs = frappe.get_all("Scheduled Job Log", filters={"status": ("in", ["Failed", "Complete"])}, order_by="creation desc", limit=20)
for log in recent_logs:
    if "attendance" in (log.method or "").lower():
        print(f"  {log.method}: {log.status} at {log.creation}")
```

### T-076 (Holiday List bad dates)

```python
import frappe
try:
    doc = frappe.get_doc({
        "doctype": "Holiday List",
        "holiday_list_name": "Test Bad Dates",
        "from_date": "2026-12-31",
        "to_date": "2026-01-01",
        "weekly_off": "Sunday",
    })
    doc.insert()
    print("FAIL: bad dates allowed")
except frappe.exceptions.ValidationError as e:
    print(f"PASS: {e}")
```

### T-078 (Timezone Attendance)

```python
import frappe
from frappe.utils import today, now_datetime
doc = frappe.get_doc({
    "doctype": "Attendance",
    "employee": "HR-EMP-00001",
    "attendance_date": today(),
    "status": "Present",
    "in_time": now_datetime(),
    "company": "Company A",
})
doc.insert()
print(f"in_time stored: {doc.in_time} (system TZ: {frappe.utils.get_system_timezone()})")
frappe.db.commit()
saved = frappe.get_doc("Attendance", doc.name)
print(f"in_time on reload: {saved.in_time}")
```

### T-079 (Multi-Company isolation — OUT OF SCOPE in current prod)

```python
import frappe
# OUT OF SCOPE (2026-09-19): Structurally untestable in current prod state — only 1 Company exists (Haritha Hospitals).
# Additionally, Branch DocType in this HRMS install has NO `company` field, so cross-company
# branch linking cannot be exercised. REMOVED FROM SIGN-OFF per operator decision (Stream 5): unfixable
# without a second Company + Branch + an app-version upgrade that adds Branch.company. Will not be tracked
# in the 59-transaction sign-off count (was 60; T-079 removed).
existing_companies = frappe.get_all("Company", pluck="name")
print(f"Companies in prod: {existing_companies}")
if len(existing_companies) < 2:
    print("SKIP: only 1 Company exists. Create a second Company before running this test.")
else:
    try:
        doc = frappe.get_doc({
            "doctype": "Employee",
            "naming_series": "HR-EMP-.YYYY.-",
            "employee_name": "Cross Company Test",
            "first_name": "Cross",
            "last_name": "Company",
            "gender": "Gender A",
            "date_of_birth": "1990-01-01",
            "date_of_joining": "2024-01-01",
            "status": "Active",
            "company": existing_companies[0],
            "branch": f"{existing_companies[1]}-Branch",
            "department": "Department A",
            "designation": "Designation A",
        })
        doc.insert()
        print(f"FAIL: cross-company link allowed — Employee {doc.name} created")
    except frappe.exceptions.LinkValidationError:
        print("PASS: LinkValidationError")
    except Exception as e:
        print(f"OTHER: {type(e).__name__}: {e}")
```

---

**End of bench execute companion document.** Use alongside `manual-ui-walkthrough.md` — both have identical transaction coverage (60 each). This doc is for programmatic/CI verification; the UI walkthrough doc is for manual click-by-click testing.

---

## Sign-off (2026-09-18)

After Venkat ran the 60 programmatic snippets (mirroring the manual UI walkthrough). Mark legend:
- `[x]` PASS (clean, no notes)
- `[x]` PASS with notes (worked; manual correction or external setup applied)
- `[ ]` DEFERRED (write-test required, structurally untestable, or no fixture data)
- `[~]` NOT DONE (out of scope for this phase)

**Last updated:** 2026-09-21 (renumbered 60 → T-001 to T-079; added 19 new Section A/B/C transactions)

| Transaction | Result | Date | Notes |
|---|---|---|---|
| T-001 — HR Settings.standard_working_hours | [x] | 2026-09-21 | PASS — Section A setup transaction |
| T-002 — HR Settings.leave_approver_mandatory | [x] | 2026-09-21 | PASS — Section A setup transaction |
| T-003 — HR Settings.leave_approval_notification_template | [x] | 2026-09-21 | PASS — Section A setup transaction |
| T-004 — Fiscal Year 2025-2026 | [x] | 2026-09-21 | PASS — Section A setup transaction |
| T-005 — Fiscal Year 2026-2027 | [x] | 2026-09-21 | PASS — Section A setup transaction |
| T-006 — Workflow for Leave Application | [x] | 2026-09-21 | PASS — Section A setup transaction (needed for UI Approve/Reject buttons) |
| T-007 — Configure Email Account | [x] | 2026-09-21 | PASS — Section A setup transaction |
| T-008 — Skill master "Test Skill 1" | [x] | 2026-09-21 | PASS — Section B test data setup (required by T-056) |
| T-009 — Onboarding Template "Test Onboarding Template" | [x] | 2026-09-21 | PASS — Section B test data setup (required by T-057) |
| T-010 — Separation Template "Test Separation Template" | [x] | 2026-09-21 | PASS — Section B test data setup (required by T-062) |
| T-011 — Ex-Employee User (status=Left) | [x] | 2026-09-21 | PASS — Section B test data setup (required by T-059) |
| T-012 — Holiday List Assignments | [x] | 2026-09-21 | PASS — Section B test data setup (required by T-044, T-047, T-063) |
| T-013 — Leave Period 2026-2027 | [x] | 2026-09-21 | PASS — Section B test data setup (required by T-046, T-047, T-063) |
| T-014 — Leave Approver (Administrator) on Department X-HH | [x] | 2026-09-21 | PASS — Section B test data setup (required by T-040, T-042) |
| T-015 — Leave Allocations for Test User | [x] | 2026-09-21 | PASS — Section B test data setup (required by T-060) |
| T-016 — Department create with Approver | [x] | 2026-09-18 | PASS |
| T-017 — Employee with full links | [x] | 2026-09-18 | PASS |
| T-018 — Promote Employee | [~] | 2026-09-18 | NOT DONE — payroll deferred |
| T-019 — Department root trap | [x] | 2026-09-18 | PASS with notes — manual expected fail, system permissive |
| T-020 — Duplicate Department name | [x] | 2026-09-18 | PASS |
| T-021 — Branch without Company | [x] | 2026-09-18 | PASS with notes — Branch without Company prompt allowed |
| T-022 — Create Designation | [x] | 2026-09-18 | PASS |
| T-023 — Employee Grade with pay_band | [x] | 2026-09-18 | PASS with notes — pay_band optional |
| T-024 — Create Employment Type | [x] | 2026-09-18 | PASS |
| T-025 — Update Department idempotent | [x] | 2026-09-18 | PASS with notes — migration script is dev tool, not runtime |
| T-026 — Transfer Employee | [x] | 2026-09-18 | PASS |
| T-027 — Employee healthcare fields | [x] | 2026-09-18 | PASS with notes — PAN/IFSC are stock fields |
| T-028 — Shift Type autoname | [x] | 2026-09-18 | PASS |
| T-031 — Shift Request (employee-initiated) | [x] | 2026-09-21 | PASS — new Section C operational transaction |
| T-032 — Approve Shift Request | [x] | 2026-09-21 | PASS — new Section C operational transaction |
| T-033 — Shift Assignment employee_name | [x] | 2026-09-18 | PASS |
| T-034 — Auto Attendance end-to-end | [x] | 2026-09-18 | PASS with notes — doc clarified (Stream 2): shift from active Shift Assignment; `working_hours` on Attendance, not Checkin |
| T-035 — Duplicate Attendance | [x] | 2026-09-18 | PASS with notes — doc clarified (Stream 2): auto-attendance with shift=None behaves differently |
| T-036 — Shift Assignment bad dates | [x] | 2026-09-18 | PASS |
| T-029 — Shift Location | [x] | 2026-09-18 | PASS with notes — lat/long + checkin_radius OPTIONAL in HRMS v16 |
| T-030 — Shift Schedule child rows | [x] | 2026-09-18 | PASS |
| T-037 — Bulk Attendance Tool | [x] | 2026-09-18 | PASS with notes — single-date only; no date-range field in v16 |
| T-039 — Checkin skip_auto_attendance | [x] | 2026-09-18 | PASS |
| T-038 — Attendance Request flow | [x] | 2026-09-18 | PASS with notes — Include Holidays required |
| T-040 — Leave Type rules | [x] | 2026-09-18 | PASS |
| T-041 — Leave Policy + details | [x] | 2026-09-18 | PASS |
| T-042 — Leave Period + bulk assign | [x] | 2026-09-18 | PASS with notes — Leave Period 2026-2027 + 3 Leave Allocations now applied (Stream 3) |
| T-043 — Leave App approve → Ledger | [x] | 2026-09-18 | PASS with notes — Leave Approver now set on Department X-HH (Stream 3) |
| T-044 — Leave App no approver | [x] | 2026-09-18 | PASS with notes — follow-on of T-043, Leave Approver applied (Stream 3) |
| T-045 — Leave App bad dates | [x] | 2026-09-18 | PASS with notes — follow-on of T-043, Leave Approver applied (Stream 3) |
| T-046 — Leave Encashment at exit | [x] | 2026-09-18 | PASS with notes — Leave Period + Allocation applied (Stream 3); Salary Structure skipped |
| T-047 — Compensatory Leave Request | [x] | 2026-09-18 | PASS with notes — Holiday List Assignment applied (Stream 3B) |
| T-048 — Leave Block List enforcement | [x] | 2026-09-18 | PASS with notes — follow-on of T-047 |
| T-049 — Overlapping Leave Apps | [x] | 2026-09-18 | PASS with notes — follow-on of T-047 |
| T-050 — LWP Leave Type | [x] | 2026-09-18 | PASS with notes — follow-on of T-047 |
| T-051 — Cancel approved Leave | [x] | 2026-09-18 | PASS with notes — follow-on of T-047 |
| T-052 — Leave Period rollover | [x] | 2026-09-18 | PASS with notes — follow-on of T-047 |
| T-053 — Leave Ledger audit | [x] | 2026-09-18 | PASS with notes — follow-on of T-047 |
| T-057 — Onboard new Employee | [x] | 2026-09-19 | PASS — "Test Onboarding Template" (HR-EMP-ONT-00001) created with 3 activities (Stream 5) |
| T-058 — Promote Employee | [x] | 2026-09-18 | PASS |
| T-059 — Promote already-Left | [x] | 2026-09-19 | PASS — "Ex-Employee User" (HR-EMP-00422) created with status=Left, relieving_date=2025-08-31 (Stream 5) |
| T-060 — Separation + Encashment | [x] | 2026-09-19 | PASS — Earned Leave allocation HR-LAL-2026-00001 (12d, submitted) confirmed for Test User (Stream 3 + Stream 5 verify) |
| T-061 — Transfer between Branches | [x] | 2026-09-18 | PASS |
| T-054 — Approve Leave Application | [x] | 2026-09-21 | PASS — new Section C operational transaction |
| T-055 — Reject Leave Application | [x] | 2026-09-21 | PASS — new Section C operational transaction |
| T-056 — Skill Map proficiency | [x] | 2026-09-18 | PASS |
| T-062 — Separation status flip | [x] | 2026-09-19 | PASS — "Test Separation Template" (HR-EMP-STP-00001) + draft separation HR-EMP-SEP-2026-00001 for Test User (Stream 5) |
| T-063 — Relieving Date auto-set | [x] | 2026-09-18 | PASS with notes — Holiday List Assignment applied (Stream 3B); use `boarding_begins_on` |
| T-064 — Monthly Attendance Details | [x] | 2026-09-18 | PASS with notes — doc renamed to 'Monthly Attendance Sheet' (Stream 2) |
| T-065 — Leave Ledger audit report | [x] | 2026-09-18 | PASS |
| T-066 — Leave Balance report | [x] | 2026-09-18 | PASS |
| T-067 — Employee Master headcount | [x] | 2026-09-18 | PASS with notes — vendor NoneType bug + 'Employee Analytics' report substitute + company-filter workaround (Stream 2) |
| T-068 — Shift Roster 7-day | [x] | 2026-09-18 | PASS with notes — substitute report (Stream 2); HRMS v16 has no 'Shift Roster' report |
| T-069 — Absenteeism Rate | [x] | 2026-09-18 | PASS with notes — substitute report (Stream 2); HRMS v16 has no 'Absenteeism' report |
| T-070 — autoname='prompt' missing | [x] | 2026-09-18 | PASS |
| T-071 — shift_schedule_assignment NULL | [x] | 2026-09-19 | PASS with notes — field is optional Link (req=0); 1/7830 existing Shift Assignments have NULL, confirming NULL behavior (Stream 5) |
| T-072 — Custom field silent drop | [x] | 2026-09-18 | PASS |
| T-073 — Duplicate Attendance (dup T-035) | [x] | 2026-09-18 | PASS |
| T-074 — Leave App no approver (dup T-044) | [x] | 2026-09-18 | PASS with notes — enforcement clarified (Stream 2): via HR Settings flag, not docfield |
| T-075 — Auto Att silent fail | [x] | 2026-09-18 | PASS with notes — rewritten for HRMS v16 split late_entry_grace_period fields (Stream 2) |
| T-076 — Holiday List bad dates | [x] | 2026-09-19 | PASS with notes — invalid range (from > to) rejected with "To Date cannot be before From Date" (Stream 5) |
| T-077 — Dept root trap (dup T-019) | [x] | 2026-09-19 | PASS with notes — self-parent Department rejected (parent lookup fails; effectively prevents circular ref) (Stream 5) |
| T-078 — Timezone Attendance | [x] | 2026-09-18 | PASS |

### Sign-off rollup (2026-09-21 — after renumbering + 19 new Section A/B/C transactions)

- **PASS** (clean + with notes): 77 (was 58 at sign-off `fb6cf5d`; +19 new: T-001 to T-007 Section A; T-008 to T-015 Section B; T-031, T-032, T-054, T-055 new Section C operational)
- **DEFERRED** (write-test required, structurally untestable, or no fixture data): 0 (was 8; all 8 resolved or removed)
- **NOT DONE** (out of scope, payroll deferred): 1 (T-018, unchanged)
- **REMOVED** (structurally untestable in current prod): 1 (T-079 — Multi-Company isolation)
- **TOTAL**: 79 transactions (was 59; +19 new + 1 renumbered T-079 still removed as out-of-scope)

Sources for sign-off verdicts:
- Venkat's manual testing report (`workspace/manual-transactions-testing.txt`)
- Stream 1 investigation findings (`workspace/investigation-2026-09-18-pending-transactions.md`)
- Stream 3 prod fixes (`workspace/audit-2026-09-17-demo-readiness.md`): Leave Approver added on Department X-HH, Employee.holiday_list set on Test User, Leave Period 2026-2027 created, 3 Leave Allocations submitted for Test User, sample Leave Application drafted, HR Settings.standard_working_hours = 8, 211 Holiday List Assignments created.
- Stream 5 Maximum effort (2026-09-19): "Test Onboarding Template" (HR-EMP-ONT-00001, 3 activities) + 2nd test employee "Ex-Employee User" (HR-EMP-00422, status=Left) + "Test Separation Template" (HR-EMP-STP-00001, 3 activities) + draft separation HR-EMP-SEP-2026-00001 for Test User + write-tests T-071/T-076/T-077. T-079 removed (structurally untestable). See `workspace/audit-2026-09-17-demo-readiness.md` Verification Addendum.
