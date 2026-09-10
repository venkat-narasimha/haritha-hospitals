# Haritha Phase A — Build `haritha_hospital` + Export Fixtures

**Date:** 2026-08-28 16:50–16:54 IST (≈ 3 min 47 s wall clock)
**Site:** pberpprod.duckdns.org (Frappe 16.30 / ERPNext 16.31 / HRMS 16.5.0)
**Operator:** Vijay / SSH `144.217.163.228` → container `erp-prod-backend-1`

---

## 1. App created — ✅
- **Location:** `/home/frappe/frappe-bench/apps/haritha_hospital/`
- **Initial commit:** `232696c feat: Initialize App` (single commit only)
- **Module path:** `apps/haritha_hospital/haritha_hospital/`
- **Created via:** `bench new-app haritha_hospital` (interactively answered prompts)
- **App metadata populated by `bench new-app`:**
  - `app_title = "Haritha Hospitals"`
  - `app_description = "Haritha Hospitals customizations - fixtures for env replication"`
  - `app_publisher = "Processbricks"`
  - `app_email = "processbricks@example.com"`
  - `app_license = "mit"`
- **Note on `setup.py`:** Frappe v16 uses `pyproject.toml` (PEP 621), not legacy `setup.py`. `install_requires` was added to `pyproject.toml` `dependencies = ["hrms>=16.5.0"]` instead.
- **License prompt quirk:** Bench rejects `MIT` uppercase; valid answer is `mit`.

## 2. App installed on pberpprod — ✅
- **Command:** `bench --site pberpprod.duckdns.org install-app haritha_hospital`
- **Output:** "Installing haritha_hospital... Creating Workspace Sidebars / Creating Desktop Icons / Updating Dashboard for haritha_hospital"
- **Warning (harmless):** `frappe.core.doctype.duckdb_sync.duckdb_sync.cleanup_old_syncs is not a valid method` — pre-existing Frappe core issue, unrelated to haritha.
- **`installed_apps` verification (via `frappe.get_single("Installed Applications").installed_applications`):**
  ```
  APP: frappe
  APP: erpnext
  APP: hrms
  APP: haritha_hospital
  ```

## 3. hooks.py configured — ✅
- Added immediately after `app_license = "mit"`:
  ```python
  # Fixtures to export (Haritha customizations)
  fixtures = ["Custom Field", "Property Setter", "Print Format", "Letter Head", "Notification"]
  ```
- Top metadata block now reads:
  ```
  app_name = "haritha_hospital"
  app_title = "Haritha Hospitals"
  app_publisher = "Processbricks"
  app_description = "Haritha Hospitals customizations - fixtures for env replication"
  app_email = "processbricks@example.com"
  app_license = "mit"

  # Fixtures to export (Haritha customizations)
  fixtures = ["Custom Field", "Property Setter", "Print Format", "Letter Head", "Notification"]
  ```

## 4. __init__.py version check — ✅ implemented + tested
- File now has `__version__ = "0.0.1"` plus `check_hrms_version()` that:
  1. Looks for `/home/frappe/frappe-bench/apps/hrms/hrms/__init__.py`
  2. Parses the `__version__` line
  3. If HRMS version < `16.5.0`, calls `frappe.throw(...)`
- **Tested manually** — found HRMS = `16.5.0`, comparison returns `True` for `>= 16.5.0`, install proceeded.

## 5. Fixtures exported — ✅ but **filtering required** (see §6)
- **Command:** `bench --site pberpprod.duckdns.org export-fixtures --app haritha_hospital`
- **Path:** `/home/frappe/frappe-bench/apps/haritha_hospital/haritha_hospital/fixtures/`
- **Files generated + counts:**

  | File | Count | Expected (per directive) | Notes |
  |---|---:|---:|---|
  | `custom_field.json`     | **78**  | 78 | ✅ exact match |
  | `property_setter.json`  | **189** | ~3 | ❌ includes 186 framework defaults |
  | `print_format.json`     | **48**  | 1  | ❌ includes 45 framework defaults |
  | `letter_head.json`      | **2**   | 2  | ✅ both Haritha |
  | `notification.json`     | **8**   | 2  | ❌ includes 6 framework defaults |

- **Backup:** `fixtures/` archived to `/root/.openclaw/workspace/projects/haritha-hospitals/phase-a/fixtures.tar.gz` for offline review.

