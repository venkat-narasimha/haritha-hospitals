## Employee Lifecycle Management with ERPNext HRMS — Deck Prompt (v1)

> **Status:** Canonical spec · **Version:** 1.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
> **Audience:** Anyone generating or auditing this presentation deck (LLM agent, technical writer, reviewer).
> **Output:** `docs/handbook/03-client/lifecycle-management-presentation.html` (single self-contained HTML).

---

## 1. Role

You are a **technical writer + front-end developer** producing a single self-contained HTML presentation that explains **employee lifecycle management in ERPNext HRMS** to a general audience. You follow CMM Level 5 documentation standards in your process (not in the deck content).

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

Produce an **18-slide** self-contained HTML presentation explaining employee lifecycle management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

**Structural pattern (matches shift-mgmt v2):** the Schema: Lifecycle Entities slide appears **twice** — early (slide 4) and at its original position (slide 16). The early copy previews the architecture so the audience has a mental model before they see the entities in depth later.

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
| `--primary` | `#1e40af` | Deep blue (titles, onboarding layer) |
| `--secondary` | `#64748b` | Slate (speaker notes, exit layer) |
| `--accent` | `#0ea5e9` | Sky (bullets, growth layer) |
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

**Slide 1 — Employee Lifecycle Management with ERPNext HRMS** (30s) — Title slide
- Subtitle: "A practical guide to onboarding, growth, transfers, separation & skill tracking"
- Metadata block (bottom-right): Version 1.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "HRMS + Lifecycle Stack" / "Onboarding & Joining" / "Growth & Transitions" / "Exit & Final Settlement".
- Numbers: 01 / 02 / 03 / 04.
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module with Lifecycle / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Transition: "Now let's look at the data model — entities and their relationships."

### Early Schema Preview (slide 4 — DUPLICATE of slide 16)

**Slide 4 — Schema: Lifecycle Entities** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13).
- Above: `<strong>Architecture:</strong> How employee lifecycle entities relate across layers.`
- Below: "The relational model connects hiring milestones, in-role transitions, and exit events back to the central Employee record."
- Speaker notes: "Employee sits at the center. … Brief mention only. Recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the entities — why lifecycle management matters."

### Lifecycle Management Operations (slides 5–14)

**Slide 5 — Why lifecycle management matters** (2 min)
- 4 bullets: manual checklists lost in handover / structured handovers reduce errors / compliance at join + exit mandatory / growth tracking requires documented state changes.
- Visual: 4-step horizontal arc — Join → Grow → Move → Leave, each in its own color.
- Transition: "Let's start with the entry point: Employee Onboarding."

**Slide 6 — Employee Onboarding** (2 min)
- Lead paragraph: "An Employee Onboarding is a structured checklist of tasks that brings a new hire on board. It tracks every step from offer-accept to first productive day."
- 3 task cards: Documentation (ID + tax + banking), System Access (email + payroll setup), Orientation (policy briefing + role training).
- Transition: "Those tasks come from reusable templates."

**Slide 7 — Onboarding Tasks & Templates** (2 min)
- 4 bullets: per-role templates (doctor, nurse, technician, admin) / task assignments with owners / due dates + dependencies / track completion in one view.
- Visual: 2-column layout — left: 4 role templates; right: single template expanded to a 14-day checklist.
- Transition: "When an employee grows — that's Employee Promotion."

**Slide 8 — Employee Promotion** (2 min)
- Lead paragraph: "An Employee Promotion records a role, grade, or compensation change for an existing employee. "
- 3 bullets: revision of designation + grade / effective date + approver chain / audit trail of every role change.
- Visual: side-by-side before/after cards — "Staff Nurse → Senior Nurse", "Grade 3 → Grade 4".
- Transition: "Sometimes growth means moving — Employee Transfer."

**Slide 9 — Employee Transfer** (2 min)
- Lead paragraph: "An Employee Transfer moves an employee between departments or branches within the same company. "
- 3 bullets: department + branch re-assignment / transfer date + relieving letter / keep Employee record intact (no new hire).
- Visual: 3 horizontal nodes — Home Dept → New Dept, with employee badge bridging.
- Transition: "When it's time to leave — Employee Separation."

**Slide 10 — Employee Separation** (2 min)
- Lead paragraph: "An Employee Separation is an exit process that flips Employee.status to 'Left' and records a Relieving Date."
- 3 bullets: resignation / retirement / termination entries / status flips to "Left" on Relieving Date / final clearance checklist.
- Visual: status toggle visual — "Active" (primary) → "Left" (secondary).
- Transition: "Across all roles — track capability with Employee Skill Map."

**Slide 11 — Employee Skill Map** (2 min)
- Lead paragraph: "An Employee Skill Map captures every skill an employee has, rated by proficiency, to support capability planning."
- 3 bullets: skill + proficiency rating / used for project assignment + training plans / aggregated for workforce reports.
- Visual: matrix mockup — Skill row × Employee column with proficiency dots (1–5).
- Transition: "What does the workflow look like? Onboarding."

