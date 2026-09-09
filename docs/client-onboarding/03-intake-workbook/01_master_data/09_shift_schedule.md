# Shift Schedule — Intake Sheet

**DocType:** `Shift Schedule` (submittable)
**Module:** HR / Shift Management
**Required fields:** 3 (parent) + 1 (per child row)
**Optional fields:** 5

## Parent DocType field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `shift_type` | Shift Type | Link → Shift Type | Y | "Morning-8h" | must exist | The base shift |
| `from_date` | From Date | Date | Y | "2026-09-01" | YYYY-MM-DD | Start of schedule |
| `to_date` | To Date | Date | Y | "2026-09-30" | YYYY-MM-DD, ≥from_date | End of schedule |
| `frequency` | Frequency | Select | Y | "Every Week" | Every Week / Every 2 Weeks / Every 3 Weeks / Every 4 Weeks | Recurrence |
| `repeat_on_days` | Repeat On Days (child table) | Table → Assignment Rule Day | Y | (see below) | child: day | REQUIRED child table |
| `company` | Company | Link → Company | N | "Haritha Hospitals Pvt Ltd" | must exist | Defaults from shift_type |
| `department` | Department | Link → Department | N | "ICU" | must exist | Optional scope |
| `enable_auto_shift_schedule` | Enable Auto Shift Schedule | Check | N | 1 | 0/1 | Auto-generate Shift Assignments |
| `shift_assignments` | Shift Assignments (child table) | Table | N | (see below) | child: employee + dates | Pre-filled assignments |

## Child table row fields (`Assignment Rule Day`)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `day` | Day | Select | Y | "Monday" | Mon/Tue/Wed/Thu/Fri/Sat/Sun | At least one day required |

## Child table row fields (`Shift Assignment` child, optional)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `employee` | Employee | Link → Employee | Y | "EMP-0001" | must exist |
| `employee_name` | Employee Name | Data | N | "Dr. Sharma" | auto-fetched |
| `shift_type` | Shift Type | Link → Shift Type | Y | "Morning-8h" | must exist |
| `start_date` | Start Date | Date | Y | "2026-09-01" | – |
| `end_date` | End Date | Date | N | "2026-09-30" | blank = ongoing |
| `shift_location` | Shift Location | Link → Shift Location | N | "Main Hospital - ICU" | optional |
| `status` | Status | Select | N | "Active" | Active / Inactive |

## Validation rules

- `to_date ≥ from_date`.
- At least one row in `repeat_on_days` child table.
- `enable_auto_shift_schedule=1` requires `shift_type` to have `enable_auto_attendance=1`.

## Common client mistakes

- Creating too many Shift Schedules (one per employee instead of one per group).
- Not setting `enable_auto_shift_schedule=1` when intending auto-generation.
- Mixing doctors and nurses in one Shift Schedule — they have different shift patterns.

## Typical hospital shift schedule templates

| schedule_name (in `name`) | shift_type | frequency | days | department |
|---|---|---|---|---|
| ICU-Nurse-Day-Rotation | Morning-8h | Every Week | Mon,Tue,Wed,Thu,Fri,Sat,Sun | ICU |
| ICU-Nurse-Evening-Rotation | Evening-8h | Every Week | Mon,Tue,Wed,Thu,Fri,Sat,Sun | ICU |
| ICU-Nurse-Night-Rotation | Night-8h | Every Week | Mon,Tue,Wed,Thu,Fri,Sat,Sun | ICU |
| Ward-Nurse-12h-Day | Day-12h | Every Week | Mon,Wed,Fri,Sun | Wards |
| Ward-Nurse-12h-Night | Night-12h | Every Week | Tue,Thu,Sat | Wards |
| OPD-Doctor-Morning | OPD-Morning | Every Week | Mon,Tue,Wed,Thu,Fri,Sat | OPD |
| OPD-Doctor-Evening | OPD-Evening | Every Week | Mon,Wed,Fri | OPD |
| Admin-General-Duty | General-Duty | Every Week | Mon,Tue,Wed,Thu,Fri,Sat | Admin |
