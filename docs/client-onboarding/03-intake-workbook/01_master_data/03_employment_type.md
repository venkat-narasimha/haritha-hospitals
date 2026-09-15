# Employment Type — Intake Sheet

**DocType:** Employment Type (not submittable)
**Module:** HR / Organization
**Required fields:** 1
**Optional fields:** 0

Employment Type is a simple label for how an employee is engaged (Full-time, Part-time, Contract, Temporary, Internship, Consultant). It is a one-row-per-type master; no children, no children tables, no custom fields.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| employee_type_name | Employment Type | Data | Y | Full-time | unique | autoname=field:employee_type_name; standard set: Full-time / Part-time / Contract / Temporary / Internship / Consultant |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Employment Type", ...}` before constructing the document.
- Employment Type has **zero custom fields** in `haritta_hospital/fixtures/custom_field.json` — the field list is pure stock.
- Import is unconditional — no FK dependencies. Safe to import in any order.

## Healthcare-specific fields

None. The `haritha_hospital` custom app adds zero custom fields to `Employment Type`. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Employment Type template? |
|---|---|
| First-time deployment | YES — populate the 6 standard rows (Full-time, Part-time, Contract, Temporary, Internship, Consultant) |
| Adding a new engagement category | YES — append one row |
| Renaming an existing category | NO — rename via web UI (changing autoname breaks Links) |

## Common client mistakes

- Using different casings for the same type (`full-time` vs `Full-time`) — Data Import will create both. Use Title Case consistently.
- Changing an existing Employment Type's name after Employees link to it — Employees will have a broken `employment_type` Link. Rename via web UI only with cascade-update enabled.
- Adding departments or job-titles into this template — wrong DocType, use Department/Designation templates.

## Related

- **Employee** template has a custom `employment_type` Link field pointing here.
- See `11_leave_type.csv` for parallel structure (label-only master).
