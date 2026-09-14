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

## Migration notes (see `scripts/migrate_master_data.py`)

- **Autoname contract — GOTCHA #4.** `Shift Location` uses `autoname = "field:location_name"` and is listed in the script's `PROMPT_AUTONAME_DOCTYPES`. The migration script explicitly pins `payload["name"] = location_name` on insert so Frappe uses the canonical name rather than auto-generating one. Client-side: every row must have a non-empty `location_name`; that value becomes the document `name` used by all downstream Shift Assignment Link fields.
- **Pre-create of canonical name — GOTCHA #9.** The migration script calls `_ensure_shift_location("Hyderabad")` BEFORE processing any `Shift Assignment` records. This is hard-coded because production only uses one Shift Location name. If your client uses a different canonical name (e.g., `"Main Campus"`), either (a) include `Main Campus` here in the intake CSV so the script will create it on first Shift Assignment insert, or (b) edit `_ensure_shift_location()` in `scripts/migrate_master_data.py` to use the canonical name from this sheet.
- **Re-runs are upserts.** Re-running the migration UPDATES existing Shift Location rows by `name`. Lat/long changes will overwrite the live geofence immediately — coordinate changes during go-live should be done as a deliberate re-import, not as a side-effect of an unrelated edit.
- **Out-of-scope Link fields.** The script does NOT populate `shift_assignment_creation_method`, `check_in_offset`, `check_out_offset`, or `geolocation` automatically — they pass through from the source JSON via `_clean_payload()` if present, otherwise they stay blank.
