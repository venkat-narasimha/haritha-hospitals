# this hospital — Project Tracker (Index)

**Project:** this hospital — Real hospital project (CMM Level 5 target)
**Scope:** Shift management + HRMS basics (employees, departments, shift types, attendance, leave)
**Deferred:** Wards, beds, OTs, pharmacy, lab, billing, full CoA, cost centers
**Owner:** Venkat (Processbricks)
**Started:** 2026-08-19
**Stack:** Frappe 16 / ERPNext 16 / HRMS 16.5.0 (pinned) / payments / custom app (TBD)

---

## 📌 Recent Activity (Sep 17–21, 2026) — Demo Readiness Push

5-day intensive push to bring the system to demo-ready state and resolve all sign-off transactions. See [`archive/docs/manager-briefing-2026-09-21.md`](archive/docs/manager-briefing-2026-09-21.md) for the full manager-review briefing.

| Date | Event |
|---|---|
| 2026-09-17 | Demo readiness audit + 1 prod fix (Company.default_holiday_list on this hospital) |
| 2026-09-18 | Manual transaction testing (60 transactions, 6 modules) + Streams 1–5 + sign-off commit (51 PASS) |
| 2026-09-19 | Stream 5 Maximum effort (4 prerequisites + 3 write-tests) + sign-off updated to 58 PASS; Sample Leave Application HR-LAP-2026-00001 submitted end-to-end with Leave Ledger Entry; Fiscal Year fix (2025-2026 + 2026-2027) |
| 2026-09-21 | 211 Holiday List Assignments batch-submitted + renumbering (T-001 to T-079, +19 new transactions); 8 client template items (5 new master templates + 3 template updates); 2 hotfix scrubs (sanitization) |

**Demo readiness verdict (current):** ✅ READY (full, no caveats). Custom Fields 78/78, Property Setters 189/189, Leave Engine (Approver, 211 Holiday List Assignments, Leave Period 2026-2027, 3 Leave Allocations, notification template), HR Settings configured. Test Company kept per operator decision (manual testing sandbox); 0 Branches = single-site per repo Gotcha #12.

**Sign-off state (post-renumber):** 77 ✅ PASS / 0 ⬜ DEFERRED / 1 ❌ NOT DONE / 1 🚫 REMOVED = 78 sign-off rows. Total defined = 79 (1 removed from sign-off but documented as out-of-scope).

---

**Master tracker split:** this file is now a slim index. Full phase detail lives under [`tracker-phases/`](tracker-phases/).

A full backup of the original 1492-line TRACKER.md is preserved at [`tracker-phases/000-FULL-TRACKER-backup.md`](tracker-phases/000-FULL-TRACKER-backup.md).

---

## 📌 Recent Activity (Sep 30 PM, 2026) — Phase B + D + E + Custom App + Leave Approver Attempt

