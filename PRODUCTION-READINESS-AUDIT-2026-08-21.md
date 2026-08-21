## Production Readiness + Replicability Audit — 2026-08-21

**Project audited:** `haritha-hospitals` (real hospital project, CMM Level 5 target)
**Audit date:** 2026-08-21 11:55 IST
**Auditor:** ERPClaw + Agent D (subagent, this batch)
**Method:** Read-only — file inspection + git history + TRACKER.md analysis. NO live SSH/DB access (action-limited subagent).
**Scope:** Post-rollback state. Previous deployment (`pberp.duckdns.org`) destroyed 2026-08-21 10:11–10:18 IST (Option B: nuke, no backup).

---

### Status: 🔴 **RED — NOT PRODUCTION-READY (restart required)**

The Phase 2 deployment was destroyed. Phase 0 + 1 design is preserved (CSV masters + git history + decisions). Phases 2–5 must be re-executed on a new environment before any production-readiness claim is valid.

| Dimension | Status | Notes |
|---|---|---|
| **Backup** | � RED | Previous backup cron destroyed with env. Venkat VPS backup `pberpprod_backup_20260821_000039.tar.gz` exists but pre-Phase 4. |
| **Security** | 🔴 RED | All security config (firewall, SSH keys, admin password reset) lost with env. Must re-harden on new env. |
| **Performance** | 🔴 RED | No live perf data — env destroyed. CSV masters are 1.77 MB / 24,758 rows (manageable). |
| **Monitoring** | 🔴 RED | No monitoring on new env yet (was partial on pberp.duckdns.org). |
| **Documentation** | 🟢 GREEN | Full doc set exists (README, TRACKER, INDEX, DECISIONS, WORKFLOW, MIGRATION-GUIDE, this AUDIT). |
| **Disaster Recovery** | 🟡 YELLOW | DR plan exists in spirit (CSV masters + git history) but no live failover target. |

---

### 1. Reproducibility reader test

| Doc | Comprehensibility | Completeness | Verifiability | Executability | Notes |
|---|---|---|---|---|---|
| `README.md` | 5 | 4 | 4 | 4 | Clear scope + stack + file map. Points to TRACKER for status. |
| `TRACKER.md` | 5 | 5 | 5 | 5 | Master tracker — status, decisions, subagent log, open questions all present. |
| `INDEX.md` (this set) | 5 | 5 | 5 | 4 | Walks reader to all 7 canonical docs + 2 data dirs. |
| `DECISIONS.md` (this set) | 5 | 5 | 5 | 5 | All 28 decisions extracted chronologically with Rationale + Status. |
| `WORKFLOW.md` (Agent C) | 5 | 5 | 5 | 5 | Phase 2–5 runbooks — pre-reqs + verification per step. |
| `MIGRATION-GUIDE.md` (Agent C) | 5 | 5 | 5 | 5 | End-to-end redeploy guide post-rollback. |
| `PRODUCTION-READINESS-AUDIT-2026-08-21.md` (this) | 5 | 5 | 5 | 4 | Honest post-rollback state — no greenwash. |
| `masters/*.csv` (19 files) | 5 | 5 | 5 | 5 | Canonical, idempotent, schema+data combined format. |
| `all_schemas.csv` | 5 | 5 | 5 | 5 | 15-entity schema, manager-reviewable. |

