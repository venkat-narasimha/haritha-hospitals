# Master-Data Templates Audit Report

**Date:** 2026-09-15
**Wave:** P5 — Data Templates Productionization (Wave 1)
**Scope:** All 15 master-data template pairs in `docs/client-onboarding/03-intake-workbook/01_master_data/`
**Reference:** `scripts/migrate_master_data.py` (Lesson #157 — 10 gotchas documented inline)
**Constraint:** Generic examples only — no Haritha-specific data, no real employee names, no real counts

---

## Methodology

For each of the 15 DocType templates (paired `.csv` + `.md`), the audit verified:

1. **CSV header completeness** — does the template include every field the migration script actually writes (`_clean_payload()` passes all non-metadata fields through, with special handling for `Company`, `Shift Schedule`, `Shift Request`, `Shift Assignment`)?
2. **CSV example values** — are they generic stand-ins, not real Haritha data?
3. **Markdown notes coverage** — do the docs surface the gotchas the migration script documents inline (gotchas #1–#10 in `migrate_master_data.py`)?
4. **Field type accuracy** — is each column's declared type (Data / Link / Date / Check / Select / Int / Float / Table) consistent with the DocType's schema?

Status legend:
- ✅ — no change needed (template reflects current migration logic)
- ⚠️ — fixed during this audit (summary of the fix below)
- ❌ — no template exists (NOT APPLICABLE this wave — all 15 already have templates)

---

## Per-Template Findings

### 01 — Department — ⚠️ fixed
**DocType:** `Department` | **GOTCHAs touched:** #5, #10
- CSV: header is complete against `_clean_payload()` pass-through. `is_group` is correctly typed as Check. `parent_department` is correctly typed as Link. No new columns required.
- MD: was missing migration notes. **Fixed:** added "Migration notes" section covering (a) skip of `parent_department="All Departments"` rows (GOTCHA #5), (b) Department Approver pre-seed for Shift Request validation (GOTCHA #10), (c) upsert semantics for re-runs, (d) order dependency on Department before downstream Link fields.
- Sample data already generic (Cardiology, Clinical Services, Main Block, etc.).

### 02 — Designation — ✅ no change needed
**DocType:** `Designation` | **GOTCHAs touched:** none
- Script treats Designation as a standard upsert; no special gotchas apply. CSV columns cover `name`, `description`, custom fields. MD tables align with the schema.
- Sample data already generic (Senior Consultant, MBBS, MD, etc.).

### 03 — Employment Type — ✅ no change needed
**DocType:** `Employment Type` | **GOTCHAs touched:** none
- Script uses standard upsert; `name` is correctly identified as the autoname source field in the MD. Standard hospital library already documented in the MD.
- Sample data already generic (Full-time, Part-time, Contract, Locum, Visiting Consultant, Internship, Probation).

### 04 — Employee Grade — ✅ no change needed
**DocType:** `Employee Grade` | **GOTCHAs touched:** none
- Standard upsert path in the script. CSV uses `grade_name` (correct autoname field). MD correctly identifies the pay-band mapping to Leave Policy.
- Sample data already generic (A2, INR, Clinical-Band-2, etc.).

### 05 — Branch — ✅ no change needed
**DocType:** `Branch` | **GOTCHAs touched:** none
- Standard upsert path. CSV + MD cover `branch`, `company`, custom `branch_code`, `branch_type`, `nabh_accredited`, `bed_count`. Correct Link to `Company`.
- Sample data already generic (Main Hospital, State A, City A, etc.).

### 06 — Holiday List — ✅ no change needed
**DocType:** `Holiday List` (+ child `Holiday`) | **GOTCHAs touched:** none
- Standard upsert path. CSV correctly distinguishes parent fields (`holiday_list_name`, `from_date`, `to_date`, `weekly_off`) from child-table rows (`holiday_date`, `description`). MD notes the weekly-off helper integration.
- Sample data already generic (State A Holiday Calendar 2026, Sunday weekly off, Republic Day, etc.).

### 07 — Shift Type — ⚠️ fixed
**DocType:** `Shift Type` | **GOTCHAs touched:** #4, #6
- CSV: header is complete against the controller's field list. All color / grace / threshold fields covered.
- MD: was missing the autoname contract note. **Fixed:** added "Migration notes" section covering (a) autoname='prompt' requires explicit `name` (GOTCHA #4), (b) Shift Type must migrate before Employee because `default_shift` is a Link (GOTCHA #6), (c) upsert semantics for re-runs, (d) `enable_auto_attendance` + `process_attendance_after` scheduler dependency.
- Sample data already generic (Morning-8h, Evening-8h, OPD-Morning, etc.).

### 08 — Shift Location — ⚠️ fixed
**DocType:** `Shift Location` | **GOTCHAs touched:** #4, #9
- CSV: header is complete against the controller's field list. `latitude`, `longitude`, `checkin_radius`, `zone_type`, `floor` all correctly typed.
- MD: was missing migration notes. **Fixed:** added "Migration notes" section covering (a) autoname=`field:location_name` explicit name requirement (GOTCHA #4, `PROMPT_AUTONAME_DOCTYPES`), (b) the `_ensure_shift_location("City A")` pre-create in `run()` (GOTCHA #9) and what to do if the client uses a different canonical name, (c) upsert behaviour for coordinate changes, (d) out-of-scope fields not auto-populated by the script.
- Sample data already generic (Main Hospital - ICU, etc.).

### 09 — Shift Schedule — ⚠️ fixed
**DocType:** `Shift Schedule` (+ child `Assignment Rule Day`) | **GOTCHAs touched:** #8
- CSV: header correctly distinguishes parent fields from the two child tables (`repeat_on_days` and `shift_assignments`). At-least-one-day requirement is documented in the MD.
- MD: was missing migration notes. **Fixed:** added "Migration notes" section covering (a) autoname='prompt' explicit `name` requirement (GOTCHA #8 part A), (b) `repeat_on_days` child rows dropped by `fields=["*"]` and re-appended via `doc.append()` (GOTCHA #8 part B), (c) re-runs wipe + re-append the child table, (d) the `shift_assignments` child is not generated by the migration, (e) `enable_auto_shift_schedule` does not auto-run during migration.
- Sample data already generic (ICU-Nurse-Day-Rotation, etc.).

### 10 — Employee — ⚠️ fixed
**DocType:** `Employee` | **GOTCHAs touched:** #6, #7
- CSV: comprehensive coverage of standard + custom + contact + emergency fields. Field types correctly declared (Date, Link, Select, Data, Small Text, Table).
- MD: was missing migration notes. **Fixed:** added "Migration notes" section covering (a) Gender + Shift Type must migrate first because `default_shift` and `gender` are Link fields (GOTCHA #6), (b) Employee ID remap by `employee_name` (GOTCHA #7) and the join-key requirement, (c) upsert by `name` not `employee_number`, (d) custom fields pass through `_clean_payload()`, (e) date validation, (f) `status` default behaviour.
- Sample data already generic (Aarav Kumar Sharma, HRH-EMP-0001, BIO-12345, REG-A-0001, etc.).

### 11 — Leave Type — ✅ no change needed
**DocType:** `Leave Type` | **GOTCHAs touched:** none
- Standard upsert path. CSV covers `name`, `max_leave_allocation_allowed`, all earned/carry-forward/optional flags, encashment, compensatory. MD correctly identifies mutually exclusive flags.
- Sample data already generic (Casual Leave, Sick Leave, Maternity Leave, etc.).

### 12 — Leave Policy — ✅ no change needed
**DocType:** `Leave Policy` (+ child `Leave Policy Detail`) | **GOTCHAs touched:** none
- Standard upsert path. CSV correctly distinguishes parent `title` from child `leave_type` + `annual_allocation`. MD maps policies to Employee Grade.
- Sample data already generic (Grade A2 Policy, Casual Leave, 12 allocations, etc.).

### 13 — Leave Period — ✅ no change needed
**DocType:** `Leave Period` | **GOTCHAs touched:** none
- Standard upsert path. CSV + MD correctly identify the active-period constraint (one active per company).
- Sample data already generic (2026-01-01 to 2026-12-31, FY 2026, etc.).

### 14 — Leave Allocation — ✅ no change needed
**DocType:** `Leave Allocation` (submittable) | **GOTCHAs touched:** none
- Standard upsert path. CSV correctly identifies `employee`, `leave_type`, `from_date`, `to_date`, `new_leaves_allocated` as required. MD notes that bulk allocation should use Leave Policy auto-generation, not this sheet.
- Sample data already generic (Mid-year hire adjustment, Grade A2 Policy, etc.).

### 15 — Shift Assignment — ⚠️ fixed
**DocType:** `Shift Assignment` (submittable) | **GOTCHAs touched:** #7, #9
- CSV: was missing `name`, `employee_name`, `shift_request`, `shift_schedule_assignment` columns. **Fixed:** added all four columns with explicit documentation. `name` is required (autoname='prompt' contract), `employee_name` is required (prod→dev ID remap join key per GOTCHA #7), `shift_request` is optional Link preserved by script, `shift_schedule_assignment` is documented as NULLIFIED by script (GOTCHA #9) — leave blank.
- MD: was missing migration notes. **Fixed:** added "Migration notes" section covering (a) employee ID remap by `employee_name` (GOTCHA #7), (b) `shift_schedule_assignment` NULLIF (GOTCHA #9), (c) `shift_request` Link preservation depends on `Shift Request` migrating first, (d) `Shift Location` pre-create requirement (GOTCHA #9) and the `City A` canonical-name issue, (e) `docstatus` preserved from source, (f) upsert by `name` semantics for re-runs.
- Sample data already generic (HR-SHA-26-09-00001, Aarav Kumar Sharma, Morning-8h, etc.).

---

## Summary

| # | Template | Status | What changed |
|---|---|---|---|
| 01 | Department | ⚠️ fixed | MD gained "Migration notes" (gotchas #5, #10) |
| 02 | Designation | ✅ | – |
| 03 | Employment Type | ✅ | – |
| 04 | Employee Grade | ✅ | – |
| 05 | Branch | ✅ | – |
| 06 | Holiday List | ✅ | – |
| 07 | Shift Type | ⚠️ fixed | MD gained "Migration notes" (gotcha #4 + #6) |
| 08 | Shift Location | ⚠️ fixed | MD gained "Migration notes" (gotchas #4, #9) |
| 09 | Shift Schedule | ⚠️ fixed | MD gained "Migration notes" (gotcha #8) |
| 10 | Employee | ⚠️ fixed | MD gained "Migration notes" (gotchas #6, #7) |
| 11 | Leave Type | ✅ | – |
| 12 | Leave Policy | ✅ | – |
| 13 | Leave Period | ✅ | – |
| 14 | Leave Allocation | ✅ | – |
| 15 | Shift Assignment | ⚠️ fixed | MD gained "Migration notes" (gotchas #7, #9); CSV gained 4 columns |

**Totals:** 6 templates fixed, 9 unchanged. **Zero missing templates** (all 15 were present before this audit).

---

## Gotcha Coverage Matrix

Maps each inline gotcha in `migrate_master_data.py` to the template(s) that now document it.

| Gotcha | Title | Now documented in |
|---|---|---|
| #1 | `get_doc()` requires `doctype` key | (script-level only; no template change needed — client fills CSV, doesn't construct dicts) |
| #2 | Company default accounts depend on Account | (Company is configured in ERPNext directly, NOT a workbook template) |
| #3 | Account root nodes skipped | (Account is NOT a workbook template — system-generated only) |
| #4 | Prompt-autoname DocTypes | 07 Shift Type ✅, 08 Shift Location ✅, 09 Shift Schedule ✅, 15 Shift Assignment ✅ |
| #5 | Department / Item Group root-skip | 01 Department ✅ (Item Group also not a workbook template) |
| #6 | Employee requires Gender + Shift Type first | 07 Shift Type ✅, 10 Employee ✅ |
| #7 | Employee ID remap by `employee_name` | 10 Employee ✅, 15 Shift Assignment ✅ |
| #8 | Shift Schedule child table + autoname | 09 Shift Schedule ✅ |
| #9 | Shift Assignment out-of-scope Links + Shift Location pre-create | 08 Shift Location ✅, 15 Shift Assignment ✅ |
| #10 | Shift Request validate_approver + autoname series | 01 Department ✅ (Department Approver pre-seed documented) |

All 7 client-visible gotchas (#4–#10) are now surfaced in at least one template. Gotchas #1–#3 are script-internal and not client-facing.

---

## Caveats and Open Items for Wave 2+

1. **Custom-field schema drift.** Every "Healthcare-specific fields (custom)" section assumes the client has added the named custom fields to their DocType. If they have not, the migration script will silently drop those columns on insert because `_clean_payload()` only retains fields present in the source payload. Recommend a Wave 2 template that enumerates the 274 Custom Field / Property Setter fixtures the script expects.
2. **Account / Cost Center / Item Group / UOM / Item / Gender / Company.** These DocTypes are migrated by the script but do NOT have intake-workbook templates (Gender is auto-seeded by Frappe; the rest are system / accounting masters covered elsewhere). If the client needs to import custom UOMs or non-stock Item Groups, that's a Wave 2 ask.
3. **Holiday List `applicable_to`.** Marked as a custom field in template 06 — verify the client has added it to their DocType before bulk import, or the column will be silently discarded.
4. **`name` field on Shift Schedule, Shift Assignment, Shift Request.** The script handles autoname='prompt' transparently, but the templates only added `name` to template 15 (Shift Assignment). Wave 2 should add explicit `name` columns to 09 Shift Schedule and to the Shift Request template if/when one is created.
5. **`[your_app].scripts.generate_shift_assignments`.** Referenced in template 15's MD but does NOT exist yet (not in `scripts/`). Either Wave 2 generates it or the MD reference is removed.
6. **`scripts/fetch_master_data.py`.** Companion script referenced in the migration script's `USAGE` section but not present in `scripts/`. If the client needs to re-run the migration from a new prod dump, this script must be written first.
7. **`_ensure_shift_location("City A")` hard-code.** Documented in templates 08 and 15 as a caveat. Wave 2 could parameterize this via env var or move it to a config block in `migrate_master_data.py`.

---

## Verification Protocol

Run after committing:

```bash
# 1. Audit report file exists and is non-trivial
ls -la docs/client-onboarding/03-intake-workbook/AUDIT-REPORT.md

# 2. At least 15 ### sections (one per template)
grep -c '^### ' docs/client-onboarding/03-intake-workbook/AUDIT-REPORT.md

# 3. New commit present
git log --oneline -3

# 4. Working tree clean (only backup may remain)
git status
```

All four checks must pass before reporting completion.
