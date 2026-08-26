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

    def insert_holiday_list_with_children():
        rows = _rd("holiday.csv")
        if not rows:
            return 0, 0, "no rows"
        hl_name = rows[0].get("parent", "Haritha Hospitals Holiday List").strip()
        if frappe.db.exists("Holiday List", hl_name):
            hl = frappe.get_doc("Holiday List", hl_name)
        else:
            hl = frappe.new_doc("Holiday List")
            hl.holiday_list_name = hl_name
            hl.from_date = "2025-01-01"
            hl.to_date = "2026-12-31"
            hl.weekly_off = "Sunday"
            hl.company = "Haritha Hospitals"
        existing_dates = {h.holiday_date for h in hl.holidays}
        added = 0
        for row in rows:
            date = row.get("holiday_date", "").strip()
            if not date or date in existing_dates:
                continue
            hl.append("holidays", {
                "holiday_date": date,
                "description": row.get("description", "").strip(),
                "weekly_off": int_or_zero(row.get("weekly_off", "0")),
                "optional_holiday": int_or_zero(row.get("optional_holiday", "0")),
            })
            existing_dates.add(date)
            added += 1
        hl.save(ignore_permissions=True)
        frappe.db.commit()
        return frappe.db.count("Holiday List"), frappe.db.count("Holiday"), f"added={added}"

    def simple_insert(entity, filename, docfield_map):
        """docfield_map: {docfield: csv_col}. None csv_col = skip."""
        rows = _rd(filename)
        current = frappe.db.count(entity)
        if current >= len(rows):
            return len(rows), current, "skip"
        inserted = 0
        errors = []
        for row in rows:
            try:
                doc = frappe.new_doc(entity)
                for df, col in docfield_map.items():
                    if col is None:
                        continue
                    v = row.get(col, "")
                    if isinstance(v, str):
                        v = v.strip()
                    if not v:
                        continue
                    if df in ("is_lwp", "weekly_off", "is_carry_forward", "optional_holiday", "is_group", "disabled"):
                        v = int_or_zero(v)
                    setattr(doc, df, v)
                doc.insert(ignore_permissions=True)
                inserted += 1
            except Exception as e:
                errors.append(str(e)[:80])
        try:
            frappe.db.commit()
        except Exception:
            frappe.db.rollback()
        final = frappe.db.count(entity)
        status = "ok" if final >= len(rows) else f"fail({final}/{len(rows)})"
        return len(rows), final, f"{status} errs={len(errors)}"

    hl_count, h_count, hl_status = insert_holiday_list_with_children()

    # Corrected fieldmaps based on DocType introspection:
    # Department: department_name (CSV col "name"), company required
    # Designation: designation_name (CSV col "name") - ONLY
    # Leave Type: leave_type_name (CSV col "name") - ONLY
    simple_results = []
    simple_results.append(("Department", simple_insert(
        "Department", "department.csv",
        {"department_name": "name", "company": None}  # company set explicitly below
    )))
    simple_results.append(("Designation", simple_insert(
        "Designation", "designation.csv",
        {"designation_name": "name"}  # designation_name is autoname
    )))
    simple_results.append(("Leave Type", simple_insert(
        "Leave Type", "leave_type.csv",
        {"leave_type_name": "name"}
    )))
    simple_results.append(("Employment Type", simple_insert(
        "Employment Type", "employment_type.csv",
        {"employee_type_name": "employee_type_name"}
    )))
    simple_results.append(("Shift Location", simple_insert(
        "Shift Location", "shift_location.csv",
        {"location_name": "location_name", "address": "address", "company": "company"}
    )))

    # Post-process: set Company on Department / Shift Location if missing
    print("\n=== 3a MASTERS SUMMARY ===")
    print(f"  Holiday List         db={hl_count}  Holiday db={h_count}  {hl_status}")
    for entity, (exp, cur, status) in simple_results:
        print(f"  {entity:20s} exp={exp:4d} db={cur:4d} {status}")

    # Second pass for Department/Shift Location: ensure Company set
    frappe.db.sql("""UPDATE `tabDepartment` SET company='Haritha Hospitals' WHERE (company IS NULL OR company='')""")
    frappe.db.sql("""UPDATE `tabShift Location` SET company='Haritha Hospitals' WHERE (company IS NULL OR company='')""")
    frappe.db.commit()
    print(f"\n  post-pass: Department company={frappe.db.count('Department', {'company': 'Haritha Hospitals'})}/{frappe.db.count('Department')}")
    print(f"  post-pass: Shift Location company={frappe.db.count('Shift Location', {'company': 'Haritha Hospitals'})}/{frappe.db.count('Shift Location')}")


main()