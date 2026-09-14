## Frappe HR Overview — Deck Prompt (v1)

> **Status:** Canonical spec · **Version:** 1.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
> **Audience:** Anyone generating or auditing this presentation deck (LLM agent, technical writer, reviewer).
> **Output:** `docs/handbook/03-client/frappe-hr-overview-presentation.html` (single self-contained HTML).
> **Module:** Frappe HR Overview — synthesis deck covering all 5 mandatory modules (Organization Management, Attendance Management, Shift Management, Leave Management, Employee Lifecycle Management) at high level.
> **Reference:** https://docs.frappe.io/hr/introduction
> **Companion decks:** see Appendix C.

---

## 1. Role

You are a **technical writer + front-end developer** producing a single self-contained HTML presentation that introduces the full **Frappe HR** landscape and routes the audience to the right deep-dive module deck. You follow CMM Level 5 documentation standards in your process (not in the deck content).

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

Produce an **18-slide** self-contained HTML presentation introducing **Frappe HR as a complete HR + Payroll application for hospital operations**. Acts as the entry point and module navigator — routes the audience to five companion deep-dive decks. Educational, general audience, light theme, professional + minimal + clean.

**Structural difference vs v2 (shift-management):** the Schema: Frappe HR Ecosystem slide appears **twice** — early (slide 4) and at its original position (slide 16). The early copy previews the architecture so the audience has a mental model before they see the modules in depth later.

**Synthesis role:** this deck does NOT replace the per-module deep-dives. It introduces all 5 mandatory modules at a high level and tells the audience which deck to watch for full detail.

## 4. Time Budget

- **Total: 40 minutes** (32 min content + 8 min Q&A).
- Per-slide timings sum to ~32 min — speaker can compress/expand as needed.
- See §8 for per-slide timings.

## 5. Output Specs

- **Format:** single `.html` file, fully self-contained (inline CSS, no external assets, no JavaScript libraries).
- **Slides:** exactly **18**, each `<section class="slide" id="slide-N">`.
- **Counter:** every slide shows `N / 18` (not 17, not 19 — must match exactly).
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
| `--primary` | `#1e40af` | Deep blue (titles, module-cluster layer) |
| `--secondary` | `#64748b` | Slate (speaker notes, reference layer) |
| `--accent` | `#0ea5e9` | Sky (bullets, Employee hub) |
| `--text` | `#0f172a` | Near-black (body text) |
| `--muted` | `#94a3b8` | Muted (slide numbers, borders) |
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

## 7. Slide Template (apply uniformly to all 18 slides)

Every slide MUST include:

1. `<div class="slide-number">N / 18</div>`
2. `<h2 class="slide-title">…</h2>`
3. `<div class="body">… main content (≤100 words), one focal visual …</div>`
4. `<aside class="speaker-notes">…</aside>` — hidden by default, toggle with `S` key.
5. **Transition note** (1 sentence) — included inside speaker notes.

## 8. Slide-by-Slide Specs (18 slides)

### Intro (slides 1–3)

**Slide 1 — Frappe HR Overview** (30s) — Title slide
- Subtitle: "A practical guide to the full HR + Payroll landscape — from hire to retire".
- Metadata block (bottom-right): Version 1.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Speaker notes: "Welcome the audience. This deck introduces Frappe HR as one complete application — five mandatory modules working together — and routes you to the right deep-dive for the detail."
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "Frappe HR Landscape" / "5 Mandatory Modules" / "How They Connect" / "Demo Roadmap".
- Numbers: 01 / 02 / 03 / 04.
- Speaker notes: "Walk through the four zones. Set expectations: we cover the 5 mandatory modules at high level, then route you to a per-module deck for full detail."
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Speaker notes: "Position HRMS as one module inside the larger ERP. All five modules we cover today live inside HRMS — not in third-party add-ons."
- Transition: "Now let's look at the data model — entities and their relationships."

### Early Schema Preview (slide 4 — DUPLICATE of slide 16)

**Slide 4 — Schema: Frappe HR Ecosystem** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13).
- Above: `<strong>Architecture:</strong> How the 5 mandatory modules connect around the Employee hub.`
- Below: "The relational model ties Organization, Attendance, Shift, Leave, and Lifecycle together through one shared Employee record."
- Speaker notes: "Employee sits at the center as the universal connector. Five module clusters ring around it: Organization, Attendance, Shift, Leave, Lifecycle. Mention only — recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the modules — why Frappe HR matters for hospital operations."

### Why Frappe HR (slide 5)

