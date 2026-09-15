# Shift Type — Intake Sheet

**DocType:** Shift Type (not submittable)
**Module:** HR / Shift Management
**Required fields:** 3 (`name`, `start_time`, `end_time`)
**Optional fields:** 18+

A Shift Type defines a shift schedule (start, end, grace periods, attendance thresholds, overtime, roster color). It is referenced by Employee (via the custom `default_shift` Link) and by Shift Schedule + Shift Assignment.

> **CRITICAL:** `Shift Type` has `autoname='prompt'` — Frappe does **NOT** auto-generate a name on insert. The CSV MUST include a `name` column populated with a client-defined shift code (e.g. `Morning-8h`, `T1`, `G0900R0830`). See Gotcha #4.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| name | Name | Data | Y | Morning-8h | unique | REQUIRED because autoname=prompt - see gotcha #4; client-defined shift code |
| start_time | Start Time | Time | Y | 08:00:00 | HH:MM:SS | required stock field |
| end_time | End Time | Time | Y | 17:00:00 | HH:MM:SS; can be < start_time (cross-midnight) | required stock field |
| holiday_list | Holiday List | Link | N | Holiday List A | must exist if set | optional link to holiday calendar |
| determine_check_in_and_check_out | Determine Check-in and Check-out | Select | N | Alternating entries as IN and OUT during the same shift | see options list | stock Select |
| working_hours_calculation_based_on | Working Hours Calculation Based On | Select | N | First Check-in and Last Check-out | see options list | stock Select |
| working_hours_threshold_for_half_day | Working Hours Threshold for Half Day | Float | N | 5 | >= 0 | hours; below this counts as Half Day |
| working_hours_threshold_for_absent | Working Hours Threshold for Absent | Float | N | 0 | >= 0 | hours; below this counts as Absent |
| begin_check_in_before_shift_start_time | Begin check-in before shift start time (in minutes) | Int | N | 60 | >= 0 | minutes before start_time allowed |
| late_entry_grace_period | Late Entry Grace Period | Int | N | 0 | >= 0 | minutes of grace for late IN |
| early_exit_grace_period | Early Exit Grace Period | Int | N | 0 | >= 0 | minutes of grace for early OUT |
| allow_check_out_after_shift_end_time | Allow check-out after shift end time (in minutes) | Int | N | 60 | >= 0 | minutes after end_time allowed |
| enable_auto_attendance | Enable Auto Attendance | Check | N | 0 | 0/1 | 1 to auto-create Attendance from Checkins |
| process_attendance_after | Process Attendance After | Date | N |  | YYYY-MM-DD | optional cutoff date |
| mark_auto_attendance_on_holidays | Mark Auto Attendance on Holidays | Check | N | 0 | 0/1 | 1 to mark attendance on holidays too |
| enable_late_entry_marking | Enable Late Entry Marking | Check | N | 0 | 0/1 | 1 to flag late IN |
| enable_early_exit_marking | Enable Early Exit Marking | Check | N | 0 | 0/1 | 1 to flag early OUT |
| color | Roster Color | Select | N | Blue | Blue / Cyan / Fuchsia / Green / Lime / Orange / Pink / Red / Violet | extended by property setter (see Section 2) |
| auto_update_last_sync | Automatically update Last Sync of Checkin | Check | N | 0 | 0/1 | 1 to track last sync timestamp |
| allow_overtime | Allow Overtime | Check | N | 0 | 0/1 | 1 to allow overtime calc on this shift |
| overtime_type | Overtime Type | Link | N |  | must exist if set | link to Overtime Type |

## Migration notes (from research §7)

- **Gotcha #4 — `autoname='prompt'`:** Frappe does NOT auto-generate the name on insert. The `name` column MUST be populated in the CSV (it will become the DocType's primary key). If you omit the column, every row fails with `Please set the document name`.
- **Gotcha #16 — naming convention is client-defined:** Stock allows any string as `name`. Production sites use codes like `G0900R0830` (G=General, 0900=start, R=returns, 0830=duration). The CSV allows arbitrary strings — adopt the client's existing convention.
- **Property setter on `color`:** `haritha_hospital/fixtures/property_setter.json` extends `color` options to include 9 colors (Blue / Cyan / Fuchsia / Green / Lime / Orange / Pink / Red / Violet) and pins default to `blue`. Templates expose the full extended list.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Shift Type", ...}` before constructing the document.

## Healthcare-specific fields

None. Shift Type has zero custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Shift Type template? |
|---|---|
| New deployment with multiple shift patterns (morning/evening/night) | YES — one row per pattern |
| Single 9-5 hospital | YES — one row only |
| Adding a new shift pattern to existing deployment | YES — append row |
| Auto-attendance setup with biometric/RFID device | YES — set `enable_auto_attendance = 1` |

## Common client mistakes

- Omitting the `name` column — **CRITICAL**: every row fails. Always populate it.
- Using the same `name` for two shifts — primary-key collision. Use distinct codes (`Morning-8h` vs `Evening-8h`).
- Setting `end_time < start_time` and assuming it's an error — for night shifts, this is correct (Frappe treats it as cross-midnight).
- Setting `color` to a value outside the 9-color list — fails Select validation. Stick to the property-setter options.
- Setting `overtime_type` without first creating an Overtime Type — fails LinkValidationError.
- Setting `enable_auto_attendance = 1` without configuring `working_hours_threshold_for_half_day` / `..._absent` — Attendance gets created but every record defaults to Present (no half-day / absent threshold applied).

## Related

- **Employee** template has custom `default_shift` Link pointing here.
- **Shift Schedule** template has stock `shift_type` Link pointing here.
- **Shift Assignment** template has stock `shift_type` Link pointing here.
- **Employee Checkin** template has stock `shift` Link (set automatically by device import).
