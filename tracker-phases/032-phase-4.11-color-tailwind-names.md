## Phase 4.11: Color field — Tailwind names (✅ DONE 2026-08-28 15:53 IST)

**Status:** ✅ Complete. Replaced 4 hex codes with Tailwind named keys.

**Root cause:** Phase 4.1 wrote hex codes (`#4C6EF5` etc.) to `tabShift Type.color`. The Roster SPA (`apps/hrms/roster/src/components/MonthViewTable.vue`) does `colors[shift.color][200]` where `colors` is `tailwindcss/colors`. Hex codes return `undefined` → `[200]` crashes the Vue render.

Pre-Phase 4.7: 0 SAs → no shift cells rendered → never hit bad lookup. Phase 4.7 create_shifts populated 2,511 new SAs → shift cells render → crash.

**Fix mapping (preserves Venkat-approved color intent):**
- `#4C6EF5` (G blue) → `Blue`
- `#51CF66` (M green) → `Green`
- `#FFA94D` (A orange) → `Orange`
- `#7048E8` (N purple) → `Violet`

**Pre-state (4 hex codes, 25 rows):**
- `#4C6EF5`: 12 rows
- `#51CF66`: 7 rows
- `#FFA94D`: 3 rows
- `#7048E8`: 3 rows

**Per-hex update:**
- `#4C6EF5` → `Blue`: remaining_hex=0, matched_name=12
- `#51CF66` → `Green`: remaining_hex=0, matched_name=7
- `#FFA94D` → `Orange`: remaining_hex=0, matched_name=3
- `#7048E8` → `Violet`: remaining_hex=0, matched_name=3

**Post-state:** `{Blue: 12, Green: 7, Orange: 3, Violet: 3}` — 0 hex codes remaining.

**bench restart:** exit 0.

**HTTP smoke test:** `GET /hr/roster` → HTTP 200 (655 bytes), valid Roster SPA shell (`/assets/hrms/roster/assets/index-*.js`).

**Backup:** `pberpprod_backup_20260828_155231.tar.gz` (2.3 MB) — SHA256 `12223921f3d48aaccab3d5910e52052b34729e1e840780ec6f82478e1cba83e4`. Offsite rsync OK to venkat@135.125.196.35.

**Script:** `scripts/fix_color_tailwind_names.py` — idempotent.

**Lessons:**
- Lesson #139 (new): HRMS Roster SPA expects `shift.color` to be a Tailwind named key. Hex codes silently break it. Always verify field domain against the actual data consumer (SPA, query report, etc.) before writing non-standard values.
- Lesson #140 (new): "Worked before" + "Works on other site" = bug is data-specific, NOT framework. Don't blame the framework.
- Lesson #141 (new): Roster crash after Phase 4.7 was actually 2 cascading bugs — draft SAs (Phase 4.10 fix) AND bad color values (this Phase 4.11 fix). Need both.

---

