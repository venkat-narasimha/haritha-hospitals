# Employee Separation Template — Intake Sheet

**DocType:** Employee Separation Template (not submittable)
**Module:** HR / Separation
**Required fields:** 2 (parent: `title`, `company`) + 1 (child: `step_name`)
**Optional fields:** 1 (parent: `department`) + 3 (child: `step_number`, `description`, `required`)

An Employee Separation Template defines a reusable separation / exit checklist (sequence of activities). Each `Employee Separation` (a separate DocType created when an employee leaves) references one of these templates to pre-populate its `activities` child table. Common default activities include **Exit Interview**, **Knowledge Handover**, and **IT Asset Return**, but templates may have any number of custom steps.

> **Import flow:** This CSV imports the **parent** Separation Template record. The child `employee_separation_steps` rows are supplied inline as repeated rows in the same CSV (Frappe Data Import deduplicates parent columns on repeated values). The child rows are documented in the table below.

## Field reference (parent — Employee Separation Template)

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| title | Title | Data | Y | Test Separation Template | unique | autoname=field:title |
| company | Company | Link→Company | Y | Haritha Hospitals | must exist | required Link; typically set to Haritha Hospitals at single-site deployments |
| department | Department | Link→Department | N | X - HH | must exist if set | optional scope-restriction; blank = template applies to all departments under the Company |

## Child table: Employee Separation Step (inline row pattern)

The `employee_separation_steps` child table lists separation activities in execution order. For the recommended 3-activity default (Exit Interview / Knowledge Handover / IT Asset Return), populate three child rows under one parent row.

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| step_name | Step Name | Data | Y | Exit Interview | non-empty | activity title; displayed in separation checklist |
| step_number | Step Number | Int | N | 1 | >= 1 | execution order; lower numbers run first; blank rows sort last |
| description | Description | Text | N | Schedule exit interview with HR | free text | detailed instructions for the activity owner |
| required | Required | Check | N | 1 | 0/1 | 1 blocks separation completion until the step is checked off; 0 = optional |

> **Tip:** To populate multiple child rows under one parent, repeat the parent columns (`title`, `company`, `department`) across multiple CSV rows and vary only the child columns. Frappe Data Import deduplicates parent columns automatically.

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Employee Separation Template", ...}` before constructing the document.
- **Gotcha #ST-1 — autoname is the literal title:** Employee Separation Template uses `autoname=field:title`, so the title you type becomes the primary key. Two rows with the same `title` value will fail `DuplicateEntryError`.
- **Gotcha #ST-2 — Company must exist:** The `company` field is a Link→Company. Linking to a Company that does not exist fails `LinkValidationError`. Import Company records first (typically configured directly in ERPNext before workbook).
- **Gotcha #ST-3 — Department scoping is optional:** Leaving `department` blank makes the template available to all Departments under the Company. Setting it scopes the template to that specific Department in the Separation wizard dropdown.
- **Gotcha #ST-4 — child rows via web UI fallback:** If the multi-row CSV pattern is rejected by your Data Import tool, populate the `employee_separation_steps` child table via the Frappe web UI on each imported parent record.
- **Gotcha #ST-5 — mirror of Onboarding Template structure:** Separation Template shares its autoname / child-table pattern with Onboarding Template; reuse the import strategy.
- Employee Separation Template has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.
- Production patterns: typically 1-2 templates per Company (e.g. "Clinical Staff Separation", "Admin Staff Separation"); 3-8 steps per template.

## Healthcare-specific fields

None. Employee Separation Template has no custom fields in the `haritha_hospital` custom app.

## When to use this sheet

| Scenario | Use Separation Template? |
|---|---|
| Standardize exit checklists across the hospital | YES — populate one row per template (clinical/admin/etc.) |
| Adding a new department-specific separation flow | YES — append a new parent row, set `department` |
| Tracking per-employee separation progress | NO — that lives on the `Employee Separation` DocType (created per exit, not via workbook) |
| Tracking final settlement or leave encashment | NO — handled via Payroll / Leave Encashment, not via this template |

## Common client mistakes

- Setting `title` to a value that collides with an existing template — fails `DuplicateEntryError`. Use department-coded names if unsure.
- Forgetting child steps — parent imports but the Separation wizard shows an empty checklist.
- Setting `step_number` to floats (e.g. `1.5`) — Int field rejects non-integers.
- Marking `Knowledge Handover` or `IT Asset Return` as `required = 0` — these typically must complete before final settlement is processed.
- Setting `department` to a department that does not exist — fails `LinkValidationError`.
- Treating this as a settlement / payout record — wrong DocType. Separation Template is the activity checklist only.

## Related

- **Employee Separation** DocType (per-exit instance; not in this workbook) references a Separation Template and copies its steps into its `activities` child table.
- **Employee Onboarding Template** template (`22_onboarding_template.csv`) shares the structure (mirror patterns).
- **Department** template (must exist before scoping `department`).
- **Company** is configured directly in ERPNext before workbook.