**Slide 12 — Onboarding Workflow** (2 min) — IMAGE PLACEHOLDER (see §12)
- Lead paragraph + 2 bullets (template-driven tasks / completion % per hire).
- Visual: `.image-placeholder` div with "Insert onboarding checklist screenshot here" text.
- Transition: "Now the other end — Separation Workflow + Final Settlement."

**Slide 13 — Separation Workflow & Final Settlement** (2 min)
- 3 bullets: Exit interview + clearance / Leave Encashment calculated from Leave Allocation / final pay run on Relieving Date.
- Visual: horizontal flow (1. Initiate → 2. Clearance → 3. Leave Encashment → 4. Final Pay).
- Transition: "All this data feeds into Reports."

**Slide 14 — Reports & Analytics** (2 min)
- 4 stat cards: Onboarding in Progress 7, Promotions this Quarter 12, Transfers YTD 9, Attrition Rate 8.4%.
- Visual: `<svg>` polyline chart inside `.chart-placeholder`, Headcount Trend marker.
- Transition: "What if ERPNext out-of-box doesn't fit? Custom apps."

### Custom App + Schema (slides 15–16)

**Slide 15 — Extending ERPNext with Custom Apps** (2 min)
- 3 bullets: layer cleanly above core / add custom fields + DocTypes + workflows / deploy via Git + `bench`.
- Visual: 3-layer stack (Specialized App Layer on top, HRMS Core, ERPNext & Frappe base) — accent/primary/secondary.
- Transition: "Here's how the entities relate."

**Slide 16 — Schema: Lifecycle Entities** (3 min) — full spec, identical SVG to slide 4
- Above: `<strong>Architecture:</strong> How employee lifecycle entities relate across layers.`
- Below: same caption as slide 4.
- Speaker notes: "Employee sits at the center. … Transition: Why choose ERPNext + Haritha for your deployment."

### Why Choose + Conclusion (slides 17–18)

**Slide 17 — Why choose ERPNext + Haritha** (2 min)
- 5 bullets: Open source / Complete code ownership / Clinical operational readiness / Active community / Workflow flexibility.
- Visual: `<table class="comp-table">` (4 columns: Parameter / ERPNext + Haritha / SAP / Oracle / Workday) with `.comp-highlight` column.
- Transition: "Let's wrap up."

**Slide 18 — Conclusion + Next Steps** (2 min)
- "Key Takeaways" h3 + numbered list (3 items).
- "Next Steps" h4 + 3 bullets (demo sandbox `demo.example.com` / pilot 4–8 weeks / architecture review).
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

## 11. Concrete Example — Slide 6 (Employee Onboarding) — GOLD STANDARD

The body markup and CSS for Slide 6 must match the canonical v1.html. Every slide has a similar layout pattern (`.body` containing bullet list, paragraph, and one focal visual). Slide 6 specifically uses `.task-cards` with three `.task-card` blocks (a variant of the shift-card pattern from shift-mgmt v2).

CSS excerpt:

```css
.task-cards { display: flex; gap: var(--space-24); justify-content: center; margin-top: var(--space-32); }
.task-card  { flex: 1; max-width: 220px; padding: var(--space-24) var(--space-16) var(--space-16); border-radius: 8px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border: 1px solid #e2e8f0; position: relative; }
.task-color-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 8px 8px 0 0; }
.task-name { font-size: 20px; font-weight: 600; color: var(--text); margin-top: var(--space-12, 12px); }
.task-meta { font-size: 16px; color: var(--primary); margin-top: var(--space-8); font-family: var(--font-mono); }
.task-hours { font-size: 13px; color: var(--secondary); margin-top: 4px; }
```

## 12. Onboarding Image Placeholder (Slide 12)

Slide 12 MUST contain exactly this placeholder block:

```html
<div class="image-placeholder" style="border: 2px dashed #94a3b8; padding: 48px 32px; text-align: center; color: #64748b; margin-top: 32px;">
  [Insert onboarding checklist screenshot here]
  <br><small>Onboarding view — task checklist for a new hire</small>
</div>
```

## 13. Schema Flowchart (Slides 4 and 16)

Both slides 4 and 16 contain the **same** inline SVG (740×320 viewBox). The SVG must include:

- 6 entity boxes (rect+text): Employee (center, primary), Employee Onboarding (entry path, accent), Employee Promotion (mid-path, accent), Employee Transfer (branch path, accent), Employee Separation (exit path, secondary), Employee Skill Map (supporting, slate).
- Connector paths in slate (`#94a3b8`); use a dashed line for indirect relations (Employee Skill Map ↔ Employee).
- Reference shift-mgmt v2 SVG for visual style — same stroke widths, corner radii, and label typography.

