"""
Haritha Hospitals - Issue 2 fix
Recreate Shift Location "Hyderabad" and backfill shift_location on 5,738 records.

Decision (2026-08-28 11:06 IST, Venkat):
- location_name = "Hyderabad" (no "Main Hospital" prefix)
- latitude = 17.3850, longitude = 78.4867 (Hyderabad city center)
- checkin_radius = 200 meters (hospital grounds)

Affected rows (from pre-check 2026-08-28 11:08 IST):
- Shift Assignment: 5,318 with empty shift_location
- Shift Schedule Assignment: 420 with empty shift_location
- Total: 5,738

Idempotent: INSERT fails (already exists) and UPDATE only matches empty rows.
"""
import frappe

# Step 2a: INSERT 1 Shift Location record
if frappe.db.exists("Shift Location", "Hyderabad"):
    print("Shift Location 'Hyderabad' already exists, skipping INSERT.")
else:
    loc = frappe.get_doc({
        "doctype": "Shift Location",
        "location_name": "Hyderabad",
        "checkin_radius": 200,
        "latitude": 17.3850,
        "longitude": 78.4867,
    })
    loc.insert(ignore_permissions=True)
    if hasattr(loc, 'submit') and getattr(loc, 'docstatus', 0) == 0:
        try:
            loc.submit()
        except Exception as e:
            print(f"Note: submit() skipped: {e}")
    print(f"Created Shift Location: {loc.name}")

# Step 2b: UPDATE SA shift_location
sa_result = frappe.db.sql(
    "UPDATE `tabShift Assignment` SET shift_location = %s WHERE IFNULL(shift_location, '') = ''",
    ("Hyderabad",),
)
frappe.db.commit()
sa_count = frappe.db.sql(
    "SELECT COUNT(*) c FROM `tabShift Assignment` WHERE shift_location = 'Hyderabad'",
    as_dict=True,
)[0]["c"]
print(f"Updated SA shift_location (Hyderabad total now: {sa_count})")

# Step 2c: UPDATE SSA shift_location
ssa_result = frappe.db.sql(
    "UPDATE `tabShift Schedule Assignment` SET shift_location = %s WHERE IFNULL(shift_location, '') = ''",
    ("Hyderabad",),
)
frappe.db.commit()
ssa_count = frappe.db.sql(
    "SELECT COUNT(*) c FROM `tabShift Schedule Assignment` WHERE shift_location = 'Hyderabad'",
    as_dict=True,
)[0]["c"]
print(f"Updated SSA shift_location (Hyderabad total now: {ssa_count})")

print(f"TOTAL backfilled: {sa_count + ssa_count}")
