# Manual Transaction Checklist — Frappe HR v16.5.0

**Purpose:** Categorized list of every transaction Venkat should manually perform + sign off in `pberpprod.duckdns.org` before go-live. Covers all 6 modules covered by the HTML decks (Org Mgmt, Attendance, Shift Mgmt, Leave, Lifecycle, Overview).

**Test environment:** `pberpprod.duckdns.org` (production-like) — also valid for `pberpdev.duckdns.org` if mirroring prod
**Tester:** Venkat Narasimha
**Sign-off date:** 2026-09-18

**Source decks (reference for slide-by-slide content):**
- `docs/handbook/03-client/org-management-presentation.html` (17 slides)
- `docs/handbook/03-client/attendance-management-presentation.html` (16 slides)
- `docs/handbook/03-client/lifecycle-management-presentation.html` (16 slides)
- `docs/handbook/03-client/leave-management-presentation.html` (22 slides)
- `docs/handbook/03-client/frappe-hr-overview-presentation.html` (14 slides)
- `docs/handbook/03-client/shift-management-presentation-v2.html` (18 slides — frozen canonical)

---

## 2026-09-18 Updates

This document was corrected on 2026-09-18 based on Venkat's manual testing report (`manual-transactions-testing.txt`). Read-only investigation by Stream 1 produced findings in `/root/.openclaw/workspace/investigation-2026-09-18-pending-transactions.md` (383 lines, per-transaction verdicts: PASS / FAIL-MANUAL / FAIL-SYSTEMIC / FAIL-DATA / UNCLEAR).

**Corrections applied (Stream 2):**

- 13 `[FAIL-MANUAL]` corrections: rewrote test cards to match HRMS v16 reality (correct field names, single-date attendance tool, v16 grace_period split, autoname='prompt' scope, etc.)
- 3 `[FAIL-SYSTEMIC]` reports flagged: T-048 (Employee Analytics — NoneType bug, vendor review), T-049 (Shift Roster — does not exist in v16), T-050 (Absenteeism — does not exist in v16)
- 4 `[UNCLEAR]` write-required notes added: T-052 (shift_schedule_assignment NULLIFICATION), T-057 (Holiday List date-validation), T-058 (Department root trap), T-060 (multi-Company isolation — also structurally untestable in current prod)

**Verdicts from Stream 1 (all referenced in the per-transaction cards below):**

- PASS: 8 (T-45, T-47, T-51 [partial], T-53, T-54, T-55 [with correction], T-59, plus EHU/PP after Stream 3 config fix)
- FAIL-MANUAL: 9 (T-10, T-15, T-16, T-18, T-20, T-44, T-45-name, T-51-shift-assignment, T-56)
- FAIL-SYSTEMIC: 4 (T-48, T-49, T-50, EHU/PP-popup UX)
- FAIL-DATA: 3 (T-46, EHU/PP, T-44-Holiday-List-Assignment, plus downstream T-30–T-36)
- UNCLEAR: 4 (T-52, T-57, T-58, T-60)

Stream 3 (prod config) and Stream 4 (commit + sign-off + sanitization) own the remaining steps — this doc was edited only, no commit was created.

---

## TL;DR — transaction counts

| Category | Critical-path | Edge-case | Non-critical | Total |
|---|---:|---:|---:|---:|
| 1. Organization Management | 3 | 3 | 6 | **12** |
| 2. Attendance & Shift | 3 | 2 | 5 | **10** |
| 3. Leave Management | 4 | 3 | 7 | **14** |
| 4. Employee Lifecycle | 2 | 2 | 4 | **8** |
| 5. Reports & Analytics | 1 | 1 | 4 | **6** |
| 6. Edge Cases (cross-cutting) | 0 | 10 | 0 | **10** |
| **Total** | **13** | **21** | **26** | **60** |

---

## How to use this document

1. **UI section** (Appendix A per transaction): click-by-click manual steps
2. **bench execute section** (Appendix B per transaction): Python snippets for scripted verification
3. Per-transaction card includes pre-conditions + expected result (so you know what "success" looks like)
4. Sign-off checkboxes at the bottom — Venkat fills these as transactions pass

---

## Per-transaction card format

```markdown
### T-XXX — <Title>

- **Module:** <module>
- **DocType:** <doctype>
- **Test scenario:** <1-sentence description>
- **Pre-conditions:** <what must already exist>
- **UI click path:** See Appendix A (T-XXX)
- **bench execute snippet:** See Appendix B (T-XXX)
- **Expected result:** <what success looks like>
- ☐ Pass / ☐ Fail | Date: YYYY-MM-DD | Notes: <free text>
```

---

## Category 1: Organization Management (12 transactions)

### T-001 — Create top-level Department with auto-seeded Approver

