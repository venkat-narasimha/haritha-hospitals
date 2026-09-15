# Holiday List — Intake Sheet

**DocType:** Holiday List (not submittable)
**Module:** HR / Leaves
**Required fields:** 3 (parent: holiday_list_name, from_date, to_date) + 2 (child Holiday: holiday_date, description)
**Optional fields:** 5+ (parent) + 2 (child)

A Holiday List is a per-company calendar of public holidays + the weekly off day. It is referenced by Employee (via `holiday_list` Link) and by Shift Type (optional). The Holiday List parent has a child table `holidays` (each row = one Holiday entry).

> **Import flow:** This CSV imports the **parent** Holiday List record. The child `Holiday` rows (one per holiday date) are imported **separately** via Data Import on the `Holiday` DocType OR via the Frappe web UI. The child rows are documented in the table below.

## Field reference (parent — Holiday List)

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| holiday_list_name | Holiday List Name | Data | Y | Holiday List A | unique per company | autoname=field:holiday_list_name |
| from_date | From Date | Date | Y | 2026-09-01 | YYYY-MM-DD | list start (inclusive) |
| to_date | To Date | Date | Y | 2027-08-31 | YYYY-MM-DD; >= from_date | list end (inclusive) |
| weekly_off | Weekly Off | Select | N | Sunday | Sunday / Monday / Tuesday / Wednesday / Thursday / Friday / Saturday | day name (not index) - see gotcha #17 |
| color | Color | Color | N | #7042B5 | hex (#RRGGBB) or named CSS color | UI tint for calendar view |
| country | Country | Autocomplete | N |  | free text | optional country label |
| subdivision | Subdivision | Autocomplete | N |  | free text | optional state/region label |
| is_half_day | Is Half Day | Check | N | 0 | 0/1 | enable if half-day holidays exist |

## Child table: Holiday (separate Data Import)

After importing the parent Holiday List, import child Holiday rows. Recommended CSV columns for the `Holiday` DocType:

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| holiday_date | Date | Date | Y | 2026-10-02 | YYYY-MM-DD | specific holiday date |
| description | Description | Text Editor | Y | Sample Holiday | <= 140 chars | free-text name |
| weekly_off | Weekly Off | Check | N | 0 | 0/1 | 1 if this row represents the recurring weekly off (rare in data; usually implicit from `weekly_off` Select) |
| is_half_day | Is Half Day | Check | N | 0 | 0/1 | 1 for half-day holidays |
| parent | Parent Holiday List | Link | Y | Holiday List A | must exist | reference back to the parent record (Frappe Data Import injects this for child rows) |
| parenttype | Parent Type | Data | Y | Holiday List | = "Holiday List" | constant for this child table |

> **Tip:** Most Data Import tools generate the `parent` / `parenttype` columns automatically when you choose "Holiday List" as the parent DocType in the import wizard.

## Migration notes (from research §7)

- **Gotcha #17 — `weekly_off` is a STRING, not an index:** Stock field is Select with full day names. Clients must enter `Sunday` (not `0` or `7`). Verified against production samples.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Holiday List", ...}` before constructing the document.
- Holiday List has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.
- Production patterns: 1 Holiday List per Company; weekly_off typically set to one day; ~10-15 holidays per year.

## Healthcare-specific fields

None. Holiday List has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Holiday List template? |
|---|---|
| Onboarding a new client with their public-holiday calendar | YES — one row per Holiday List |
| Single-site, single holiday calendar | YES — one row only |
| Multi-site, multi-calendar (state-wise holidays) | YES — one row per site/region |
| Just updating one holiday date | NO — use web UI on the existing Holiday List |

## Common client mistakes

- Setting `weekly_off` to a numeric index (`0` for Sunday) — fails with `ValueError`. Use the day name (`Sunday`).
- Setting `from_date` > `to_date` — fails `Date Range` validation.
- Forgetting to import the child `Holiday` rows — parent imports successfully but the calendar shows zero holidays. Import children separately.
- Leaving `weekly_off` blank — stock-optional but functionally required. Calendar widget assumes a default only at the company level.
- Setting `is_half_day = 1` without populating half-day child rows — flag has no effect unless child rows have `is_half_day = 1` too.

## Related

- **Employee** template's `holiday_list` Link points here (functionally required at single-site).
- **Shift Type** template's `holiday_list` Link points here (optional).
- **Leave Application** indirectly uses this via Employee's `holiday_list` for "include holidays in leave span" logic.
