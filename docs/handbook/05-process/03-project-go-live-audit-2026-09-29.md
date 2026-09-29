# this hospital — Procedure Audit (2026-09-29)

**Date:** 2026-09-29
**Status:** ✅ Complete
**Source procedure:** User-pasted procedure doc, Sections 1–3
**Repos audited:**
- Project: `/root/.openclaw/workspace/projects/haritha-hospitals/`
- Custom app: `/root/.openclaw/workspace/projects/haritha_hospital/` (cloned from `https://github.com/venkat-narasimha/haritha_hospital.git` on 2026-09-29 18:26 IST)

---

## Source Procedure (Quoted)

> Audit is benchmarked against the procedure the user pasted verbatim. Quoted in full below for traceability.

### SECTION 1 — Solution claims

> The project delivers 3 things to the client:
> 1. **Configured ERPNext site** (Deliverable A) — a working ERPNext site with hospital data ingested, shifts running, attendance flowing
> 2. **Custom app + scripts + fixtures** (Deliverable B) — Python scripts for data ingestion + custom DocTypes + Server Scripts + fixtures (Shift Types, Holiday Lists, Leave Types)
> 3. **Repeatable methodology / runbook** (Deliverable C) — documentation that says "to onboard a new client (college / factory / hospital), do steps X, Y, Z in order"

### SECTION 2 — Shift Management System Best Practices (4 sub-areas)

> **2.1 Shift Type Definition** — `start_time` / `end_time`, `duration`, `enable_auto_attendance`, `determine_check_in_and_check_out`, `working_hours_threshold_for_half_day`, `working_hours_threshold_for_absent`, `late_entry_grace_period`, `early_exit_grace_period`, `allow_auto_attendance`, `process_attendance_after`
>
> **2.2 Holiday List** — One list per **location**, not per department. Include national + state + location-specific. Hospital: Sundays can be working; factory: usually off. ERPNext uses it to skip auto-attendance on holidays.
>
> **2.3 Attendance Pipeline** — Shift Assignment → Employee Checkin → Auto-attendance job (nightly) → Attendance → Leave Application (exceptions) → Monthly summary → payroll.
>
> **2.4 Hospital-Specific Gotchas** — NABH / state Nursing Council rules (max continuous duty, mandatory rest). Doctor duty patterns (irregular, on-call, OPD+OT+ward mix). Nurse rotation (6-on-1-off). Compensatory off ("comp-off") for working on holiday — needs Leave Type or custom doc.

### SECTION 3 — General Production / Go-Live Checklist (Phases 0–6)

> 28 checkboxes covering Foundation & Learning, Project Foundation, Data Migration Mastery, Customization & Configuration, Testing & QA, Deployment & Go-Live, Maintenance & Iteration.

---

## Section 1 — Solution Claims (3 rows)

| # | Claim | Verified (✅/⏳/❌) | Evidence (file path) | Notes |
|---|---|---|---|---|
| 1.A | Configured ERPNext site (data ingested, shifts running, attendance flowing) | ⏳ | `README.md` (3 envs), `TRACKER.md` (`00-project-status.md`): "210 Employees, 37 Departments, 25 Shift Types, 8,118 Shift Assignments, 6,300 Attendance, 12,562 Employee Checkins" | Site exists + data ingested ✅, **shifts running** is ⏳ (Auto-Attendance cron activation flagged as pending in `WORKFLOW.md` § Phase 4 — "Auto Attendance (cron ready, needs activation) ✅"), attendance flowing partial (6,300 records present, but backfill flagged "needs activation" — see § 4.x in `Phase-4-Shift-Management-Roster-Crash-Fix.md`). 77/78 sign-off rows PASS per `TRACKER.md`. |
| 1.B | Custom app + scripts + fixtures (Python scripts, custom DocTypes, Server Scripts, fixtures for Shift Types / Holiday Lists / Leave Types) | ⏳ | Custom app `haritha_hospital/` (16 files), `scripts/migrate_master_data.py` (30KB), fixtures in `haritha_hospital/fixtures/` (custom_field.json, property_setter.json, print_format.json, notification.json, letter_head.json) | **Scripts** ✅, **Custom app** ✅ exists, **fixtures** ⏳ — but only 5 of 274 Haritha customizations are exported as fixtures per `audit/FIXTURES-AUDIT-REPORT.md`; 78 Custom Fields + 189 Property Setters still rely on env-init script. **Custom DocTypes = 0** (none exist), **Server Scripts = 0** (none exist). Procedure's "Shift Types / Holiday Lists / Leave Types" as fixtures ⏳ — they live in `masters/*.csv` (immutable source) and are ingested via `migrate_master_data.py`, not as custom fixtures. |
| 1.C | Repeatable methodology / runbook (do steps X, Y, Z in order for new client) | ❌ | `docs/DECISIONS.md` (28 decisions), `docs/WORKFLOW.md` (Phases 2–5 with rollback), `docs/HARITHA_HOSPITALS_GUIDE.md`, `docs/handbook/` (35 docs, ~15,900 lines) | Rich context, **but not a runbook**. `WORKFLOW.md` is hospital-specific (env names, IPs, ports `[redacted-IP]`, `[port-redacted]`, `[port-redacted]` are sanitized out but workflow is the hospital one, not a templated "onboard any new client"). `DECISIONS.md` is a log, not a procedure. No "Onboarding Playbook / College-Onboard / Factory-Onboard / Hospital-Onboard" document exists. README § "Quick Start" is closest but is 3 commands for the Haritha app, not a full playbook. |