**Slide 5 — Why Frappe HR for hospital operations** (2 min)
- 5 bullets: open-source with no license fees / hospital-adaptable workflows (24/7 shifts, clinical roles) / modular — adopt one module at a time / active community (5,000+ contributors) / end-to-end coverage from hire to retire.
- Visual: stacked-card icon row showing "Open Source → Modular → Community → End-to-End" with arrows.
- Speaker notes: "Frame the value: a single application that covers the full employee lifecycle, built on an open-source stack with no per-seat license fees. Hospitals adapt it for round-the-clock shifts and clinical roles."
- Transition: "Let's walk through each of the 5 mandatory modules."

### Module Walkthrough (slides 6–10) — high level, route to deep-dive decks

**Slide 6 — Organization Management** (2 min)
- Lead paragraph: "Organization Management defines the people master and the hierarchy around it — Company, Department, Designation, Branch, Employee Grade, Employment Type — all linking to a single Employee record."
- 3 entity cards: "Company" (top of hierarchy) / "Department" (functional grouping) / "Employee" (universal connector — 200+ fields across tabs).
- Visual: `.entity-cards` row of three `.entity-card` blocks; color-bar = primary.
- Speaker notes: "Organization is the foundation. Without clean master data — Company, Department, Designation — every downstream module reads garbage. For full detail, watch the Organization Management deep-dive deck."
- Transition: "Once people are defined, we track presence — Attendance."

**Slide 7 — Attendance Management** (2 min)
- Lead paragraph: "Attendance Management is the daily presence ledger. It supports multiple input methods — biometric, web check-in, mobile GPS — and correlates check-ins to shifts to produce a clean presence record."
- 3 bullets: multiple input methods (biometric, web, mobile) / correlator matches check-ins to shifts / daily + monthly register, late marks, overtime.
- Visual: horizontal flow (1. Check-in Source → 2. Correlator → 3. Attendance Register).
- Speaker notes: "Attendance is the source of truth for presence. The correlator decides whether a check-in counts as Present, Late, or Half-day — configurable per shift and grace policy. For full detail, watch the Attendance Management deep-dive deck."
- Transition: "Attendance needs context — Shift Management."

**Slide 8 — Shift Management** (2 min)
- Lead paragraph: "Shift Management defines when work happens. A Shift Type is a reusable template (Morning 06:00–14:00, Evening 14:00–22:00, Night 22:00–06:00) — and a Shift Schedule maps employees to those templates across a calendar."
- 3 bullets: Shift Type (reusable template) / Shift Schedule (planned calendar) / auto-attendance correlator (shift → check-in match).
- Visual: 3 shift cards (Morning / Evening / Night) with start–end times.
- Speaker notes: "Shifts are templates, not assignments. A Shift Schedule is the planned calendar; a Shift Assignment maps one employee to one slot. Auto-attendance reads the schedule and the correlator matches check-ins. For full detail, watch the Shift Management deep-dive deck."
- Transition: "Presence has a counterpart — absence."

**Slide 9 — Leave Management** (2 min)
- Lead paragraph: "Leave Management handles planned and unplanned absence. A Leave Type defines the policy (Casual Leave: 12 days/year, Sick Leave: 12 days/year); a Leave Allocation grants the balance; a Leave Application is the employee request; a Leave Approval is the workflow outcome."
- 3 bullets: Leave Type (policy template) / Leave Allocation (granted balance) / Leave Application + Approval workflow.
- Visual: horizontal flow (1. Employee → 2. Leave Application → 3. Manager Approval → 4. Ledger).
- Speaker notes: "Leave is the mirror of attendance. When a leave application is approved, the system posts 'On Leave' against the Attendance ledger so the correlator skips that day. For full detail, watch the Leave Management deep-dive deck."
- Transition: "And people move through stages — Lifecycle Management."

**Slide 10 — Employee Lifecycle Management** (2 min)
- Lead paragraph: "Employee Lifecycle Management covers every status change an employee goes through — onboarding, transfer, promotion, separation. Each lifecycle event is a separate workflow with checklists, approvals, and audit history."
- 3 bullets: Onboarding (offer letter → Day 1 readiness checklist, 14-day template) / Movement (transfer, promotion, role change) / Separation (resignation, retirement, exit clearance).
- Visual: timeline SVG (Onboarding → Active → Movement → Separation) with 4 stage nodes.
- Speaker notes: "Lifecycle is the chronology. Each event creates an audit record — who approved, when, what changed. Onboarding templates keep new-hire readiness consistent. For full detail, watch the Employee Lifecycle deep-dive deck."
- Transition: "Now — how do all five fit together?"

