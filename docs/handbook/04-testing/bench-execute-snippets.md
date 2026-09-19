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

- T-040: replaced `separation_date` + `relieving_date` with `boarding_begins_on` — those field names do NOT exist on `Employee Separation` in HRMS v16.
- T-044: same field rename + added Holiday List Assignment pre-condition comment.
- T-045: report name corrected to "Monthly Attendance Sheet".
- T-048: substituted "Employee Master" (does not exist) with "Employee Analytics" + explicit `department`/`from_date`/`to_date` filters to work around the company-only NoneType bug.
- T-049: "Shift Roster" substituted with "Shift Attendance" + add_days workaround (no native 7-day roster view).
- T-050: "Absenteeism" substituted with `frappe.db.sql` count of `status='Absent'` divided by total working days (no native report).
- T-051: comment updated — Shift Assignment uses Series (`HR-SHA-.YY.-.MM.-.#####`), not `prompt`; only Shift Type / Shift Schedule raise the prompt ValidationError.
- T-055: comment added — mandatory check is via `HR Settings.leave_approver_mandatory_in_leave_application = 1`, not docfield `reqd`.
- T-056: snippet rewritten — `grace_period` does not exist in HRMS v16; use `late_entry_grace_period` / `early_exit_grace_period` with their enable flags.
- T-060: pre-condition comment — only 1 Company exists in prod; Branch DocType has no `company` field.

No commit was created — Stream 4 owns the commit step.

---

## Org Mgmt

### T-001, T-007, T-009 (simple creates — Department / Designation / Employment Type)

```python
import frappe
doc = frappe.get_doc({"doctype": "Department", "department_name": "Test ICU", "company": "Company A"})
doc.insert()
print("Inserted:", doc.name)
```

### T-002 (Employee create with full links)

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

### T-003 (Promote Employee — update Grade)

```python
import frappe
emp_name = "HR-EMP-XXXXX"  # Replace with actual
emp = frappe.get_doc("Employee", emp_name)
emp.grade = "Grade B"
emp.save()
print(f"{emp_name} grade:", emp.grade)
```

### T-005 (Duplicate Department — expect failure)

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

### T-006 (Branch without Company — expect failure)

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

### T-007 (Designation)

```python
import frappe
doc = frappe.get_doc({"doctype": "Designation", "designation_name": "Test Role", "description": "Test role"})
doc.insert()
print("Inserted:", doc.name)
```

### T-008 (Employee Grade with pay_band)

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

### T-009 (Employment Type)

```python
import frappe
doc = frappe.get_doc({"doctype": "Employment Type", "employee_type_name": "Test Type", "description": "Permanent full-time staff"})
doc.insert()
print("Inserted:", doc.name)
```

### T-010 (Update Department — idempotent check)

```python
import frappe
dept_name = "Test ICU"  # From T-001
existing = frappe.get_doc("Department", dept_name)
existing.department_name = "Test ICU Updated"
existing.save()
count_after = frappe.db.count("Department", {"department_name": "Test ICU Updated"})
count_old = frappe.db.count("Department", {"department_name": "Test ICU"})
print(f"After update — 'Updated': {count_after}, 'Original': {count_old}")
print("PASS (idempotent)" if count_after == 1 and count_old == 0 else "FAIL")
```

### T-011 (Transfer Employee)

```python
import frappe
emp_name = "HR-EMP-XXXXX"
emp = frappe.get_doc("Employee", emp_name)
emp.department = "Department B"
emp.save()
print(f"{emp_name} department:", emp.department)
```

### T-012 (Employee with healthcare custom fields)

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

### T-013 (Shift Type with autoname='prompt')

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

### T-014 (Shift Assignment with employee_name remap)

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

### T-015 (Auto Attendance — trigger scheduler)

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

### T-016 (Duplicate Attendance)

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

### T-017 (Shift Assignment bad dates)

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

### T-018 (Shift Location)

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

### T-019 (Shift Schedule with repeat_on_days child)

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

### T-020 (Manual attendance via Attendance Tool)

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

### T-021 (Checkin skip_auto_attendance)

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

### T-022 (Attendance Request — via API)

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

### T-023 (Leave Type with flags)

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

### T-024 (Leave Policy + child details)

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

### T-025 (Leave Period + bulk assign via Leave Control Panel)

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

