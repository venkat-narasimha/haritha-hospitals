# Designation — Intake Sheet

**DocType:** Designation (not submittable)
**Module:** HR / Organization
**Required fields:** 1
**Optional fields:** 2+

Designations are job titles (e.g. Nurse, Technician, Manager). Every Employee references one Designation via Link. Designations are independent — they do not roll up to a parent, and they do not require a Company.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| designation_name | Designation | Data | Y | Designation A | unique | autoname=field:designation_name |
| description | Description | Text | N | Sample role description | <= 500 chars | free text |
| appraisal_template | Appraisal Template | Link | N |  | must exist if set | custom field; optional template link |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Designation", ...}` before constructing the document.
- Designation import is unconditional — no FK dependencies on other masters. Safe to import in any order.
- All 78 custom fields are stored in `haritha_hospital/fixtures/custom_field.json`. Once the app is installed, the `appraisal_template` Link is visible and importable.

## Healthcare-specific fields

The `haritha_hospital` custom app adds 3 custom fields to `Designation`:

| fieldname | label | type | when to use |
|---|---|---|---|
| `appraisal_template` | Appraisal Template | Link→Appraisal Template | set if this designation has a dedicated appraisal template |
| `required_skills_section` | Required Skills | Section Break | layout only (no data) |
| `skills` | Skills | Table→Designation Skill | populate via web UI for skill-matrix reports |

The `skills` child table is best populated via the Frappe web UI after import — Data Import does not handle nested child tables cleanly.

## When to use this sheet

| Scenario | Use Designation template? |
|---|---|
| Onboarding a new hospital client with 20+ titles | YES — populate one row per title |
| Adding new titles to an existing deployment | YES — append rows and re-import |
| Single-titled organization | YES — but only 1 row is required |
| Adding skills matrix data | NO — populate `Designation Skill` child via UI |

## Common client mistakes

- Putting "Senior" / "Junior" prefix into the name inconsistently (`Sr. Nurse` vs `Senior Nurse`) — design Data Import with the canonical title.
- Setting `description` to 1000+ chars when the field is `<= 500`. Truncate before import.
- Trying to set `skills` as a column in the CSV — child tables are not flat-importable. Use the web UI.
- Linking to an `Appraisal Template` that does not exist — fails with `LinkValidationError`. Import Appraisal Templates first.

## Related

- **Employee** template uses `designation` as a Link (highly recommended — leave blank only for very early joiners).
- See `01_department.csv` for org-chart context.
