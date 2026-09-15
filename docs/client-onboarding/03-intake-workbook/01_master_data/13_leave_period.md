# Leave Period — Intake Sheet

**DocType:** `Leave Period` (master)
**Module:** HR / Leave
**Autoname rule:** `field:leave_period_name (inferred)`

**Required fields:** 3  |  **Optional fields:** 1

## Purpose

Annual leave cycle boundary (Jan-Dec or Apr-Mar). Allocations and applications scoped to a period.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `leave_period_name` | Leave Period Name | Data | **Y** | `FY 2026` | unique |  |
| `from_date` | From Date | Date | **Y** | `2026-01-01` | YYYY-MM-DD |  |
| `to_date` | To Date | Date | **Y** | `2026-12-31` | YYYY-MM-DD; >= from_date |  |
| `is_active` | Is Active | Check | **N** | `1` | 0/1 |  |

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment | Yes — required |
| Annual rollover | Yes — create new period, mark old inactive |

## Common client mistakes

- Multiple active periods — set is_active=1 on exactly one.
