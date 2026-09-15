# Holiday List — Intake Sheet

**DocType:** `Holiday List` (master)
**Module:** HR / Setup
**Autoname rule:** `field:holiday_list_name`

**Required fields:** 3  |  **Optional fields:** 4

## Purpose

Calendar of organizational + statutory holidays. Foundation for Attendance 'On Leave' auto-creation + Leave date calculations.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `holiday_list_name` | Holiday List Name | Data | **Y** | `Holiday Calendar A` | unique |  |
| `from_date` | From Date | Date | **Y** | `2026-01-01` | YYYY-MM-DD |  |
| `to_date` | To Date | Date | **Y** | `2026-12-31` | YYYY-MM-DD; must be >= from_date |  |
| `color` | Color | Color | **N** | `` | color picker |  |
| `country` | Country | Autocomplete | **N** | `` | country name |  |
| `subdivision` | Subdivision | Autocomplete | **N** | `` | state / province |  |
| `weekly_off` | Weekly Off | Select | **N** | `Sunday` | /Sunday/Monday/Tuesday/Wednesday/Thursday/Friday/Saturday |  |

## Healthcare-specific extensions (optional, India-context)

- If client operates in a jurisdiction with state-specific holidays (e.g., regional founding day, religious observance), add to the Holiday rows — not the parent.

## Child-table format hint

CSV may include child Holiday rows by repeating the holiday_list_name with different holiday_date + description values. The migration script processes child rows when the parent is processed.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment — define current year's holidays | Yes — required |
| Annual holiday calendar update | Yes — overwrite with new year's data |

## Common client mistakes

- Setting to_date before from_date — fails ValidationError.
- Mixing up Calendar type with Holiday type — Calendar is the parent, Holiday is the child.
- Omitting weekly_off — calendar UI shows every day as work-day.
