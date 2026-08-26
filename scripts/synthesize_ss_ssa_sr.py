"""
Synthesize Shift Schedule (5), Shift Schedule Assignment (one per unique
employee+shift_type combo in tabShift Assignment), and Shift Request (8)
for Haritha Hospitals demo site (pberpprod.duckdns.org).

Idempotent: re-running skips anything that already exists.
Run inside bench console:  exec(open("/tmp/synthesize_ss_ssa_sr.py").read())
"""
import json
import frappe

COMPANY = "Haritha Hospitals"
res = {"ss_inserted": 0, "ssa_inserted": 0, "sr_inserted": 0,
       "ssa_skipped_existing": 0, "errors": []}


def commit_every(n, counter=[0]):
    counter[0] += 1
    if counter[0] % n == 0:
        frappe.db.commit()


# ---------------------------------------------------------------- 1. Shift Schedule
SCHEDULES = [
    # (name, shift_type, frequency, repeat_on_days, docstatus)
    ("SS-ICU-MORNING",     "G0900R0830", "Weekly", "1,2,3,4,5",   1),
    ("SS-GENERAL-EVENING", "G1000R0800", "Weekly", "1,2,3,4,5,6", 1),
    ("SS-EMERGENCY-NIGHT", "N2000R1200", "Daily",  "",            1),
    ("SS-ADMIN-DAY",       "M0800R0800", "Weekly", "1,2,3,4,5",   1),
    ("SS-OPD-AFTERNOON",   "A1300S1230", "Weekly", "1,2,3,4,5,6", 1),
]

valid_sts = {r[0] for r in frappe.db.sql("SELECT name FROM `tabShift Type`")}
all_schedules = [s[0] for s in SCHEDULES]

for name, st, freq, days, ds in SCHEDULES:
    if st not in valid_sts:
        res["errors"].append(f"ShiftSchedule {name}: missing shift_type {st}")
        continue
    if frappe.db.exists("Shift Schedule", name):
        continue
    doc = frappe.get_doc({
        "doctype": "Shift Schedule",
        "__newname": name,
        "shift_type": st,
        "frequency": freq,
        "repeat_on_days": days,
        "docstatus": ds,
    })
    doc.insert(ignore_permissions=True)
    res["ss_inserted"] += 1
    commit_every(25)

frappe.db.commit()

# map shift_type -> schedule name (query back so autoname quirks can't break us)
ss_map = {}
for row in frappe.db.sql(
    "SELECT name, shift_type FROM `tabShift Schedule` ORDER BY creation", as_dict=True
):
    ss_map.setdefault(row.shift_type, row.name)
fallback_ss = all_schedules[0] if all_schedules else None

# ------------------------------------------- 2. Shift Schedule Assignment (from real SA combos)
combos = frappe.db.sql(
    """SELECT employee, shift_type, MIN(start_date) AS min_date
       FROM `tabShift Assignment`
       WHERE docstatus = 1
       GROUP BY employee, shift_type""",
    as_dict=True,
)
res["sa_unique_combos"] = len(combos)

for row in combos:
    ssa_name = f"SSA-{row.employee}-{row.shift_type}"
    if frappe.db.exists("Shift Schedule Assignment", ssa_name) or \
       frappe.db.exists("Shift Schedule Assignment",
                        {"employee": row.employee, "shift_type": row.shift_type}):
        res["ssa_skipped_existing"] += 1
        continue
    payload = {
        "doctype": "Shift Schedule Assignment",
        "name": ssa_name,
        "employee": row.employee,
        "shift_type": row.shift_type,
        "shift_schedule": ss_map.get(row.shift_type, fallback_ss),
        "shift_status": "Active",
        "company": COMPANY,
        "enabled": 1,
        "create_shifts_after": row.min_date,
        "docstatus": 1,
    }
    try:
        frappe.get_doc(payload).insert(ignore_permissions=True)
        res["ssa_inserted"] += 1
    except Exception as e:
        msg = str(e)
        if "Duplicate" in msg or "independent of this data" in msg:
            res["ssa_skipped_existing"] += 1
            frappe.db.rollback()
        else:
            res["errors"].append(f"SSA {ssa_name}: {msg[:160]}")
            frappe.db.rollback()
    commit_every(150)

frappe.db.commit()

# ---------------------------------------------------------------- 3. Shift Request
if frappe.db.count("Shift Request") == 0:
    EMP = ["HR-EMP-00213", "HR-EMP-00216", "HR-EMP-00220", "HR-EMP-00306"]
    REQUESTS = [
        # employee_idx, shift_type, from, to, status, docstatus
        (0, "G0900R0830", "2025-03-10", "2025-03-12", "Approved",   1),
        (1, "M0800R0830", "2025-07-01", "2025-07-03", "Approved",   1),
        (0, "N2000R1200", "2025-08-15", "2025-08-16", "Pending",    0),
        (1, "G1000R0830", "2025-09-05", "2025-09-06", "Pending",    0),
        (2, "A1400R0600", "2025-10-20", "2025-10-21", "Pending",    0),
        (3, "G1100R0830", "2025-04-18", "2025-04-19", "Rejected",   1),
        (2, "M0800R0600", "2025-11-10", "2025-11-11", "Withdrawn",  0),
        (3, "N1700S1600", "2025-12-05", "2025-12-06", "Withdrawn",  0),
    ]
    for idx, st, fd, td, status, ds in REQUESTS:
        frappe.get_doc({
            "doctype": "Shift Request",
            "employee": EMP[idx],
            "shift_type": st,
            "from_date": fd,
            "to_date": td,
            "status": status,
            "approver": "Administrator",
            "company": COMPANY,
            "docstatus": ds,
        }).insert(ignore_permissions=True)
        res["sr_inserted"] += 1
    frappe.db.commit()

# ---------------------------------------------------------------- verify
res["final_counts"] = {
    "Shift Schedule": frappe.db.count("Shift Schedule"),
    "Shift Schedule Assignment": frappe.db.count("Shift Schedule Assignment"),
    "Shift Request": frappe.db.count("Shift Request"),
}
print("JSON_RESULT_START")
print(json.dumps(res, default=str))
