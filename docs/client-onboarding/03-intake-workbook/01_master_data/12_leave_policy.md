# Leave Policy — Intake Sheet

**DocType:** `Leave Policy`
**Module:** HR / Leave Management
**Required fields:** 1 (parent) + 1 (per child row)
**Optional fields:** 3

## Parent DocType field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `title` | Title | Data | Y | "Grade A2 Policy" | unique | Visible name |
| `leave_policy_details` | Leave Policy Details (child table) | Table | Y | (see below) | child: leave_type + annual_leaves | REQUIRED child table |

## Child table row fields (`Leave Policy Detail`)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `leave_type` | Leave Type | Link → Leave Type | Y | "Casual Leave" | must exist |
| `annual_allocation` | Annual Allocation | Float | Y | 12 | leaves per year |

## Healthcare-specific fields

None required — Leave Policy is generic across departments.

## Validation rules

- `title` unique.
- At least one row in `leave_policy_details`.
- `annual_allocation ≥ 0`.

## Common client mistakes

- Creating one Leave Policy per employee — should be per Grade (so multiple employees share the same allocation).
- Not aligning Leave Policy with Leave Period — allocation dates must match.
- Forgetting to assign Leave Policy to Employee Grade — leads to no allocation on import.

## Typical hospital leave policy mapping

| Grade | CL | SL | EL | Maternity | Paternity | Comp-Off |
|---|---|---|---|---|---|---|
| A1 (Senior Consultants) | 12 | 12 | 30 | 180 | 15 | as earned |
| A2 (Consultants) | 12 | 12 | 30 | 180 | 15 | as earned |
| B1 (SR / Supervisors) | 12 | 12 | 24 | 180 | 15 | as earned |
| B2 (JR / Sr Nurses) | 12 | 12 | 24 | 180 | 15 | as earned |
| C1 (Residents / Nurses) | 12 | 12 | 18 | 180 | 15 | as earned |
| C2 (Interns / ANM) | 6 | 12 | 0 | 180 | 0 | as earned |
| S1 (Sr Support) | 12 | 12 | 24 | 180 | 15 | as earned |
| S2 (Support) | 12 | 12 | 18 | 180 | 15 | as earned |
| S3 (Jr Support) | 12 | 12 | 12 | 180 | 15 | as earned |

→ Build one Leave Policy per row above; assign each Leave Policy to the matching Employee Grade via Employee.grade link.
