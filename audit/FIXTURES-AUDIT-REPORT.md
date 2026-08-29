# Haritha pberpprod Customization Audit Report

**Site:** `pberpprod.duckdns.org` (Haritha Hospitals)
**Stack:** Frappe 16.30 / ERPNext 16.31 / HRMS 16.5
**DB:** `_b80f05e76a0dcaad` (MariaDB)
**Audit date:** 2026-08-28 (Asia/Calcutta)
**Audit mode:** READ-ONLY — no fixes applied

---

## 1. Customization Counts

| Type | Count | Notes |
|------|------:|-------|
| **Custom Field** | **78** | All `module=NULL/''` (user-added via Customize Form) |
| **Property Setter** | **189** | All `module=NULL/''` (user-added) |
| **Workflow** | 0 | — |
| **Client Script** | 0 | — |
| **Server Script** | 0 | — |
| **Print Format** | 48 | 47 standard + 1 user-customized (IRS 1099) |
| **Web Form** | 7 | 7 standard (from frappe/erpnext/hrms) + 0 custom |
| **Notification** | 8 | 6 standard + 2 user (both disabled) |
| **Custom DocType** | 0 | No custom schemas |
| **DocPerm** | 1388 | On 565 DocTypes (all from core apps) |
| **Workspace** | 28 | All public, from core apps |
| **Dashboard Chart (custom)** | 0 | All 82 are standard |
| **Number Card (custom)** | 0 | All 82 are standard |
| **Report (custom)** | 0 | All 220 are `is_standard='Yes'` (from apps) |
| **Letter Head** | 2 | Both Haritha-specific HTML designs |
| **Module Def (custom)** | 0 | No custom module |

**Installed apps:** `['frappe', 'erpnext', 'hrms']` — **no custom app** on the site.

---

## 2. Per-Type Detailed List

### 2a. Custom Fields (78) — all are Haritha-created overlays on 3rd-party DocTypes

**Targets (most-popular DocTypes):**
- Employee: 22 fields (expense_approver, leave_approver, job_applicant, health_insurance_*, default_shift, payroll_cost_center, pan_number, ifsc_code, micr_code, employment_type, grade, bank info, etc.)
- Company: 13 fields (HR & Payroll tab/section, default payroll/expense/employee-advance accounts, HRA components, arrear_component, basic_component)
- Department: 8 fields (Expense Approvers, Leave Approvers, Shift Request Approver, Leave Block List, Payroll Cost Center, section breaks)
- Designation: 3 fields (Appraisal Template, Skills, Required Skills section)
- Employee Tax Exemption Declaration: 8 fields (HRA exemption, monthly_house_rent, monthly_hra_exemption, annual_hra_exemption, salary_structure_hra, rented_in_metro_city, column/section breaks)
- Employee Tax Exemption Proof Submission: 10 fields (rent dates, total_eligible_hra_exemption, etc.)
- Print Settings: 3 fields (compact_item_print, print_taxes_with_zero_amount, print_uom_after_quantity)
- Contact, Address, Customer, Communication, Email Account: 4 fields (company, tax_category, is_billing_contact, is_your_company_address, crm_deal)
- Timesheet, Project, Task: 3 fields (salary_slip link, total_expense_claim)
- Terms and Conditions, Income Tax Slab, UTM Campaign, Quotation, Salary Component: 5 fields (hr toggle, marginal_relief_limit, crm_campaign, crm_deal, component_type)
- DocPerm / DocShare / Custom DocPerm: 3 fields (`impersonate` — Frappe platform field, not Haritha-specific)

**No hospital-specific markers** — search for `patient`, `doctor`, `nurse`, `bed`, `ward`, `opd`, `ipd`, `haritha` returned **zero matches** in fieldnames or labels.

**Owner-app categorization:**
| Category | Count |
|----------|------:|
| 3rd-party core DocTypes (frappe/erpnext/hrms) | **78** (100%) |
| Custom (none) | 0 |

