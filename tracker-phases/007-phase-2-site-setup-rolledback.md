## Phase 2: Site Setup (🔄 ROLLED BACK 2026-08-21 — work preserved, env destroyed)

> **Rollback 2026-08-21:** All Phase 2 deployment work (pberp.duckdns.org site, 9 containers, apps, custom fields, MySQL grants, Company, Holidays) was destroyed when pberp env was torn down at 10:11–10:18 IST. Details below kept as historical record of what was planned and executed. Re-execute from scratch on new env.

**Goal:** Create Haritha Hospitals site on a fresh environment.

**Resolution:**
- ✅ **NEW dedicated env** (clean slate) — compose project `pberp` on main VPS (vijay@144.217.163.228)
- ✅ Skip custom app initially — use custom fields + fixtures for haritha-specific data
- ✅ Apps: frappe 16.x, erpnext 16.x, hrms 16.5.0 (pinned), payments

**Phases executed:**
- A: Pre-flight checks + certificate fix
- B: Compose up — 9 containers (backend, frontend, scheduler, queue-short, queue-long, websocket, redis-cache, redis-queue, db)
- C: Site creation — `pberp.duckdns.org`
- D: Apps install — frappe, erpnext, hrms 16.5.0, payments
- E: Custom fields fixtures
- F: MySQL grants (db user permissions for scheduler IP)
- G: Company "Haritha Hospitals" + Holiday List

**Deliverables:**
- [x] Site location: NEW env `pberp.duckdns.org` (compose project `pberp`)
- [x] Apps installed: frappe, erpnext, hrms 16.5.0, payments
- [x] Custom app: deferred (use custom fields + fixtures)
- [x] Company "Haritha Hospitals" created (INR, India)
- [x] Holidays loaded
- [x] Pre-flight backup (cron added in Phase I)

---

