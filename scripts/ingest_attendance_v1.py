import csv as _csv

BATCH_SIZE = 500
ENTITY = "Attendance"

# Read CSV
with open("/tmp/csvs_attendance.csv") as f:
    lines = f.readlines()
ds = next(i for i, l in enumerate(lines) if l.strip() == "## Data") + 1
rows = list(_csv.DictReader(lines[ds:]))
total = len(rows)
print("CSV rows: {}".format(total))

# Idempotency
current = frappe.db.count(ENTITY)
print("DB rows: {}".format(current))
if current >= total:
    print("Already done")
else:
    # Build FK maps
    emp_map = {}
    for e in frappe.get_all("Employee", fields=["name", "employee_number"]):
        if e.employee_number:
            emp_map["EMP-{}".format(str(e.employee_number).zfill(4))] = e.name
            emp_map["EMP-{}".format(str(e.employee_number))] = e.name
    st_map = {s.name: s.name for s in frappe.get_all("Shift Type", fields=["name"])}
    co = "Haritha Hospitals"
    start = current
    for batch_end in range(start + BATCH_SIZE, total + BATCH_SIZE, BATCH_SIZE):
        batch_end = min(batch_end, total)
        batch = rows[start:batch_end]
        if not batch:
            break
        print("  batch {}-{}...".format(start, batch_end), end=" ", flush=True)
        try:
            for row in batch:
                emp_csv = row.get("employee", "").strip()
                emp_pk = emp_map.get(emp_csv, "")
                if not emp_pk:
                    raise Exception("Employee not found: " + emp_csv)
                doc = frappe.new_doc(ENTITY)
                doc.employee = emp_pk
                doc.attendance_date = row.get("attendance_date", "").strip()
                doc.status = row.get("status", "Present").strip()
                doc.shift = st_map.get(row.get("shift", "").strip(), row.get("shift", "").strip()) or None
                doc.leave_type = row.get("leave_type", "").strip() or None
                doc.leave_application = row.get("leave_application", "").strip() or None
                doc.late_entry_by = int(row.get("late_entry_by", 0) or 0)
                doc.early_out_by = int(row.get("early_out_by", 0) or 0)
                doc.is_wfh = int(row.get("is_wfh", 0) or 0)
                doc.company = row.get("company", "").strip() or co
                doc.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.db.rollback()
            print("ERROR: {}".format(str(e)[:150]))
            print("HALTING")
            break
        new_count = frappe.db.count(ENTITY)
        if new_count < batch_end:
            print("FAIL DB={} < expected={}".format(new_count, batch_end))
            break
        print("OK total={}".format(new_count))
        start = batch_end
    print("DONE. Final: {}".format(frappe.db.count(ENTITY)))