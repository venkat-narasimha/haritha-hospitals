# Employment Type — Intake Sheet

**DocType:** `Employment Type`
**Module:** HR
**Required fields:** 1
**Optional fields:** 1

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `name` | Employment Type Name | Data | Y | "Full-time" | unique | autoname from this field |
| `description` | Description | Text | N | "Permanent full-time staff" | – | Free text |

## Healthcare-specific fields

None required — standard `description` is enough.

## Validation rules

- `name` is unique; used as a Link field on Employee.
- Cannot delete an Employment Type if any Employee references it (Frappe blocks delete by default).

## Common client mistakes

- Using "Permanent" vs "Full-time" inconsistently — pick one canonical label.
- Creating too granular types (e.g., "Full-time Day", "Full-time Night") — use Shift Type for time-pattern variations, not Employment Type.

## Standard employment types to import

| name | description |
|---|---|
| Full-time | Permanent full-time staff (typically 40h/week or rotational 48h/week for hospital) |
| Part-time | Permanent part-time staff (typically <30h/week) |
| Contract | Fixed-term contract (e.g., 1-year renewable) |
| Locum | Temporary / on-call doctor covering a shift |
| Visiting Consultant | External consultant who visits on scheduled days |
| Internship | Intern (MBBS, Nursing, Lab Tech) |
| Probation | Initial employment period (often 6 months) |
