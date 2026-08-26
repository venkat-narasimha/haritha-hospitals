def main():
    import csv as _csv

    CSV_DIR = "/tmp"

    def _rd(fname):
        with open(f"{CSV_DIR}/csvs_{fname}") as f:
            lines = f.readlines()
        ds = next(i for i, l in enumerate(lines) if l.strip() == "## Data") + 1
        return list(_csv.DictReader(lines[ds:]))

    def int_or_zero(v):
        if not v:
            return 0
        try:
            return int(v)
        except (ValueError, TypeError):
            return 0

    # Dedup: keep oldest row per (entity, name)
    def dedup(entity, name_field):
        rows = frappe.get_all(entity, fields=["name"], order_by="creation asc")
        seen = set()
        to_delete = []
        for r in rows:
            actual_name = frappe.db.get_value(entity, r["name"], name_field) or r["name"]
            if actual_name in seen:
                to_delete.append(r["name"])
            else:
                seen.add(actual_name)
        if to_delete:
            for n in to_delete:
                try:
                    frappe.delete_doc(entity, n, ignore_permissions=True)
                except Exception as e:
                    print(f"  skip delete {n}: {e}")
            frappe.db.commit()
        return len(to_delete)

    # --- 3a cleanup: dedup masters ---
    print("=== 3a dedup ===")
    for entity, field in [
        ("Department", "department_name"),
        ("Designation", "designation_name"),
        ("Leave Type", "leave_type_name"),
    ]:
        deleted = dedup(entity, field)
        print(f"  {entity:20s} deleted {deleted} dupes; final={frappe.db.count(entity)}")

    # --- 3b-1: Shift Type ---
    print("\n=== 3b-1 Shift Type ===")
    st_rows = _rd("shift_type.csv")
    st_current = frappe.db.count("Shift Type")
    if st_current < len(st_rows):
        inserted = 0
        for row in st_rows:
            if frappe.db.exists("Shift Type", row["name"]):
                continue
            try:
                doc = frappe.new_doc("Shift Type")
                doc.name = row["name"].strip()
                doc.start_time = row.get("start_time", "").strip()
                doc.end_time = row.get("end_time", "").strip()
                doc.duration = row.get("duration", "") or 0
                if doc.duration:
                    try:
                        doc.duration = float(doc.duration)
                    except (ValueError, TypeError):
                        doc.duration = 0
                doc.is_past_end_time = int_or_zero(row.get("is_past_end_time", "0"))
                doc.is_oncall = int_or_zero(row.get("is_oncall", "0"))
                doc.is_emergency = int_or_zero(row.get("is_emergency", "0"))
                doc.mark_auto_attendance = int_or_zero(row.get("mark_auto_attendance", "0"))
                doc.last_sync_of_checkin = row.get("last_sync_of_checkin", "").strip()
                doc.company = row.get("company", "").strip()
                doc.holiday_list = row.get("holiday_list", "").strip()
                doc.enable_auto_attendance = int_or_zero(row.get("enable_auto_attendance", "0"))
                csv_val = row.get("determine_check_in_and_check_out", "").strip()
                if csv_val == "Alternating entries as IN and OUT":
                    csv_val = "Alternating entries as IN and OUT during the same shift"
                doc.determine_check_in_and_check_out = csv_val
                doc.working_hours_calculation_based_on = row.get("working_hours_calculation_based_on", "").strip()
                doc.begin_check_in_before_shift_start_time = int_or_zero(row.get("begin_check_in_before_shift_start_time", "60"))
                doc.allow_check_out_after_shift_end_time = int_or_zero(row.get("allow_check_out_after_shift_end_time", "60"))
                doc.mark_auto_attendance_on_holidays = int_or_zero(row.get("mark_auto_attendance_on_holidays", "0"))
                doc.working_hours_threshold_for_half_day = row.get("working_hours_threshold_for_half_day", "") or 0
                doc.working_hours_threshold_for_absent = row.get("working_hours_threshold_for_absent", "") or 0
                doc.process_attendance_after = row.get("process_attendance_after", "").strip()
                doc.auto_update_last_sync_of_checkin = int_or_zero(row.get("auto_update_last_sync_of_checkin", "0"))
                doc.enable_late_entry_marking = int_or_zero(row.get("enable_late_entry_marking", "0"))
                doc.late_entry_grace_period = int_or_zero(row.get("late_entry_grace_period", "15"))
                doc.enable_early_exit_marking = int_or_zero(row.get("enable_early_exit_marking", "0"))
                doc.early_exit_grace_period = int_or_zero(row.get("early_exit_grace_period", "15"))
                doc.insert(ignore_permissions=True)
                inserted += 1
            except Exception as e:
                print(f"  ERR row {row.get('name')}: {str(e)[:80]}")
        frappe.db.commit()
        print(f"  Shift Type inserted={inserted}, final={frappe.db.count('Shift Type')}")
    else:
        print(f"  Shift Type skip (already {st_current} >= {len(st_rows)})")

    # --- 3c-1: Employee ---
    print("\n=== 3c-1 Employee ===")
    emp_rows = _rd("employee.csv")
    emp_current = frappe.db.count("Employee")
    print(f"  CSV={len(emp_rows)}, current={emp_current}")
    if emp_current < len(emp_rows):
        inserted = 0
        errors = 0
        for row in emp_rows:
            if frappe.db.exists("Employee", row["employee"]):
                continue
            try:
                doc = frappe.new_doc("Employee")
                doc.employee = row.get("employee", "").strip()
                doc.employee_name = row.get("employee_name", "").strip()
                doc.company = row.get("company", "").strip()
                doc.status = row.get("status", "Active").strip()
                doc.employee_number = row.get("employee_number", "").strip()
                doc.department = row.get("department", "").strip()
                doc.designation = row.get("designation", "").strip()
                doc.employment_type = row.get("employment_type", "").strip()
                doc.default_shift = row.get("default_shift", "").strip()
                doc.date_of_joining = row.get("date_of_joining", "").strip()
                doc.branch = row.get("branch", "").strip()
                doc.gender = row.get("gender", "").strip()
                doc.date_of_birth = row.get("date_of_birth", "").strip()
                doc.user_id = row.get("user_id", "").strip()
                doc.holiday_list = row.get("holiday_list", "").strip()
                doc.attendance_device_id = row.get("attendance_device_id", "").strip()
                if row.get("is_synthetic_data"):
                    doc.is_synthetic_data = int_or_zero(row["is_synthetic_data"])
                doc.insert(ignore_permissions=True)
                inserted += 1
            except Exception as e:
                errors += 1
                if errors < 3:
                    print(f"  ERR row {row.get('employee')}: {str(e)[:80]}")
        frappe.db.commit()
        print(f"  Employee inserted={inserted}, errors={errors}, final={frappe.db.count('Employee')}")
    else:
        print(f"  Employee skip (already {emp_current} >= {len(emp_rows)})")

    print("\n=== FINAL COUNTS ===")
    for dt in ["Holiday List", "Holiday", "Department", "Designation", "Employment Type", "Leave Type", "Shift Location", "Shift Type", "Employee"]:
        print(f"  {dt:20s} {frappe.db.count(dt)}")


main()