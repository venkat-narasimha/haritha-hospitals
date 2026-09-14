# Employee — Intake Sheet

**DocType:** `Employee`
**Module:** HR
**Required fields:** 5–6 (depends on HR Settings naming rule)
**Optional fields:** 30+ (varies with custom fields)

## Field reference (standard)

### Identity

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `first_name` | First Name | Data | Y* | "Aarav" | non-empty | *Required if HR Settings naming=First/Middle/Last |
| `middle_name` | Middle Name | Data | N | "Kumar" | – | optional |
| `last_name` | Last Name | Data | N* | "Sharma" | – | *Required only if naming=First+Last |
| `employee_name` | Employee Name | Data | Y | "Aarav Kumar Sharma" | non-empty | Auto-derived but required for import |
| `employee_number` | Employee Number | Data | Y* | "HRH-EMP-0001" | unique | *Required only if HR Settings → Employee Number naming |
| `gender` | Gender | Select | Y | "Male" | Male/Female/Other | – |
| `date_of_birth` | Date of Birth | Date | Y | "1990-05-12" | YYYY-MM-DD, ≤today | – |
| `date_of_joining` | Date of Joining | Date | Y | "2024-01-15" | YYYY-MM-DD | – |
| `employment_type` | Employment Type | Link → Employment Type | N | "Full-time" | must exist | – |
| `status` | Status | Select | Y | "Active" | Active/Suspended/Left/Permanently Disabled | Default: Active |

### Organisation

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `company` | Company | Link → Company | Y | "ABC Healthcare Pvt Ltd" | must exist | – |
| `department` | Department | Link → Department | N | "Cardiology" | must exist | – |
| `designation` | Designation | Link → Designation | N | "Senior Consultant" | must exist | – |
| `branch` | Branch | Link → Branch | N | "Main Hospital" | must exist | – |
| `grade` | Grade | Link → Employee Grade | N | "A2" | must exist | Drives salary band |
| `reports_to` | Reports To | Link → Employee | N | "EMP-0001" | must exist if set | For org chart |
| `leave_approver` | Leave Approver | Link → User | N | "hr.manager@hosp.com" | must exist if set | Defaults to department approver |
| `expense_approver` | Expense Approver | Link → User | N | "hr.manager@hosp.com" | must exist if set | – |
| `shift_request_approver` | Shift Request Approver | Link → User | N | "hod.cardiology@hosp.com" | must exist if set | Defaults to department approver |

### Attendance

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `default_shift` | Default Shift | Link → Shift Type | N | "Morning-8h" | must exist | Fallback when no Shift Assignment |
| `attendance_device_id` | Attendance Device ID (Biometric) | Data | N | "BIO-12345" | unique if set | Links to Employee Checkin |
| `holiday_list` | Holiday List | Link → Holiday List | N | "State A Holiday Calendar 2026" | must exist | Defaults from Company |

### Contact

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `cell_number` | Cell Number | Data | N | "+91-9876543210" | – | – |
| `personal_email` | Personal Email | Data | N | "aarav@gmail.com" | valid email | One of personal_email/company_email required for User creation |
| `company_email` | Company Email | Data | N | "aarav@hosp.com" | valid email | One of personal_email/company_email required for User creation |
| `preferred_contact_email` | Preferred Contact Email | Select | N | "Company Email" | Company Email / Personal Email | – |
| `current_address` | Current Address | Text | N | "Flat 101, MG Road" | – | – |
| `permanent_address` | Permanent Address | Text | N | "Same as current" | – | – |

### Personal

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `blood_group` | Blood Group | Select | N | "B+" | A+/A-/B+/B-/AB+/AB-/O+/O- | Required for hospital staff (statutory) |
| `marital_status` | Marital Status | Select | N | "Married" | Single/Married/Divorced/Widowed | – |
| `passport_number` | Passport Number | Data | N | "P1234567" | – | – |
| `place_of_issue` | Place of Issue | Data | N | "City A" | – | – |
| `allergies` | Allergies | Small Text | N | "Penicillin" | – | – |
| `medical_concerns` | Medical Concerns | Small Text | N | "" | – | – |

### Education (child table)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `school` | School/University | Data | N | "AIIMS" | – |
| `qualification` | Qualification | Link → Qualification | N | "MBBS" | – |
| `year_of_passing` | Year of Passing | Int | N | 2015 | 4-digit year |
| `class_per` | Class / Percentage | Data | N | "First Class" | – |