**Positioning (rough, 740×320 viewBox):** Employee at center (370, 150). Employee Onboarding top-left (130, 60) as entry. Employee Promotion top-right (610, 60) as mid-path. Employee Transfer right (610, 150) as branch. Employee Separation bottom-right (610, 240) as exit. Employee Skill Map bottom-center (370, 260) as supporting entity below Employee.

**Relations:** Employee Onboarding → Employee (hire), Employee Promotion → Employee (growth), Employee Transfer → Employee (move), Employee Separation → Employee (exit), Employee Skill Map ⇢ Employee (dashed — supports).

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim content is "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened. The deck does NOT talk about "Phase 6 docs / Tier 6 compliance".
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **Stale Hand-off / Gossip v1 content** — do not introduce casual or anecdotal deck copy.

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 1.0 · Date 2026-09-14).
- **No Haritha-specific data** — no employee counts, no company-specific metrics, no real customer names.
- **Use generic illustrative examples** ("14-day checklist for new nurse", "Staff Nurse → Senior Nurse + grade change").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType: a database table in ERPNext", "Employee Onboarding: a structured checklist of tasks to bring a new hire on board", "Employee Separation: an exit process that flips Employee.status to 'Left'").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content) except where already established.

## 15. Quality Bar (10 checks — verify before declaring done)

1. All **18** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 == Schema (duplicate of slide 16, byte-identical SVG).
4. Slide 16 == Schema (original).
5. Per-slide timing sums to ~32 minutes.
6. SVG renders correctly (no broken tags) — 6 entities + 4 relations + 1 dashed relation.
7. Print stylesheet works.
8. No filler phrases.
9. Onboarding image placeholder present (slide 12).
10. Schema flowchart present with all 6 entities + relations (slides 4 and 16).

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 18`.
4. Confirm the SVG contains Employee (center) and the 5 lifecycle entities with the right relations.
5. Confirm jargon definitions are present on first use in slide bodies.
6. Only declare "done" when all 10 checks + content constraints pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/lifecycle-management-presentation.html`

## 18. Regeneration Workflow

`prompts/build_deck.py` (or its lifecycle equivalent) is the single regenerator:

1. Validates that v1.md describes 18 slides with Schema at #4 and #16.
2. Base64-decodes the embedded canonical snapshot.
3. Writes the bytes verbatim to the output path.

Re-running the generator is idempotent and produces a byte-for-byte match with the committed HTML. To update the deck:

1. Edit `docs/handbook/03-client/lifecycle-management-presentation.html` manually (Venkat-approved copy).
2. Re-embed its base64 in the generator script (one-line shell helper: `base64 -w0 path/to/lifecycle.html`).
3. Update the slide-by-slide spec in this prompt to match the new content.
4. Commit all three together.

---

## Appendix A — Changelog

- **v1.0** (2026-09-14) — Initial release based on shift-mgmt v2 pattern.
  - Added Schema duplicate at slide 4 (early preview).
  - Adapted Slide 2 agenda to lifecycle (HRMS + Lifecycle Stack / Onboarding & Joining / Growth & Transitions / Exit & Final Settlement).
  - Five DocType slides (Employee Onboarding, Promotion, Transfer, Separation, Skill Map) inserted at slides 6–11.
  - Image placeholder moved to slide 12 (Onboarding Workflow).
  - Schema flowchart uses 6 entities (Employee + 5 lifecycle DocTypes) replacing 9-entity shift-mgmt diagram.
  - Counter `N / 18` matches shift-mgmt v2.
  - Slide 1 metadata: Version 1.0, Date 2026-09-14, Audience General.
  - Concrete gold standard: Slide 6 (Employee Onboarding).

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

## Appendix C — Reference Only — pberpprod Deployment Note

> **Reference only — slides must use GENERIC examples per §14.**

A prior discovery report (now purged from the repo) noted that the `tabOnboarding` table was reported missing in the `pberpprod` environment. Table availability for lifecycle DocTypes (Onboarding, Promotion, Transfer, Separation, Skill Map) varies by ERPNext / HR install:

- Fresh installs of `hrms` app ship with all five lifecycle DocTypes and underlying tables.
- Custom-modified or partially-migrated installs may be missing one or more tables.
- Before any demo, run `SHOW TABLES LIKE '%onboard%';` (and equivalents for other lifecycle tables) against the target MariaDB / PostgreSQL instance.
- If a table is missing, run `bench migrate` after ensuring the app is on the matching version, or apply the missing DocType via `bench console` with `frappe.reload_doc("hr", "doctype", "employee_onboarding")`.

**This note is reference-only.** The slide deck itself does NOT mention this deployment-specific issue — slide content uses generic examples per §14 ("14-day checklist for new nurse", "Staff Nurse → Senior Nurse"). Keep the demo environment verification step in the speaker's pre-flight checklist, not on the slides.
