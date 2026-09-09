# Shift Location — Intake Sheet

**DocType:** `Shift Location`
**Module:** HR / Shift Management
**Required fields:** 3 (location_name + lat + long)
**Optional fields:** 4

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `location_name` | Location Name | Data | Y | "Main Hospital - ICU" | unique | autoname from this field |
| `latitude` | Latitude | Float | Y | 17.3850 | -90 to 90 | From site survey |
| `longitude` | Longitude | Float | Y | 78.4867 | -180 to 180 | From site survey |
| `geolocation` | Geolocation | Geolocation | N | – | combined lat/long field | Auto-fills lat/long |
| `checkin_radius` | Check-in Radius | Int | N | 100 | meters | Geofence radius |
| `address` | Address | Text | N | "Main Block, 2nd Floor" | – | Human-readable address |
| `shift_assignment_creation_method` | Shift Assignment Creation Method | Select | N | "Manual" | Manual / Auto / None | – |
| `check_in_offset` | Check-in Offset | Int | N | 0 | minutes before shift start | – |
| `check_out_offset` | Check-out Offset | Int | N | 0 | minutes after shift end | – |

## Healthcare-specific fields

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `zone_type` | Zone Type | Select | N | "ICU" | ICU / OT / Ward / OPD / Casualty / Lab / Pharmacy / Admin |
| `floor` | Floor | Data | N | "2nd" | Building floor for multi-floor hospitals |
| `requires_late_attendance_alert` | Late Attendance Alert | Check | N | 1 | For critical zones (ICU, Casualty) |

## Validation rules

- `location_name` unique.
- `latitude ∈ [-90, 90]`, `longitude ∈ [-180, 180]`.
- `checkin_radius ≥ 0`; typical 50–200 m for indoor units, 500 m+ for campus-wide.
- Requires `HR Settings → Allow Geolocation Tracking = 1` (admin enables first).

## Common client mistakes

- Using imprecise coordinates (e.g., city centre instead of building entrance).
- Setting radius too tight (10 m) — fails due to GPS variance; too loose (5 km) — defeats purpose.
- Not creating separate locations for separate buildings (one "Hospital" location for ICU and Casualty).
- Forgetting to enable `Allow Geolocation Tracking` in HR Settings first.

## Typical hospital shift locations

| location_name | latitude | longitude | checkin_radius | zone_type |
|---|---|---|---|---|
| Main Hospital - ICU | (from survey) | (from survey) | 50 | ICU |
| Main Hospital - OT Block | (from survey) | (from survey) | 50 | OT |
| Main Hospital - Casualty | (from survey) | (from survey) | 75 | Casualty |
| Main Hospital - Wards | (from survey) | (from survey) | 100 | Ward |
| Main Hospital - OPD | (from survey) | (from survey) | 150 | OPD |
| Main Hospital - Lab | (from survey) | (from survey) | 100 | Lab |
| Main Hospital - Pharmacy | (from survey) | (from survey) | 50 | Pharmacy |
| Main Hospital - Admin Block | (from survey) | (from survey) | 200 | Admin |
