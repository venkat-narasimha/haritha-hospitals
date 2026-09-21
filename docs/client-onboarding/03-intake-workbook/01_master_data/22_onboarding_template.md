# Employee Onboarding Template — Intake Sheet

**DocType:** Employee Onboarding Template (not submittable)
**Module:** HR / Onboarding
**Required fields:** 2 (parent: `title`, `company`) + 1 (child: `step_name`)
**Optional fields:** 1 (parent: `department`) + 3 (child: `step_number`, `description`, `required`)

An Employee Onboarding Template defines a reusable onboarding checklist (sequence of activities). Each `Employee Onboarding` (a separate DocType created when an employee joins) references one of these templates to pre-populate its `activities` child table. Common default activities include **Welcome**, **IT Setup**, and **HR Orientation**, but templates may have any number of custom steps.

> **Import flow:** This CSV imports the **parent** Onboarding Template record. The child `employee_onboarding_steps` rows are supplied inline as repeated rows in the same CSV (Frappe Data Import deduplicates parent columns on repeated values). The child rows are documented in the table below.

## Field reference (parent — Employee Onboarding Template)

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| title | Title | Data | Y | Test Onboarding Template | unique | autoname=field:title |
| company | Company | Link→Company | Y | Haritha Hospitals | must exist | required Link; typically set to Haritha Hospitals at single-site deployments |
| department | Department | Link→Department | N | X - HH | must exist if set | optional scope-restriction; blank = template applies to all departments under the Company |
| intro | Introduction | Text Editor | N |  | free text | optional introduction text shown on the Onboarding record |

## Child table: Employee Onboarding Step (inline row pattern)

The `employee_onboarding_steps` child table lists onboarding activities in execution order. For the recommended 3-activity default (Welcome / IT Setup / HR Orientation), populate three child rows under one parent row.

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| step_name | Step Name | Data | Y | Welcome | non-empty | activity title; displayed in onboarding checklist |
| step_number | Step Number | Int | N | 1 | >= 1 | execution order; lower numbers run first; blank rows sort last |
| description | Description | Text | N | Welcome email + first-day orientation | free text | detailed instructions for the activity owner |
| required | Required | Check | N | 1 | 0/1 | 1 blocks onboarding completion until the step is checked off; 0 = optional |

> **Tip:** To populate multiple child rows under one parent, repeat the parent columns (`title`, `company`, `department`) across multiple CSV rows and vary only the child columns. Frappe Data Import deduplicates parent columns automatically.

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Employee Onboarding Template", ...}` before constructing the document.
- **Gotcha #OT-1 — autoname is the literal title:** Employee Onboarding Template uses `autoname=field:title`, so the title you type becomes the primary key. Two rows with the same `title` value will fail `DuplicateEntryError`.
- **Gotcha #OT-2 — Company must exist:** The `company` field is a Link→Company. Linking to a Company that does not exist fails `LinkValidationError`. Import Company records first (typically configured directly in ERPNext before workbook).
- **Gotcha #OT-3 — Department scoping is optional:** Leaving `department` blank makes the template available to all Departments under the Company. Setting it scopes the template to that specific Department in the Onboarding wizard dropdown.
- **Gotcha #OT-4 — child rows via web UI fallback:** If the multi-row CSV pattern is rejected by your Data Import tool, populate the `employee_onboarding_steps` child table via the Frappe web UI on each imported parent record.
- Employee Onboarding Template has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.
- Production patterns: typically 1-2 templates per Company (e.g. "Clinical Staff Onboarding", "Admin Staff Onboarding"); 3-8 steps per template.

## Healthcare-specific fields

None. Employee Onboarding Template has no custom fields in the `haritha_hospital` custom app.

## When to use this sheet

| Scenario | Use Onboarding Template? |
|---|---|
| Standardize onboarding checklists across the hospital | YES — populate one row per template (clinical/admin/etc.) |
| Adding a new department-specific onboarding flow | YES — append a new parent row, set `department` |
| Tracking per-employee onboarding progress | NO — that lives on the `Employee Onboarding` DocType (created per hire, not via workbook) |
| Single-step ad-hoc onboarding | NO — skip the template; create the Employee Onboarding record directly via web UI |

## Common client mistakes

- Setting `title` to a value that collides with an existing template — fails `DuplicateEntryError`. Use department-coded names (e.g. `Clinical Onboarding - HH`) if unsure.
- Forgetting child steps — parent imports but the Onboarding wizard shows an empty checklist.
- Setting `step_number` to floats (e.g. `1.5`) — Int field rejects non-integers.
- Marking every step as `required = 0` — defeats the purpose of the template. At least Welcome and HR Orientation should be required.
- Setting `department` to a department that does not exist — fails `LinkValidationError`.
- Trying to populate per-employee onboarding progress here — wrong DocType. Use Employee Onboarding (separate, per-hire record).

## Related

- **Employee Onboarding** DocType (per-hire instance; not in this workbook) references an Onboarding Template and copies its steps into its `activities` child table.
- **Department** template (must exist before scoping `department`).
- **Company** is configured directly in ERPNext before workbook.