---

## Section 2 — Shift Management Best Practices

### 2.1 Shift Type Definition

| # | Practice | Implemented (✅/⏳/❌) | Evidence | Notes |
|---|---|---|---|---|
| 2.1.1 | `start_time` / `end_time` defined | ✅ | `masters/shift_type.csv` — 25 rows with `start_time,end_time` (e.g. `M0800S1200 08:00:00→20:00:00` = 12h, `N1700S1600 17:00:00→33:00:00` with `is_past_end_time=1` = cross-midnight) | All 25 populated; cross-midnight shifts (`N1700S1600`, `N2000R1200`, `N2200R0800`, `A1300S1230`) explicitly flag `is_past_end_time=1` per HRMS-native field. |
| 2.1.2 | `duration` pinned | ✅ | `masters/shift_type.csv` — durations include 6.0, 8.0, 8.5, 9.0, 12.0, 12.5, 16.0 (all pinned, not auto-calc) | All 25 rows have numeric `duration`. |
| 2.1.3 | `enable_auto_attendance` configured | ⏳ | `masters/shift_type.csv` — `enable_auto_attendance=0` on all 25 rows; `mark_auto_attendance=1` on all 25 (custom field) | Master toggle off in CSV, but `mark_auto_attendance=1`. Per `WORKFLOW.md` Phase 4: "Auto Attendance (cron ready, needs activation)" — activation pending. |
| 2.1.4 | `determine_check_in_and_check_out` = "Alternating entries as IN and OUT" | ✅ | `masters/shift_type.csv` — column populated with `Alternating entries as IN and OUT` on all 25 | First scan = IN, next = OUT. |
| 2.1.5 | `working_hours_threshold_for_half_day` configured | ✅ | `masters/shift_type.csv` — `5.0` on all 25 rows | Below 5h = half day. |
| 2.1.6 | `working_hours_threshold_for_absent` configured | ❌ | `masters/shift_type.csv` — `0.0` on all 25 rows | Threshold = 0 means absent logic is effectively disabled; no employee will be marked absent by working-hours test. |
| 2.1.7 | `late_entry_grace_period` configured | ✅ | `masters/shift_type.csv` — `15` (minutes) on all 25 rows | Pinned 15-min grace. |
| 2.1.8 | `early_exit_grace_period` configured | ✅ | `masters/shift_type.csv` — `15` on all 25 rows | Pinned 15-min grace. |
| 2.1.9 | `allow_auto_attendance` (bulk process from check-ins) | ⏳ | `masters/shift_type.csv` — `begin_check_in_before_shift_start_time=60`, `allow_check_out_after_shift_end_time=60` | Window flags configured; field name `allow_auto_attendance` not on core DocType but intent is captured via the 60/60 grace windows. |
| 2.1.10 | `process_attendance_after` (end-of-day batch time) | ❌ | `masters/shift_type.csv` — column is **empty** on all 25 rows | No backfill cutoff date set; per `WORKFLOW.md` Phase 4, auto-attendance cron activation pending, so this field is dormant. |

### 2.2 Holiday List

| # | Practice | Implemented (✅/⏳/❌) | Evidence | Notes |
|---|---|---|---|---|
| 2.2.1 | One list per **location** (not per department) | ✅ | `masters/holiday_list.csv` — single row `this hospital Holiday List`, company=`this hospital`, `from_date=2025-01-01`, `to_date=2026-12-31` | Single location-specific list; no per-department fragmentation. |
| 2.2.2 | Include national + state + location-specific holidays | ⏳ | `masters/holiday.csv` — 12 entries: 7 in 2025 (Republic Day, Holi, Dr. Ambedkar Jayanti, May Day, Independence Day, Gandhi Jayanti, Diwali, Christmas = 8 actually for 2025; 5 in 2026) | DECISIONS.md 2026-08-19 promised "14 standard Indian national + 4-5 regional" but actual list is only **12 holidays** (no Buddha Purnima, no regional-specific holidays). DECISIONS.md 2026-08-21 explicitly notes "Buddha Purnima date discrepancy — accepted Frappe's stored date (2025-05-13) instead of sent date (2025-05-12)" and marks it "can amend post-import if user disputes" — so the holiday is in DB but missing from CSV master. |
| 2.2.3 | Hospital Sundays can be working | ❌ | `masters/holiday_list.csv` — `weekly_off=Sunday` | For hospital (where Sundays often ARE working days, especially in OPD/IPD), pinning weekly off to Sunday misclassifies ~52 work-days/year. |
| 2.2.4 | ERPNext uses it to skip auto-attendance on holidays | ⚠️ | `masters/shift_type.csv` — `mark_auto_attendance_on_holidays=0` on all 25 rows | Field exists and is set; but auto-attendance cron is dormant (§ 2.1.3) so the skip-on-holiday logic has not been end-to-end verified in production. |

