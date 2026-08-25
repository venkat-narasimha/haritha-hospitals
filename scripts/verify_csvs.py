#!/usr/bin/env python3
"""
Haritha Hospitals CSV pre/post-ingest verification.

Usage:
  python3 verify_csvs.py [--csvs-dir DIR] [--json OUT.json] [--quiet]

Format expected per CSV:
  Line 1-3 : comment header (# ...)
  Line 4   : blank
  Line 5+  : ## Schema section (markdown table)
  ## Data  : marker line
  Line +1  : column header row
  Line +2+ : data rows

Checks performed:
  1. Row counts vs manifest
  2. Designation collision check (3 known pairs)
  3. Shift duplicate check (A4, B2, C1)
  4. Shift code format = 10-char [P][HHMM][S][HHMM]
  5. Cross-ref Employee <-> Shift Type <-> Shift Assignment FK integrity
  6. Holiday list completeness
  7. Foreign key integrity (all entities)
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path
from collections import defaultdict


# ---- Expected manifest (captured 2026-08-25 21:55 IST from CSVs) ----
# Format per CSV: comment-header (3 lines) + blank + ## Schema (markdown table)
#                  + ## Data marker + CSV header + data rows
EXPECTED_COUNTS = {
    "employee": 210,
    "shift_type": 25,
    "shift_assignment": 5317,
    "attendance": 6300,
    "employee_checkin": 12562,
    "leave_application": 1,
    "designation": 48,
    "holiday_list": 1,
    "holiday": 14,
    "company": 1,
    "department": 36,
    "shift_schedule": 1,
    "shift_schedule_assignment": 1,
    "shift_request": 1,
    "shift_location": 1,
    "leave_type": 7,
    "leave_allocation": 1,
    "fiscal_year": 2,
    "employment_type": 6,
}

# ---- Known collision pairs (resolved in Aug 19 fixes) ----
DESIGNATION_COLLISIONS = [
    ("Physician Assistant", "Physician Asstant"),
    ("Senior Executive", "Sr.Executive"),
    ("Senior Manager", "Sr.Manager"),
]

# ---- Known shift duplicates (resolved in Aug 19 fixes) ----
SHIFT_DUPLICATES = ["A4", "B2", "C1"]

# ---- Shift code regex: [G|M|A|N][HHMM][R|S][HHMM] = 10-char ----
# G=General, M=Morning, A=Afternoon, N=Night
# R=Regular end-time, S=Special/extended end-time (past midnight or split)
SHIFT_CODE_RE = re.compile(r"^[GMAN]\d{4}[RS]\d{4}$")


def find_data_marker(path: Path) -> int:
    """Return 0-indexed line index of '## Data' marker, or -1."""
    with open(path) as f:
        for i, line in enumerate(f):
            if line.strip() == "## Data":
                return i
    return -1


def find_data_section_start(path: Path) -> int:
    """Return 0-indexed line index of FIRST DATA ROW (after ## Data + header)."""
    marker = find_data_marker(path)
    return marker + 2 if marker >= 0 else -1


def find_header_line(path: Path) -> int:
    """Return 0-indexed line index of CSV header (right after ## Data)."""
    marker = find_data_marker(path)
    return marker + 1 if marker >= 0 else -1


def read_csv_data(path: Path) -> tuple[list[str], list[dict]]:
    """Read CSV, return (headers, data_rows_as_dicts)."""
    header_idx = find_header_line(path)
    if header_idx < 0:
        return [], []
    with open(path) as f:
        lines = f.readlines()[header_idx:]
    if not lines:
        return [], []
    reader = csv.DictReader(lines)
    rows = list(reader)
    headers = reader.fieldnames or []
    return headers, rows


def check_row_counts(csvs_dir: Path) -> dict:
    results = {}
    for entity, expected in EXPECTED_COUNTS.items():
        path = csvs_dir / f"{entity}.csv"
        if not path.exists():
            results[entity] = {"expected": expected, "actual": None, "status": "MISSING_FILE"}
            continue
        start = find_data_section_start(path)
        with open(path) as f:
            data_lines = f.readlines()[start:]
        actual = sum(1 for line in data_lines if line.strip())
        status = "OK" if actual == expected else f"MISMATCH (off by {actual - expected:+d})"
        results[entity] = {"expected": expected, "actual": actual, "status": status}
    return results


def check_designation_collisions(csvs_dir: Path) -> dict:
    path = csvs_dir / "designation.csv"
    if not path.exists():
        return {"status": "SKIP", "reason": "designation.csv not found"}
    _, rows = read_csv_data(path)
    names = {r.get("name", "").strip() for r in rows if r.get("name")}
    collisions_found = []
    for a, b in DESIGNATION_COLLISIONS:
        if a in names and b in names:
            collisions_found.append(f"{a} + {b} both present")
    return {
        "status": "FAIL" if collisions_found else "OK",
        "collision_count": len(collisions_found),
        "details": collisions_found,
        "total_designations": len(names),
    }


def check_shift_duplicates(csvs_dir: Path) -> dict:
    path = csvs_dir / "shift_type.csv"
    if not path.exists():
        return {"status": "SKIP", "reason": "shift_type.csv not found"}
    _, rows = read_csv_data(path)
    codes = []
    for r in rows:
        code = r.get("name", "").strip()
        if code:
            codes.append(code)
    dupes = [d for d in SHIFT_DUPLICATES if codes.count(d) > 1]
    return {
        "status": "FAIL" if dupes else "OK",
        "duplicates_found": dupes,
        "total_shift_types": len(codes),
        "unique_codes": len(set(codes)),
    }


def check_shift_code_format(csvs_dir: Path) -> dict:
    path = csvs_dir / "shift_type.csv"
    if not path.exists():
        return {"status": "SKIP", "reason": "shift_type.csv not found"}
    _, rows = read_csv_data(path)
    malformed = []
    for r in rows:
        code = r.get("name", "").strip()
        if code and not SHIFT_CODE_RE.match(code):
            malformed.append(code)
    return {
        "status": "FAIL" if malformed else "OK",
        "malformed_codes": malformed[:10],  # cap output
        "malformed_count": len(malformed),
        "total_codes_checked": len(rows),
    }


def check_fk_integrity(csvs_dir: Path) -> dict:
    """Employee <-> Shift Type <-> Shift Assignment cross-reference.

    Note: Haritha employee.csv has NO 'name' column (PK collision with HRMS).
    Join key for shift_assignment.employee = employee.attendance_device_id (= 'EMP-NNNN').
    """
    entities = {}
    for e in ["employee", "shift_type", "shift_assignment", "department", "designation",
              "leave_application", "holiday_list", "holiday", "shift_schedule",
              "shift_schedule_assignment", "shift_request", "shift_location"]:
        path = csvs_dir / f"{e}.csv"
        if path.exists():
            _, rows = read_csv_data(path)
            entities[e] = rows
        else:
            entities[e] = []

    # Employee join keys (no 'name' column in this schema)
    emp_attendance_ids = {r.get("attendance_device_id", "").strip() for r in entities["employee"]
                          if r.get("attendance_device_id")}
    emp_employee_numbers = {r.get("employee_number", "").strip() for r in entities["employee"]
                            if r.get("employee_number")}

    # Shift Type.name must be unique
    st_names = [r.get("name", "").strip() for r in entities["shift_type"] if r.get("name")]
    st_dupes = [n for n in set(st_names) if st_names.count(n) > 1]

    # Shift Assignment.employee should match employee.attendance_device_id
    sa_orphans_emp = []
    sa_orphans_st = []
    for r in entities["shift_assignment"]:
        emp = r.get("employee", "").strip()
        st = r.get("shift_type", "").strip()
        if emp and emp not in emp_attendance_ids:
            sa_orphans_emp.append(emp)
        if st and st not in set(st_names):
            sa_orphans_st.append(st)

    return {
        "status": "OK" if not (sa_orphans_emp or sa_orphans_st or st_dupes) else "FAIL",
        "employee_join_keys": len(emp_attendance_ids),
        "shift_type_duplicates": st_dupes[:5],
        "shift_assignment_orphan_employees": len(set(sa_orphans_emp)),
        "shift_assignment_orphan_shift_types": len(set(sa_orphans_st)),
        "total_shift_assignments_checked": len(entities["shift_assignment"]),
    }


def check_holiday_completeness(csvs_dir: Path) -> dict:
    """Indian national holidays — Haritha-selected set + Telangana state.

    Note: holidays repeat yearly (2025-01-26 + 2026-01-26 = same holiday).
    Count unique descriptions, not rows.
    """
    HARITHA_NATIONAL_HOLIDAYS = {
        "Republic Day", "Independence Day", "Gandhi Jayanti",
        "Christmas", "Diwali", "Holi", "May Day",
        "Dr. Ambedkar Jayanti",
    }
    path = csvs_dir / "holiday.csv"
    if not path.exists():
        return {"status": "SKIP", "reason": "holiday.csv not found"}
    _, rows = read_csv_data(path)
    descriptions = {r.get("description", "").strip() for r in rows if r.get("description")}
    missing = HARITHA_NATIONAL_HOLIDAYS - descriptions
    return {
        "status": "OK" if not missing else "WARN",
        "total_unique_holidays": len(descriptions),
        "total_rows": len(rows),
        "holidays_list": sorted(descriptions),
        "missing_from_haritha_set": sorted(missing),
    }


def check_fk_holistic(csvs_dir: Path) -> dict:
    """Foreign-key style integrity across all entities."""
    all_refs = {}
    for entity in EXPECTED_COUNTS:
        path = csvs_dir / f"{entity}.csv"
        if path.exists():
            _, rows = read_csv_data(path)
            all_refs[entity] = rows

    # Department must have unique name
    dept_names = [r.get("name", "").strip() for r in all_refs.get("department", []) if r.get("name")]
    dept_dupes = [n for n in set(dept_names) if dept_names.count(n) > 1]

    # Company must have unique name
    comp_names = [r.get("name", "").strip() for r in all_refs.get("company", []) if r.get("name")]
    comp_dupes = [n for n in set(comp_names) if comp_names.count(n) > 1]

    # Designation must have unique name
    des_names = [r.get("name", "").strip() for r in all_refs.get("designation", []) if r.get("name")]
    des_dupes = [n for n in set(des_names) if des_names.count(n) > 1]

    ok = not (dept_dupes or comp_dupes or des_dupes)
    return {
        "status": "OK" if ok else "FAIL",
        "department_dupes": dept_dupes[:5],
        "company_dupes": comp_dupes[:5],
        "designation_dupes": des_dupes[:5],
    }


def run_all(csvs_dir: Path) -> dict:
    return {
        "csvs_dir": str(csvs_dir),
        "checks": {
            "1_row_counts": check_row_counts(csvs_dir),
            "2_designation_collisions": check_designation_collisions(csvs_dir),
            "3_shift_duplicates": check_shift_duplicates(csvs_dir),
            "4_shift_code_format": check_shift_code_format(csvs_dir),
            "5_fk_integrity_emp_st_sa": check_fk_integrity(csvs_dir),
            "6_holiday_completeness": check_holiday_completeness(csvs_dir),
            "7_fk_holistic": check_fk_holistic(csvs_dir),
        },
    }


def print_human(report: dict, quiet: bool):
    print("=" * 70)
    print(f"HARITHA CSV VERIFY REPORT — {report['csvs_dir']}")
    print("=" * 70)

    checks = report["checks"]
    fails = 0
    warns = 0

    for name, result in checks.items():
        if name == "1_row_counts":
            print(f"\n[1] ROW COUNTS")
            for entity, r in result.items():
                icon = "✅" if r["status"] == "OK" else "❌"
                print(f"  {icon} {entity:30s} expected={r['expected']:6}  actual={str(r['actual']):6}  {r['status']}")
                if r["status"] != "OK" and r["status"] != "MISSING_FILE":
                    fails += 1
        else:
            status = result.get("status", "?")
            icon = {"OK": "✅", "WARN": "⚠️ ", "FAIL": "❌", "SKIP": "⏭️ "}.get(status, "?")
            print(f"\n[{name.split('_')[0]}] {name.upper().replace('_', ' ')[2:]} — {icon} {status}")
            for k, v in result.items():
                if k != "status":
                    print(f"    {k}: {v}")
            if status == "FAIL":
                fails += 1
            elif status == "WARN":
                warns += 1

    print("\n" + "=" * 70)
    print(f"SUMMARY: {fails} FAIL(s), {warns} WARN(s)")
    print("=" * 70)
    return fails


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csvs-dir", default="/root/.openclaw/workspace/projects/haritha-hospitals/masters")
    parser.add_argument("--json", help="Write JSON report to file")
    parser.add_argument("--quiet", action="store_true", help="Only print summary line")
    args = parser.parse_args()

    csvs_dir = Path(args.csvs_dir)
    if not csvs_dir.is_dir():
        print(f"ERROR: {csvs_dir} not a directory", file=sys.stderr)
        sys.exit(2)

    report = run_all(csvs_dir)

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2, default=str))

    if args.quiet:
        fails = sum(1 for c in report["checks"].values()
                    if isinstance(c, dict) and c.get("status") == "FAIL")
        print(f"FAILS={fails}")
        sys.exit(1 if fails else 0)

    fails = print_human(report, args.quiet)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
