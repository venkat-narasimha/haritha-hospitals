# Haritha Hospitals

**Project:** Haritha Hospitals — Real hospital project (CMM Level 5 target).
**Owner:** Venkat (Processbricks).
**Started:** 2026-08-19.
**Scope:** Shift management + HRMS basics (employees, departments, shift types, attendance, leave). Out of scope (deferred): wards, beds, OTs, pharmacy, lab, billing, full CoA, cost centers.

## 🔄 Project Status (2026-08-21 10:33 IST)

**Restart from Phase 1.** The Phase 2 deployment (pberp.duckdns.org) was destroyed in a teardown at 10:11–10:18 IST 2026-08-21 (Option B: nuke only, no backup). 24,511 records + deployment artifacts lost. Phase 0 + 1 design preserved (CSVs + git history intact). Phases 2–5 need redo. New env domain TBD. See `TRACKER.md` for full details.

## Stack

- Frappe 16.x
- ERPNext 16.x
- HRMS 16.5.0 (pinned per lesson #44 — v16.5.1+ breaks on `repost_allowed_types`)
- Payments (optional)
- Custom app: TBD (pberp_hospital patterns as reference)

## Files

- `TRACKER.md` — Project tracker (status, phases, decisions, subagent log)
- `README.md` — This file (project overview)
- `all_schemas.csv` — Schema definitions for 15 master entities (single CSV, schema-only)
- `docs/` — Project documentation (TBD)
- `fixtures/` — Frappe fixtures (TBD — Rule #9 compliance from day 1)
- `mapping/` — Data mapping rules (TBD)
- `scout/` — Source data scout reports (TBD)
- `scripts/` — Utility scripts (TBD)

## How to Use

1. **Schema Review:** Open `all_schemas.csv` — each row = field definition (15 entities, ~95 fields).
2. **Tracker:** Open `TRACKER.md` — phase status, decisions, subagent log.
3. **Approval:** User reviews `all_schemas.csv` and approves/adjusts before any data import.

## Reference

- pberpqa hospital demo: `../pberpqa-hospital-demo/` (NOT perfect — gaps documented)
- Source data: `../../uploads/pberpqa-real-data-for-demo/roster_and_attendance_june.xlsx` (210 employees, 36 depts, 51 desigs, 31 shift codes)

## Conventions

- File naming: kebab-case for files, snake_case for data
- Git: all commits as `venkat-narasimha <srivenkatnarasimha@gmail.com>` (per rule #11)
- Custom Fields: every field in fixtures from day 1 (per Rule #9)
- HRMS pin: v16.5.0 only (per lesson #44)
- Holidays: standard Indian national + 4-5 Telangana
- Shift codes: 10-char `[P][HHMM][S][HHMM]` (Option A, HRMS-native flags)

---

*Last updated: 2026-08-21 10:33 IST — restart-from-Phase-1 update after pberp teardown*
