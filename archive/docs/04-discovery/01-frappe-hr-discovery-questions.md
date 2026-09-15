# Frappe HR Discovery Questions — Concise Answers

**Date:** 2026-09-15
**Context:** Venkat's 12-question discovery prompt for the Haritha Hospitals Frappe HR + HRMS deployment. These are the consolidated answers per the research + templates + HTML decks + manual testing deliverables produced in this session.

---

## Q1: Do we need to make any changes in Frappe HR with the data we got?

No. The hospital data was already ingested (210 employees, 25 shift types, 7829 shift assignments, etc.) and verified working. Stock schema + custom app fields (`haritta_hospital`) cover what we have. Only gaps are non-blockers (e.g., Overtime Type missing — out of scope for go-live v1).

---

## Q2: What do we need from the shift management data?

Mandatory:

- **Shift Type** (when work happens)
- **Shift Assignment** (who works when)
- **Shift Location** (where — for biometric GPS)

Optional / advanced:

- **Shift Schedule** (rotation patterns — only needed if your shifts repeat on a weekly pattern; otherwise Shift Assignment alone suffices)
- **Shift Request** (employee-initiated swap requests — operational polish, not required for go-live)

---

## Q3: What do we need from leave management?

Mandatory:

- **Leave Type** (define kinds like Sick/Casual/Earned with rules)
- **Leave Policy** (bundle of Leave Types + allocation rules)
- **Leave Allocation** (per-employee grants)
- **Leave Application** (employee submits)
- **Leave Approval** (manager approves — uses Employee.leave_approver Link)

Optional / advanced:

- **Leave Period** (if you want cycle boundaries beyond what Leave Policy auto-handles)
- **Leave Block List** (block dates for departments)
- **Leave Encashment** (at exit)
- **Compensatory Leave Request** (OT → leave credit)
- **Leave Ledger Entry** (auto-generated audit — you don't need to populate it)

---

## Q4: Bare minimum in Frappe HR for go-live?

Stock Frappe HR ready out-of-the-box + the 3 modules with data populated:

- Org Mgmt: Company / Department / Designation / Branch / Grade / Employee / Employment Type
- Shift Mgmt: Shift Type / Shift Assignment / Shift Location
- Leave Mgmt: Leave Type / Leave Policy / Leave Allocation / Leave Application

Plus configuration:

- HR Settings: leave approver defaults, holiday list
- Payroll Settings: statutory components (even if payroll itself is deferred)
- Per-role permission setup
- Auto Attendance scheduler enabled with grace period configured

---

## Q5: Do we have templates for the client to get the data?

Yes. `docs/client-onboarding/03-intake-workbook/` has 19 CSV+MD templates + README + 2 signoff docs + settings checklists. All rebuilt this session (P5) from actual project schema.

---

## Q6: Do we have a template for the data we uploaded (to show the client)?

Yes:

- `docs/client-onboarding/03-intake-workbook/reconciliation/sample-raw-to-erp.md` — shows side-by-side: raw Excel row → Frappe HR record (name field)
- `docs/client-onboarding/03-intake-workbook/mapping/frappe-hr-data-mapping.md` — field-by-field mapping with gotchas
- `docs/client-onboarding/03-intake-workbook/AUDIT-REPORT.md` — 15-template audit coverage matrix

---

## Q7: Flexible benefits in this initial version?

No. Defer entirely. It's a payroll-adjacent feature; per the original Q7 decision, we agreed not to cover payroll in v1. Add later if a client asks.

---

## Q8: Configuration we need to do?

1. Custom-field fixtures load via `bench execute haritta_hospital.install.import_fixtures` (or `bench install-app haritta_hospital`)
2. HR Settings: default leave approver, holiday list, fiscal year
3. Payroll Settings: even with payroll deferred, configure tax slabs + components for future
4. Permission setup: HR Manager / HR User roles
5. Auto Attendance scheduler: enable + grace period per Shift Type
6. Email/SMS notifications
7. Workflow: Leave Approval (uses Leave Approver Link)
8. Company default accounts (deferred accounts, set per migration script's two-step pattern)

---

## Q10: What is the master data?

The 15 DocTypes loaded ONCE during initial onboarding (in `MIGRATION_ORDER` order):

1. Company
2. Account
3. Cost Center
4. Department
5. Designation
6. Item Group
7. UOM
8. Gender
9. Employment Type
10. Shift Type
11. Shift Location
12. Holiday List
13. Employee
14. Item
15. Shift Request
16. Shift Schedule
17. Shift Assignment

Plus 4 added in v2 templates:

- Branch
- Employee Grade
- Leave Type
- Leave Policy
- Leave Period
- Leave Allocation

Total ~19 master-data DocTypes.

---

## Q11: What is the transaction data?

Daily/periodic operational data after go-live:

- **Attendance** — auto-generated from Employee Checkin
- **Employee Checkin** — raw biometric/mobile punches
- **Leave Application** — employee submits
- **Leave Approval events** — appended automatically
- **Attendance Request** — regularisation flow
- **Holiday** (child rows) — calendar updates

4 transaction CSV templates just shipped at `docs/client-onboarding/03-intake-workbook/01_master_data/16-19.*`:

- 16_attendance
- 17_employee_checkin
- 18_leave_application
- 19_leave_ledger_entry

---

## Q12: Reports (RICEFW)?

**R — Reports (stock, ready):**

- Monthly Attendance Details
- Leave Balance
- Leave Ledger Entry
- Employee Master
- Shift Roster
- Absenteeism Rate (derived view)

**I — Interfaces:**

- Biometric device → Employee Checkin (via `skip_auto_attendance` flag for devices that should bypass auto-attendance)
- Frappe HR Mobile App → Checkin + Leave Application

**C — Conversions:**

- The 19 templates + migration script = the conversion path

**E — Enhancements:**

- Per-hospital custom fields in `haritta_hospital` app (78 Custom Fields + 189 Property Setters)

**F — Forms:**

- No Web Forms in v1

**W — Workflows:**

- Stock Leave Approval workflow (uses Employee.leave_approver Link)
- Shift Request approval workflow

---

**Document location:** `archive/docs/04-discovery/01-frappe-hr-discovery-questions.md`
**Last updated:** 2026-09-15
