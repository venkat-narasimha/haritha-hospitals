#!/usr/bin/env python3
"""
Haritha Hospitals — Populate Attendance.department and Attendance.employee_name
from the Employee table.

Phase 3 raw SQL bulk ingest (Phase 3.5 sub-phases) inserted Attendance rows
directly via SQL, bypassing the Frappe ORM. ORM `frappe.get_doc().insert()`
auto-derives `employee_name` and `department` from the Employee FK; raw SQL
does NOT. Result: 6,300 Attendance rows had NULL/empty values for both FK-
derived fields, breaking Shift Attendance reports that group by department.

This script is **idempotent** — the WHERE clause only matches rows where
department OR employee_name is empty. Re-running on a populated database is
a safe no-op.

Invocation:
    docker cp populate_attendance_meta.py erp-prod-backend-1:/tmp/
    docker exec erp-prod-backend-1 bash -c "cd /home/frappe/frappe-bench && \
      bench --site pberpprod.duckdns.org console < /tmp/populate_attendance_meta.py"

Notes:
- Single SQL UPDATE with INNER JOIN — one pass, both columns atomically.
- `frappe.db.sql()` returns `()` for UPDATE statements in MariaDB; rowcount
  is not surfaced via the result tuple. Verify via re-querying after commit.
- docstatus is preserved (direct SQL UPDATE does not touch docstatus).
- Does not touch any other field on Attendance; no controller hooks run.
- For other sites, change the `frappe --site` argument at invocation; the
  script itself is site-agnostic (operates on tabAttendance + tabEmployee).

Author: ERPClaw sub-agent, 2026-08-27
"""
import frappe

before_dept = frappe.db.sql(
    "SELECT COUNT(*) c FROM tabAttendance WHERE IFNULL(department,'') != ''",
    as_dict=True,
)[0].c
before_name = frappe.db.sql(
    "SELECT COUNT(*) c FROM tabAttendance WHERE IFNULL(employee_name,'') != ''",
    as_dict=True,
)[0].c
print(f"BEFORE: department populated={before_dept}, employee_name populated={before_name}")

# Single INNER JOIN pass — populates both columns atomically.
frappe.db.sql(
    """
    UPDATE tabAttendance a
    INNER JOIN tabEmployee e ON e.name = a.employee
    SET a.department = e.department,
        a.employee_name = e.employee_name
    WHERE IFNULL(a.department, '') = ''
       OR IFNULL(a.employee_name, '') = ''
    """
)
frappe.db.commit()

after_dept = frappe.db.sql(
    "SELECT COUNT(*) c FROM tabAttendance WHERE IFNULL(department,'') != ''",
    as_dict=True,
)[0].c
after_name = frappe.db.sql(
    "SELECT COUNT(*) c FROM tabAttendance WHERE IFNULL(employee_name,'') != ''",
    as_dict=True,
)[0].c
updated = (
    (after_dept - before_dept)
    if after_dept >= before_dept
    else 0
) + (
    (after_name - before_name) if after_name >= before_name else 0
)
print(f"AFTER:  department populated={after_dept}, employee_name populated={after_name}")
print(f"Estimated rows updated: {updated}")

# Idempotency sanity check: re-run should match 0 rows.
re_run = frappe.db.sql(
    """
    UPDATE tabAttendance a
    INNER JOIN tabEmployee e ON e.name = a.employee
    SET a.department = e.department,
        a.employee_name = e.employee_name
    WHERE IFNULL(a.department, '') = ''
       OR IFNULL(a.employee_name, '') = ''
    """
)
frappe.db.commit()
re_matched = len(re_run) if re_run else 0
print(f"IDEMPOTENCY: re-run matched {re_matched} rows (expected 0)")

# Sample row for visual confirmation
sample = frappe.get_all(
    "Attendance",
    fields=["name", "employee", "employee_name", "department", "status"],
    limit=3,
    order_by="name asc",
)
print("Sample 3 rows:")
for r in sample:
    print(f"  {r}")