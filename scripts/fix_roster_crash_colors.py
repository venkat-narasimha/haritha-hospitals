"""
Phase 4.10: Fix Roster page crash.

Root cause: Shift Type color field is stored as CapitalCase ('Blue', 'Green', etc.)
per HRMS schema default, but the Roster Vue frontend (apps/hrms/roster/src/components/MonthViewTable.vue)
accesses colors via `colors[shift.color as Color][300]` where `colors = tailwindcss/colors`.
Tailwind CSS colors use LOWERCASE keys. `colors['Blue']` is undefined → `[300]` throws TypeError.

Pre-Phase-4.7 worked because 0 SAs meant no shift cells rendered, no `colors[...]` access.
After Phase 4.7 created 2,511 SAs, every cell with a shift crashes Vue render.

pberpqa works because either Shift Type colors are stored as lowercase there, or
no shifts are visible.

Fix: Normalize Shift Type.color values from CapitalCase to lowercase.
- Direct DB UPDATE (bypass ORM Select validation)
- Also add Property Setter so the dropdown shows lowercase options for future edits

Lesson #124 (new): HRMS Shift Type.color default is CapitalCase ('Blue','Green',...)
but Roster Vue (apps/hrms/roster/) expects lowercase ('blue','green',...) to match Tailwind.
When setting Shift Type colors, always lowercase them. Either:
- Override default to lowercase when creating new Shift Types, OR
- Run this normalization script after bulk import.
"""

import frappe

print("=== Phase 4.10: Fix Roster crash (Shift Type color lowercase normalization) ===\n")

# Pre-state
print("--- Pre-state: Shift Type colors ---")
pre_colors = frappe.db.sql(
    "SELECT name, color FROM `tabShift Type` ORDER BY name",
    as_dict=True,
)
for r in pre_colors:
    print(f"  {r['name']:20} {r['color']!r}")

# Step 1: Build mapping CapitalCase → lowercase
mapping = {
    "Blue": "blue",
    "Cyan": "cyan",
    "Fuchsia": "fuchsia",
    "Green": "green",
    "Lime": "lime",
    "Orange": "orange",
    "Pink": "pink",
    "Red": "red",
    "Violet": "violet",
    "Yellow": "yellow",
}

# Step 2: Direct DB UPDATE (bypass Frappe ORM Select validation)
print("\n--- Step 1: Direct DB UPDATE for color normalization ---")
updated = 0
for st in pre_colors:
    old = st["color"]
    if old in mapping:
        new = mapping[old]
        if old != new:
            frappe.db.sql(
                "UPDATE `tabShift Type` SET color = %s WHERE name = %s",
                (new, st["name"]),
            )
            updated += 1
            print(f"  {st['name']:20} {old!r} → {new!r}")
frappe.db.commit()
print(f"\nUpdated {updated} Shift Type records.")

# Step 3: Property Setter for color field options (so future edits work too)
print("\n--- Step 2: Property Setter for Shift Type.color.options ---")
prop_setter_name = "Shift Type-color-options"
existing = frappe.db.exists("Property Setter", prop_setter_name)
if existing:
    print(f"  Property Setter '{prop_setter_name}' already exists.")
else:
    # Lowercase options (matches Tailwind)
    new_options = "\n".join(mapping.values())  # blue\ncyan\nfuchsia\ngreen\n...
    ps = frappe.get_doc({
        "doctype": "Property Setter",
        "doctype_or_field": "DocField",
        "doc_type": "Shift Type",
        "field_name": "color",
        "property": "options",
        "value": new_options,
        "property_type": "Text",
    })
    ps.insert()
    print(f"  Created Property Setter with lowercase options:\n{new_options}")

# Step 4: Post-state verify
print("\n--- Post-state: Shift Type colors ---")
post_colors = frappe.db.sql(
    "SELECT name, color FROM `tabShift Type` ORDER BY name",
    as_dict=True,
)
for r in post_colors:
    print(f"  {r['name']:20} {r['color']!r}")

# Verify: ensure all are now lowercase
print("\n--- Verification ---")
bad = [r for r in post_colors if r["color"] not in mapping.values()]
if bad:
    print(f"FAIL: {len(bad)} records still have CapitalCase colors:")
    for r in bad:
        print(f"  {r['name']:20} {r['color']!r}")
else:
    print(f"PASS: All {len(post_colors)} Shift Type colors are lowercase.")

# Verify Property Setter
ps_check = frappe.db.get_value(
    "Property Setter",
    "Shift Type-color-options",
    "value",
)
print(f"\nProperty Setter value:\n{ps_check}")

print("\n=== Fix complete ===")
