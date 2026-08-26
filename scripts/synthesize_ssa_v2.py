#!/usr/bin/env python3
"""SSA v2: 420 SSAs (one per unique employee x shift_type combo), distributed across 5 templates, linked to SA rows."""
import frappe

# 1. Get existing 5 Shift Schedule templates
ss_list = frappe.get_all("Shift Schedule", fields=["name", "shift_type"])
ss_by_shift_type = {ss.shift_type: ss.name for ss in ss_list if ss.shift_type}
ss_names = [ss.name for ss in ss_list]
print("Found {0} SS templates: {1}".format(len(ss_list), ss_names))

# 2. DELETE all existing SSAs (broken from prior run)
frappe.db.sql("DELETE FROM `tabShift Schedule Assignment`")
frappe.db.commit()
print("Deleted all old SSAs")

# 3. Get unique (employee, shift_type) combos from SA
combos = frappe.db.sql("""
    SELECT employee, shift_type, COUNT(*) as sa_count,
           MIN(start_date) as min_date, MAX(end_date) as max_date
    FROM `tabShift Assignment`
    WHERE docstatus = 1
    GROUP BY employee, shift_type
""", as_dict=True)
print("Found {0} unique (employee, shift_type) combos".format(len(combos)))

# 4. For each combo, create SSA + link SA rows
ssa_created = 0
sa_linked = 0
for combo in combos:
    # Pick SS template by shift_type match, else rotate
    ss_name = ss_by_shift_type.get(combo.shift_type, ss_names[ssa_created % len(ss_names)])

    ssa_doc = frappe.get_doc({
        "doctype": "Shift Schedule Assignment",
        "shift_schedule": ss_name,
        "employee": combo.employee,
        "shift_type": combo.shift_type,
        "company": "Haritha Hospitals",
        "enabled": 1,
        "docstatus": 1,
    })
    ssa_doc.insert(ignore_permissions=True)
    ssa_name = ssa_doc.name
    ssa_created += 1

    # Link all SA rows for this combo via set_value (safer than raw UPDATE per Lesson #108)
    sa_rows = frappe.get_all("Shift Assignment",
                              filters={"employee": combo.employee, "shift_type": combo.shift_type, "docstatus": 1},
                              fields=["name"])
    for sa in sa_rows:
        frappe.db.set_value("Shift Assignment", sa.name, "shift_schedule_assignment", ssa_name, update_modified=False)
        sa_linked += 1

    if ssa_created % 50 == 0:
        frappe.db.commit()
        print("  progress: {0} SSAs created, {1} SA linked".format(ssa_created, sa_linked))

frappe.db.commit()
print("SSAs created: {0}".format(ssa_created))
print("SA rows linked: {0}".format(sa_linked))

# 5. Verify
print("--- VERIFY ---")
print("SSA count: {0}".format(frappe.db.count("Shift Schedule Assignment")))
sa_linked_count = frappe.db.sql(
    "SELECT COUNT(*) FROM `tabShift Assignment` WHERE shift_schedule_assignment IS NOT NULL AND shift_schedule_assignment != ''"
)[0][0]
print("SA with shift_schedule_assignment: {0}".format(sa_linked_count))
print("--- SSA by shift_schedule ---")
print(frappe.db.sql(
    "SELECT shift_schedule, COUNT(*) as cnt FROM `tabShift Schedule Assignment` GROUP BY shift_schedule ORDER BY cnt DESC",
    as_dict=True
))
