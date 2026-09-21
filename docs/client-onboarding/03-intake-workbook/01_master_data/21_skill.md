# Skill — Intake Sheet

**DocType:** Skill (not submittable)
**Module:** HR / Skill Management
**Required fields:** 1
**Optional fields:** 1

Skill is the master list of skills available at the company (e.g. Phlebotomy, IV Cannulation, ACLS, BLS, Triage, Patient Counseling). Each skill is referenced by **Employee Skill Map** (a per-employee proficiency record) and optionally by **Designation Skill** (a per-designation skill requirement). This sheet governs the master only — proficiency ratings and designation-skill matrices are tracked elsewhere.

> **Important:** This template governs the **skill catalogue only**. Per-employee skill mastery (Employee Skill Map) and per-designation skill requirements (Designation Skill child table) are populated via the Frappe web UI, not via Data Import. See the "Healthcare-specific fields" subsection below.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| skill_name | Skill Name | Data | Y | Test Skill 1 | unique | autoname=field:skill_name |
| description | Description | Text | N | Skill for testing | <= 500 chars | free-text note |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Skill", ...}` before constructing the document.
- **Gotcha #SK-1 — master only:** Skill is a flat master. Do not attempt to populate per-employee ratings here — those belong on the Employee Skill Map DocType, populated via web UI.
- Skill has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.
- Import is unconditional — no FK dependencies. Safe to import in any order, but recommended **before** Employee Skill Map so the Link resolves.

## Healthcare-specific fields

None. Skill has no custom fields in the `haritha_hospital` custom app.

The `Designation` DocType has a `skills` child table (Documented in `02_designation.md`) that Links to Skill via `skill` (Link→Skill). Populate that child table via the Frappe web UI after importing both Designation and Skill records.

## When to use this sheet

| Scenario | Use Skill template? |
|---|---|
| New hospital onboarding with a defined clinical-skill matrix | YES — populate one row per skill in the matrix |
| Adding a new skill discovered post-launch | YES — append a new row |
| Per-employee skill ratings | NO — use Employee Skill Map via web UI |
| Per-designation skill requirements | NO — populate Designation `skills` child table via web UI |

## Common client mistakes

- Typing skill names inconsistently (`BLS` vs `Basic Life Support`) — breaks Designation Skill and Employee Skill Map joins. Standardize capitalization and abbreviations.
- Setting `description` to 1000+ chars when the field is `<= 500`. Truncate before import.
- Trying to populate proficiency levels here — Skill has no rating field. Use Employee Skill Map.
- Treating Skill as a sub-tag of Department — wrong DocType. Department is org structure; Skill is capability catalogue.

## Related

- **Designation** template has a `skills` child table that Links to Skill (web UI population).
- **Employee Skill Map** (separate DocType, not in this workbook) tracks per-employee proficiency ratings.
- See `02_designation.md` for parallel structure.