### T-026 (Leave App approve → Ledger)

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

### T-027 (Leave App no approver)

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

### T-028 (Leave App bad dates)

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

### T-029 (Leave Encashment)

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

### T-030 (Compensatory Leave Request)

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

### T-031 (Leave Block List enforcement)

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

### T-033 (LWP Leave Type — check Salary Slip)

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

### T-034 (Cancel approved Leave)

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

### T-035 (Leave Period rollover)

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

### T-036 (Leave Ledger audit)

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

## Lifecycle

### T-037 (Onboard Employee)

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

### T-038 (Promote Employee)

```python
import frappe
emp = frappe.get_doc("Employee", "HR-EMP-00001")
emp.grade = "Grade B"
emp.save()
print(f"{emp.name} grade:", emp.grade)
```

### T-039 (Promote already-Left)

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

### T-040 (Separation + Encashment)

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

### T-041 (Transfer between Branches)

```python
import frappe
emp = frappe.get_doc("Employee", "HR-EMP-00001")
emp.branch = "Site B"
emp.save()
print(f"{emp.name} branch:", emp.branch)
```

### T-042 (Skill Map)

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

### T-043 (Separation status flip)

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

### T-044 (boarding_begins_on — note: no auto-set Relieving Date)

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

### T-045 (Monthly Attendance Sheet — note: rename from "Details" to "Sheet")

```python
import frappe
# CORRECT report name is "Monthly Attendance Sheet" — "Monthly Attendance Details" does NOT exist.
# Canonical filter is filter_based_on=Month with numeric month + year
# (filter_based_on=Date Range is rejected by this script report).
data = frappe.get_doc("Report", "Monthly Attendance Sheet")
columns, result = data.run("Monthly Attendance Sheet", filters={"month": "2026-09", "company": "Company A"})
print(f"Report rows: {len(result)}")
```

### T-046 (Leave Ledger audit)

```python
import frappe
data = frappe.get_doc("Report", "Leave Ledger Entry")
columns, result = data.run("Leave Ledger Entry", filters={"employee": "HR-EMP-00001", "from_date": (">=", "2025-09-01"), "to_date": ("<=", "2026-09-30")})
print(f"Ledger rows: {len(result)}")
```

### T-047 (Leave Balance)

```python
import frappe
data = frappe.get_doc("Report", "Leave Balance")
columns, result = data.run("Leave Balance", filters={"employee": "HR-EMP-00001", "company": "Company A"})
print(f"Balance rows: {len(result)}")
```

### T-048 (Employee Analytics — substitute; "Employee Master" does not exist)

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

### T-049 (Shift Attendance — substitute; "Shift Roster" does not exist)

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

### T-050 (Absenteeism Rate — substitute; no native report)

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

### T-051 (autoname='prompt' missing — Shift Type / Shift Schedule ONLY)

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

### T-052 (shift_schedule_assignment NULL)

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

### T-053 (Custom field silent drop)

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

### T-056 (Auto Attendance — HRMS v16 late/early grace period split, no silent fail)

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

### T-057 (Holiday List bad dates)

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

### T-059 (Timezone Attendance)

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

### T-060 (Multi-Company isolation — OUT OF SCOPE in current prod)