### How Modules Connect (slide 11)

**Slide 11 — How the modules connect** (2 min)
- Lead paragraph: "Org defines the Employee record → Attendance + Shift track daily presence → Leave handles absence → Lifecycle covers every status change. The same Employee record is the join key across every module."
- 3 bullets: one Employee, one record, every module reads it / Shift defines expected presence, Attendance confirms it / Lifecycle writes stage changes, every module reacts.
- Visual: linear flow diagram (Org → Employee → {Attendance, Shift, Leave} → Lifecycle).
- Speaker notes: "Stress the join key: the Employee record. Whatever happens in Shift (planned) and Attendance (actual) and Leave (absence) and Lifecycle (status) all reference the same Employee. A quick scenario: a nurse on Maternity Leave — Lifecycle flags the leave period, Attendance marks On Leave, Shift skips roster assignment, Org keeps the Department link intact."
- Transition: "Which deck covers what — let's navigate."

### Module Navigator (slide 12)

**Slide 12 — Module Navigator** (2 min) — IMAGE PLACEHOLDER (see §12)
- Lead paragraph: "Each mandatory module has its own deep-dive deck. This overview introduces each at high level; the per-module decks cover the entities, workflows, and reports in full detail."
- 2 bullets: deep-dive decks run ~40 minutes each / this overview plus three deep-dives covers the mandatory scope.
- Visual: `.image-placeholder` div with "Insert module navigator roadmap diagram here" text (exact block in §12).
- Speaker notes: "Walk the audience through the five companion decks. Recommend watching order: Org → Attendance → Shift → Leave → Lifecycle — the dependency order. The module navigator diagram visualizes this on screen."
- Transition: "What's intentionally NOT in this overview."

### Out of Scope (slide 13)

**Slide 13 — Out of Scope (deferred)** (2 min)
- 3 bullets: **Flexible Benefits** — cafeteria-style benefit plans (deferred — payroll-adjacent, separate deck planned) / **Payroll** — handled by the Payroll / Frappe Payroll team (separate scope) / **Full Statutory Compliance** — tax filings, labour-law filings — handled by compliance specialists.
- Visual: 3-card "Out of Scope" row (Flexible Benefits / Payroll / Statutory Compliance) with reason + owner tag.
- Speaker notes: "Be explicit about what this overview does NOT cover. Flexible Benefits and Payroll are on the roadmap but live outside the 5 mandatory modules. Statutory Compliance is its own specialist domain. Each will get a separate deck when its scope is finalized."
- Transition: "What we'll show in the live demo."

### Demo Roadmap (slide 14)

**Slide 14 — Demo Roadmap** (2 min)
- 3 bullets: **In this demo** — Organization Management + Attendance + Shift (full deep-dive) + Leave + Lifecycle (brief overview) / **Follow-up deep-dives** — per-module deck for each of the 5 mandatory modules / **Future demos** — Flexible Benefits (when ready), Payroll integration, Statutory Compliance.
- Visual: 3-row roadmap (Today / This Month / Future) with module chips.
- Speaker notes: "Set expectations for the live demo. Today covers all 5 modules but spends time on the high-touch ones (Org, Attendance, Shift). Leave and Lifecycle get a brief overview plus a pointer to their dedicated deep-dive deck."
- Transition: "What if ERPNext out-of-box doesn't fit? Custom apps."

### Custom App + Schema (slides 15–16)

**Slide 15 — Extending ERPNext with Custom Apps** (2 min)
- 3 bullets: layer cleanly above core / add custom fields + DocTypes + workflows / deploy via Git + `bench`.
- Visual: 3-layer stack (Specialized App Layer on top, HRMS Core, ERPNext & Frappe base) — accent/primary/secondary.
- Speaker notes: "Custom fields let you add a `Cost Center Code` to Department without forking. Custom DocTypes add whole new entities — e.g., `Clinical Role Matrix` — linked to Employee."
- Transition: "Here's how the modules relate."

**Slide 16 — Schema: Frappe HR Ecosystem** (3 min) — full spec, identical SVG to slide 4
- Above: `<strong>Architecture:</strong> How the 5 mandatory modules connect around the Employee hub.`
- Below: same caption as slide 4.
- Speaker notes: "Walk the audience through each connection. Employee is the universal connector — every module reads or writes through it. Org defines the record; Attendance + Shift track daily presence; Leave handles absence; Lifecycle covers stage changes. Arrows show data flow direction."
- Transition: "Why choose ERPNext + Haritha for your deployment."

### Why Choose + Conclusion (slides 17–18)