## 6. ⚠️ STOP — Property Setter NOT filtered correctly
- **Expected:** ~3 Haritha-specific property setters.
- **Got:** 189 rows. ALL rows have **no `app` column populated** (verified `frappe.db.has_column("Property Setter", "app") == False`).
- **Verified actual Haritha-specific PSs in DB (3 only):**
  1. `Shift Type-color-default` → `default = "blue"` (modified 2026-08-28 10:41:17)
  2. `Shift Type-color-options` → color options including blue/cyan/etc.
  3. `Attendance-status-options` → Present / Absent / On Leave / Half Day / Work From Home / Holiday / Weekly Off
- **The other 186 rows** are stock PSs: `Sales Invoice-commission_section-hidden`, `Lead-utm_analytics_section-hidden`, dozens of `*-scan_barcode-hidden` (2026-08-26 batch), etc. — all installed by Frappe/ERPNext/HRMS app code, not Haritha customizations.

### ⚠️ Same issue affects Print Format and Notification
- **`print_format.json`** — 48 rows. Module breakdown:
  - Accounts 22, Selling 6, Regional 5, Stock 4, None 3, Payroll 3, Buying 3, HR 2
  - The 3 `module=None` records (likely Haritha custom): `Drop Shipping Format`, `Cheque Printing Format`, `Payment Receipt Voucher`
  - **Note:** "Drop Shipping Format" name sounds like ERPNext stock too — needs manual review.
- **`notification.json`** — 8 rows. Module breakdown:
  - HR 3, None 2, Accounts 1, Payroll 1, Manufacturing 1
  - The 2 `module=None` records: `Error Log`, `Integration Request` — **these are stock Frappe notifications, NOT Haritha customizations.**
- **`letter_head.json`** — 2 rows, both custom (Company Letterhead, Company Letterhead - Grey) ✅
- **`custom_field.json`** — 78 rows, all Haritha ✅

### Recommendation (for Venkat review)
The `fixtures = [...]` mechanism in `hooks.py` is too coarse — it dumps ALL records of the doctype globally. For Property Setter and Print Format we need **curation**:
1. **Option A — Custom export script** that uses filters (e.g. `module=None`, or doc_type whitelist) to write only Haritha-specific rows to `property_setter.json` / `print_format.json` / `notification.json`.
2. **Option B — `app_include_specific_doctype_fields` / per-doctype export hooks** in `hooks.py` — bench actually supports a dict form `fixtures = {"Property Setter": [{"dt": "...", "filters": {...}}], ...}` since Frappe 14.

**Not done in this scope** per directive ("Stop after step 5 + remote setup. Do NOT commit or push").

## 7. Git remote — ✅ configured, NO push
- **Remote added:** `origin = git@github.com:venkat-narasimha/haritha_hospital.git`
- **Current state:**
  - 1 commit: `232696c feat: Initialize App`
  - Working tree changes (uncommitted):
    - `M haritha_hospital/__init__.py`
    - `M haritha_hospital/hooks.py`
    - `M pyproject.toml`
    - `?? haritha_hospital/fixtures/` (5 new JSON files)
  - **NO push attempted** — `git ls-remote origin` failed (no SSH client in container) but no fetch/push has been run.
- **Per Venkat directive: STOP. No additional commits. No push.**

## 8. Self-verification checklist
- [x] App directory exists with module files
- [x] `hooks.py` has `fixtures = [...]` line
- [x] `__init__.py` has version check (`check_hrms_version`)
- [x] `installed_apps` includes `haritha_hospital`
- [x] Fixtures directory has 5 JSON files
- [ ] Property Setter JSON has expected 3 rows (**189 instead** — STOP per directive)
- [x] Git remote configured (no push)

## 9. Total wall clock
**≈ 3 min 47 s** (16:50:57 → 16:54:44 IST)

---

## Files saved to workspace
- `/root/.openclaw/workspace/projects/haritha-hospitals/phase-a/REPORT.md` (this file)
- `/root/.openclaw/workspace/projects/haritha-hospitals/phase-a/fixtures.tar.gz` (exported fixtures, 39 KB compressed)
- `/root/.openclaw/workspace/projects/haritha-hospitals/phase-a/logs/step1_newapp.log`
- `/root/.openclaw/workspace/projects/haritha-hospitals/phase-a/logs/step3_install.log`
- `/root/.openclaw/workspace/projects/haritha-hospitals/phase-a/logs/step4_export.log`

## ⏸ STOPPED — Awaiting Venkat review before commit/push and before any fixture curation work.