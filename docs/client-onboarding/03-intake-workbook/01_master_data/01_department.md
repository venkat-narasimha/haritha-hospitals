# Department — Intake Sheet

**DocType:** `Department` (master)
**Module:** HR / Setup
**Autoname rule:** `field:department_name`

**Required fields:** 2  |  **Optional fields:** 6

## Purpose

Functional units within a Company. Departments group employees for reporting, approval routing, and cost-center rollups.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `department_name` | Department Name | Data | **Y** | `Department A` | unique within company |  |
| `company` | Company | Link→Company | **Y** | `Company A` | must exist in tabCompany |  |
| `parent_department` | Parent Department | Link→Department | **N** | `Department B` | must exist if set |  |
| `is_group` | Is Group | Check | **N** | `0` | 0/1 |  |
| `leave_block_list` | Leave Block List | Link→Leave Block List | **N** | `` | must exist if set |  |
| `department_code` | Department Code | Data | **N** | `CARD` | free-form short code |  |
| `building` | Building / Wing | Data | **N** | `Main Block - 2nd Floor` | free-form text |  |
| `hod` | Head of Department | Link→Employee | **N** | `` | must exist in Employee |  |

## Migration notes

- Rows with parent_department = 'All Departments' are SKIPPED (GOTCHA #5). Do not import the implicit Frappe root.
- Department Approver rows are pre-seeded (GOTCHA #10) via `_ensure_department_approvers()` BEFORE Shift Request inserts run, so `validate_approver()` passes on the target site.
- Run Department BEFORE Shift Request (migration order enforces this).
- Upsert pattern is idempotent: re-running updates in place, does not duplicate.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Setting up org structure during initial deployment | Yes — required for all clients |
| Adding a new department mid-deployment | Yes — single-row insert |
| Renaming an existing department | Yes — upsert handles name change |
| Hiding a department from HR dropdowns | Use is_group=1 + disable in target, not delete |

## Common client mistakes

- Setting parent_department to 'All Departments' (dropped silently).
- Creating a department with no Company — fails LinkValidationError.
- Using department_code > 10 chars — risks breaking legacy reports.

## Related gotchas

This DocType touches gotcha(s): `##5, ##10` from `scripts/migrate_master_data.py`.
