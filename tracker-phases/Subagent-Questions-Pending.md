# Subagent Log, Open Questions & Pending Actions

> **Consolidated file** — merged from `013-subagent-log.md`, `014-open-questions.md`, `015-pending-actions.md`.

----

## Source: 013-subagent-log.md (Subagent Log)

## Subagent Log

| Date | Task | Agent | Status |
|---|---|---|---|
| 2026-08-27 14:30 | Phase 3.6: bulk-submit 6,314 draft docs to fix Phase 3 ingest miss | bulk-submit-11-631 (inline) | ✅ done |
| 2026-08-19 12:30 | pberpqa reference + scout analysis | pberpqa_ref_an | ✅ done |
| 2026-08-19 12:30 | Source data Excel analysis | source_data_an | ✅ done |
| 2026-08-19 12:30 | Tracker + docs scan | tracker_docs_an | ✅ done |
| 2026-08-19 14:00 | Week-off pattern analysis | pberpqa_week_off_an | ✅ done |
| 2026-08-19 16:06 | Read 9 HRMS shift management docs | read_shift_mgmt_doc, read_shift_type_doc, read_shift_location_doc, read_shift_request_doc, read_shift_assignment_doc, read_shift_schedule_doc, read_shift_assignment_tool_doc, read_ssa_doc, read_roster_doc | ✅ done |
| 2026-08-19 15:33 | Update schema CSV (add SS, SSA, SR + remove shift_code) | update_schema_csv | ✅ done (commit 8307c0b) |
| 2026-08-19 15:42 | Comprehensive 7-change schema update | comprehensive_csv_update | ✅ done (commit aac7b3e) |
| 2026-08-19 19:35 | Generate 19 schema+data CSVs | generate_19_csvs | ✅ done |
| 2026-08-19 22:47 | Push 19 CSVs to GitHub | commit_push_masters | ✅ done (commit 21d54f4) |
| 2026-08-20 14:00 | Phase G (Company + Holidays) | phase_g_setup | ✅ done |
| 2026-08-20 14:30 | Phase H1 (6 small entities) | phase_h1_small_entities | ✅ done |
| 2026-08-20 15:00 | Phase H1.5 (delete 18 defaults) | phase_h15_delete_defaults | ✅ done |
| 2026-08-20 15:30 | Phase H2 (210 Employees) | phase_h2_employees | ✅ done |
| 2026-08-20 16:00 | Phase H3 (5,317 Shift Assignments) | phase_h3_shift_assignment | ✅ done |
| 2026-08-20 16:30 | Phase H4 (6,300 Attendance) | phase_h4_attendance | ✅ done (raw SQL bulk insert) |
| 2026-08-20 17:00 | Phase H5 (12,562 Employee Checkin) | phase_h5_employee_checkin | ✅ done (background jobs) |
| 2026-08-20 17:30 | Phase DB cleanup (force-delete 6 X-HH Departments) | force_delete_hr_dept | ✅ done |
| 2026-08-20 18:00 | Phase I (Backup script + cron + first run) | phase_i_backup | ✅ done |
| 2026-08-20 18:30 | Phase J-1 (nginx HTTPS routing) | phase_j1_nginx_routing | ✅ done |
| 2026-08-20 19:00 | Phase J-2 (worker fix — hrms/payments imports) | phase_j2_worker_fix (failed 2× token limit, direct exec succeeded) | ✅ done |
| 2026-08-21 06:31 | Phase K-1 (smoke tests) | phase_k1_smoke | ✅ done |
| 2026-08-21 06:31 | Phase K-2 (functional CRUD) | phase_k2_functional | ✅ done |
| 2026-08-21 06:31 | Phase K-3 (HRMS integration) | phase_k3_integration | ✅ done |

---



---

## Source: 014-open-questions.md (Open Questions)

## Open Questions

