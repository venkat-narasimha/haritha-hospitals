# Shift Location — Intake Sheet

**DocType:** Shift Location (not submittable)
**Module:** HR / Shift Management
**Required fields:** 1
**Optional fields:** 4

A Shift Location is a geofenced site where Checkins are accepted. Each Location has a name, a radius (meters), and lat/long coordinates. Used by Shift Assignment (optional Link) and by Employee Checkin (geo-validation).

> **Single-site deployment note:** Most single-site hospital deployments need only ONE row (e.g. `Site A`). See Gotcha #15.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| location_name | Location Name | Data | Y | Site A | unique | autoname=field:location_name; see gotcha #15 for single-site deployments |
| checkin_radius | Checkin Radius | Int | N | 200 | > 0 meters | geofence radius for Checkin validity |
| latitude | Latitude | Float | N | 0.0000 | -90 to 90 | decimal degrees; WGS84 |
| longitude | Longitude | Float | N | 0.0000 | -180 to 180 | decimal degrees; WGS84 |
| geolocation | Geolocation | Geolocation | N |  | lat,lon format | alternative to separate lat/long |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Shift Location", ...}` before constructing the document.
- **Gotcha #8 — `autoname=field:location_name`:** the autoname field is `location_name`. CSV must populate it.
- **Gotcha #15 — single-site deployments have 1 location:** All Shift Assignments link to a single Shift Location. The template supports multiple rows for multi-site clients but expects 1 row for typical hospital deployments.
- **Migration script pre-creates `_ensure_shift_location('Site A')`:** before Shift Assignment migration. Ensure your Site A row matches this name exactly if you want migration auto-fill to succeed.
- Shift Location has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.

## Healthcare-specific fields

None. Shift Location has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Shift Location template? |
|---|---|
| Single-site hospital | YES — one row only (`Site A`) |
| Multi-site hospital chain | YES — one row per physical site |
| Geofenced attendance only at main entrance | YES — set small radius (50-100m) |
| Geofenced attendance covering entire campus | YES — set larger radius (300-500m) |

## Common client mistakes

- Leaving `latitude` / `longitude` as `0.0` / `0.0` — geofence resolves to "Null Island" off the African coast; no employee Checkin will pass geo-validation.
- Setting `checkin_radius` too small (e.g. `10`) — fringe-area Checkins rejected. Common production value: `200` meters.
- Mixing `geolocation` with separate `latitude` / `longitude` — only use ONE convention per row. Pick lat/long columns for CSV import.
- Setting `location_name` after employees already link to it — primary-key change breaks Shift Assignment Links. Use web UI rename with cascade only.

## Related

- **Shift Assignment** template's `shift_location` Link points here (optional; defaults to None if unset).
- **Employee Checkin** template's `geolocation` / `latitude` / `longitude` fields are validated against the assigned Shift Location's geofence.