**Slide 17 — Why choose ERPNext + Haritha** (2 min)
- 5 bullets: Open source / Complete code ownership / Clinical operational readiness / Active community / Workflow flexibility.
- Visual: `<table class="comp-table">` (4 columns: Parameter / ERPNext + Haritha / SAP / Oracle / Workday) with `.comp-highlight` column.
- Speaker notes: "Highlight the cell-by-cell comparison. Stress code ownership — no vendor lock-in — and the active community as the long-term sustainability argument."
- Transition: "Let's wrap up."

**Slide 18 — Conclusion + Next Steps** (2 min)
- "Key Takeaways" h3 + numbered list (3 items).
- "Next Steps" h4 + 3 bullets (demo sandbox `demo.example.com` / pilot 4-8 weeks / architecture review).
- Speaker notes: "Recap the three takeaways: Frappe HR is one application, five mandatory modules cover hire-to-retire, the per-module decks give the depth. The next-step bullets give the audience a concrete path from this deck to a working deployment."
- Transition: "Thank you and welcome to the Q&A."

## 9. Slide Template HTML

```html
<section class="slide" id="slide-N">
  <div class="slide-number">N / 18</div>
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

## 11. Concrete Example — Slide 6 (Organization Management) — GOLD STANDARD

The body markup and CSS for Slide 6 must showcase the **Organization Management** module at high level and reuse the `.entity-cards` pattern from the canonical `org-management-presentation.html`. Every slide has a similar layout pattern (`.body` containing lead paragraph, three entity-card blocks, and a transition inside speaker notes). Slide 6 specifically uses `.entity-cards` with three `.entity-card` blocks representing Company, Department, and Employee.

CSS excerpt (mirrors the `.entity-cards` pattern from the org-management deep-dive deck):

```css
.entity-cards { display: flex; gap: var(--space-24); justify-content: center; margin-top: var(--space-32); }
.entity-card  { flex: 1; max-width: 220px; padding: var(--space-24) var(--space-16) var(--space-16); border-radius: 8px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border: 1px solid #e2e8f0; position: relative; }
.entity-color-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 8px 8px 0 0; }
.entity-name { font-size: 20px; font-weight: 600; color: var(--text); margin-top: var(--space-12, 12px); }
.entity-meta { font-size: 14px; color: var(--secondary); margin-top: var(--space-8); font-family: var(--font-mono); }
.entity-note { font-size: 13px; color: var(--secondary); margin-top: 4px; }
```

## 12. Module Navigator Image Placeholder (Slide 12)

Slide 12 MUST contain exactly this placeholder block:

```html
<div class="image-placeholder" style="border: 2px dashed #94a3b8; padding: 48px 32px; text-align: center; color: #64748b; margin-top: 32px;">
  [Insert module navigator roadmap diagram here]
  <br><small>Module navigator — which deck to watch for which module</small>
</div>
```

## 13. Schema Flowchart (Slides 4 and 16)

Both slides 4 and 16 contain the **same** inline SVG (740×320 viewBox). The SVG must include:

- **6 entity/group boxes** (rect+text): Employee (center, accent) — the universal connector — surrounded by 5 module-cluster boxes (Org Management / Attendance / Shift / Leave / Lifecycle, alternating primary/secondary).
- **Connector paths** in slate (`#94a3b8`) showing data-flow direction:
  - Employee → Attendance + Shift (presence data flows from the Employee record).
  - Leave → Attendance (Leave posts On Leave status into the Attendance ledger).
  - Lifecycle → Employee (Lifecycle writes status changes onto the Employee record).
  - Org Management → Employee (Org defines the Employee record).
- One dashed line for an indirect relation (e.g., Org Management → Attendance via Employee — Org structure flows through into attendance rollups).

**Positioning (rough):** Employee at center (370, 150). The five module clusters arranged around Employee in a ring at radius ~140 px.

**Modules in the ring (suggested ordering, clockwise from top):** Org Management (top), Attendance (top-right), Shift (bottom-right), Leave (bottom-left), Lifecycle (top-left).

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim content is "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened. The deck does NOT talk about "Phase 6 docs / Tier 6 compliance".
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **Haritha-specific data from any discarded draft** — do not reuse any company name, employee count, department list, branch, or shift pattern from internal drafts. All examples in the slides MUST be generic.

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 1.0 · Date 2026-09-14).
- **No Haritha-specific data** — no employee counts, no company-specific metrics, no real customer names.
- **Use generic illustrative examples** ("Casual Leave: 12 days/year", "Employee: 200+ fields across tabs", "Onboarding template: 14-day checklist").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType: a database table in ERPNext", "Module: a logical grouping of related doctypes and workflows", "Shift Type: a reusable template that defines when work happens").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content) except where already established.
- **Overview tone** — slides stay HIGH-LEVEL and route to the per-module deep-dive decks for detail. Do not duplicate module-specific detail in this deck.

