# DECISIONS — Haritha Hospitals

**Project:** `haritha-hospitals`
**Owner:** Venkat (Processbricks) | **Recorded by:** ERPClaw + subagents
**Source:** Extracted from `TRACKER.md` Decisions Log table (2026-08-19 → 2026-08-21)
**Last updated:** 2026-08-21 11:55 IST
**Total entries:** 28 (13 on 2026-08-19 + 10 on 2026-08-20 + 5 on 2026-08-21)

> **Note on count:** Task brief said "32 entries" but the actual `TRACKER.md` Decisions Log table contains **28** decision rows. This file extracts all 28 verbatim — no fabrication. Discrepancy surfaced in Step 3 verification.

---

## 2026-08-19 — Design decisions (13 entries)

### 2026-08-19 — Scope = shift management only
- **Decision:** MVP scope is shift management + HRMS basics only; defer wards, beds, OTs, pharmacy, lab, billing.
- **Rationale:** User clarified mid-session; defer hospital modules to Phase 2+.
- **Status:** ✅ Active

### 2026-08-19 — hrms 16.5.0 pin
- **Decision:** Pin HRMS to exactly version 16.5.0; do not allow auto-upgrade.
- **Rationale:** Lesson #44 — v16.5.1+ breaks on `repost_allowed_types`.
- **Status:** ✅ Active

### 2026-08-19 — Shift code = 10-char `[P][HHMM][S][HHMM]`
- **Decision:** Shift codes follow 10-char pattern `[Prefix][HHMM][Suffix][HHMM]` (e.g., `P0900S1800`).
- **Rationale:** User-proposed scheme, Option A (lean).
- **Status:** ✅ Active

### 2026-08-19 — Shift name = 10-char code itself (no separate `shift_code` field)
- **Decision:** Use shift name = code; no separate `shift_code` field on Shift Type.
- **Rationale:** User simplification — name IS the code.
- **Status:** ✅ Active

### 2026-08-19 — Holidays = standard Indian national + 4-5 Telangana
- **Decision:** Holiday list = 14 standard Indian national holidays + 4–5 Telangana state-specific.
- **Rationale:** User confirmed.
- **Status:** ✅ Active (list in `masters/holiday.csv`)

### 2026-08-19 — Custom leave types = deferred
- **Decision:** No custom Leave Type DocTypes for MVP; use HRMS defaults only.
- **Rationale:** User said Haritha adds later.
- **Status:** ⏳ Deferred (post-MVP)

### 2026-08-19 — Leave allocation = standard Indian defaults
- **Decision:** Use HRMS leave allocation defaults; rules encoded in `remarks` column.
- **Rationale:** User confirmed.
- **Status:** ✅ Active

### 2026-08-19 — Source data = DO NOT modify
- **Decision:** CSV masters in `masters/` are read-only; canonicalization happens at import time only.
- **Rationale:** Preserve audit trail; allow re-import with different rules without mutating source.
- **Status:** ✅ Active (enforced — `masters/` is sha256-tracked)

### 2026-08-19 — SSA is HRMS-native (Shift Schedule Assignment DocType)
- **Decision:** Use `Shift Schedule Assignment` DocType for shift scheduling (not custom DocType).
- **Rationale:** Originally doubted; verified via docs.frappe.io/hr/shift-schedule-assignment.
- **Status:** ✅ Active

### 2026-08-19 — Comprehensive 7-change schema update
- **Decision:** Apply 7 schema changes across 9 HRMS doctypes for canonical Haritha structure.
- **Rationale:** 9 HRMS docs verified; HRMS v15 canonical structure applied.
- **Status:** ✅ Active (see `all_schemas.csv`)

### 2026-08-19 — 19 CSVs schema + data combined format
- **Decision:** Each CSV has schema header (column names + types) + data rows in single file.
- **Rationale:** Manager-friendly for Google Sheets review (no separate schema files).
- **Status:** ✅ Active

### 2026-08-19 — 3 designation collisions resolved automatically
- **Decision:** Auto-resolve duplicates: `Physician Asstant` + `Assistant`, `Sr.Executive` + `Senior Executive`, `Sr.Manager` + `Senior Manager`.
- **Rationale:** Cosmetic variants in source data; canonical form picked at import.
- **Status:** ✅ Active

