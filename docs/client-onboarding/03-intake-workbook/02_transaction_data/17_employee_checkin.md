# Employee Checkin — Intake Sheet

**DocType:** `Employee Checkin`
**Module:** HR / Attendance
**Autoname rule:** default Frappe hash (no explicit `naming_series` in stock schema)
**Stock-required fields:** 2 (`employee`, `time`)
**Stock-optional fields:** 15+
**Custom fields:** 0 (per `haritha_hospital/fixtures/custom_field.json` Section 1)

> **Note:** Employee Checkin is the raw punch record (IN / OUT event) typically ingested directly from biometric devices, mobile apps, or manual entry. The HRMS Attendance scheduler then aggregates Checkin pairs into Attendance records.

## Purpose

Raw per-employee punch log that feeds the HRMS Attendance scheduler. Each Checkin is a single datetime stamp tagged with IN or OUT, optionally carrying the source device ID and GPS coordinates. The scheduler runs as a scheduled task (typically hourly) and pairs IN/OUT Checkins into Attendance records based on time proximity and the Employee's Shift Type.

`log_type` is the only Select field with a fixed enum (per Section 4): ` / IN / OUT` — case-sensitive, no lowercase variants accepted.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `employee` | Employee | Link→Employee | Y | `EMP-A001` | must exist in tabEmployee | required stock field (per Section 4) |
| `employee_name` | Employee Name | Data | N | `Employee A` | non-empty | STOCK-optional; RECOMMENDED as join key for prod→dev ID remap (GOTCHA #7) |
| `time` | Time | Datetime | Y | `2025-09-01 09:00:00` | YYYY-MM-DD HH:MM:SS | required stock field; 24h clock, naive local time (per Section 4) |
| `log_type` | Log Type | Select | Y | `IN` | /IN/OUT | required stock field; case-sensitive IN/OUT (per Section 4 options) |
| `shift` | Shift | Link→Shift Type | N | `Shift Type A` | must exist if set | stock-optional; for shift-bound checkins (filled by Attendance scheduler) |
| `device_id` | Location / Device ID | Data | N | `Device-A001` | unique if set | stock-optional; biometric/RFID device tag (Section 4 label: Location / Device ID) |
| `skip_auto_attendance` | Skip Auto Attendance | Check | N | `0` | 0/1 | stock-optional; set 1 to exclude punch from auto-attendance scheduler |
| `attendance` | Attendance Marked | Link→Attendance | N | `HR-ATT-26-09-00001` | must exist if set | stock-optional; back-link after auto-attendance scheduler pairs this punch (Section 4 label: Attendance Marked) |
| `shift_start` | Shift Start | Datetime | N | `2025-09-01 09:00:00` | YYYY-MM-DD HH:MM:SS | stock-optional; planned shift start (set by scheduler) |
| `shift_end` | Shift End | Datetime | N | `2025-09-01 18:00:00` | YYYY-MM-DD HH:MM:SS | stock-optional; planned shift end (set by scheduler) |
| `shift_actual_start` | Shift Actual Start | Datetime | N | `2025-09-01 09:00:00` | YYYY-MM-DD HH:MM:SS | stock-optional; actual shift start after grace/early windows |
| `shift_actual_end` | Shift Actual End | Datetime | N | `2025-09-01 18:00:00` | YYYY-MM-DD HH:MM:SS | stock-optional; actual shift end after grace/early windows |
| `geolocation` | Geolocation | Geolocation | N | `0.0000, 0.0000` | lat,lon string | stock-optional; combined lat,lon captured from mobile app |
| `latitude` | Latitude | Float | N | `0.0000` | -90 to 90 | stock-optional; geolocation from device |
| `longitude` | Longitude | Float | N | `0.0000` | -180 to 180 | stock-optional; geolocation from device |
| `offshift` | Off-shift | Check | N | `0` | 0/1 | stock-optional; 1 when punch is outside any Shift Assignment window |
| `overtime_type` | Overtime Type | Link→Overtime Type | N | `Overtime Type A` | must exist if set | stock-optional; required only if Shift Type.allow_overtime=1 and punch is overtime-eligible |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Employee Checkin", ...}` before constructing the document.
- **Gotcha #7 — Employee ID remap by `employee_name`.** Same constraint as Attendance. The upload script remaps the `employee` field using `employee_name` as the join key. Client CSV MUST supply both `employee` (original) and `employee_name` (the join key), even though `employee_name` is stock-optional.
- **`log_type` is case-sensitive (`IN`/`OUT`, NOT `in`/`out`).** Wrong case is a silent failure — the Attendance scheduler ignores the punch with no warning. Validate the entire CSV before import.
- **`time` is naive local time** (no timezone offset). Verify the biometric device timezone matches the Frappe site's `timezone` setting in System Settings. A mismatch causes all punches to be paired against the wrong shift window.
- **Pairing IN/OUT into Attendance.** The HRMS Attendance scheduler runs as a scheduled task (typically hourly). It pairs Checkin records into Attendance based on `time` proximity and `log_type`. Out-of-order or missing pairs result in Half Day or Absent Attendance. For backfills spanning more than 7 days, manually trigger "Mark Attendance" via the HRMS Attendance tool after import.
- **Duplicate `time` for same employee is NOT enforced.** Frappe allows multiple Checkin records at the same `time` (rare but possible from device glitches). The Attendance scheduler uses the EARLIEST IN and LATEST OUT for a given day.
- **`skip_auto_attendance=1` for corrections.** If the punch is a manual correction for an Attendance record that already exists, set `skip_auto_attendance=1` to prevent the scheduler from creating a SECOND Attendance record for the same day.
- **`device_id` should match `Employee.attendance_device_id`.** When a punch arrives with `device_id="Device-A001"`, the scheduler looks up the Employee whose `attendance_device_id="Device-A001"` and links them. If no match, the punch is logged but no Employee is linked — the upload script will warn but not fail.
- **No custom `source` field.** This template does NOT include a `source` field — it does not exist in the stock `Employee Checkin` schema (Section 4). If a client requires tracking the origin of each punch (Biometric / Mobile / Manual / ERP), that must be added as a new Custom Field to `Employee Checkin` (this project's `haritha_hospital` app does NOT define one per Section 1).
- **No custom `naming_series`.** Section 4 lists no `naming_series` field on `Employee Checkin`. The stock controller's autoname is the default hash. (Production samples show a `HR-CHECKIN-<n>-<seq>` pattern — Section 8 Q? flags this as a custom series set elsewhere; this template does not codify it.)

## Healthcare-specific extensions

None required as standard. For mobile-app checkins at multi-site hospital networks, the `geolocation`, `latitude`, and `longitude` fields can be used to geofence punches to a specific campus — populate them with the device's GPS reading at the time of punch.

If a client requires a strict source vocabulary (Biometric / Mobile / Manual / ERP), that field must be added as a new Custom Field to `Employee Checkin` (this project's `haritha_hospital` app does NOT define one per Section 1).

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Daily biometric ingestion | **No** — use biometric device sync plugin / webhook |
| Backfill from legacy biometric export | **Yes** — bulk import historical punches |
| Manual entry at reception (visitor / contractor punch) | **Yes** — one-off log |
| Mobile-app check-in | **No** — app writes directly via API |
| Test data for UAT | **Yes** — set `skip_auto_attendance=1` |
| Off-shift overtime punch capture | **Yes** — populate `offshift=1` and `overtime_type` |

## Common client mistakes

- Wrong case on `log_type` (`in` instead of `IN`) — silent failure, the scheduler ignores the punch.
- Inconsistent `time` timezone — `time` is stored as naive local time; verify the biometric device timezone matches the Frappe site's `timezone` setting (System Settings).
- Leaving `skip_auto_attendance=1` by default — all punches are excluded, no Attendance records created.
- Importing Checkin records out of chronological order — Frappe does not require it, but the Attendance scheduler processes them in `time` order; out-of-order entries can confuse IN/OUT pairing.
- Setting `device_id` to the same value as another employee's `attendance_device_id` — silently breaks Employee-to-Checkin join.
- Forgetting to populate `latitude` / `longitude` — defaults to `0`; geofencing reports will treat the punch as origin (0,0).
- Linking `attendance` to a row that does not yet exist on the target site — link drops silently at insert time (no `LinkValidationError` for optional Links).
- Creating Checkin records for a date before the Employee's `date_of_joining` — accepted by Frappe but flagged for review.

## Related

- **DocType:** `Employee Checkin` — Frappe HR v16.5.0 stock controller (non-submittable)
- **Upstream:** Biometric device / mobile app / manual entry / API webhook
- **Downstream:** `tabAttendance` (auto-attendance scheduler pairs IN/OUT into a single record)
- **Related template:** `10_employee.csv` (Employee master, sets `attendance_device_id`), `07_shift_type.csv` (Shift Type master, sets `enable_auto_attendance` and grace windows), `16_attendance.csv` (consumes Checkin pairs)
- **File location:** `docs/client-onboarding/03-intake-workbook/01_master_data/17_employee_checkin.csv`
- **Upload script:** TBD — Wave 4 will add `scripts/upload_employee_checkin.py`
