# Project Status — Haritha Hospitals ERPNext + HRMS Deployment

**Date:** 2026-09-15 (relocated from root README.md → slim navigation + status content split)
**Context:** The rich project status (phase history, stack inventory, customizations catalog, recent milestones) used to live in the root `README.md`. It's now archived here as part of Option B (slim root README + relocate status).

This doc contains the historical snapshot of all phases + deliveries up to Sep 10, 2026.

---

## Project Status (as of 2026-08-31)

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
| Phase 6 — Process & maturity docs | ✅ done (35 docs, 9 tiers, 2026-08-29) |
| Phase 6 — Tier 6 Compliance/Maturity | ✅ done (12 docs: ISO 27001 + CMM L5, 2026-08-29) |
| Client demo deck + script | ✅ done (2026-08-30) |

### Headline numbers

- **Custom app `haritta_hospital` built** — **274 production-validated customizations** as Frappe JSON fixtures (78 Custom Fields + 189 Property Setters + 3 Print Formats + 2 Notifications + 2 Letter Heads)
- **Installed on both envs** — `pberpdev` (fresh, all 274 loaded) and `pberpprod` (idempotent re-install verified)
- **Master data migrated prod → dev** — 16 DocTypes via `scripts/migrate_master_data.py`. pberpdev now mirrors prod: 1 Company, 210 Employees, 37 Departments, 25 Shift Types, 8,118 Shift Assignments, 6,300 Attendance, 12,562 Employee Checkins
- **Phase 6 + Tier 6 documentation complete** — 35 docs across 9 tiers (`docs/handbook/`), ~15,900 lines
- **P1 outage resolved (2026-08-29 03:06 IST)** — gunicorn `--preload` sys.path freeze; both envs restarted; always restart backend after `install-app` (LEARNINGS #153)
- **Roster SPA verified rendering** — Phase 4.10/4.11 fixes held; `/hr/roster` shows 211 employees × 31 days without crash

---

## Recent Deliverables (2026-08-30)

| Deliverable | Path | Notes |
|---|---|---|
| **Client demo deck** | `docs/handbook/03-client/03.4-client-presentation.pptx` | 11 slides, 543 KB, screenshots + diagrams embedded |
| **Speaker script** | `docs/handbook/03-client/03.5-speaker-script.md` | Talking notes for each slide |
| **Demo screenshots** | `docs/handbook/03-client/screenshots/` | 10 PNGs from pberpprod (login, dashboard, roster, etc.) |
| **Diagram assets** | `docs/handbook/03-client/assets/` | 20 mermaid-rendered PNGs |
| **Phase 6 + Tier 6 docs** | `docs/handbook/` | 35 docs, ~15,900 lines, 9 tiers |

---

## Stack

- **Frappe** v16.30.0 — foundation framework
- **ERPNext** v16.30.0 — accounting, inventory, selling, buying
- **HRMS** v16.5.0 — pinned per Lesson #44 (v16.5.1+ breaks on `repost_allowed_types`)
- **MariaDB** 10.x — Docker named volumes, restart-safe
- **Redis** — cache + queue broker; Socket.IO for realtime desk
- **Docker Compose** — compose-based deployment (`erp-{env}-*` containers on main VPS, `erpdev-*` on Venkat VPS)
- **nginx-proxy** — reverse proxy with TLS termination (DuckDNS + Let's Encrypt / self-signed fallback)
- **Custom app** `haritta_hospital` (0.0.1) — owns the 274 customizations as fixtures
- **Python 3.11** — Frappe v16 baseline
- **3 environments**: `pberpdev` (dev), `pberpqa` (QA — skipped for Haritha per Venkat), `pberpprod` (prod)

---

## Customizations catalog

All captured as Frappe fixtures in the `venkat-narasimha/haritha_hospital` custom app repo.

| Type | Count | Notes |
|---|---:|---|
| Custom Fields | 78 | Employee (PAN, IFSC, approvers), Company (Payroll cost center), Attendance (status extensions), Shift Type (color + HRMS flags), Shift Assignment (Dept link), Holiday List (regional), Leave Application workflow |
| Property Setters | 189 | ~120 HRMS, ~50 ERPNext, ~19 Frappe core. Status options, defaults, mandatory toggles, field order |
| Print Formats | 3 | Payslip, Shift Card, Leave Application |
| Notifications | 2 | Both disabled |
| Letter Heads | 2 | Haritha Hospitals (default) + Haritha Hospitals — Confidential (HR/Payroll) |
| **Total** | **274** | ✅ All production-validated on both `pberpdev` and `pberpprod` |

---

## Conventions

- **Git commits:** `venkat-narasimha <srivenkatnarasimha@gmail.com>`
- **Custom Fields:** all in `haritta_hospital` fixtures from day 1
- **HRMS pin:** v16.5.0 only
- **Always restart backend container** after `bench install-app`
- **DB passwords verified monthly** via `docker exec erp-${env}-db-1 printenv MYSQL_ROOT_PASSWORD`
- **Holidays:** standard Indian national + 4-5 Telangana regional
- **QA env skipped** for Haritha — direct dev → prod promotion with custom-app fixtures as the safety net

---

## Recent milestones

- **2026-08-29 — Phase 6 docs complete** — 22 docs across 8 tiers, ~10,000 lines, Mermaid diagrams
- **2026-08-29 — Master data migration prod → dev** — 16 DocTypes; 8,118 Shift Assignments on dev, all bulk-submitted
- **2026-08-29 — P1 outage resolved** — gunicorn `--preload` sys.path freeze; zero data loss
- **2026-08-28 — Custom app `haritta_hospital` installed** — 274 customizations verified on both envs
- **2026-08-28 — Phase 4.10/4.11 Roster crash fixed** — CapitalCase → lowercase Tailwind colors; SPA renders 211 × 31 cleanly
- **2026-08-28 — Phase 4.8 Attendance HRMS-recompute** — 6,300 → 9,734 records
- **2026-08-27 — Phase 3.6/3.7/3.8/3.9/3.10** — bulk-submit 6,314 docs, attendance linkage
- **2026-08-26 — Phase 3 data import** — 24,511 records across 9 entities
- **2026-08-25 — Phase 2 site setup** — pberpprod.duckdns.org fresh init + apps installed
- **2026-08-21 — Rollback event** — `pberp.duckdns.org` env destroyed in teardown; restart from Phase 1

---

## More status docs

- **[TRACKER.md](https://github.com/venkat-narasimha/haritha-hospitals/blob/main/TRACKER.md)** — phase-by-phase history + subagent log
- **[docs/HARITHA_HOSPITALS_GUIDE.md](../../HARITHA_HOSPITALS_GUIDE.md)** — comprehensive end-to-end guide (corrected from `../HARITHA_HOSPITALS_GUIDE.md` which resolved to `docs/handbook/HARITHA_HOSPITALS_GUIDE.md` 404)
- **[DECISIONS.md](https://github.com/venkat-narasimha/haritha-hospitals/blob/main/docs/DECISIONS.md)** — decision log

---

*Relocated from root README.md on 2026-09-15 as part of repo wayfinding cleanup. Last meaningful status update: 2026-09-10.*
