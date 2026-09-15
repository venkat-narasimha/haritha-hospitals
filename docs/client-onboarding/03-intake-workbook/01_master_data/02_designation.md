# Designation — Intake Sheet

**DocType:** `Designation` (master)
**Module:** HR / Setup
**Autoname rule:** `field:designation_name`

**Required fields:** 1  |  **Optional fields:** 3

## Purpose

Job titles / roles within the Company. Designations are linked from Employee.designation and drive approval limits + salary bands.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `designation_name` | Designation Name | Data | **Y** | `Designation A` | unique within company |  |
| `description` | Description | Text | **N** | `Role description here` | free-form text |  |
| `appraisal_template` | Appraisal Template | Link→Appraisal Template | **N** | `` | must exist in tabAppraisal Template |  |
| `skills` | Skills | Table→Designation Skill | **N** | `` | child rows |  |

## Healthcare-specific extensions (optional, India-context)

- If client uses clinical role categorization, the custom `skills` table child rows let you attach required skills (e.g., 'BLS Certified', 'ACLS Certified') per designation.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment — define all job titles | Yes — bulk import |
| New hire cohort adds a new role | Yes — single-row insert |

## Common client mistakes

- Creating too many designations (50+) — keep the list tight (real job families).
- Title-casing inconsistencies (e.g., 'staff nurse' vs 'Staff Nurse') — Frappe compares names case-sensitively on Linux MariaDB.
