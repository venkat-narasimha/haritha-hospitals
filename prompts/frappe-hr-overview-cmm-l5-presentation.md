## Frappe HR Overview — Deck Prompt (v2)

> **Status:** Active spec · **Version:** 2.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
> **Audience:** Anyone generating or auditing this presentation deck (LLM agent, technical writer, reviewer).
> **Output:** `docs/handbook/03-client/frappe-hr-overview-presentation.html` (single self-contained HTML).

---

## 1. Role

You are a **technical writer + front-end developer** producing a single self-contained HTML presentation that introduces **Frappe HR** as a complete HR + Payroll application for hospital operations. You follow CMM Level 5 documentation standards in your process (not in the deck content).

CMM L5 means:

- **Quantitative process management** — every spec below has a measurable check.
- **Defect prevention** — verify before declaring done (see §16 self-review).
- **Change management** — version this prompt, document every change.
- **Technology change management** — design tokens frozen, do not improvise new values.

## 2. Audience (3 personas)

1. **Priya — HR Manager (internal):** practical features, KPIs, ROI on deployment.
2. **Arjun — Operations Lead (internal):** workflow, error reduction, daily-life impact.
3. **Sarah — External Evaluator (external):** capabilities, cost, ease vs SAP / Workday / BambooHR.

## 3. Goal

Produce a **14-slide** self-contained HTML presentation introducing the full Frappe HR landscape and routing the audience to the right deep-dive module deck. Educational, general audience, light theme, professional + minimal + clean.

**Structural choices (v2.0):**

- Overview is the **synthesis** deck — high-level, not exhaustive. Individual module decks (org-management v2.2, attendance v2.1, shift-management v2.0 frozen, leave-management v2.0, lifecycle-management v2.0) provide the detail.
- 14 slides vs the 16–22 slide module decks because this is a navigator, not a feature explainer.
- 5 module clusters arranged **radially** around Employee at the center (slide 4 preview / slide 13 full spec).
- Slide 12 = inline SVG module roadmap showing which deck for which audience question.
- "Why choose" framing absorbed into Conclusion (matches attendance v2.1 + org-mgmt v2.0 + lifecycle + leave v2.0 pattern).

## 4. Time Budget

- **Total: 40 minutes** (32 min content + 8 min Q&A).
- Per-slide timings sum to ~32 min — speaker can compress/expand as needed.
- See §8 for per-slide timings.

## 5. Output Specs

- **Format:** single `.html` file, fully self-contained (inline CSS, no external assets, no JavaScript libraries).
- **Slides:** exactly **14**, each `<section class="slide" id="slide-N">`.
- **Counter:** every slide shows `N / 14` (not 13, not 15 — must match exactly).
- **Navigation:** keyboard arrows (←/→) + click handlers (Prev/Next buttons + click-half slide).
- **Speaker notes:** hidden by default, toggle with `S` key. Body class `show-speaker-notes`.
- **Print:** include `@media print { ... }` for clean PDF export.
- **Accessibility:** semantic HTML, contrast ≥4.5:1 for body text, keyboard nav, ARIA labels.
- **No external images** — use inline SVG or pure CSS shapes.
- **No JavaScript libraries** — vanilla JS only.

## 6. Design Tokens (exact values — do not improvise)

### 6.1 Colors

| Token | Hex | Use |
|---|---|---|
| `--primary` | `#1e40af` | Deep blue (titles, org mgmt cluster) |
| `--secondary` | `#64748b` | Slate (speaker notes, lifecycle cluster) |
| `--accent` | `#0ea5e9` | Sky (attendance + shift clusters) |
| `--text` | `#0f172a` | Near-black (body text) |
| `--muted` | `#94a3b8` | Muted (boundaries, dividers) |
| `--bg-odd` | `#ffffff` | Odd slides background |
| `--bg-even` | `#f8fafc` | Even slides background |
| `--code-bg` | `#f1f5f9` | Inline code background |
| `--code-text` | `#0f172a` | Inline code text |

