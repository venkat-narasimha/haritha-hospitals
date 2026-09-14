# Department — Intake Sheet

**DocType:** `Department`
**Module:** HR
**Required fields:** 2
**Optional fields:** 5+ (varies with custom fields)

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `department_name` | Department Name | Data | Y | "Cardiology" | unique within company | The visible name |
| `company` | Company | Link → Company | Y | "ABC Healthcare Pvt Ltd" | must exist | Multi-company possible |
| `parent_department` | Parent Department | Link → Department | N | "Clinical Services" | must exist if set | Use `is_group=1` for parents |
| `is_group` | Is Group | Check | N | 0 | 0/1 | Tree-structure flag |
| `leave_block_list` | Leave Block List | Link → Leave Block List | N | "" | must exist if set | Block leave during critical periods |
| `leave_approvers` | Leave Approvers | Table | N | (see below) | child: approver (User) | Per-department approver chain |
| `expense_approvers` | Expense Approvers | Table | N | (see below) | child: approver (User) | Per-department expense approver |
| `shift_request_approvers` | Shift Request Approvers | Table | N | (see below) | child: approver (User) | Per-department shift approver |

## Healthcare-specific fields (custom — add via Customize Form first)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `department_code` | Department Code | Data | N | "CARD" | Short code for reports/badges (≤6 chars) |
| `building` | Building / Wing | Data | N | "Main Block - 2nd Floor" | For geofencing + signage |
| `hod` | Head of Department | Link → Employee | N | "Dr. Sharma" | Used for approval workflows |
| `nabl_accredited` | NABL Accredited | Check | N | 0 | For Lab departments |
| `nabh_accredited` | NABH Accredited | Check | N | 0 | For quality reporting |

## Validation rules

- `department_name` is unique within a Company.
- If `parent_department` is set, `is_group` on parent must be 1.
- `leave_approvers` user must have a role that allows leave approval.

## Common client mistakes

- Using the same `department_name` across different Companies — should be unique.
- Setting `is_group=1` on leaf departments — they should be `0`.
- Not creating parent departments first before child departments.
- Missing `leave_approvers` — leads to leave applications failing to route.

## Typical hospital departments to import

- Clinical: ICU, NICU, PICU, Casualty/ER, OT, Wards (General/Semi-Private/Private), OPD, Cardiology, Neurology, Orthopaedics, Paediatrics, Gynaecology, ENT, Dermatology, Ophthalmology, Dental
- Diagnostics: Pharmacy, Lab (Pathology/Microbiology/Biochemistry), Radiology (X-Ray/CT/MRI)
- Support: Admin, HR, Finance, IT, Housekeeping, Security, Maintenance, Dietary, Medical Records
- Tree roots: Clinical Services (group), Diagnostics (group), Support Services (group)

## Migration notes (see `scripts/migrate_master_data.py`)

- **Skip root rows.** Rows with `parent_department = "All Departments"` are SKIPPED by the migration script — that root is auto-created by Frappe on app install and the script cannot re-insert it (GOTCHA #5). Leave the root out of your CSV.
- **Department Approver pre-seed (GOTCHA #10).** Before inserting any `Shift Request`, the migration script calls `_ensure_department_approvers()` which adds a `Department Approver` child row with `approver="Administrator"` and `parentfield="shift_request_approver"` for every department referenced by the source SR JSON. If your client does NOT want `Administrator` as the default approver, populate the `shift_request_approvers` table here in this intake sheet so real approvers win on re-import.
- **Upsert semantics.** The migration script upserts by `name`. Re-running it UPDATES existing department rows (does not duplicate). Custom fields (`department_code`, `building`, `hod`) are overwritten on each re-run, so back up edits you want to preserve.
- **Order matters.** `Department` is migrated BEFORE `Designation`, `Employee Grade`, `Branch`, `Shift Type`, `Shift Location`, `Holiday List`, `Employee`, `Item` — any of those that reference a department will fail with `LinkValidationError` if department is not yet present.
