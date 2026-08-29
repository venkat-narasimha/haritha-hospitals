## Phase 4.12: Re-apply Phase 4.2 Location (✅ DONE 2026-08-28 15:54 IST)

**Status:** ✅ Complete. Hyderabad Shift Location re-verified after Phase 4.8 restore cascade.

**Discovery:** At script-run time, pre-state check showed **Location already exists with canonical coords** (the task description assumed `Locations=0`, but the Location doc was actually preserved through Phase 4.8 restore — only orphan-references-vs-missing-doc concern was theoretical, not realized). Script ran in idempotent "already exists, no changes" path; no INSERT issued, no UPDATE issued.

**Before → After (no mutation needed, state was already correct):**
- Shift Location count: 1 → 1 (Hyderabad, unchanged)
- SA with shift_location='Hyderabad': 7,829 → 7,829 (unchanged — references already resolve)
- SSA with shift_location='Hyderabad': 420 → 420 (unchanged)
- Location detail: name=Hyderabad, location_name=Hyderabad, latitude=17.385, longitude=78.4867, checkin_radius=200 (matches Phase 4.2 canonical values)

**Backup:** `pberpprod_backup_20260828_155333.tar.gz` (2.2 MB) — SHA256 `f5c04497bc128faaedfb6a7e1f1edf2520cea25c2ff9b12f72d07a116ba0f0b5`. Offsite rsync OK to venkat@135.125.196.35.

**Script:** `scripts/reapply_phase_4_2_location.py` — idempotent:
- If Location exists with canonical coords (lat=17.385, lon=78.4867, radius=200): no-op.
- If Location exists with non-canonical coords: UPDATE to canonical.
- If Location missing: INSERT with canonical.
- Always commits and reports SA/SSA counts for verification.

**bench restart (Step 6):** exit 0.

**Lesson applied:** #79 (pre-mutation backup with SHA256 + offsite rsync), #72 (pre/post-state verify with same query set), #124 (always run pre-state verify before script — even when task description claims X=0, current DB may differ; design scripts idempotent to handle either case).

**Note:** Phase 4.9 (Property Setter + Holiday/Attendance re-apply) and Phase 4.11 (color fix) also landed; this confirms the cascade re-apply is complete and the prod DB is at the canonical Phase 4.2/4.7/4.11 state.

