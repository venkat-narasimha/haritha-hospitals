#!/usr/bin/env python3
"""
Haritha Hospitals — Shift Attendance Report Linkage Fix.

Phase 3 raw SQL bulk ingest skipped the HRMS compute/derive hooks:
  1. Employee Checkin.attendance = NULL  (12,562 rows) → INNER JOIN in
     default-mode report returns 0 rows.
  2. Employee Checkin.shift + shift_start/end + shift_actual_start/end = NULL.
  3. Attendance.in_time / out_time / working_hours = NULL/0.
  4. Attendance.late_entry / early_exit = 0 (always).

This script is **idempotent** — every UPDATE has WHERE clauses that skip
rows already populated. Safe to re-run.

Invocation:
    docker cp fix_shift_attendance_linkage.py erp-prod-backend-1:/tmp/
    docker exec erp-prod-backend-1 bash -c "cd /home/frappe/frappe-bench && \
      bench --site pberpprod.duckdns.org console < /tmp/fix_shift_attendance_linkage.py"

Author: ERPClaw sub-agent, 2026-08-27
"""
import datetime as _dt
import json as _json
import sys as _sys
import time as _time

import frappe


# ----------------------------- helpers ---------------------------------------

def _stamp() -> str:
    return _dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def _print(*args):
    msg = " ".join(str(a) for a in args)
    print(f"[{_stamp()}] {msg}", flush=True)


def _count(table: str, where: str = "1=1") -> int:
    return frappe.db.sql(
        f"SELECT COUNT(*) c FROM `{table}` WHERE {where}"
    )[0][0]


def _step(label: str):
    _print(f"=== {label} ===")


# ----------------------------- Step 1 ----------------------------------------

def step1_link_checkin_to_attendance() -> int:
    """Populate Employee Checkin.attendance via INNER JOIN on Attendance."""
    _step("Step 1: link Employee Checkin → Attendance")
    ec_total_before = _count("tabEmployee Checkin")
    ec_with_att_before = _count(
        "tabEmployee Checkin", "IFNULL(attendance,'') != ''"
    )
    _print(f"  before: EC total={ec_total_before}, with attendance={ec_with_att_before}")

    # Run the UPDATE — returns (matched_rows,).
    result = frappe.db.sql("""
        UPDATE `tabEmployee Checkin` ec
        INNER JOIN tabAttendance a
          ON a.employee = ec.employee
         AND DATE(ec.time) = a.attendance_date
         AND a.status IN ('Present', 'Half Day')
        SET ec.attendance = a.name
        WHERE IFNULL(ec.attendance, '') = ''
    """)
    matched = result[0][0] if result else 0
    frappe.db.commit()
    _print(f"  updated {matched} Employee Checkin rows")

    # Verify
    ec_with_att_after = _count(
        "tabEmployee Checkin", "IFNULL(attendance,'') != ''"
    )
    by_log = frappe.db.sql("""
        SELECT log_type, COUNT(*) c
        FROM `tabEmployee Checkin`
        WHERE IFNULL(attendance,'') != ''
        GROUP BY log_type
    """, as_dict=True)
    _print(f"  after: EC with attendance={ec_with_att_after}, by log_type={by_log}")
    return matched


# ----------------------------- Step 2 ----------------------------------------

def step2_populate_shift_and_times() -> int:
    """Populate EC.shift, shift_start, shift_end, shift_actual_start, shift_actual_end."""
    _step("Step 2: populate EC.shift + shift_start + shift_end")
    # EC.shift + shift_start + shift_end from Attendance + Shift Type
    res1 = frappe.db.sql("""
        UPDATE `tabEmployee Checkin` ec
        INNER JOIN tabAttendance a ON a.name = ec.attendance
        INNER JOIN `tabShift Type` st ON st.name = a.shift
        SET
            ec.shift = a.shift,
            ec.shift_start = TIMESTAMP(DATE(ec.time), st.start_time),
            ec.shift_end = CASE
                WHEN st.end_time >= st.start_time
                    THEN TIMESTAMP(DATE(ec.time), st.end_time)
                ELSE TIMESTAMP(DATE(ec.time) + INTERVAL 1 DAY, st.end_time)
            END
        WHERE IFNULL(ec.attendance, '') != ''
          AND IFNULL(a.shift, '') != ''
          AND (IFNULL(ec.shift,'') = '' OR ec.shift_start IS NULL)
    """)
    r1 = res1[0][0] if res1 else 0
    frappe.db.commit()
    _print(f"  updated {r1} rows for shift/shift_start/shift_end")

    # EC.shift_actual_start (first IN of the day) + shift_actual_end (last OUT of the day)
    _step("Step 2b: populate EC.shift_actual_start + shift_actual_end")
    res2 = frappe.db.sql("""
        UPDATE `tabEmployee Checkin` ec
        INNER JOIN (
            SELECT
                employee,
                DATE(time) AS day,
                MIN(CASE WHEN log_type = 'IN' THEN time END) AS first_in,
                MAX(CASE WHEN log_type = 'OUT' THEN time END) AS last_out
            FROM `tabEmployee Checkin`
            GROUP BY employee, DATE(time)
        ) bounds ON bounds.employee = ec.employee AND DATE(ec.time) = bounds.day
        SET
            ec.shift_actual_start = bounds.first_in,
            ec.shift_actual_end = bounds.last_out
        WHERE ec.shift_actual_start IS NULL OR ec.shift_actual_end IS NULL
    """)
    r2 = res2[0][0] if res2 else 0
    frappe.db.commit()
    _print(f"  updated {r2} rows for shift_actual_start/end")

    # Verify
    n_shift = _count("tabEmployee Checkin", "IFNULL(shift,'') != ''")
    n_ss = _count("tabEmployee Checkin", "shift_start IS NOT NULL")
    n_se = _count("tabEmployee Checkin", "shift_end IS NOT NULL")
    n_actual_start = _count("tabEmployee Checkin", "shift_actual_start IS NOT NULL")
    n_actual_end = _count("tabEmployee Checkin", "shift_actual_end IS NOT NULL")
    _print(
        f"  after: shift={n_shift}, shift_start={n_ss}, shift_end={n_se}, "
        f"shift_actual_start={n_actual_start}, shift_actual_end={n_actual_end}"
    )
    return r1 + r2


