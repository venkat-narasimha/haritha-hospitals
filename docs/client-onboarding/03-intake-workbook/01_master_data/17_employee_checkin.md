# Employee Checkin — Intake Sheet

**DocType:** `Employee Checkin`
**Module:** HR / Attendance
**Required fields:** 3
**Optional fields:** 7+

> **Note:** Employee Checkin is the raw punch record (IN/OUT event) typically ingested directly from biometric devices, mobile apps, or manual entry. The HRMS Attendance scheduler then aggregates Checkin pairs into Attendance records.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `employee` | Employee | Link → Employee | Y | "EMP-A001" | must exist | – |
| `employee_name` | Employee Name | Data | Y | "Employee A" | non-empty | Join key for prod → dev ID remap |
| `time` | Time | Datetime | Y | "2025-09-01 09:00:00" | YYYY-MM-DD HH:MM:SS | 24h clock |
| `log_type` | Log Type | Select | Y | "IN" | IN / OUT | Case-sensitive |
| `device_id` | Device ID | Data | N | "BIO-A001" | unique if set | Biometric device ID |
| `source` | Source | Data | N | "Biometric" | Biometric / Mobile / Manual / ERP | Origin of the punch |
| `skip_auto_attendance` | Skip Auto Attendance | Check | N | 0 | 0/1 | Set 1 to exclude from auto-attendance scheduler |
| `shift` | Shift | Link → Shift Type | N | "Shift Type A" | must exist if set | For shift-bound checkins |
| `latitude` | Latitude | Float | N | 17.3850 | -90 to 90 | Geolocation from device |
| `longitude` | Longitude | Float | N | 78.4867 | -180 to 180 | Geolocation from device |
| `attendance` | Attendance | Link → Attendance | N | "HR-ATT-26-09-00001" | must exist if set | Back-link after auto-attendance |

## Healthcare-specific fields

None required as standard. Optional extension: convert `source` from `Data` to a `Select` via Custom Field with hospital-specific values (e.g., `"Biometric-Fingerprint"`, `"Mobile-App"`, `"Manual-Reception"`) — Frappe will then enforce the vocabulary in the dropdown.

## Validation rules

- One Employee Checkin per (employee, time) tuple is NOT enforced by Frappe — duplicate timestamps will coexist (rare, usually a device glitch).
- `log_type` is case-sensitive (`IN`/`OUT`, not `in`/`out`).
- `skip_auto_attendance=1` excludes the punch from the Attendance scheduler — use for admin corrections / test data.
- `time` must be ≤ NOW() for production records (future-dated punches are allowed but flagged for review).

## Common client mistakes

- Wrong case on `log_type` (`in` instead of `IN`) — silent failure, the scheduler ignores the punch.
- Inconsistent `time` timezone — `time` is stored as naive local time; verify the biometric device timezone matches the Frappe site's `timezone` setting (System Settings).
- Leaving `skip_auto_attendance=1` by default — all punches are excluded, no Attendance records created.
- Importing Checkin records out of order — Frappe does not require chronological order, but the Attendance scheduler processes them in `time` order; out-of-order entries can confuse IN/OUT pairing.
- Setting `device_id` to the same value as another employee's `attendance_device_id` — silently breaks Employee-to-Checkin join.
- Forgetting to populate `source` — defaults to `""`; reporting dashboards group by source and will miss untagged punches.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Daily biometric ingestion | **No** — use biometric device sync plugin / webhook |
| Backfill from legacy biometric export | **Yes** — bulk import historical punches |
| Manual entry at reception (visitor / contractor punch) | **Yes** — one-off log |
| Mobile-app check-in | **No** — app writes directly via API |
| Test data for UAT | **Yes** — set `skip_auto_attendance=1` |

## Migration notes (post-go-live upload)

- **Employee ID remap by `employee_name`.** Same constraint as Attendance (GOTCHA #7). The upload script remaps `employee` using `employee_name` as the join key. Client CSV MUST supply both `employee` (original) and `employee_name` (the join key).
- **Pairing IN/OUT into Attendance.** The HRMS Attendance scheduler runs as a scheduled task (typically hourly). It pairs Checkin records into Attendance based on `time` proximity and `log_type`. Out-of-order or missing pairs result in Half Day or Absent Attendance. For backfills spanning more than 7 days, manually trigger "Mark Attendance" via the HRMS Attendance tool after import.
- **Duplicate `time` for same employee.** The upload script does NOT pre-check uniqueness — Frappe allows multiple Checkin records at the same `time` (rare but possible from device glitches). The Attendance scheduler uses the EARLIEST IN and LATEST OUT for a given day.
- **`skip_auto_attendance=1` for corrections.** If the punch is a manual correction for an Attendance record that already exists, set `skip_auto_attendance=1` to prevent the scheduler from creating a SECOND Attendance record for the same day.
- **`device_id` should match `Employee.attendance_device_id`.** When a punch arrives with `device_id="BIO-A001"`, the scheduler looks up the Employee whose `attendance_device_id="BIO-A001"` and links them. If no match, the punch is logged but no Employee is linked — the upload script will warn but not fail.

## Related

- **DocType:** `Employee Checkin` — Frappe HR v16.5.0 stock controller
- **Upstream:** Biometric device / mobile app / manual entry
- **Downstream:** `tabAttendance` (auto-attendance scheduler)
- **Related template:** `10_employee.csv` (Employee master, sets `attendance_device_id`)
- **File location:** `docs/client-onboarding/03-intake-workbook/01_master_data/17_employee_checkin.csv`
- **Upload script:** TBD — Wave 4 will add `scripts/upload_employee_checkin.py`
