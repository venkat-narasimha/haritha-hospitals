# Client Onboarding Process — 6 Phases

**Project:** Haritha Hospitals ERPNext + HRMS Implementation
**Date:** 2026-09-09
**Methodology:** Convergent 6-phase model (Frappe + NestorBird + Ksolves + Oracle AIM + SAP Activate)

> Every major implementation framework in the market converges on six phases:
> Discovery → Environment + Master-Data → Validation → Migration → Configuration/UAT → Training/Cutover/Hypercare.
> We adopt this canon, adapted to Frappe + a 24/7 hospital context.

---

## Phase 1 — Discovery & Scope Freeze

| Field | Detail |
|---|---|
| **Duration** | 1–2 weeks |
| **Owner** | Joint (Partner leads, Client provides) |
| **Inputs** | Client kickoff, access to process owners, existing SOPs |
| **Activities** | Stakeholder interviews, current-state process maps, future-state design, gap analysis, success criteria, scope freeze |
| **Outputs** | Requirements doc, AS-IS / TO-BE process maps, scope-freeze document, success criteria, project charter |
| **Sign-off** | `02-templates/00_signoff_project_planning.md` |
| **Tools** | Frappe's `partner/implementation` 8-item checklist, Oracle AIM BP010–BP090 |

**Key activities:**
- Frame requirements around **business problems**, not modules (e.g., "shift handover gaps", "statutory filing delays", "geofence violations on night rounds" — not "implement Attendance DocType").
- Agree **Project Champion** on client side (Frappe: "highly critical for overall success").
- Capture the **Customer Tasks** list per Frappe: masters sharing in the specific format, briefing on core processes, provider using and role matrix, testing and validating system.
- Agree **Escalation Matrix** — 3–4 hierarchical layers.
- Define **success criteria** with measurable metrics (e.g., 100% biometric attendance captured, zero payroll discrepancies, monthly roster published 7 days in advance).

**Healthcare-specific scope items:**
- Operating hours: 24/7 inpatient vs OPD hours vs emergency only
- Departments in scope (ICU, OT, Wards, Casualty, OPD, Pharmacy, Lab, Radiology, Admin, HR, Finance, Housekeeping)
- Designations in scope (doctors, nurses, technicians, support staff, admin)
- Statutory obligations: ESI/PF/PT/Gratuity applicability

---

## Phase 2 — Environment Provisioning + Master-Data Intake

| Field | Detail |
|---|---|
| **Duration** | 1 week |
| **Owner** | Client fills workbook; Partner provisions site |
| **Inputs** | Signed Phase 1 charter, sponsor approval, valid email domains for user creation |
| **Activities** | Provision sandbox site, share intake workbook, client fills DocType sheets, add custom fields via Customize Form |
| **Outputs** | Sandbox site URL, filled `03-intake-workbook/01_master_data/*.csv`, custom-field definitions |
| **Sign-off** | `02-templates/01_signoff_steering_committee.md` (governance + intake readiness) |
| **Tools** | Frappe Cloud or self-hosted bench; this kit's `03-intake-workbook/`; Frappe Data Import template download |

**Key activities:**
- Provision **separate staging and production sites** (Frappe: "when custom code is involved, you must have a separate staging site").
- Client fills each DocType sheet's `client_value` column, following the `.md` validation rules.
- Add **Employee custom fields** before Employee import: `medical_council_reg_no`, `reg_validity_date`, `specialization`, `police_verification_date`, `health_checkup_due_date`, `next_of_kin`.
- Pre-create **Shift Type library** (6–8 types): 3×8h rotating, 2×12h, 1 on-call, 1 half-day OPD, 1 general duty.
- Pre-create **Shift Locations** with lat/long/radius for each physical zone (Main, ICU, OT, Casualty, OPD, Annexe).
- One **Holiday List per state** if multi-state operations; one default per Company.
- Assign **Project Champion** as primary approver for missing departmental approvers.

**Healthcare-specific intake items:**
- Designations library (Medical Director → Receptionist — see `01_master_data/02_designation.md`)
- Department codes (CARD, ICU, OT-1, OPD-A) for short codes
- Per-state holiday lists (e.g., Telangana vs Andhra Pradesh)
- Blood group, emergency contact, medical council reg no for each Employee

---

## Phase 3 — Validation & Dry-Run Migration

