# Employment Type — Intake Sheet

**DocType:** `Employment Type` (master)
**Module:** HR / Setup
**Autoname rule:** `field:employee_type_name`

**Required fields:** 1  |  **Optional fields:** 1

## Purpose

Contractual engagement category (Full-time / Part-time / Contract / Intern). Drives leave accrual rules + probation + contract end-date tracking.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `employee_type_name` | Employment Type | Data | **Y** | `Employment Type A` | unique within company |  |
| `description` | Description | Text | **N** | `Full-time permanent staff` | free-form text |  |

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment | Yes — define ~4-7 types |
| Adding a new contract type | Yes — single-row insert |

## Common client mistakes

- Too-granular types (e.g., 'Resident-1st-Year', 'Resident-2nd-Year') — keep to ~4-7 canonical types.
