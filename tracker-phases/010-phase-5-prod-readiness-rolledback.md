## Phase 5: Production Readiness (🔄 ROLLED BACK 2026-08-21 — work partially preserved)

> **Rollback 2026-08-21:** Backup cron on vijay@144.217.163.228 (`/home/vijay/scripts/pberp_backup.sh`) is destroyed along with the env. The cron schedule (`0 */6 * * *`) and offsite push to venkat@135.125.196.35 will need to be recreated on new env. One backup file (`pberpprod_backup_20260821_000039.tar.gz`, 1.6 MB) exists on venkat VPS — covers pre-Phase 4 state.

**Goal:** Audit and harden for production.

**Phases executed:**
- I: Backup cron + first run + offsite to venkat VPS ✅
  - Script: `/home/vijay/scripts/pberp_backup.sh` (139 lines, hardened per Lesson #79)
  - Cron: `0 */6 * * *` (00:00, 06:00, 12:00, 18:00 IST)
  - Local retention: 7 days at `/home/vijay/backups/pberp/`
  - Offsite: forever at `venkat@135.125.196.35:/home/venkat/pberp_backups/`
  - First run: `pberpprod_backup_20260821_000039.tar.gz` (1.6 MB) ✅

**Deliverables:**
- [x] Backups (cron 4×/day, 7d local + forever offsite) ✅
- [ ] ⚠️ Pre-flight + post-flight process documentation — pending
- [ ] ⚠️ Disaster recovery tested — pending
- [ ] ⚠️ UI smoke test (real browser) — pending
- [ ] ⚠️ User training — pending
- [ ] ⚠️ Go-live — pending

**Remaining phase:**
- L: Cert monitoring + final sign-off report — **PENDING (next session)**

---

