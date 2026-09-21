# Holiday List Assignment — Intake Sheet

**DocType:** Holiday List Assignment (not submittable)
**Module:** HR / Leaves
**Required fields:** 4 (`applicable_for`, `assigned_to`, `holiday_list`, `from_date`)
**Optional fields:** 2 (`employee_name`, `employee_company`)

Holiday List Assignment links a specific Holiday List to a specific **Employee** or **Company**, effective from a given `from_date`. It is the per-employee / per-company override that determines which holiday calendar each employee uses (overriding the Company-level default). Without this assignment, employees inherit the Holiday List from their Employee record (or the Company default).

> **CRITICAL — gotcha captured during Sep 21 audit:** The HRMS **resolver that determines which Holiday List applies to a given employee filters on `docstatus=1`** (Submitted). Records imported via `frappe.get_doc().insert()` are saved at `docstatus=0` (Draft) and are therefore **invisible** to the resolver until they are explicitly submitted via the web UI or `frappe.db.submit()`. See Gotcha #HLA-1 below.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| applicable_for | Applicable For | Select | Y | Employee | Employee / Company | drives the Dynamic Link target; pick `Employee` to assign a Holiday List to a single employee, `Company` for company-wide default |
| assigned_to | Assigned To | Dynamic Link | Y | HR-EMP-00421 | resolves against `applicable_for` | must exist in the target DocType (Employee OR Company) |
| employee_name | Employee Name | Data | N | Test User | non-empty if set | convenience display; auto-fills when `applicable_for=Employee` |
| employee_company | Employee Company | Link→Company | N | Haritha Hospitals | must exist if set | company the employee belongs to (display / validation); leave blank when `applicable_for=Company` |
| holiday_list | Holiday List | Link→Holiday List | Y | Haritha Hospitals Holiday List | must exist | the calendar being assigned |
| from_date | From Date | Date | Y | 2025-01-01 | YYYY-MM-DD | effective start date; the resolver uses the most-recent-from_date assignment on or before today |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Holiday List Assignment", ...}` before constructing the document.
- **Gotcha #HLA-1 — `docstatus=1` REQUIRED for resolver visibility (Sept 21 audit finding):** The HRMS resolver that determines which Holiday List applies to a given employee filters on `docstatus=1`. Records imported via `frappe.get_doc().insert()` are saved at `docstatus=0` (Draft) and are therefore **invisible** to the resolver. **After import, every Holiday List Assignment must be submitted** — either via the web UI list view (`Actions → Submit`) or programmatically via `frappe.db.submit("Holiday List Assignment", name)`. A Stream 3B bulk-import on Sept 17 left 210 rows in Draft state and the resolver returned zero assignments until each was manually submitted.
- **Gotcha #HLA-2 — Dynamic Link + Select pairing:** `assigned_to` is a Dynamic Link — its target DocType is governed by the value of `applicable_for`. Picking `applicable_for=Employee` requires `assigned_to` to be a valid Employee ID; picking `applicable_for=Company` requires it to be a valid Company name. The Data Import tool does NOT validate this pairing automatically — verify manually before submit.
- **Gotcha #HLA-3 — `from_date` is the effective start, not the holiday-list start:** `from_date` is when this assignment becomes effective, NOT the calendar window of the Holiday List itself. For example, an employee joining mid-year gets a Holiday List Assignment with `from_date=2025-06-15` even though the Holiday List covers `2025-01-01` to `2025-12-31`.
- **Gotcha #HLA-4 — most-recent-from_date wins:** The resolver returns the assignment with the largest `from_date` that is `<= today` for the (Employee or Company) target. Two assignments for the same employee on overlapping `from_date` windows will produce undefined behavior — design assignments in chronological order.
- **Gotcha #HLA-5 — autoname is system-generated:** Holiday List Assignment uses the default Frappe autoname (hash-based). Do not supply a `name` column in the CSV — let Frappe generate it.
- Holiday List Assignment has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.
- Production patterns: typically 1 Company-wide Holiday List Assignment + per-employee overrides for transfers / site changes.

## Healthcare-specific fields

None. Holiday List Assignment has no custom fields in the `haritha_hospital` custom app.

## When to use this sheet

| Scenario | Use Holiday List Assignment template? |
|---|---|
| Assigning a Holiday List company-wide | YES — populate one row with `applicable_for=Company`, `assigned_to=<Company name>` |
| Assigning a Holiday List to a single employee | YES — populate one row with `applicable_for=Employee`, `assigned_to=<Employee ID>` |
| Changing an employee's Holiday List mid-year | YES — append a new row with the new `holiday_list` and the effective `from_date` |
| Just updating the holiday list (not per-employee) | NO — edit the Holiday List record directly via web UI |
| Bulk holiday calendar rollout | YES — one row per (Company or Employee × Holiday List) |

## Common client mistakes

- **Importing via `insert()` and forgetting to submit — RESOLVER INVISIBLE.** This is the #1 issue from the Sept 21 audit. After import, every row MUST be at `docstatus=1`.
- Setting `applicable_for=Employee` and `assigned_to=Haritha Hospitals` (a Company name) — fails Dynamic Link validation on submit.
- Setting `applicable_for=Company` and `assigned_to=HR-EMP-00421` (an Employee ID) — fails Dynamic Link validation on submit.
- Leaving `from_date` blank — required field.
- Linking to a Holiday List that does not exist — fails LinkValidationError. Import Holiday List records first.
- Creating two assignments for the same Employee with overlapping `from_date` windows — resolver picks one but the other becomes dead-weight. Use the latest-effective-date pattern instead.
- Setting `from_date` in the future for a new-hire transfer — assignment will not take effect until that date. Use today's date for immediate effect.

## Related

- **Holiday List** template (`06_holiday_list.csv`) — must import first; `holiday_list` Link resolves here.
- **Employee** template's `holiday_list` Link — acts as the fallback when no Holiday List Assignment matches.
- **Company** is configured directly in ERPNext before workbook.
- After import, run a submission batch (web UI or script) to flip all rows to `docstatus=1`.