### 6.2 Typography

- **Body:** `Inter, system-ui, -apple-system, sans-serif` at 18px / 1.6 line-height.
- **Headings:** same font, weight 600. Slide title 40px, h3 24px, h4 18px.
- **Code:** `JetBrains Mono`, `ui-monospace`, monospace at 14px.

### 6.3 Layout

- Max-width **960px**, centered, `min-height: 680px`, `min-height: 640px` for slides.
- Padding: **64px top/bottom, 32px sides**.
- Spacing scale: 8 / 16 / 24 / 32 / 48 / 64 px — use these exact values, no other sizes.

### 6.4 Animation

- Slide-in: 200ms ease-out, `translateY(8px) → 0` + `opacity: 0 → 1`.

## 7. Slide Template (apply uniformly to all 14 slides)

Every slide MUST include:

1. `<div class="slide-number">N / 14</div>`
2. `<h2 class="slide-title">…</h2>`
3. `<div class="body">… main content (≤100 words), one focal visual …</div>`
4. `<aside class="speaker-notes">…</aside>` — hidden by default, toggle with `S` key.
5. **Transition note** (1 sentence) — included inside speaker notes.

## 8. Slide-by-Slide Specs (14 slides)

### Intro (slides 1–3)

**Slide 1 — Frappe HR Overview** (30s) — Title slide
- Subtitle: "A practical synthesis of the five mandatory modules for hospital operations"
- Metadata block (bottom-right): Version 2.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Transition: "Let's start with what we're covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "Frappe HR Landscape" / "5 Mandatory Modules" / "How They Connect" / "Demo Roadmap".
- Numbers: 01 / 02 / 03 / 04.
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Transition: "Now let's look at the data model — how the five modules connect to the Employee master."

### Early Schema Preview (slide 4 — clean preview, no labels)

**Slide 4 — Schema: Frappe HR Ecosystem** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13 § Schema Flowchart § Slide 4 variant).
- Above: `<strong>Architecture:</strong> How the five Frappe HR modules relate to the Employee master.`
- Below: "The Employee master sits at the center with five module clusters arranged radially. Arrows show key data flows between modules."
- Speaker notes: "Employee is at the center. Five module clusters around it: Org Management (top, primary), Attendance (right, accent), Shift Management (bottom-right, accent), Leave Management (bottom-left, accent), Lifecycle Management (left, secondary). One big dashed circle grouping them all as 'Frappe HR scope'. Brief mention only. Recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the big picture — why Frappe HR matters for hospital operations."

### Module-by-Module Intro (slides 5–10)

**Slide 5 — Why Frappe HR for hospital operations** (2 min)
- 3 bullets: open-source + code ownership / hospital-adaptable (ward rotations, on-call patterns, statutory compliance) / modular + extendable without core changes.
- Visual: 3 hospital-shape icons (bed / monitor / stethoscope) with Frappe HR motifs inside.
- Transition: "Let's meet each of the five mandatory modules."

**Slide 6 — Organization Management (defines people + hierarchy)** (2 min)
- Lead paragraph: "Organization Management defines the Employee master and the org structure (Department, Branch, Designation, Grade, Employment Type). It's the foundation everything else assumes."
- 3 bullets: Employee + Department + Branch / 200+ Employee fields across tabs / multi-branch ready.
- Visual: hierarchical tree (Company → Department → Employee).
- Deep-dive pointer: "See `docs/handbook/03-client/org-management-presentation.html` for details."
- Transition: "Next: how do we know who's actually showing up?"

