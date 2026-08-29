## 📜 Historical Project Status (2026-08-21) — Rollback

At **10:11–10:18 IST 2026-08-21**, the `pberp.duckdns.org` environment was torn down (Option B: nuke, no backup). All Phase 2–5 deployment work was destroyed. Restart from Phase 1.

| Phase | Before rollback (2026-08-19/20) | After rollback (2026-08-21) |
|---|---|---|
| Phase 0 — Schema Planning | ✅ done | ✅ done (preserved) |
| Phase 1 — Schema Approval | ✅ done | ✅ done (preserved) |
| Phase 2 — Site Setup | ✅ done at pberp.duckdns.org | 🔄 rolled back — needs redo |
| Phase 3 — Data Import (24,511 records) | ✅ done at pberp.duckdns.org | 🔄 rolled back — needs redo |
| Phase 4 — Workflow Testing (backend PASS) | ✅ done at pberp.duckdns.org | 🔄 rolled back — needs redo |
| Phase 5 — Production Readiness | ⚠️ partial (backup cron only) | 🔄 rolled back — needs redo |
| Phase L — Cert monitoring + sign-off | ⏳ pending | ⏳ pending |

**What was lost:** pberp.duckdns.org env, 24,511 records across 9 entities, all live config (Company, Holidays, Custom Fields), backup cron on vijay@144.217.163.228, all nginx/websocket/workers config.

**What is preserved (intact):**
- CSV masters in `masters/` (19 files, 1.77 MB, 24,758 rows) — canonical source
- All Phase 0 + 1 design decisions (schema, canonicalization, holidays)
- Full git history (a468113 and earlier)
- Lessons learned (table at bottom)
- Venkat VPS backups: `pberpprod_backup_20260821_000039.tar.gz` (only one backup ever created — covers 1.6 MB but pre-Phase 4 data)

**Open question:** New env domain — reuse `pberp.duckdns.org` (faster, but was the destroyed env) or pick new domain (cleaner)? See Open Questions section.

**Restart strategy:** Pick new env domain → re-run Phase 2 (site setup) → re-run Phase 3 (CSV import) → re-run Phase 4 (testing) → re-run Phase 5 (production readiness). CSV masters are idempotent so re-import is safe.

---

