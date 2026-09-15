# Leave Period — Intake Sheet

**DocType:** Leave Period (not submittable)
**Module:** HR / Leaves
**Required fields:** 3
**Optional fields:** 2

A Leave Period defines a date range over which Leave Allocations and Carry-Forward calculations apply. Typical calendar: a fiscal year or anniversary year (e.g. 2026-09-01 to 2027-08-31).

> **Production note:** Single-site deployments typically have 0 Leave Periods (leave module is configured but not yet active). The template exists for forward-compatibility.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| from_date | From Date | Date | Y | 2026-09-01 | YYYY-MM-DD | period start (inclusive) |
| to_date | To Date | Date | Y | 2027-08-31 | YYYY-MM-DD; >= from_date | period end (inclusive) |
| is_active | Is Active | Check | N | 1 | 0/1 | only one Leave Period should be active at a time per company |
| company | Company | Link→Company | Y | Company A | must exist | required stock field |
| optional_holiday_list | Holiday List for Optional Leave | Link→Holiday List | N | Holiday List A | must exist if set | optional link for restricted-holiday support |

## Migration notes (from research §7)

- **Gotcha #14 — leave module is configured but unpopulated:** 0 Leave Periods at single-site deployments. Template exists for forward-compatibility.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Leave Period", ...}` before constructing the document.
- Leave Period has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.

## Healthcare-specific fields

None. Leave Period has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Leave Period template? |
|---|---|
| First-time leave-module activation | YES — populate one period row |
| Calendar-year fiscal (Jan-Dec) | YES — set from_date=YYYY-01-01, to_date=YYYY-12-31 |
| Anniversary fiscal (Sep-Aug) | YES — set from_date=YYYY-09-01, to_date=YYYY+1-08-31 |
| Switching mid-year between two policies | YES — create overlap periods; mark older one `is_active=0` |

## Common client mistakes

- Setting `from_date > to_date` — fails Date Range validation.
- Setting `is_active = 1` on multiple Leave Periods simultaneously — only one active period per Company. The system picks the latest; older periods still work but new allocations go to the active one.
- Omitting `company` — required Link; fails import.
- Linking to a `Holiday List` that does not exist — fails LinkValidationError.

## Related

- **Leave Allocation** template's `leave_period` Link points here (optional).
- **Holiday List** template's `holiday_list_name` is referenced via `optional_holiday_list` here.
- **Leave Type** has no direct link to Leave Period but is granted within the period's date range.