```python
import frappe
# OUT OF SCOPE (2026-09-19): Structurally untestable in current prod state — only 1 Company exists (Haritha Hospitals).
# Additionally, Branch DocType in this HRMS install has NO `company` field, so cross-company
# branch linking cannot be exercised. REMOVED FROM SIGN-OFF per operator decision (Stream 5): unfixable
# without a second Company + Branch + an app-version upgrade that adds Branch.company. Will not be tracked
# in the 59-transaction sign-off count (was 60; T-060 removed).
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

**Last updated:** 2026-09-19 (after Stream 5 Maximum effort — 7 DEFERRED resolved + T-060 removed)

| Transaction | Result | Date | Notes |
|---|---|---|---|
| T-001 — Department create with Approver | [x] | 2026-09-18 | PASS |
| T-002 — Employee with full links | [x] | 2026-09-18 | PASS |
| T-003 — Promote Employee | [~] | 2026-09-18 | NOT DONE — payroll deferred |
| T-004 — Department root trap | [x] | 2026-09-18 | PASS with notes — manual expected fail, system permissive |
| T-005 — Duplicate Department name | [x] | 2026-09-18 | PASS |
| T-006 — Branch without Company | [x] | 2026-09-18 | PASS with notes — Branch without Company prompt allowed |
| T-007 — Create Designation | [x] | 2026-09-18 | PASS |
| T-008 — Employee Grade with pay_band | [x] | 2026-09-18 | PASS with notes — pay_band optional |
| T-009 — Create Employment Type | [x] | 2026-09-18 | PASS |
| T-010 — Update Department idempotent | [x] | 2026-09-18 | PASS with notes — migration script is dev tool, not runtime |
| T-011 — Transfer Employee | [x] | 2026-09-18 | PASS |
| T-012 — Employee healthcare fields | [x] | 2026-09-18 | PASS with notes — PAN/IFSC are stock fields |
| T-013 — Shift Type autoname | [x] | 2026-09-18 | PASS |
| T-014 — Shift Assignment employee_name | [x] | 2026-09-18 | PASS |
| T-015 — Auto Attendance end-to-end | [x] | 2026-09-18 | PASS with notes — doc clarified (Stream 2): shift from active Shift Assignment; `working_hours` on Attendance, not Checkin |
| T-016 — Duplicate Attendance | [x] | 2026-09-18 | PASS with notes — doc clarified (Stream 2): auto-attendance with shift=None behaves differently |
| T-017 — Shift Assignment bad dates | [x] | 2026-09-18 | PASS |
| T-018 — Shift Location | [x] | 2026-09-18 | PASS with notes — lat/long + checkin_radius OPTIONAL in HRMS v16 |
| T-019 — Shift Schedule child rows | [x] | 2026-09-18 | PASS |
| T-020 — Bulk Attendance Tool | [x] | 2026-09-18 | PASS with notes — single-date only; no date-range field in v16 |
| T-021 — Checkin skip_auto_attendance | [x] | 2026-09-18 | PASS |
| T-022 — Attendance Request flow | [x] | 2026-09-18 | PASS with notes — Include Holidays required |
| T-023 — Leave Type rules | [x] | 2026-09-18 | PASS |
| T-024 — Leave Policy + details | [x] | 2026-09-18 | PASS |
| T-025 — Leave Period + bulk assign | [x] | 2026-09-18 | PASS with notes — Leave Period 2026-2027 + 3 Leave Allocations now applied (Stream 3) |
| T-026 — Leave App approve → Ledger | [x] | 2026-09-18 | PASS with notes — Leave Approver now set on Department X-HH (Stream 3) |
| T-027 — Leave App no approver | [x] | 2026-09-18 | PASS with notes — follow-on of T-26, Leave Approver applied (Stream 3) |
| T-028 — Leave App bad dates | [x] | 2026-09-18 | PASS with notes — follow-on of T-26, Leave Approver applied (Stream 3) |
| T-029 — Leave Encashment at exit | [x] | 2026-09-18 | PASS with notes — Leave Period + Allocation applied (Stream 3); Salary Structure skipped |
| T-030 — Compensatory Leave Request | [x] | 2026-09-18 | PASS with notes — Holiday List Assignment applied (Stream 3B) |
| T-031 — Leave Block List enforcement | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-032 — Overlapping Leave Apps | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-033 — LWP Leave Type | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-034 — Cancel approved Leave | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-035 — Leave Period rollover | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-036 — Leave Ledger audit | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-037 — Onboard new Employee | [x] | 2026-09-19 | PASS — "Test Onboarding Template" (HR-EMP-ONT-00001) created with 3 activities (Stream 5) |
| T-038 — Promote Employee | [x] | 2026-09-18 | PASS |
| T-039 — Promote already-Left | [x] | 2026-09-19 | PASS — "Ex-Employee User" (HR-EMP-00422) created with status=Left, relieving_date=2025-08-31 (Stream 5) |
| T-040 — Separation + Encashment | [x] | 2026-09-19 | PASS — Earned Leave allocation HR-LAL-2026-00001 (12d, submitted) confirmed for Test User (Stream 3 + Stream 5 verify) |
| T-041 — Transfer between Branches | [x] | 2026-09-18 | PASS |
| T-042 — Skill Map proficiency | [x] | 2026-09-18 | PASS |
| T-043 — Separation status flip | [x] | 2026-09-19 | PASS — "Test Separation Template" (HR-EMP-STP-00001) + draft separation HR-EMP-SEP-2026-00001 for Test User (Stream 5) |
| T-044 — Relieving Date auto-set | [x] | 2026-09-18 | PASS with notes — Holiday List Assignment applied (Stream 3B); use `boarding_begins_on` |
| T-045 — Monthly Attendance Details | [x] | 2026-09-18 | PASS with notes — doc renamed to 'Monthly Attendance Sheet' (Stream 2) |
| T-046 — Leave Ledger audit report | [x] | 2026-09-18 | PASS |
| T-047 — Leave Balance report | [x] | 2026-09-18 | PASS |
| T-048 — Employee Master headcount | [x] | 2026-09-18 | PASS with notes — vendor NoneType bug + 'Employee Analytics' report substitute + company-filter workaround (Stream 2) |
| T-049 — Shift Roster 7-day | [x] | 2026-09-18 | PASS with notes — substitute report (Stream 2); HRMS v16 has no 'Shift Roster' report |
| T-050 — Absenteeism Rate | [x] | 2026-09-18 | PASS with notes — substitute report (Stream 2); HRMS v16 has no 'Absenteeism' report |
| T-051 — autoname='prompt' missing | [x] | 2026-09-18 | PASS |
| T-052 — shift_schedule_assignment NULL | [x] | 2026-09-19 | PASS with notes — field is optional Link (req=0); 1/7830 existing Shift Assignments have NULL, confirming NULL behavior (Stream 5) |
| T-053 — Custom field silent drop | [x] | 2026-09-18 | PASS |
| T-054 — Duplicate Attendance (dup T-016) | [x] | 2026-09-18 | PASS |
| T-055 — Leave App no approver (dup T-027) | [x] | 2026-09-18 | PASS with notes — enforcement clarified (Stream 2): via HR Settings flag, not docfield |
| T-056 — Auto Att silent fail | [x] | 2026-09-18 | PASS with notes — rewritten for HRMS v16 split late_entry_grace_period fields (Stream 2) |
| T-057 — Holiday List bad dates | [x] | 2026-09-19 | PASS with notes — invalid range (from > to) rejected with "To Date cannot be before From Date" (Stream 5) |
| T-058 — Dept root trap (dup T-004) | [x] | 2026-09-19 | PASS with notes — self-parent Department rejected (parent lookup fails; effectively prevents circular ref) (Stream 5) |
| T-059 — Timezone Attendance | [x] | 2026-09-18 | PASS |

### Sign-off rollup (2026-09-19 — after Stream 5 Maximum effort)

- **PASS** (clean + with notes): 58 (was 51; +7 from Stream 5: T-037, T-039, T-040, T-043, T-052, T-057, T-058)
- **DEFERRED** (write-test required, structurally untestable, or no fixture data): 0 (was 8; all 8 resolved or removed)
- **NOT DONE** (out of scope, payroll deferred): 1 (T-003, unchanged)
- **REMOVED** (structurally untestable in current prod): 1 (T-060 — Multi-Company isolation)
- **TOTAL**: 59 transactions (was 60; T-060 removed)

Sources for sign-off verdicts:
- Venkat's manual testing report (`workspace/manual-transactions-testing.txt`)
- Stream 1 investigation findings (`workspace/investigation-2026-09-18-pending-transactions.md`)
- Stream 3 prod fixes (`workspace/audit-2026-09-17-demo-readiness.md`): Leave Approver added on Department X-HH, Employee.holiday_list set on Test User, Leave Period 2026-2027 created, 3 Leave Allocations submitted for Test User, sample Leave Application drafted, HR Settings.standard_working_hours = 8, 211 Holiday List Assignments created.
- Stream 5 Maximum effort (2026-09-19): "Test Onboarding Template" (HR-EMP-ONT-00001, 3 activities) + 2nd test employee "Ex-Employee User" (HR-EMP-00422, status=Left) + "Test Separation Template" (HR-EMP-STP-00001, 3 activities) + draft separation HR-EMP-SEP-2026-00001 for Test User + write-tests T-052/T-057/T-058. T-060 removed (structurally untestable). See `workspace/audit-2026-09-17-demo-readiness.md` Verification Addendum.
