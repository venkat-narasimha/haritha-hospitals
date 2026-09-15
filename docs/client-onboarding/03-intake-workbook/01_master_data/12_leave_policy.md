# Leave Policy — Intake Sheet

**DocType:** `Leave Policy` (master)
**Module:** HR / Leave
**Autoname rule:** `field:title`

**Required fields:** 1  |  **Optional fields:** 1

## Purpose

Bundle of Leave Types + allocation rules. One per role-group (e.g., Staff Nurse Policy = 12 CL + 6 SL + 24 EL).

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `title` | Title | Data | **Y** | `Leave Policy A` | unique |  |
| `description` | Description | Text | **N** | `Annual leave policy for Staff Nurse role` | free-form |  |

## Child-table format hint

leave_policy_details child rows: `leave_type` (Link→Leave Type) + `annual_allocation` (Float).

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment — define 1-3 policies for different role groups | Yes — required |

## Common client mistakes

- Creating one policy per employee (should be one per role-group).
