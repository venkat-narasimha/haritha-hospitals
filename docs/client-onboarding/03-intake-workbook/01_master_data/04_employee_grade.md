# Employee Grade — Intake Sheet

**DocType:** Employee Grade (not submittable)
**Module:** HR / Organization
**Required fields:** 1
**Optional fields:** 3

Employee Grade is an optional salary-banding master. It links to a Salary Structure (a separate DocType) and can carry a default base pay + currency for the grade.

> **NOTE for this deployment:** Employee Grade is a **stock DocType but is not populated at single-site hospital deployments** (e.g. the reference deployment has 0 Employee Grade records; every Employee has `grade=None`). See Gotcha #13.
>
> **Recommendation:** Use this template only if the client explicitly maintains grade-based pay bands. Otherwise skip import — Employees work fine without a Grade.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| grade_name | Grade Name | Data | Y | Grade A | unique | autoname=field:grade_name; NOTE: DocType is available but not populated at single-site deployments (see gotcha #13) |
| default_salary_structure | Default Salary Structure | Link | N |  | must exist if set | stock field |
| default_base_pay | Default Base Pay | Currency | N | 0 | >= 0 | stock field; per-grade baseline pay |
| currency | Currency | Link | N |  | must exist if set | stock field; e.g. INR |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Employee Grade", ...}` before constructing the document.
- **Gotcha #13 — unused at single-site:** Employee Grade has 0 custom fields and 0 records at single-site deployments. The template still exists for multi-grade / multi-band clients.
- Employee Grade has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.

## Healthcare-specific fields

None. (Per Section 1 of research — Employee Grade has no custom fields in the fixture.)

## When to use this sheet

| Scenario | Use Employee Grade template? |
|---|---|
| Multi-grade salary bands (Junior/Mid/Senior/Lead) | YES — populate one row per grade |
| Single-band uniform pay | NO — skip entirely |
| Migrating from a legacy payroll system with grades | YES — preserve grades for parallel-run |

## Common client mistakes

- Treating Employee Grade as "department equivalent" — wrong DocType, use `Department`.
- Setting `default_base_pay` without setting `currency` — leaves a currency-less Float that displays oddly in payroll. Set both.
- Linking to a `Salary Structure` that doesn't exist yet — fails with `LinkValidationError`. Import Salary Structures first.
- Assuming Grade is required on Employee — it is optional (the Employee template's `grade` field is custom-optional).

## Related

- **Employee** template has a custom `grade` Link field (optional).
- See `01_department.csv` for parallel org-chart structure.
