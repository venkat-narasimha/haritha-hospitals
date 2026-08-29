## Phase 2 (Restart #2 — pberpprod.duckdns.org) (2026-08-25 22:00 IST) 🔄 IN PROGRESS

> Resumption context: Aug 21 10:11–10:18 IST rollback destroyed prior `pberp.duckdns.org` env. After considering options, Venkat chose **Option B (wipe + reinit) on `pberpprod.duckdns.org`** at 21:43 IST 2026-08-25. pberpprod was created but never loaded with real data — treated as QA/dev for wipe purposes.

**Goal:** Spin up Haritha Hospitals on `pberpprod.duckdns.org` with clean state.

**Plan (gated, no auto-progression):**

```
Step A1: bench --site prod backup --with-files (mandatory pre-flight)
Step A2: copy backup to /home/vijay/backups/prod/ (local)
Step A3: copy backup to venkat@135.125.196.35:/home/vijay/backups/prod/ (offsite)
Step A4: verify backup integrity (tar tzf + smoke-restore in dev)
Step A5: SHA256 backup, store checksum
  ↓ user ✅ on backup integrity
Step B1: stop site traffic (maintenance mode or DNS pause)
Step B2: drop database _<dbname>
Step B3: bench new-site pberpprod.duckdns.org
Step B4: install apps: frappe → erpnext → hrms 16.5.0 → payments
Step B5: configure domain + DuckDNS + cert (same URL, but cert may need refresh)
Step B6: 4×/day cron backup (per Lesson #79 hardening)
  ↓ user ✅ on env live
Phase 3: ingest in sub-phases (3a masters → 3b shift_assignments → 3c attendance/checkin/leave)
```

**Runbook reuse:** Aug 20 Phase 2 execution at `pberp.duckdns.org` is preserved in git history — sub-agents should reference commit history for exact commands, container names, MySQL grant patterns.

**Subagent model:** OX Alpha free (1M ctx, code-writing specialty, structured output).

**Lessons to apply (cumulative):**
- #44: pin hrms 16.5.0 (NOT 16.5.1+)
- #46: restart backend + workers after install-app
- #47: asset sync per-directory via host-staged `docker cp`
- #66: verify `sites/apps.txt` after install-app
- #79: wrap `bench backup` with `timeout 900` + `${PIPESTATUS[0]}` capture
- #80: edit `site_config.json` AND `sites/apps.txt` atomically

