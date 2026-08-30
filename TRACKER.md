# Haritha Hospitals — Project Tracker (Index)

**Project:** Haritha Hospitals — Real hospital project (CMM Level 5 target)
**Scope:** Shift management + HRMS basics (employees, departments, shift types, attendance, leave)
**Deferred:** Wards, beds, OTs, pharmacy, lab, billing, full CoA, cost centers
**Owner:** Venkat (Processbricks)
**Started:** 2026-08-19
**Stack:** Frappe 16 / ERPNext 16 / HRMS 16.5.0 (pinned) / payments / custom app (TBD)

---

**Master tracker split:** this file is now a slim index. Full phase detail lives under [`tracker-phases/`](tracker-phases/).

A full backup of the original 1492-line TRACKER.md is preserved at [`tracker-phases/000-FULL-TRACKER-backup.md`](tracker-phases/000-FULL-TRACKER-backup.md).

---

## Phase Index

> **Consolidated 2026-08-30:** 38 numbered phase files merged into 9 logical phase documents (preserving all content). The numbered filenames referenced in the right-column summaries (e.g. `003+004+005`) point to the original files, which are preserved in git history.

| # | File | Summary |
|---|------|---------|
| 000 | [000-FULL-TRACKER-backup.md](tracker-phases/000-FULL-TRACKER-backup.md) | Full 1492-line backup of the original monolithic TRACKER.md (historical reference) |
| S   | [Status-Wrapups.md](tracker-phases/Status-Wrapups.md) | End-of-day status wrap-ups (2026-08-27) + historical rollback status (2026-08-21) |
| L   | [Decisions-Lessons-Learned.md](tracker-phases/Decisions-Lessons-Learned.md) | Decisions log + Known Issues / Lessons Learned |
| Q   | [Subagent-Questions-Pending.md](tracker-phases/Subagent-Questions-Pending.md) | Subagent log, Open Questions, Pending Actions (Next Session) |
| 0   | [Phase-0-Schema-Planning.md](tracker-phases/Phase-0-Schema-Planning.md) | **Phase 0 → 1.5** — Schema Planning, Approval, CSV Master Re-Verification (003+004+005) |
| 2   | [Phase-2-Site-Setup-Rollback-History.md](tracker-phases/Phase-2-Site-Setup-Rollback-History.md) | **Phase 2** — Site Setup, Restart #2 on pberpprod, Pre-flight Backup, all rollback history (006+016+007+008+009+010) |
| 3   | [Phase-3-Data-Import.md](tracker-phases/Phase-3-Data-Import.md) | **Phase 3 → 3.10** — Data Import, Reconcile, Bulk Submit, Property Setter, Attendance Link/Backfill, Backup Bundle Fix (017+018+012+019+021+022+023) |
| 4   | [Phase-4-Shift-Management-Roster-Crash-Fix.md](tracker-phases/Phase-4-Shift-Management-Roster-Crash-Fix.md) | **Phase 4.1 → 4.12** — Shift Type end_time+color, Location backfill, SS submit, SSA create_shifts, Option B 1-SSA-per-employee, Attendance HRMS-recompute, Tailwind color normalization, Roster crash root cause (026+024+025+027+028+029+034+030+033+032+035+031) |
| 0+  | [Phase-0plus-Foundation-Migration.md](tracker-phases/Phase-0plus-Foundation-Migration.md) | **Phase 0+** — Custom app build + Master Data Migration (prod → dev) (036) |
| 6   | [Phase-6-Process-Maturity.md](tracker-phases/Phase-6-Process-Maturity.md) | **Phase 6** — Process & Maturity Documentation, 34 docs / ~14,030 lines (037) |

## Quick Stats

- Environments: pberpdev, pberpprod (pberpqa skipped)
- Active env (2026-08-29): pberpprod.duckdns.org
- See per-phase files for commit counts, customizations captured, and run logs.

## See Also

- [README.md](README.md)
- [docs/](docs/)
- [docs/phase6/README.md](docs/phase6/README.md)