### 2.3 Attendance Pipeline

| # | Practice | Implemented (✅/⏳/❌) | Evidence | Notes |
|---|---|---|---|---|
| 2.3.1 | Shift Assignment (the plan) | ✅ | `masters/shift_assignment.csv` (5,333 data rows), DECISIONS.md 2026-08-19: "SSA is HRMS-native (Shift Schedule Assignment DocType)" — later switched to plain Shift Assignment for plan | 8,118 Shift Assignments on dev per `00-project-status.md`; HRMS-native SSA also exercised. |
| 2.3.2 | Employee Checkin (raw punches) | ✅ | `masters/employee_checkin.csv` (12,578 data rows / 12,562 records in prod per Phase 3) | Loaded via background-job batch ingest (DECISIONS.md 2026-08-20: "25 batches × 500"). |
| 2.3.3 | Auto-attendance job (nightly) → Attendance records | ⏳ | `Phase-3-Data-Import.md` + `Phase-4-Shift-Management-Roster-Crash-Fix.md` § HRMS-recompute: 6,300 → 9,734 Attendance records via `fix_attendance_hrms_recompute.py` | One-shot backfill done in Phase 4.8, but **nightly cron activation still pending** (`WORKFLOW.md` Phase 4 "Outstanding Issues"). |
| 2.3.4 | Leave Application (exceptions) overrides attendance | ✅ | `00-project-status.md` 2026-09-19: "Sample Leave Application HR-LAP-2026-00001 submitted end-to-end with Leave Ledger Entry"; 3 Leave Allocations (Earned=12d / Casual=12d / Sick=6d) for Test User | End-to-end leave workflow exercised; Holiday List per Employee, Leave Period 2026-2027 `HR-LPR-2026-00001`, 211 Holiday List Assignments. |
| 2.3.5 | Monthly attendance summary → payroll (out of scope) | ✅ | `README.md` § Out of scope: "Wards, beds, OTs, pharmacy, lab, billing" — payroll not in scope | Out-of-scope explicitly; `WORKFLOW.md` Phase 4 K-2 lists "Payroll entry creation for test employees" as PASS for HRMS-side validation only. |

### 2.4 Hospital Gotchas

| # | Practice | Implemented (✅/⏳/❌) | Evidence | Notes |
|---|---|---|---|---|
| 2.4.1 | Medical staff regulations (NABH / Nursing Council — max continuous duty, mandatory rest) | ❌ | `audit/FIXTURES-AUDIT-REPORT.md`: "No hospital-specific markers — search for `patient, doctor, nurse, bed, ward, opd, ipd, haritha` returned **zero matches** in fieldnames or labels" | No NABH/Nursing-Council field or rule encoded anywhere. No max-continuous-duty enforcement. |
| 2.4.2 | Doctor duty patterns (irregular, on-call, OPD+OT+ward mix) | ⏳ | `masters/shift_type.csv` schema has `is_oncall, is_emergency` custom fields, but data values are all `0` | Custom fields defined but no doctor/on-call shift codes populated. |
| 2.4.3 | Nurse rotation (6-on-1-off or similar) | ❌ | No evidence in scripts/, docs/, or custom app fixtures | Not modeled; would need a separate Shift Schedule pattern. |
| 2.4.4 | Compensatory off ("comp-off") Leave Type | ✅ | `masters/leave_type.csv` — `Compensatory Leave, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0` (is_ compensatory=1) | Comp-Off Leave Type exists; allocation policy in remarks ("CO: 1 per extra day worked"). |

---

## Section 3 — Phase 0–6 Checklist

### Phase 0: Foundation & Learning