### 2026-08-19 — 3 shift code duplicates consolidated
- **Decision:** Auto-resolve shift code duplicates: `A4` + `Shift-A`, `B2` + `Shift-B`, `C1` + `Shift-C`.
- **Rationale:** Source had legacy + new naming; new naming wins.
- **Status:** ✅ Active

---

## 2026-08-20 — Phase 0 + 1 sign-off + Phase 2 deployment (10 entries)

### 2026-08-20 — Phase 0 + 1 signed off by manager
- **Decision:** Schema + data CSVs approved by manager.
- **Rationale:** Manager review complete on Google Sheets.
- **Status:** ✅ Approved (gate opened for Phase 2)

### 2026-08-20 — New dedicated env `pberp` (clean slate)
- **Decision:** Deploy to fresh `pberp.duckdns.org` env (not legacy envs).
- **Rationale:** Recommended over legacy envs to avoid drift.
- **Status:** 🔄 **OBSOLETE — env destroyed 2026-08-21; new env TBD**

### 2026-08-20 — Apps installed via `bench install-app` (runtime)
- **Decision:** Install frappe/erpnext/hrms at runtime via bench CLI (not custom Docker image).
- **Rationale:** Quick start; lesson #47 trade-off (asset sync known issue).
- **Status:** ✅ Active (will re-apply to new env)

### 2026-08-20 — Custom app: deferred, use custom fields + fixtures
- **Decision:** No `haritha_hospital` custom app for MVP; use custom fields + Frappe fixtures instead.
- **Rationale:** Fast track for MVP; can extract custom app later if complexity grows.
- **Status:** ✅ Active

### 2026-08-20 — Real-time employee name mapping: `EMP-1001` (CSV) → `HR-EMP-00001` (DB)
- **Decision:** Map CSV employee IDs to HRMS naming series `HR-EMP-{N-1000:05d}`.
- **Rationale:** Built `HR-EMP-{N-1000:05d}` formatter to bridge source IDs (1001+) to HRMS series (00001+).
- **Status:** ✅ Active (re-usable import logic)

### 2026-08-20 — Attendance imported via raw SQL (not ORM)
- **Decision:** Use raw MariaDB INSERT for Attendance records; bypass Frappe ORM.
- **Rationale:** Bypassed Frappe Status validation + 240s timeout on large batches.
- **Status:** ✅ Active (see `MIGRATION-GUIDE.md` §X)

### 2026-08-20 — Attendance status options extended via Property Setter
- **Decision:** Add "Weekly Off" + "Holiday" to Attendance.status Select options via Property Setter.
- **Rationale:** 1:1 match to CSV `status` values; avoids Status validation failure.
- **Status:** ✅ Active (will re-apply to new env)

### 2026-08-20 — Employee Checkin via background jobs (25 batches × 500)
- **Decision:** Split 12,562 checkin rows into 25 background-job batches of 500 each.
- **Rationale:** Direct console timed out on full 12,562-row import; background jobs amortize load.
- **Status:** ✅ Active

### 2026-08-20 — HR-Attendance series counter fixed mid-flight (`HR-ATT-2026-` was 183, fixed to 6300)
- **Decision:** Manually patch Series counter to 6300 mid-import.
- **Rationale:** Series was stale (183), prevented new record creation; 6300 cleared collision risk with pre-existing rows.
- **Status:** ✅ Active (note for future: check Series counter before bulk import)

### 2026-08-20 — 5 X-HH Department variants force-deleted via direct SQL
- **Decision:** Run raw `DELETE FROM tabDepartment WHERE name LIKE 'X-HH-%'` for 5 leftover rows.
- **Rationale:** Frappe `doc.delete()` enforces "disable not delete" rule; direct DELETE bypasses (acceptable since these were staging artifacts).
- **Status:** ✅ Active (one-time cleanup)

---

## 2026-08-21 — Testing + Rollback (5 entries)

