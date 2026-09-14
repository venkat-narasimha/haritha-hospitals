# Leave Period — Intake Sheet

**DocType:** `Leave Period`
**Module:** HR / Leave Management
**Required fields:** 3
**Optional fields:** 2

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `from_date` | From Date | Date | Y | "2026-01-01" | YYYY-MM-DD | Period start |
| `to_date` | To Date | Date | Y | "2026-12-31" | YYYY-MM-DD, >from_date | Period end |
| `is_active` | Is Active | Check | Y | 1 | 0/1 | Only one active per company |
| `company` | Company | Link → Company | N | "ABC Healthcare Pvt Ltd" | must exist | – |
| `fiscal_year` | Fiscal Year | Link → Fiscal Year | N | "FY 2026" | must exist | For reporting |

## Healthcare-specific fields

None required.

## Validation rules

- Only one `is_active=1` period per Company at a time.
- `to_date > from_date`.

## Common client mistakes

- Creating multiple active periods — only one allowed.
- Using fiscal year (April–March for India) vs calendar year — align with Leave Policy allocation dates.
- Forgetting to set `is_active=1` — allocation generation won't trigger.

## Standard hospital leave period

For India: typically Jan 1 to Dec 31 (calendar year) OR Apr 1 to Mar 31 (fiscal year). Pick one based on company's leave cycle. Most hospitals follow calendar year for simplicity.

Recommended: Jan 1 to Dec 31, named "Leave Period 2026".