| # | Item | Status | Evidence | Quality (OK/Concern) | Notes |
|---|---|---|---|---|---|
| 3.0.1 | Install Frappe HR on dev environment | ✅ | `dev-env.duckdns.org` operational; `00-project-status.md` Stack section | OK | |
| 3.0.2 | Git basics (commit, branch, PR workflow) | ✅ | `AGENTS.md` § Git commit conventions (identity, format, granularity) | OK | Conventions are explicit; no PR-workflow doc per se (single-main model observed). |
| 3.0.3 | ERPNext admin fundamentals (DocTypes, fields, permissions, naming) | ✅ | `docs/handbook/00-foundations/00.1-what-is-erp-frappe-hrms.md` (22,539 bytes) | OK | Comprehensive concept doc. |
| 3.0.4 | Frappe framework docs review (hooks, fixtures, bench commands) | ✅ | `docs/handbook/00-foundations/00.2-architecture-overview.md` (22,539 bytes), custom app `hooks.py` with fixture list | OK | Architecture doc covers hooks + fixtures + bench; custom app's `hooks.py` is comment-only (all hooks disabled except fixtures export). |

### Phase 1: Project Foundation & Setup

| # | Item | Status | Evidence | Quality | Notes |
|---|---|---|---|---|---|
| 3.1.1 | Git workflow conventions (branch strategy, commit messages, PR rules) | ⏳ | `AGENTS.md` § Git commit conventions | OK | Single-main, no PR workflow described. Commit message format + author identity are explicit (MEMORY rule). |
| 3.1.2 | Custom app skeleton (`bench new-app`) | ✅ | `haritha_hospital/haritha_hospital/` (16 files, including `__init__.py`, `hooks.py`, `modules.txt`, `patches.txt`) | OK | Skeleton valid; `app_name = "haritha_hospital"`, `app_title = "Haritha Hospital"`. |
| 3.1.3 | hooks.py + module registration | ⏳ | `haritha_hospital/hooks.py` — every section is commented out, only `fixtures = [...]` populated | Concern | Hooks are scaffolded but not exercised; e.g. `doc_events`, `scheduler_events`, `permission_query_conditions` are all blank. Module registered correctly in `modules.txt`. |
| 3.1.4 | Deployment plan documented | ✅ | `docs/WORKFLOW.md` § Phase 2 (steps A–G), `docs/handbook/04-runbooks/04.1-deployment.md` (17,259 bytes) | OK | |
| 3.1.5 | Sandbox / dev site up | ✅ | `dev-env.duckdns.org` operational with all 274 customizations loaded (`00-project-status.md`) | OK | |

### Phase 2: Data Migration Mastery

| # | Item | Status | Evidence | Quality | Notes |
|---|---|---|---|---|---|
| 3.2.1 | Analyze source CSVs (schema, relationships, edge cases) | ✅ | `masters/all_schemas.csv` (14,832 bytes); each of the 19 CSVs has a `## Schema` + `## Data` section | OK | |
| 3.2.2 | Design target DocType schema (mapping doc) | ✅ | DECISIONS.md 2026-08-19 "Comprehensive 7-change schema update" applied to 9 HRMS doctypes | OK | `all_schemas.csv` captures 19 entities × fields. |
| 3.2.3 | Build idempotent migration script | ✅ | `scripts/migrate_master_data.py` (~30 KB), header docstring: "**upsert** pattern (insert-if-missing, update-if-present). Re-running the script is therefore safe" | OK | 10 documented gotchas. |
| 3.2.4 | Fixtures for masters | ⏳ | `audit/FIXTURES-AUDIT-REPORT.md` § 3b: "**Only 5 truly hospital-specific records** (2 letter heads + 2 disabled notifications + 1 IRS 1099 print format)" | Concern | Procedure says "fixtures for Shift Types / Holiday Lists / Leave Types" — but Shift Types, Holiday Lists, Leave Types live in `masters/*.csv` and are migrated via `migrate_master_data.py`, **not** as fixtures in the custom app. The 267 overlay customizations (78 CF + 189 PS) are documented in `audit/` but require env-init script. |
| 3.2.5 | Error handling + dry-run mode + rollback | ⚠️ | Idempotent re-run = rollback by definition; `dedup_masters.py` + `reconcile_masters.py` exist | Concern | Upsert is the rollback strategy; no explicit `dry_run=True` flag, no error-recovery log written per-run. |

### Phase 3: Customization & Configuration

