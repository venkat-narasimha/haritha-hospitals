# Shift Schedule — Intake Sheet

**DocType:** Shift Schedule (not submittable)
**Module:** HR / Shift Management
**Required fields:** 3 (`name`, `frequency`, `shift_type`) + 1 (child `repeat_on_days`)
**Optional fields:** 1

A Shift Schedule defines a recurring shift pattern (e.g. "OPD Afternoon — every Monday/Wednesday/Friday — shift `A1300S1230`"). It generates Shift Schedule Assignments (a separate DocType, out of P5 scope) for each employee assigned to the schedule.

> **CRITICAL:** `Shift Schedule` has `autoname='prompt'` — the CSV MUST include a `name` column populated with a client-defined schedule code. See Gotcha #8.

## Field reference (parent — Shift Schedule)

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| name | Schedule Name | Data | Y | Schedule A | unique | REQUIRED because autoname=prompt - see gotcha #8; client-defined schedule code |
| frequency | Frequency | Select | Y | Every Week | Every Week / Every 2 Weeks / Every 3 Weeks / Every 4 Weeks | required stock field |
| shift_type | Shift Type | Link | Y | T1 | must exist | required stock field; link to Shift Type |
| amended_from | Amended From | Link | N |  | must exist if set | for amendment workflow only |

## Child table: repeat_on_days (separate Data Import)

The `repeat_on_days` child table is a Table field on Shift Schedule, pointing at the `Assignment Rule Day` child DocType. **One row per day-of-week that the schedule fires on.** Recommended CSV columns for the child import:

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| day | Day | Select | Y | Monday | Monday / Tuesday / Wednesday / Thursday / Friday / Saturday / Sunday | the weekday on which the schedule fires |
| parent | Parent Shift Schedule | Link | Y | Schedule A | must exist | reference back to the parent record |
| parenttype | Parent Type | Data | Y | Shift Schedule | = "Shift Schedule" | constant for this child table |

> **Pattern:** For an "OPD every weekday" schedule, you would import 5 child rows (Monday, Tuesday, Wednesday, Thursday, Friday), each with `parent=Schedule A`.

## Migration notes (from research §7)

- **Gotcha #8 — `autoname='prompt'` + child-table loss in list payloads:** Two obstacles: (a) `/api/resource/<DT>?fields=['*']` strips child rows from list-view responses — fetch each record individually if needed. (b) `autoname='prompt'` means the `name` must be pinned (this is what the `name` column does). Without `name`, every row fails with `Please set the document name`.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Shift Schedule", ...}` before constructing the document.
- Shift Schedule has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.

## Healthcare-specific fields

None. Shift Schedule has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Shift Schedule template? |
|---|---|
| Recurring weekly shift pattern (OPD rotation) | YES — one parent row + N child day rows |
| Ad-hoc one-off shift | NO — use Shift Assignment template instead |
| Rotating weekly patterns (Week 1 = morning, Week 2 = evening) | YES — create two Schedule rows with same shift_type |
| Rotating fortnightly/monthly patterns | YES — set `frequency` accordingly |

## Common client mistakes

- Omitting the `name` column — **CRITICAL**: every row fails.
- Setting `frequency = Every Week` but forgetting to add child `repeat_on_days` rows — schedule fires but no days are selected (paradoxical state).
- Setting `frequency = Every 2 Weeks` but only adding 1 day — schedule fires every other week on that one day. (Often unexpected.)
- Linking to a `Shift Type` that does not exist — fails LinkValidationError. Import Shift Types first.
- Confusing Shift Schedule with Shift Assignment — Schedule = template; Assignment = specific date range for an employee.

## Related

- **Shift Type** template's `shift_type` Link points here (one direction).
- **Shift Assignment** template is the per-employee, per-date-range instantiation.
- **Shift Schedule Assignment** (separate DocType, OUT OF P5 SCOPE) is the linking record between an Employee and a Schedule.
