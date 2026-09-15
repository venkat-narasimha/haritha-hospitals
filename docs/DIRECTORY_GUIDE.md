# Documentation Directory Guide — Diátaxis-aligned

**Purpose:** Find the right document for the right need. This repo's `docs/` is organised using the [Diátaxis framework](https://diataxis.fr/) — the dominant approach for technical documentation (adopted by Django, Kubernetes, Divio, and many others).

---

## The 4 quadrants (Diátaxis)

| Quadrant | Purpose | When you need it | Examples in this repo |
|---|---|---|---|
| **Tutorials** | Learning-oriented | "I'm new, teach me step by step" | `docs/handbook/00-foundations/` (project walkthrough) |
| **How-to guides** | Task-oriented | "I have a job to do" | `docs/client-onboarding/03-intake-workbook/README.md` (client intake process) |
| **Reference** | Information-oriented | "I need to look something up" | `docs/client-onboarding/03-intake-workbook/01_master_data/*.md` (field tables), `docs/handbook/01-schema/` |
| **Explanation** | Understanding-oriented | "I want to know more, why decisions were made this way" | `docs/handbook/02-workflow/`, project walkthrough decks |

**Core principle:** Each document should serve ONE quadrant. Don't mix tutorial steps with reference tables, or how-to recipes with background discussion. If a document drifts across quadrants, split it.

---

## Directory map

### Project-level docs

| Path | Quadrant | When to read |
|---|---|---|
| `README.md` | (project overview) | First read — what is this repo |
| `TRACKER.md` | (project status) | Check current phase + outstanding items |
| `AGENTS.md` | (process conventions) | How AI collaborators work in this repo |

### `docs/handbook/` — primary documentation

| Path | Quadrant | Content |
|---|---|---|
| `00-foundations/` | Tutorials | Project walkthrough, environment overview |
| `01-schema/` | Reference | Data model, ERPNext schema, custom app fixtures |
| `02-workflow/` | Explanation | Migration workflow, end-to-end process |
| `03-client/` | Reference + how-to | 5 HTML presentation decks + demo script + FAQ + speaker script — **primary deliverable for client presentations** |
| `04-runbooks/` | How-to | Operational procedures (deployments, backups, monitoring) |
| `04-testing/` | How-to | Manual UI walkthrough + bench execute companion for transaction testing |
| `05-process/` | Explanation | Methodology, decision logs |
| `07-user-manuals/` | Tutorials | End-user guides (HR Manager / Employee / Admin) |
| `08-testing/` | How-to | Test plans, regression scripts |
| `09-compliance/` | Explanation | ISO 27001-aligned policies + CMM L5 maturity docs |

### `docs/client-onboarding/` — client-facing deliverables (rebuilt in P5)

| Path | Quadrant | Content |
|---|---|---|
| `03-intake-workbook/README.md` | How-to | Workbook overview + 6-step client process |
| `03-intake-workbook/01_master_data/` (NN_*.csv/.md) | Reference | 19 CSV templates + MD notes for client data intake (master + transaction) |
| `03-intake-workbook/02_settings_checklists/` | Reference | HR / Payroll / Auto-Attendance settings checklists |
| `03-intake-workbook/03_signoff/` | How-to | Per-DocType signoff + master validation report |
| `03-intake-workbook/mapping/frappe-hr-data-mapping.md` | Reference | Field-by-field mapping for all 19 templates |
| `03-intake-workbook/AUDIT-REPORT.md` | Reference | Audit of 15 templates vs migration script |
| `03-intake-workbook/reconciliation/sample-raw-to-erp.md` | Explanation | Raw row → prod record example |

### `prompts/` — canonical deck-generation prompts

| Path | Quadrant | Content |
|---|---|---|
| `README.md` | Reference | Prompts directory overview + methodology |
| `*-cmm-l5-presentation.md` (6 files) | Reference | Canonical prompts for 5 module HTML decks + shift-mgmt v2 frozen |
| `build_deck.py` | (generator) | Helper script referenced by the prompts |
| `P5-rebuild-plan.md` | Explanation | The 5-phase P5 rebuild plan |
| `P5-rebuild-research.md` | Reference | Source-of-truth research report for P5 templates |

### `scripts/` — operational code

| Path | Quadrant | Content |
|---|---|---|
| `migrate_master_data.py` | Reference | Master-data migration script with 10 inline gotchas documented |
| (other 44 files) | How-to | Operational scripts (backups, scheduler fixes, setup wizards) |

### `archive/` — superseded/historical

| Path | Content |
|---|---|
| `REPORT.md` | Historical project status (pre-rebuild) |
| `docs/04-discovery/01-frappe-hr-discovery-questions.md` | Archived Venkat's 12 discovery Q&A (Sep 15) |
| `fixtures.tar.gz` | Snapshot of original fixtures for reference |
| `logs/` | Historical operation logs |

---

## How to use this guide

1. **You're new to the project?** → Start with `README.md` → `docs/handbook/00-foundations/` (Tutorial quadrant)
2. **You have a task to do?** → Jump straight to the relevant how-to guide in `docs/handbook/` or `docs/client-onboarding/`
3. **You need to look something up?** → Reference quadrant — schema docs, field tables, template docs
4. **You want to understand why something was designed a certain way?** → Explanation quadrant — workflow + compliance + reconciliation docs

---

## Quadrant migration (gradual, optional)

The existing `docs/handbook/` structure (00-09 tiers) predates Diátaxis adoption here. Over time, content can be re-tagged to the 4 quadrants. No big-bang re-org needed — Diátaxis adoption usually happens gradually. See WriteTheDocs guidance: "start simple to achieve the best results."

---

**Last updated:** 2026-09-15
**Framework:** [Diátaxis](https://diataxis.fr/) (Daniele Procida / Divio)
**Adopted by:** Django, Divio, django CMS, Kubernetes docs (style guide), many others