**Slide 7 — Attendance Management (daily presence)** (2 min)
- Lead paragraph: "Attendance Management tracks daily presence (Present / Absent / On Leave / Half Day). Inputs from biometric + mobile + manual routes through Auto Attendance."
- 3 bullets: multi-source inputs (biometric / mobile / manual) / Auto Attendance engine / 12,000+ rows/month scale.
- Visual: 3 input source icons converging into Attendance ledger.
- Deep-dive pointer: "See `docs/handbook/03-client/attendance-management-presentation.html` for details."
- Transition: "Presence is one side — the other is when work happens."

**Slide 8 — Shift Management (when work happens)** (2 min)
- Lead paragraph: "Shift Management defines shift patterns (Shift Type), assigns them per day per employee (Shift Assignment), and rolls up to attendance via Auto Attendance. The frozen v2 deck covers this in depth."
- 3 bullets: 25+ Shift Types / 7,800+ Shift Assignments / shift roster view.
- Visual: 7-day calendar with morning/evening/night/OFF cells.
- Deep-dive pointer: "See `docs/handbook/03-client/shift-management-presentation-v2.html` (canonical, frozen)."
- Transition: "What about when work doesn't happen — leave."

**Slide 9 — Leave Management (policies + applications + audit)** (2 min)
- Lead paragraph: "Leave Management configures leave types + policies + periods, allocates days per employee, and records every leave movement as an immutable Ledger Entry."
- 3 bullets: 7 Leave Types / 3-layer (Config → Policy → Action) / Leave Ledger Entry audit trail.
- Visual: 3-layer schematic (Config top, Policy middle, Action bottom) with Employee center.
- Deep-dive pointer: "See `docs/handbook/03-client/leave-management-presentation.html` for details."
- Transition: "One last mandatory module — what about when employees start, move, or leave?"

**Slide 10 — Employee Lifecycle Management (hire to retire)** (2 min)
- Lead paragraph: "Employee Lifecycle covers Onboarding (entry), Promotion + Transfer (growth), Separation (exit), and Skill Map (supporting reference). Structured hire-to-retire workflows."
- 3 bullets: 5 lifecycle documents / 3 dashed groupings (Entry / Growth / Exit) / supporting Skill Map.
- Visual: 4-stage horizontal timeline (Pre-joining → Onboarding → Growth → Separation).
- Deep-dive pointer: "See `docs/handbook/03-client/lifecycle-management-presentation.html` for details."
- Transition: "Now the connections — how these five modules interact in real workflow."

### Connections + Roadmap + Schema Full + Conclusion (slides 11–14)

**Slide 11 — How the modules connect (scenario walkthrough)** (2 min)
- Lead paragraph: "Here's a real Day 1 scenario showing the modules in concert."
- 5-step scenario:
  1. **Org Mgmt** — Priya is hired → Employee record created with Department (Nursing) + Branch (Main).
  2. **Shift Mgmt** — Auto-assigned to Morning shift (06:00–14:00) for 30 days.
  3. **Attendance** — Biometric punches → Auto Attendance creates Attendance row (Present).
  4. **Leave Mgmt** — Priya applies Sick Leave for Day 5 → Leave Approver approves → Leave Ledger posts.
  5. **Lifecycle** — After 90 days, Probation review → confirmed via Employee Promotion.
- Visual: 5-step horizontal flow with module labels above each step.
- Transition: "Now your audience asks: which deck covers which question?"

**Slide 12 — Module Roadmap (SVG)** (2 min)
- Lead paragraph: "Here's where to find detail for each module. Pick the deck that matches your audience's question."
- Inline SVG module roadmap: 6 boxes (5 modules + Employee) arranged as a graph with edges showing input → output flow.
  - Org Mgmt (top-left) → "When defining people + hierarchy"
  - Attendance (right) → "When tracking daily presence"
  - Shift Mgmt (bottom-right) → "When scheduling shifts"
  - Leave Mgmt (bottom-left) → "When managing leave"
  - Lifecycle (left) → "When handling onboarding / promotion / exit"
  - Employee (center) → "Master — referenced by all"
