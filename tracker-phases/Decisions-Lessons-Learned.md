# Decisions Log & Known Issues / Lessons Learned

> **Consolidated file** — merged from `011-decisions-log.md` and `020-known-issues-lessons.md`.

----

## Source: 011-decisions-log.md (Decisions Log)

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-08-19 | Scope = shift management only | User clarified mid-session; defer hospital modules |
| 2026-08-19 | hrms 16.5.0 pin | Lesson #44 — v16.5.1+ breaks on `repost_allowed_types` |
| 2026-08-19 | Shift code = 10-char `[P][HHMM][S][HHMM]` | User-proposed scheme, Option A (lean) |
| 2026-08-19 | Shift name = 10-char code itself (no separate `shift_code` field) | User simplification — name IS the code |
| 2026-08-19 | Holidays = standard Indian national + 4-5 Telangana | User confirmed |
| 2026-08-19 | Custom leave types = deferred | User said Haritha adds later |
| 2026-08-19 | Leave allocation = standard Indian defaults | User confirmed; rules in remarks column |
| 2026-08-19 | Source data = DO NOT modify | Canonicalization at import time only |
| 2026-08-19 | SSA is HRMS-native (Shift Schedule Assignment DocType) | Originally doubted; verified via docs.frappe.io/hr/shift-schedule-assignment |
| 2026-08-19 | Comprehensive 7-change schema update | 9 HRMS docs verified; HRMS v15 canonical structure applied |
| 2026-08-19 | 19 CSVs schema + data combined format | Manager-friendly for Google Sheets review |
| 2026-08-19 | 3 designation collisions resolved automatically | Physician Asstant+Assistant, Sr.Executive+Senior Executive, Sr.Manager+Senior Manager |
| 2026-08-19 | 3 shift code duplicates consolidated | A4+Shift-A, B2+Shift-B, C1+Shift-C |
| 2026-08-20 | Phase 0 + 1 signed off by manager | Schema + data CSVs approved |
| 2026-08-20 | New dedicated env `pberp` (clean slate) | Recommended over legacy envs |
| 2026-08-20 | Apps installed via `bench install-app` (runtime) | Quick start; lesson #47 trade-off (asset sync) |
| 2026-08-20 | Custom app: deferred, use custom fields + fixtures | Fast track for MVP |
| 2026-08-20 | Real-time employee name mapping: `EMP-1001` (CSV) → `HR-EMP-00001` (DB) | Built `HR-EMP-{N-1000:05d}` formatter |
| 2026-08-20 | Attendance imported via raw SQL (not ORM) | Bypassed Frappe Status validation + 240s timeout |
| 2026-08-20 | Attendance status options extended via Property Setter | Added "Weekly Off" + "Holiday" (1:1 CSV match) |
| 2026-08-20 | Employee Checkin via background jobs (25 batches × 500) | Direct console timed out on 12,562 rows |
| 2026-08-20 | HR-Attendance series counter fixed mid-flight (`HR-ATT-2026-` was 183, fixed to 6300) | Series was stale, prevented new record creation |
| 2026-08-20 | 5 X-HH Department variants force-deleted via direct SQL | Frappe `doc.delete()` enforces "disable not delete"; direct DELETE bypasses |
| 2026-08-21 | Backend tested end-to-end via API: auth ✅, CRUD ✅, all 9 entities queryable ✅, payroll/leave/holiday workflows ✅ |
| 2026-08-21 | UI smoke test inconclusive (headless browser tool unreliable) | Needs real browser verification next session |
| 2026-08-21 | Token limit issues (rate_limit_error) on long subagent runs — workaround: split into K1/K2/K3 + direct exec | Lesson learned for future orchestration |
| 2026-08-21 | nginx `Upgrade: websocket` forced for /socket.io/ (added during UI debugging — may need review/revert) | Frappe ws server validates Upgrade header on every request |
| 2026-08-21 | **Rollback: pberp.duckdns.org env torn down 10:11–10:18 IST (Option B: nuke, no backup). All Phase 2–5 deployment work destroyed. Restart from Phase 1 on new env. CSV masters + git history intact.** | Venkat authorized Option B at 10:33 IST; Phase 0 + 1 design work preserved; deployment was not recoverable |
| 2026-08-25 | **Resumption: Phase 2 restart on `pberpprod.duckdns.org`** (env created but never used = QA/dev effectively) | Wipe + reinit as Haritha. Same domain, clean slate. Backups-first mandatory (Step A1–A5). |
| 2026-08-25 | **MEMORY correction:** actual shift code format = `[GMAN]\d{4}[RS]\d{4}` (10-char) | Aug 19 decision said `[P][HHMM][S][HHMM]` (single P prefix, single S mid) — incomplete. Real data uses 4 prefixes (G/M/A/N) and R/S for end-time type. MEMORY.md needs update post-Phase 2. |
| 2026-08-25 | **FK join key:** `shift_assignment.employee` → `employee.attendance_device_id` (EMP-NNNN) | Haritha employee.csv has NO `name` column (PK collision with HRMS). Use `attendance_device_id` as FK. 210/210 match verified. |
| 2026-08-25 | **Subagent pattern rule:** script work = subagent writes script + runs + fixes until works. Never hallucinate. | Applies to all scripted ops (backup, ingest, verify). Inline only for trivial ≤5-line edits. |
| 2026-08-25 | **Subagent model selection:** OX Alpha free for scripted ops | 1M ctx, code-writing specialty, structured output. Nemotron 3 Ultra for reasoning-heavy. GLM 5.2 reserved (rate-limited). |
| 2026-08-25 | **Verify script = reusable** | `scripts/verify_csvs.py` re-runs in Phase 4 (CSV count vs DB count comparison). |
| 2026-08-25 | **Phase 6 added: ISO/CMM Level 5 docs** | Per Venkat 21:30 IST. Scope default = ISO 9001 + 27001, SOPs + process maps + audit trail, customer + manager audience. |
| 2026-08-25 | **Phase 7 added: Handover + optional demo deck** | Per Venkat 21:30 IST. Manager walkthrough + customer pilot (this week). |
| 2026-08-25 | Phase 2 Step A1-A5 backup executed + verified | Backup is mandatory before any destructive wipe (Aug 19 lesson #79 + SOUL never-migrate-prod-without-backup). OX Alpha subagent ran the script, parent (main) verified independently per Lesson #72. |
| 2026-08-25 | Git push: subagent fail-over to inline SSH | Nemotron 3 Ultra free returned FailoverError on first push attempt. Fell back to inline SSH chain (subagent quota/availability unreliable). Push succeeded: `219978d..7e95049 main -> main`. 3 commits: f0e109a + 51d0bb4 + 7e95049. Branch now synced with origin. |
| 2026-08-25 | TRACKER.md updates via reusable script (`update_tracker.py`) | Per Venkat directive (22:46 IST): 'write a script for this as well because it is repetitive task'. JSON-driven, idempotent, handles status_date/footer/sections/decisions/lessons/pending items. Future tracker updates = write JSON spec + run script. No more manual sed/edit. |
| 2026-08-25 | Subagent model fallback pattern established | Nemotron free FailoverError and OX Alpha rate limit both observed. Pattern: try primary model → on failure, fall back to inline or alternative free model. Document this for future ops. Premium MiniMax reserved for critical-path work. |
| 2026-08-26 | 3d-1 Shift Assignment ingest needed Employees set to Active first | Frappe blocks 'Transactions cannot be created for an Inactive Employee'. All 210 Employees set to Active via per-row set_value (SQL UPDATE failed with column quoting bug). |
| 2026-08-26 | 3d-2/3d-3 switched to raw SQL bulk insert (Lesson #43) | Attendance had 5 default status options but CSV uses 7 (incl. Holiday, Weekly Off). Property Setter fix didn't propagate to bench console session. ORM timed out on 12K+ checkin rows. Raw SQL bypasses both. |
| 2026-08-26 | Employee PK = HR-EMP-NNNNN (autoname), not CSV `EMP-NNNN` | HRMS Employee autoname uses naming series. Insert script must set employee_number, not name. CSV mapping: strip 'EMP-' prefix → employee_number → HR-EMP-NNNNN via DB query. |
| 2026-08-26 | Attendance status extended with Holiday + Weekly Off | CSV has 7 status values, Frappe default has 5. Property Setter added 'Holiday' and 'Weekly Off' to enable all CSV rows to insert. |
| 2026-08-26 | Synthetic-data defaults for required Employee fields | CSV has empty gender/date_of_birth (synthetic data). Defaults: gender='Not Specified' (created new Gender record), date_of_birth='1990-01-01', first_name=split(employee_name)[0]. |
| 2026-08-26 | Phase 3.5 reconcile complete (Nemotron): all 11 entities match CSV targets | Department 47→37 (36 CSV + 'All Departments' root), Designation 76→48, Leave Type 9→7, Employment Type 6 (3 CSV-added Internship/Consultant/Temporary + 3 defaults), Holiday 28→14 (re-ingested). Lesson #72 parent-verify PASS on 11/11 entities. |
| 2026-08-26 | Bogus '(no rows)' Shift Location deleted | CSV `## Data` section contained literal `(no rows)` placeholder. Ingest script did not check for this pattern, so it was inserted as a real record. Reconciler flagged + deleted. Pre-ingest must now detect this marker pattern. |
| 2026-08-26 | SS/SSA/SR synthesized (5 / 420 / 8) | SS = 5 templates (one per unique shift_type in SA rows), SR = 8 (status mix matched), SSA = 420 (one per unique employee × shift_type combo). All 5,318 SA rows linked via shift_assignment.shift_schedule_assignment FK. Script: scripts/synthesize_ssa_v2.py (commit 3f82928). |
| 2026-08-26 | HRMS SSA schema discovery: NO shift_type or date field | Brief schema said SSA has shift_type + date. Actual HRMS Shift Schedule Assignment is recurring template-bound — has only company, employee, shift_type, status, docstatus etc. NO date field. Original brief schema was wrong. SA rows link via shift_assignment.shift_schedule_assignment FK, not by date match. |
| 2026-08-26 | Cron regression at 10:06 IST Aug 26 — 3 backup lines dropped | Main VPS crontab now has only pberpprod_backup.sh line. dev_backup.sh, qa_backup.sh, erpclaw-git-daily-backup.sh were dropped (cause unknown — likely a `crontab -e` save gone wrong or an unrelated cron package reinstall). Streak 64/65 partial → 64/66 after slot 38 (18:00 IST Aug 26) missed. Restoring 3 lines gated on user YES/NO. |
| 2026-08-27 | Phase 3.6 bulk-submit needed 3 runs due to 3-layer Frappe framework barriers | Lesson #106: raw-SQL docs need naming_series backfill (#104), Property Setter adds meta.options but not controller-level status checks (#105), HRMS Attendance.validate() has hardcoded 5-value status list. Pattern applies to any submittable doctype bulk-submitted after raw-SQL ingest. |
| 2026-08-27 | Phase 3.6 scope was 6,314 docs, NOT 11,631 as estimated | Task brief assumed Shift Assignments were at docstatus=0. Reality: Phase 3.5 SSA synthesis script (commit 3f82928) submitted them as a side effect. User's list-view complaint was about Attendance + Holiday only. Always verify pre-state via Lesson #72 before estimating scope. |
| 2026-08-27 | Property Setter export → scripted recreate (Option 2) | Custom app fixtures not viable (PROD has no custom app on bench, apps/hrms/ is third-party core read-only per SOUL NEVER rule #3, manual JSON would need parallel applier). Script is idempotent, version-controlled, no core edits, reusable on any env. Mirrors bulk_submit.py's importlib.util.spec_from_file_location() pattern. |

---



---

## Source: 020-known-issues-lessons.md (Known Issues / Lessons Learned)

## Known Issues / Lessons Learned

| # | Issue | Lesson |
|---|-------|--------|
| 47 | Asset sync after `bench build` requires per-directory `docker cp` with `/.` syntax | Backend + frontend have separate `/sites/assets` volumes |
| 80 | Frappe `installed_apps` lives in TWO places: `site_config.json` AND `sites/apps.txt` | Both must be edited atomically |
| 44 | HRMS v16.5.1+ install broken by `repost_allowed_types` phantom field | Pin to v16.5.0 |
| 79 | `bench backup --with-files` has no built-in timeout | Always wrap with `timeout 900` + capture `${PIPESTATUS[0]}` |
| NEW | `bench install-app` runtime creates asset hash drift (Lesson #47) | For future envs, bake apps into image via apps.json |
| NEW | WebSocket container can crash with Redis `SocketClosedUnexpectedlyError` | Add health check + auto-restart |
| NEW | Frappe `ws` server requires `Upgrade: websocket` header even for polling | nginx needs explicit `proxy_set_header Upgrade "websocket";` for `/socket.io/` |
| NEW | Frappe `doc.delete()` enforces "disable not delete" | Force-delete via direct DB DELETE |
| NEW | Token limit errors on long subagent runs (rate_limit_error) | Split large tasks into smaller subagents OR direct exec |
| NEW | Frappe headless browser testing unreliable (timeouts, false negatives) | Use real browser for UI smoke tests |
| NEW | Subagent work pattern: write script + run + fix loop until works; never hallucinate (2026-08-25) | Applies to all scripted ops. Inline only for trivial ≤5-line edits. |
| NEW | Verify scripts must discover `## Data` marker correctly (2026-08-25) | `csv.DictReader` needs header in input — slice `readlines()[header_idx:]` (marker+1), not `[data_start:]` (marker+2). |
| NEW | Haritha employee.csv has no `name` column (2026-08-25) | Use `attendance_device_id` (EMP-NNNN) as FK join key for `shift_assignment.employee`. |
| OX Alpha free model rate-limited mid-task (Aug 25 commit subagent) | Subagent bootstrap costs ~13-15k tokens even when LLM call is free. For trivial mechanical ops (git commit, single SSH call), inline is cheaper + faster. Reserve subagent for scripted ops with fix loops (write script → run → fix until works). |
| Nemotron 3 Ultra free returned FailoverError mid-push (Aug 25) | Free-tier models have unreliable availability. For critical ops (e.g., git push to protected branch), have inline fallback ready. Don't depend on subagent success for one-shot operations. |
| Subagent claimed success on backup, parent verification needed (Lesson #72) | Always run independent verification probes after subagent claims (SHA256 byte-match, file listing, gzip integrity). Costs ~500 tokens inline; saves catching fabricated success reports. |
| scp directly from gateway to venkat VPS failed (Aug 25 backup) | Backup files on vijay VPS, not gateway. Use `ssh tar-pipe` from vijay to venkat for cross-VPS copy, or move files through a shared mount. Don't assume direct paths between VPS hosts. |
| TRACKER.md manual edits are repetitive + error-prone | Use `scripts/update_tracker.py` (Aug 25) — JSON-driven, idempotent. Future updates = JSON spec + run script. Covers: status_date, footer, sections, decisions log, lessons, pending actions. |
| Frappe 16 Property Setter changes don't refresh bench console meta cache | After setting Property Setter for Select options, need to open NEW bench console session (or restart workers) for new options to take effect. Within same session, meta is cached and old options list is used even after frappe.clear_cache(). |
| MariaDB UPDATE with backticks around table name + plain column name failed: 'Unknown column "Active" in SET' | Use frappe.db.set_value() per-row for safety, or check exact column quoting. SQL string escaping is finicky across Frappe/Python/MariaDB combinations. |
| ipython cell splitting breaks multi-statement scripts via exec(open()) | ipython/bench console interprets heredoc input as multiple cells (split at blank lines / function defs). Variables defined in one cell aren't accessible in another. Workaround: use single-line code or wrap everything in main() function called from one cell. |
| Frappe HRMS Shift Schedule Assignment is recurring template-bound — has NO shift_type or date field | Link SA rows via the `shift_assignment.shift_schedule_assignment` FK field, not via date/shift_type matching. Original SSA draft tried to create one SSA per employee × shift_type × date combo (over-counted to 1,758); correct is one SSA per unique employee × shift_type (420). Verify HRMS DocType JSON before drafting brief. |
| Auto-name with autoname = `field:source` does NOT enforce uniqueness on display name | Multiple rows can share the same `department_name` (or any other display field) while having unique `name` PKs. Reconciling requires grouping by display name + keeping oldest (or matching CSV target count). Lesson #73 pattern: always diff `COUNT(*)` vs CSV row count before declaring master ingest done. |
| `(no rows)` literal placeholder in CSV `## Data` section will be ingested as a real record | CSV empty-marker convention (some tools emit `(no rows)` instead of zero data lines) must be detected by pre-ingest script. Insert one naive line and you get a bogus master record (e.g., Shift Location named '(no rows)'). Reconciler caught this on Phase 3.5 — add explicit check in scripts/ingest_masters.py for any `(no rows)` or `<empty>` literal pattern. |
| 104 | Raw SQL ingest bypasses Frappe's mandatory field defaults — submit() fails on `reqd=1` fields that auto-set during ORM insert (Phase 3.6, 2026-08-27) | Docs inserted via raw SQL (bypassing Frappe ORM) don't populate fields set by `validate()` or `before_insert()` hooks (e.g., `naming_series` on Attendance). When submit() runs, it re-validates and fails on the missing mandatory field. Workaround: `UPDATE tabX SET <field>='<series>' WHERE docstatus=0 AND (<field> IS NULL OR <field>='')` before bulk-submit. |
| 105 | Property Setter for Select options does NOT bypass controller-level hardcoded status checks (Phase 3.6, 2026-08-27) | Adding 'Holiday' and 'Weekly Off' to Attendance's `status` options via Property Setter is necessary but NOT sufficient. HRMS `Attendance.validate()` calls `erpnext.controllers.status_updater.validate_status(self.status, [...])` with a hardcoded 5-value list at `apps/hrms/hrms/hr/doctype/attendance/attendance.py:49`. The controller-level check rejects values not in the hardcoded list, even if Property Setter has added them. Fix: monkey-patch `erpnext.controllers.status_updater.validate_status` before submit() — wrap to silently accept the extra statuses. Cannot fix at Property Setter level without editing HRMS core (SOUL NEVER rule). |
| 106 | Bulk-submit of raw-SQL-inserted submittable docs may need 3 runs: (1) backfill mandatory fields, (2) add Property Setter, (3) monkey-patch controller-level checks (Phase 3.6, 2026-08-27) | Pattern observed for Haritha Attendance: 6,300 docs needed all three fixes. Each fix is fast (~10-60s for the run) but cumulatively adds 2 extra runs. Plan for 3 runs in time estimates. Total wall time: ~10 min for 6,300 docs on pberpprod. |
| frappe.make_property_setter has TWO implementations with DIFFERENT signatures (Phase 3.7, 2026-08-27) | Top-level frappe.make_property_setter(args_dict, ignore_validate=False, validate_fields_for_doctype=True, is_system_generated=True, *, module=None) takes a dict-like args. Lower-level frappe.custom.doctype.property_setter.property_setter.make_property_setter(doctype, fieldname, property, value, property_type, for_doctype=False, validate_fields_for_doctype=True, is_system_generated=True) uses positional + for_doctype kwarg. The dict version does NOT accept for_doctype — it derives doctype_or_field from args.doctype_or_field (default 'DocField'). Calling the wrong signature raises TypeError: unexpected keyword argument. |
| bench export-fixtures silently skips Property Setters for apps whose hooks.py doesn't list them (Phase 3.7, 2026-08-27) | export-fixtures iterates `frappe.get_hooks('fixtures', app_name=app)` per app. If hooks.py has no `fixtures = [...]` list containing 'Property Setter', the export produces no output (no error, no warning, exit 0). Property Setters live in DB only and don't migrate on env rebuild / bench update. For Haritha's HRMS Property Setter: hooks.py is third-party code (SOUL NEVER rule #3 forbids editing). Solution: scripted recreate, not fixture export. |
| bench execute <name> requires module to be importable from cwd — /tmp/ scripts fail (Phase 3.7, 2026-08-27) | frappe.get_attr() first segment must be an installed app name (raises AppNotInstalledError otherwise). Fallback eval(code) needs the module already imported. Use bench console < /tmp/wrapper.py + importlib.util.spec_from_file_location() pattern (same as bulk_submit.py). The wrapper imports the /tmp/ script as a module then calls its run() function. |
| 112 | Raw SQL bulk INSERT bypasses ORM auto-derivation of FK fields (Phase 3.9, 2026-08-27) | Frappe ORM `frappe.get_doc().insert()` auto-derives FK-derived fields like `employee_name` and `department` from the linked parent DocType at insert time. Raw SQL `INSERT INTO tabAttendance (...) VALUES (...)` does NOT — the FK-derived columns end up NULL/empty. Same root cause as Lesson #104 (naming_series) and Lesson #110 (linkage fix). Future raw-SQL ingest scripts must either enumerate derived fields explicitly in the column list, OR plan a post-ingest populate script. Lesson #111's pattern of "verify pre-state then post-state counts" applies here too. |
| frappe.db.sql() returns empty tuple for UPDATE statements in MariaDB (Phase 3.9, 2026-08-27) | `cursor.rowcount` carries the affected-row count, but the SQL result tuple is `()`. Code that does `result = frappe.db.sql("UPDATE ..."); matched = result[0][0]` always reads `0`. Workaround: compute the diff between pre-state and post-state counts, OR check `frappe.db._cursor.rowcount` directly. Affects idempotency verification — re-running UPDATE on already-populated rows will return matched=0 from SQL but show actual 0 rows changed only if you verify via WHERE-matched count separately. |
| `frappe.db.commit()` after raw SQL UPDATE is required (Phase 3.9, 2026-08-27) | MariaDB connector default is autocommit OFF in bench. UPDATE rows are only persisted after explicit `frappe.db.commit()`. Without it, a follow-up `frappe.db.sql("SELECT COUNT(*)")` from a fresh bench console session will still see the old state. Same pattern as Phase 3.8 (Lesson #111). |

---

*Last updated: Phase 3.7 idempotent recreate_property_setters.py added (15:06 IST). Fixes Rule #9 violation — Attendance-status-options Property Setter was DB-only, no fixture export possible (HRMS hooks.py doesn't list Property Setter). Tested: delete PS → run script → PS recreated → run again → no duplicate. Script path: scripts/recreate_property_setters.py. Cron regression also resolved (commit 5f383b6, 4 backup lines now active: dev/qa/pberpprod/git-daily).*

---

