# Project Status — Haritha Hospitals ERPNext + HRMS Deployment

**Date:** 2026-09-21 (refreshed with Sep 17-21 events; originally relocated from root README.md on 2026-09-15)
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

## Demo Readiness Status (2026-09-21)

Final readiness check after all cleanup work landed on `main`. Every area PASS, no caveats.

| Area | Verdict |
|---|---|
| Custom Fields | ✅ PASS (78/78, 189/189 — perfect fixture match) |
| Leave Engine | ✅ PASS (Leave Approver, Holiday List per Employee, Leave Period, Allocations seeded, Notifications configured) |
| Branches | ✅ PASS-INTENTIONAL (Test Company kept per operator decision 2026-09-17) |
| HR Settings | ✅ PASS (standard_working_hours=8.0, leave_approver_mandatory=1, leave_approval_notification_template set) |
| **Overall** | **✅ READY (full, no caveats)** as of 2026-09-21 |

## Recent milestones

- **2026-09-21 — Demo readiness REACHED (full, no caveats)** — All areas PASS after final clean-up: 211 Holiday List Assignments batch-submitted, transactions renumbered T1-T60 → T-001-T-079 (added 19 new entries), scrub hotfix removed internal refs, 3 existing + 5 new master template commits landed
- **2026-09-21 — 5 new master templates added** — Fiscal Year, Skill, Onboarding Template, Separation Template, Holiday List Assignment (current `main` HEAD)
- **2026-09-21 — 3 existing client templates updated** — Department (add `leave_approvers`), HR Settings (add Workflow + Email Account sections), README (link `settings_checklists/`)
- **2026-09-21 — Scrub hotfix on synthesized report** — removed 7 internal-infrastructure references per operator feedback
- **2026-09-21 — Transactions renumbered to T-001-T-079** — T1-T60 replaced by properly-flowing numbering; 19 new setup transactions added across Sections A/B/C; sign-off grew to 77 PASS / 0 DEFERRED / 1 NOT DONE / 1 REMOVED
- **2026-09-21 — 211 Holiday List Assignments batch-submitted** — all rows promoted docstatus 0 → 1 via per-doc `hla.submit()` (Stream 3B raw SQL INSERT left them in Draft; one-shot fix, 0 errors)
- **2026-09-19 — Sample Leave Application submitted end-to-end** — `HR-LAP-2026-00001`, Casual Leave -1.0 day on 2026-10-02, Leave Ledger Entry created. Three-attempt retry: caught NotificationTemplate-vs-Email-Template schema gap; HR Settings `leave_approval_notification_template` set; caught Holiday List Assignment `docstatus=0` bug → fix via `hla.submit()` on `HR-HLA-2026-00003`; third attempt succeeded
- **2026-09-19 — Fiscal Years created on Haritha Hospitals** — FY 2025-2026 (2025-04-01 → 2026-03-31) and FY 2026-2027 (2026-04-01 → 2027-03-31), both linked to Haritha Hospitals
- **2026-09-19 — Stream 5 Maximum effort** — 4 prod docs created (`HR-EMP-ONT-00001` Onboarding Template, `HR-EMP-00422` Ex-Employee status=Left, `HR-EMP-STP-00001` Separation Template, `HR-EMP-SEP-2026-00001` Separation draft); 3 write-tests added for T52/T57/T58; T60 removed (sign-off updated to 58 PASS)
- **2026-09-18 — Manual transaction testing complete (60 transactions, 6 modules)** — Venkat's manual report uploaded + Streams 1-4 executed end-to-end:
  - Stream 1 — Investigation of pending T-items: 8 PASS / 4 FAIL-SYSTEMIC / 13 FAIL-MANUAL / 3 FAIL-DATA / 4 UNCLEAR (~36 KB written)
  - Stream 2 — 13 manual corrections + 7 inline notes applied to both test docs (test docs grew: 1,203 → 1,262 lines; 1,015 → 1,087 lines)
  - Stream 3 — Leave setup on prod (Leave Approver on Department X-HH, Holiday List on Test User, Leave Period 2026-2027 `HR-LPR-2026-00001`, 3 Leave Allocations submitted for Test User: Earned=12d / Casual=12d / Sick=6d, sample Leave Application drafted `HR-LAP-2026-00001`)
  - Stream 3B — Fix 1: HR Settings `standard_working_hours = 8.0`; Fix 2: 211 Holiday List Assignments created (after schema catch for `applicable_for` + `assigned_to`)
  - Stream 4 — Sign-off checkboxes + sanitization grep (initial sign-off: 59 rows)
  - Push to `main`
- **2026-09-17 — Demo readiness audit + 1 prod fix applied** — Audit surfaced 3 issues; operator decisions recorded (skip FY for now, apply Holiday List, keep Test Company intentionally); audit doc grew to ~205 lines after operator decisions. Backup taken, then applied `Company.default_holiday_list = "Haritha Hospitals Holiday List"` on Haritha Hospitals


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

*Relocated from root README.md on 2026-09-15 as part of repo wayfinding cleanup. Refreshed with Sep 17-21 events on 2026-09-21 (last meaningful status update: 2026-09-21).*
