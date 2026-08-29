## Open Questions

1. **Site location** — ✅ RESOLVED 2026-08-25: `pberpprod.duckdns.org` (Option B wipe + reinit; never used in production)
2. **Custom app `haritha_hospital`** — needed or just custom fields + fixtures? ✅ RESOLVED: deferred, using custom fields + fixtures
3. ~~**New env domain** — reuse `pberp.duckdns.org` or pick new?~~ ✅ RESOLVED: `pberpprod.duckdns.org`
4. Hospital-specific holidays (founder day, anniversary)? ⏳ Pending user input
5. ⚠️ **UI verification in real browser** — needed before go-live
6. ⚠️ **nginx `Upgrade: websocket` force-set** — should we revert? (added during debugging, prior env)
7. ⚠️ **User `Administrator` default `desktop:home_page="setup-wizard"`** — clear before production?
8. 🆕 **ISO/CMM L5 scope** — confirm default (ISO 9001 + 27001, SOPs + process maps + audit trail, customer + manager audience) or specify more (2026-08-25)
9. 🆕 **Demo order** — manager walkthrough first, customer pilot first, or both same session? (2026-08-25)

**Resolved:**
- ~~Telangana 2025 + 2026 holiday list~~ — using standard Indian national 14 holidays (per user)
- ~~Shift code convention~~ — 10-char `[P][HHMM][S][HHMM]`, name IS the code
- ~~Source data canonicalization~~ — 3 designation + 3 shift dupes resolved at import time
- ~~Apps stack~~ — frappe, erpnext, hrms 16.5.0, payments (no custom app for MVP)

---

