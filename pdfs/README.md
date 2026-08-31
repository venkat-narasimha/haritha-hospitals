# Haritha Hospitals — PDF Documentation

Generated PDFs of all markdown documentation in this repo.

## Structure

| Path | Description |
|---|---|
| `README.pdf` | Top-level project overview |
| `TRACKER.pdf` | Project tracker (master index) |
| `HARITHA_HOSPITALS_GUIDE.pdf` | Comprehensive guide (in `docs/`) |
| `audit/*.pdf` | Audit reports |
| `config/*.pdf` | Config documentation |
| `docs/*.pdf` | Loose top-level docs |
| `docs/phase6/*.pdf` | Phase 6 documentation (Tier 0-8) |
| `masters/*.pdf` | Master documentation |
| `phase-a/*.pdf` | Phase A docs |
| `reports/*.pdf` | Reports |
| `scripts/*.pdf` | Script docs |
| `tracker-phases/*.pdf` | Per-phase tracker files |
| `updates/*.pdf` | Update logs |

## Generation

- **Tool:** pandoc 3.1.13 + tectonic 0.17.0 (portable LaTeX engine)
- **Date:** 2026-08-31
- **Source:** All `*.md` files in this repo (excluding `assets/`, `screenshots/`, `.git/`)
- **Total files:** 67 PDFs (5.7 MB)
- **Mermaid diagrams:** Pre-processed to embedded PNGs from `docs/phase6/03-client/assets/`

## Notes

- PDFs are READ-ONLY snapshots — source of truth is the markdown
- To regenerate: run the converter scripts in `/tmp/` on the VPS (see `preprocess_md.py` + `convert_all.py`)
- One source file (`03.3-faq.md`) had `$$$` characters that triggered LaTeX math mode; these were escaped to `$\$\$` in the source