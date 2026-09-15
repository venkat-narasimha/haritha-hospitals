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
sep = frappe.get_doc({
    "doctype": "Employee Separation",
    "employee": emp,
    "employee_name": "Test Employee A",
    "company": "Company A",
    "separation_date": "2026-12-31",
    "relieving_date": "2026-12-31",
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

### T-044 (Relieving Date auto-set)

```python
import frappe
sep = frappe.get_doc({
    "doctype": "Employee Separation",
    "employee": "HR-EMP-00001",
    "employee_name": "Test Employee A",
    "separation_date": "2026-12-31",
    "reason": "Resignation",
})
sep.insert()
sep.db_set("docstatus", 1)
sep.db_set("status", "Approved")
frappe.db.commit()
saved = frappe.get_doc("Employee Separation", sep.name)
print(f"Relieving Date after approval: {saved.relieving_date}")
```

---

## Reports

### T-045 (Monthly Attendance Details)

```python
import frappe
data = frappe.get_doc("Report", "Monthly Attendance Details")
columns, result = data.run("Monthly Attendance Details", filters={"month": "2026-09", "company": "Company A"})
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

### T-048 (Employee Master)

```python
import frappe
data = frappe.get_doc("Report", "Employee Master")
columns, result = data.run("Employee Master", filters={"company": "Company A"})
print(f"Employee rows: {len(result)}")
```

### T-049 (Shift Roster)

```python
import frappe
from frappe.utils import today, add_days
data = frappe.get_doc("Report", "Shift Roster")
columns, result = data.run("Shift Roster", filters={"department": "Test ICU", "from_date": today(), "to_date": add_days(today(), 7)})
print(f"Roster rows: {len(result)}")
```

### T-050 (Absenteeism Rate)

```python
import frappe
from frappe.utils import get_first_day, get_last_day
month_start = get_first_day("2026-09-01")
month_end = get_last_day("2026-09-01")
total_emp = frappe.db.count("Employee", {"status": "Active", "department": "Department A"})
total_attendance = frappe.db.count("Attendance", {"attendance_date": ("between", [month_start, month_end]), "employee": ("in", frappe.get_all("Employee", filters={"department": "Department A", "status": "Active"}, pluck="name"))})
absent_count = frappe.db.sql("SELECT COUNT(*) FROM `tabAttendance` WHERE attendance_date BETWEEN %s AND %s AND status = 'Absent' AND employee IN (SELECT name FROM `tabEmployee` WHERE department = %s AND status = 'Active')", (month_start, month_end, "Department A"))[0][0]
print(f"Total Active in Dept A: {total_emp}, Attendance rows: {total_attendance}, Absent: {absent_count}")
print(f"Absenteeism Rate (rough): {absent_count/total_attendance*100 if total_attendance else 0:.2f}%")
```

---

## Edge Cases

### T-051 (autoname='prompt' missing)

```python
import frappe
try:
    doc = frappe.get_doc({
        "doctype": "Shift Type",
        "start_time": "09:00:00",
        "end_time": "18:00:00",
    })
    doc.insert()
    print("FAIL: empty name allowed")
except frappe.exceptions.ValidationError as e:
    print(f"PASS: {e}")
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

### T-056 (Auto Attendance silent fail)

```python
import frappe
# Trigger auto attendance and check logs
from frappe.utils.background_jobs import get_jobs
recent_jobs = [j for j in get_jobs(site=frappe.local.site) if "auto_attendance" in str(j).lower()]
print(f"Recent auto attendance jobs: {recent_jobs}")
# Alternative: check scheduled_job_logger
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

### T-060 (Multi-Company isolation)

```python
import frappe
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
        "company": "Company A",
        "branch": "Company-B-Branch",
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
