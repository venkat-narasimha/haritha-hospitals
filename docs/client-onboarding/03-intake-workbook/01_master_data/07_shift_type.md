# Shift Type — Intake Sheet

**DocType:** `Shift Type` (master)
**Module:** HR / Shift Management
**Autoname rule:** `prompt`

**Required fields:** 3  |  **Optional fields:** 11

## Purpose

Reusable shift template that defines when work happens (start/end times, grace periods, auto-attendance policy).

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `name` | Shift Name | Data | **Y** | `Morning-8h` | non-empty (autoname='prompt') |  |
| `start_time` | Start Time | Time | **Y** | `09:00:00` | HH:MM:SS; 24h clock |  |
| `end_time` | End Time | Time | **Y** | `18:00:00` | HH:MM:SS; end_time < start_time means shift spans midnight |  |
| `color` | Color | Select | **N** | `blue` | blue/cyan/fuchsia/green/lime/orange/pink/red |  |
| `holiday_list` | Holiday List | Link→Holiday List | **N** | `Holiday Calendar A` | must exist in tabHoliday List |  |
| `enable_auto_attendance` | Enable Auto Attendance | Check | **N** | `0` | 0/1 |  |
| `process_attendance_after` | Process Attendance After | Date | **N** | `` | YYYY-MM-DD; required if enable_auto_attendance=1 |  |
| `working_hours_threshold_for_half_day` | Working Hours Threshold for Half Day | Float | **N** | `4.5` | hours; 0 disables |  |
| `working_hours_threshold_for_absent` | Working Hours Threshold for Absent | Float | **N** | `2.0` | hours; 0 disables |  |
| `enable_late_entry_marking` | Enable Late Entry Marking | Check | **N** | `0` | 0/1 |  |
| `late_entry_grace_period` | Late Entry Grace Period | Int | **N** | `15` | minutes |  |
| `enable_early_exit_marking` | Enable Early Exit Marking | Check | **N** | `0` | 0/1 |  |
| `early_exit_grace_period` | Early Exit Grace Period | Int | **N** | `15` | minutes |  |
| `allow_overtime` | Allow Overtime | Check | **N** | `0` | 0/1 |  |

## Migration notes

- GOTCHA #4: autoname='prompt' — name column REQUIRED in CSV or ValidationError on insert. The migration script pins name explicitly on every row.
- GOTCHA #6: Shift Type MUST migrate BEFORE Employee. Every Employee.default_shift Link resolves against an already-existing Shift Type when Employee inserts run.
- Migration order: Shift Type is at index 10 in MIGRATION_ORDER (before Employee at 13).

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment — define all shift types used by hospital | Yes — required |
| Adding a new shift type mid-deployment | Yes — single insert |

## Common client mistakes

- Empty `name` column — fails autoname='prompt'.
- Setting process_attendance_after to a past date — auto-attendance reprocesses historical data (expensive).

## Related gotchas

This DocType touches gotcha(s): `##4, ##6` from `scripts/migrate_master_data.py`.
