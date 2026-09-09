# Auto-Attendance Policies — Configuration Checklist

**Module:** HR / Shift Management
**Phase:** 5 — Configuration, Integrations & UAT
**DocTypes touched:** `Shift Type`, `Shift Location`, `Employee Checkin`, `Attendance`, `HR Settings`

## Pre-requisites

- [ ] All Shift Types imported and signed off
- [ ] All Shift Locations imported with lat/long
- [ ] Biometric devices installed at each Shift Location
- [ ] Biometric device API integration tested (or Data Import of punch logs)
- [ ] HR Settings → Allow Geolocation Tracking = 1
- [ ] All Employee records have `attendance_device_id` populated (if biometric)
- [ ] Holiday Lists assigned to all Employees (via Company or Branch)

## Configuration items

### Enable auto-attendance per Shift Type

For each Shift Type (per `01_master_data/07_shift_type.md`), verify:

- [ ] `enable_auto_attendance` = 1 (for biometric-monitored shifts)
- [ ] `process_attendance_after` = date ≥ today (or earlier, to backfill)
- [ ] `working_hours_threshold_for_half_day` set (e.g., 4 hours)
- [ ] `working_hours_threshold_for_absent` set (e.g., 0 = disabled, or 2 hours)
- [ ] `working_hours_calculation_based_on` = "First and Last Check-in" (default)
- [ ] `determine_check_in_and_check_out` = "Alternating entries" (default) or "Strictly based on Log Type" (for IN/OUT buttons)

### Biometric integration

- [ ] **API endpoint**: `/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field`
- [ ] **Authentication**: Token-based; token stored in biometric device config
- [ ] **Field mapping**: `employee_field_value` → maps to `attendance_device_id` on Employee
- [ ] **Push vs Pull**: Push (device → server on each punch) or Pull (cron job polls device)
- [ ] **Time sync**: NTP on all devices (drift causes wrong shift attribution)
- [ ] **Offline mode**: Device buffers punches when offline; syncs on reconnect
- [ ] **Duplicate handling**: Server deduplicates based on (employee + time + log_type)
- [ ] **Test device → production device**: Document device mapping (serial number → Shift Location)

### Geo-fencing validation

- [ ] `HR Settings → Allow Geolocation Tracking` = 1
- [ ] Each Shift Location has `latitude`, `longitude`, `checkin_radius`
- [ ] Mobile app (if used) validates location on check-in
- [ ] Web-based biometric at fixed terminal skips geofence (no GPS)
- [ ] Override mechanism for legitimate exceptions (e.g., HR manually approves)

### Late entry / early exit policies

For each Shift Type:

- [ ] `enable_late_entry_marking` = 1
- [ ] `late_entry_grace_period` = 15 minutes (or per hospital policy)
- [ ] `enable_early_exit_marking` = 1
- [ ] `early_exit_grace_period` = 15 minutes
- [ ] **Escalation**: How many late entries trigger a warning? (e.g., 3 in a month → email to HR)

### Overtime calculation

For each Shift Type (where overtime applies):

- [ ] `allow_overtime` = 1
- [ ] `overtime_type` = link to Overtime Type
- [ ] Overtime Type: rate (e.g., 1.5x basic for hours beyond 8)
- [ ] Overtime Type: applies on (weekdays / weekends / holidays)
- [ ] Auto-OT calculation triggers via Attendance → check-in/out times

### Attendance adjustment workflow

- [ ] **Manual Attendance** — Allowed for specific roles (HR Executive, Department Manager)
- [ ] **Attendance Request** — Employee can request missed punch correction
- [ ] **Approval chain** — Department Manager → HR (typical)
- [ ] **Audit trail** — All manual changes logged with reason

### Holidays and weekly off

- [ ] `mark_auto_attendance_on_holidays` = 0 for most shifts (don't mark present on holiday)
- [ ] `mark_auto_attendance_on_holidays` = 1 for on-call shifts (mark present if working on holiday)
- [ ] Weekly off handled by Holiday List → not by Shift Type
- [ ] Compensatory Off generation for holiday work → auto or manual?

### Reporting

- [ ] **Daily Attendance Report** — Department-wise present/absent/late count
- [ ] **Monthly Attendance Summary** — Per employee, per department
- [ ] **Late Entry Report** — Filter by date range, department
- [ ] **Geofence Violation Log** — Out-of-range check-ins (if mobile app)
- [ ] **Overtime Report** — Hours + payout (if payroll in scope)

## Validation tests

- [ ] Biometric punch on device → Employee Checkin record created within 30 seconds
- [ ] Geofence check-in via mobile → validates location correctly
- [ ] Auto-attendance scheduler runs → Attendance record created with correct status
- [ ] Late entry (punch 15 min after shift start) → flagged but Present (grace period)
- [ ] Late entry (punch 30 min after shift start) → flagged and Half Day (if threshold met)
- [ ] Early exit (punch 30 min before shift end) → flagged and Half Day (if threshold met)
- [ ] Holiday (Republic Day) → No attendance auto-marked (unless on-call)
- [ ] Missed punch → Employee Checkin has 1 row → Attendance shows Absent after grace
- [ ] Two punches in 1 min (duplicate) → deduplicated, single Checkin kept
- [ ] Manual attendance entry by HR → reflects in reports + audit trail

## Sign-off

Configured by: _________________________  Date: ___________

Biometric integration verified by: _________________________  Date: ___________

Verified by:   _________________________  Date: ___________

Client HR Lead approval: _________________________  Date: ___________