- Visual: `<div class="roadmap-graph">` with 6 boxes + connectors + audience-question labels.
- Transition: "What's NOT in this Frappe HR overview — what we deliberately defer."

**Slide 13 — Schema: Frappe HR Ecosystem (full spec)** (3 min) — full spec, ENHANCED over slide 4 (see §13 § Schema Flowchart § Slide 13 variant)
- Above: `<strong>Architecture:</strong> How the five Frappe HR modules relate to the Employee master — with connector labels, module cluster colors, and a legend.`
- Below: "The Employee master sits at the center. Five module clusters (Org Mgmt, Attendance, Shift, Leave, Lifecycle) are arranged radially. Arrows show key data flows between modules (defines, checks in via, scheduled via, applies for, auto-creates On Leave, stages through). One dashed circle grouping them as 'Frappe HR scope'."
- Speaker notes: "Walk the audience through each connection. The radial layout makes Employee the obvious anchor. Arrows show that Org Mgmt defines the Employee, Attendance + Shift track daily presence, Leave handles absence, Lifecycle covers stage changes. The dashed grouping shows everything is one Frappe HR scope."
- Transition: "Let's wrap up."

**Slide 14 — Conclusion + Why choose + Next Steps** (2 min)
- "Key Takeaways" h3 + numbered list (3 items).
  - Frappe HR covers hire-to-retire via 5 mandatory modules.
  - Employee master is the universal anchor; modules hang off it.
  - Each module has its own deep-dive deck for detail.
- "Why choose ERPNext + Haritha" h4 (absorbed from standalone slide):
  - 3 bullets (concise): Open source + code ownership / Modular — pay only for what you use / Active community + extensible architecture.
- "Next Steps" h4 + 3 bullets (start with overview then deep-dive to relevant module / run the demo sandbox at `demo.example.com` / architecture review with our team).
- Transition: "Thank you and welcome to the Q&A."

## 9. Slide Template HTML

```html
<section class="slide" id="slide-N">
  <div class="slide-number">N / 14</div>
  <h2 class="slide-title">[Slide Title]</h2>
  <div class="body">
    [Main content here, max 100 words, with one focal visual]
  </div>
  <aside class="speaker-notes">
    [What the presenter says — 2–3 sentences. Hidden by default; press 'S' to toggle.]
    <br><br>
    Transition: [1 sentence]
  </aside>
</section>
```

> NOTE: Slide 1 and other title-only slides use `<div class="body title-wrapper">` instead of plain `<div class="body">`.

