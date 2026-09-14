# Shift Type — Intake Sheet

**DocType:** `Shift Type`
**Module:** HR / Shift Management
**Required fields:** 3
**Optional fields:** 15+

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `name` | Shift Name | Data | Y | "Morning-8h" | unique | autoname from this field |
| `start_time` | Start Time | Time | Y | "06:00:00" | HH:MM:SS | 24h format |
| `end_time` | End Time | Time | Y | "14:00:00" | HH:MM:SS | end<start ⇒ night shift spans midnight |
| `holiday_list` | Holiday List | Link → Holiday List | N | "State A Holiday Calendar 2026" | must exist | Inherits from Employee/Company if blank |
| `color` | Color | Select | N | "Blue" | Blue/Cyan/Fuchsia/Green/Lime/Orange/Pink/Red/Violet/Yellow | For roster UI |
| `enable_auto_attendance` | Enable Auto Attendance | Check | N | 1 | 0/1 | Drives scheduler |
| `determine_check_in_and_check_out` | Determine Check-in/out | Select | N | "Alternating entries" | "Alternating entries" vs "Strictly based on Log Type" | Biometric handling |
| `working_hours_calculation_based_on` | Working Hours Calc Based On | Select | N | "First and Last Check-in" | First/Last vs Every Valid Check-in/out | Calculation method |
| `begin_check_in_before_shift_start_time` | Begin Check-in Before Shift Start | Int | N | 60 | minutes, ≥0 | Default 60 |
| `allow_check_out_after_shift_end_time` | Allow Check-out After Shift End | Int | N | 60 | minutes, ≥0 | Default 60 |
| `working_hours_threshold_for_half_day` | Half-Day Threshold (hrs) | Float | N | 4.0 | 0 disables | Min hours to count half-day |
| `working_hours_threshold_for_absent` | Absent Threshold (hrs) | Float | N | 0 | 0 disables | Below this = absent |
| `process_attendance_after` | Process Attendance After | Date | N | "2026-09-01" | YYYY-MM-DD | Required if `enable_auto_attendance=1` |
| `enable_late_entry_marking` | Enable Late Entry Marking | Check | N | 1 | 0/1 | Late entry flag |
| `late_entry_grace_period` | Late Entry Grace Period | Int | N | 15 | minutes | Grace period |
| `enable_early_exit_marking` | Enable Early Exit Marking | Check | N | 1 | 0/1 | Early exit flag |
| `early_exit_grace_period` | Early Exit Grace Period | Int | N | 15 | minutes | Grace period |
| `mark_auto_attendance_on_holidays` | Mark Auto Attendance on Holidays | Check | N | 0 | 0/1 | Mark present on holiday? |
| `allow_overtime` | Allow Overtime | Check | N | 0 | 0/1 | OT calculation enabled |
| `overtype_type` | Overtime Type | Link → Overtime Type | N | "" | must exist if allow_overtime=1 | OT rules |
| `auto_update_last_sync` | Auto Update Last Sync | Check | N | 1 | 0/1 | For single biometric device |

## Validation rules

- `end_time < start_time` is allowed → treated as night shift spanning midnight.
- `working_hours_threshold_for_half_day ≥ working_hours_threshold_for_absent`.
- `process_attendance_after` mandatory if `enable_auto_attendance=1`.

## Common client mistakes

- Not setting `end_time < start_time` for night shifts (e.g., typing 22:00 + 8 = next day).
- Forgetting `process_attendance_after` when auto-attendance is enabled (scheduler fails silently).
- Setting `working_hours_threshold_for_half_day=0` and `=0` — same value disables both.
- Using the same color for all shifts — choose distinct colors for visual scanning of roster.

## Recommended hospital shift library

| name | start_time | end_time | enable_auto_attendance | grace | notes |
|---|---|---|---|---|---|
| Morning-8h | 06:00 | 14:00 | 1 | 15 | 8h rotating for nurses/doctors |
| Evening-8h | 14:00 | 22:00 | 1 | 15 | 8h rotating for nurses/doctors |
| Night-8h | 22:00 | 06:00 | 1 | 15 | 8h rotating for nurses/doctors |
| Day-12h | 07:00 | 19:00 | 1 | 20 | 12h shift for ICU nurses |
| Night-12h | 19:00 | 07:00 | 1 | 20 | 12h shift for ICU nurses |
| OPD-Morning | 09:00 | 13:00 | 1 | 15 | OPD consulting hours |
| OPD-Evening | 17:00 | 20:00 | 1 | 15 | OPD consulting hours |
| On-Call | 20:00 | 08:00 | 0 | 0 | Standby; OT-only |
| General-Duty | 09:00 | 18:00 | 1 | 15 | Admin/support staff 9-to-6 |
| Visiting-Consultant | 10:00 | 13:00 | 0 | 0 | Manual attendance |

## Migration notes (see `scripts/migrate_master_data.py`)

- **Autoname contract — GOTCHA #4.** `Shift Type` declares `autoname='prompt'` — Frappe will not auto-generate the document `name` on insert. The migration script explicitly pins `payload["name"] = <source_name>` on every insert so the autoname hook is satisfied. Client-side: every Shift Type row MUST have a non-empty `name` in the CSV; if blank, Frappe will raise `ValidationError: Naming Series 'prompt' is invalid`.
- **Referenced by Employee before Shift Assignment.** `Shift Type` is migrated BEFORE `Holiday List`, `Employee`, and `Shift Assignment`. Every Employee's `default_shift` Link field must resolve against an existing Shift Type by the time Employee inserts run (GOTCHA #6).
- **Upsert semantics.** Re-running the migration UPDATES existing Shift Type rows (does not duplicate). Color / grace-period changes will overwrite the live shift definition, which can change roster behaviour immediately for downstream Shift Schedules.
- **`enable_auto_attendance` + `process_attendance_after`.** Both are needed for the scheduler to run. If `enable_auto_attendance=1` and `process_attendance_after` is blank, the scheduler fails silently — no error in the migration log, but no attendance processing.
