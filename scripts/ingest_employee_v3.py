import csv as _csv

# 1. Dedup (skip for now — duplicates don't block FK inserts)
# Just show counts
for entity in ["Department", "Designation", "Leave Type"]:
    print("{}: {}".format(entity, frappe.db.count(entity)))

# 2. Build FK maps
dept_map = {d["department_name"]: d["name"] for d in frappe.db.sql(
    "SELECT name, department_name FROM `tabDepartment` WHERE department_name IS NOT NULL AND department_name != ''", as_dict=True
)}
desig_map = {d["designation_name"]: d["name"] for d in frappe.db.sql(
    "SELECT name, designation_name FROM `tabDesignation` WHERE designation_name IS NOT NULL AND designation_name != ''", as_dict=True
)}
et_map = {e["employee_type_name"]: e["name"] for e in frappe.db.sql(
    "SELECT name, employee_type_name FROM `tabEmployment Type` WHERE employee_type_name IS NOT NULL AND employee_type_name != ''", as_dict=True
)}
hl_map = {h["holiday_list_name"]: h["name"] for h in frappe.db.sql(
    "SELECT name, holiday_list_name FROM `tabHoliday List` WHERE holiday_list_name IS NOT NULL AND holiday_list_name != ''", as_dict=True
)}
print("Maps: dept={} desig={} et={} hl={}".format(len(dept_map), len(desig_map), len(et_map), len(hl_map)))

# 3. Ingest Employee with required field defaults
with open("/tmp/csvs_employee.csv") as f:
    lines = f.readlines()
ds = next(i for i, l in enumerate(lines) if l.strip() == "## Data") + 1
rows = list(_csv.DictReader(lines[ds:]))

current = frappe.db.count("Employee")
print("Employee: current={}, csv={}".format(current, len(rows)))
if current >= len(rows):
    print("Already done")
else:
    inserted = 0
    errors = []
    for row in rows:
        emp_id = row.get("attendance_device_id", "").strip()
        if not emp_id or frappe.db.exists("Employee", emp_id):
            continue
        try:
            emp_name = row.get("employee_name", "").strip()
            # Split employee_name into first/last (first part = first_name, rest = last_name)
            parts = emp_name.split(" ", 1)
            first_name = parts[0] if parts else emp_name
            last_name = parts[1] if len(parts) > 1 else ""

            # Defaults for synthetic data
            gender = row.get("gender", "").strip() or "Not Specified"
            dob = row.get("date_of_birth", "").strip() or "1990-01-01"

            doc = frappe.new_doc("Employee")
            doc.employee = emp_id
            doc.first_name = first_name
            doc.last_name = last_name
            doc.employee_name = emp_name
            doc.company = row.get("company", "").strip() or "Haritha Hospitals"
            doc.status = row.get("status", "Active").strip()
            doc.employee_number = row.get("employee_number", "").strip()
            doc.department = dept_map.get(row.get("department", "").strip(), "")
            doc.designation = desig_map.get(row.get("designation", "").strip(), "")
            doc.employment_type = et_map.get(row.get("employment_type", "").strip(), "")
            doc.default_shift = row.get("default_shift", "").strip() or None
            doc.date_of_joining = row.get("date_of_joining", "").strip() or None
            doc.gender = gender
            doc.date_of_birth = dob
            doc.holiday_list = hl_map.get(row.get("holiday_list", "").strip(), "")
            doc.insert(ignore_permissions=True)
            inserted += 1
        except Exception as e:
            errors.append((emp_id, str(e)[:100]))
    frappe.db.commit()
    print("Inserted: {}, errors: {}".format(inserted, len(errors)))
    for eid, msg in errors[:5]:
        print("  {}: {}".format(eid, msg))

print("Final: Employee={}".format(frappe.db.count("Employee")))