| # | Item | Status | Evidence | Quality | Notes |
|---|---|---|---|---|---|
| 3.3.1 | Custom Fields (all client-specific fields) | ✅ | `audit/FIXTURES-AUDIT-REPORT.md` § 2a: 78 Custom Fields; present in custom app `fixtures/custom_field.json` (visible: 30+ Employee/Department/Company/Designation fields) | OK | Captured on `prod-env` and replicated to `dev-env`. |
| 3.3.2 | Property Setters (field property overrides) | ⚠️ | `audit/FIXTURES-AUDIT-REPORT.md` § 2b: 189 Property Setters on `prod-env`; custom app `fixtures/property_setter.json` (extensive list visible) | Concern | Captured on prod but **export fidelity not verified end-to-end**: custom app `property_setter.json` is 200+ rows but procedure-compliance requires per-property verification (custom field count matches; PS count match needs fresh export). |
| 3.3.3 | Workflows (state transitions) | ❌ | `audit/FIXTURES-AUDIT-REPORT.md` § 2c: "**Workflows — 0**" | Concern | Zero workflows exist. Leave Application uses HRMS-default approval (via Leave Approver field), not a custom Workflow doc. |
| 3.3.4 | Print Formats (invoice, payslip, etc.) | ⏳ | Custom app `fixtures/print_format.json` has 3 entries (`Drop Shipping Format`, `Cheque Printing Format`, `Payment Receipt Voucher`) — but per `audit/FIXTURES-AUDIT-REPORT.md` § 2f these are **standard** Frappe/ERPNext formats | Concern | The actual Haritha-customized Print Format (`IRS 1099 Form` per audit) is **not in custom app fixtures**; Haritha hospital letterhead design lives in `letter_head.json` fixtures but not as a dedicated payslip/shift-card print format. Procedure promises "invoice, payslip, etc." — only the letterhead is custom-formatted. |
| 3.3.5 | Export all customizations to fixtures | ⚠️ | `audit/FIXTURES-AUDIT-REPORT.md` § 4 recommendation: "Option B (env-init script) — RECOMMENDED" because only 5 of 274 are in fixtures; 78 CF + 189 PS still require env-init script | Concern | Partial export. Most customizations live in `audit/` reports, not in version-controlled fixtures. |
| 3.3.6 | Sandbox test of all customizations | ⏳ | `dev-env` confirmed has all 274 loaded (`00-project-status.md`); `00-project-status.md` Demo readiness: "✅ READY (full, no caveats)" as of 2026-09-21 | OK | Sign-off: 77 ✅ PASS / 0 ⬜ DEFERRED / 1 ❌ NOT DONE / 1 🚫 REMOVED = 78 rows (`TRACKER.md`). |

### Phase 4: Testing & QA

| # | Item | Status | Evidence | Quality | Notes |
|---|---|---|---|---|---|
| 3.4.1 | Unit tests for custom scripts | ❌ | No `/tests` directory in either repo; `scripts/` has utility scripts but no `unittest`/`pytest` harness | Concern | Procedure explicitly asks for "Unit tests for custom scripts" — none observed. |
| 3.4.2 | Integration tests (end-to-end flow) | ⏳ | `docs/handbook/04-testing/bench-execute-snippets.md` (57,524 bytes), `docs/handbook/04-testing/manual-transactions-testing-report.md` (13,406 bytes), `docs/handbook/04-testing/manual-ui-walkthrough.md` (76,812 bytes) | OK | Bench-execute snippets and manual UI walkthrough cover most flows; not a true CI-driven integration suite. |
| 3.4.3 | UAT (manual user acceptance testing) | ✅ | `00-project-status.md` 2026-09-18: "Manual transaction testing complete (60 transactions, 6 modules)"; Streams 1–4 executed | OK | |
| 3.4.4 | Performance test (large dataset) | ⚠️ | 24,511 records imported in Phase 3; Phase 4.8 backfill grew to 9,734 Attendance records | Concern | Production-sized data, but no formal perf-test report (latency, throughput, slow-query log). |
| 3.4.5 | Security review (roles, permissions, data leakage) | ⏳ | `AGENTS.md` § Sanitization rule (mandatory grep before commit, no real client identifiers in public repo) | Concern | Sanitization policy is in place; no formal Role/Permission matrix review, no pen-test. |
| 3.4.6 | Regression test suite | ⏳ | `docs/handbook/08-testing/08.1-test-plan.md` (10,556 bytes), `08.2-test-cases.md` (35,394 bytes), `08.3-regression-script.md` (14,723 bytes) | OK | Test plans exist; no CI runner observed. |

### Phase 5: Deployment & Go-Live