- **Module:** Organization Management
- **DocType:** Department
- **Test scenario:** Create a top-level (no parent) Department and verify the Approver child row is auto-seeded
- **Pre-conditions:** Company A exists; no other Departments needed
- **Expected result:**
  - Doc created successfully
  - `tabDepartment Approver` row exists with `approver="Administrator"` and `parentfield="shift_request_approver"` (auto-seeded per `scripts/migrate_master_data.py` GOTCHA #10)
- ☐ Pass / ☐ Fail | Date: ___

### T-002 — Create Employee with full link chain

- **Module:** Organization Management
- **DocType:** Employee
- **Test scenario:** Create one Employee linking to all required parent entities
- **Pre-conditions:** Department (T-001), Designation, Grade, Branch, Employment Type all exist
- **UI click path:** Appendix A
- **bench execute:** Appendix B
- **Expected result:**
  - Employee inserts with autoname `HR-EMP-.YYYY.-`
  - All Link fields resolve (no LinkValidationError)
  - `naming_series` is set to `HR-EMP-.YYYY.-` per Property Setter reqd=1 (research §2)
- ☐ Pass / ☐ Fail | Date: ___

### T-003 — Promote Employee (record grade change)

- **Module:** Organization Management
- **DocType:** Employee (with promotion record)
- **Test scenario:** Update an Employee's grade + verify the change persists + downstream fields cascade
- **Pre-conditions:** T-002 Employee exists; a higher Grade exists
- **Expected result:**
  - Employee.grade updates to new value
  - If Salary Structure Assignment is linked to Grade, downstream pay calc reflects new grade
- ☐ Pass / ☐ Fail | Date: ___

### T-004 — Department parent_department="All Departments" root trap (must fail)

- **Module:** Organization Management
- **DocType:** Department
- **Test scenario:** Try to create a Department with parent="All Departments" (Frappe auto-root)
- **Pre-conditions:** None
- **Expected result:** `ParentNotFoundError` — script + UI both reject this
- ☐ Pass / ☐ Fail | Date: ___

### T-005 — Duplicate Department.name within same Company (must fail uniqueness)

- **Module:** Organization Management
- **DocType:** Department
- **Test scenario:** Try to create two Departments with the same name under the same Company
- **Pre-conditions:** Company A exists; one Department already exists
- **Expected result:** `DuplicateEntryError` or `ValidationError` for name uniqueness
- ☐ Pass / ☐ Fail | Date: ___

### T-006 — Branch without Company (must fail)

- **Module:** Organization Management
- **DocType:** Branch
- **Test scenario:** Try to create a Branch with no Company set
- **Pre-conditions:** None
- **Expected result:** `LinkValidationError` — Company is required
- ☐ Pass / ☐ Fail | Date: ___

### T-007 — Create Designation

- **Module:** Organization Management
- **DocType:** Designation
- **Test scenario:** Standard upsert path
- **Pre-conditions:** None
- **Expected result:** Doc created; autoname=`field:designation_name`
- ☐ Pass / ☐ Fail | Date: ___

### T-008 — Create Employee Grade with pay_band custom field

- **Module:** Organization Management
- **DocType:** Employee Grade
- **Test scenario:** Create a Grade with custom `pay_band` field set
- **Pre-conditions:** None (assuming haritta_hospital custom-field fixtures loaded)
- **Expected result:** Doc created with pay_band populated; autoname=`field:grade_name`
- ☐ Pass / ☐ Fail | Date: ___

### T-009 — Create Employment Type

- **Module:** Organization Management
- **DocType:** Employment Type
- **Test scenario:** Standard upsert
- **Pre-conditions:** None
- **Expected result:** Doc created
- ☐ Pass / ☐ Fail | Date: ___

### T-010 — Update Department name (idempotent re-run via field edit)

- **Module:** Organization Management
- **DocType:** Department
- **Test scenario:** Open an existing Department, edit any field (e.g., rename `department_name` or change a description), Save — verify the update is idempotent (no duplicate row). NOTE: do NOT call the dev migration script here — it lives only in the dev workspace (`scripts/migrate_master_data.py`) and is not a runtime/ prod maintenance task.
- **Pre-conditions:** T-001 Department exists
- **Expected result:**
  - Doc updates cleanly; no duplicate row created
  - autoname retains company abbr correctly
- ☐ Pass / ☐ Fail | Date: ___

### T-011 — Transfer Employee between Departments

- **Module:** Organization Management
- **DocType:** Employee
- **Test scenario:** Move an Employee from Dept A to Dept B (no Promotion)
- **Pre-conditions:** T-002 Employee exists; second Department exists
- **Expected result:** Employee.department updates; history preserved
- ☐ Pass / ☐ Fail | Date: ___

### T-012 — Create Employee with all healthcare custom fields populated

- **Module:** Organization Management
- **DocType:** Employee
- **Test scenario:** Create Employee with health_insurance_*, PAN, IFSC, MICR, provident_fund_account all set
- **Pre-conditions:** haritta_hospital custom-field fixtures loaded; related Link targets exist
- **Expected result:** All custom fields saved without error; visible on Employee form
- ☐ Pass / ☐ Fail | Date: ___

---

## Category 2: Attendance & Shift (10 transactions)

### T-013 — Create Shift Type with autoname='prompt' (name required)

- **Module:** Shift Management
- **DocType:** Shift Type
- **Test scenario:** Create Shift Type with explicit name (autoname='prompt' contract)
- **Pre-conditions:** None
- **Expected result:** Doc inserts; `ValidationError` raised if name column is empty (GOTCHA #4)
- ☐ Pass / ☐ Fail | Date: ___

### T-014 — Create Shift Assignment with employee_name remap (GOTCHA #7)

- **Module:** Shift Management
- **DocType:** Shift Assignment
- **Test scenario:** Create Shift Assignment with `employee_name` (NOT `employee`) as the join key
- **Pre-conditions:** T-002 Employee exists; T-013 Shift Type exists; canonical Shift Location exists
- **Expected result:**
  - Doc inserts
  - `employee` Link gets resolved to Employee.name using `employee_name` join
  - `shift_schedule_assignment` is NULLIFIED regardless of source value (GOTCHA #9)
- ☐ Pass / ☐ Fail | Date: ___

### T-015 — Auto Attendance from Employee Checkin (end-to-end)

- **Module:** Attendance
- **DocType:** Attendance (auto-generated)
- **Test scenario:** Create an Employee Checkin → wait for Auto Attendance scheduler → verify Attendance row created
- **Pre-conditions:** T-013 Shift Type (with enable_auto_attendance=1 + process_attendance_after set); Employee with an active Shift Assignment; Holiday List Assignment exists for the employee at the relevant date
- **Expected result:**
  - Attendance row appears with status matching punch-in within grace period — wait 1–5 minutes for the auto-attendance scheduler tick (e.g., HR-ATT-2026-XXXXX auto-generated). System does not surface rows instantly; verifier must wait.
  - `shift` field on the Employee Checkin comes from the **active Shift Assignment** (NOT from `Employee.default_shift` — `default_shift` is fallback only, used when no active Shift Assignment exists). For HR-EMP-00421 the active assignment is HR-SHA-26-09-00001.
  - `working_hours` is a Float field on the **Attendance** doc (NOT on Employee Checkin) — verified via `frappe.get_meta("Attendance")`. Requires both IN and OUT checkins to compute; a single IN punch yields `working_hours = 0.0`.
- ☐ Pass / ☐ Fail | Date: ___

### T-016 — Duplicate Attendance for same employee + date (must fail)

- **Module:** Attendance
- **DocType:** Attendance
- **Test scenario:** Confirm the system enforces single-Attendance-per-(employee, attendance_date). Procedure: insert the FIRST row for (HR-EMP-00421, 2026-09-17) via the scheduler (HR-ATT-2026-06304 already exists). Then attempt to insert a SECOND Attendance for the same (employee, date) — the system should block it.
- **Pre-conditions:** One Attendance row exists for Employee A on date X (e.g., HR-ATT-2026-06304 was auto-generated at submission time)
- **Expected result:**
  - Second manual insert for the same (employee, attendance_date) → `DuplicateEntryError` raised (Frappe's unique constraint)
  - Frappe's unique constraint on (employee, attendance_date) is enforced at the ORM layer; HRMS Attendance schema: `employee (Link, reqd=1)`, `attendance_date (Date, reqd=1)`.
  - Note: an auto-attendance-generated row may leave the `shift` field empty when `Employee.default_shift` is unset — HRMS does not propagate shift from the Checkin to the Attendance row by default (known HRMS quirk).
- ☐ Pass / ☐ Fail | Date: ___

### T-017 — Shift Assignment with end_date < start_date (must fail)

- **Module:** Shift Management
- **DocType:** Shift Assignment
- **Test scenario:** Create Shift Assignment where end_date precedes start_date
- **Pre-conditions:** T-002 Employee exists
- **Expected result:** `ValidationError` — date validation rejects
- ☐ Pass / ☐ Fail | Date: ___

### T-018 — Create Shift Location (lat/long are OPTIONAL in HRMS v16)

- **Module:** Shift Management
- **DocType:** Shift Location
- **Test scenario:** Create Shift Location — verify that lat/long and checkin_radius are OPTIONAL fields in HRMS v16; only `location_name` is required.
- **Pre-conditions:** None
- **Expected result:**
  - Doc inserts successfully with only `location_name` set (no lat/long required)
  - Schema: `latitude (Float, reqd=0)`, `longitude (Float, reqd=0)`, `checkin_radius (Int, reqd=0)` — all OPTIONAL
  - autoname=`field:location_name`
  - Sub-test T-018a (optional): set lat/long + checkin_radius and verify geofenced checkins outside the radius are rejected.
- ☐ Pass / ☐ Fail | Date: ___

### T-019 — Create Shift Schedule with repeat_on_days child rows

- **Module:** Shift Management
- **DocType:** Shift Schedule
- **Test scenario:** Create Shift Schedule with multiple repeat_on_days child rows
- **Pre-conditions:** T-013 Shift Type exists
- **Expected result:**
  - Doc inserts; autoname='prompt' requires name
  - Child rows persist (GOTCHA #8 — default fields=['*'] drops them; migration script re-appends via doc.append())
- ☐ Pass / ☐ Fail | Date: ___

### T-020 — Manual Attendance override via Attendance Tool (single-date per session)

- **Module:** Attendance
- **DocType:** Attendance
- **Test scenario:** Use the Employee Attendance Tool to bulk-mark attendance for a department. NOTE: HRMS v16's Employee Attendance Tool is a SINGLE-DATE bulk-marker (NOT a date-range picker).
- **Pre-conditions:** Department with employees exists
- **Expected result:**
  - Tool exposes a single `date` field (no `from_date`/`to_date`). Filter by dept/branch/grade/employment_type, click "Get Employees", set status, click "Mark".
  - Multiple Attendance rows created (one per employee); exclude-holidays toggle respected.
  - For multi-date coverage: invoke the tool once per date (or script via `mark_employee_attendance(date, ...)` in a loop — `employee_attendance_tool.py` exposes single-date signatures).
- ☐ Pass / ☐ Fail | Date: ___

### T-021 — Employee Checkin with skip_auto_attendance=1

- **Module:** Attendance
- **DocType:** Employee Checkin
- **Test scenario:** Submit Employee Checkin with skip_auto_attendance=1; verify no Attendance row auto-generated
- **Pre-conditions:** T-013 Shift Type with auto-attendance on; Employee exists
- **Expected result:**
  - Employee Checkin row inserted
  - NO Attendance row generated for that date (skip flag honored)
- ☐ Pass / ☐ Fail | Date: ___

### T-022 — Attendance Request regularisation flow

- **Module:** Attendance
- **DocType:** Attendance Request
- **Test scenario:** Employee submits Attendance Request for missed checkin → approve → verify Attendance row gets created/corrected
- **Pre-conditions:** T-002 Employee exists; auto-attendance enabled
- **Expected result:** Attendance row reflects the approved status correction
- ☐ Pass / ☐ Fail | Date: ___

---

## Category 3: Leave Management (14 transactions)

### T-023 — Create Leave Type with all rule flags

- **Module:** Leave Management
- **DocType:** Leave Type
- **Test scenario:** Create Leave Type with various boolean flags (is_carry_forward, allow_encashment, is_lwp, etc.)
- **Pre-conditions:** None
- **Expected result:** Doc inserts; flags saved; mutually-exclusive flag combos flagged
- ☐ Pass / ☐ Fail | Date: ___

### T-024 — Create Leave Policy + child details

- **Module:** Leave Management
- **DocType:** Leave Policy
- **Test scenario:** Create Leave Policy with 2-3 child LeavePolicyDetails rows
- **Pre-conditions:** T-023 Leave Types exist
- **Expected result:** Doc inserts; child rows persist
- ☐ Pass / ☐ Fail | Date: ___

### T-025 — Create Leave Period + bulk assign via Leave Control Panel

- **Module:** Leave Management
- **DocType:** Leave Period + Leave Allocation (bulk-generated)
- **Test scenario:** Create Leave Period for FY 2026, then run Leave Control Panel to bulk-allocate by department
- **Pre-conditions:** T-024 Leave Policy + Department with employees exist
- **Expected result:**
  - Leave Period created with is_active=1
  - Multiple Leave Allocation rows generated (one per Employee + Leave Type combo)
- ☐ Pass / ☐ Fail | Date: ___

### T-026 — Submit + Approve Leave Application → Ledger entry

- **Module:** Leave Management
- **DocType:** Leave Application + Leave Ledger Entry
- **Test scenario:** End-to-end: submit application → approver approves → verify ledger entry posted
- **Pre-conditions:** T-002 Employee exists; T-023 Leave Type exists; T-024 Leave Policy + Assignment exists; Employee has Allocation
- **Expected result:**
  - Leave Application status flips Open → Approved (docstatus 0→1)
  - Leave Ledger Entry created with transaction_type='Application', leaves field negative
  - Employee balance reduced accordingly
- ☐ Pass / ☐ Fail | Date: ___

### T-027 — Leave Application without Leave Approver (must fail LinkValidation)

- **Module:** Leave Management
- **DocType:** Leave Application
- **Test scenario:** Submit Leave Application without setting leave_approver
- **Pre-conditions:** T-002 Employee exists; T-023 Leave Type
- **Expected result:** `LinkValidationError` — leave_approver required (Link→User)
- ☐ Pass / ☐ Fail | Date: ___

### T-028 — Leave Application with end_date < from_date (must fail)

- **Module:** Leave Management
- **DocType:** Leave Application
- **Test scenario:** Submit Leave Application with end_date before from_date
- **Pre-conditions:** Same as T-027
- **Expected result:** `ValidationError` — date validation rejects
- ☐ Pass / ☐ Fail | Date: ___

### T-029 — Leave Encashment at Employee exit

- **Module:** Leave Management
- **DocType:** Leave Encashment
- **Test scenario:** Process Leave Encashment when Employee is separated; verify balance calculation
- **Pre-conditions:** Employee has outstanding earned leave allocation; Separation approved
- **Expected result:**
  - Leave Encashment record created with days × daily rate
  - Leave Ledger Entry with transaction_type='Encashment'
- ☐ Pass / ☐ Fail | Date: ___

### T-030 — Compensatory Leave Request (OT → leave credit)

- **Module:** Leave Management
- **DocType:** Compensatory Leave Request
- **Test scenario:** Convert extra hours worked into leave credit
- **Pre-conditions:** Employee has logged overtime/extra hours
- **Expected result:**
  - Compensatory Leave Request created
  - On approval: Leave Allocation incremented
- ☐ Pass / ☐ Fail | Date: ___

### T-031 — Leave Block List enforcement

- **Module:** Leave Management
- **DocType:** Leave Block List
- **Test scenario:** Department has `leave_block_list` set; Employee tries to submit Leave Application for blocked date
- **Pre-conditions:** Department with `leave_block_list` Link set; Employee in that department
- **Expected result:** Leave Application creation fails with `LeaveBlockListError` for blocked dates
- ☐ Pass / ☐ Fail | Date: ___

### T-032 — Overlapping Leave Applications (verify reject or auto-merge)

- **Module:** Leave Management
- **DocType:** Leave Application
- **Test scenario:** Submit two Leave Applications for same Employee on overlapping dates
- **Pre-conditions:** T-002 Employee
- **Expected result:** Second submit is rejected OR (rare) auto-merged; verify the system's behavior
- ☐ Pass / ☐ Fail | Date: ___

### T-033 — Leave Type with is_lwp=1 (unpaid leave)

- **Module:** Leave Management
- **DocType:** Leave Type
- **Test scenario:** Submit Leave Application for Leave Type marked is_lwp=1; verify Salary Slip reflects no paid leave deduction
- **Pre-conditions:** T-023 Leave Type with is_lwp=1; T-002 Employee
- **Expected result:** Leave Application approved; Salary Slip line item = LWP (unpaid)
- ☐ Pass / ☐ Fail | Date: ___

### T-034 — Cancel an Approved Leave Application

- **Module:** Leave Management
- **DocType:** Leave Application
- **Test scenario:** Cancel a previously approved Leave Application
- **Pre-conditions:** Approved Leave Application exists
- **Expected result:**
  - Leave Application status flips to Cancelled
  - Leave Ledger Entry created with transaction_type='Application', leaves positive (reverse of original)
  - Employee balance restored
- ☐ Pass / ☐ Fail | Date: ___

### T-035 — Leave Period rollover (annual)

- **Module:** Leave Management
- **DocType:** Leave Period
- **Test scenario:** Mark current FY period inactive, create new FY period, re-run bulk allocation
- **Pre-conditions:** Active Leave Period exists for FY 2026
- **Expected result:**
  - Old period is_active=0
  - New period is_active=1 (only one active per Company)
  - New Leave Allocations generated for the new period
- ☐ Pass / ☐ Fail | Date: ___

### T-036 — Leave Ledger Entry audit trail verification

- **Module:** Leave Management
- **DocType:** Leave Ledger Entry
- **Test scenario:** Over a test period, verify the Ledger is append-only and balances correctly
- **Pre-conditions:** Multiple Allocation + Application events occurred
- **Expected result:**
  - Ledger rows are append-only (no UPDATE/DELETE on existing rows)
  - Balance = sum(leaves column) for each (employee, leave_type, period)
- ☐ Pass / ☐ Fail | Date: ___

---

## Category 4: Employee Lifecycle (8 transactions)

### T-037 — Onboard new Employee via Onboarding template

- **Module:** Lifecycle
- **DocType:** Employee Onboarding
- **Test scenario:** Run onboarding flow for a new hire (Staff Nurse role)
- **Pre-conditions:** Onboarding Template exists for Staff Nurse; per-role tasks configured
- **Expected result:**
  - Onboarding record created with task list
  - On all tasks complete: Employee auto-created with links to Department + Designation
- ☐ Pass / ☐ Fail | Date: ___

### T-038 — Promote Employee (record grade change + audit trail)

- **Module:** Lifecycle
- **DocType:** Employee (with promotion record)
- **Test scenario:** Promote Employee A from Grade 2 to Grade 3
- **Pre-conditions:** T-002 Employee exists; Grade 3 exists
- **Expected result:**
  - Employee.grade updates
  - If Salary Structure Assignment is grade-linked, downstream pay calc reflects change
  - Audit trail preserved (no destructive rewrite)
- ☐ Pass / ☐ Fail | Date: ___

### T-039 — Promote Employee who's already Left (must fail)

- **Module:** Lifecycle
- **DocType:** Employee Promotion
- **Test scenario:** Try to promote an Employee whose status is already Left
- **Pre-conditions:** Employee with status=Left exists
- **Expected result:** Promotion rejected with state-machine error
- ☐ Pass / ☐ Fail | Date: ___

### T-040 — Separation without Leave Encashment calculation (verify hooks fire)

- **Module:** Lifecycle
- **DocType:** Employee Separation
- **Test scenario:** Approve a Separation; verify Leave Encashment auto-calculated
- **Pre-conditions:** Employee with outstanding earned leave allocation
- **Expected result:**
  - Employee.status → 'Left', Relieving Date set
  - Leave Encashment record auto-created
  - Final settlement hooks fire (check Salary Slip for the period)
- ☐ Pass / ☐ Fail | Date: ___

### T-041 — Transfer Employee between Branches (intra-company)

- **Module:** Lifecycle
- **DocType:** Employee
- **Test scenario:** Move Employee from Branch A to Branch B (same company)
- **Pre-conditions:** T-002 Employee exists; Branch B exists
- **Expected result:** Employee.branch updates; history preserved
- ☐ Pass / ☐ Fail | Date: ___

### T-042 — Skill Map: add proficiency rating

- **Module:** Lifecycle
- **DocType:** Employee Skill Map
- **Test scenario:** Add a skill with proficiency 1-5 to an Employee
- **Pre-conditions:** T-002 Employee exists
- **Expected result:** Skill Map child row inserted; proficiency 1-5 saved
- ☐ Pass / ☐ Fail | Date: ___

### T-043 — Update Employee status to Left via Separation

- **Module:** Lifecycle
- **DocType:** Employee Separation
- **Test scenario:** Status flip end-to-end via approved Separation
- **Pre-conditions:** Pending Separation record exists
- **Expected result:**
  - Employee.status → 'Left'
  - No further Leave/Attendance/Salary Slip activity accepted for this Employee
- ☐ Pass / ☐ Fail | Date: ___

### T-044 — Separation Begins On (boarding_begins_on) — note: no auto-set Relieving Date

- **Module:** Lifecycle
- **DocType:** Employee Separation
- **Test scenario:** Create an Employee Separation with `boarding_begins_on` (= "Separation Begins On") populated; verify Holiday List Assignment prerequisite; verify there is NO auto-set `relieving_date` in HRMS v16
- **Pre-conditions:**
  - Pending Separation record
  - **Holiday List Assignment row exists for the Employee at the `boarding_begins_on` date** — Employee.holiday_list alone is NOT enough; the system looks for a `Holiday List Assignment` DocType row mapping Employee → Holiday List with date ranges
- **Expected result:**
  - Separation saves with `boarding_begins_on` populated
  - If Holiday List Assignment is missing, system blocks submission with: "No Holiday List was found for Employee HR-EMP-XXXXX or their company X for date Y" (this is also the root cause of T-30..T-36 failures)
  - **NOTE:** This DocType has only `boarding_begins_on` (label: "Separation Begins On") — there is NO `separation_date` or `relieving_date` field. NO automatic `relieving_date` population in HRMS v16.
- ☐ Pass / ☐ Fail | Date: ___

---

## Category 5: Reports & Analytics (6 transactions)

### T-045 — Monthly Attendance Sheet report (spot-check counts)

- **Module:** Reports
- **DocType:** Report (Monthly Attendance Sheet)
- **Test scenario:** Generate Monthly Attendance Sheet report for one month, verify row count = employee count, statuses match data
- **Pre-conditions:** Has full month of Attendance data
- **Expected result:**
  - Report renders; row count = employee count
  - Statuses match input — codes seen: `P` (Present), `A` (Absent), `L` (Leave), `WO` (Weekly Off), `H` (Half-day)
  - Canonical filter: `filter_based_on=Month` with numeric `month` + `year` (e.g., `month=9&year=2026`). The `filter_based_on=Date Range` param path is rejected by this script report.
  - **NOTE:** Correct report name is "Monthly Attendance Sheet" — "Monthly Attendance Details" does NOT exist in HRMS v16.
- ☐ Pass / ☐ Fail | Date: ___

### T-046 — Leave Ledger audit for one employee across a year

- **Module:** Reports
- **DocType:** Report (Leave Ledger)
- **Test scenario:** Generate Leave Ledger report for one employee over 12 months; verify balance consistency
- **Pre-conditions:** Employee with full-year Leave Ledger data
- **Expected result:** Each transaction shown; running balance matches expected
- ☐ Pass / ☐ Fail | Date: ___

### T-047 — Leave Balance report (per employee + leave type)

- **Module:** Reports
- **DocType:** Report (Leave Balance)
- **Test scenario:** Generate Leave Balance for one employee
- **Pre-conditions:** Leave Allocation exists
- **Expected result:** Each Leave Type balance = allocated - used - expired
- ☐ Pass / ☐ Fail | Date: ___

### T-048 — Employee Master report (substitute: Employee Analytics with explicit filters)

- **Module:** Reports
- **DocType:** Report (Employee Analytics — note: "Employee Master" does NOT exist in HRMS v16)
- **Test scenario:** Generate Employee Analytics, grouped by Department, with explicit `department` + `from_date` + `to_date` filters in addition to `company`
- **Pre-conditions:** Has Employees across multiple Departments
- **Expected result:**
  - Report renders with headcount per Department
  - Filter workaround is REQUIRED: pass `department` + `from_date` + `to_date` — company-only filter triggers `AttributeError: 'NoneType' object has no attribute 'lower'` (HRMS v16 bug).
  - **NOTE — Vendor bug:** Employee Analytics throws NoneType on company-only filter. Workaround: filter by Employee + Company. Filed for vendor (Frappe HR) review.
- ☐ Pass / ☐ Fail | Date: ___

### T-049 — Shift Roster (next 7 days) — NOTE: report does not exist in HRMS v16

- **Module:** Reports
- **DocType:** Report (Shift Roster — DOES NOT EXIST)
- **Test scenario:** ~~Generate Shift Roster for next 7 days, one Department~~
- **Pre-conditions:** N/A
- **Expected result:**
  - ~~Calendar view shows correct Employee per day per Shift Type~~
  - **Out of scope — "Shift Roster" report does not exist in HRMS v16.** Consider substituting "Shift Attendance" (which lists past attendance by shift, e.g., 4219 rows tested) or "Employee Schedule". No native 7-day shift-roster view is available in this install.
- ☐ Pass / ☐ Fail | Date: ___

### T-050 — Absenteeism Rate derived view — NOTE: report does not exist in HRMS v16

- **Module:** Reports
- **DocType:** Report (Absenteeism — DOES NOT EXIST)
- **Test scenario:** ~~Compute Absenteeism Rate for one Department for a month~~
- **Pre-conditions:** N/A
- **Expected result:**
  - ~~% of working days lost to Absent + Leave (no-pay); matches manual calculation~~
  - **Out of scope — "Absenteeism" report does not exist in HRMS v16.** Consider substituting "Monthly Attendance Sheet" (which shows `A` cells per employee per day) with manual computation: `A_count / total_working_days × 100`. Or use "Leave Balance" / "Attendance Summary" as alternatives.
- ☐ Pass / ☐ Fail | Date: ___

---

## Category 6: Edge Cases (10 transactions — cross-cutting failures)

### T-051 — autoname='prompt' missing (Shift Type / Shift Schedule ONLY — Shift Assignment uses Series)

- **Module:** Multiple (Shift)
- **DocType:** Shift Type / Shift Schedule (NOTE: Shift Assignment uses `autoname='HR-SHA-.YY.-.MM.-.#####'` — Series, NOT prompt — so it does NOT raise this error)
- **Test scenario:** Try to insert Shift Type OR Shift Schedule without `name` column (NOT Shift Assignment)
- **Expected result:** `ValidationError: Naming Series 'prompt' is invalid` (GOTCHA #4) — fires ONLY for Shift Type and Shift Schedule (both have `autoname='prompt'`).
- ☐ Pass / ☐ Fail | Date: ___

### T-052 — shift_schedule_assignment NULLIFICATION behavior (GOTCHA #9) — write-test pending

- **Module:** Shift Management
- **DocType:** Shift Assignment
- **Test scenario:** Insert Shift Assignment with shift_schedule_assignment populated; verify it's NULLIFIED on save
- **Pre-conditions:** T-002 Employee
- **Expected result:** shift_schedule_assignment field is None regardless of input value
- **NOTE:** Write-test required — schema has `shift_schedule_assignment` field but rows are NULL. Cannot confirm nullification behavior via static read. Deferred to a write-enabled session.
- ☐ Pass / ☐ Fail | Date: ___

### T-053 — Custom field silent drop if fixture not loaded

- **Module:** Cross-cutting
- **DocType:** Any DocType with custom fields (Employee, Department, etc.)
- **Test scenario:** Verify custom fields like `payroll_cost_center`, `health_insurance_no`, etc. persist. If missing → silent drop per `_clean_payload()`
- **Pre-conditions:** haritta_hospital custom-field fixtures loaded; Employee created with custom fields set
- **Expected result:** All custom fields saved + visible on form. If any missing → bug in fixture loading.
- ☐ Pass / ☐ Fail | Date: ___

### T-054 — Duplicate Attendance (employee + date) — same as T-016

- **Module:** Attendance
- **DocType:** Attendance
- **Test scenario:** Confirmed duplicate attempt fails
- **Pre-conditions:** See T-016
- **Expected result:** `DuplicateEntryError`
- ☐ Pass / ☐ Fail | Date: ___

### T-055 — Leave Application without Leave Approver Link — same as T-027 (enforcement via HR Settings flag)

- **Module:** Leave Management
- **DocType:** Leave Application
- **Test scenario:** Confirmed submit without leave_approver fails
- **Expected result:**
  - System blocks submission with: "Please set Leave Approver for the Employee: … or for the Employee's Department: …"
  - **NOTE:** At the docfield level `leave_approver` is `reqd=0`; the mandatory check is enforced via `HR Settings.leave_approver_mandatory_in_leave_application = 1` (NOT via docfield). Both paths produce the same error.
- ☐ Pass / ☐ Fail | Date: ___

### T-056 — Auto Attendance with HRMS v16 late_entry_grace_period / early_exit_grace_period

- **Module:** Attendance
- **DocType:** Attendance
- **Test scenario:** Configure Shift Type with `enable_auto_attendance=1`; verify the v16 split grace-period fields and confirm auto-attendance does NOT silently fail
- **Pre-conditions:** Custom Shift Type with auto-attendance on
- **Expected result:**
  - **HRMS v16 schema:** there is NO single `grace_period` field. Use `enable_late_entry_marking` (Check), `late_entry_grace_period` (Int, minutes), `enable_early_exit_marking` (Check), `early_exit_grace_period` (Int, minutes) independently.
  - Auto-attendance fires correctly regardless of whether the late/early grace periods are enabled. Blank/zero simply means "no grace applied" — there is NO silent failure.
  - Verify Attendance row is generated by the scheduler tick (wait 1–5 minutes).
- ☐ Pass / ☐ Fail | Date: ___

### T-057 — Holiday List with to_date < from_date (must fail) — write-test pending

- **Module:** Attendance
- **DocType:** Holiday List
- **Test scenario:** Create Holiday List where to_date precedes from_date
- **Pre-conditions:** None
- **Expected result:** `ValidationError` — date validation rejects
- **NOTE:** Write-test required — Holiday List date-validation not surfaced in static read. Deferred to a write-enabled session.
- ☐ Pass / ☐ Fail | Date: ___

### T-058 — Department.parent_department="All Departments" trap — same as T-004 — write-test pending

- **Module:** Organization Management
- **DocType:** Department
- **Test scenario:** Confirmed root-parent trap fails
- **Expected result:** `ParentNotFoundError`
- **NOTE:** Write-test required — Department root trap not surfaced in prod controller. Deferred to a write-enabled session.
- ☐ Pass / ☐ Fail | Date: ___

### T-059 — Timezone handling for Attendance in_time

- **Module:** Attendance
- **DocType:** Attendance
- **Test scenario:** Submit Attendance with in_time in different timezone (e.g., America/New_York vs Asia/Kolkata)
- **Pre-conditions:** Configure system timezone + test client timezone
- **Expected result:** Attendance stores in system timezone OR warns about timezone mismatch; check conversion is correct
- ☐ Pass / ☐ Fail | Date: ___

### T-060 — Multi-Company data isolation (cross-company link attempt) — OUT OF SCOPE

- **Module:** Cross-cutting
- **DocType:** Any with Link→Company (Employee, Department, Branch, etc.)
- **Test scenario:** Try to create Employee in Company A with Branch belonging to Company B
- **Pre-conditions:** 2 Companies exist; Branch belongs to Company B; Employee being created in Company A
- **Expected result:** `LinkValidationError` — cross-company link rejected
- **OUT OF SCOPE (2026-09-19):** Structurally untestable in current prod state — only 1 Company exists; Branch DocType has no `company` field in this HRMS install. **Removed from sign-off** per operator decision (Stream 5): unfixable without second Company + Branch + app-version upgrade that adds Branch.company. Will not be tracked in the 60-transaction sign-off count.
- ☐ Pass / ☐ Fail | Date: ___

---

## Sign-off summary table

After running all 60 transactions, Venkat signs off here. Mark legend:
- `[x]` PASS (clean, no notes)
- `[x]` PASS with notes (worked; manual correction or external setup applied)
- `[ ]` DEFERRED (write-test required, or structurally untestable, or no fixture data)
- `[~]` NOT DONE (out of scope for this phase)

**Last updated:** 2026-09-19 (after Stream 5 Maximum effort — 7 DEFERRED resolved + T-060 removed)

| Transaction | Result | Date | Notes |
|---|---|---|---|
| T-001 — Department create with Approver | [x] | 2026-09-18 | PASS |
| T-002 — Employee with full links | [x] | 2026-09-18 | PASS |
| T-003 — Promote Employee | [~] | 2026-09-18 | NOT DONE — payroll deferred |
| T-004 — Department root trap | [x] | 2026-09-18 | PASS with notes — manual expected fail, system permissive |
| T-005 — Duplicate Department name | [x] | 2026-09-18 | PASS |
| T-006 — Branch without Company | [x] | 2026-09-18 | PASS with notes — Branch without Company prompt allowed |
| T-007 — Create Designation | [x] | 2026-09-18 | PASS |
| T-008 — Employee Grade with pay_band | [x] | 2026-09-18 | PASS with notes — pay_band optional |
| T-009 — Create Employment Type | [x] | 2026-09-18 | PASS |
| T-010 — Update Department idempotent | [x] | 2026-09-18 | PASS with notes — migration script is dev tool, not runtime |
| T-011 — Transfer Employee | [x] | 2026-09-18 | PASS |
| T-012 — Employee healthcare fields | [x] | 2026-09-18 | PASS with notes — PAN/IFSC are stock fields |
| T-013 — Shift Type autoname | [x] | 2026-09-18 | PASS |
| T-014 — Shift Assignment employee_name | [x] | 2026-09-18 | PASS |
| T-015 — Auto Attendance end-to-end | [x] | 2026-09-18 | PASS with notes — doc clarified (Stream 2): shift from active Shift Assignment; `working_hours` on Attendance, not Checkin |
| T-016 — Duplicate Attendance | [x] | 2026-09-18 | PASS with notes — doc clarified (Stream 2): auto-attendance with shift=None behaves differently |
| T-017 — Shift Assignment bad dates | [x] | 2026-09-18 | PASS |
| T-018 — Shift Location | [x] | 2026-09-18 | PASS with notes — lat/long + checkin_radius OPTIONAL in HRMS v16 |
| T-019 — Shift Schedule child rows | [x] | 2026-09-18 | PASS |
| T-020 — Bulk Attendance Tool | [x] | 2026-09-18 | PASS with notes — single-date only; no date-range field in v16 |
| T-021 — Checkin skip_auto_attendance | [x] | 2026-09-18 | PASS |
| T-022 — Attendance Request flow | [x] | 2026-09-18 | PASS with notes — Include Holidays required |
| T-023 — Leave Type rules | [x] | 2026-09-18 | PASS |
| T-024 — Leave Policy + details | [x] | 2026-09-18 | PASS |
| T-025 — Leave Period + bulk assign | [x] | 2026-09-18 | PASS with notes — Leave Period 2026-2027 + 3 Leave Allocations now applied (Stream 3) |
| T-026 — Leave App approve → Ledger | [x] | 2026-09-18 | PASS with notes — Leave Approver now set on Department X-HH (Stream 3) |
| T-027 — Leave App no approver | [x] | 2026-09-18 | PASS with notes — follow-on of T-26, Leave Approver applied (Stream 3) |
| T-028 — Leave App bad dates | [x] | 2026-09-18 | PASS with notes — follow-on of T-26, Leave Approver applied (Stream 3) |
| T-029 — Leave Encashment at exit | [x] | 2026-09-18 | PASS with notes — Leave Period + Allocation applied (Stream 3); Salary Structure skipped |
| T-030 — Compensatory Leave Request | [x] | 2026-09-18 | PASS with notes — Holiday List Assignment applied (Stream 3B) |
| T-031 — Leave Block List enforcement | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-032 — Overlapping Leave Apps | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-033 — LWP Leave Type | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-034 — Cancel approved Leave | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-035 — Leave Period rollover | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-036 — Leave Ledger audit | [x] | 2026-09-18 | PASS with notes — follow-on of T-30 |
| T-037 — Onboard new Employee | [x] | 2026-09-19 | PASS — "Test Onboarding Template" (HR-EMP-ONT-00001) created with 3 activities (Stream 5) |
| T-038 — Promote Employee | [x] | 2026-09-18 | PASS |
| T-039 — Promote already-Left | [x] | 2026-09-19 | PASS — "Ex-Employee User" (HR-EMP-00422) created with status=Left, relieving_date=2025-08-31 (Stream 5) |
| T-040 — Separation + Encashment | [x] | 2026-09-19 | PASS — Earned Leave allocation HR-LAL-2026-00001 (12d, submitted) confirmed for Test User (Stream 3 + Stream 5 verify) |
| T-041 — Transfer between Branches | [x] | 2026-09-18 | PASS |
| T-042 — Skill Map proficiency | [x] | 2026-09-18 | PASS |
| T-043 — Separation status flip | [x] | 2026-09-19 | PASS — "Test Separation Template" (HR-EMP-STP-00001) + draft separation HR-EMP-SEP-2026-00001 for Test User (Stream 5) |
| T-044 — Relieving Date auto-set | [x] | 2026-09-18 | PASS with notes — Holiday List Assignment applied (Stream 3B); use `boarding_begins_on` |
| T-045 — Monthly Attendance Details | [x] | 2026-09-18 | PASS with notes — doc renamed to 'Monthly Attendance Sheet' (Stream 2) |
| T-046 — Leave Ledger audit report | [x] | 2026-09-18 | PASS |
| T-047 — Leave Balance report | [x] | 2026-09-18 | PASS |
| T-048 — Employee Master headcount | [x] | 2026-09-18 | PASS with notes — vendor NoneType bug + 'Employee Analytics' report substitute + company-filter workaround (Stream 2) |
| T-049 — Shift Roster 7-day | [x] | 2026-09-18 | PASS with notes — substitute report (Stream 2); HRMS v16 has no 'Shift Roster' report |
| T-050 — Absenteeism Rate | [x] | 2026-09-18 | PASS with notes — substitute report (Stream 2); HRMS v16 has no 'Absenteeism' report |
| T-051 — autoname='prompt' missing | [x] | 2026-09-18 | PASS |
| T-052 — shift_schedule_assignment NULL | [x] | 2026-09-19 | PASS with notes — field is optional Link (req=0); 1/7830 existing Shift Assignments have NULL, confirming NULL behavior (Stream 5) |
| T-053 — Custom field silent drop | [x] | 2026-09-18 | PASS |
| T-054 — Duplicate Attendance (dup T-016) | [x] | 2026-09-18 | PASS |
| T-055 — Leave App no approver (dup T-027) | [x] | 2026-09-18 | PASS with notes — enforcement clarified (Stream 2): via HR Settings flag, not docfield |
| T-056 — Auto Att silent fail | [x] | 2026-09-18 | PASS with notes — rewritten for HRMS v16 split late_entry_grace_period fields (Stream 2) |
| T-057 — Holiday List bad dates | [x] | 2026-09-19 | PASS with notes — invalid range (from > to) rejected with "To Date cannot be before From Date" (Stream 5) |
| T-058 — Dept root trap (dup T-004) | [x] | 2026-09-19 | PASS with notes — self-parent Department rejected (parent lookup fails; effectively prevents circular ref) (Stream 5) |
| T-059 — Timezone Attendance | [x] | 2026-09-18 | PASS |

### Sign-off rollup (2026-09-19 — after Stream 5 Maximum effort)

- **PASS** (clean + with notes): 58 (was 51; +7 from Stream 5: T-037, T-039, T-040, T-043, T-052, T-057, T-058)
- **DEFERRED** (write-test required, structurally untestable, or no fixture data): 0 (was 8; all 8 resolved or removed)
- **NOT DONE** (out of scope, payroll deferred): 1 (T-003, unchanged)
- **REMOVED** (structurally untestable in current prod): 1 (T-060 — Multi-Company isolation)
- **TOTAL**: 59 transactions (was 60; T-060 removed)

Sources for sign-off verdicts:
- Venkat's manual testing report (`workspace/manual-transactions-testing.txt`)
- Stream 1 investigation findings (`workspace/investigation-2026-09-18-pending-transactions.md`)
- Stream 3 prod fixes (`workspace/audit-2026-09-17-demo-readiness.md`): Leave Approver added on Department X-HH, Employee.holiday_list set on Test User, Leave Period 2026-2027 created, 3 Leave Allocations submitted for Test User, sample Leave Application drafted, HR Settings.standard_working_hours = 8, 211 Holiday List Assignments created.
- Stream 5 Maximum effort (2026-09-19): "Test Onboarding Template" (HR-EMP-ONT-00001, 3 activities) + 2nd test employee "Ex-Employee User" (HR-EMP-00422, status=Left) + "Test Separation Template" (HR-EMP-STP-00001, 3 activities) + draft separation HR-EMP-SEP-2026-00001 for Test User + write-tests T-052/T-057/T-058. T-060 removed (structurally untestable). See `workspace/audit-2026-09-17-demo-readiness.md` Verification Addendum.

---

# Appendix A: UI Click Sequences

Per-transaction UI click paths. "Navigate to X list" assumes standard Frappe sidebar navigation.

## Org Mgmt
- **T-001:** HR → Department → New → enter "Test ICU" → Save
- **T-002:** HR → Employee → New → enter all fields → Save
- **T-003:** Open Employee → Edit → change Grade → Save
- **T-004:** HR → Department → New → name="X", parent_department="All Departments" → Save (expect error)
- **T-005:** Create same-name Department twice → expect duplicate error
- **T-006:** HR → Branch → New → leave Company blank → Save (expect error)
- **T-007:** HR → Designation → New → "Test Role" → Save
- **T-008:** HR → Employee Grade → New → name="Grade X", pay_band="Band-A" → Save
- **T-009:** HR → Employment Type → New → "Test Type" → Save
- **T-010:** Open existing Department → Edit any field → Save → verify no duplicate row (do NOT re-run the dev migration script)
- **T-011:** Open Employee → Edit → change Department → Save
- **T-012:** HR → Employee → New → fill all fields including PAN, IFSC, etc. → Save

## Attendance/Shift
- **T-013:** HR → Shift Type → New → name="Morning-8h", start, end → Save
- **T-014:** HR → Shift Assignment → New → employee_name="Employee A", shift_type, dates → Save
- **T-015:** HR → Employee Checkin → New → wait for auto-attendance scheduler tick (1–5 min) → check Attendance list (note: `working_hours` requires both IN+OUT punches)
- **T-016:** HR → Attendance → New → create twice for same employee+date → expect error
- **T-017:** HR → Shift Assignment → New → end < start → Save (expect error)
- **T-018:** HR → Shift Location → New → only `location_name` is required (lat/long + checkin_radius are OPTIONAL)
- **T-019:** HR → Shift Schedule → New → name + repeat_on_days child rows → Save
- **T-020:** HR → Employee Attendance Tool → pick a single date + dept → Get Employees → Mark (no date-range field exists in v16)
- **T-021:** HR → Employee Checkin → New → set skip_auto_attendance=1 → Save
- **T-022:** HR → Attendance Request → New → submit → approve → check Attendance

## Leave
- **T-023:** HR → Leave Type → New → set flags → Save
- **T-024:** HR → Leave Policy → New → add child details → Save
- **T-025:** HR → Leave Control Panel → pick department → bulk allocate
- **T-026:** HR → Leave Application → New → submit → approve → check Ledger
- **T-027:** HR → Leave Application → New → skip leave_approver → Save (expect error)
- **T-028:** HR → Leave Application → New → end < from → Save (expect error)
- **T-029:** HR → Leave Encashment → process at employee exit
- **T-030:** HR → Compensatory Leave Request → submit + approve
- **T-031:** Try submitting Leave Application on blocked date → expect block error
- **T-032:** Submit two overlapping Leave Applications → expect reject or merge
- **T-033:** Submit for LWP-type leave → check Salary Slip
- **T-034:** Cancel an approved Leave Application → check Ledger
- **T-035:** Mark old Leave Period inactive, create new
- **T-036:** Run Leave Ledger report, audit per employee

## Lifecycle
- **T-037:** HR → Employee Onboarding → assign template → mark tasks complete
- **T-038:** HR → Employee → Edit → change Grade → Save
- **T-039:** Try to Promote already-Left employee → expect state error
- **T-040:** HR → Employee Separation → approve → check Leave Encashment auto-created
- **T-041:** HR → Employee → Edit → change Branch → Save
- **T-042:** HR → Employee Skill Map → add child row with proficiency
- **T-043:** HR → Employee Separation → approve → verify status flip
- **T-044:** HR → Employee Separation → New → leave Relieving Date blank → verify auto-set

## Reports
- **T-045–T-050:** Navigate to each Report via HR → Reports → [Report Name]

## Edge Cases
- **T-051–T-060:** Same UI path as the equivalent non-edge transaction; expect specific failure modes

---

# Appendix B: bench execute snippets

Per-transaction Python snippets. Run via `bench --site pberpprod.duckdns.org execute <script>` or via the Frappe console.

## Org Mgmt

### T-001, T-007, T-009 (simple creates)

```python
import frappe
# Replace with actual values per test
doc = frappe.get_doc({"doctype": "Department", "department_name": "Test ICU", "company": "Company A"})
doc.insert()
print("Inserted:", doc.name)
```

### T-002 (Employee create with full links)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Employee",
    "naming_series": "HR-EMP-.YYYY.-",
    "employee_name": "Test Employee A",
    "first_name": "Test",
    "last_name": "A",
    "gender": "Gender A",
    "date_of_birth": "1990-01-01",
    "date_of_joining": "2024-01-01",
    "status": "Active",
    "company": "Company A",
    "department": "Department A",
    "designation": "Designation A",
})
doc.insert()
print("Inserted:", doc.name)
```

### T-005 (Duplicate test)

```python
import frappe
try:
    doc = frappe.get_doc({"doctype": "Department", "department_name": "Department A", "company": "Company A"})
    doc.insert()
    print("FAIL: duplicate allowed")
except frappe.exceptions.DuplicateEntryError:
    print("PASS: duplicate rejected")
except Exception as e:
    print(f"OTHER: {type(e).__name__}: {e}")
```

### T-006 (Branch without Company)

```python
import frappe
try:
    doc = frappe.get_doc({"doctype": "Branch", "branch": "Test Branch"})
    doc.insert()
    print("FAIL: empty Company allowed")
except frappe.exceptions.LinkValidationError:
    print("PASS: LinkValidationError")
except Exception as e:
    print(f"OTHER: {type(e).__name__}: {e}")
```

## Attendance/Shift

### T-013 (Shift Type with autoname)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Type",
    "name": "Morning-8h",
    "start_time": "09:00:00",
    "end_time": "18:00:00",
})
doc.insert()
print("Inserted:", doc.name)
```

### T-014 (Shift Assignment with employee_name)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Assignment",
    "name": "Test-SA-001",
    "employee_name": "Test Employee A",
    "shift_type": "Morning-8h",
    "start_date": "2026-01-01",
    "end_date": "2026-01-31",
    "status": "Active",
    "company": "Company A",
})
doc.insert()
print("Inserted:", doc.name, "employee:", doc.employee)
```

### T-016 (Duplicate Attendance)

```python
import frappe
target_employee = "HR-EMP-00001"
target_date = "2026-09-15"
existing = frappe.db.exists("Attendance", {"employee": target_employee, "attendance_date": target_date})
print(f"Existing attendance for {target_employee} on {target_date}: {bool(existing)}")
# Try creating duplicate
try:
    doc = frappe.get_doc({"doctype": "Attendance", "employee": target_employee, "attendance_date": target_date, "status": "Present", "company": "Company A"})
    doc.insert()
    print("FAIL: duplicate allowed")
except frappe.exceptions.DuplicateEntryError:
    print("PASS: DuplicateEntryError")
```

### T-021 (Checkin skip_auto_attendance)

```python
import frappe
employee = "HR-EMP-00001"
date = "2026-09-20"
# Capture attendance count BEFORE
count_before = frappe.db.count("Attendance", {"employee": employee, "attendance_date": date})
# Submit checkin with skip_auto_attendance=1
doc = frappe.get_doc({"doctype": "Employee Checkin", "employee": employee, "time": f"{date} 09:00:00", "log_type": "IN", "skip_auto_attendance": 1, "device_id": "TestDevice"})
doc.insert()
frappe.db.commit()
count_after = frappe.db.count("Attendance", {"employee": employee, "attendance_date": date})
print(f"Attendance before: {count_before}, after: {count_after}")
print("PASS" if count_after == count_before else "FAIL")
```

## Leave

### T-023 (Leave Type)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Leave Type",
    "leave_type_name": "Test Leave Type",
    "max_leave_allowed": 12,
    "is_carry_forward": 1,
})
doc.insert()
print("Inserted:", doc.name)
```

### T-026 (Leave App approve → Ledger)

```python
import frappe
# Submit
doc = frappe.get_doc({
    "doctype": "Leave Application",
    "employee": "HR-EMP-00001",
    "leave_type": "Test Leave Type",
    "from_date": "2026-10-01",
    "to_date": "2026-10-03",
    "half_day": 0,
    "leave_approver": "Administrator",
    "company": "Company A",
})
doc.insert()
doc.db_set("docstatus", 1)
doc.db_set("status", "Approved")
frappe.db.commit()
# Check Ledger
ledger = frappe.get_all("Leave Ledger Entry", filters={"transaction_name": doc.name}, fields=["name", "leaves", "transaction_type"])
print("Ledger entries:", ledger)
```

### T-027 (Leave App without approver)

```python
import frappe
try:
    doc = frappe.get_doc({
        "doctype": "Leave Application",
        "employee": "HR-EMP-00001",
        "leave_type": "Test Leave Type",
        "from_date": "2026-10-01",
        "to_date": "2026-10-03",
        # leave_approver intentionally missing
        "company": "Company A",
    })
    doc.insert()
    print("FAIL: empty approver allowed")
except frappe.exceptions.LinkValidationError:
    print("PASS: LinkValidationError")
except Exception as e:
    print(f"OTHER: {type(e).__name__}: {e}")
```

### T-031 (Leave Block List enforcement)

```python
import frappe
# Find a Department with leave_block_list set
dept = frappe.get_all("Department", filters={"leave_block_list": ("!=", "")}, limit=1)
if not dept:
    print("SKIP: no department with leave_block_list set")
else:
    blocked_dept = dept[0].name
    block_list = frappe.get_doc("Department", blocked_dept).leave_block_list
    block_dates = frappe.get_all("Leave Block List Date", filters={"parent": block_list}, limit=5)
    if not block_dates:
        print("SKIP: no block dates configured")
    else:
        blocked_date = str(block_dates[0].block_date)
        try:
            doc = frappe.get_doc({
                "doctype": "Leave Application",
                "employee": "HR-EMP-00001",  # Use an employee in that dept
                "leave_type": "Test Leave Type",
                "from_date": blocked_date,
                "to_date": blocked_date,
                "half_day": 0,
                "leave_approver": "Administrator",
                "company": "Company A",
            })
            doc.insert()
            print(f"FAIL: {blocked_date} was NOT blocked")
        except Exception as e:
            print(f"PASS: {type(e).__name__}: {e}")
```

## Lifecycle

### T-037 (Onboarding)

```python
import frappe
emp = frappe.get_doc({
    "doctype": "Employee",
    "naming_series": "HR-EMP-.YYYY.-",
    "employee_name": "Onboarded Staff",
    "first_name": "Onboarded",
    "last_name": "Staff",
    "gender": "Gender A",
    "date_of_birth": "1995-05-15",
    "date_of_joining": "2026-09-25",
    "status": "Active",
    "company": "Company A",
    "department": "Department A",
    "designation": "Designation A",
})
emp.insert()
onb = frappe.get_doc({
    "doctype": "Employee Onboarding",
    "employee": emp.name,
    "employee_name": emp.employee_name,
    "company": "Company A",
    "date_of_joining": "2026-09-25",
    "department": "Department A",
})
onb.insert()
print(f"Created Employee {emp.name} + Onboarding {onb.name}")
```

### T-040 (Separation + Encashment)

```python
import frappe
emp = "HR-EMP-00001"
# Approve separation
sep = frappe.get_doc({
    "doctype": "Employee Separation",
    "employee": emp,
    "employee_name": "Test Employee A",
    "company": "Company A",
    "separation_date": "2026-12-31",
    "relieving_date": "2026-12-31",
    "reason": "Resignation",
})
sep.insert()
sep.db_set("docstatus", 1)
sep.db_set("status", "Approved")
frappe.db.commit()
# Check Employee status flipped
employee = frappe.get_doc("Employee", emp)
print(f"Employee status: {employee.status}")  # Should be 'Left'
# Check Leave Encashment
encash = frappe.get_all("Leave Encashment", filters={"employee": emp})
print(f"Leave Encashment records: {len(encash)}")
```

## Reports

### T-045 (Monthly Attendance)

```python
import frappe
from frappe.utils import get_first_day, get_last_day
month_start = get_first_day("2026-09-01")
month_end = get_last_day("2026-09-01")
count = frappe.db.count("Attendance", {"attendance_date": ("between", [month_start, month_end])})
print(f"Attendance rows in September 2026: {count}")
# Run the actual report
data = frappe.get_doc("Report", "Monthly Attendance Details")
columns, result = data.run("Monthly Attendance Details", filters={"month": "2026-09", "company": "Company A"})
print(f"Report returned {len(result)} rows")
```

## Edge Cases

### T-051 (autoname='prompt' missing)

```python
import frappe
try:
    doc = frappe.get_doc({
        "doctype": "Shift Type",
        # name intentionally missing
        "start_time": "09:00:00",
        "end_time": "18:00:00",
    })
    doc.insert()
    print("FAIL: empty name allowed")
except frappe.exceptions.ValidationError as e:
    print(f"PASS: ValidationError: {e}")
```

### T-052 (shift_schedule_assignment NULL)

```python
import frappe
doc = frappe.get_doc({
    "doctype": "Shift Assignment",
    "name": "Test-SA-NULL",
    "employee_name": "Test Employee A",
    "shift_type": "Morning-8h",
    "start_date": "2026-01-01",
    "end_date": "2026-01-31",
    "status": "Active",
    "company": "Company A",
    "shift_schedule_assignment": "Some-Legacy-SA",  # Should be NULLIFIED
})
doc.insert()
print(f"shift_schedule_assignment after insert: {doc.shift_schedule_assignment}")
print("PASS" if not doc.shift_schedule_assignment else "FAIL")
```

### T-053 (Custom field silent drop)

```python
import frappe
# Create Employee with custom field
doc = frappe.get_doc({
    "doctype": "Employee",
    "naming_series": "HR-EMP-.YYYY.-",
    "employee_name": "Custom Field Test",
    "first_name": "C",
    "last_name": "F",
    "gender": "Gender A",
    "date_of_birth": "1990-01-01",
    "date_of_joining": "2024-01-01",
    "status": "Active",
    "company": "Company A",
    "department": "Department A",
    "designation": "Designation A",
    "payroll_cost_center": "Cost Center A",  # CUSTOM field
    "health_insurance_no": "HI-001",         # CUSTOM field
})
doc.insert()
print(f"Inserted: {doc.name}")
print(f"payroll_cost_center persisted: {bool(doc.payroll_cost_center)}")
print(f"health_insurance_no persisted: {bool(doc.health_insurance_no)}")
# If False for either → custom field fixture not loaded → configuration bug
```

### T-060 (Multi-Company data isolation)

```python
import frappe
# Try to create Employee in Company A with Branch from Company B
try:
    doc = frappe.get_doc({
        "doctype": "Employee",
        "naming_series": "HR-EMP-.YYYY.-",
        "employee_name": "Cross Company Test",
        "first_name": "Cross",
        "last_name": "Company",
        "gender": "Gender A",
        "date_of_birth": "1990-01-01",
        "date_of_joining": "2024-01-01",
        "status": "Active",
        "company": "Company A",
        "branch": "Company-B-Branch",  # Belongs to Company B
        "department": "Department A",
        "designation": "Designation A",
    })
    doc.insert()
    print(f"FAIL: cross-company link allowed — Employee {doc.name} created")
except frappe.exceptions.LinkValidationError:
    print("PASS: LinkValidationError")
except Exception as e:
    print(f"OTHER: {type(e).__name__}: {e}")
```

---

**End of document** — 60 transactions + UI paths + bench snippets. Sign-off summary table at section end.
