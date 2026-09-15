# Branch — Intake Sheet

**DocType:** `Branch` (master)
**Module:** HR / Setup
**Autoname rule:** `field:branch`

**Required fields:** 2  |  **Optional fields:** 2

## Purpose

Physical / logical site location. Drives attendance + GPS check-in scope + per-branch Holiday List overrides.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `branch` | Branch | Data | **Y** | `Site A` | unique within company |  |
| `company` | Company | Link→Company | **Y** | `Company A` | must exist in tabCompany |  |
| `branch_code` | Branch Code | Data | **N** | `MAIN` | short code |  |
| `city` | City | Data | **N** | `City A` | free-form |  |

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Multi-site deployment (hospital + clinic + lab) | Yes — required |
| Single-site deployment | Optional — Employee.branch can be empty |

## Common client mistakes

- Creating Branch with no Company — fails LinkValidationError.
- Duplicating branch code across branches — use unique 3-5 char codes.
