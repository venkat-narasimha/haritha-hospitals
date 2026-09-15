# P5 Rebuild Plan — Data Templates from Actual Project Schema

**Date:** 2026-09-15
**Owner:** Venkat Narasimha (decision); ERPClaw (execution)
**Scope:** Replace all 19 master-data + 4 transaction templates in `docs/client-onboarding/03-intake-workbook/` (22 files total) + 3 signoff/README docs (25 files total) with versions that reflect the actual ERPNext/Frappe HR schema of this project, not assumed generic patterns.

## Goal (per Venkat)

> "If we give these templates to our clients then after they filling them then we import to ERPNext and give them solution and go for live / production."

Every field on every template must be:
- Importable without error (column name matches stock or custom field name)
- Correctly typed (Data / Link / Date / Int / Float / Select / Check / Table / Text)
- Required/Optional marked per actual DocType enforcement, not assumed

## Sources (consult ALL before writing any template)

| # | Source | What I learn |
|---|---|---|
| 1 | `haritta_hospital/fixtures/custom_field.json` (78 fields) | Custom field names + types + which DocType they attach to |
| 2 | `haritta_hospital/fixtures/property_setter.json` (189 entries) | Field-property overrides (e.g., `reqd: 1` flips on stock fields) |
| 3 | `scripts/migrate_master_data.py` (full read — lines 240-end still pending) | What the actual import code reads + the 10 inline gotchas |
| 4 | docs.frappe.io/hr — Employee / Attendance / Shift Management / Leaves / Employee Lifecycle Management | Canonical stock field names + types for v16.5.0 |
| 5 | SSH into pberpprod via `docker exec erp-prod-backend-1` | Sample 5-10 Employee rows + 3-5 Shift Type rows + 5 Holiday List rows from actual imported data |

## Phases

| # | Phase | Output | Owner | Self-checks |
|---|---|---|---|---|
| **0** | Research | `prompts/P5-rebuild-research.md` (consolidated: custom-field inventory by DocType, stock-field reference per DocType, property-setter overrides, sample actual data, 10 gotchas) | 1 subagent on `minimax/MiniMax-M3` | SC-4, SC-5 |
| **1** | Rebuild 15 master-data templates | Replace `01_master_data/01-15.{csv,md}` (30 files) | 1 subagent | SC-1, SC-2, SC-3, SC-7 |
| **2** | Rebuild 4 transaction templates | Replace `01_master_data/16-19.{csv,md}` (8 files) | 1 subagent | SC-1, SC-2, SC-3, SC-7 |
| **3** | Rebuild README + 2 signoff docs | Replace `README.md` + `03_signoff/01_per_doctype_signoff_template.md` + `03_signoff/02_master_validation_report.md` | 1 subagent | SC-1, SC-7 |
| **4** | Self-checks + final review | All 8 SCs run; fix any failures in place | me (main session) | All 8 SCs |
| **5** | Commit + push | 1 consolidated commit ("rebuild P5 templates from actual project schema") | me | git log + remote HEAD verify |

## 8 Self-checks (explicit, all must pass)

| # | Check | Pass criteria |
|---|---|---|
| **SC-1** | Field count consistency | CSV column count == MD table row count (per template pair) |
| **SC-2** | Required marking consistency | CSV `required` column == MD `Required?` column |
| **SC-3** | No leaks | `grep -rE 'pberpprod\|_b80f05e76a0dcaad|erp-prod|144\.217\.163\.228|/home/vijay/|MYSQL_ROOT_PASSWORD|12603|7829|12562|Hyderabad|Telangana|TSMC'` returns empty in P5 scope |
| **SC-4** | Stock schema accuracy | Every stock field name verified against docs.frappe.io/hr v16.5.0 |
| **SC-5** | Custom-field accuracy | Every custom field name exists in `haritta_hospital/fixtures/custom_field.json` (78-field universe) |
| **SC-6** | Gotcha coverage | All 10 gotchas from `migrate_master_data.py` documented in at least one relevant template's `.md` |
| **SC-7** | Example value patterns | All example values use generic placeholders (no real client data) |
| **SC-8** | End-to-end import path | Each template's CSV column set is a strict subset of what `frappe.core.doctype.data_import.data_import` accepts via standard Import File template — no fields that would be silently dropped or rejected |

