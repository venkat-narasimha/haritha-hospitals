"""Debug why Department/Designation/Leave Type fail. Local imports to avoid exec() scoping bug."""
def _rd(fname):
    import csv as csv_mod
    with open(f"/tmp/csvs_{fname}") as f:
        lines = f.readlines()
    ds = next(i for i, l in enumerate(lines) if l.strip() == "## Data") + 1
    return next(csv_mod.DictReader(lines[ds:]))


for entity, fname, docfield_map in [
    ("Department", "department.csv", {"department_name": "department_name", "company": None}),
    ("Designation", "designation.csv", {"name": "name", "description": "description"}),
    ("Leave Type", "leave_type.csv", {"name": "name"}),
]:
    row = _rd(fname)
    print(f"\n--- {entity} ---")
    print(f"  CSV row: {row}")
    try:
        d = frappe.new_doc(entity)
        for df, col in docfield_map.items():
            if col is None:
                continue
            v = row.get(col, "")
            if isinstance(v, str):
                v = v.strip()
            if not v:
                continue
            setattr(d, df, v)
        if entity == "Department":
            d.company = "Haritha Hospitals"
        elif entity == "Leave Type":
            d.company = "Haritha Hospitals"
        d.insert(ignore_permissions=True)
        frappe.db.commit()
        print("  OK")
    except Exception as e:
        import traceback
        traceback.print_exc()