| Field | Detail |
|---|---|
| **Duration** | 1 week |
| **Owner** | Partner runs validation; Client confirms data accuracy |
| **Inputs** | Filled workbook, sandbox site, custom fields |
| **Activities** | Dry-run import via Data Import tool, run validation script, generate error report, iterate, sign-off per DocType |
| **Outputs** | `03-intake-workbook/03_signoff/02_master_validation_report.md` populated, per-DocType sign-offs |
| **Sign-off** | `03-intake-workbook/03_signoff/01_per_doctype_signoff_template.md` (one per DocType) |
| **Tools** | `bench execute haritha_hospital.scripts.migrate_master_data --dry-run`, Frappe Data Import validation |

**Key activities:**
- Run **dry-run import** into sandbox; do NOT commit to production yet.
- For each DocType: count rows attempted / succeeded / failed; classify errors (validation, FK, format, uniqueness).
- Iterate: fix workbook → re-import → re-validate → client confirms accuracy.
- Sign-off per DocType using the template — Client Project Lead + HR Lead must physically/digitally sign.
- Build a **parallel-run week** on sandbox: live data feed into sandbox alongside legacy system (per Tabsyst partner evaluation criteria).
- Document **data lineage**: source system → workbook → ERPNext record id.

**Healthcare-specific validation:**
- Verify all Employee records have `blood_group` populated (statutory for clinical staff).
- Verify medical_council_reg_no is present for all doctors (NMC/state council compliance).
- Verify Shift Location geofence radii are reasonable (50–200 m indoor, 500 m+ campus).
- Verify Holiday List covers at least one full year per state.

---

## Phase 4 — Production Migration

| Field | Detail |
|---|---|
| **Duration** | 1–2 days (typically weekend cutover) |
| **Owner** | Partner leads; Client provides downtime access |
| **Activities** | Full Data Import to production, integrity checks, smoke tests, user creation |
| **Outputs** | Production site live, `name` mapping workbook, integrity check report |
| **Sign-off** | `02-templates/04_signoff_go_live.md` |
| **Tools** | `bench execute haritha_hospital.scripts.migrate_master_data --live`, Data Import, integrity check script |

**Key activities:**
- Schedule cutover during **low-traffic window** (weekend, ideally Friday 18:00 → Monday 06:00 for hospital with reduced admin staff).
- Take **full database backup** before migration.
- Import in **dependency order**: Company → Holiday List → Department → Designation → Employment Type → Employee Grade → Branch → Shift Type → Shift Location → Shift Schedule → Employee → Leave Type → Leave Policy → Leave Period → Leave Allocation → Shift Assignment.
- After each import step, run **integrity check** (count matches, FK validity, no orphans).
- Smoke-test critical user paths: login, view employee, assign shift, apply leave, run attendance.
- **Rollback plan documented** and rehearsed (per Oracle AIM PM040).

**Healthcare-specific cutover items:**
- Parallel-run for at least 1 week post-cutover (continue manual process alongside ERPNext).
- Communication to all staff 7 days, 3 days, 1 day, and on cutover day.
- Rollback trigger thresholds agreed (e.g., >5 critical failures = rollback).
- Biometric devices reconfigured to point at production URL.
- Payroll NOT run on ERPNext for first month (use parallel payroll calculation).

---

## Phase 5 — Configuration, Integrations & UAT

| Field | Detail |
|---|---|
| **Duration** | 2–3 weeks |
| **Owner** | Partner configures; Client executes UAT |
| **Activities** | Configure HR / Payroll / Auto-Attendance settings, biometric API integration, UAT execution, defect triage |
| **Outputs** | Settings configured, UAT test cases executed, defect log, UAT sign-off |
| **Sign-off** | `02-templates/03_signoff_uat.md` |
| **Tools** | `03-intake-workbook/02_settings_checklists/`, Frappe bench scheduler, biometric API |

**Key activities:**
- Complete the three **settings checklists** in `02_settings_checklists/`: HR, Payroll, Auto-Attendance.
- Integrate biometric device(s) via `add_log_based_on_employee_field` API endpoint (recommended) OR Data Import of punch logs (fallback).
- Configure **auto-attendance scheduler** — `enable_auto_attendance`, `process_attendance_after`, `working_hours_threshold_for_half_day`, `working_hours_threshold_for_absent`.
- Configure **late entry / early exit** grace periods per Shift Type.
- Configure **geofence validation** for Shift Locations (requires HR Settings → Allow Geolocation Tracking = 1).
- Execute UAT with **Client's actual end users** (HR, Nursing Supervisor, Doctors) — not just Partner QA.
- Triage defects by severity: P1 (blocks payroll), P2 (blocks user workflow), P3 (cosmetic).
- UAT exit criteria: zero open P1, <3 open P2, all P3 logged for future.