## 15. Quality Bar (10 checks — verify before declaring done)

1. All **18** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 == Schema (duplicate of slide 16, byte-identical SVG).
4. Slide 16 == Schema (original).
5. Per-slide timing sums to ~32 minutes.
6. SVG renders correctly (no broken tags).
7. Print stylesheet works.
8. No filler phrases.
9. Module navigator image placeholder present (slide 12).
10. Schema flowchart present with all **6 entities/groups** + relations (slides 4 and 16).

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 18`.
4. **Match the canonical overview HTML byte-for-byte** — `prompts/build_deck.py` embeds the canonical snapshot and emits it directly. Any drift is a defect.
5. Only declare "done" when all 10 checks + byte-for-byte match pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/frappe-hr-overview-presentation.html`

## 18. Regeneration Workflow

`prompts/build_deck.py` is the single regenerator (same pattern as shift-mgmt v2):

1. Validates that the prompt describes 18 slides with Schema at #4 and #16.
2. Base64-decodes the embedded canonical snapshot.
3. Writes the bytes verbatim to the output path.

Re-running `python3 prompts/build_deck.py` is idempotent and produces a byte-for-byte match with the committed `frappe-hr-overview-presentation.html`. To update the deck:

1. Edit `docs/handbook/03-client/frappe-hr-overview-presentation.html` manually (Venkat-approved copy).
2. Re-embed its base64 in `prompts/build_deck.py` (one-line shell helper: `base64 -w0 path/to/frappe-hr-overview-presentation.html`).
3. Update the slide-by-slide spec in this prompt (`frappe-hr-overview-cmm-l5-presentation.md`) to match the new content.
4. Commit all three together.

---

## Appendix A — Changelog

- **v1.0** (2026-09-14) — Initial release — Frappe HR overview synthesis deck based on shift-mgmt v2 pattern.
  - Adapted all 18 sections from `shift-management-cmm-l5-presentation-v2.md`.
  - Synthesis role: introduces all 5 mandatory modules at high level, routes to per-module deep-dive decks.
  - Modules in scope: Organization Management, Attendance Management, Shift Management, Leave Management, Employee Lifecycle Management.
  - Modules out of scope: Flexible Benefits (deferred), Payroll (separate team).
  - Schema: 6 entity/group boxes — Employee (center) + 5 module clusters around (Org Mgmt / Attendance / Shift / Leave / Lifecycle).
  - Concrete gold standard: Slide 6 (Organization Management) with `.entity-cards` CSS pattern reused from the org-management deep-dive deck.
  - Module navigator image placeholder on slide 12.

---

## Appendix B — Lessons Applied (#151–#164)

- **#151** Quantitative process management — every spec has a measurable check (§15).
- **#152** Defect prevention — verify before declaring done (§16).
- **#153** Change management — version this prompt.
- **#154** Technology change management — design tokens frozen (§6).
- **#155** Peer review — generator output self-reviewed before "done".
- **#156** Process measurement — counter `N / 18` must match exactly.
- **#157** Process analysis — single root cause for duplicates (Schema preview).
- **#158** Process innovation — speaker notes pattern reusable across all 18 slides.
- **#159** Continuous improvement — lessons from v1 prompt are explicit drops in §14.
- **#160** Defect analysis — schema SVG character escaping (`&#39;` artifacts).
- **#161** Content freshness check — do not lie about dates; verify mtime vs claimed.
- **#162** Always do broad grep before claiming scope.
- **#163** "Up to date?" means BOTH structure AND metadata.
- **#164** Per-directory footers drift independently.

---

## Appendix C — Companion Module Decks

This overview deck is the entry point. Each mandatory module has its own deep-dive deck:

- **Organization Management:** `docs/handbook/03-client/org-management-presentation.html`
- **Attendance Management:** `docs/handbook/03-client/attendance-management-presentation.html`
- **Shift Management:** `docs/handbook/03-client/shift-management-presentation-v2.html` (canonical, frozen)
- **Leave Management:** `docs/handbook/03-client/leave-management-presentation.html`
- **Employee Lifecycle Management:** `docs/handbook/03-client/lifecycle-management-presentation.html`

Recommended viewing order: Org → Attendance → Shift → Leave → Lifecycle (dependency order).