## 10. Speaker Notes Toggle (vanilla JS)

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 's' || e.key === 'S') {
    document.body.classList.toggle('show-speaker-notes');
  }
  if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
    e.preventDefault();
    /* next slide */
  }
  if (e.key === 'ArrowLeft'  || e.key === 'PageUp') {
    e.preventDefault();
    /* prev slide */
  }
});
```

CSS rule:

```css
.speaker-notes { display: none; font-size: 14px; color: var(--secondary); border-left: 3px solid var(--accent); padding-left: var(--space-16); margin-top: var(--space-24); font-style: italic; background: rgba(241, 245, 249, 0.6); padding-top: var(--space-8); padding-bottom: var(--space-8); }
body.show-speaker-notes .speaker-notes { display: block; }
```

## 11. Concrete Examples — GOLD STANDARDS

### 11.1 Slide 4 (Schema radial preview) — GOLD STANDARD

CSS excerpt for the radial module cluster layout (5 modules around Employee center, wrapped in a single dashed circle "Frappe HR scope"):

```css
.module-cluster { display: inline-block; padding: var(--space-16) var(--space-24); border-radius: 50%; min-width: 120px; min-height: 60px; text-align: center; background: var(--bg-even); border: 1.5px solid; }
.module-cluster.org { border-color: var(--primary); background: rgba(30, 64, 175, 0.05); }
.module-cluster.attendance, .module-cluster.shift { border-color: var(--accent); background: rgba(14, 165, 233, 0.05); }
.module-cluster.lifecycle { border-color: var(--secondary); background: rgba(100, 116, 139, 0.05); }
.module-cluster .cluster-name { font-size: 14px; font-weight: 600; color: var(--text); }
.module-cluster .cluster-entities { font-size: 11px; color: var(--secondary); margin-top: 2px; }
```

### 11.2 Slide 12 (Module Roadmap SVG) — GOLD STANDARD

CSS excerpt for the 6-box roadmap graph:

```css
.roadmap-graph { display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 100px); gap: var(--space-24); margin-top: var(--space-32); max-width: 720px; }
.roadmap-cell { padding: var(--space-16); border-radius: 8px; background: var(--bg-even); border: 1px solid #e2e8f0; }
.roadmap-cell.module { font-weight: 600; color: var(--text); }
.roadmap-cell.question { font-size: 13px; color: var(--secondary); font-style: italic; }
.roadmap-cell .cell-title { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
.roadmap-cell .cell-desc { font-size: 12px; color: var(--secondary); }
```

## 12. Image / Diagram Placeholder (Slides 6, 7, 8, 9, 10, 11)

Slides with inline form/timeline/scenario flow mockups use pure CSS (no external images).

## 13. Schema Flowchart (Slides 4 + 13)

Both slides 4 and 13 contain an inline SVG (740×320 viewBox). They share the same entity set + groupings but differ in annotation density.

### 13.1 Slide 4 variant — clean preview

- **6 element positions arranged radially**:
  - **Employee** — center (primary `#1e40af`, 140×60 — master anchor)
  - **Org Management cluster** — top (primary, 140×60 rounded module box)
  - **Attendance cluster** — right (accent `#0ea5e9`, rounded module box)
  - **Shift Management cluster** — bottom-right (accent, rounded module box)
  - **Leave Management cluster** — bottom-left (accent, rounded module box)
  - **Lifecycle Management cluster** — left (secondary `#64748b`, rounded module box)
- **1 dashed circle** (or rounded rectangle) wrapping all 5 module clusters + Employee, labeled "Frappe HR scope" (small label at top of canvas).
- Each module cluster box contains 2-3 entity names in smaller text (e.g., "Org Mgmt — Employee, Department, Branch").
- NO connector labels, NO module descriptions, NO legend box.
- Connector paths in slate (`#94a3b8`); 5-6 arrows from Employee to each module cluster (implicit radial flow).

### 13.2 Slide 13 variant — full spec

Same as Slide 4 PLUS:

- **Connector labels** (1–2 words each, font-size 11, fill="secondary"):
  - Org Management → Employee: `"defines"`
  - Employee → Attendance: `"checks in via"`
  - Employee → Shift Management: `"scheduled via"`
  - Employee → Leave Management: `"applies for"`
  - Attendance ← Leave Management: `"auto-creates On Leave"` (curved arrow or dashed)
  - Lifecycle → Employee: `"stages through"` (Lifecycle → Employee direction showing employee moves through stages)
- **Field hints** (entity names inside each module cluster, slightly larger than in Slide 4 preview for clarity):
  - Org Management: `Employee, Department, Branch, Designation`
  - Attendance: `Attendance, Employee Checkin, Auto Attendance`
  - Shift Management: `Shift Type, Shift Assignment, Holiday List`
  - Leave Management: `Leave Type, Leave Policy, Leave Application, Leave Ledger Entry`
  - Lifecycle Management: `Employee Onboarding, Promotion, Transfer, Separation, Skill Map`
- **Legend box** (120×80 rect, white fill, slate border, bottom-left of canvas, ~translate(15,180)):
  - Color swatches: primary = `Org Mgmt / Master`; accent = `Attendance / Shift / Leave`; secondary = `Lifecycle`.
  - Connector symbols: solid arrow = `direct lifecycle`; dashed arrow = `cross-module data flow`.

### 13.3 SVG technical specs

- viewBox: `0 0 740 320`, width="740", height="320".
- Font family: `var(--font-main)` for cluster names, `var(--font-mono)` for entity hints.
- Module cluster box dimensions: 140×60 (rounded rectangle, `rx="30"` for ellipse-like feel, or sharp rectangle for architectural feel — pick one and stay consistent).
- Employee master anchor: 140×60 (rect, primary color).
- Dashed grouping circle stroke-width: 1.5 (the "Frappe HR scope" wrapper).
- Layout coordinates (approx, radial positioning):
  - Employee: `x=300 y=130 w=140 h=60` (center)
  - Org Management: `x=300 y=20 w=140 h=60` (top)
  - Attendance: `x=590 y=130 w=140 h=60` (right)
  - Shift Management: `x=480 y=230 w=140 h=60` (bottom-right)
  - Leave Management: `x=120 y=230 w=140 h=60` (bottom-left)
  - Lifecycle Management: `x=10 y=130 w=140 h=60` (left)
  - "Frappe HR scope" dashed wrapper: `<circle cx=370 cy=160 r=180 />` (or rounded rect `x=0 y=10 w=740 h=300 rx=150`)
- Reference the existing shift-mgmt v2 SVG for visual style consistency. Use the `rx="30"` rounded rectangle style for module clusters to visually distinguish them as clusters (not single doctypes).

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened.
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **Module roadmap image placeholder (v1 slide 12)** — replaced by inline SVG roadmap graph (§11.2 gold standard).
- **"Why choose ERPNext + Haritha" as standalone slide** — absorbed into Conclusion slide 14 (matches attendance v2.1 + org-mgmt v2.0 + lifecycle v2.0 + leave v2.0 pattern).
- **Flexible Benefits / Payroll as in-scope** — explicitly OUT of scope (deferred per Venkat's call).

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 2.0 · Date 2026-09-14).
- **No vendor-specific data** — no employee counts, no real customer names, no company-specific metrics.
- **Use generic illustrative examples** ("Employee A", "Morning shift 06:00–14:00", "FY 2025–2026").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Each module slide MUST link to its deep-dive deck** via the "Deep-dive pointer" pattern (slide 6 → org-mgmt deck, slide 7 → attendance deck, etc.) — this IS the navigation purpose of the overview deck.
- **Define jargon on first use** ("DocType", "Module", "Shift Type").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content).

## 15. Quality Bar (10 checks — verify before declaring done)

1. Exactly **14** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 = Schema preview (5 module clusters + Employee center + 1 dashed "Frappe HR scope" wrapper — NO connector labels, NO legend, NO detailed entity lists).
4. Slide 13 = Schema full spec (5 module clusters + Employee + 6 labeled connectors + legend + detailed entity lists inside clusters).
5. Per-slide timings sum to ~32 minutes.
6. Both SVGs render correctly (no broken tags, no overlap).
7. Print stylesheet works.
8. No filler phrases anywhere.
9. Slide 12 = Module Roadmap SVG (6 cells — 5 module + Employee — with audience-question labels) — NOT image placeholder.
10. Each module slide (6, 7, 8, 9, 10) has a deep-dive pointer in format `See docs/handbook/03-client/{name}-presentation.html for details.` — this is the overview's navigation purpose.

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 14`.
4. **Match this prompt's slide-by-slide spec exactly.** Any drift between spec and generated HTML is a defect.
5. Only declare "done" when all 10 checks pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/frappe-hr-overview-presentation.html`

## 18. Prompt Maintenance Workflow

See `prompts/README.md` § Prompt Maintenance Workflow.

---

## Appendix A — Changelog

See `prompts/README.md` § Current Prompts table for version history.

---

## Appendix B — Lessons Applied (#151–#164)

See `prompts/README.md` § Shared Methodology (Lessons #151–#164).
