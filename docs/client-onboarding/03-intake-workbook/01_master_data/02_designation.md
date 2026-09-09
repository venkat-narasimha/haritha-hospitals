# Designation — Intake Sheet

**DocType:** `Designation`
**Module:** HR
**Required fields:** 1
**Optional fields:** 3

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|
| `designation_name` | Designation Name | Data | Y | "Senior Consultant" | unique | The job title |
| `description` | Description | Text | N | "Senior clinical role" | – | Optional free text |
| `required_skills` | Required Skills | Table → Employee Skill | N | (rows) | child: skill | Feeds Employee Skill Map |
| `appraisal_template` | Appraisal Template | Link → Appraisal Template | N | "" | must exist if set | For performance reviews |

## Healthcare-specific fields (custom)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `clinical_role` | Clinical Role | Select | N | "Doctor" | Doctor / Nurse / Technician / Support / Admin |
| `requires_registration` | Requires Medical Registration | Check | N | 1 | For roles needing NMC/state council reg |
| `min_qualification` | Minimum Qualification | Data | N | "MBBS, MD" | Used for job posting + filtering |

## Validation rules

- `designation_name` is unique across the system.
- `clinical_role` (if added as custom) drives Employee custom-field validation (e.g., forces `medical_council_reg_no` if `requires_registration=1`).

## Common client mistakes

- Spelling inconsistencies ("Senior Consultant" vs "Sr Consultant") — ERPNext treats them as different.
- Mixing clinical and non-clinical designations in the same sheet — keep them separate or use `clinical_role` field to differentiate.
- Creating one designation per person — Designation is a *role*, not a person.

## Typical hospital designations to import

- **Medical:** Medical Director, HOD, Senior Consultant, Consultant, Junior Consultant, Registrar, Senior Resident (SR), Junior Resident (JR), Intern, Medical Officer
- **Nursing:** Chief Nursing Officer, Nursing Superintendent, Nurse In-charge, Staff Nurse, ANM, Nursing Assistant
- **Allied Health:** Pharmacist, Lab Technician, Radiology Technician, OT Technician, Dialysis Technician
- **Support:** Receptionist, Housekeeping Supervisor, Security Supervisor, Maintenance Technician, Dietary Supervisor
- **Admin:** Admin Manager, HR Executive, Finance Officer, IT Administrator, Medical Records Officer
