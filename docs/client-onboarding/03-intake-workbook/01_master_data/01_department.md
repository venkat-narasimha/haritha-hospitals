# Department — Intake Sheet

**DocType:** Department (not submittable)
**Module:** HR / Organization
**Required fields:** 2
**Optional fields:** 5+

Departments represent the org chart. Every employee belongs to one Department, and Departments roll up to a Company (set once globally). Departments may also nest into a parent Department for sub-units (e.g. Clinical Services → Cardiology, Pediatrics).

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| department_name | Department | Data | Y | Department A | unique per company | autoname=field:department_name; bare name OK (Frappe appends " - <abbr>" on save - see gotcha #11) |
| parent_department | Parent Department | Link→Department | N | Department A | must exist if set | use for nested hierarchy; leave blank for top-level |
| company | Company | Link→Company | Y | Company A | must exist | Company is configured in ERPNext before workbook |
| is_group | Is Group | Check | N | 0 | 0/1 | set 1 only for group/parent rows (do not import employees under group) |
| disabled | Disabled | Check | N | 0 | 0/1 | soft-disable flag |
| payroll_cost_center | Payroll Cost Center | Link→Cost Center | N |  | must exist if set | custom field; link to Cost Center for payroll postings |
| leave_block_list | Leave Block List | Link→Leave Block List | N |  | must exist if set | custom field; optional block-list reference |

## Migration notes (from research §7)

- **Gotcha #5 — Department root trap:** Frappe auto-creates an `All Departments` root. Trying to import a row with `parent_department="All Departments"` raises `ParentNotFoundError`. **Always leave `parent_department` blank for top-level departments.** Nested children should reference a real sibling imported earlier in the same CSV.
- **Gotcha #11 — name auto-suffix:** When a Department is saved under a Company, Frappe automatically appends ` - <company-abbr>` to `department_name` (e.g. `Nursing` becomes `Nursing - HH`). Clients should enter the **bare name** (e.g. `Nursing`); Frappe normalizes on import. Do NOT type the suffix manually — duplicate-detection will fail.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Department", ...}` before constructing the document. Affects all 22 P5 templates.
- **Gotcha #10a — Department Approver pre-seed:** If you later import Shift Requests that link back to these Departments, the `_ensure_department_approvers()` helper seeds `approver='Administrator'` into the `shift_request_approver` child table after migration. No action needed for Department import itself.

## Healthcare-specific fields

The `haritha_hospital` custom app adds 8 custom fields to `Department`. The two most useful for hospital clients are:

| fieldname | label | type | when to use |
|---|---|---|---|
| `payroll_cost_center` | Payroll Cost Center | Link→Cost Center | set if this department has its own payroll Cost Center for expense allocation |
| `leave_block_list` | Leave Block List | Link→Leave Block List | set if this department has restricted leave-block dates |

The other 5 (`approvers`, `column_break_9`, `section_break_4`, `shift_request_approver`, `expense_approvers`) are layout/child-table fields and are populated via the Frappe web UI, not Data Import. The `leave_approvers` child table is documented below.

## Leave Approvers (child table) — HRMS v16

> **HRMS v16 gap** (Sep 17–21 audit, Item 6): Per-Department approver inheritance was missing from earlier intake. Without populating this child table, Leave Application approval cannot resolve a Department approver, and any employee whose HR Settings has `leave_approver_mandatory_in_leave_application=1` will fail `Leave Application.submit()`.

The `leave_approvers` child table is attached to each Department and stores one or more User records who can approve Leave Applications from anyone in that Department (or any nested child Department).

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| approver | Approver | Link→User | Y | `Administrator` | User must exist | **Schema field is `approver`, NOT `leave_approver`** — Sep 18 schema gotcha; the Stream 3 brief used the wrong field name |
| role | Role | (n/a) | — | — | — | No `role` field exists in the HRMS v16 schema. Single-level approver only; multi-level (primary / secondary) requires a custom script. |

### Behaviour

- **Per-Department scope:** `leave_approvers` rows on a Department apply to all employees whose `Employee.department` resolves to that Department (including nested child Departments).
- **Inheritance:** Child Departments inherit approvers from their parent if they have no rows of their own.
- **Required when:** HR Settings → `leave_approver_mandatory_in_leave_application` is **1** (default in HRMS v16). If set, `Leave Application.submit()` raises a validation error when no approver resolves.
- **Workbook dependency:** This template pairs with [`02_settings_checklists/01_hr_settings.md`](../02_settings_checklists/01_hr_settings.md) — set `leave_approver_mandatory_in_leave_application` and the **Workflow for Leave Application** together with this child table.

### Example

| Department | approver (User) | Result |
|---|---|---|
| `Department X - HH` | `Administrator` | Any employee in `Department X - HH` (or its children) routes leave to `Administrator` |
| `Nursing - HH` | `nurse.manager@hospital.example` | Nursing staff leave routes to the nurse manager |

### How to populate

- **Not via this CSV.** Child tables cannot be Data-Imported through the master-data CSV format. They must be set via the Frappe web UI: open the Department record → expand **Leave Approvers** → add row → set **Approver** to a User.
- **Or programmatically** via the partner's migration script: `frappe.get_doc({"doctype":"Department","name":dept,"leave_approvers":[{"approver":"Administrator"}]}).save()`. The seed helper `_ensure_department_approvers()` (used for Shift Requests — see `migration/`) can be extended for Leave Approvers.
- **Bulk seeding tip:** For hospital onboarding, seed `Administrator` as the Department approver for every Department, then have HR replace per-Department after go-live via the web UI.

## When to use this sheet

| Scenario | Use Department template? |
|---|---|
| Onboarding a new hospital client with 20+ departments | YES — populate one row per department |
| Adding new departments to an existing deployment | YES — append rows to current CSV and re-import |
| Single-site deployment (1 department) | YES — but only 1 row is required |
| Multi-company deployment | YES — set `company` per row |

## Common client mistakes

- Typing the company abbreviation into `department_name` (e.g. `Nursing - HH` instead of `Nursing`). Frappe will then append again, producing `Nursing - HH - HH`. **Use the bare name.**
- Setting `parent_department = "All Departments"` — fails with `ParentNotFoundError`. Leave blank for top-level rows.
- Setting `is_group = 1` and then trying to import employees under it — `is_group` rows are container-only, they cannot have child records directly.
- Leaving `company` blank — fails with `LinkValidationError`. Company is required even though it appears as a single global value at single-site deployments.

## Related

- **Company** is configured in ERPNext directly (not via workbook).
- **Employee** template uses `department` as a Link.
- **Shift Assignment** template uses `department` as an optional Link (auto-derived from Employee in most cases).
- See `08_shift_location.csv` if you need geofenced departments (rare; usually site-level only).