# ----------------------------- Step 3 ----------------------------------------

def step3_populate_attendance_times() -> int:
    """Populate Attendance.in_time, out_time, working_hours from linked checkins."""
    _step("Step 3: populate Attendance.in_time/out_time/working_hours")
    res = frappe.db.sql("""
        UPDATE tabAttendance a
        INNER JOIN (
            SELECT
                attendance,
                MIN(CASE WHEN log_type = 'IN' THEN time END) AS in_time,
                MAX(CASE WHEN log_type = 'OUT' THEN time END) AS out_time
            FROM `tabEmployee Checkin`
            WHERE IFNULL(attendance, '') != ''
            GROUP BY attendance
        ) bounds ON bounds.attendance = a.name
        SET
            a.in_time = bounds.in_time,
            a.out_time = bounds.out_time,
            a.working_hours = ROUND(TIMESTAMPDIFF(SECOND, bounds.in_time, bounds.out_time) / 3600.0, 2)
        WHERE a.status IN ('Present', 'Half Day')
          AND (a.in_time IS NULL OR a.out_time IS NULL)
    """)
    n = res[0][0] if res else 0
    frappe.db.commit()
    _print(f"  updated {n} Attendance rows")

    # Verify
    n_in = _count("tabAttendance", "in_time IS NOT NULL")
    n_out = _count("tabAttendance", "out_time IS NOT NULL")
    n_wh = _count("tabAttendance", "working_hours > 0")
    _print(f"  after: in_time={n_in}, out_time={n_out}, working_hours>0={n_wh}")

    sample = frappe.db.sql("""
        SELECT name, employee, attendance_date, status, in_time, out_time,
               working_hours
        FROM tabAttendance
        WHERE in_time IS NOT NULL
        LIMIT 3
    """, as_dict=True)
    for r in sample:
        _print(f"  sample: {r}")
    return n


# ----------------------------- Step 4 ----------------------------------------

def step4_populate_late_early() -> int:
    """Populate Attendance.late_entry + early_exit via time comparison."""
    _step("Step 4: populate Attendance.late_entry + early_exit")
    res = frappe.db.sql("""
        UPDATE tabAttendance a
        INNER JOIN `tabShift Type` st ON st.name = a.shift
        SET
            a.late_entry = CASE
                WHEN a.in_time IS NOT NULL
                 AND TIME(a.in_time) > ADDTIME(TIME(st.start_time),
                       SEC_TO_TIME(IFNULL(st.late_entry_grace_period, 0) * 60))
                THEN 1 ELSE 0
            END,
            a.early_exit = CASE
                WHEN a.out_time IS NOT NULL
                 AND TIME(a.out_time) < SUBTIME(TIME(st.end_time),
                       SEC_TO_TIME(IFNULL(st.early_exit_grace_period, 0) * 60))
                THEN 1 ELSE 0
            END
        WHERE a.status IN ('Present', 'Half Day')
          AND a.shift IS NOT NULL
          AND a.shift != ''
          AND a.in_time IS NOT NULL
    """)
    n = res[0][0] if res else 0
    frappe.db.commit()
    _print(f"  updated {n} Attendance rows")

    # Verify
    n_late = _count("tabAttendance", "late_entry = 1")
    n_early = _count("tabAttendance", "early_exit = 1")
    _print(f"  after: late_entry=1 → {n_late}, early_exit=1 → {n_early}")

    sample = frappe.db.sql("""
        SELECT name, employee, attendance_date, status, in_time, out_time,
               late_entry, early_exit
        FROM tabAttendance
        WHERE late_entry = 1 OR early_exit = 1
        LIMIT 5
    """, as_dict=True)
    for r in sample:
        _print(f"  sample late/early: {r}")
    return n


# ----------------------------- orchestrator ----------------------------------

def run():
    started = _time.time()
    _print(f"=== fix_shift_attendance_linkage.run START (site={frappe.local.site}) ===")
    frappe.flags.in_bulk_update = True

    n1 = step1_link_checkin_to_attendance()
    n2 = step2_populate_shift_and_times()
    n3 = step3_populate_attendance_times()
    n4 = step4_populate_late_early()

    elapsed = round(_time.time() - started, 1)
    _print(f"=== DONE in {elapsed}s — totals: step1={n1} step2={n2} step3={n3} step4={n4} ===")
    return {
        "step1_ec_attendance": n1,
        "step2_ec_shift_times": n2,
        "step3_att_times": n3,
        "step4_att_late_early": n4,
        "elapsed_sec": elapsed,
        "site": frappe.local.site,
        "timestamp": _dt.datetime.utcnow().isoformat() + "Z",
    }


# Auto-run when piped via stdin (bench console < script.py).
if __name__ == "__main__" or True:
    try:
        RESULT = run()
    except Exception as _e:
        _print(f"FATAL: {_e}")
        import traceback
        traceback.print_exc()
        _sys.exit(1)
