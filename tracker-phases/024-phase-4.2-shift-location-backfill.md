## Phase 4.2: Shift Location "Hyderabad" + backfill (✅ DONE 2026-08-28 11:08 IST)

**Status:** ✅ Complete. 1 Location created, 5,738 records backfilled.

**Before → After:**
- Shift Location records: 0 → 1 ("Hyderabad")
- SA with shift_location: 0 → 5,318
- SSA with shift_location: 0 → 420

**Location details:** name="Hyderabad", lat=17.3850, lon=78.4867, radius=200m (Hyderabad city center)

**Backup:** `pberpprod_backup_20260828_110813.tar.gz` (3.4M) — local sha256 `5d8f2b7a252f9280c7f0962dbe6709fe42edea98832c0b6448a116bfc991420d` → offsite rsync to `venkat@135.125.196.35` confirmed by backup script ("OK: offsite rsync").

**Script:** `scripts/fix_issue_2_location.py` — idempotent (INSERT skipped if Hyderabad exists; UPDATE only matches empty rows).

**Execution log:**
1. Pre-check: Locations=0, SA+loc=0, SSA+loc=0 ✅
2. INSERT Shift Location "Hyderabad" → created
3. UPDATE `tabShift Assignment` SET shift_location='Hyderabad' WHERE empty → 5,318 rows
4. UPDATE `tabShift Schedule Assignment` SET shift_location='Hyderabad' WHERE empty → 420 rows
5. Verify: Locations=1, SA+loc=5318, SSA+loc=420, SA total=5318, SSA total=420 (100% coverage) ✅
6. `bench restart` exit 0 ✅
7. Post-restart verify: data persists ✅

**Docs cited:** https://docs.frappe.io/hr/shift-location

**User decision:** 2026-08-28 11:06 IST, Venkat — location name "Hyderabad" (no "Main Hospital" prefix), Hyderabad city center coords (lat=17.3850, lon=78.4867), 200m hospital-grounds radius.