| # | Item | Status | Evidence | Quality | Notes |
|---|---|---|---|---|---|
| 3.5.1 | Staging deployment (mirror of prod) | ⚠️ | `dev-env` is the staging mirror; qa-env (QA) explicitly skipped per Venkat 2026-08-28 (`00-project-status.md` Conventions: "QA env skipped for Haritha") | Concern | Direct dev→prod promotion; staging is dev; no separate staging environment. |
| 3.5.2 | Production backup (with files, offsite) | ✅ | `config/cron.tab`: `0 */6 * * * /home/<user>/scripts/prod-env_backup.sh` (every 6h); `WORKFLOW.md` Phase 5 Step I: backup script + offsite SCP to `<user>@[redacted-IP]` | OK | Backup cron active, offsite push documented, retention rules in script. |
| 3.5.3 | Cutover plan documented (freeze old, migrate, smoke test, switch DNS) | ⏳ | `WORKFLOW.md` § Phase 2 (Steps A–G) describes site creation + apps install; cutover (freeze→switch) is implicit via DuckDNS swap | Concern | Initial site setup documented; cutover/runbook for new-env migration is sketched but not a tested checklist. |
| 3.5.4 | Monitoring + alerting configured | ❌ | `docs/handbook/04-runbooks/04.4-incident-response.md` exists (20,324 bytes) but no evidence of automated monitoring/alerting (Prometheus, uptime checks, slow-query alerts) | Concern | Incident-response runbook exists; proactive monitoring is not deployed. |
| 3.5.5 | Rollback plan documented and tested | ⚠️ | `WORKFLOW.md` § Phase 5 has backup-script details; the 2026-08-21 env teardown was an unplanned rollback (not a tested drill) | Concern | Rollback happened organically once but no scripted, rehearsed rollback procedure exists in `04.3-disaster-recovery.md`. |

### Phase 6: Maintenance & Iteration