## Required vs Optional — sourcing rule (no assumptions)

For each field on each template, required/optional is determined by:

1. **Stock DocType spec** (docs.frappe.io/hr v16.5.0) → if marked required there, it's required
2. **Property Setter override** (`haritta_hospital/fixtures/property_setter.json`) → if a setter changes `reqd: 0` to `reqd: 1`, it's required even if stock says optional
3. **Migration script behavior** (`migrate_master_data.py`) → if the script raises ValidationError on missing field, it's required
4. **Actual data** (pberpprod samples) → if all imported rows populate a field, it's at least functionally required
5. **If sources disagree or unclear** → mark "?" + flag in the template + report to me for resolution before final commit

No guessing. If the research report leaves any field ambiguous, the template carries the "?" flag and I resolve it before final commit.

## Deliverables (final shape)

```
docs/client-onboarding/03-intake-workbook/
├── README.md                                          (rebuilt Phase 3)
├── 01_master_data/
│   ├── 01_department.{csv,md}                         (rebuilt Phase 1)
│   ├── 02_designation.{csv,md}                         (rebuilt Phase 1)
│   ├── 03_employment_type.{csv,md}                     (rebuilt Phase 1)
│   ├── 04_employee_grade.{csv,md}                     (rebuilt Phase 1)
│   ├── 05_branch.{csv,md}                             (rebuilt Phase 1)
│   ├── 06_holiday_list.{csv,md}                        (rebuilt Phase 1)
│   ├── 07_shift_type.{csv,md}                          (rebuilt Phase 1)
│   ├── 08_shift_location.{csv,md}                     (rebuilt Phase 1)
│   ├── 09_shift_schedule.{csv,md}                      (rebuilt Phase 1)
│   ├── 10_employee.{csv,md}                             (rebuilt Phase 1)
│   ├── 11_leave_type.{csv,md}                           (rebuilt Phase 1)
│   ├── 12_leave_policy.{csv,md}                         (rebuilt Phase 1)
│   ├── 13_leave_period.{csv,md}                         (rebuilt Phase 1)
│   ├── 14_leave_allocation.{csv,md}                     (rebuilt Phase 1)
│   ├── 15_shift_assignment.{csv,md}                    (rebuilt Phase 1)
│   ├── 16_attendance.{csv,md}                          (rebuilt Phase 2)
│   ├── 17_employee_checkin.{csv,md}                     (rebuilt Phase 2)
│   ├── 18_leave_application.{csv,md}                    (rebuilt Phase 2)
│   └── 19_leave_ledger_entry.{csv,md}                   (rebuilt Phase 2)
├── 02_settings_checklists/                              (untouched — out of P5 scope; verify in a separate wave)
└── 03_signoff/
    ├── 01_per_doctype_signoff_template.md              (rebuilt Phase 3)
    └── 02_master_validation_report.md                  (rebuilt Phase 3)

+ prompts/P5-rebuild-research.md                        (research artifact, kept in repo for traceability)
+ prompts/P5-rebuild-plan.md                            (this file)
```

## Subagent failure fallback

Given today's pattern of silent subagent failures, if any wave's subagent settles without producing output, I do that wave myself in main session with the same research report + verification protocol. No silent failure goes unfixed.

## Time estimate

| Phase | Owner | Est. |
|---|---|---|
| 0 | subagent | 20 min |
| 1 | subagent | 35 min |
| 2 | subagent | 15 min |
| 3 | subagent | 15 min |
| 4 | me | 20 min |
| 5 | me | 5 min |
| **Total** | | **~110 min** |

## Current status

- Phase 0: dispatched (in progress)
- Plan saved at: `prompts/P5-rebuild-plan.md`
