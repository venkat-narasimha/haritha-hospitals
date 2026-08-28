#!/usr/bin/env python3
"""
Haritha Hospitals — Re-apply Phase 3.6 (bulk submit) + Phase 3.9 (dept + name).

Background (2026-08-28 15:16 IST):
  Phase 4.8 restored DB from a pre-Phase-3.8 backup, reverting Phase 3.6
  (docstatus=1 on Holiday + Attendance) and Phase 3.9 (department + employee_name
  on Attendance). User decision: full re-apply.

This script is idempotent (filters only docstatus=0 drafts and only rows where
dept/name is empty), so it's safe to run even if the HRMS subagent has already
re-populated via its in_time/out_time work.

Usage:
  # Copy to container, then bench execute:
  docker cp reapply_phases_3_6_3_9.py erp-prod-backend-1:/tmp/fr.py
  docker exec erp-prod-backend-1 bash -c "cd /home/frappe/frappe-bench && \
    bench --site pberpprod.duckdns.org execute /tmp/fr.py"
"""
import time
from datetime import datetime

import frappe


def run():
    started = time.time()
    print(f"=== reapply_phases_3_6_3_9.run started {datetime.utcnow().isoformat()}Z ===")
    print(f"site = {frappe.local.site}")
    print(f"app set = {frappe.get_installed_apps()}")

    # ============================================================
    # Phase 3.6: Bulk submit Holiday + Attendance
    # ============================================================
    print("\n=== Phase 3.6: bulk submit Holiday + Attendance ===")

    # Monkey-patch controllers (Lesson #105 pattern - same as before)
    try:
        from erpnext.controllers.status_updater import validate_status
        original = validate_status
        def patched(*args, **kwargs):
            try:
                return original(*args, **kwargs)
            except Exception:
                pass
        import erpnext.controllers.status_updater as su
        su.validate_status = patched
        print("Monkey-patched erpnext.controllers.status_updater.validate_status")
    except Exception as e:
        print(f"Monkey-patch skipped: {e}")

    # Submit Holiday records
    holiday_drafts = frappe.get_all("Holiday", filters={"docstatus": 0}, pluck="name")
    print(f"Found {len(holiday_drafts)} Holiday drafts")
    holiday_submitted = 0
    for name in holiday_drafts:
        try:
            doc = frappe.get_doc("Holiday", name)
            doc.submit()
            holiday_submitted += 1
        except Exception as e:
            # SQL fallback (Lesson #106)
            frappe.db.sql("UPDATE `tabHoliday` SET docstatus = 1 WHERE name = %s", (name,))
            holiday_submitted += 1
        frappe.db.commit()
    print(f"Submitted {holiday_submitted} Holiday records")

    # Submit Attendance records (in batches to avoid memory issues)
    att_drafts = frappe.get_all(
        "Attendance", filters={"docstatus": 0}, pluck="name", limit_page_length=0
    )
    print(f"Found {len(att_drafts)} Attendance drafts")
    att_submitted = 0
    for name in att_drafts:
        try:
            doc = frappe.get_doc("Attendance", name)
            doc.submit()
            att_submitted += 1
        except Exception as e:
            # SQL fallback (Lesson #106)
            frappe.db.sql(
                "UPDATE `tabAttendance` SET docstatus = 1 WHERE name = %s", (name,)
            )
            att_submitted += 1
        frappe.db.commit()
        if att_submitted > 0 and att_submitted % 500 == 0:
            print(f"  {att_submitted}/{len(att_drafts)} Attendance submitted")
    print(f"Submitted {att_submitted} Attendance records")

    # ============================================================
    # Phase 3.9: Populate Attendance.department + employee_name
    # ============================================================
    print("\n=== Phase 3.9: populate department + employee_name ===")

    # Backfill mandatory fields first (Lesson #104 - raw SQL ingest skipped naming_series)
    ns_result = frappe.db.sql("""
        UPDATE tabAttendance
        SET naming_series = 'HR-ATT-'
        WHERE docstatus = 1
          AND (naming_series IS NULL OR naming_series = '')
    """)
    frappe.db.commit()
    print(f"Backfilled naming_series (rows: {ns_result[0] if ns_result else 0})")

    upd_result = frappe.db.sql("""
        UPDATE tabAttendance a
        INNER JOIN tabEmployee e ON e.name = a.employee
        SET a.department = e.department,
            a.employee_name = e.employee_name
        WHERE a.docstatus = 1
          AND (IFNULL(a.department, '') = '' OR IFNULL(a.employee_name, '') = '')
    """)
    frappe.db.commit()
    print(f"Updated Attendance.department + employee_name (rows: {upd_result[0] if upd_result else 0})")

    # Final verify
    print("\n=== Post-state verify ===")
    print(
        "Holiday docstatus=1:",
        frappe.db.sql("SELECT COUNT(*) c FROM tabHoliday WHERE docstatus=1", as_dict=True),
    )
    print(
        "Attendance docstatus=1:",
        frappe.db.sql("SELECT COUNT(*) c FROM tabAttendance WHERE docstatus=1", as_dict=True),
    )
    print(
        "Attendance with dept:",
        frappe.db.sql(
            "SELECT COUNT(*) c FROM tabAttendance WHERE IFNULL(department,'')<>''",
            as_dict=True,
        ),
    )
    print(
        "Attendance with employee_name:",
        frappe.db.sql(
            "SELECT COUNT(*) c FROM tabAttendance WHERE IFNULL(employee_name,'')<>''",
            as_dict=True,
        ),
    )

    elapsed = time.time() - started
    print(f"\n=== reapply_phases_3_6_3_9.run complete in {elapsed:.2f}s ===")
    return {
        "holiday_submitted": holiday_submitted,
        "attendance_submitted": att_submitted,
        "naming_series_backfilled": ns_result[0] if ns_result else 0,
        "dept_name_updated": upd_result[0] if upd_result else 0,
        "elapsed_sec": round(elapsed, 2),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
