# Shift Location — Intake Sheet

**DocType:** `Shift Location` (master)
**Module:** HR / Shift Management
**Autoname rule:** `field:location_name`

**Required fields:** 3  |  **Optional fields:** 2

## Purpose

GPS-tagged site location for biometric attendance check-in scope (lat/long + radius from center).

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `location_name` | Location Name | Data | **Y** | `Site A — Main Block` | unique |  |
| `latitude` | Latitude | Float | **Y** | `17.4126` | -90 to 90 |  |
| `longitude` | Longitude | Float | **Y** | `78.4080` | -180 to 180 |  |
| `checkin_radius` | Check-in Radius | Int | **N** | `200` | meters; 50-200 indoors, 500+ for campus |  |
| `address` | Address | Text | **N** | `Street A, City A` | free-form |  |

## Migration notes

- GOTCHA #8: although autoname is `field:location_name`, the migration script includes Shift Location in PROMPT_AUTONAME_DOCTYPES so it pins name explicitly on insert (defensive coding against schema drift).
- The migration script pre-creates ONE canonical Shift Location before processing any Shift Assignment. If client uses a different location name, add that row to this template AND edit `_ensure_shift_location()` in the migration script.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Multi-site deployment with GPS check-in | Yes — required per site |
| Single-site / no GPS check-in | Optional — can be omitted |

## Common client mistakes

- Lat/long with too many decimal places (use 4-6 max).
- checkin_radius = 0 (offices — disables check-in).

## Related gotchas

This DocType touches gotcha(s): `##8` from `scripts/migrate_master_data.py`.
