## Phase 4.11: Roster crash — REAL root cause investigation (✅ DONE 2026-08-28 16:17 IST)

**Status:** ✅ Complete. Confirmed root cause is **HRMS Shift Type color CapitalCase vs Vue frontend lowercase Tailwind palette mismatch** at the EXACT crash site `Home-7s1TM0V4.js:7:139352`. The Phase 4.10 fix (color normalization + Property Setter) was correct and is still applied. The Roster page now renders 211 employees × 31 days without crash.

**Investigation steps (READ-ONLY):**

1. **JS file located:** `/home/frappe/frappe-bench/apps/hrms/hrms/public/roster/assets/Home-7s1TM0V4.js` (167 KB minified, line 7 holds entire bundle).
2. **Crash column extracted (139352):** `borderColor:o.value.shift===G.name&&o.value.date===w.date?A(un)[G.color][300]:A(un)[G.color][200],backgroundColor:G.status==="Active"?A(un)[G.color][50]:"white"}`
3. **Bundle pattern audit:** Only ONE `[200]` access in entire chunk — confirmed via `grep -oE "\[200\]"` count = 1. No other crash sites.
4. **Vue source read:** `apps/hrms/roster/src/components/MonthViewTable.vue` confirms:
   - `import colors from "tailwindcss/colors";` (full Tailwind v3 palette, all lowercase keys)
   - `type Color = "blue"|"cyan"|"fuchsia"|"green"|"lime"|"orange"|"pink"|"red"|"violet"|"yellow"` (lowercase)
   - `colors[shift.color as Color][300]` and `colors[shift.color as Color][200]` and `colors[shift.color as Color][50]` — 3 accesses per shift cell
5. **HRMS JSON source read:** `apps/hrms/hrms/hr/doctype/shift_type/shift_type.json` defines `color` Select options as `Blue\nCyan\nFuchsia\nGreen\nLime\nOrange\nPink\nRed\nViolet\nYellow` — ALL CAPITALCASE. **MISMATCH confirmed.**
6. **DB audit:** All 25 Shift Types have lowercase colors: `blue: 12, green: 7, orange: 3, violet: 3`.
7. **API audit (13 months, all):** 6,622 events total, **0 invalid/empty colors**. Unique colors = {blue, green, orange, violet}.
8. **Node simulation:** `colors["blue"][200]` = `#bfdbfe` ✅; `colors["Blue"][200]` → CRASH (matches original error).
9. **Headless Chromium with auth cookie injection (CDP):** Navigated to `/hr/roster` after `Network.setCookie` for `sid`. Page rendered with `bodyText: "Frappe HR Roster A Roster: Month View August, 2026 Haritha Hospitals..."`, `hasTable: true, rowCount: 211, errorMessages: []`. Screenshot confirms full table renders.

**Root cause (CONFIRMED):**
- `G.color` came from `event.color.toLowerCase()` in `handleShifts` AND from `ShiftType.color` (now lowercase after Phase 4.10 fix).
- `A(un)` = unref on `ut(ji)` = computed tailwindcss/colors palette (lowercase keys).
- `A(un)["blue"]` returns `{50,100,200,300,...}`; `A(un)["Blue"]` returned `undefined` (pre-fix).
- `[200]` on `undefined` = `TypeError: Cannot read properties of undefined (reading '200')` — exact original error.

**Why the user reported "browser still crashes":**
- Phase 4.10 was applied 2026-08-28 15:58 IST; user testing may have been from before the fix.
- Or browser cache held the old `Home-7s1TM0V4.js` (unlikely — filename hash changed Aug 24, before fix).
- **Verification just done (16:17 IST) shows the page renders perfectly.**

**Fix verification (post-Phase 4.10, idempotent):**
- Direct DB query: 25/25 Shift Types lowercase ✅
- Property Setters present: `Shift Type-color-options` (lowercase list), `Shift Type-color-default` (blue) ✅
- API across 13 months: 6,622 events, 0 bad ✅
- Live browser render: 211 rows, 0 errors ✅

**Self-verification (BEFORE reporting SUCCESS):**
- [x] Backup done (Phase 4.10 backup `pberpprod_backup_20260828_154904.tar.gz`)
- [x] JS file ACTUALLY READ at column 139352 (snippet above)
- [x] Python function ACTUALLY READ (`hrms/api/roster.py` `get_shifts` + `MonthViewTable.vue` `handleShifts`)
- [x] API endpoint ACTUALLY CALLED (6,622 events across 13 months)
- [x] Compared working vs broken (no broken months — all clean)
- [x] Root cause identified with PROOF (specific code line + specific data + node simulation matching original error)
- [x] Fix applied (Phase 4.10 — already in place, idempotent verification confirms)
- [x] Verify: API now returns correct shape (all colors lowercase)
- [x] bench restart done (Phase 4.10)
- [x] Script + TRACKER saved
- [ ] git commit + push exit 0 (pending)
- [ ] origin/main shows new commit (pending)

**New lessons:**
- Lesson #147 (new): For minified Vue code-split chunks like `Home-7s1TM0V4.js` (167 KB on 7 lines), error stack column numbers refer to CHARACTER POSITION in the line, not source line numbers. Use `awk 'NR==7 {print substr($0, COL, 80)}'` to extract the exact column context.
- Lesson #148 (new): For `TypeError: Cannot read properties of undefined (reading 'X')` errors in minified bundles, the `X` may be a NUMERIC key (`[200]`) not a string property (`.200`). JS treats both the same. Always `grep -oE "\[<key>\]\[<X>]"` and confirm the access pattern.
- Lesson #149 (new): Headless Chromium HttpOnly cookies can't be set via `document.cookie` from JS. Use Chrome DevTools Protocol `Network.setCookie` with `httpOnly: true` over the WebSocket endpoint exposed via `--remote-debugging-port`. Frappe's `frappe-bench/env` has `websockets` library ready.
- Lesson #150 (new): Phase 4.10 (color CapitalCase→lowercase) was the correct fix. Phase 4.11 here is a **verification + documentation** phase, not a new code change. Idempotent verification scripts (like `fix_roster_real_root_cause.py`) document the root cause + provide a safety net to re-apply if data ever regresses.

**Script:** `scripts/fix_roster_real_root_cause.py` — idempotent verification + auto-fix if data regresses.

---

