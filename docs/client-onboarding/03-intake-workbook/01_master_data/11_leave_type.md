# Leave Type — Intake Sheet

**DocType:** `Leave Type` (master)
**Module:** HR / Leave
**Autoname rule:** `field:leave_type_name (inferred)`

**Required fields:** 1  |  **Optional fields:** 9

## Purpose

Kind of leave (Sick, Casual, Earned, etc.) with rules for accrual + carry-forward + encashment.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `leave_type_name` | Leave Type | Data | **Y** | `Leave Type A` | unique |  |
| `max_leave_allowed` | Maximum Leave Allowed | Int | **N** | `12` | >=0 |  |
| `max_continuous_days_allowed` | Maximum Continuous Days Allowed | Int | **N** | `5` | >=0 |  |
| `is_carry_forward` | Is Carry Forward | Check | **N** | `0` | 0/1 |  |
| `is_lwp` | Is Leave Without Pay | Check | **N** | `0` | 0/1 |  |
| `is_earned_leave` | Is Earned Leave | Check | **N** | `0` | 0/1 |  |
| `is_compensatory` | Is Compensatory | Check | **N** | `0` | 0/1 |  |
| `allow_encashment` | Allow Encashment | Check | **N** | `0` | 0/1 |  |
| `max_leaves_encashed` | Maximum Leaves Encashed | Int | **N** | `0` | >=0 |  |
| `earning_component` | Earning Component | Link→Salary Component | **N** | `` | must exist if set |  |

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment — define all leave types used by hospital | Yes — required |

## Common client mistakes

- Setting conflicting flags (e.g., is_lwp=1 AND is_earned_leave=1 — usually mutually exclusive).
