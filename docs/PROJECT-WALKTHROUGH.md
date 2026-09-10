# Haritha Hospitals — Project Walkthrough for Newcomers

**Last updated:** 2026-09-10 — repo refresh: renamed phase6→handbook, phase-a→archive, fixed 42 stale path refs
**Audience:** Someone new to the project (treat as having zero context)
**Reading time:** ~15-20 minutes
**Sources:** Verified from `git log` + `TRACKER.md` + `README.md` + `tracker-phases/` + recent commits

---

## 1. What is this project? (TL;DR)

**Haritha Hospitals ERPNext + HRMS deployment** is a real-world hospital shift-management + HRMS rollout built on Frappe v16 for Processbricks' client. The project delivers employee rosters, shift schedules, attendance, leave, and check-ins — all wired together via a custom Frappe app (`haritha_hospital`) that captures every customization as portable JSON fixtures. It is *not* a generic hospital ERP (wards, beds, OT, pharmacy, lab, billing are explicitly out of scope).

| | |
|---|---|
| **Built for** | Processbricks' client — Haritha Hospitals (real hospital, CMM L5 maturity target) |
| **By** | Venkat Narasimha (Processbricks) |
| **Concept started** | 2026-04-01 (per README header) |
| **Work on this repo began** | 2026-08-19 (first commit) |
| **Current state** | Phases 0–4 + Phase 6 (docs) + Phase 0+ (custom app + migration) done; Phase 5 (prod hardening) deferred; client onboarding kit added 2026-09-09 |
| **Production env** | https://pberpprod.duckdns.org |
| **Dev env** | https://pberpdev.duckdns.org |
| **Venkat's prototyping VPS** | https://dev-erp.duckdns.org |

---

## 2. The two repositories

| Repo | URL | Purpose | Default branch |
|---|---|---|---|
| `haritha_hospital` (singular) | github.com/venkat-narasimha/haritha_hospital | Frappe custom app code + 274 customizations as fixtures (78 Custom Fields + 189 Property Setters + 3 Print Formats + 2 Notifications + 2 Letter Heads) | `main` |
| `haritha-hospitals` (dash) | github.com/venkat-narasimha/haritha-hospitals | Workspace docs: `TRACKER.md`, `HARITHA_HOSPITALS_GUIDE.md`, `masters/`, `scripts/`, `docs/`, `pdfs/`, `prompts/` | `main` |

> **Verified:** `haritha-hospitals` has **82 commits** between 2026-08-19 and 2026-09-09. The custom app is the consumer of fixtures produced by operations on this repo; both repos ship independently.

---

## 3. Timeline — chronological walkthrough

Built from the full `git log --reverse` of the workspace repo (82 commits).

### Phase 0 — Schema planning (2026-08-19)

**Goal:** Plan the data model and define 15 master entities for shift + HRMS.

- `c9c9a3b` — `feat(schema): initial project structure + 15-entity schema CSV`
- `8307c0c` — `feat(schema): add Shift Schedule, SSA, SR entities + remove shift_code field`
- `aac7b3e` — `feat(schema): comprehensive HRMS v15 verification — 19 entities, 168 fields`
- `21d54f4` — `feat(schemas): add 19 schema+data CSVs (one per entity)`

**Key artifacts:** `all_schemas.csv`, `masters/` folder, `Decisions-Lessons-Learned.md` (the consolidated decisions log: scope = shift only, HRMS pinned to v16.5.0, shift codes `[GMAN]\d{4}[RS]\d{4}`, holidays = Indian national + Telangana regional).

**Outcome:** 19 CSVs covering Company, Department, Designation, Employee, Shift Type, Shift Assignment, Attendance, Employee Checkin, Holiday List, Leave Type, Employment Type, etc. ~1.77 MB / 24,758 rows.

### Phase 1 — Schema approval (2026-08-20)

**Goal:** Manager sign-off on schema + data.

- `d3ab288` — Phase 0 + 1 marked done in tracker
- 3 designation collisions resolved automatically (Physician Asstant+Assistant, Sr.Executive+Senior Executive, Sr.Manager+Senior Manager)
- 3 shift code duplicates consolidated (A4+Shift-A, B2+Shift-B, C1+Shift-C)

### Phase 2 — Site setup on `pberp.duckdns.org` (2026-08-20 → 2026-08-21)

**Goal:** Stand up a Frappe v16 site and install ERPNext + HRMS + customizations.

