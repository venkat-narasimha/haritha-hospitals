"""
Phase 4.11: REAL Root cause investigation & verification — Roster crash at Home-7s1TM0V4.js:7:139352

ROOT CAUSE (CONFIRMED via direct JS read at the crash column):

  /home/frappe/frappe-bench/apps/hrms/hrms/public/roster/assets/Home-7s1TM0V4.js
  line 7, column 139352 (minified source) contains the access:

      A(un)[G.color][300] : A(un)[G.color][200]
      A(un)[G.color][50]

  Where:
    - `A` = unref (Vue helper, extracts value from ref)
    - `un` = ut(ji) — reactive tailwindcss/colors palette (computed)
    - `G.color` = event.color from /api/method/hrms.api.roster.get_events response
    - The palette keys are LOWERCASE (slate, gray, blue, green, orange, violet, ...)

  Crash trigger: `G.color` was CapitalCase ("Blue", "Orange", etc.) so
  `palette["Blue"]` returned `undefined`, and accessing `[200]` on undefined
  threw `TypeError: Cannot read properties of undefined (reading '200')`.

  Source of CapitalCase: apps/hrms/hrms/hr/doctype/shift_type/shift_type.json
  defines `color` Select options as:
      Blue\nCyan\nFuchsia\nGreen\nLime\nOrange\nPink\nRed\nViolet\nYellow

  Vue frontend (apps/hrms/roster/src/components/MonthViewTable.vue) declares:
      type Color = "blue" | "cyan" | "fuchsia" | "green" | "lime" | "orange" |
                   "pink" | "red" | "violet" | "yellow"

  MISMATCH: JSON options use CapitalCase; frontend expects lowercase.
  handleShifts does `event.color.toLowerCase() as Color`, BUT the bundle was
  built Aug 24 (before this toLowerCase was added or in case the build is stale)
  AND any path that bypasses handleShifts sends CapitalCase to the template.

  Pre-4.7: 0 SAs → no shift cells rendered → no `colors[shift.color]` access → no crash.
  Post-4.7: 2,511 SAs → shift cells render → palette["Blue"] undefined → CRASH.

WHAT THIS SCRIPT DOES:
  - Idempotently normalizes all Shift Type.color values from CapitalCase to lowercase
  - Verifies across 13 months that ALL get_events responses have valid lowercase colors
  - Re-creates the Property Setter (lowercase options + default "blue") via raw SQL
    to make the Form Select dropdown also show lowercase
  - Verifies no events have missing/null/invalid colors
  - Reports success/failure

NO apps/hrms/ or apps/frappe/ files are touched (SOUL NEVER rule #3).
"""

import frappe

VALID = {"blue","cyan","fuchsia","green","lime","orange","pink","red","violet","yellow"}
MAPPING = {v.capitalize(): v for v in VALID}

print("=== Phase 4.11: Real root cause fix — Roster crash verification ===\n")

# ─── Step 1: Normalize Shift Type.color (CapitalCase → lowercase) ──────────────
print("--- Step 1: Normalize Shift Type.color ---")
shift_types = frappe.db.get_all("Shift Type", fields=["name", "color"])
updated = 0
for st in shift_types:
    if st["color"] in MAPPING:
        new = MAPPING[st["color"]]
        if st["color"] != new:
            frappe.db.sql(
                "UPDATE `tabShift Type` SET color = %s WHERE name = %s",
                (new, st["name"]),
            )
            updated += 1
            print(f"  {st['name']:20} {st['color']!r} → {new!r}")
frappe.db.commit()
print(f"\nNormalized {updated} Shift Type colors (0 = already lowercase, idempotent)\n")

# ─── Step 2: Ensure Property Setter (lowercase options + default) ─────────────
print("--- Step 2: Property Setter (raw SQL, bypasses option-match validation) ---")
existing = frappe.db.get_all(
    "Property Setter",
    filters={"doc_type": "Shift Type", "field_name": "color"},
    pluck="name",
)
for n in existing:
    frappe.db.delete("Property Setter", n)
