import csv as _csv

# 1. Dedup Department + Designation + Leave Type via SQL
for entity, field in [("Department", "department_name"), ("Designation", "designation_name"), ("Leave Type", "leave_type_name")]:
    rows = frappe.db.sql(
        "SELECT name, `{0}` AS field_val FROM `tab{1}` ORDER BY creation ASC".format(field, entity),
        as_dict=True,
    )
    seen = set()
    to_delete = []
    for r in rows:
        if r["field_val"] in seen:
            to_delete.append(r["name"])
        else:
            seen.add(r["field_val"])
    for n in to_delete:
        try:
            frappe.delete_doc(entity, n, ignore_permissions=True)
        except Exception as e:
            print("  delete fail {}: {}".format(n, str(e)[:60]))
    frappe.db.commit()
    print("{}: deleted {}, final={}".format(entity, len(to_delete), frappe.db.count(entity)))

# 2. Build FK maps
dept_map = {d["department_name"]: d["name"] for d in frappe.db.sql(
    "SELECT name, department_name FROM `tabDepartment`", as_dict=True
)}
desig_map = {d["designation_name"]: d["name"] for d in frappe.db.sql(
    "SELECT name, designation_name FROM `tabDesignation`", as_dict=True
)}
et_map = {e["employee_type_name"]: e["name"] for e in frappe.db.sql(
    "SELECT name, employee_type_name FROM `tabEmployment Type`", as_dict=True
)}
hl_map = {h["holiday_list_name"]: h["name"] for h in frappe.db.sql(
    "SELECT name, holiday_list_name FROM `tabHoliday List`", as_dict=True
)}
print("Maps: dept={} desig={} et={} hl={}".format(len(dept_map), len(desig_map), len(et_map), len(hl_map)))

# 3. Ingest Employee (skip branch — Branch "Hyderabad" doesn't exist)
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
            doc = frappe.new_doc("Employee")
            doc.employee = emp_id
            doc.employee_name = row.get("employee_name", "").strip()
            doc.company = row.get("company", "").strip() or "Haritha Hospitals"
            doc.status = row.get("status", "Active").strip()
            doc.employee_number = row.get("employee_number", "").strip()
            doc.department = dept_map.get(row.get("department", "").strip(), "")
            doc.designation = desig_map.get(row.get("designation", "").strip(), "")
            doc.employment_type = et_map.get(row.get("employment_type", "").strip(), "")
            doc.default_shift = row.get("default_shift", "").strip() or None
            doc.date_of_joining = row.get("date_of_joining", "").strip() or None
            doc.gender = row.get("gender", "").strip() or None
            doc.date_of_birth = row.get("date_of_birth", "").strip() or None
            doc.holiday_list = hl_map.get(row.get("holiday_list", "").strip(), "")
            doc.insert(ignore_permissions=True)
            inserted += 1
        except Exception as e:
            errors.append((emp_id, str(e)[:80]))
    frappe.db.commit()
    print("Inserted: {}, errors: {}".format(inserted, len(errors)))
    for eid, msg in errors[:3]:
        print("  {}: {}".format(eid, msg))

print("Final: Employee={}".format(frappe.db.count("Employee")))