import csv as _csv

BATCH_SIZE = 500
ENTITY = "Shift Assignment"

# Read CSV
with open("/tmp/csvs_shift_assignment.csv") as f:
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
    # Build FK lookup maps:
    # CSV format "EMP-NNNN" -> lookup by employee_number NNNN -> DB PK (HR-EMP-NNNNN)
    emp_map = {}
    for e in frappe.get_all("Employee", fields=["name", "employee_number"]):
        if e.employee_number:
            emp_map["EMP-{}".format(str(e.employee_number).zfill(4))] = e.name
            # Also handle without leading zeros (e.g., "EMP-1" vs "EMP-0001")
            emp_map["EMP-{}".format(str(e.employee_number))] = e.name

    # Direct PK map (Shift Type PK = name like "G0900R0830")
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
                doc.shift_type = st_map.get(row.get("shift_type", "").strip(), row.get("shift_type", "").strip())
                doc.start_date = row.get("start_date", "").strip()
                doc.end_date = row.get("end_date", "").strip() or None
                doc.status = row.get("status", "Active").strip()
                doc.docstatus = int(row.get("docstatus", 0) or 0)
                doc.company = row.get("company", "").strip() or co
                doc.shift_location = row.get("shift_location", "").strip() or None
                doc.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.db.rollback()
            print("ERROR: {}".format(str(e)[:120]))
            print("HALTING")
            break
        new_count = frappe.db.count(ENTITY)
        if new_count < batch_end:
            print("FAIL DB={} < expected={}".format(new_count, batch_end))
            break
        print("OK total={}".format(new_count))
        start = batch_end
    print("DONE. Final: {}".format(frappe.db.count(ENTITY)))