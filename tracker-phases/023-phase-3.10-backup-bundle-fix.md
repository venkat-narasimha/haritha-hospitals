## Phase 3.10: Backup Script Bundle Fix (✅ DONE 2026-08-27 19:25 IST)

**Status:** ✅ Complete. `pberpprod_backup.sh` now bundles 4 loose files into ONE tar.gz per timestamp, integrity check via `tar -tzf` + `gunzip -t`, single-file rsync to offsite.

**Bug found:** Original script's `TARFILE=$(ls $DEST/*.tar.gz)` glob matched nothing → `set -euo pipefail` silently exited at assignment → script ended after `copied 4 backup files` line in log. NO SHA256, NO offsite rsync.

**Severity:** Lesson #79 violation. Offsite backup at venkat@135.125.196.35 was last successful push BEFORE 2026-08-21 rollback — **6 days of silent offsite failure**. If restore had been needed during this window, NO offsite copy existed.

**Fix:**
- Bundle 4 loose files into ONE tar.gz (`pberpprod_backup_<TIMESTAMP>.tar.gz`)
- Integrity: `tar -tzf` + `gunzip -t` (loud failure on corruption)
- SHA256 on bundle
- Single-file rsync to offsite (was loose-files glob)
- Remove loose files after bundle (2x storage savings)

**Verified:**
- `.bak` original at `pberpprod_backup.sh.bak-20260827-prebundlefix` (md5 `c2b34c4f…`)
- New script md5 `8ee5d04e…` (matches workspace)
- `bash -n` syntax passes
- Cron entry unchanged: `0 */6 * * * /home/vijay/scripts/pberpprod_backup.sh ...`

**Next validation:** Cron slot 2026-08-28 00:00 IST will be first end-to-end test.

**Lessons added:**
- #113: `set -euo pipefail` + empty glob + `$(ls *.tar.gz)` = silent script exit
- #114: Silent cron failures hide for days — always read the actual log file

**Pending follow-up:** Audit `dev_backup.sh` + `qa_backup.sh` for same `set -e + empty glob` pattern (Lesson #113 is generic).