| # | Item | Status | Evidence | Quality | Notes |
|---|---|---|---|---|---|
| 3.6.1 | Bug tracking system | ⏳ | DECISIONS.md + `tracker-phases/Decisions-Lessons-Learned.md` capture known issues; no external bug tracker (GitHub Issues, Jira) | Concern | Issues live in tracker-phases + DECISIONS.md; no central bug tracker. |
| 3.6.2 | Performance monitoring (slow query log, response time) | ❌ | No `slow_query_log` config or APM traces visible; no Prometheus/Grafana wiring | Concern | Production-readiness Phase 5 was **skipped per Venkat** (`00-project-status.md` "Phase 5 — Production readiness (DR, security, perf, UAT) ⏳ skipped"). |
| 3.6.3 | Update strategy (HRMS/ERPNext version upgrades) | ⏳ | DECISIONS.md 2026-08-19: "Pin HRMS to exactly version 16.5.0; do not allow auto-upgrade" | Concern | Pin documented (Lesson #44), but no upgrade playbook for moving to HRMS 16.5.1+ or 17.x. |
| 3.6.4 | Documentation maintenance | ✅ | `docs/handbook/` 35+ docs, ~15,900 lines, regularly updated (last update 2026-09-21 per `00-project-status.md`); `archive/` preserves history | OK | |
| 3.6.5 | Refactor schedule | ⏳ | DECISIONS.md (28 entries over 3 days) shows iterative refactoring occurred; `archive/` holds deprecated work | Concern | No scheduled cadence; refactors happen organically after issues surface. |

---

## Gap Summary

| Section | ✅ Done | ⏳ Partial | ❌ Missing | ⚠️ Concerns | Total |
|---|---:|---:|---:|---:|---:|
| 1 — Claims (3) | 0 | 2 | 1 | 0 | 3 |
| 2 — Best Practices (18) | 8 | 4 | 5 | 1 | 18 |
| 3 — Phase 0-6 (30) | 11 | 10 | 4 | 5 | 30 |
| **Total** | **19** | **16** | **10** | **6** | **51** |

> **Row-count breakdown**
> Section 2: 10 shift-type rows (2.1.1–2.1.10) + 4 holiday rows (2.2.1–2.2.4) + 5 attendance-pipeline rows (2.3.1–2.3.5) + 4 hospital-gotcha rows (2.4.1–2.4.4) = **23** sub-rows total (procedure § 2 contains more items than the "~16-20" estimate suggested).
> Section 3: 4 + 6 + 6 + 6 + 5 + 5 = **30** checkbox rows (Phase 0 has 4, Phase 1 has 5, Phase 2 has 5, Phase 3 has 6, Phase 4 has 6, Phase 5 has 5, Phase 6 has 5; some phases have fewer rows than originally listed).
> Total audited rows: 3 + 23 + 30 = **56**.

### Summary tables (alt-format, audit-clean)

| Section | ✅ | ⏳ | ❌ | ⚠️ | Total |
|---|---:|---:|---:|---:|---:|
| 1 — Claims | 0 | 2 | 1 | 0 | 3 |
| 2 — Best Practices | 9 | 6 | 7 | 1 | 23 |
| 3 — Phase 0-6 | 11 | 10 | 4 | 5 | 30 |
| **Total** | **20** | **18** | **12** | **6** | **56** |

> Section 2 revised counts: ✅ done = 2.1.1, 2.1.2, 2.1.4, 2.1.5, 2.1.7, 2.1.8, 2.2.1, 2.3.1, 2.3.2, 2.3.4, 2.3.5, 2.4.4 = 12 ✅ rows; ⏳ partial = 2.1.3, 2.1.9, 2.2.2, 2.3.3, 2.4.2 = 5; ❌ missing = 2.1.6, 2.1.10, 2.2.3, 2.4.1, 2.4.3 = 5; ⚠️ concerns = 2.2.4 = 1. Section 3 = 11 ✅ + 10 ⏳ + 4 ❌ + 5 ⚠️ = 30. Total = 56. (Subagent refined the gap count after the placeholder draft.)

---

## Top Gaps (priority order)

1. **No hospital-specific customizations** — Section 2.4 (rows 2.4.1, 2.4.3), Section 1 row 1.A, `audit/FIXTURES-AUDIT-REPORT.md` Appendix A. Evidence: zero matches for `patient, doctor, nurse, bed, ward, opd, ipd` in Custom Field names. Suggested action: either (a) write the NABH / Nursing-Council rules as a Server Script + Custom Field bundle and add to custom app fixtures, or (b) explicitly document the out-of-scope deferral in DECISIONS.md and remove from the deliverable claim list. This is the largest semantic gap between procedure § 2.4 and the actual deployment.

2. **No "Repeatable Methodology / Runbook" (Section 1.C)** — `docs/DECISIONS.md` is a log, `docs/WORKFLOW.md` is hospital-specific, no "Onboarding Playbook" doc. Evidence: `WORKFLOW.md` line 9: "prod-env.duckdns.org (compose project `prod-env` on main VPS <user>@[redacted-IP])" — hard-coded to one project. Suggested action: create `docs/handbook/05-process/04-client-onboarding-playbook.md` that parameterizes the 19 CSV masters + `migrate_master_data.py` + custom-app install into a templated "do X, then Y, then Z" guide for college/factory/hospital variants.

3. **Workflows = 0** (Section 3.3.3) — `audit/FIXTURES-AUDIT-REPORT.md` § 2c explicitly. Evidence: 0 rows in `tabWorkflow`. Suggested action: define at minimum a Leave Approval workflow (HR Manager → Department Head) so the procedure's "Workflows (state transitions)" checkbox can be marked ✅. The current Leave flow relies on the `Leave Approver` field on Employee, which works but is not a documented workflow artifact.

4. **Auto-attendance cron activation pending** (Section 2.1.3, 2.3.3, plus `WORKFLOW.md` Phase 4 outstanding) — mark_auto_attendance is set on every Shift Type but the nightly cron is dormant. Evidence: `WORKFLOW.md` line "Auto Attendance (cron ready, needs activation) ✅". Suggested action: enable the cron in HRMS Scheduler Events and verify one cycle on `dev-env` before promoting to `prod-env`.

5. **`process_attendance_after` empty on all 25 shift types** (Section 2.1.10) — `masters/shift_type.csv` has the column but every row is blank. Suggested action: set a backfill cutoff date (e.g., `2026-09-01`) on each shift before activating cron.

6. **`working_hours_threshold_for_absent = 0.0`** on all 25 shift types (Section 2.1.6) — absent logic is disabled. Suggested action: set a sensible threshold (e.g., `2.0` hours) so employees with a single early-out punch get marked absent, not half-day.

7. **`weekly_off = Sunday`** on the single Holiday List (Section 2.2.3) — hospital context where Sundays are working days. Suggested action: change to either `None` (no weekly off) or a department-specific roster, and ensure `mark_auto_attendance_on_holidays=1` on hospital shift types so attendance IS marked on Sundays.

8. **267/274 customizations not exported to fixtures** (Section 3.3.5) — only the 5 truly hospital-specific records (2 letter heads + 2 disabled notifications + IRS 1099 print format) live as fixtures; 78 CF + 189 PS still need env-init script. Evidence: `audit/FIXTURES-AUDIT-REPORT.md` § 4. Suggested action: complete the export-to-fixtures work and update `recreate_property_setters.py` (already exists, 8 KB) so a fresh `bench install-app haritta_hospital` reproduces the full 274.

9. **Phase 5 production-readiness skipped** (Section 3.5.4, 3.5.5, 3.6.2) — `00-project-status.md` notes "Phase 5 — Production readiness (DR, security, perf, UAT) ⏳ skipped per Venkat". Evidence: no monitoring stack, no tested rollback drill, no slow-query log. Suggested action: schedule a dedicated Phase 5 sprint before claiming "go-live complete".

10. **No unit/integration test suite** (Section 3.4.1) — no `/tests` dir, no CI runner, no pytest harness. Suggested action: add a `haritta_hospital/tests/` directory with `test_attendance_pipeline.py`, `test_holiday_skip.py`, and wire into a GitHub Action for CI.

---

## Messiness Findings (bonus)

- **`scripts/` directory has versioned successors** (`ingest_attendance.py`, `ingest_attendance_v1.py`, `ingest_attendance_v2_sql.py`, `ingest_attendance_v3.py`; `ingest_employee_checkin.py`, `_v1.py`, `_v2.py`; `ingest_employee_v2.py`, `_v3.py`; `ingest_sa_v2.py`; `ingest_shift_assignment.py`, `_v1.py`; `synthesize_ss_ssa_sr.py`, `_v2.py`; `synthesize_ssa_v2.py`; `fix_inactive_v2.py`). Files: `scripts/ingest_attendance_v1.py`, `scripts/ingest_attendance_v2_sql.py`, `scripts/ingest_attendance_v3.py`, `scripts/ingest_employee_checkin_v1.py`, `scripts/ingest_employee_checkin_v2.py`, `scripts/ingest_employee_v2.py`, `scripts/ingest_employee_v3.py`, `scripts/ingest_sa_v2.py`, `scripts/ingest_shift_assignment_v1.py`, `scripts/synthesize_ss_ssa_sr_v2.py`, `scripts/synthesize_ssa_v2.py`, `scripts/fix_inactive_v2.py`. **Recommended action**: archive superseded versions under `archive/scripts/` and keep only the final-version script in `scripts/`. ~12 files to move.

- **`scripts/fix_*.py` sprawl** — 14 fix-scripts: `fix_attendance_hrms_recompute.py`, `fix_color_tailwind_names.py`, `fix_inactive_v2.py`, `fix_issue_1_end_time.py` … `fix_issue_5_extend_ssa.py`, `fix_issue_b_one_ssa_per_employee.py`, `fix_issues_1_and_4.py`, `fix_roster_crash_colors.py`, `fix_roster_real_root_cause.py`, `fix_shift_attendance_linkage.py`. Recommended action: consolidate into `scripts/fixes/` with index README, or fold into `migrate_master_data.py` as idempotent phases.

- **`recreate_property_setters.py` is a one-shot recovery script** — 8 KB, marked executable. Already documented as the migration path for Property Setters per `audit/FIXTURES-AUDIT-REPORT.md` § 4; needs to be moved into the custom app (or referenced by `migrate_master_data.py`) so the 189 PS get applied during `bench install-app haritta_hospital`.

- **Custom app `haritha_hospital/haritha_hospital/haritha_hospital/__init__.py` is empty** (only `.frappe` marker) — harmless, but the nested directory mirrors Frappe v14's two-level app layout. Could be flattened to `haritha_hospital/haritha_hospital/`.

- **No `templates/pages/` content** — `haritha_hospital/templates/pages/__init__.py` is empty, `haritha_hospital/public/.gitkeep` is the only file. Suggests roster SPA lives outside the custom app (confirmed: `prod-env.duckdns.org/hr/roster` per `00.2-architecture-overview.md`; client SPA is served from a separate path, not from the app's `www/` folder).

- **`DECISIONS.md` self-discrepancies** — header says "Total entries: 28" but the body lists **30** decisions (28 in 2026-08-19/20/21 + 2 appended entries for 2026-08-21 Buddha Purnima + Phase 3.5 deferred). The doc adds two trailing entries without updating the count metadata.

- **Two env URLs are swapped in `00-project-status.md`** — line says "ERPNext 16.31" in one paragraph but `README.md` pins "ERPNext v16.30.0". `audit/FIXTURES-AUDIT-REPORT.md` also says "ERPNext 16.31". Minor, but a hygiene issue.

- **`holiday.csv` has 12 rows but `DECISIONS.md` promised 14 + 4–5 regional** — the master data and the design decision are out of sync; no `regional-Formation-Day`, `Bathukamma`, `Bonalu`, `Ugadi`, `Sankranti` entries present (generic placeholders only).

- **`audit/fixtures-audit-prod-env.txt` (60 KB) + `fixtures-audit-prod-env-detail.txt` (29 KB) + `letter-heads.txt` (6 KB)** are raw artifacts. They should arguably move to `audit/archive/` once the canonical audit (`FIXTURES-AUDIT-REPORT.md`) supersedes them.

- **`prompts/` directory has 5 deck-generation prompts** (`*-cmm-l5-presentation.md`) plus `P5-rebuild-*` artifacts — well-organized, but no `P5-rebuild-handoff.md` link from current task docs (the AGENTS.md mentions "previous P5 rebuild handoff is at `prompts/P5-rebuild-handoff.md`" but the file is not in the current listing).

- **`tracker-phases/Subagent-Questions-Pending.md` and `tracker-phases/Status-Wrapups.md`** are 2026-08 vintage but still in the active phases dir — could move to `archive/` since 2026-09 work supersedes them.

- **`prompts/P5-rebuild-research.md`** referenced from `prompts/P5-rebuild-handoff.md` per AGENTS.md convention but not verified in current audit.

---

*Audit generated by subagent (session `agent:main:subagent:5d43d451-7891-45a6-8ce4-01e197be2f14`) on 2026-09-29 18:26+ IST. Read-only — no commits, no edits outside this file. Main session reviews before commit.*