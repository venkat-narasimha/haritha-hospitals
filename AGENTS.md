# AGENTS.md — Process Conventions for AI + Human Collaborators

**Purpose:** Conventions for working in this repo. Whether you're a human contributor or an AI subagent (like the ones dispatched during P5 rebuild), these are the rules of the road.

---

## Repo structure quick-reference

See `docs/DIRECTORY_GUIDE.md` for the full Diátaxis-aligned directory map. Key things to know:

- `prompts/` — canonical deck-generation prompts + P5 plan + P5 research (source-of-truth for AI work)
- `scripts/migrate_master_data.py` — production migration script with 10 inline gotchas
- `docs/handbook/` — primary documentation (9 tiers)
- `docs/client-onboarding/` — client-facing deliverables (templates, signoff, mapping)
- `archive/` — superseded content (do NOT work from here)

---

## AI subagent conventions

### When to use a subagent vs. main session

| Use a subagent for | Do in main session when |
|---|---|
| Reading N source files + writing a single deliverable (e.g., generating 19 CSV templates from research report) | Quick file inspection or 1-line change |
| Long content production (multi-KB document, deck generation) | Multi-step verification + commit + push |
| Tasks that benefit from isolated context (read fresh, no carry-over confusion) | Tasks that need live memory of prior conversation turns |

### Subagent prompt pattern (proven to work)

A subagent prompt that succeeds has these properties:

1. **Exact output target** — file path + format + acceptance criteria
2. **Explicit verification protocol** at the end — file exists + grep checks + commit hash + report
3. **One pass, no iteration** — subagent should commit + report; iteration handled by main session
4. **model override** when needed — explicitly specify the model
5. **"DO NOT silently settle"** — subagents must report explicitly even on failure

Pattern that failed in this session: dispatching subagent with vague task and waiting. The fix: include the verification protocol in the prompt itself, not as a follow-up.

### Known subagent failure modes in this repo (observed Sep 2025)

- **Silent settlement**: subagent reports completion but produces no files. Counter with explicit verification protocol + file size thresholds + grep checks.
- **8+ hour zombie runs**: subagent marked "running" for hours with no output. Mitigation: dispatch with hard time limit + check-in checkpoints + cancellation plan.
- **Sandbox path mismatches**: subagent writes to a path that doesn't exist or is inaccessible to main session. Mitigation: verify on disk + commit before claiming done.

---

## Git commit conventions

### Commit author identity (MEMORY rule — non-negotiable)

```bash
git config user.name "venkat-narasimha"
git config user.email "srivenkatnarasimha@gmail.com"
```

This repo's deploy key (`/root/.openclaw/github_key`) is for github.com. The SSH key for the VPS (`/root/.openclaw/ssh_key`) is separate.

### Commit message format

```
<type>(<scope>): <short description>

<optional body>

Refs:
<related files>
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`. Scope: `<module>` or `<area>`. Short description: imperative, lowercase, no period.

### Commit granularity

- One commit per logical change set, even if the change spans multiple files (see P5 Wave 2 commit: 19 files in one commit, related to "rebuild 4 transaction templates")
- Avoid bundling unrelated changes — separate commits for separate concerns
- Prefer smaller, atomic commits over large omnibus commits

---

## File path conventions

| Pattern | Purpose | Example |
|---|---|---|
| `prompts/<doc>-cmm-l5-presentation.md` | Canonical deck-generation prompt for a module | `prompts/org-management-cmm-l5-presentation.md` |
| `prompts/P5-*.md` | P5 rebuild artifacts (plan, research) | `prompts/P5-rebuild-research.md` |
| `docs/handbook/NN-<topic>/` | Numbered handbook tier | `docs/handbook/04-runbooks/` |
| `docs/client-onboarding/NN-*/` | Numbered client onboarding section | `docs/client-onboarding/03-intake-workbook/` |
| `archive/<category>/` | Archived content (do NOT work from here) | `archive/docs/04-discovery/` |
| `NN_<doctype>.csv` + `NN_<doctype>.md` | Template pairs (CSV data + MD documentation) | `01_department.csv` + `01_department.md` |

---

## Required/Optional field rule

When documenting a field's required status in CSVs or templates:
- **Required**: stock DocType spec marks it required, Property Setter sets reqd=1, script rejects without it, or 100% of imported data populates it
- **Optional**: none of the above
- **"?" flag**: ambiguous — leave the marker + flag for human resolution

Don't guess. If uncertain, mark "?" + report to human.

---

## Sanitization rule (public repo)

This is a **public** repo (`venkat-narasimha/haritha-hospitals`). Before committing:
- NO real client identifiers (hospital name, employee names, employee counts)
- NO real institutional references (regulatory bodies, geographic names like Hyderabad/Telangana)
- NO real values from pberpprod in code or templates
- Use **generic placeholders only** (e.g., `Employee A`, `Site A`, `Department A`, `REG-A-0001`, `2026-09-01`)
- The exception is the `archive/` directory where historical content with real context may live

Grep before committing (mandatory):
```bash
grep -rE 'pberpprod|_b80f05e76a0dcaad|erp-prod|144\.217\.163\.228|/home/vijay/|MYSQL_ROOT_PASSWORD|12603|7829|12562|Hyderabad|Telangana|TSMC|Haritha Hospitals' <changed-paths>
```

If grep returns matches in code/templates → replace with generic placeholders before committing.

---

## MEMORY hygiene

When updating `MEMORY.md` (in the workspace root, not in this repo):
- Add new sections under "Active Projects" with current state + commits + open items
- Don't write to MEMORY yourself if a heartbeat will capture the changes
- For long-lived facts that span sessions, write here

---

## Handoff doc convention

When ending a session that another session will continue:
1. Create `prompts/<topic>-handoff.md` (or `archive/<topic>/<name>-handoff.md`)
2. Include: TL;DR + current state (git log, file inventory) + pending work + open decisions + caveats
3. Provide a copy-paste-able "continue-work prompt" inside the handoff doc
4. Update `MEMORY.md` with a "handoff" entry referencing the doc path
5. Commit + push the handoff doc in the current session

The previous P5 rebuild handoff is at `prompts/P5-rebuild-handoff.md` — good template reference.

---

## "Do not break rules" rule (Venkat's explicit instruction)

This is Venkat's standing rule. When he says "do not break rules and do not do in main session", he means:
- **Use subagents** for heavy work, not main-session file writes
- If a subagent fails, **report the failure explicitly** rather than doing the work in main session
- After 2+ failures on the same task, **stop and ask Venkat** rather than retrying or bypassing

---

## Verification before claiming "done"

Any task completion claim (commit, push, file write) must include:
1. **Verify on disk** — does the file exist? Is the size reasonable?
2. **Verify in git** — is it staged? Committed? Pushed?
3. **Verify content** — does the content actually match the task brief (not just placeholder)?

"Don't assume" extends to verification — don't claim done without checking.
