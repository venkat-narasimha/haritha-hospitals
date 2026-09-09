# Employee Grade — Intake Sheet

**DocType:** `Employee Grade`
**Module:** HR
**Required fields:** 1
**Optional fields:** 4

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `grade_name` | Grade Name | Data | Y | "A2" | unique | Pay-band identifier |
| `description` | Description | Text | N | "Junior Doctors and Nurses" | – | Free text |
| `default_currency` | Default Currency | Link → Currency | N | "INR" | must exist | For salary band |
| `min_salary` | Minimum Salary | Currency | N | 40000 | ≥0 | Lower bound of pay band |
| `max_salary` | Maximum Salary | Currency | N | 80000 | ≥min_salary | Upper bound of pay band |

## Healthcare-specific fields

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `pay_band` | Pay Band | Data | N | "Clinical-Band-2" | Optional grouping label |
| `min_experience_years` | Min Experience (years) | Int | N | 2 | For job postings |

## Validation rules

- `grade_name` unique.
- `max_salary ≥ min_salary` (enforced on save).
- `default_currency` defaults to Company currency if left blank.

## Common client mistakes

- Using grade names with inconsistent casing ("A2" vs "a2").
- Setting min/max salary too narrow — leaves no room for increment.
- Not aligning grades with Leave Policy (each grade typically maps to one Leave Policy).

## Typical hospital grade structure

| grade_name | description | min_salary | max_salary |
|---|---|---|---|
| A1 | Senior Consultants / Department Heads | 200000 | 400000 |
| A2 | Consultants | 120000 | 250000 |
| B1 | Senior Residents / Nursing Supervisors | 80000 | 150000 |
| B2 | Junior Doctors / Senior Staff Nurses | 50000 | 100000 |
| C1 | Junior Residents / Staff Nurses | 30000 | 70000 |
| C2 | Interns / ANM | 15000 | 35000 |
| S1 | Senior Support (Admin Manager, Senior Tech) | 40000 | 90000 |
| S2 | Support Staff (Receptionist, Tech, Housekeeping Sup.) | 20000 | 50000 |
| S3 | Junior Support (Housekeeping, Security) | 12000 | 25000 |
