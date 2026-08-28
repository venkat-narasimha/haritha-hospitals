import frappe

color_map = {
    "G": "#4C6EF5",
    "M": "#51CF66",
    "A": "#FFA94D",
    "N": "#7048E8",
}
sts = frappe.get_all("Shift Type", fields=["name", "color"])
updated = 0
for st in sts:
    prefix = st["name"][0]
    new_color = color_map.get(prefix)
    if new_color and st["color"] != new_color:
        frappe.db.sql(
            "UPDATE `tabShift Type` SET color = %s WHERE name = %s",
            (new_color, st["name"]),
        )
        updated += 1
        result = frappe.db.sql(
            "SELECT name, color FROM `tabShift Type` WHERE name = %s",
            (st["name"],),
            as_dict=True,
        )
        print(f"  {st['name']}: now {result[0]['color']}")
frappe.db.commit()
print(f"Issue 4 script done ({updated} updates; already-applied updates skipped)")
