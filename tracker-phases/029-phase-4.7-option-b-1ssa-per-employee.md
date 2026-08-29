## Phase 4.7: Option B — 1 SSA per employee (✅ DONE 2026-08-28 11:38 IST)

**Status:** ✅ Complete. Cancelled 210 duplicate SSAs (keep oldest per employee), deleted 288 orphan SAs (created in prior Phase 4.6 run), re-ran `create_shifts()` on the 210 remaining SSAs for the 2026-08-28 → 2026-11-26 window. Zero failures.

**Decision (Venkat, 2026-08-28 11:32 IST):** Option B — re-design SSAs to 1 per employee (vs A=enable `allow_multiple_shift_assignments` or C=accept partial). Rationale: HRMS real-world deployments have 1 SSA per employee; multiple SSAs was a Phase 3.5 synthesis artifact.

**Source review (Step 2):** `apps/hrms/hrms/hr/doctype/shift_schedule_assignment/shift_schedule_assignment.py:64` — `def create_shifts(self, start_date: str, end_date: str | None = None)`. Default `end_date = start_date + 90 days`. `create_individual_assignment()` calls `create_shift_assignment()` (in `shift_assignment_tool.py:323`) which always creates a NEW SA — no dedup — so safe to re-run after orphan deletion.

**Pre-state (Step 1, 2026-08-28 11:33 IST):**
- SSA total: 420 (ds=1: 420, ds=2: 0)
- Employees with multi SSA (ds=1): 107
- SA total: 5,606 (5,318 historical + 288 orphans)
- SA covering today: 28
- `HR Settings > allow_multiple_shift_assignments` = 0 (unchanged)

**Backup (Step 0, 2026-08-28 11:33 IST):**
- Bundle: `pberpprod_backup_20260828_113328.tar.gz` (1.9 MiB)
- SHA256: `20712ddb5010cc5d21d003ae93dac0d3f1319f490df7e89bf5e78df182456700` (byte-match offsite rsync to `venkat@135.125.196.35`)
- gzip + tar layers OK, ~1 min before any data mutation.

**Execution (Step 5, 2026-08-28 11:35–11:38 IST, ~3 min wall time):**
- Script: `scripts/fix_issue_b_one_ssa_per_employee.py` (6,554 bytes, copied to `/tmp/fb.py` in `erp-prod-backend-1`)
- **Step 3a:** Deleted 288 orphan SAs (creation >= 2026-08-28), 0 failures.
- **Step 3b:** Cancelled 210 duplicate SSAs (107 employees × ~2 duplicates each, keep oldest per employee), 0 failures.
- **Step 3c:** Reset `create_shifts_after` = `2026-08-27` on all 210 remaining SSAs; called `create_shifts("2026-08-28", "2026-11-26")` on each.
  - 210/210 SSAs processed successfully.
  - 2,511 new SAs created (one SA per consecutive repeat_on_days block per SSA per repeat week).
  - 0 failures.

**Post-state (Step 6, 2026-08-28 11:38 IST):**
| metric | before | after |
|---|---|---|
| SSA total | 420 | 420 |
| SSA docstatus=1 | 420 | 210 |
| SSA docstatus=2 | 0 | 210 |
| Employees with multi SSA (ds=1) | 107 | 0 |
| SA total | 5,606 | 7,829 (+2,223) |
| SA pre 2026-08-28 (historical) | 5,318 | 5,318 (unchanged) |
| SA in 2026-08-28 → 2026-11-26 | 288 | 2,511 |
| SA covering today (2026-08-28) | 28 | 210 |
| SA range | 2025-05-26 → 2026-11-26 | 2025-05-26 → 2026-11-26 |

**SA in Aug-Nov 2026 by shift_schedule (post):**
- Admin Day Shift (Mon-Fri, 210 SSAs → ~13 blocks × 210 emps = ~2,730 — but actually per-emp 13 blocks per 13 weeks ≈ 13 × 210 = 2,730; observed will be lower because some SSAs only had 1 cycle so far)

**Why SA count (2,511) is higher than Phase 4.6 estimate (~2,100):**
After deleting 288 orphans and re-running on 210 SSAs (not 420), the per-SSA SA count averages 2,511 / 210 ≈ 12. The 5 schedules break down by repeat_on_days count: Mon-Fri (5) → ~13 blocks/13 weeks ≈ 13 SAs; Mon-Sat (6) → ~13 SAs; 7 days (7) → ~13 SAs. So ~12-13 SAs per SSA is expected.

**bench restart (Step 7):** exit 0; `bench console` ping returned `alive: [{'alive': 1}]`, SA count = 7,829 preserved.

**Lesson applied:** #79 (pre-mutation backup with SHA256 + offsite rsync), #72 (pre/post-state verify with same query set), #106 (SQL fallback when doc.cancel() raises), #119-#123 (use `bench console < script.py` not `bench console -c "..."` for backtick-heavy SQL).

**Script is NOT idempotent for Step 3c:** re-running will create duplicate SAs in the 2026-08-28 → 2026-11-26 window (because `create_shift_assignment()` in HRMS always inserts without dedup). Step 3a (orphan deletion) and Step 3b (duplicate cancel) ARE idempotent. To re-run safely, first delete SAs in the window: `DELETE FROM \`tabShift Assignment\` WHERE start_date BETWEEN '2026-08-28' AND '2026-11-26'`.

**Commit hash:** see `git log origin/main -1` after push.