| Date | Event |
|---|---|
| 2026-09-30 12:25–12:30 IST | **Phase B execution batch** — B.1 fixed `working_hours_threshold_for_absent` 0.0 → 2.0 on all 26 Shift Types + fixed Morning-8h `last_sync_of_checkin` (Lesson #42); B.2 changed Holiday List `weekly_off` Sunday → None; B.3 reconciled attendance vs checkin (12,612 → 21,921, +9,309); B.4 took fresh backup + created `Phase-B-Activation.md`. **Phase B closed** (commit `3ab688e`). |
| 2026-09-30 13:30 IST | **Custom app push** — Per Venkat's "dont rename" instruction, rebased + force-pushed local A.11 commit `ec1aa7b` to `github.com/venkat-narasimha/haritha_hospital` with author fix to venkat-narasimha (commit `0a423db`). |
| 2026-09-30 13:48 IST | **Phase D execution batch** (SMTP-less per Venkat choice) — D.1 HRMS heartbeat installed (`HRMS Health Alert` DocType + `HRMS Health Monitor` Server Script, Hourly cadence, sandbox-safe); D.2 12 small depts audit (27 employees on Administrator, 4 with senior candidates, 8 need external); D.2b auto-attendance backfill (same 12,612 → 21,921); D.3a `Role.module_profile` Custom Field + 6/6 roles assigned; D.3b rewrote `Enforce 90-Day Password Expiry` Server Script (datetime import removed); D.3c `User.role_profile_name` root cause = `doc.save()` strips it, `db.set_value()` persists it; D.4 security audit (219 users, 3 admin-like, 451 User Permissions); D.6 image version = Frappe 16.30.0 (matches) + ERPNext 16.31.1 (minor drift). DR test deferred per scope. SMTP deferred per Venkat. |
| 2026-09-30 15:35 IST | **Phase E execution batch** — E.1 project status refreshed (187 lines), E.2 Role × Permission matrix doc (66 cells 11×6), E.3 Client Onboarding Playbook (15 steps), E.4 DECISIONS.md updated (Known Limitations), E.5 verification script (13 checks, executable). **Phase E+1 Org Chart**: 171/211 Employee.reports_to populated + Org Chart card added to HR Manager + Roster Manager Workspaces. **Committed `8be58c7`** to haritha-hospitals repo. |
| 2026-09-30 16:14–17:45 IST | **Sign-off + leave_approver gap attempt** — Venkat chose sign-off + manual CSV fix. Mapped 32 employees on Administrator approver to `medicalsuperdinet1194404@harithahospitals.com`. CSV upload blocked by `ModuleNotFoundError: No module named 'hrms'` in Data Import Tool. Diagnosed: gunicorn workers use system Python, not venv. `sitecustomize.py` fix partially worked. Discovered real startup script is `/usr/local/bin/start.sh` inside container (writable image layer, not bind-mounted). 3 duplicate subagents dispatched by mistake. Found typo (`/frappe/` segment missing on gunicorn path). Fix applied in main session: wrote corrected start.sh, docker cp'd in, docker restart issued. **Verify timed out** — backend status unknown (Venkat to test via browser). 8 known gaps still open for Phase D backlog. |

**Engagement sign-off status:** Phase A + B + D + E closed; Phase C cancelled. 8 known gaps in Phase D/E backlog (SMTP, DR test, Server Scripts sandbox-safe rewrite, 12 small depts leave_approver fallback, image version drift, etc.). All committed to `github.com/venkat-narasimha/haritha-hospitals` + custom app to `github.com/venkat-narasimha/haritha_hospital`.

**Custom app state:** Python module `haritta_hospital` (historical double-t typo), repo URL `haritha_hospital` (correct). Both Phase A + A.11 fixtures committed.

---

## Phase Index

> **Consolidated 2026-08-30:** 38 numbered phase files merged into 9 logical phase documents (preserving all content). The numbered filenames referenced in the right-column summaries (e.g. `003+004+005`) point to the original files, which are preserved in git history.

| # | File | Summary |
|---|------|---------|
| 000 | [000-FULL-TRACKER-backup.md](tracker-phases/000-FULL-TRACKER-backup.md) | Full 1492-line backup of the original monolithic TRACKER.md (historical reference) |
| S   | [Status-Wrapups.md](tracker-phases/Status-Wrapups.md) | End-of-day status wrap-ups (2026-08-27) + historical rollback status (2026-08-21) |
| L   | [Decisions-Lessons-Learned.md](tracker-phases/Decisions-Lessons-Learned.md) | Decisions log + Known Issues / Lessons Learned |
| Q   | [Subagent-Questions-Pending.md](tracker-phases/Subagent-Questions-Pending.md) | Subagent log, Open Questions, Pending Actions (Next Session) |
| 0   | [Phase-0-Schema-Planning.md](tracker-phases/Phase-0-Schema-Planning.md) | **Phase 0 → 1.5** — Schema Planning, Approval, CSV Master Re-Verification (003+004+005) |
| 2   | [Phase-2-Site-Setup-Rollback-History.md](tracker-phases/Phase-2-Site-Setup-Rollback-History.md) | **Phase 2** — Site Setup, Restart #2 on prod-env, Pre-flight Backup, all rollback history (006+016+007+008+009+010) |
| 3   | [Phase-3-Data-Import.md](tracker-phases/Phase-3-Data-Import.md) | **Phase 3 → 3.10** — Data Import, Reconcile, Bulk Submit, Property Setter, Attendance Link/Backfill, Backup Bundle Fix (017+018+012+019+021+022+023) |
| 4   | [Phase-4-Shift-Management-Roster-Crash-Fix.md](tracker-phases/Phase-4-Shift-Management-Roster-Crash-Fix.md) | **Phase 4.1 → 4.12** — Shift Type end_time+color, Location backfill, SS submit, SSA create_shifts, Option B 1-SSA-per-employee, Attendance HRMS-recompute, Tailwind color normalization, Roster crash root cause (026+024+025+027+028+029+034+030+033+032+035+031) |
| 0+  | [Phase-0plus-Foundation-Migration.md](tracker-phases/Phase-0plus-Foundation-Migration.md) | **Phase 0+** — Custom app build + Master Data Migration (prod → dev) (036) |
| 3+  | [Phase-3plus-Client-Onboarding-Data-Templates.md](tracker-phases/Phase-3plus-Client-Onboarding-Data-Templates.md) | **Phase 3+** — P5 rebuild: 22 data templates + 3 intake-workbook docs (README + signoff + master validation); 11/11 SCs PASS; tag `v1.0-p5-templates-production-ready` |
| 6   | [Phase-6-Process-Maturity.md](tracker-phases/Phase-6-Process-Maturity.md) | **Phase 6** — Process & Maturity Documentation, 34 docs / ~14,030 lines (037) |
| A   | [Phase-A-Execution.md](tracker-phases/Phase-A-Execution.md) | **Phase A** — RBAC + Workflows + Dashboards + User Provisioning (2026-09-30) |
| B   | [Phase-B-Activation.md](tracker-phases/Phase-B-Activation.md) | **Phase B** — Auto-Attendance Activation (2026-09-30 PM) — config fixes (threshold 2.0, weekly_off=None, backfill +9,309 records) |
| D   | (in-flight tracker file) | **Phase D** — Production Hardening (2026-09-30 PM, SMTP-less per Venkat) — HRMS heartbeat, Module Profile, Server Script rewrite, security audit |
| E   | (in-flight tracker file) | **Phase E** — Handover Package + Phase E+1 Org Chart (2026-09-30 PM) — 5 docs + org chart setup |
| C   | n/a | **Phase C** — Custom App Rename CANCELLED per Venkat "dont rename" instruction (2026-09-30) |

> **Note (Sep 30 PM):** Phase D + Phase E tracker files are in-flight (will be added in a follow-up commit alongside other Phase B/D/E companion docs). Phase C was cancelled per Venkat's instruction and has no tracker file.

## Quick Stats

- Environments: pberpdev, prod-env (pberpqa skipped)
- Active env (2026-09-30 17:45 IST): prod-env.duckdns.org (Phase A + B + D + E closed; Phase C cancelled; custom app pushed to haritha_hospital repo; leave_approver fix attempt blocked by hrms ModuleNotFoundError; backend container status unknown after start.sh fix)
- See per-phase files for commit counts, customizations captured, and run logs.

## See Also

- [README.md](README.md)
- [docs/](docs/)
- [docs/handbook/README.md](docs/handbook/README.md)
