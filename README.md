# Haritha Hospitals

> ERPNext + HRMS deployment for **Processbricks' Haritha Hospitals** project — shift management + HRMS basics on Frappe v16 with a custom app (`haritta_hospital`).

[![Frappe](https://img.shields.io/badge/Frappe-v16.30.0-blue)](https://frappeframework.com) [![ERPNext](https://img.shields.io/badge/ERPNext-v16.30.0-blue)](https://docs.frappe.io) [![HRMS](https://img.shields.io/badge/HRMS-v16.5.0-blue)](https://docs.frappe.io/hr) [![Public](https://img.shields.io/badge/repo-public-lightgrey)](#license)

---

## About

Production deployment of **Frappe v16.30.0 + ERPNext v16.30.0 + HRMS v16.5.0** for a real hospital chain. A custom app `haritta_hospital` captures 274 production-validated customizations as portable fixtures, plus an idempotent migration script for replicating any env.

| | |
|---|---|
| **Owner** | Venkat Narasimha (Processbricks) |
| **Started** | 2026-04-01 (concept); project repo from 2026-08-19 |
| **Stack** | Frappe v16.30.0 · ERPNext v16.30.0 · HRMS v16.5.0 · custom app `haritta_hospital` |
| **Envs** | `pberpprod.duckdns.org` (prod) · `pberpdev.duckdns.org` (dev) · `dev-erp.duckdns.org` (Venkat VPS prototype) |
| **In scope** | Shift management + HRMS basics (employees, departments, shift types, attendance, leave) |
| **Out of scope** | Wards, beds, OTs, pharmacy, lab, billing, full CoA beyond the 2 cost centers (deferred) |

For full project status (phase history, milestones, customizations catalog, conventions), see **[docs/handbook/00-foundations/00-project-status.md](docs/handbook/00-foundations/00-project-status.md)**.

---

## Quick Start

This is a deployed customization for an existing Frappe bench. To reproduce locally:

```bash
# 1. Install custom app (in your bench env)
bench get-app https://github.com/venkat-narasimha/haritha_hospital.git
bench install-app haritha_hospital --site <yoursite>

# 2. Run master data migration (16 DocTypes, idempotent)
bench execute haritta_hospital.scripts.migrate_master_data.run --site <yoursite>

# 3. Verify
bench --site <yoursite> console
>>> frappe.get_all("Employee", limit=5, pluck="name")
```

See [`scripts/migrate_master_data.py`](scripts/migrate_master_data.py) for the migration script + 10 documented gotchas.

For client data intake templates (master + transaction CSVs), see [`docs/client-onboarding/03-intake-workbook/`](docs/client-onboarding/03-intake-workbook/).

---

## Documentation

| Doc | Purpose |
|---|---|
| **[docs/DIRECTORY_GUIDE.md](docs/DIRECTORY_GUIDE.md)** | Diátaxis-aligned map of all `docs/` content — find the right doc for the right need (tutorial / how-to / reference / explanation) |
| **[docs/HARITHA_HOSPITALS_GUIDE.md](docs/HARITHA_HOSPITALS_GUIDE.md)** | Comprehensive end-to-end guide (architecture, customizations, migration, ops runbook) |
| **[docs/handbook/](docs/handbook/)** | Primary documentation — 9 tiers, ~15,900 lines (foundations, schema, workflow, client, runbooks, process, user manuals, testing, compliance) |
| **[TRACKER.md](TRACKER.md)** | Phase-by-phase history + subagent log |
| **[AGENTS.md](AGENTS.md)** | Process conventions for AI + human collaborators |

---

## Repo layout

```
.
├── README.md                              ← you are here (slim navigation + standard sections)
├── AGENTS.md                              ← process conventions for collaborators
├── TRACKER.md                             ← project phase tracker
├── prompts/                               ← canonical deck-generation prompts (5 modules + 2 utility)
├── scripts/                               ← operational scripts (~45 files; migrate_master_data.py is primary)
├── masters/                               ← source CSVs (19 files, ~1.77 MB, 24,758 rows)
├── docs/
│   ├── DIRECTORY_GUIDE.md                 ← Diátaxis-aligned wayfinding (start here for docs/)
│   ├── handbook/                          ← primary documentation (9 tiers)
│   │   ├── 00-foundations/                ← project overview, status (incl. 00-project-status.md)
│   │   ├── 01-schema/                     ← data model reference
│   │   ├── 02-workflow/                   ← end-to-end process
│   │   ├── 03-client/                     ← HTML presentation decks + demo script + FAQ
│   │   ├── 04-runbooks/                   ← operational procedures
│   │   ├── 04-testing/                    ← manual UI walkthrough + bench execute companion
│   │   ├── 05-process/                    ← methodology, decision logs
│   │   ├── 07-user-manuals/               ← HR Manager / Employee / Admin guides
│   │   ├── 08-testing/                    ← test plans, regression scripts
│   │   └── 09-compliance/                 ← ISO 27001 + CMM L5
│   ├── client-onboarding/                 ← client-facing deliverables (templates, signoff, mapping)
│   │   ├── 03-intake-workbook/            ← 19 CSV+MD templates (master+transaction)
│   │   └── ...
│   ├── HARITHA_HOSPITALS_GUIDE.md
│   ├── DECISIONS.md
│   ├── WORKFLOW.md
│   └── PRODUCTION-READINESS-AUDIT-2026-08-21.md
├── tracker-phases/                        ← per-phase tracker files (master TRACKER.md is the index)
├── config/                                ← cron.tab for backups
├── updates/                               ← phase update JSON snapshots
├── audit/                                 ← fixture audit reports
├── archive/                               ← superseded/historical content (do NOT work from here)
└── pdfs/                                  ← generated PDFs
```

For full directory tree, run `tree -L 3` or see the [DIRECTORY_GUIDE](docs/DIRECTORY_GUIDE.md).

---

## Key operational links

| Env | URL |
|---|---|
| Prod | https://pberpprod.duckdns.org |
| Dev | https://pberpdev.duckdns.org |
| Venkat VPS prototype | https://dev-erp.duckdns.org |
| Roster SPA | https://pberpprod.duckdns.org/hr/roster |

---

## Contributing

See **[AGENTS.md](AGENTS.md)** for process conventions including:

- Git commit identity + message conventions
- Subagent dispatch + verification patterns (this repo uses many)
- "Do not break rules" — no main-session file writes for heavy work; use subagents
- Required vs Optional field rule (don't guess — mark "?" + report)
- Sanitization rule (no real client identifiers in public repo)
- Verification-before-claiming-done discipline

For AI-assisted work, prompts are at `prompts/`. The 5 module deck prompts (`*-cmm-l5-presentation.md`) generate the HTML presentations in `docs/handbook/03-client/`.

---

## Conventions (summary)

- **Git commits:** `venkat-narasimha <srivenkatnarasimha@gmail.com>` (per Rule #11)
- **Custom Fields:** all in `haritta_hospital` fixtures from day 1
- **HRMS pin:** v16.5.0 only (v16.5.1+ breaks on `repost_allowed_types`)
- **Always restart backend container** after `bench install-app` (gunicorn `--preload` sys.path freeze)

---

## License

This is an internal Processbricks / Haritha Hospitals deployment. Custom app `haritta_hospital` source is at https://github.com/venkat-narasimha/haritha_hospital (MIT or as specified there).

---

## Contact

- **Project owner:** Venkat Narasimha
- **Custom app issues:** https://github.com/venkat-narasimha/haritha_hospital/issues
- **Workspace context:** `/root/.openclaw/workspace/` (LEARNINGS + MEMORY there)

---

*README restructured 2026-09-15: slimmed to standard README + repo map; detailed status relocated to [docs/handbook/00-foundations/00-project-status.md](docs/handbook/00-foundations/00-project-status.md).*
