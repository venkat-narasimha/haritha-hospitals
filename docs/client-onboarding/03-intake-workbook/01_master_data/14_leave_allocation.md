# Leave Allocation — Intake Sheet

**DocType:** `Leave Allocation` (submittable)
**Module:** HR / Leave Management
**Required fields:** 5
**Optional fields:** 4

> **Note:** Leave Allocation is typically auto-generated from Leave Policy via "Allocate Leaves" button on Leave Period. Manual entry here is for **adjustments only** (mid-year hires, corrections, special grants).

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `employee` | Employee | Link → Employee | Y | "EMP-0001" | must exist | – |
| `leave_type` | Leave Type | Link → Leave Type | Y | "Casual Leave" | must exist | – |
| `from_date` | From Date | Date | Y | "2026-01-01" | YYYY-MM-DD | Allocation start |
| `to_date` | To Date | Date | Y | "2026-12-31" | YYYY-MM-DD, >from_date | Allocation end |
| `new_leaves_allocated` | New Leaves Allocated | Float | Y | 12 | ≥0 | Number of leaves allocated |
| `leave_period` | Leave Period | Link → Leave Period | N | "Leave Period 2026" | must exist if set | Period alignment |
| `leave_policy` | Leave Policy | Link → Leave Policy | N | "Grade A2 Policy" | must exist if set | Source policy |
| `carry_forward` | Carry Forward Unused Leaves | Check | N | 0 | 0/1 | If carry-forward applicable |
| `unused_leaves` | Unused Leaves (carry over) | Float | N | 0 | ≥0 | From previous period |
| `notes` | Notes | Small Text | N | "Mid-year hire adjustment" | – | Reason for manual allocation |

## Healthcare-specific fields

None required.

## Validation rules

- `to_date > from_date`.
- `new_leaves_allocated ≥ 0`.
- One allocation per (employee, leave_type, leave_period) tuple.

## Common client mistakes

- Manually allocating leaves when Leave Policy auto-generation should be used.
- Allocating leaves for past periods — these are rejected (no retroactive allocation).
- Forgetting `carry_forward=1` on Earned Leave allocation — unused EL doesn't roll over.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Bulk allocation at year-start | **No** — use Leave Policy + "Allocate Leaves" tool |
| Mid-year hire (joining 2026-06-01) | **Yes** — manual allocation for remaining period |
| Special grant (e.g., 5 extra CL for award winner) | **Yes** — manual adjustment |
| Correction (allocation was wrong) | **Yes** — cancel + re-allocate |

## Typical mid-year allocation example

For an employee joining 2026-06-01 in Grade A2 (12 CL/year):
- New allocation: `new_leaves_allocated = 12 × (214/365) ≈ 7` (pro-rata)
- `from_date = 2026-06-01`, `to_date = 2026-12-31`
- Leave Period: "Leave Period 2026"
- Leave Policy: "Grade A2 Policy" (for reference)
