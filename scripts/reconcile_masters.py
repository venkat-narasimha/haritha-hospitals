"""Reconcile Haritha Hospitals master entities to CSV targets.

Run: bench console -> exec(open("/tmp/reconcile_masters.py").read())
Targets: Department 37, Designation 48, Leave Type 7, Employment Type 6, Holiday 14.
"""
import csv
import io
import os

import frappe

MASTERS = "/tmp"  # container path; files are /tmp/csvs_<entity>.csv


def _fname(entity_file):
    return "csvs_{}".format(entity_file)


def csv_rows(entity_file):
    """Return list of dict rows from a masters CSV (skips # comment schema block)."""
    path = os.path.join(MASTERS, _fname(entity_file))
    with open(path) as f:
        lines = f.read().splitlines()
    # data section starts after the '## Data' marker (schema block precedes it)
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "## Data")
    reader = csv.reader(io.StringIO("\n".join(lines[start + 1:])))
    rows = [r for r in reader]
    header = [c.strip() for c in rows[0]]
    return [dict(zip(header, r + [""] * (len(header) - len(r)))) for r in rows[1:] if any(c.strip() for c in r)]


def sql_list(vals):
    return ",".join("'{}'".format(v.replace("'", "\\'")) for v in vals)


report = {}

# ---- 1. Department: delete non-CSV, keep root; NOTE Dept PKs carry '- <abbr>' suffix,
# so match on department_name column (canonical), not PK.
dept_rows = csv_rows("department.csv")
valid_dept = [r["name"].strip() for r in dept_rows]
frappe.db.sql(
    "DELETE FROM `tabDepartment` WHERE name != 'All Departments' AND department_name NOT IN ({})".format(sql_list(valid_dept))
)
# pass 1: ensure all CSV departments exist (company triggers abbr-suffixed PK)
dept_pk = {}
for r in dept_rows:
    nm = r["name"].strip()
    pk = frappe.db.get_value("Department", {"department_name": nm}, "name")
    if pk:
        dept_pk[nm] = pk
        continue
    doc = frappe.new_doc("Department")
    doc.department_name = nm
    doc.company = (r.get("company") or "").strip() or "Haritha Hospitals"
    doc.is_group = int(r.get("is_group") or 0)
    doc.insert(ignore_permissions=True)
    dept_pk[nm] = doc.name
# pass 2: wire parents (all rows exist now, so child-before-parent order is safe)
for r in dept_rows:
    nm = r["name"].strip()
    pd = (r.get("parent_department") or "").strip()
    target = "All Departments" if (not pd or pd == "All Departments") else dept_pk.get(pd, "All Departments")
    pk = dept_pk[nm]
    if frappe.db.get_value("Department", pk, "parent_department") != target:
        d = frappe.get_doc("Department", pk)
        d.parent_department = target
        d.save(ignore_permissions=True)
report["Department"] = frappe.db.count("Department")

# ---- 2. Designation ----
valid_desig = [r["name"].strip() for r in csv_rows("designation.csv")]
frappe.db.sql(
    "DELETE FROM `tabDesignation` WHERE name NOT IN ({})".format(sql_list(valid_desig))
)
report["Designation"] = frappe.db.count("Designation")

# ---- 3. Leave Type ----
valid_leave = [r["name"].strip() for r in csv_rows("leave_type.csv")]
frappe.db.sql(
    "DELETE FROM `tabLeave Type` WHERE name NOT IN ({})".format(sql_list(valid_leave))
)
report["Leave Type"] = frappe.db.count("Leave Type")

# ---- 4. Employment Type: delete non-CSV, insert missing ----
etype_rows = csv_rows("employment_type.csv")
valid_etype = [r["name"].strip() for r in etype_rows]
frappe.db.sql(
    "DELETE FROM `tabEmployment Type` WHERE name NOT IN ({})".format(sql_list(valid_etype))
)
inserted_et = []
for r in etype_rows:
    nm = r["name"].strip()
    if not frappe.db.exists("Employment Type", nm):
        doc = frappe.new_doc("Employment Type")
        doc.employee_type_name = nm
        if r.get("description"):
            doc.description = r["description"]
        if r.get("allow_employee_creation") not in ("", None):
            doc.allow_employee_creation = int(r["allow_employee_creation"] or 0)
        doc.insert(ignore_permissions=True)
        inserted_et.append(nm)
report["Employment Type"] = frappe.db.count("Employment Type")

# ---- 5. Holiday: wipe children of target list, re-ingest 14 from CSV ----
HL_NAME = "Haritha Hospitals Holiday List"
if not frappe.db.exists("Holiday List", HL_NAME):
    raise RuntimeError("Holiday List {!r} missing - aborting holiday ingest".format(HL_NAME))
hol_rows = csv_rows("holiday.csv")
hol_for_hl = [
    r for r in hol_rows
    if (r.get("parent") or "").strip() == HL_NAME or len(hol_rows) == 14
]
hl = frappe.get_doc("Holiday List", HL_NAME)
hl.holidays = []
for r in sorted(hol_for_hl, key=lambda x: x.get("holiday_date", "")):
    hl.append("holidays", {
        "holiday_date": r["holiday_date"].strip(),
        "description": (r.get("description") or "").strip(),
        "weekly_off": int(r.get("weekly_off") or 0),
        "optional_holiday": int(r.get("optional_holiday") or 0),
    })
hl.save(ignore_permissions=True)
report["Holiday"] = frappe.db.count("Holiday", {"parent": HL_NAME})

# NOTE: Holiday count must be counted per parent; global tabHoliday count equals it here (single list).
report["Holiday(global)"] = frappe.db.count("Holiday")
report["Inserted Employment Types"] = inserted_et
print("RECONCILE_REPORT:", report)

TARGETS = {"Department": 37, "Designation": 48, "Leave Type": 7, "Employment Type": 6, "Holiday(global)": 14}
final = {dt: frappe.db.count(dt) for dt in ["Department", "Designation", "Leave Type", "Employment Type", "Holiday"]}
print("FINAL_COUNTS:", final)
mismatches = []
for k, t in TARGETS.items():
    key = k.replace("(global)", "") if k == "Holiday(global)" else k
    got = report[k] if "(global)" in k else report.get(key)
    status = "OK" if got == t else "MISMATCH"
    if status == "MISMATCH":
        mismatches.append((key, got, t))
    print("{}: got={} target={} {}".format(key, got, t, status))
print("RESULT:", "ALL_MATCH" if not mismatches else "MISMATCHES={}".format(mismatches))
frappe.db.commit()
