"""
Fix Issue B — Option B: 1 SSA per employee.
- Delete 288 orphan SAs (created today, wrongly linked)
- Cancel duplicate SSAs (keep oldest per employee)
- Re-run create_shifts() on remaining 210 SSAs for the 2026-08-28 → 2026-11-26 window

Source: /home/frappe/frappe-bench/apps/hrms/hrms/hr/doctype/shift_schedule_assignment/shift_schedule_assignment.py
create_shifts signature: create_shifts(self, start_date: str, end_date: str | None = None)
default end_date = start_date + 90 days.

Lesson applied: #79 (backup), #72 (verify), #106 (SQL fallback on cancel).
"""
import frappe

START_DATE = "2026-08-28"
END_DATE = "2026-11-26"

# ===== Step 3a: Delete 288 NEW SAs (created today, orphans from prior run) =====
print("=== Step 3a: Deleting orphan SAs (created >= 2026-08-28) ===")
orphan_sas = frappe.db.sql("""
    SELECT name FROM `tabShift Assignment`
    WHERE creation >= '2026-08-28'
""", as_dict=True)
print(f"Found {len(orphan_sas)} orphan SAs to delete")

deleted_sa = 0
delete_failures = []
for sa in orphan_sas:
    try:
        # Try doc-level delete first
        frappe.delete_doc("Shift Assignment", sa["name"], force=True, ignore_permissions=True)
        deleted_sa += 1
    except Exception as e:
        # SQL fallback (Lesson #106) — also nuke linked child rows
        try:
            frappe.db.sql(
                "DELETE FROM `tabShift Assignment` WHERE name = %s", (sa["name"],)
            )
            deleted_sa += 1
        except Exception as e2:
            delete_failures.append(f"{sa['name']}: {e2}")
    frappe.db.commit()

print(f"Deleted {deleted_sa} orphan SAs ({len(delete_failures)} failures)")

# ===== Step 3b: For each employee with multiple SSAs, cancel all but oldest =====
print("\n=== Step 3b: Cancelling duplicate SSAs (keep oldest per employee) ===")
multi = frappe.db.sql("""
    SELECT employee, COUNT(*) c
    FROM `tabShift Schedule Assignment`
    WHERE docstatus = 1
    GROUP BY employee
    HAVING c > 1
""", as_dict=True)
print(f"Found {len(multi)} employees with multiple SSAs")

cancelled = 0
cancel_failures = []
for m in multi:
    employee = m["employee"]
    ssas = frappe.db.sql("""
        SELECT name, creation FROM `tabShift Schedule Assignment`
        WHERE employee = %s AND docstatus = 1
        ORDER BY creation ASC
    """, (employee,), as_dict=True)
    # Keep first (oldest), cancel rest
    for ssa in ssas[1:]:
        try:
            doc = frappe.get_doc("Shift Schedule Assignment", ssa["name"])
            doc.cancel()
        except Exception as e:
            # SQL fallback (Lesson #106)
            try:
                frappe.db.sql(
                    "UPDATE `tabShift Schedule Assignment` SET docstatus = 2 WHERE name = %s",
                    (ssa["name"],),
                )
            except Exception as e2:
                cancel_failures.append(f"{ssa['name']}: {e2}")
                continue
        cancelled += 1
        frappe.db.commit()

print(f"Cancelled {cancelled} duplicate SSAs ({len(cancel_failures)} failures)")

# ===== Step 3c: Re-run create_shifts() for the 210 remaining SSAs =====
print(f"\n=== Step 3c: Re-running create_shifts({START_DATE}, {END_DATE}) ===")
remaining_ssas = frappe.get_all(
    "Shift Schedule Assignment", filters={"docstatus": 1}, pluck="name"
)
print(f"Remaining SSAs (docstatus=1): {len(remaining_ssas)}")

# Reset create_shifts_after on each remaining SSA so cron doesn't re-create from old value
# (We just deleted everything from 2026-08-28 onward; resetting ensures clean state.)
print("Resetting create_shifts_after to start window boundary...")
reset_count = 0
for ssa_name in remaining_ssas:
    try:
        frappe.db.sql(
            "UPDATE `tabShift Schedule Assignment` SET create_shifts_after = %s WHERE name = %s",
            ("2026-08-27", ssa_name),
        )
        reset_count += 1
    except Exception as e:
        print(f"  reset fail {ssa_name}: {e}")
frappe.db.commit()
print(f"Reset create_shifts_after on {reset_count} SSAs")

processed = 0
sa_created = 0
failures = []
for ssa_name in remaining_ssas:
    try:
        ssa_doc = frappe.get_doc("Shift Schedule Assignment", ssa_name)
        ssa_doc.create_shifts(START_DATE, END_DATE)
        processed += 1
        # Count new SAs linked to this SSA in the window
        new_count = frappe.db.sql(
            """
            SELECT COUNT(*) c FROM `tabShift Assignment`
            WHERE shift_schedule_assignment = %s
              AND start_date >= %s
              AND start_date <= %s
        """,
            (ssa_name, START_DATE, END_DATE),
            as_dict=True,
        )[0].c
        sa_created += new_count
        if processed % 25 == 0 or processed == len(remaining_ssas):
            print(
                f"  {processed}/{len(remaining_ssas)} processed, {sa_created} new SAs so far"
            )
        frappe.db.commit()
    except Exception as e:
        failures.append(f"{ssa_name}: {e}")
        frappe.db.rollback()

print(f"\nFinal: {processed}/{len(remaining_ssas)} processed, {sa_created} new SAs created")
if failures:
    print(f"Failures: {len(failures)}")
    for f in failures[:10]:
        print(f"  {f}")

# ===== Summary =====
print("\n=== Post-run Summary ===")
ssa_total = frappe.db.count("Shift Schedule Assignment")
ssa_ds1 = frappe.db.sql(
    "SELECT COUNT(*) c FROM `tabShift Schedule Assignment` WHERE docstatus=1", as_dict=True
)[0].c
ssa_ds2 = frappe.db.sql(
    "SELECT COUNT(*) c FROM `tabShift Schedule Assignment` WHERE docstatus=2", as_dict=True
)[0].c
multi_after = frappe.db.sql(
    "SELECT employee, COUNT(*) c FROM `tabShift Schedule Assignment` WHERE docstatus=1 GROUP BY employee HAVING c > 1",
    as_dict=True,
)
sa_total = frappe.db.count("Shift Assignment")
sa_today = frappe.db.sql(
    "SELECT COUNT(*) c FROM `tabShift Assignment` WHERE start_date <= '2026-08-28' AND end_date >= '2026-08-28'",
    as_dict=True,
)[0].c
sa_range = frappe.db.sql(
    "SELECT MIN(start_date) min_s, MAX(end_date) max_e FROM `tabShift Assignment`",
    as_dict=True,
)[0]
sa_aug_nov = frappe.db.sql(
    "SELECT COUNT(*) c FROM `tabShift Assignment` WHERE start_date BETWEEN '2026-08-28' AND '2026-11-26'",
    as_dict=True,
)[0].c

print(f"SSA total: {ssa_total} (docstatus=1: {ssa_ds1}, docstatus=2: {ssa_ds2})")
print(f"Employees with multi SSA: {len(multi_after)}")
print(f"SA total: {sa_total}")
print(f"SA covering today (2026-08-28): {sa_today}")
print(f"SA range: {sa_range.min_s} → {sa_range.max_e}")
print(f"SA in 2026-08-28 → 2026-11-26: {sa_aug_nov}")