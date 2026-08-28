import frappe

# Hex → Tailwind name mapping (preserves Venkat-approved color intent)
HEX_TO_NAME = {
    "#4C6EF5": "Blue",    # G (General) blue
    "#51CF66": "Green",   # M (Morning) green
    "#FFA94D": "Orange",  # A (Afternoon) orange
    "#7048E8": "Violet",  # N (Night) purple
}

for hex_val, name in HEX_TO_NAME.items():
    updated = frappe.db.sql(
        "UPDATE `tabShift Type` SET color = %s WHERE color = %s",
        (name, hex_val),
    )
    frappe.db.commit()
    # Verify THIS hex value
    remaining = frappe.db.sql(
        "SELECT COUNT(*) c FROM `tabShift Type` WHERE color = %s",
        (hex_val,),
        as_dict=True,
    )[0].c
    matched = frappe.db.sql(
        "SELECT COUNT(*) c FROM `tabShift Type` WHERE color = %s",
        (name,),
        as_dict=True,
    )[0].c
    print(f"{hex_val} -> {name}: remaining_hex={remaining}, matched_name={matched}")

print("\nFinal color distribution:")
print(frappe.db.sql("SELECT color, COUNT(*) c FROM `tabShift Type` GROUP BY color", as_dict=True))
print("Hex codes remaining:", frappe.db.sql("SELECT COUNT(*) c FROM `tabShift Type` WHERE color LIKE '%#%'", as_dict=True)[0].c)
