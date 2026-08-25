#!/usr/bin/env python3
"""Investigate the 3 verify failures: shift code format, FK orphans, holiday list."""
import sys
sys.path.insert(0, '/root/.openclaw/workspace/projects/haritha-hospitals/scripts')
from verify_csvs import read_csv_data
from pathlib import Path
from collections import Counter

base = Path('/root/.openclaw/workspace/projects/haritha-hospitals/masters')

# 1. Shift code format — find actual format
print("=" * 70)
print("[A] SHIFT CODE FORMAT — actual codes found")
print("=" * 70)
_, st_rows = read_csv_data(base / 'shift_type.csv')
codes = [r.get('name', '').strip() for r in st_rows if r.get('name')]
print(f"Total: {len(codes)}")
print(f"All codes (sorted):")
for c in sorted(codes):
    print(f"  {c}")
print(f"\nUnique prefixes: {Counter(c[0] for c in codes if c)}")
print(f"\nSample row structure (first row):")
print(f"  {st_rows[0]}")

# 2. FK orphan — shift_assignment.employee vs employee.name
print("\n" + "=" * 70)
print("[B] FK ORPHAN — shift_assignment.employee vs employee.name")
print("=" * 70)
_, emp_rows = read_csv_data(base / 'employee.csv')
_, sa_rows = read_csv_data(base / 'shift_assignment.csv')

emp_names = {r.get('name', '').strip() for r in emp_rows if r.get('name')}
emp_numbers = {r.get('employee_number', '').strip() for r in emp_rows if r.get('employee_number')}
emp_user_ids = {r.get('user_id', '').strip() for r in emp_rows if r.get('user_id')}
emp_attendance_ids = {r.get('attendance_device_id', '').strip() for r in emp_rows if r.get('attendance_device_id')}

sa_emp_vals = [r.get('employee', '').strip() for r in sa_rows if r.get('employee')]
sa_emp_unique = set(sa_emp_vals)

print(f"employee.name count: {len(emp_names)}")
print(f"employee.employee_number count: {len(emp_numbers)}")
print(f"employee.user_id count: {len(emp_user_ids)}")
print(f"employee.attendance_device_id count: {len(emp_attendance_ids)}")
print(f"shift_assignment.employee unique values: {len(sa_emp_unique)}")

# Try to match sa_employee against each emp field
for field_name, field_set in [
    ("employee.name", emp_names),
    ("employee.employee_number", emp_numbers),
    ("employee.user_id", emp_user_ids),
    ("employee.attendance_device_id", emp_attendance_ids),
]:
    matched = sa_emp_unique & field_set
    print(f"  Match against {field_name}: {len(matched)}/{len(sa_emp_unique)} ({len(matched)*100//len(sa_emp_unique)}%)")

print(f"\nSample shift_assignment.employee values: {sorted(sa_emp_unique)[:5]}")
print(f"Sample employee.name values: {sorted(emp_names)[:5]}")
print(f"Sample employee.attendance_device_id values: {sorted(emp_attendance_ids)[:5]}")
print(f"\nFirst shift_assignment row:")
print(f"  {sa_rows[0]}")

# 3. Holiday list
print("\n" + "=" * 70)
print("[C] HOLIDAY LIST — actual holidays")
print("=" * 70)
_, h_rows = read_csv_data(base / 'holiday.csv')
print(f"Total holidays: {len(h_rows)}")
seen_dates = set()
for r in h_rows:
    parent = r.get('parent', '')
    date = r.get('holiday_date', '')
    desc = r.get('description', '')
    weekly_off = r.get('weekly_off', '')
    optional = r.get('optional_holiday', '')
    seen_dates.add(date)
    print(f"  {date} | {desc:30s} | parent={parent[:35]:35s} | weekly_off={weekly_off} | optional={optional}")

# Show holiday_list parents
_, hl_rows = read_csv_data(base / 'holiday_list.csv')
print(f"\nHoliday lists ({len(hl_rows)}):")
for r in hl_rows:
    print(f"  {r}")
