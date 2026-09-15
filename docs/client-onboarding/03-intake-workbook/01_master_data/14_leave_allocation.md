# Leave Allocation — Intake Sheet

**DocType:** `Leave Allocation` (submittable)
**Module:** HR / Leave
**Autoname rule:** `naming_series (default HR-LAL-.YYYY.MM.-#####)`

**Required fields:** 6  |  **Optional fields:** 0

## Purpose

Per-employee per-leave-type per-period allocation. Auto-generated when Leave Policy Assignment is submitted, OR manually entered for adjustments.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `employee` | Employee | Link→Employee | **Y** | `Employee A` | must exist in tabEmployee |  |
| `leave_type` | Leave Type | Link→Leave Type | **Y** | `Leave Type A` | must exist in tabLeave Type |  |
| `from_date` | From Date | Date | **Y** | `2026-01-01` | YYYY-MM-DD |  |
| `to_date` | To Date | Date | **Y** | `2026-12-31` | YYYY-MM-DD |  |
| `new_leaves_allocated` | New Leaves Allocated | Float | **Y** | `12.0` | >=0 |  |
| `docstatus` | Document Status | Int | **Y** | `1` | 0=Draft/1=Submitted/2=Cancelled |  |

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Mid-year correction | Yes |
| Initial deployment | No — use Leave Policy Assignment instead |

## Common client mistakes

- Filling this template before Leave Policy Assignment — creates duplicate allocations.