These all touch core ERPNext/HRMS/Frappe DocTypes — **cannot edit the DocType itself** but the Custom Fields **can be exported as fixtures** in a custom app (Frappe's standard mechanism supports this).

### 2b. Property Setters (189) — all on 3rd-party DocTypes

**Grouped by DocType (top):**
- Sales Invoice: 20 (default_print_format, accounting_dimensions_section hidden, additional_discount_section hidden, base_rounded_total hidden/print_hide, loyalty_points_redemption hidden, subscription_section hidden, tax_id hidden/print_hide, etc.)
- Sales Order: 15 (similar pattern — default_print_format='Sales Order with Item Image', hide accounting_dimensions, etc.)
- Delivery Note: 13
- Purchase Invoice: 11
- Purchase Order: 10
- Quotation: 10
- Supplier Quotation: 8
- Purchase Receipt: 9
- POS Invoice: 6
- Sales Invoice Item / Delivery Note Item / POS Invoice Item: 5, 3, 3 respectively
- Item, Employee, Packed Item, Shift Type, Request for Quotation, Salary Slip: small handfuls

**Patterns observed:**
- `accounting_dimensions_section hidden=1` — **most common** (hides accounting dimensions UI)
- `scan_barcode hidden=0` — reveals barcode scan feature
- `barcode hidden=0` — reveals barcode field
- `default_print_format = 'X with Item Image'` — on Sales/Purchase/Quotation/Delivery/POS docs
- `base_rounded_total hidden=0, print_hide=1`
- `rounded_total hidden=0, print_hide=0` (Salary Slip — show on print, hide on form)
- `in_words hidden=0, print_hide=0` (show in print)
- `naming_series hidden=1, reqd=0` (Customer/Supplier — hide series)
- `employee_number hidden=1, reqd=0`; `naming_series hidden=0, reqd=1` (Employee — use employee_number)
- `item_code hidden=0, reqd=1` (Item — reveal item_code)
- `discount_and_margin hidden=1` (Sales Invoice Item etc.)
- `loyalty_points_redemption hidden=1` (POS/Sales)
- `utm_analytics_section hidden=0` (Lead/Opportunity/POS — reveal UTM)
- `Shift Type color default='blue'` + options list — customization of color picker

**Owner-app categorization:**
| Category | Count |
|----------|------:|
| 3rd-party core DocTypes (frappe/erpnext/hrms) | **189** (100%) |
| Custom (none) | 0 |

These can also be exported as fixtures.

### 2c. Workflows — **0** ✅ (nothing to export)

### 2d. Client Scripts — **0** ✅

### 2e. Server Scripts — **0** ✅

### 2f. Print Formats (48)

**Standard (47)** — all from ERPNext/HRMS apps:
- Accounts: 8 (Standard balance sheet, P&L, GL, AR/AP, Trial Balance, Cash Flow)
- HR: 3 (Appointment Letter, Job Offer, Salary Slip variants)
- Selling: 6 (POS variants, Quotation/Sales Order standard + with-item-image)
- Stock: 4 (Delivery Note variants, Pick List)
- Accounts (more): Bank/Cash Payment Voucher, Sales/Purchase Auditing Voucher, Sales Invoice Return, Credit Note, Dunning, Journal Voucher
- Buying: 2 (Purchase Order + variants)
- Payroll: 3 (Salary Slip variants)

**Custom (1):**
- **`IRS 1099 Form`** — DocType=Supplier, Module=Regional, standard=No, custom_format=1, **enabled**. This is a US tax-reporting regional print format. Despite being in the Regional module, it's marked as user-customized (standard='No', custom_format=1). Probably a customized version of the standard IRS 1099 from the Regional app.

**Disabled (4):** Purchase eInvoice, Detailed Tax Invoice, Simplified Tax Invoice, Tax Invoice (all Sales Invoice Regional formats — not in use).

### 2g. Notifications (8)

**Standard (6)** — from core apps:
- `Exit Interview Scheduled` (HR, enabled)
- `Material Request Receipt Notification` (Manufacturing, enabled)
- `Notification for new fiscal year` (Accounts, enabled)
- `Retention Bonus` (Payroll, enabled)
- `Training Scheduled` (HR, enabled)
- `Training Feedback` (HR, enabled)

**Custom (2)** — both **disabled**:
- `Error Log` — Document Type=Error Log, event=New, **enabled=0** (off)
- `Integration Request` — Document Type=Integration Request, event=Save, **enabled=0** (off)

### 2h. Web Forms (7) — all standard from core apps

- `addresses` (Address, Utilities)
- `issues` (Issue, Support)
- `job-application` (Job Applicant, HR)
- `request-to-delete-data` (Personal Data Deletion Request, Website)
- `request-data` (Personal Data Download Request, Website)
- `tasks` (Task, Projects)
- `edit-profile` (User, Core)

### 2i. Custom DocTypes — **0** ✅

No custom schemas. This means Haritha has not built any custom data models (no Hospital-specific Patient, Doctor, OPD, IPD tables).

### 2j. DocPerm (1388 rows on 565 DocTypes)

All from core apps — these are the standard role-permission matrix that ships with ERPNext/HRMS/Frappe. They are part of each DocType's JSON fixtures and will be recreated automatically when the apps are (re)installed.

**Owner-app distribution** (sampled top):
- Contact: 12 perms, 12 roles
- Company: 11 perms, 11 roles
- Customer: 9, Item: 9, Fiscal Year: 9, Serial and Batch Bundle: 9, Terms and Conditions: 9
- Cost Center: 8, Employee Checkin: 8, Expense Claim: 8, Leave Application: 8, etc.

**No custom-DocType DocPerms** (no user-defined DocTypes → no extra perms needed).

### 2k. Workspaces (28) — all from core apps

| Workspace | Module | App |
|-----------|--------|------|
| Welcome Workspace | Core | (none) |
| Financial Reports | Accounts | erpnext |
| Invoicing | Accounts | erpnext |
| Assets | Assets | erpnext |
| Buying | Buying | erpnext |
| CRM | CRM | erpnext |
| Manufacturing | Manufacturing | erpnext |
| Projects | Projects | erpnext |
| Quality | Quality Management | erpnext |
| Selling | Selling | erpnext |
| ERPNext Settings | Setup | erpnext |
| Home | Setup | erpnext |
| Stock | Stock | erpnext |
| Subcontracting | Subcontracting | erpnext |
| Support | Support | erpnext |
| Build | Core | frappe |
| Users | Core | frappe |
| Integrations | Integrations | frappe |
| Website | Website | frappe |
| Expenses | HR | hrms |
| HR Setup | HR | hrms |
| Leaves | HR | hrms |
| Performance | HR | hrms |
| Recruitment | HR | hrms |
| Shift & Attendance | HR | hrms |
| Tenure | HR | hrms |
| Payroll | Payroll | hrms |
| Tax & Benefits | Payroll | hrms |

**All 28 are public** (for_user=''); all come from app fixtures.

### 2l. Custom Dashboard Charts — **0** (all 82 are `is_standard=1`)

### 2m. Custom Number Cards — **0** (all 82 are `is_standard=1`)

### 2n. Custom Reports — **0**

All 220 reports have `is_standard='Yes'` (Frappe uses Select Yes/No here, not 0/1). They map to core modules (Accounts=52, Stock=50, Selling=23, Manufacturing=21, HR=18, etc.). 1 disabled: `Electronic Invoice Register` (Regional).

### 2o. Letter Heads (2) — **both Haritha-specific**

- `Company Letterhead` (default=0, disabled=0) — HTML with rounded corners, company logo + address, invoice title/number on right. Source=HTML, Content=3003 chars (Jinja template pulling `doc.company`, `doc.company_address`, `doc.billing_address`, etc.). Footer=0.
- `Company Letterhead - Grey` (default=1, disabled=0) — Same template but with light-grey `#f8f8f8` background. Content=3369 chars. **This is the active default.**

Both letter heads are Jinja-driven, no static images, so they are easy to export as fixtures.

---

## 3. Categorization Summary

### 3a. **3rd-party core (frappe / erpnext / hrms)** — all will be recreated by re-installing apps

| Type | Count | Recreated by |
|------|------:|--------------|
| DocPerm | 1388 | App fixtures (auto) |
| Property Setters | 189 | Need to export as fixtures OR recreate via env-init script |
| Custom Fields | 78 | Need to export as fixtures OR recreate via env-init script |
| Web Forms | 7 | App fixtures (auto) |
| Workspaces | 28 | App fixtures (auto) |
| Dashboard Charts | 82 | App fixtures (auto) |
| Number Cards | 82 | App fixtures (auto) |
| Reports | 220 | App fixtures (auto) |
| Notifications | 6 | App fixtures (auto) |
| Print Formats | 47 | App fixtures (auto) |

### 3b. **Haritha-specific (truly user-created)** — must be exported/recreated

| Type | Count | Details |
|------|------:|---------|
| **Letter Heads** | **2** | `Company Letterhead`, `Company Letterhead - Grey` (HTML/Jinja templates) |
| **Notifications** | **2** | `Error Log` (disabled), `Integration Request` (disabled) — both off but exist |
| **Print Formats** | **1** | `IRS 1099 Form` (Supplier, Regional module, custom_format=1, enabled) |

Total Haritha-specific customizations to export: **5 records**.

### 3c. **Unknown** — none

All records categorized. No data requiring investigation.

---

## 4. Recommendation

**Best fit: Option B (env-init script) — RECOMMENDED**, with a small twist:

Given the audit shows:
- **Zero** Custom DocTypes, Workflows, Client/Server Scripts
- **Zero** Custom Workspaces, Dashboard Charts, Number Cards, Reports, Web Forms
- **Only 5 truly Haritha-specific records** (2 letter heads + 2 disabled notifications + 1 IRS 1099 print format)
- **78+189 = 267 overlay customizations** on 3rd-party DocTypes (Custom Fields + Property Setters)

A custom `haritha_hospital` app with fixtures would be overkill — there's nothing custom-app-worthy here. The cleaner approach is:

1. **Create `recreate_pberpprod_customizations.py`** (env-init script, similar to the existing `fix_shift_attendance_linkage.py`) that, run after `bench migrate` on a fresh env, creates:
   - 78 Custom Fields via `frappe.custom.doctype.custom_field.custom_field.create_custom_field`
   - 189 Property Setters via `frappe.custom.doctype.property_setter.property_setter.make_property_setter`
   - 1 Print Format via `frappe.client.insert`
   - 2 Notifications via `frappe.client.insert` (or just leave them out — they're disabled)
   - 2 Letter Heads via `frappe.client.insert`
2. Add it to a post-migrate hook (or invoke manually in the deploy playbook)
3. **No custom app needed** — keep apps.txt at `frappe/erpnext/hrms` only

**Alternative (if Venkat wants version-controlled fixtures):** Option C (Hybrid) — create minimal `haritha_hospital` app with a `fixtures/` folder containing JSON for the 5 user-created records (letter heads, IRS 1099 print format, the 2 notifications). The 267 overlay customizations would still go in the env-init script.

**DO NOT use Option A** (full custom app for everything) — there's no Custom DocType / Script / Workflow to justify a custom app.

### Recommended approach summary

| Customization | Where it goes |
|---------------|---------------|
| Letter Heads (2) | env-init script (small JSON insert) |
| Print Format `IRS 1099 Form` | env-init script |
| Notifications `Error Log`, `Integration Request` | env-init script (or skip — both disabled) |
| Custom Fields (78) | env-init script using `create_custom_field()` |
| Property Setters (189) | env-init script using `make_property_setter()` |
| All standard DocPerms, Reports, Workspaces, Charts, Cards, Web Forms | App fixtures (auto on reinstall) — nothing to do |

### Why env-init script beats fixtures here

- **Fixtures would require creating an app** just to host 5 user records + JSON for 267 custom fields/PS. App adds bench overhead.
- **env-init script is simpler**: one Python file that runs idempotently against the site DB after `bench new-site` + `bench install-app erpnext hrms`.
- **Existing precedent**: `fix_shift_attendance_linkage.py` (in sites/) is exactly this pattern.
- **Re-runnable**: scripts can be `if exists skip` so they're idempotent.

---

## 5. Risk Assessment

### What breaks if we skip this export

If we provision a new env (e.g. new staging) by just `bench new-site` + `bench install-app erpnext hrms` + DB restore of master-data (Company, Items, Customers, Employees, etc.) **without** applying the customization script:

| Customization | What breaks |
|---------------|-------------|
| **78 Custom Fields** | **HIGH** — Employee fields (PAN, IFSC, MICR, Health Insurance, Job Applicant, Expense Approver, etc.) and Company HR settings would be missing. HRMS forms would not show approvers, payroll cost centers, HRA exemption tables. Payroll/HR workflows broken. |
| **189 Property Setters** | **HIGH** — Print formats wouldn't default to "*with Item Image*" versions (manual selection required). Accounting Dimensions sections would be visible (clutter). `scan_barcode`/`barcode` fields would be hidden (POS/Warehouse broken). Employee `employee_number` wouldn't auto-show. Item `item_code` would be hidden. |
| **2 Letter Heads** | **MEDIUM** — All printed Sales/Purchase/Quotation/Delivery docs would have no hospital branding. Looks unprofessional. |
| **Print Format `IRS 1099 Form`** | **LOW** — Only matters for US tax reporting (Supplier); not used in India (Haritha is India-based). |
| **2 Notifications (Error Log, Integration Request)** | **LOW** — Both are **disabled** anyway, so no functional impact. |

### What's needed for env replication (full recipe)

1. `bench new-site {newsite}.local`
2. `bench --site {newsite} install-app erpnext hrms` (sets up standard DocPerms, Reports, Workspaces, Charts, Cards, Web Forms automatically)
3. Restore master data via Frappe's data import (or DB snapshot of company-relevant tables only — Items, Customers, Suppliers, Employees, Chart of Accounts, Warehouses, etc.)
4. **Run env-init script**: `bench --site {newsite} execute haritha_customizations.setup_all()`
   - Creates 78 Custom Fields
   - Creates 189 Property Setters
   - Creates 2 Letter Heads (with HTML content from /audit/letter-heads.txt)
   - Creates Print Format `IRS 1099 Form` (if needed)
5. Verify: `bench --site {newsite} console` → `frappe.get_all("Custom Field", {"module": ""})` → expect 78

### Reusability across non-prod environments

The same env-init script works for **staging, QA, dev** — they all start from the same `frappe + erpnext + hrms` baseline. The script is idempotent (uses `create_custom_field` which checks existence, and `make_property_setter` which is also idempotent on the unique key `(doc_type, field_name, property)`).

### Risk if Venkat picks Option A (full custom app) instead

- Adds maintenance overhead for a 5-record custom app
- No benefit — Frappe's fixture system would handle the 267 overlay customizations the same way env-init does
- Conflicts with bench deploy if app isn't in all environments' apps.txt
- **Net negative** — not recommended

---

## 6. Audit Artifacts (saved to disk)

- `audit/fixtures-audit-pberpprod.txt` (60 KB) — Full categorized output, all 78 CF + 189 PS + 48 PF + 8 Notif + 7 WebForm + 28 WS + 220 Reports + 1388 DocPerm summary + categorization
- `audit/fixtures-audit-pberpprod-detail.txt` (29 KB) — Full per-Doctype breakdown of Property Setters
- `audit/letter-heads.txt` (6 KB) — Full Jinja HTML content of both Letter Heads (3003 + 3369 chars)
- `audit/fixtures-audit-script.py` (15 KB) — The Python audit script (reusable for re-audit)

---

## 7. Self-Verification

- [x] All customization types queried (15 types covered)
- [x] Per-type details captured (full lists, not just counts)
- [x] Owner-app identified for each record (via Module Def.app_name mapping)
- [x] Categorization clear (3rd-party vs Haritha vs unknown — no unknowns)
- [x] Recommendation justified based on actual audit results
- [x] No modifications made (READ-ONLY)
- [x] All raw data saved for Venkat's review

---

## Appendix A — Notable Observations

1. **`is_standard` semantics differ across DocTypes**: Report uses Select `'Yes'/'No'`, others use Check `0/1`. The audit script initially filtered `is_standard=0` for Reports and got 0 results — corrected to check actual values.
2. **`module=NULL/''` for Custom Fields/PS**: All 78 Custom Fields and 189 Property Setters have empty module — this is normal for records created via Customize Form, but makes categorization via module alone impossible. We used DocType-level ownership instead (the underlying DocType determines which app "owns" the customization target).
3. **The `impersonate` Custom Field** appears on DocPerm/DocShare/Custom DocPerm — this is a Frappe platform feature for user impersonation (added by Frappe 13+). Not Haritha-specific.
4. **`IRS 1099 Form`** is in the Regional ERPNext module but marked `standard='No'` and `custom_format=1` — indicates Haritha customized the default. Worth checking the diff against the upstream Regional print format to see what was changed.
5. **`Electronic Invoice Register` report** is the only disabled report — Regional, India e-invoicing context.
6. **Two Letter Heads with no images**: Both use Jinja templates that pull `Company.company_logo` dynamically — easy to export as fixtures, no binary file dependency.
7. **No custom DocTypes = no schema migration risk**: Re-provisioning is straightforward — no need to manage DB schema changes for custom tables.
