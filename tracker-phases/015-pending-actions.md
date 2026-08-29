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

