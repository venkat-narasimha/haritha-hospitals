import csv as _csv

BATCH_SIZE = 500
ENTITY = "Employee Checkin"
TABLE = "tabEmployee Checkin"

with open("/tmp/csvs_employee_checkin.csv") as f:
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
        print("  batch {}-{} ({} rows)...".format(start, batch_end, len(batch)), end=" ", flush=True)
        values_list = []
        for idx, row in enumerate(batch):
            emp_csv = row.get("employee", "").strip()
            emp_pk = emp_map.get(emp_csv, "")
            if not emp_pk:
                continue
            ck_time = row.get("time", "").strip()
            log_type = row.get("log_type", "").strip()
            device_id = row.get("device_id", "").strip()
            is_off = int(row.get("is_off", 0) or 0)
            shift_csv = row.get("shift", "").strip()
            shift_pk = st_map.get(shift_csv, shift_csv) if shift_csv else ""
            ck_name = "HR-CHECKIN-{}-{:06d}".format(start + idx + 1, start + idx + 1)
            # Columns: name, employee, time, log_type, device_id, shift, offshift, owner, modified_by, creation, modified
            values_list.append(
                "('{}', '{}', '{}', '{}', '{}', '{}', {}, 'Administrator', 'Administrator', NOW(), NOW())".format(
                    ck_name.replace("'", "''"),
                    emp_pk.replace("'", "''"),
                    ck_time,
                    log_type.replace("'", "''"),
                    device_id.replace("'", "''"),
                    (shift_pk or "").replace("'", "''"),
                    is_off,
                )
            )
        if not values_list:
            print("SKIP (no valid rows)")
            continue
        sql = "INSERT INTO `{}` (name, employee, time, log_type, device_id, shift, offshift, owner, modified_by, creation, modified) VALUES {}".format(
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