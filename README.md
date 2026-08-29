# Haritha Hospitals

ERPNext + HRMS deployment for **Processbricks' Haritha Hospitals** project — a real hospital shift-management and HRMS rollout. Built on Frappe v16 with a custom app (`haritha_hospital`) that captures all customizations as portable fixtures, plus a migration playbook for replicating any env.

| | |
|---|---|
| **Owner** | Venkat Narasimha (Processbricks) |
| **Started** | 2026-04-01 (concept); project on this repo 2026-08-19 |
| **Stack** | Frappe v16.30.0 · ERPNext v16.30.0 · HRMS v16.5.0 (pinned) · custom app `haritha_hospital` |
| **Envs** | `pberpprod.duckdns.org` (prod) · `pberpdev.duckdns.org` (dev) · `dev-erp.duckdns.org` (Venkat VPS prototyping) |
| **Scope** | Shift management + HRMS basics (employees, departments, shift types, attendance, leave) |
| **Out of scope** | Wards, beds, OTs, pharmacy, lab, billing, full Chart of Accounts, cost centers beyond the 2 created (deferred) |

---

## Project Status (2026-08-29)

- **Custom app `haritha_hospital` built** — captures **274 production-validated customizations** as Frappe JSON fixtures (78 Custom Fields + 189 Property Setters + 3 Print Formats + 2 Notifications + 2 Letter Heads).
- **Installed on both envs** — `pberpdev` (fresh, all 274 loaded) and `pberpprod` (idempotent re-install verified, `installed_apps` updated, count matches).
- **Master data migrated prod → dev** — 16 DocTypes via `scripts/migrate_master_data.py`. pberpdev now mirrors prod: 1 Company, 210 Employees, 37 Departments, 25 Shift Types, 8,118 Shift Assignments, 6,300 Attendance, 12,562 Employee Checkins, etc.
- **Phase 6 documentation complete** — 22 docs across 8 tiers (`docs/phase6/`), ~10,000 lines, Mermaid diagrams, Tier 0-8 incremental review structure.
- **P1 outage resolved (2026-08-29 03:06 IST)** — gunicorn `--preload` sys.path freeze after `install-app`; both envs restarted (~30-60s downtime each, zero data loss). Always restart backend after `install-app` (LEARNINGS #153).
- **Roster SPA verified rendering** — Phase 4.10/4.11 fixes held; `/hr/roster` shows 211 employees × 31 days without crash.

| Phase | State |
|---|---|
| Phase 0 — Schema planning | ✅ done |
| Phase 1 — Schema approval | ✅ done |
| Phase 2 — Site setup (pberpprod) | ✅ done |
| Phase 3 — Data import (24,511 records) | ✅ done |
| Phase 3.5–3.10 — Reconcile / bulk-submit / property setters / linkage | ✅ done |
| Phase 4 — Roster crash + Attendance HRMS-recompute | ✅ done |
| Phase 0+ — Custom app + master data migration + outage recovery | ✅ done |
| Phase 5 — Production readiness (DR, security, perf, UAT) | ⏳ skipped per Venkat |
| Phase 6 — Process & maturity docs | ✅ done (2026-08-29) |

---

## Stack

- **Frappe** v16.30.0 — foundation framework
- **ERPNext** v16.30.0 — accounting, inventory, selling, buying
- **HRMS** v16.5.0 — pinned per Lesson #44 (v16.5.1+ breaks on `repost_allowed_types`)
- **MariaDB** 10.x — Docker named volumes, restart-safe
- **Redis** — cache + queue broker; Socket.IO for realtime desk
- **Docker Compose** — compose-based deployment (`erp-{env}-*` containers on main VPS, `erpdev-*` on Venkat VPS)
- **nginx-proxy** — reverse proxy with TLS termination (DuckDNS + Let's Encrypt / self-signed fallback)
- **Custom app** `haritha_hospital` (0.0.1) — owns the 274 customizations as fixtures
- **Python 3.11** — Frappe v16 baseline
- **3 environments**: `pberpdev` (dev), `pberpqa` (QA — skipped for Haritha per Venkat), `pberpprod` (prod)

---

## Repo layout

| Path | Purpose |
|---|---|
| `TRACKER.md` | Project tracker — phase history, subagent log, decisions |
| `README.md` | This file — top-level project overview |
| `HARITHA_HOSPITALS_GUIDE.md` | *(at `docs/HARITHA_HOSPITALS_GUIDE.md`)* — comprehensive end-to-end guide (architecture, customizations, migration, ops) |
| `INDEX.md` | Curated reading index |
| `DECISIONS.md` | Decision log |
| `WORKFLOW.md` | Shift management workflow notes |
| `PRODUCTION-READINESS-AUDIT-2026-08-21.md` | Pre-rollback audit |
| `MIGRATION-GUIDE.md` | Migration playbook reference |
| `all_schemas.csv` | Schema definitions for 15 master entities (schema-only, single CSV) |
| `masters/` | Source CSVs — 19 files, ~1.77 MB, 24,758 rows (Company, Department, Designation, Employee, Shift Type, Shift Assignment, Attendance, Employee Checkin, etc.) |
| `docs/` | Documentation — `HARITHA_HOSPITALS_GUIDE.md` + `phase6/` (Tier 0-8) + `pberp-setup-plan.md` |
| `docs/phase6/` | **Phase 6 documentation** — 22 docs, 8 tiers, ~10,000 lines (foundations, schema, workflow, client, runbooks, process, user manuals, testing) |
| `scripts/` | Utility scripts (≈45 files) — `migrate_master_data.py`, `recreate_property_setters.py`, `bulk_submit.py`, `fix_attendance_hrms_recompute.py`, `verify_csvs.py`, `update_tracker.py`, etc. |
| `fixtures/` | Legacy fixtures dir (pre-custom-app) |
| `mapping/` | Data mapping rules |
| `scout/` | Source data scout reports |
| `phase-a/` | Phase A fixtures bundle (`fixtures.tar.gz`) + `REPORT.md` + `logs/` |
| `audit/` | Fixture audit reports (pberpprod detail + summary) |
| `config/` | `cron.tab` for backup cron |
| `updates/` | Phase update JSON snapshots |
| `reports/` | Generated reports |
| `.gitignore` | Standard Frappe ignores |

> There is no `memory/` or `uploads/` at this level. Daily logs and source data live in the OpenClaw workspace, not the project repo.

---

## Customizations catalog

All captured as Frappe fixtures in the `venkat-narasimha/haritha_hospital` custom app repo (`apps/haritha_hospital/haritha_hospital/fixtures/`).

| Type | Count | Notes |
|---|---:|---|
| Custom Fields | 78 | Employee (PAN, IFSC, approvers), Company (Payroll cost center), Attendance (status extensions), Shift Type (color + HRMS flags), Shift Assignment (Dept link), Holiday List (Telangana regional), Leave Application workflow |
| Property Setters | 189 | Largest category — ~120 HRMS, ~50 ERPNext, ~19 Frappe core. Status options, defaults, mandatory toggles, field order |
| Print Formats | 3 | Payslip, Shift Card, Leave Application |
| Notifications | 2 | Both disabled (Shift assignment change + Leave approval pending) |
| Letter Heads | 2 | Haritha Hospitals (default) + Haritha Hospitals — Confidential (HR/Payroll) |
| **Total** | **274** | ✅ All production-validated on both `pberpdev` and `pberpprod` |

---

## Quick links

- **[HARITHA_HOSPITALS_GUIDE.md](docs/HARITHA_HOSPITALS_GUIDE.md)** — comprehensive guide (architecture, customizations, migration, ops runbook)
- **[TRACKER.md](TRACKER.md)** — phase-by-phase history + subagent log
- **[docs/phase6/](docs/phase6/)** — Phase 6 Tier 0-8 documentation (foundations, schema, workflow, runbooks, user manuals, testing)
- **[scripts/migrate_master_data.py](scripts/migrate_master_data.py)** — idempotent master data migration (16 DocTypes, 10 gotchas documented)
- **[scripts/recreate_property_setters.py](scripts/recreate_property_setters.py)** — idempotent Property Setter recreate (HRMS doesn't list `Property Setter` as a fixture)
- **[masters/](masters/)** — 19 source CSVs (canonical reference)
- **[INDEX.md](INDEX.md)** — curated reading index

---

## Key operational links

- **Prod:** https://pberpprod.duckdns.org
- **Dev:** https://pberpdev.duckdns.org
- **Venkat VPS prototype:** https://dev-erp.duckdns.org
- **Roster SPA:** https://pberpprod.duckdns.org/hr/roster

---

## Conventions (current)

- **Git commits:** `venkat-narasimha <srivenkatnarasimha@gmail.com>` (Rule #11)
- **Custom Fields:** all in `haritha_hospital` fixtures from day 1 (Rule #9)
- **HRMS pin:** v16.5.0 only (Lesson #44 — v16.5.1+ breaks on `repost_allowed_types`)
- **Shift codes:** 10-char `[P][HHMM][S][HHMM]` (actual format `[GMAN]\d{4}[RS]\d{4}` — HRMS-native flags)
- **Color palette:** G=blue, M=green, A=orange, N=violet (lowercase Tailwind, matching `MonthViewTable.vue`)
- **Always restart backend container** after `bench install-app` (Lesson #153 — gunicorn `--preload` sys.path freeze)
- **DB passwords verified monthly** via `docker exec erp-${env}-db-1 printenv MYSQL_ROOT_PASSWORD` (Lesson #154)
- **Holidays:** standard Indian national + 4-5 Telangana regional
- **QA env skipped** for Haritha — direct dev → prod promotion with custom-app fixtures as the safety net

---

## Recent milestones

- **2026-08-29 — Phase 6 docs complete** — 22 docs across 8 tiers (`docs/phase6/`), ~10,000 lines, Mermaid diagrams
- **2026-08-29 — Master data migration prod → dev** — 16 DocTypes via `migrate_master_data.py`; 8,118 Shift Assignments on dev, all bulk-submitted; idempotent script saved
- **2026-08-29 — P1 outage resolved** — gunicorn `--preload` sys.path freeze; both envs restarted, zero data loss; LEARNINGS #153
- **2026-08-28 — Custom app `haritha_hospital` installed** — 274 customizations verified on both envs; idempotent
- **2026-08-28 — Phase 4.10/4.11 Roster crash fixed** — CapitalCase → lowercase Tailwind colors; SPA now renders 211 × 31 cleanly
- **2026-08-28 — Phase 4.8 Attendance HRMS-recompute** — 6,300 → 9,734 Attendance records; `early_exit` count 7 → 1,498 (the main bug from Phase 3.8)
- **2026-08-27 — Phase 3.6/3.7/3.8/3.9/3.10** — bulk-submit 6,314 docs, recreate_property_setters.py, attendance linkage, populate fields, backup bundle fix
- **2026-08-26 — Phase 3 data import** — 24,511 records across 9 entities
- **2026-08-25 — Phase 2 site setup** — pberpprod.duckdns.org fresh init + apps installed (frappe, erpnext, hrms 16.5.0, payments)
- **2026-08-21 — Rollback event** — `pberp.duckdns.org` env destroyed in Option-B teardown; preserved CSVs + git history; restart from Phase 1

---

## References

- **Custom app repo:** https://github.com/venkat-narasimha/haritha_hospital (custom app + 274 fixtures)
- **Frappe docs:** https://docs.frappe.io/
- **HRMS docs:** https://docs.frappe.io/hr/
- **Frappe framework:** https://frappeframework.com/docs/
- **LEARNINGS:** `/root/.openclaw/workspace/.learnings/LEARNINGS.md` (workspace-level, includes #44, #106, #114, #142-#150, #151-#157)
- **MEMORY:** `/root/.openclaw/workspace/MEMORY.md` (workspace-level tech stack + DB passwords)

---

*Last updated: 2026-08-29 — refreshed after Phase 6 completion + custom-app build + master data migration + P1 outage recovery*
