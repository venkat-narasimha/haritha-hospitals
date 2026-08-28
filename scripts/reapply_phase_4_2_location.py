import frappe

# Step 2a: Insert Hyderabad Location (idempotent — handles re-apply case)
loc_name = "Hyderabad"
if frappe.db.exists("Shift Location", loc_name):
    loc = frappe.get_doc("Shift Location", loc_name)
    print(f"Shift Location already exists: {loc.name} (lat={loc.latitude}, lon={loc.longitude}, radius={loc.checkin_radius})")
    # Verify required fields, fix if missing
    updated = False
    if loc.latitude != 17.3850:
        loc.latitude = 17.3850
        updated = True
    if loc.longitude != 78.4867:
        loc.longitude = 78.4867
        updated = True
    if loc.checkin_radius != 200:
        loc.checkin_radius = 200
        updated = True
    if updated:
        loc.save(ignore_permissions=True)
        print(f"Updated Shift Location {loc.name} with canonical coords/radius")
    else:
        print(f"Shift Location {loc.name} already has canonical coords — no changes needed")
else:
    loc = frappe.get_doc({
        "doctype": "Shift Location",
        "location_name": loc_name,
        "checkin_radius": 200,
        "latitude": 17.3850,
        "longitude": 78.4867,
    })
    loc.insert(ignore_permissions=True)
    print(f"Created Shift Location: {loc.name} (lat={loc.latitude}, lon={loc.longitude}, radius={loc.checkin_radius})")

frappe.db.commit()

# Step 2b: Verify SA references resolve
sa_count = frappe.db.sql(
    "SELECT COUNT(*) c FROM `tabShift Assignment` WHERE shift_location = %s",
    (loc_name,),
    as_dict=True,
)[0].c
ssa_count = frappe.db.sql(
    "SELECT COUNT(*) c FROM `tabShift Schedule Assignment` WHERE shift_location = %s",
    (loc_name,),
    as_dict=True,
)[0].c
print(f"SA with loc='{loc_name}': {sa_count}")
print(f"SSA with loc='{loc_name}': {ssa_count}")
print(f"Total Shift Locations: {frappe.db.count('Shift Location')}")