## Healthcare-specific fields (custom — REQUIRED for hospital context)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `medical_council_reg_no` | Medical Council Reg. No. | Data | Y* | "REG-A-0001" | *Required for all doctors (NMC/state council) |
| `reg_council` | Registration Council | Link | N | "State Medical Council" | NMC / State council |
| `reg_validity_date` | Registration Validity | Date | N | "2027-12-31" | License expiry |
| `specialization` | Specialization | Data | N | "Cardiology" | Free text or Link if master exists |
| `police_verification_date` | Police Verification Date | Date | N | "2024-06-15" | Mandatory for some hospitals |
| `health_checkup_due_date` | Health Checkup Due Date | Date | N | "2026-12-31" | Annual staff health check |
| `next_of_kin` | Next of Kin | Data | N | "Sunita Sharma (Spouse)" | – |
| `role_in_department` | Role in Department | Select | N | "Member" | Member / HOD / I/C / Senior / Junior |

## Emergency contact (custom — recommended)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `emergency_contact_name` | Emergency Contact Name | Data | Y | "Sunita Sharma" | Required for clinical staff |
| `emergency_phone_number` | Emergency Phone | Data | Y | "+91-9876543211" | Required for clinical staff |
| `emergency_contact_relation` | Relation | Select | N | "Spouse" | Spouse/Parent/Sibling/Child/Friend |

## Validation rules

- `company_email` OR `personal_email` is mandatory for auto-creating a User account.
- `employee_number` unique across the system (if naming=Employee Number).
- `medical_council_reg_no` (if added as custom) should be enforced `reqd=1` for any Employee with `designation` containing "Doctor" / "Consultant" / "Resident" — enforce via Client Script on Employee.
- `blood_group` should be `reqd=1` for all clinical staff (nurse, doctor, technician) — enforce via Client Script.
- `emergency_contact_name` and `emergency_phone_number` should be `reqd=1` for clinical staff.
- `date_of_birth ≤ date_of_joining`.

## Common client mistakes

- Forgetting to set `status` — all employees default to "Active", which is correct but should be explicit.
- Leaving `attendance_device_id` blank — biometric punches don't link to Employee.
- Using personal email as `company_email` — security risk; use official hospital email.
- Inconsistent `employee_number` formats (HR-001 vs HRH-001 vs HRH-EMP-001) — pick one and stick.
- Forgetting to populate `blood_group` and `medical_council_reg_no` for clinical staff — caught in UAT.
- Missing `holiday_list` on Employee — falls back to Company default; verify Company default is set correctly.

## Import order reminder

Import Department, Designation, Employment Type, Employee Grade, Branch, Shift Type, Shift Location, Holiday List BEFORE Employee — these are all Link fields on Employee.

## Typical hospital employee categories

- Medical staff (consultants, residents, interns) — require medical_council_reg_no
- Nursing staff (CNO, supervisors, staff nurses, ANM) — require blood_group, emergency contact
- Allied health (pharmacists, lab/rad techs, OT techs) — require blood_group, emergency contact
- Support (reception, housekeeping, security, dietary) — basic requirements
- Admin (HR, finance, IT, admin managers) — basic requirements

## Migration notes (see `scripts/migrate_master_data.py`)

- **Gender + Shift Type must exist first — GOTCHA #6.** Both `gender` and `default_shift` are Link fields with `mandatory_depends_on` set in HRMS. The migration script enforces `Gender` and `Shift Type` are inserted BEFORE `Employee` in `MIGRATION_ORDER`. If either DocType is missing when Employee rows run, every insert fails with `LinkValidationError`. Client-side: import the Gender master (auto-seeded by Frappe as `Male/Female/Other`) and the Shift Type CSV before this one.
- **Employee ID remap by name — GOTCHA #7.** Production and dev Employee IDs do NOT align (`HR-EMP-00211` vs `HR-EMP-00002`). The migration script builds `DEV_EMP_BY_NAME = {e.employee_name: e.name}` once at the top of `run()` and uses it to remap the `employee` Link field on every Shift Request and Shift Assignment record. Client-side: every Employee row in the CSV must have a non-empty `employee_name`; that's the join key downstream.
- **Upsert by name, not employee_number.** The script upserts by document `name`. If `employee_number` changes between runs, the existing record is matched by the old `name` and the new `employee_number` overwrites the old one — verify HR Settings → Employee Number naming is OFF or the import will collide.
- **Custom fields pass through.** `medical_council_reg_no`, `blood_group`, `emergency_contact_name`, `emergency_phone_number`, `next_of_kin`, etc. are passed through from source JSON via `_clean_payload()`. They are NOT required by the migration script, but they ARE enforced by Client Script on the live form for clinical staff. Empty values here will surface as form-level warnings during UAT.
- **Date validation.** `date_of_birth ≤ date_of_joining` is enforced by Frappe; the migration script does not pre-check. Imports with swapped dates will fail per-row with a clear `ValidationError`.
- **`status` defaults to `Active`.** The migration does NOT force `status` — if the CSV leaves `status` blank, the script still inserts with `status="Active"` (Frappe default). Use `status` for explicit off-boarding of legacy records on a fresh go-live.
