import csv as _csv

BATCH_SIZE = 500
ENTITY = "Attendance"
TABLE = "tabAttendance"

with open("/tmp/csvs_attendance.csv") as f:
    lines = f.readlines()
ds = next(i for i, l in enumerate(lines) if l.strip() == "## Data") + 1
rows = list(_csv.DictReader(lines[ds:]))
total = len(rows)
print("CSV rows: {}".format(total))

current = frappe.db.count(ENTITY)
print("DB rows: {}".format(current))
if current >= total:
    print("Already done")
else:
    emp_map = {}
    for e in frappe.get_all("Employee", fields=["name", "employee_number"]):
        if e.employee_number:
            emp_map["EMP-{}".format(str(e.employee_number).zfill(4))] = e.name
            emp_map["EMP-{}".format(str(e.employee_number))] = e.name
    st_map = {s.name: s.name for s in frappe.get_all("Shift Type", fields=["name"])}

    start = current
    for batch_end in range(start + BATCH_SIZE, total + BATCH_SIZE, BATCH_SIZE):
        batch_end = min(batch_end, total)
        batch = rows[start:batch_end]
        if not batch:
            break
        print("  batch {}-{}...".format(start, batch_end), end=" ", flush=True)
        values_list = []
        for idx, row in enumerate(batch):
            emp_csv = row.get("employee", "").strip()
            emp_pk = emp_map.get(emp_csv, "")
            if not emp_pk:
                continue
            att_date = row.get("attendance_date", "").strip()
            status = row.get("status", "Present").strip()
            shift_csv = row.get("shift", "").strip()
            shift_pk = st_map.get(shift_csv, shift_csv) if shift_csv else ""
            leave_type = row.get("leave_type", "").strip()
            leave_app = row.get("leave_application", "").strip()
            late_by = int(row.get("late_entry_by", 0) or 0)
            early_by = int(row.get("early_out_by", 0) or 0)
            is_wfh = int(row.get("is_wfh", 0) or 0)
            company = row.get("company", "").strip() or "Haritha Hospitals"
            # late_entry/early_exit are tinyint (0 or 1) in modern schema; mark as 1 if value > 0
            late_entry = 1 if late_by > 0 else 0
            early_exit = 1 if early_by > 0 else 0
            att_name = "HR-ATT-{}-{:05d}".format(att_date.replace("-", ""), start + idx + 1)
            values_list.append(
                "('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}', 'Administrator', 'Administrator', NOW(), NOW())".format(
                    att_name.replace("'", "''"),
                    emp_pk.replace("'", "''"),
                    att_date,
                    status.replace("'", "''"),
                    (shift_pk or "").replace("'", "''"),
                    leave_type.replace("'", "''"),
                    leave_app.replace("'", "''"),
                    late_entry,
                    early_exit,
                    company.replace("'", "''"),
                )
            )
        if not values_list:
            print("SKIP (no valid rows)")
            continue
        # Columns match actual schema: name, employee, attendance_date, status, shift, leave_type, leave_application, late_entry, early_exit, company, owner, modified_by, creation, modified
        sql = "INSERT INTO `{}` (name, employee, attendance_date, status, shift, leave_type, leave_application, late_entry, early_exit, company, owner, modified_by, creation, modified) VALUES {}".format(
            TABLE, ",".join(values_list)
        )
        try:
            frappe.db.sql(sql)
            frappe.db.commit()
        except Exception as e:
            frappe.db.rollback()
            print("ERROR: {}".format(str(e)[:200]))
            print("HALTING")
            break
        new_count = frappe.db.count(ENTITY)
        if new_count < batch_end:
            print("FAIL DB={} < expected={}".format(new_count, batch_end))
            break
        print("OK total={}".format(new_count))
        start = batch_end
    print("DONE. Final: {}".format(frappe.db.count(ENTITY)))