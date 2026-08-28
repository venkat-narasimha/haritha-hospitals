"""
Fix Haritha Issue 5: Extend 420 Shift Schedule Assignments (SSAs) to today + 90 days.

Steps:
1. UPDATE all SSA create_shifts_after to today (idempotent — skip if already today).
2. Call create_shifts(today, today+90) for each SSA to generate new Shift Assignments.

Note: HRMS ShiftScheduleAssignment.create_shifts(start_date, end_date) creates
1 SA per block of consecutive `repeat_on_days` (e.g., Mon-Fri → 1 SA per week).
Actual SA count will be less than naive "1 per day" estimate (~4-5k vs ~12.6k).

Idempotency: re-running with create_shifts_after already advanced would reset
and create duplicates. Don't re-run blindly.
"""
import frappe
from frappe.utils import getdate, add_days

def main():
    today = getdate("2026-08-28")
    date_to = add_days(today, 90)
    print(f"today={today}, date_to={date_to}")

    # Step 3a: UPDATE all SSA create_shifts_after to today (idempotent)
    ssas = frappe.get_all(
        "Shift Schedule Assignment",
        filters={"enabled": 1, "docstatus": 1},
        fields=["name", "employee", "shift_schedule", "create_shifts_after", "docstatus"],
    )
    print(f"Found {len(ssas)} active submitted SSAs")

    updated_count = 0
    skipped_count = 0
    for ssa in ssas:
        if ssa["create_shifts_after"] != today:
            frappe.db.sql(
                "UPDATE `tabShift Schedule Assignment` SET create_shifts_after = %s WHERE name = %s",
                (today, ssa["name"]),
            )
            updated_count += 1
        else:
            skipped_count += 1
    frappe.db.commit()
    print(f"Updated {updated_count} SSAs create_shifts_after to {today} (skipped {skipped_count} already-today)")

    # Step 3b: Call create_shifts(today, date_to) for each SSA
    ssa_count = 0
    sa_before = frappe.db.count("Shift Assignment")
    failures = []
    for ssa_row in ssas:
        ssa_name = ssa_row["name"]
        try:
            ssa_doc = frappe.get_doc("Shift Schedule Assignment", ssa_name)
            ssa_doc.create_shifts(today, date_to)
            ssa_count += 1
            if ssa_count % 25 == 0:
                # Periodic commit + progress
                frappe.db.commit()
                sa_now = frappe.db.count("Shift Assignment")
                print(f"  processed {ssa_count}/{len(ssas)} SSAs; SAs now {sa_now} (+{sa_now - sa_before})")
        except Exception as e:
            failures.append(f"{ssa_name}: {e}")
            print(f"  FAILED {ssa_name}: {e}")
            frappe.db.rollback()

    frappe.db.commit()
    sa_after = frappe.db.count("Shift Assignment")
    print(f"\nFinal: {ssa_count}/{len(ssas)} SSAs processed, SAs {sa_before} -> {sa_after} (+{sa_after - sa_before} new)")
    if failures:
        print(f"Failures: {len(failures)}")
        for f in failures[:10]:
            print(f"  - {f}")

    # Final summary
    print("\nPost-state summary:")
    print("  SA total:", sa_after)
    print("  SA covering today:", frappe.db.sql(
        "SELECT COUNT(*) c FROM `tabShift Assignment` WHERE start_date <= %s AND end_date >= %s",
        (today, today), as_dict=True))
    print("  SA range:", frappe.db.sql(
        "SELECT MIN(start_date) min_start, MAX(end_date) max_end FROM `tabShift Assignment`", as_dict=True))
    print("  SA in Aug-Nov 2026:", frappe.db.sql(
        "SELECT COUNT(*) c FROM `tabShift Assignment` WHERE start_date BETWEEN %s AND %s",
        (today, date_to), as_dict=True))
    print("  SSA create_shifts_after distribution:", frappe.db.sql(
        "SELECT create_shifts_after, COUNT(*) c FROM `tabShift Schedule Assignment` GROUP BY create_shifts_after ORDER BY create_shifts_after", as_dict=True))

if __name__ == "__main__":
    main()