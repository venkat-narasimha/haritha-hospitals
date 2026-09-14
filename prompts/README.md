# Prompts Directory

> **Purpose:** Canonical prompts that produce Frappe HR presentation decks (HTML).
> Each prompt is a complete, deterministic spec for generating one self-contained HTML deck.
> Frozen template: `shift-management-cmm-l5-presentation-v2.md` (do not modify).

## Current Prompts

| Prompt | Module | Output Deck | v |
|---|---|---|---|
| shift-management-cmm-l5-presentation-v2.md | Shift Management | shift-management-presentation-v2.html | 2.0 (frozen) |
| org-management-cmm-l5-presentation.md | Organization Management | org-management-presentation.html | 2.2 |
| attendance-management-cmm-l5-presentation.md | Attendance Management | attendance-management-presentation.html | 1.0 (pending rewrite) |
| leave-management-cmm-l5-presentation.md | Leave Management | leave-management-presentation.html | 1.0 (pending rewrite) |
| lifecycle-management-cmm-l5-presentation.md | Employee Lifecycle | lifecycle-management-presentation.html | 1.0 (pending rewrite) |
| frappe-hr-overview-cmm-l5-presentation.md | Frappe HR Overview (synthesis) | frappe-hr-overview-presentation.html | 1.0 (pending rewrite) |

## Prompt Maintenance Workflow

When a deck needs visual updates or content changes:

1. Edit the corresponding `*.html` file manually (Venkat-approved copy).
2. Update the corresponding `*-cmm-l5-presentation.md` prompt to reflect the new content.
3. Run the deck generator (Venkat's choice of tool) on the updated prompt.
4. Commit all together (HTML + prompt + any generator changes).

To update an existing prompt:

1. Read the current prompt + the corresponding HTML (verify byte-for-byte match if frozen).
2. Re-read this README for shared conventions.
3. Modify in place — preserve §1–§7 (Role through Slide Template), update §8 slide-by-slide specs as needed.
4. Update the "Current Prompts" table above with new version.
5. Self-verify per the prompt's §15 checks.
6. Commit.

## Shared Methodology (Lessons #151–#164)

All prompts follow CMM L5 process management principles:

- **#151** Quantitative process management — every spec has a measurable check (§15).
- **#152** Defect prevention — verify before declaring done (§16 self-review).
- **#153** Change management — version each prompt, document every change.
- **#154** Technology change management — design tokens frozen (§6).
- **#155** Peer review — generator output self-reviewed before "done".
- **#156** Process measurement — slide counter `N / TOTAL` must match exactly.
- **#157** Process analysis — single root cause for schema slide duplication (preview + full spec).
- **#158** Process innovation — speaker notes pattern reusable across all slides.
- **#159** Continuous improvement — lessons from earlier prompts are explicit constraints in §14.
- **#160** Defect analysis — schema SVG character escaping (`'` artifacts).
- **#161** Content freshness check — do not lie about dates; verify mtime vs claimed.
- **#162** Always do broad grep before claiming scope.
- **#163** "Up to date?" means BOTH structure AND metadata.
- **#164** Per-directory footers drift independently — rely on README version table instead.

## Schema SVG Conventions

When designing the schema SVG for a prompt's §13:

1. **Relationship labels on connectors** — 1–2 word label per connector (e.g., "belongs to", "creates", "references").
2. **Color coding by layer** — Master data uses primary blue; Config uses accent sky; Transaction/process uses secondary slate; Reference uses muted.
3. **Grouping rectangles** — Dashed `<rect>` (`stroke-dasharray="4,4"`) around related entity clusters, with small cluster label.
4. **Layered positioning** — Top = context; Middle = core; Center = master anchor; Surrounding = attributes.
5. **Field hints in labels** — Each entity box shows entity name + 1–3 key fields in smaller text below.
6. **Legend box** — Small legend (120×80) in corner explaining colors + connector symbols.
7. **All natural entities** — Include every entity the module naturally has; don't artificially reduce.
8. **Slide 4 vs Slide 16 differentiation** — Slide 4 = clean preview (entities + groupings only, NO connector labels, NO legend); Slide 16 = full spec (adds connector labels + field hints + legend).

## Slide Count + Slide 12 Decision Rationale

Slide count varies per deck based on entity count + concept coverage. Decisions are documented in §8 of each prompt during creation/rewrite.

Slide 12 content type varies per deck:

- **Image placeholder** — when the natural "central artifact" is a screenshot (e.g., Roster in shift-mgmt).
- **Table mockup** — when the central entity deserves a data table (e.g., Employee key fields in org-management).
- **Inline SVG diagram** — when workflow/process is more accurate as a vector (e.g., approval flows).
- **Roadmap diagram** — synthesis decks use module navigation diagrams.

Constraints (frozen from v2 §14):

- Body ≤100 words per slide.
- One focal point per slide.
- Generic examples only — no Haritha-specific data, no employee counts, no company-specific metrics.
- No filler phrases.
- Define jargon on first use.

## How to Add a New Prompt

1. Identify the Frappe HR module + its DocTypes.
2. Read https://docs.frappe.io/hr/{module} for canonical structure.
3. Use `shift-management-cmm-l5-presentation-v2.md` as template (frozen).
4. Dispatch a subagent with: full v2 prompt + this README + per-deck decisions (slide count + slide 12 type + schema entity list + layout concept).
5. Subagent writes + self-verifies + reports.
6. Add to "Current Prompts" table above with version.
7. Review + commit.

## How to Add a New Module/Schema SVG

1. Identify DocTypes from the Frappe HR docs.
2. Decide: which entities belong in the SVG, how to group them (dashed rectangles), what relationships to show with labels.
3. Apply the 8 Schema SVG Conventions above.
4. For Slide 4 vs Slide 16 differentiation, see "Schema SVG Conventions" #8.
5. Specify in the prompt's §13 (Schema Flowchart) with two clear subsections: "Slide 4 variant" + "Slide 16 variant".