**Healthcare-specific configuration:**
- Shift Type: `enable_auto_attendance=1` for nursing shifts; manual for on-call/visiting consultants.
- Geofence radii: tighter for ICU/OT (50 m), wider for OPD/Admin (200 m).
- Holiday List: assign per Department for OPD vs wards (Central Govt vs State Govt pattern).
- Payroll: night-shift allowance, on-call allowance configured in Salary Component (deferred to phase 2 if Payroll module not in initial scope).

---

## Phase 6 — Training, Cutover & Hypercare

| Field | Detail |
|---|---|
| **Duration** | 1–2 weeks training + 2–4 weeks hypercare |
| **Owner** | Partner trains; Client adopts |
| **Activities** | Train-the-trainer sessions, role-specific training videos, runbooks, go-live day execution, hypercare rotation |
| **Outputs** | Training videos, runbooks per role, go-live sign-off, satisfaction survey |
| **Sign-off** | `02-templates/02_signoff_training.md`, `02-templates/04_signoff_go_live.md`, `02-templates/05_signoff_post_implementation.md` |
| **Tools** | Frappe School, Loom/recorded demos, runbook Markdown, WhatsApp hypercare channel |

**Key activities:**
- **Training plan** by role: HR Lead (4h), HR Executive (8h), Department Manager (4h), Shift Supervisor (4h), Employee self-service (1h), IT Admin (4h).
- **Runbooks** per role: step-by-step Markdown for common tasks (assign shift, approve leave, run attendance, generate payroll register).
- **Go-live day**: war-room approach — Partner + Client IT + Client HR physically present, communication tree active, rollback plan ready.
- **Hypercare** (2–4 weeks): daily standups for week 1, every-other-day for week 2, weekly for weeks 3–4. Bug-fix SLA: P1 same-day, P2 next-day, P3 within week.
- **Post-implementation review** at week 4: satisfaction survey, outstanding issues log, ongoing support plan (e.g., monthly retainer or quarterly check-in).

**Healthcare-specific training:**
- Biometric device operation for security/housekeeping staff.
- Geofence check-in via mobile app for visiting consultants.
- Attendance adjustment workflow for clinical staff (managers approve, HR audits).
- Statutory reporting (ESI/PF/PT) for HR/Finance.

---

## Phase gates summary

| Gate | Sign-off template | Owner of sign-off |
|---|---|---|
| Discovery done | `02-templates/00_signoff_project_planning.md` | Client Project Lead |
| Steering + intake ready | `02-templates/01_signoff_steering_committee.md` | Client Project Lead |
| Per-DocType accuracy | `03-intake-workbook/03_signoff/01_per_doctype_signoff_template.md` (× 15) | Client HR Lead |
| Validation report | `03-intake-workbook/03_signoff/02_master_validation_report.md` | Client HR Lead + Partner Tech Lead |
| UAT passed | `02-templates/03_signoff_uat.md` | Client Project Lead + Partner Lead |
| Training complete | `02-templates/02_signoff_training.md` | Client HR Lead |
| Go-live verified | `02-templates/04_signoff_go_live.md` | Joint (both Project Leads) |
| Hypercare closed | `02-templates/05_signoff_post_implementation.md` | Joint + Project Champion |

## Phase duration totals

- HRMS-only: **6–9 weeks** (Phases 1–6, no hypercare overlap)
- HRMS + full Payroll: **8–12 weeks**
- HRMS + Payroll + Multi-module: **12–20 weeks**

## Custom Development Tracker

Per Frappe guidance: every customisation, even if later de-scoped, gets an estimate and active tracker entry. This kit does not generate custom code, but partner-side extensions to `haritha_hospital.scripts.migrate_master_data` and `extract_doctype_fields` should be tracked in this phase.

## Weekly Review Cadence

Per Frappe: joint customer/partner cadence — minimum weekly during Phases 1–5, daily during Phase 6 cutover week. Use `01_signoff_steering_committee.md` agenda template as standing weekly agenda.