- `7efaf6f` — Phase 2 setup plan for pberp.duckdns.org
- `a468113` — Site setup, data import of 24,511 records, nginx + workers, backup cron
- Apps installed: frappe 16.30.0, erpnext 16.30.0, hrms 16.5.0 (pinned per Lesson #44), payments
- Backend API smoke test PASS: auth, CRUD, all 9 entities queryable, payroll/leave/holiday workflows

### ⚠️ Rollback event — 2026-08-21 10:11–10:18 IST

The `pberp.duckdns.org` env was torn down under **Option B (nuke, no backup)** at Venkat's authorization. All Phase 2–5 deployment work was destroyed. CSV masters + git history + Phase 0/1 design were preserved.

- `a0d1be9` — `docs(tracker): rollback event 2026-08-21 — pberp teardown, restart from Phase 1`

**Lesson learned:** never run destructive ops without an explicit, recent backup. Always backup-first; never auto-restore in prod.

### Phase 2 (restart) — Site setup on `pberpprod.duckdns.org` (2026-08-25)

- `cb546db` — `docs(workflow): add WORKFLOW.md with Phase 2-5 runbooks`
- `fe33f31` — `docs(migration): add MIGRATION-GUIDE.md`
- `e60202d` — `docs(index): add INDEX.md`
- `e44215d` — `docs(decisions): add DECISIONS.md extracted from TRACKER.md (28 entries)`
- `219978d` — `docs(audit): add PRODUCTION-READINESS-AUDIT-2026-08-21.md`
- `7e95049` — `docs(verify): pre-ingest verification script + Phase 1.5/2 sections`
- `5350324` — `docs(tracker): reusable update_tracker.py + Phase 2 backup`

**Outcome:** Fresh `pberpprod.duckdns.org` env with backup-first procedures in place.

### Phase 3 — Data import, 24,511 records (2026-08-25 → 2026-08-27)

- `07d497e`, `b98cc47` — Reusable scripts for shift_assignment, attendance, employee_checkin (Phase 3a-3d)
- `aaa5b8a`, `4bccc4a` — `os.chdir(BENCH_DIR)` + explicit `sites_path` fix so `frappe.init()` discovers site
- `d6a42db` — Phase 3 done 2026-08-26
- `2a1c9f3` — synthesized SS / SSA / SR for demo (Phase 3.5 fill-in)
- `3f82928` — fixed SSA count: 420 SSAs per unique employee × shift_type combo + linked SA rows
- `3f76391`, `a4e281a` — reconcile + SS/SSA/SR + cron regression notes

**Bulk-submit drama (Phase 3.6):** 6,314 draft docs had to be bulk-submitted. The submit needed **3 separate runs** because of three framework barriers (Lesson #106):
1. Naming-series backfill (Lesson #104)
2. Property Setter to add `Holiday` + `Weekly Off` to status options
3. Monkey-patch `erpnext.controllers.status_updater.validate_status` because HRMS `Attendance.validate()` has a hardcoded 5-value list

**Phase 3.7–3.10 follow-ons:**
- `ec9f989` — idempotent `recreate_property_setters.py` (Property Setters can't be fixture-exported because HRMS `hooks.py` is third-party — Lesson #151)
- `c7bf823` — Phase 3.8: Shift Attendance report linkage fix
- `606cd90` — Phase 3.9: populate Attendance.department + employee_name from Employee (Lesson #112 — raw SQL skips ORM FK derivation)
- `a89d07e` — Phase 3.10: backup script bundle fix (silent 6-day offsite failure resolved)
- `dd6643e` — TRACKER: cleanup orphan items 11-21

### Phase 4 — Shift management + roster crash fix (2026-08-28)

The roster SPA at `/hr/roster` crashed when rendering 211 employees × 31 days.

- `647c86c` — Phase 4.2: Shift Location 'Hyderabad' + 5,738 record backfill
- `647c86c` — Phase 4.3: submit 5 Draft Shift Schedules
- `51a8067`, `3a4748c` — Phase 4.1/4.5: Shift Type `end_time` wrap + Tailwind color palette (G=blue, M=green, A=orange, N=violet — lowercase)
- `403a25e` — Phase 4.6: extend 420 SSAs `create_shifts_after` to today + 90 days
- `f0f5c8c` — Phase 4.7: **Option B** — 1 SSA per employee (cancel duplicates + delete orphans + re-run)

**Crash root cause:** CapitalCase Tailwind colors in `MonthViewTable.vue` did not match the HRMS palette. After normalizing to lowercase, the roster renders cleanly.

### Phase 0+ — Custom app build + master data migration (2026-08-28 → 2026-08-29)

This is the foundational milestone that turned ad-hoc operations into a portable, reproducible deployment.

- **Custom app `haritha_hospital` v0.0.1** built — captures **274 production-validated customizations** as Frappe JSON fixtures
- **Installed on both envs:** `pberpdev` (fresh) and `pberpprod` (idempotent re-install verified, `installed_apps` updated, count matches)
- **Master data migrated prod → dev** via `scripts/migrate_master_data.py` — 16 DocTypes via upsert pattern (Lesson #157). pberpdev now mirrors prod: 1 Company, 210 Employees, 37 Departments, 25 Shift Types, 8,118 Shift Assignments, 6,300 Attendance, 12,562 Employee Checkins, etc.

### ⚠️ P1 outage — 2026-08-29 03:06 IST

Both `pberpprod` and `pberpdev` returned HTTP 500 after `bench install-app haritha_hospital` on dev. Cause: gunicorn `--preload` freezes `sys.path` at container startup; new Python packages added via `install-app` are not picked up by running workers. Fix: restart backend + scheduler + queue-short + queue-long containers. ~30–60s downtime per env, **zero data loss**.

- **Lesson #153:** Gunicorn `--preload` + new Python package = backend container restart required
- **Lesson #154:** `docker restart` ≠ `docker-compose down`

### Phase 6 — Process & maturity documentation (2026-08-29)

A massive documentation push: **34 docs across 9 tiers** (some sources count 35 with the README), ~15,900 lines total, plus **67 PDF renders** in `pdfs/`.

- Tiers 0–8: foundations, schema, workflow, client deck, runbooks, process, user manuals, testing
- Tier 9 (compliance): **12 docs** — ISO 27001-aligned policies + CMM L5 maturity
- Client demo deliverable: 11-slide PPTX (543 KB) + speaker script + 10 screenshots + 20 mermaid-rendered diagrams

### Recent — client onboarding kit (2026-09-09)

Last commit added a client onboarding data collection kit:
- `docs/client-onboarding/` — process docs, intake workbook (master data + settings checklists), sign-off templates
- Purpose: standardize the data-gathering process for future hospital clients

---

## 4. The custom app (`haritha_hospital`)

Lives at github.com/venkat-narasimha/haritha_hospital. Version 0.0.1.

**What it does:** Owns every customization Haritha needs as JSON fixtures. This means a fresh env can install the app, run `bench migrate`, and immediately have every Custom Field, Property Setter, Print Format, Notification, and Letter Head that the prod env has — without copy-pasting from a doc.

**What's in it (274 fixtures):**

| Type | Count | Notes |
|---|---:|---|
| Custom Fields | 78 | Employee (PAN, IFSC, approvers), Company (Payroll cost center), Attendance (status extensions), Shift Type (color + HRMS flags), Shift Assignment (Dept link), Holiday List (Telangana regional), Leave Application workflow |
| Property Setters | 189 | Largest category — ~120 HRMS, ~50 ERPNext, ~19 Frappe core. Status options, defaults, mandatory toggles, field order |
| Print Formats | 3 | Payslip, Shift Card, Leave Application |
| Notifications | 2 | Both disabled (Shift assignment change + Leave approval pending) |
| Letter Heads | 2 | Haritha Hospitals (default) + Haritha Hospitals — Confidential (HR/Payroll) |

**Why it exists:** Two earlier alternatives were ruled out:
- "Custom fields in production DB only" — non-portable, breaks env rebuild / `bench update` resets
- "Property Setters as fixtures" — broken because HRMS `hooks.py` doesn't declare Property Setters, and `bench export-fixtures` silently skips apps without the declaration (Lesson #151)

**Known caveats:**
- Lesson #155: Letter Head table has no `module` column
- Lesson #156: Print Format / Notification `module IS NULL` = old stock seeds — need backfill before fixture export

---

## 5. Documentation overview (35 docs across 9 tiers)

> **Verified counts** (from `find docs/handbook -maxdepth 1 -name "*.md" | wc -l` per tier):
> 00-foundations: 2 · 01-schema: 2 · 02-workflow: 2 · 03-client: 5 · 04-runbooks: 4 · 05-process: 2 · 07-user-manuals: 3 · 08-testing: 3 · 09-compliance: 13
> Plus `docs/handbook/README.md` and 67 PDF renders in `pdfs/`.

| Tier | Path | Purpose |
|---|---|---|
| 0 | `docs/handbook/00-foundations/` | ERP / Frappe / HRMS concepts (background for non-ERP readers) |
| 1 | `docs/handbook/01-schema/` | Schema reference + ERD |
| 2 | `docs/handbook/02-workflow/` | Shift management workflow + process diagrams |
| 3 | `docs/handbook/03-client/` | Client demo deck + speaker script + 10 screenshots + 20 mermaid-rendered diagrams |
| 4 | `docs/handbook/04-runbooks/` | Deployment, daily ops, disaster recovery, incident response |
| 5 | `docs/handbook/05-process/` | Change management + post-mortem template |
| 6 | `docs/handbook/09-compliance/` | ISO 27001 + CMM L5 maturity (13 docs — largest tier) |
| 7 | `docs/handbook/07-user-manuals/` | User / Manager / Admin guides |
| 8 | `docs/handbook/08-testing/` | Test plan + test cases + regression script |

**Plus the standalone project docs** (not in handbook/):
- `docs/HARITHA_HOSPITALS_GUIDE.md` (26 KB — comprehensive end-to-end architecture + ops guide)
- `docs/DECISIONS.md` (28+ entries)
- `docs/WORKFLOW.md` (shift management workflow notes)
- `docs/MIGRATION-GUIDE.md` (env replication playbook)
- `docs/PRODUCTION-READINESS-AUDIT.md`
- `docs/pberp-setup-plan.md` (original Phase 2 plan)
- `docs/client-onboarding/` (added 2026-09-09 — process + workbook + sign-offs)

**PDF renders:** `pdfs/` contains 67 PDF versions of these docs for offline / client distribution.

---

## 6. Operational runbooks

All under `docs/handbook/04-runbooks/`:

| Doc | Purpose |
|---|---|
| `04.1-deployment.md` | How to deploy a fresh env from scratch (Docker Compose, app install, fixture load) |
| `04.2-daily-ops.md` | Daily ops checklist (backups, queue health, cron, etc.) |
| `04.3-disaster-recovery.md` | Recovery from DB loss, env destruction, rollback events |
| `04.4-incident-response.md` | P1/P2/P3 incident handling, escalation, comms templates |

Plus `scripts/migrate_master_data.py` (master data migration between envs) and `scripts/recreate_property_setters.py` (idempotent PS recreation — required because HRMS doesn't fixture-export Property Setters).

---

## 7. Critical incidents + lessons learned

### 2026-08-29 — Both envs HTTP 500 (P1 outage)

- **Symptom:** Every page on pberpprod and pberpdev returned HTTP 500 immediately after `bench install-app haritha_hospital` on dev.
- **Cause:** gunicorn `--preload` freezes `sys.path` at container startup; new Python packages added via `install-app` are not picked up by the long-running workers.
- **Fix:** `docker restart <env>-backend-1 <env>-scheduler-1 <env>-queue-short-1 <env>-queue-long-1`. ~30–60s downtime per env.
- **Lesson #153:** Always restart backend + workers after `install-app`. Build this into the post-install script.
- **Data loss:** zero.

### 2026-08-21 — `pberp.duckdns.org` destroyed (rollback event)

- **What:** Environment torn down (Option B: nuke, no backup) at Venkat's authorization.
- **What was lost:** Phase 2–5 deployment work, 24,511 records, all live config (Company, Holidays, Custom Fields), backup cron on vijay@144.217.163.228, nginx/websocket/workers config.
- **What was preserved:** CSV masters (19 files, 1.77 MB), git history, Phase 0/1 design, single Venkat-VPS backup.
- **Lesson:** never destructive ops without explicit recent backup; auto-restore in prod is forbidden.

### Phase 3.6 — Bulk-submit needed 3 runs (Lesson #106)

6,314 Attendance docs needed three back-to-back framework workarounds:
1. Backfill `naming_series` (Lesson #104 — raw SQL bypasses ORM defaults)
2. Add Property Setter for `Holiday` + `Weekly Off` status options
3. Monkey-patch `erpnext.controllers.status_updater.validate_status` (Lesson #105 — Property Setter doesn't bypass controller-level checks)

### Earlier recurring lessons

- **#44:** HRMS v16.5.1+ broken — pin to v16.5.0
- **#46:** After `install-app`, restart backend AND workers (same root cause as #153)
- **#47:** Asset sync after `bench build` requires per-directory `docker cp` with `/.` syntax
- **#79:** `bench backup --with-files` has no built-in timeout — always `timeout 900`
- **#151:** `bench export-fixtures --app X` requires `fixtures = [...]` declaration in `hooks.py`
- **#152:** Frappe v16 uses `module` column, not `app`
- **#157:** Master data migration pattern — upsert via `frappe.get_doc().save()`

---

## 8. Open items / known gaps

### Phase 5 — Production readiness (deferred per Venkat)

Per README: "⏳ skipped per Venkat". Items not done:
- DR test (full env restore from backup)
- Security audit
- SSL audit
- UAT
- Performance baseline

### Other open items

- Cron regression on Aug 26 at 10:06 IST — 3 backup lines (dev_backup.sh, qa_backup.sh, erpclaw-git-daily-backup.sh) were dropped from main VPS crontab. Commit `5f383b6` restored them, but the root cause (likely a `crontab -e` save gone wrong) is unaddressed.
- Real-time employee name mapping fragility: `EMP-1001` (CSV) → `HR-EMP-00001` (DB) relies on a custom formatter; any change to the autoname series will break ingest.
- UI smoke tests inconclusive — Frappe headless browser testing is unreliable (timeouts, false negatives). Real browser verification still needed for new UI work.
- `pberpqa` env skipped — direct dev → prod promotion with custom-app fixtures as the only safety net.

---

## 9. How to navigate this project (for new contributors)

1. **Read this walkthrough first** — you are here.
2. **Read `docs/HARITHA_HOSPITALS_GUIDE.md`** — comprehensive architecture + ops guide (~26 KB).
3. **Read `TRACKER.md`** — it's now a slim index pointing to `tracker-phases/`. Read the relevant phase file for deep history (e.g., `tracker-phases/Phase-4-Shift-Management-Roster-Crash-Fix.md` for the roster work).
4. **Read `docs/handbook/`** — operational docs (foundations → schema → workflow → client → runbooks → process → compliance → user manuals → testing).
5. **Read `.learnings/LEARNINGS.md`** — 159+ known pitfalls; #44, #46, #79, #104-106, #112, #151-157 are the most relevant.
6. **Skim `DECISIONS.md` and `docs/DECISIONS.md`** — 28+ decisions with rationale.
7. **Ask Venkat** for anything not covered. He's the project owner and the only one who knows why some trade-offs were made (e.g., why Option B teardown was authorized, why QA env was skipped).

**Tactical entry points by task:**
- "I need to deploy a new env" → `docs/handbook/04-runbooks/04.1-deployment.md` + `docs/MIGRATION-GUIDE.md`
- "I need to add a Custom Field" → `scripts/recreate_property_setters.py` + the `haritha_hospital` app's fixtures
- "I need to migrate data between envs" → `scripts/migrate_master_data.py`
- "Something crashed" → `docs/handbook/04-runbooks/04.4-incident-response.md` + `LEARNINGS.md`

---

## 10. Appendix: glossary

- **DocType:** A database table in ERPNext (like `Employee`, `Shift Type`, etc.). Defines schema + form + permissions + behavior.
- **Frappe:** Open-source Python+JS framework that ERPNext is built on.
- **ERPNext:** Open-source ERP application built on Frappe (accounting, inventory, selling, buying, etc.).
- **HRMS:** Frappe HR (Human Resources Management System) — separate app on top of ERPNext. Pinned to v16.5.0 in this project (Lesson #44).
- **Custom app:** A user-built Frappe app. Haritha has `haritha_hospital`.
- **Fixtures:** JSON files capturing customizations (Custom Fields, Property Setters, Print Formats, etc.) for git-tracked deployment.
- **Whitelisted method:** A Frappe Python method exposed to the JavaScript client via `@frappe.whitelist()` decorator.
- **Bench:** Frappe's CLI for managing sites, apps, deployments. `bench --site <name> <command>`.
- **Site:** A single Frappe deployment. One site per env here: `pberpdev`, `pberpprod`. (Note: `pberpqa` was created but never used for Haritha.)
- **DocField:** A single field on a DocType (column in the table).
- **Property Setter:** A customization that overrides default DocType properties (e.g., adding a value to a Select field's options). HRMS Property Setters cannot be fixture-exported (Lesson #151).
- **Hooks:** Python entry points in a custom app that respond to events (e.g., `doc_events`, `fixtures`).
- **Master data:** Reference data (Employees, Departments, Shift Types) vs transactional data (Attendance, Checkin).
- **Geo-fencing:** Location-based check-in validation using GPS + radius — out of scope for current project.
- **SSA:** HRMS-native `Shift Schedule Assignment` DocType — recurring template that binds an employee to a shift type. **Has NO `shift_type` or `date` field** (Lesson discovered 2026-08-26).
- **SR:** `Shift Request` DocType — employee-submitted request for a shift change.
- **SS:** `Shift Schedule` DocType — shift template.
- **Lesson:** The numbered entry in `.learnings/LEARNINGS.md`. Currently at #159.
- **Property Setter vs Custom Field:** Custom Field = adds a new field. Property Setter = modifies an existing field's property (options, default, mandatory, etc.).
