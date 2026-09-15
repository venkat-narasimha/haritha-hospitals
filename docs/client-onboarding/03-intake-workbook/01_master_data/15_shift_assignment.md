# Shift Assignment — Intake Sheet

**DocType:** `Shift Assignment` (submittable)
**Module:** HR / Shift Management
**Autoname rule:** `prompt`

**Required fields:** 8  |  **Optional fields:** 4

## Purpose

Concrete employee × date-range × shift-type allocation. The operational rotation that drives attendance.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `name` | Shift Assignment Name | Data | **Y** | `Shift Assignment A` | non-empty (autoname='prompt') |  |
| `employee` | Employee | Link→Employee | **Y** | `Employee A` | must exist in tabEmployee |  |
| `employee_name` | Employee Name | Data | **Y** | `Employee A` | non-empty; case-sensitive match |  |
| `shift_type` | Shift Type | Link→Shift Type | **Y** | `Morning-8h` | must exist in tabShift Type |  |
| `company` | Company | Link→Company | **N** | `Company A` | must exist if set |  |
| `start_date` | Start Date | Date | **Y** | `2026-01-01` | YYYY-MM-DD |  |
| `end_date` | End Date | Date | **Y** | `2026-12-31` | YYYY-MM-DD |  |
| `status` | Status | Select | **Y** | `Active` | Active/Inactive |  |
| `docstatus` | Document Status | Int | **Y** | `1` | 0=Draft/1=Submitted/2=Cancelled |  |
| `shift_location` | Shift Location | Link→Shift Location | **N** | `Site A — Main Block` | must exist if set |  |
| `shift_request` | Shift Request | Link→Shift Request | **N** | `` | must exist if set |  |
| `shift_schedule_assignment` | Shift Schedule Assignment | Link→Shift Schedule Assignment | **N** | `` | NULLIFIED by migration script (GOTCHA #9) |  |

## Migration notes

- GOTCHA #7: The script remaps the `employee` Link using `employee_name` as the join key. Both columns REQUIRED — the prod→dev ID mapping needs both.
- GOTCHA #9: `shift_schedule_assignment` is ALWAYS NULLIFIED (set to None) by the migration script regardless of source value. Leave that column blank.
- GOTCHA #9: `_ensure_shift_location()` pre-creates a canonical Shift Location before processing any Shift Assignment. If your client uses a different location name, populate 08_shift_location.csv AND edit `_ensure_shift_location()` accordingly.
- Migration order: Shift Request must migrate BEFORE Shift Assignment (one SA in production references an SR).

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment — bulk rotation | Yes |
| Mid-deployment reassignment | Yes |
| Temporary shift swap | Use Shift Request + workflow |

## Common client mistakes

- Populating shift_schedule_assignment — it will be discarded anyway.
- Missing employee_name — remap will fail.
- Date validation: end_date must be >= start_date, else rejected.

## Related gotchas

This DocType touches gotcha(s): `##7, ##9` from `scripts/migrate_master_data.py`.
