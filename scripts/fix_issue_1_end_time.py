import frappe

fixes = [
    ("A1300S1230", "01:30:00"),
    ("N1700S1600", "09:00:00"),
    ("N2000R1200", "08:00:00"),
    ("N2200R0800", "06:00:00"),
]
for name, new_end_time in fixes:
    frappe.db.sql(
        "UPDATE `tabShift Type` SET end_time = %s WHERE name = %s",
        (new_end_time, name),
    )
    frappe.db.commit()
    result = frappe.db.sql(
        "SELECT name, end_time FROM `tabShift Type` WHERE name = %s",
        (name,),
        as_dict=True,
    )
    print(f"  {name}: now {result[0]['end_time']}")
print("Issue 1 done")
