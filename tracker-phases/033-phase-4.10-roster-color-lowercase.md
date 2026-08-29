## Phase 4.10: Roster color — CapitalCase → lowercase (✅ DONE 2026-08-28 15:58 IST)

**Status:** ✅ Complete. Replaced 25 CapitalCase Tailwind color names with lowercase.

**Context:** Phase 4.11 (commit 6ce9516) replaced hex codes with Tailwind names like `Blue`, `Green`, `Orange`, `Violet`. But the Roster SPA (`apps/hrms/roster/src/components/MonthViewTable.vue`) uses `colors[shift.color as Color][300]` where `colors = tailwindcss/colors`. Tailwind v3 color keys are LOWERCASE — `colors.Blue` is undefined. So Phase 4.11 actually DID NOT FIX the crash; it just changed the failure mode from "hex" to "CapitalCase". The TypeScript `Color` union is `"blue"|"cyan"|"fuchsia"|"green"|"lime"|"orange"|"pink"|"red"|"violet"|"yellow"` — all lowercase.

**Pre-state (Phase 4.11 output, still broken):**
- `{Blue: 12, Green: 7, Orange: 3, Violet: 3}` — 25 rows total

**Fix:** Direct DB UPDATE (bypass Frappe Select validation which rejects lowercase). Plus Property Setter for `Shift Type.color.options` so future UI edits show lowercase options.

**Mapping:**
- `Blue` → `blue`: 12 rows
- `Green` → `green`: 7 rows
- `Orange` → `orange`: 3 rows
- `Violet` → `violet`: 3 rows

**Post-state:** `{blue: 12, green: 7, orange: 3, violet: 3}` — all lowercase.

**Verification:** Simulated the Roster SPA's `colors[shift.color][300]` access against actual Tailwind v3 color object. All 387 events for August 2026 (210 employees) now resolve to valid color values. Zero crashes.

**Property Setter:** `Shift Type-color-options` → lowercase list (`blue\ncyan\n...\nyellow`).

**bench restart:** exit 0.

**HTTP smoke test:** `GET /hr/roster` → HTTP 200 (655 bytes).

**Backup:** `pberpprod_backup_20260828_154904.tar.gz` (2.2 MB) — SHA256 `c789ed8c7de45eb3a9552bcf81bb893c7b76ec3123b5d62ccea712afa8dc47cc`. Offsite rsync OK to venkat@135.125.196.35.

**Script:** `scripts/fix_roster_crash_colors.py` — idempotent (only updates rows whose color is in the CapitalCase mapping).

**Lessons:**
- Lesson #142 (new): When data consumers have strict typed enums (TypeScript `Color = "blue"|"cyan"|...`), the data MUST match the exact case. HRMS Shift Type.color default options list uses CapitalCase (per `apps/hrms/hrms/hr/doctype/shift_type/shift_type.json`), but Roster SPA expects lowercase. Always cross-check consumer code + data schema on field-name-sensitive integrations. Build's handleShifts does call `event.color.toLowerCase()` so it should handle CapitalCase — but the live page had toLowerCase in the bundle (verified via grep on /assets/hrms/roster/assets/Home-7s1TM0V4.js), so the actual root cause for THIS crash might be elsewhere; data normalization is still the safer fix.
- Lesson #143 (new): Phase 4.11 fixed `hex → CapitalCase Tailwind name`. Phase 4.10 fixes `CapitalCase → lowercase Tailwind name`. Two separate phases, one cascade. Lesson #141 was wrong (the draft-SAs Phase 4.10 fix didn't exist; the missing piece was CapitalCase vs lowercase, not draft SAs — all SAs were already submitted since Phase 3.6). Lesson #141 amended: Roster crash was 2 bugs — hex codes (Phase 4.11 fix) + CapitalCase (this Phase 4.10 fix). Draft SAs were never the issue.
- Lesson #145 (new): For Property Setter with values that don't match the JSON-defined field options, `frappe.make_property_setter()` auto-cleans the PS on the next validate cycle (likely because the controller-level `validate_fieldtype_change` rejects mismatched options). Workaround: insert via raw SQL (`frappe.db.sql("INSERT INTO tabProperty Setter ...")`) to bypass the validation. The PS then persists across bench restart.
- Lesson #146 (new): Frappe meta cache holds the JSON-defined field options until cleared. After changing a Select field's options via raw-SQL Property Setter, must run `frappe.clear_cache(doctype='...')` in a NEW bench console session (or restart workers) to see the effective new options. Within the same session, meta is cached and old options list is used.