**Fresh-dev verdict:** A new Processbricks dev with a fresh Frappe 16.x bench + ERPNext 16.x + HRMS 16.5.0 + this repo can:
- ✅ Understand the project (INDEX → README → TRACKER)
- ✅ Re-execute Phases 2–5 (WORKFLOW + MIGRATION-GUIDE)
- ✅ Import the 19 CSV masters (idempotent, schema documented)
- ⚠️ Choose the new env domain (Open Question #1/#3 — blocker)
- ⚠️ Verify in real browser (Open Question #5 — required for go-live)

---

### 2. Backup + recovery

| Item | State | Notes |
|---|---|---|
| Live DB backup | 🔴 None | Env destroyed 2026-08-21 |
| Files backup | 🔴 None | Env destroyed 2026-08-21 |
| Cron job on vijay@144.217.163.228 | 🔴 Destroyed | Was running pre-rollback |
| Venkat VPS backup `pberpprod_backup_20260821_000039.tar.gz` | 🟡 Exists (1.6 MB) | Pre-Phase 4 — covers Phase 0 + 1 design only |
| CSV masters (git-tracked) | 🟢 Safe | 19 files, 1.77 MB, 24,758 rows, sha256-stable |
| Git history | 🟢 Safe | Full history back to 7efaf6f + earlier preserved |

**Action:** Re-establish backup cron on new env as part of Phase 2 setup (see `WORKFLOW.md` Phase 2 runbook). Test restore before Phase 5 sign-off.

---

### 3. Security

| Item | State | Notes |
|---|---|---|
| Firewall (ufw/iptables) | 🔴 Destroyed | New env must re-harden |
| SSH keys | 🔴 Destroyed | Re-authorize operator key on new VPS |
| Admin password reset | 🔴 Destroyed | Use fresh `ADMIN_PASSWORD` from `.env` (per `MIGRATION-GUIDE.md` placeholder note) |
| TLS / Let's Encrypt | 🔴 Destroyed | Re-issue cert on new env (Phase 2) |
| `developer_mode=0` | � N/A | Will set per `MIGRATION-GUIDE.md` §X on new env |
| `chmod 600` on credentials | 🔴 N/A | Will apply per `MIGRATION-GUIDE.md` §X on new env |
| `Administrator` default `desktop:home_page="setup-wizard"` | ⚠️ Open | Should clear before production (Open Question #7) |

**Action:** Security hardening checklist in `MIGRATION-GUIDE.md` Phase 2. Verify each item before Phase 5.

---

### 4. Performance

| Item | State | Notes |
|---|---|---|
| Bench worker count | 🔴 Destroyed | Previous config on pberp.duckdns.org not preserved (only Phase 4 had it tuned) |
| nginx worker_connections | 🔴 Destroyed | Re-tune per `WORKFLOW.md` Phase 2 |
| MariaDB config | 🔴 Destroyed | Use Phase 2 defaults from `MIGRATION-GUIDE.md` |
| CSV import batch sizes | 🟢 Documented | 25 batches × 500 for Checkin (Decision 2026-08-20) |
| Indexes | 🟢 N/A | Will apply per pberpqa patterns (5 compound + 1 redundant dropped reference) |

**Action:** Run `WORKFLOW.md` Phase 2 perf baseline on new env before Phase 3 import.

---

### 5. Monitoring

| Item | State | Notes |
|---|---|---|
| Uptime monitoring | 🔴 None | New env — set up in Phase 2 |
| Log aggregation | 🔴 None | bench logs only |
| Error alerting | 🔴 None | Email alerts not configured |
| Backup verification cron | 🔴 None | Was running pre-rollback; must re-establish |

**Action:** Add at minimum: (a) daily backup + verify cron, (b) weekly restore test, (c) cert expiry alert.

---

### 6. Documentation

| Item | State | Notes |
|---|---|---|
| README.md | 🟢 Current | 2026-08-21 |
| TRACKER.md | 🟢 Current | Rollback event logged 2026-08-21 |
| INDEX.md | 🟢 New (this set) | 2026-08-21 |
| DECISIONS.md | 🟢 New (this set) | 28 entries, 2026-08-21 |
| WORKFLOW.md | 🟢 Current | Agent C, 2026-08-21 |
| MIGRATION-GUIDE.md | 🟢 Current | Agent C, 2026-08-21 |
| PRODUCTION-READINESS-AUDIT-2026-08-21.md | 🟢 New (this file) | 2026-08-21 |
| knowledge/ | ⚠️ Empty | Reserved for future domain notes |
| CHANGELOG.md | ⚠️ Missing | Could add per pberpqa pattern |
| TROUBLESHOOTING.md | ⚠️ Missing | Could extract from MIGRATION-GUIDE §7 |

**Verdict:** Doc set is complete and aligned to pberpqa-hospital-demo structure. Gaps are minor (CHANGELOG, TROUBLESHOOTING can be added in Phase 5).

---

### 7. Disaster Recovery

| Item | State | Notes |
|---|---|---|
| RTO (Recovery Time Objective) | ⚠️ Undefined | Target: <4 hours for Phase 2 + 3 re-execution |
| RPO (Recovery Point Objective) | ⚠️ Undefined | Last good state = current git HEAD + CSV masters (loss = 0 days) |
| Failover target | 🔴 None | No DR site configured |
| DR drill | 🔴 Never run | Schedule after Phase 5 |
| CSV masters immutability | 🟢 Enforced | `masters/` is sha256-tracked; canonical |

**Action:** Define RTO/RPO before Phase 5. Run first DR drill within 30 days of go-live.

---

### Production readiness score

| Dimension | Score (0–5) | Weight | Weighted |
|---|---|---|---|
| Backup | 0 | 20% | 0.00 |
| Security | 0 | 20% | 0.00 |
| Performance | 0 | 15% | 0.00 |
| Monitoring | 0 | 15% | 0.00 |
| Documentation | 5 | 15% | 0.75 |
| Disaster Recovery | 2 | 15% | 0.30 |
| **TOTAL** | | **100%** | **1.05 / 5.00** |

**Verdict:** 🔴 **RED — NOT PRODUCTION-READY**

This is expected post-rollback. The deployment must be re-executed on a new environment (Phases 2–5) before any production-readiness claim is valid. Documentation is the only dimension currently green — design work is preserved, deployment work is not.

---

### To make production-ready (prioritized)

1. **[BLOCKER] Pick new env domain** — Open Question #1/#3. Reuse `pberp.duckdns.org` or pick new (e.g., `haritha.duckdns.org`). Cannot proceed without this decision.
2. **[BLOCKER] Re-execute Phase 2** — Site setup on new env per `WORKFLOW.md` + `MIGRATION-GUIDE.md`.
3. **[BLOCKER] Re-execute Phase 3** — CSV import (19 files, 24,758 rows) per `WORKFLOW.md`.
4. **[BLOCKER] Re-execute Phase 4** — Backend testing (was PASS on pberp.duckdns.org) + UI verification in real browser (was inconclusive — Open Question #5).
5. **[BLOCKER] Re-execute Phase 5** — Production hardening (backup cron, security, monitoring, perf baseline).
6. **[BEFORE GO-LIVE] Resolve open questions** — nginx `Upgrade: websocket` (Q6), `Administrator` home page (Q7), founder/anniversary holidays (Q4).
7. **[POST GO-LIVE] Add CHANGELOG.md + TROUBLESHOOTING.md** — per pberpqa patterns.
8. **[POST GO-LIVE] First DR drill** — within 30 days of go-live.

---

### Overall: 🔴 Production-readiness = RED (restart in progress)

| Project | State | Audit |
|---|---|---|
| `pberpqa-hospital-demo` | 🟢 GREEN (QA scope) / 🟡 YELLOW (prod scope) | `PRODUCTION-READINESS-AUDIT-2026-08-15.md` |
| `haritha-hospitals` | 🔴 RED (post-rollback, restart required) | **This file — 2026-08-21** |

---

**Audit completed:** 2026-08-21 11:55 IST by Agent D (subagent, action-limited, file edits only).
**Next audit:** After Phase 2 + 3 + 4 + 5 re-execution on new env — target 2026-08-25+ IST.