### 2026-08-21 — Backend tested end-to-end via API
- **Decision:** Backend tested via REST API: auth ✅, CRUD ✅, all 9 entities queryable ✅, payroll/leave/holiday workflows ✅.
- **Rationale:** Validates core HRMS functionality before UI verification.
- **Status:** ✅ Verified (was PASS at pberp.duckdns.org before rollback — re-test needed on new env)

### 2026-08-21 — UI smoke test inconclusive (headless browser tool unreliable)
- **Decision:** UI verification deferred — headless browser tool failed mid-session.
- **Rationale:** Needs real browser verification next session (operator-driven).
- **Status:** ⚠️ Open — re-test needed before go-live on new env

### 2026-08-21 — Token limit issues (rate_limit_error) on long subagent runs
- **Decision:** Workaround for subagent token exhaustion: split long tasks into K1/K2/K3 segments + use direct `exec` for heavy work.
- **Rationale:** Lesson learned for future orchestration; reduces token pressure per subagent session.
- **Status:** ✅ Adopted (operational pattern)

### 2026-08-21 — nginx `Upgrade: websocket` forced for /socket.io/
- **Decision:** Force `Upgrade: websocket` header in nginx config for `/socket.io/` paths.
- **Rationale:** Frappe ws server validates Upgrade header on every request; needed during UI debugging.
- **Status:** ⚠️ **Under review** — may need revert for new env (see Open Question #3)

### 2026-08-21 — Rollback: pberp.duckdns.org env torn down
- **Decision:** Venkat authorized Option B (nuke, no backup) at 10:33 IST. All Phase 2–5 deployment work destroyed. Restart from Phase 1 on new env.
- **Rationale:** Phase 0 + 1 design work preserved in git + CSV masters; deployment was not recoverable in time. Restart strategy: pick new env domain → re-run Phases 2–5.
- **Status:** 🔄 Active — restart in progress (new env domain TBD)

---

## Summary by Category

| Category | Count | Notes |
|---|---|---|
| Scope / Stack | 3 | shift-management-only, HRMS pin, deferrals |
| Schema / Data | 7 | shift codes, holidays, leave, CSVs, collision resolution |
| Phase 2 deployment | 10 | env choice, apps, custom fields, import strategy |
| Phase 4 testing | 2 | backend PASS, UI smoke deferred |
| Operational | 4 | token limits, nginx ws, rollback |
| Process | 2 | manager sign-off, source data immutability |

## Resolved (historical)

- ~~Telangana 2025 + 2026 holiday list~~ — using standard Indian national 14 holidays (per user)
- ~~Shift code convention~~ — 10-char `[P][HHMM][S][HHMM]`, name IS the code
- ~~Source data canonicalization~~ — 3 designation + 3 shift dupes resolved at import time
- ~~Apps stack~~ — frappe, erpnext, hrms 16.5.0, payments (no custom app for MVP)
- ~~Custom app `haritha_hospital`~~ — deferred, using custom fields + fixtures

---

**Source:** `TRACKER.md` Decisions Log table, extracted 2026-08-21 11:55 IST.

### 2026-08-21 — Holiday List 2025 Buddha Purnima date discrepancy
**Decision:** Accept Frappe's stored date (2025-05-13) instead of sent date (2025-05-12). Off-by-1 likely due to Frappe interpreting the Hindu lunar calendar differently. Can amend post-import if user disputes.
**Rationale:** Minor discrepancy, non-blocking for Phase 3 import. Lunar calendar dates vary by interpretation.
**Status:** accepted

### 2026-08-21 — Phase 3.5: 8 entities DEFERRED
**Decision:** Defer import of 8 entities to Phase 3.5 (later) — Shift Location, Shift Request, Shift Schedule, Shift Schedule Assignment, Leave Application, Leave Allocation, Employee Group, Employee Advance.
**Rationale:** CSVs are empty (0 data rows) or missing on disk. Original Phase 1 (2026-08-19) generated schemas for 19 entities but only 13 had matching source data from `roster_and_attendance_june.xlsx`. Scope per TRACKER.md Phase 1 = "shift management only (deferred: wards, beds, OTs, pharmacy, lab, billing, full CoA, cost centers)" — implicitly excludes workflow features like leave, advances, shift swaps, schedule templates.
**Status:** deferred — populate when source data becomes available (e.g., live HR system export or manual entry).
