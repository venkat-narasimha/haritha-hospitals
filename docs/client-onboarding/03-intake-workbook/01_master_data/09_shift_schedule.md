# Shift Schedule — Intake Sheet

**DocType:** `Shift Schedule` (master)
**Module:** HR / Shift Management
**Autoname rule:** `prompt`

**Required fields:** 2  |  **Optional fields:** 2

## Purpose

Planned rotation pattern (e.g., ICU-Nurse-Day-Rotation). Child rows define which days of the week are active.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `name` | Shift Schedule Name | Data | **Y** | `ICU-Nurse-Day-Rotation` | non-empty (autoname='prompt') |  |
| `shift_type` | Shift Type | Link→Shift Type | **Y** | `Morning-8h` | must exist in tabShift Type |  |
| `company` | Company | Link→Company | **N** | `Company A` | must exist if set |  |
| `enable_auto_shift_schedule` | Enable Auto Shift Schedule | Check | **N** | `0` | 0/1 |  |

## Migration notes

- GOTCHA #8 part A: autoname='prompt' — name column REQUIRED in CSV.
- GOTCHA #8 part B: repeat_on_days child rows are DROPPED by Frappe's default fields=['*'] REST pattern. The migration script re-appends child rows programmatically via doc.append().
- CSV format for child rows: header + N rows where same `name` repeats with different `repeat_on_day` column. OR use a separate child CSV file (ask implementer for format).

## Child-table format hint

repeat_on_days child rows: each row has `day` (Sunday-Saturday) and `idx` (sort order)

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Complex rotations (e.g., 4-on-2-off for nurses) | Yes |
| Simple weekday assignments | Use Shift Assignment directly without Shift Schedule |

## Common client mistakes

- Empty `name` column.
- Forgetting repeat_on_days — schedule has no rotation pattern.

## Related gotchas

This DocType touches gotcha(s): `##8` from `scripts/migrate_master_data.py`.
