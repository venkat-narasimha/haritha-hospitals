## Phase 4: Shift Management Workflow Testing (🔄 ROLLED BACK 2026-08-21 — work preserved, env destroyed)

> **Rollback 2026-08-21:** All backend API testing (K-1, K-2, K-3 — PASS), nginx config, worker fixes, and websocket routing were destroyed with pberp.duckdns.org. Backend tests were PASS (verified via API) — scripts can be re-run on new env. UI smoke test was already inconclusive (headless browser unreliable).

**Goal:** Test end-to-end shift management.

**Phases executed:**
- J-1: nginx HTTPS + security headers + routing config (TLSv1.2/1.3, HSTS, CSP, rate limiting)
- J-2: Worker fix (hrms/payments/frappe/erpnext imports in queue workers)
- K-1: Smoke + functional tests (auth, CRUD, entity counts) — **PASS**
- K-2: Functional CRUD + payroll integration — **PASS**
- K-3: HRMS integration (shift/leave/holiday/process_attendance) — **PASS**

**Backend tests PASS** for:
- Shift Assignment workflow ✅
- Auto Attendance (cron ready, needs activation) ✅
- Manual Attendance ✅
- Leave Application + Allocation ✅
- Employee Checkin ✅
- Holiday List ✅

**UI Smoke Test (08:00–09:40 IST 2026-08-21):**
- Site loads at https://pberp.duckdns.org ✅ (HTTP 200)
- Login form loads, API auth works ✅
- All asset bundles serve HTTP 200 (frappe/erpnext/hrms/payments dist/css/js) ✅
- Socket.io proxy added (nginx → pberp-websocket-1:9000) ✅
- System Settings `setup_complete=1` set ✅
- WebSocket container crashed with Redis `SocketClosedUnexpectedlyError` — restarted ✅
- Frappe desk bootstrap IS running (confirmed via browser console stack trace: `desk.js:34 startup`, `sidebar.js:30 prepare`, `notifications.js:476 make`)
- Vue.js SPA mounted but stays on loading splash — **inconclusive** due to headless browser tool unreliability (timeouts, false-negative evaluations)
- **No reliable UI smoke test result** — needs manual browser verification

**Issues encountered (resolved):**
- nginx upstream port: `:80` → `:8080` (frontend listens on 8080)
- Installed Application `is_setup_complete=1` (4 apps)
- System Settings `setup_complete=1`
- Custom app migration path not used (apps installed at runtime, not via apps.json)
- Asset hash sync required (Lesson #47): frontend assets rebuilt + synced via host-staged `docker cp`
- WebSocket container restart loop (Redis connection transient error)

**Issues outstanding (UI):**
- Desk JS mount hangs in headless browser — needs real browser test
- nginx `Upgrade: websocket` header force-set (added during debugging — may need revert if not needed)
- User `Administrator` default `desktop:home_page=setup-wizard` — may need clearing for production

**Deliverables:**
- [x] Shift Assignment creation (via API) ✅
- [x] Manual Attendance ✅
- [x] Leave Application + Allocation ✅
- [x] Employee Checkin ✅
- [x] Reports (API tested, UI untested)
- [ ] ⚠️ Auto Attendance cron activation — pending
- [ ] ⚠️ UI smoke test in real browser — pending

---

