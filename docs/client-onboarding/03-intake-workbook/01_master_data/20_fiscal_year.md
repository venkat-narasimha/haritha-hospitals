# Fiscal Year — Intake Sheet

**DocType:** Fiscal Year (not submittable)
**Module:** HR / Setup
**Required fields:** 3 (parent: `year`, `year_start_date`, `year_end_date`) + 1 (child: `company`)
**Optional fields:** 0 (parent) + 0 (child)

Fiscal Year defines a financial / operational year window. In India (and at Haritha Hospitals) the default fiscal year runs **1 April → 31 March**. Fiscal Year rows back date-bound HR transactions: leave allocations, leave applications, leave ledger entries, payroll, and tax-period reports. The parent record carries the year window; the child `companies` table lists which Company records use this Fiscal Year.

> **Import flow:** This CSV imports the **parent** Fiscal Year record. The child `companies` rows (one per Company) can be supplied inline as repeated rows in the same CSV OR added via the Frappe web UI. The child rows are documented in the table below.

## Field reference (parent — Fiscal Year)

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| year | Year | Data | Y | 2026-2027 | unique | autoname=field:year; canonical form `YYYY-YYYY`; recommended to use the dash form for clarity |
| year_start_date | Year Start Date | Date | Y | 2026-04-01 | YYYY-MM-DD | first day of the fiscal year; India FY = April 1 |
| year_end_date | Year End Date | Date | Y | 2027-03-31 | YYYY-MM-DD; >= year_start_date | last day of the fiscal year; India FY = March 31 |
| disabled | Disabled | Check | N | 0 | 0/1 | soft-disable flag (rare) |

## Child table: Company (inline row pattern)

The `companies` child table lists which Companies use this Fiscal Year. For a single-company deployment (Haritha Hospitals), this is exactly one row referencing the Haritha Hospitals Company. For multi-company deployments, repeat the parent `year` value and supply a different `company` per row.

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| company | Company | Link→Company | Y | Haritha Hospitals | must exist | one row per Company that uses this Fiscal Year; Frappe Data Import deduplicates parent columns on repeated values |

> **Tip:** Most Data Import tools allow you to keep `year`, `year_start_date`, `year_end_date` constant across multiple rows while varying `company` to populate the child table inline.

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Fiscal Year", ...}` before constructing the document.
- **Gotcha #FY-1 — `year` autoname is the literal value:** Fiscal Year uses `autoname=field:year`, so the `year` you type becomes the primary key. Two rows with the same `year` value will fail `DuplicateEntryError`. Use the canonical `YYYY-YYYY` form.
- **Gotcha #FY-2 — child Company must exist:** The child `companies` table is a Link→Company. Linking to a Company that does not exist fails `LinkValidationError`. Import Company records first (typically a single global row during initial setup, not via workbook).
- **Gotcha #FY-3 — short years (e.g. `2026`) are accepted but ambiguous:** Stock validation does not enforce `YYYY-YYYY`; clients may enter a single year. Recommend `YYYY-YYYY` to disambiguate transitions.
- Fiscal Year has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.
- Production patterns: 1 Fiscal Year per Indian financial year; one Company row in the child table at single-site deployments.

## Healthcare-specific fields

None. Fiscal Year has no custom fields in the `haritha_hospital` custom app.

## When to use this sheet

| Scenario | Use Fiscal Year template? |
|---|---|
| Onboarding a new client with Indian Apr-Mar fiscal calendar | YES — populate one row per fiscal year (current + next) |
| Multi-company deployment with overlapping fiscal years | YES — populate multiple Company rows per Fiscal Year |
| Calendar-year fiscal calendar (Jan-Dec) | YES — set `year_start_date` = Jan 1, `year_end_date` = Dec 31 |
| Just adding next year's window | YES — append a new parent row |

## Common client mistakes

- Setting `year` to a single calendar year (`2026`) — accepted but ambiguous at year-end rollover. Prefer `2026-2027`.
- Setting `year_end_date` < `year_start_date` — fails Date Range validation.
- Linking to a Company that does not exist — fails LinkValidationError.
- Creating two Fiscal Year rows with overlapping date ranges — HRMS allows this but downstream leave / payroll reports may double-count. Use one row per Company per year.
- Forgetting the child `companies` row — parent imports but the Fiscal Year is effectively orphaned; no Company uses it.

## Related

- **Fiscal Year Company** child table is documented inline above.
- **Leave Period** template (`13_leave_period.csv`) draws from Fiscal Year for date boundaries.
- **Leave Allocation** template uses `from_date` / `to_date` that fall within a Fiscal Year window.
- **Leave Ledger Entry** entries are filtered by the Fiscal Year window for period-close reports.