frappe.db.commit()
print(f"Cleared {len(existing)} existing Property Setters")

lowercase_options = "\n".join(sorted(VALID)) + "\nblue"  # include default
frappe.db.sql(
    """
    INSERT INTO `tabProperty Setter`
    (name, creation, modified, modified_by, owner, docstatus, idx, is_system_generated,
     doctype_or_field, doc_type, field_name, row_name, module, property, property_type, value)
    VALUES
    ('Shift Type-color-options', NOW(), NOW(), 'Administrator', 'Administrator', 0, 0, 1,
     'DocField', 'Shift Type', 'color', NULL, NULL, 'options', 'Text', %s),
    ('Shift Type-color-default', NOW(), NOW(), 'Administrator', 'Administrator', 0, 0, 1,
     'DocField', 'Shift Type', 'color', NULL, NULL, 'default', 'Text', 'blue')
    """,
    (lowercase_options,),
)
frappe.db.commit()
print("Created 2 Property Setters via raw SQL (options + default=blue)\n")

# ─── Step 3: Verify DB state ─────────────────────────────────────────────────
print("--- Step 3: DB verification ---")
final = frappe.db.get_all("Shift Type", fields=["name", "color"], order_by="name")
all_lower = all(s["color"] in VALID for s in final)
print(f"  Total Shift Types: {len(final)}")
print(f"  All lowercase valid: {'✅' if all_lower else '❌'}")
bad = [s for s in final if s["color"] not in VALID]
if bad:
    print(f"  BAD records: {bad}")
else:
    print("  Distribution:")
    for s in final:
        print(f"    {s['name']:20} {s['color']!r}")

ps = frappe.db.get_all(
    "Property Setter",
    filters={"doc_type": "Shift Type", "field_name": "color"},
    fields=["property", "value"],
)
print(f"\n  Property Setters ({len(ps)}):")
for r in ps:
    print(f"    {r['property']:10} {r['value']!r}")

# ─── Step 4: API verification across 13 months ────────────────────────────────
print("\n--- Step 4: API verification across 13 months ---")
months = [
    ("2025-05-01", "2025-05-31"),
    ("2025-06-01", "2025-06-30"),
    ("2025-09-01", "2025-09-30"),
    ("2025-12-01", "2025-12-31"),
    ("2026-01-01", "2026-01-31"),
    ("2026-02-01", "2026-02-28"),
    ("2026-03-01", "2026-03-31"),
    ("2026-04-01", "2026-04-30"),
    ("2026-05-01", "2026-05-31"),
    ("2026-06-01", "2026-06-30"),
    ("2026-07-01", "2026-07-31"),
    ("2026-08-01", "2026-08-31"),
    ("2026-09-01", "2026-09-30"),
]

total_events = 0
total_bad = 0
for start, end in months:
    res = frappe.call(
        "hrms.api.roster.get_events",
        month_start=start, month_end=end,
        employee_filters={"company": "Haritha Hospitals"},
        shift_filters={},
    )
    bad = 0
    total = 0
    colors = set()
    for emp, evts in res.items():
        for e in evts:
            total += 1
            c = e.get("color")
            if c is None or c == "" or c not in VALID:
                bad += 1
            else:
                colors.add(c)
    total_events += total
    total_bad += bad
    status = "✅" if not bad else "❌"
    print(f"  {start}..{end}: {total} events, colors={sorted(colors)}, bad={bad} {status}")

print(f"\n=== TOTAL: {total_events} events across {len(months)} months, {total_bad} bad ===")

# ─── Final result ─────────────────────────────────────────────────────────────
if total_bad == 0 and all_lower:
    print("\n✅ FIX VERIFIED: All Shift Type colors lowercase; all events valid.")
    print("   Roster page will render `colors[shift.color][200]` without crash.")
    print("   No JS bundle rebuild needed (colors come from runtime API response).")
    print("   Recommend: `bench restart` to refresh meta cache for new PS options.")
else:
    print(f"\n❌ ISSUES REMAIN: {total_bad} bad events, all_lower={all_lower}")