1. **Site location** — ✅ RESOLVED 2026-08-25: `pberpprod.duckdns.org` (Option B wipe + reinit; never used in production)
2. **Custom app `haritha_hospital`** — needed or just custom fields + fixtures? ✅ RESOLVED: deferred, using custom fields + fixtures
3. ~~**New env domain** — reuse `pberp.duckdns.org` or pick new?~~ ✅ RESOLVED: `pberpprod.duckdns.org`
4. Hospital-specific holidays (founder day, anniversary)? ⏳ Pending user input
5. ⚠️ **UI verification in real browser** — needed before go-live
6. ⚠️ **nginx `Upgrade: websocket` force-set** — should we revert? (added during debugging, prior env)
7. ⚠️ **User `Administrator` default `desktop:home_page="setup-wizard"`** — clear before production?
8. 🆕 **ISO/CMM L5 scope** — confirm default (ISO 9001 + 27001, SOPs + process maps + audit trail, customer + manager audience) or specify more (2026-08-25)
9. 🆕 **Demo order** — manager walkthrough first, customer pilot first, or both same session? (2026-08-25)

**Resolved:**
- ~~Telangana 2025 + 2026 holiday list~~ — using standard Indian national 14 holidays (per user)
- ~~Shift code convention~~ — 10-char `[P][HHMM][S][HHMM]`, name IS the code
- ~~Source data canonicalization~~ — 3 designation + 3 shift dupes resolved at import time
- ~~Apps stack~~ — frappe, erpnext, hrms 16.5.0, payments (no custom app for MVP)

---



---

## Source: 015-pending-actions.md (Pending Actions — Next Session)

## Pending Actions (Next Session)

> **📍 Session state (2026-08-27 21:02 IST):** Phases 3.6–3.10 closed today. Phase 4 browser verify + workflow test next. User offline (~215h). Wrap-up commit pending push from VPS.

**🔴 Your turn now (Phase 4 kickoff):**
- [ ] **Browser verify Shift Attendance report** — expect Late Entries >0, Early Exits >0, department column populated, employee_name populated
- [ ] **Phase 4 manual shift mgmt workflow verify** — Roster, Attendance marking, Leave, Holiday skip

**Carry-forward (later phases / housekeeping):**
- [ ] **Phase 6: ISO/CMM L5 docs** — SOPs + process maps + audit trail (per Venkat 2026-08-25)
- [ ] **Phase 7: Handover + optional demo deck** — manager walkthrough + customer pilot
- [ ] **Audit `dev_backup.sh` + `qa_backup.sh` for Lesson #113 pattern** — bundle + `set -e` + empty glob check (silent cron failure)
- [ ] **Backfill lessons #107–#112** — subagents claimed to add but file only has up to #110 (#111, #112 in TRACKER; #107-#109 missing)
- [ ] **Open retention bug** — `find -maxdepth 1 -type d -mtime +7` should be `find -name '*.tar.gz' -mtime +7 -delete` (file-level). Non-blocking, document post-cron-validation.

**Defer (per Venkat 2026-08-27 21:01 IST):**
- 🟡 **LEARNINGS.md git storage location** — currently pushed to orphan branch `lessons-2026-08-27`. Need to decide: merge to main (requires `git filter-repo` on sqlite files) / leave on orphan / move to haritha-hospitals repo. **Defer per Venkat — deal with later.**

**Carry-forward (non-Haritha / wider stack):**
- dev-erp scheduler MySQL 1045 grant fix (A/B/C/D candidates, awaiting YES/NO)
- pberpDEV/QA sign-off on pb_material v1.0.1 install
- git_backup root-perm fix (verified FAIL on 03:00 IST Aug 20 slot)
- ⚠️ **UI verification in real browser** — needed before go-live
- ⚠️ **nginx `Upgrade: websocket` force-set** — review/revert (prior env debugging)
- ⚠️ **User `Administrator` default `desktop:home_page="setup-wizard"`** — clear before production?
- **Activate Auto Attendance cron** — `enable_auto_attendance=1` on Shift Types (Phase 4 follow-up)
- **Disaster recovery test** — restore from backup
- **User training** — for Haritha Hospital staff

**✅ Already-resolved today (2026-08-27):**
- ✅ Cron regression (3 dropped backup lines) — commit `5f383b6`
- ✅ Property Setter Rule #9 gap — commit `ec9f989`
- ✅ All submittable docs docstatus=1 — commit `c13753b` (Phase 3.6)
- ✅ Attendance linkage fix — commit `c7bf823` (Phase 3.8)
- ✅ Department + employee_name — commit `606cd90` (Phase 3.9)
- ✅ Backup script bundle fix — script deployed md5 `8ee5d04e…` (Phase 3.10)

**Next validation event:** Cron slot 2026-08-28 00:00 IST = first end-to-end test of bundled backup script (Phase 3.10).

---

