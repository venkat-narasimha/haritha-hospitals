## Employee Lifecycle Management with ERPNext HRMS — Deck Prompt (v2)

> **Status:** Active spec · **Version:** 2.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
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

Produce a **16-slide** self-contained HTML presentation explaining employee lifecycle management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

**Structural choices (v2.0):**

- Lifecycle follows a directional flow: entry (Onboarding) → growth (Promotion + Transfer) → exit (Separation), with Skill Map as a supporting reference.
- Slide 12 = inline SVG onboarding checklist visualization (5-7 task boxes, color-coded by status — Day 1 / Day 7 / Day 14 template).
- "Why choose" framing absorbed into conclusion slide (matches attendance v2.1 + org-mgmt v2.0 pattern).
- Schema full spec at slide 15 immediately before the closing slide.

## 4. Time Budget

- **Total: 40 minutes** (32 min content + 8 min Q&A).
- Per-slide timings sum to ~32 min — speaker can compress/expand as needed.
- See §8 for per-slide timings.

## 5. Output Specs

- **Format:** single `.html` file, fully self-contained (inline CSS, no external assets, no JavaScript libraries).
- **Slides:** exactly **16**, each `<section class="slide" id="slide-N">`.
- **Counter:** every slide shows `N / 16` (not 15, not 17 — must match exactly).
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
| `--primary` | `#1e40af` | Deep blue (titles, separation/exit layer, master anchor) |
| `--secondary` | `#64748b` | Slate (speaker notes, supporting reference layer) |
| `--accent` | `#0ea5e9` | Sky (entry/growth layer) |
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

## 7. Slide Template (apply uniformly to all 16 slides)

Every slide MUST include:

1. `<div class="slide-number">N / 16</div>`
2. `<h2 class="slide-title">…</h2>`
3. `<div class="body">… main content (≤100 words), one focal visual …</div>`
4. `<aside class="speaker-notes">…</aside>` — hidden by default, toggle with `S` key.
5. **Transition note** (1 sentence) — included inside speaker notes.

## 8. Slide-by-Slide Specs (16 slides)

### Intro (slides 1–3)

**Slide 1 — Employee Lifecycle Management with ERPNext HRMS** (30s) — Title slide
- Subtitle: "Structured hire-to-retire workflows for hospital operations"
- Metadata block (bottom-right): Version 2.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Transition: "Let's start with what employee lifecycle means in ERPNext HRMS."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "HRMS + Lifecycle Stack" / "Onboarding & Joining" / "Growth & Transitions" / "Exit & Final Settlement".
- Numbers: 01 / 02 / 03 / 04.
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Transition: "Now let's look at the core entities that drive lifecycle transitions."

### Early Schema Preview (slide 4 — clean preview, no labels)

**Slide 4 — Schema: Lifecycle Entities** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13 § Schema Flowchart § Slide 4 variant).
- Above: `<strong>Architecture:</strong> How employee lifecycle entities relate across stages.`
- Below: "The relational model connects entry, growth, and exit transactions to the Employee master, with Skill Map as a supporting reference."
- Speaker notes: "Employee sits at the center. Lifecycle documents (Onboarding, Promotion, Transfer, Separation) form a flow around Employee. Entry on the left (accent), Growth across the top (accent), Exit at the bottom (primary). Skill Map is a supporting reference (muted). Brief mention only. Recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the entities — why lifecycle management matters."

### Employee Lifecycle Operations (slides 5–12)

**Slide 5 — Why lifecycle management matters** (2 min)
- 3 bullets: manual checklists get lost / structured handovers reduce errors / compliance at join + exit is mandatory / growth tracking requires documented state changes.
- Visual: 3-stage timeline (green Joining / yellow Growth / red Separation) with hospital-shape icons.
- Transition: "Let's start with the entry point: Employee Onboarding."

**Slide 6 — Employee Onboarding (entry path)** (2 min)
- Lead paragraph: "Employee Onboarding is a structured checklist that brings a new hire on board. It assigns tasks to specific users with due dates; completion triggers automatic Employee creation when paired with onboarding programs."
- 3 bullets: task lists per role (doctor / nurse / technician / admin) / due dates + assignees / completion audit trail.
- Visual: lifecycle timeline (Pre-joining → Day 1 → Day 14 → Day 30) with task density bar.
- Transition: "Tasks need structure — Onboarding Tasks & Templates."

**Slide 7 — Onboarding Tasks & Templates** (2 min)
- Lead paragraph: "An Onboarding Template is a reusable bundle of tasks (e.g., 'Issue ID badge', 'Complete HIPAA training', 'Orient to ward 3') that HR can attach to a new Onboarding record."
- 3 bullets: per-role templates / task dependencies / progress tracking.
- Visual: template card mockup with task list (5-7 tasks with status badges).
- Transition: "Once onboarded, growth happens — Employee Promotion."

**Slide 8 — Employee Promotion (role/grade/date change)** (2 min)
- Lead paragraph: "Employee Promotion is a formal record of a role or grade change. It updates the Employee's designation + grade + effective date, often triggering a Salary Structure Assignment update."
- 3 bullets: promotion_date / new_designation + new_grade / approval workflow.
- Visual: promotion form mockup (Employee A: Staff Nurse → Senior Nurse, Grade 2 → Grade 3, eff 2025-09-01).
- Transition: "Sometimes growth means horizontal move — Employee Transfer."

**Slide 9 — Employee Transfer (intra-company move)** (2 min)
- Lead paragraph: "Employee Transfer moves an Employee between Departments or Branches within the same Company. It updates the Employee's department + branch + effective date."
- 3 bullets: intra-company only (separate from Promotion) / new Department + Branch / approval workflow.
- Visual: transfer form mockup (Employee A: Cardiology → Emergency, Branch A → Branch B, eff 2025-10-15).
- Transition: "Eventually the employee leaves — Employee Separation."

**Slide 10 — Employee Separation (exit path)** (2 min)
- Lead paragraph: "Employee Separation is the exit process. Approval flips Employee.status to 'Left' and sets a mandatory Relieving Date. Triggers Leave Encashment calculation and final settlement processing."
- 3 bullets: status flip to Left / Relieving Date mandatory / Leave Encashment + final settlement hooks.
- Visual: separation form mockup (Employee A: Reason = Resignation, Status → Left, Relieving 2025-12-31).
- Transition: "Throughout all this, skills get tracked — Employee Skill Map."

**Slide 11 — Employee Skill Map (skill tracking)** (2 min)
- Lead paragraph: "Employee Skill Map lets HR record skills per employee with proficiency levels. Useful for capability planning, training gap analysis, and roster assignment by skill."
- 3 bullets: skill name + proficiency (1-5) / multiple skills per employee / search by skill.
- Visual: skill matrix mockup (rows = employees, columns = skills, cells = proficiency dots).
- Transition: "Here's the visual onboarding workflow your HR team reads."

**Slide 12 — Onboarding Workflow (SVG checklist)** (2 min)
- Lead paragraph: "The Onboarding Workflow is a step-by-step task checklist HR uses to track new-hire progress. Tasks are color-coded by status (pending / in-progress / complete)."
- Inline SVG checklist visualization: 6 task boxes arranged vertically, each with status badge (✓ complete, ⟳ in-progress, ○ pending).
  - Task 1: Issue ID badge · **Complete** ✓
  - Task 2: Submit joining documents · **Complete** ✓
  - Task 3: Complete HIPAA training · **In Progress** ⟳
  - Task 4: Orient to ward 3 · **Pending** ○
  - Task 5: Probation review (Day 30) · **Pending** ○
  - Task 6: Confirm payroll activation · **Pending** ○
- Visual: `<div class="checklist">` with 6 task rows.
- Transition: "What about the exit side? Separation workflow + final settlement."

### Custom App + Schema + Conclusion (slides 13–16)

**Slide 13 — Separation Workflow & Final Settlement** (2 min)
- Lead paragraph: "Separation ties into Leave Encashment (convert unused leave to cash at exit) and final settlement (unused salary advance, gratuity, exit interview)."
- 3 bullets: Leave Encashment triggered / final settlement workflow / exit interview tracking.
- Visual: separation flow diagram (Submit → HR Review → Clearance → Status → Left).
- Transition: "What does the data give us — Reports & Analytics."

**Slide 14 — Extending ERPNext with Custom Apps** (2 min)
- 3 bullets: layer cleanly above core / add custom fields + DocTypes + workflows / deploy via Git.
- Visual: 3-layer stack (Specialized App Layer on top, HRMS Core, ERPNext & Frappe base) — accent/primary/secondary.
- Transition: "Here's the full schema with relationship labels and field hints."

**Slide 15 — Schema: Lifecycle Entities (full spec)** (3 min) — full spec, ENHANCED over slide 4 (see §13 § Schema Flowchart § Slide 15 variant)
- Above: `<strong>Architecture:</strong> How lifecycle entities relate across stages — with relationship labels, field hints, and a legend for color and connector meanings.`
- Below: "Onboarding enters, Promotion + Transfer grow, Separation exits. Employee Skill Map is a supporting reference. All four lifecycle documents update the central Employee master."
- Speaker notes: "Walk the audience through the directional flow. Read the labels: 'starts' (Onboarding → Employee), 'updates' (Promotion → Employee), 'moves' (Transfer → Employee), 'ends' (Separation → Employee), 'maps to' (Skill Map → Employee). The dashed groups show Entry / Growth / Exit phases. Skill Map is outside any grouping as a supporting reference."
- Transition: "Let's wrap up."

**Slide 16 — Conclusion + Why choose + Next Steps** (2 min)
- "Key Takeaways" h3 + numbered list (3 items).
  - Lifecycle covers hire-to-retire: Onboarding, Promotion, Transfer, Separation.
  - Each lifecycle doc updates the central Employee master.
  - Skill Map + onboarding templates + custom apps extend without core changes.
- "Why choose ERPNext + Haritha" h4 (absorbed from standalone slide):
  - 3 bullets (concise): Open source + code ownership / Lifecycle workflow templates reusable across clients / Active community.
- "Next Steps" h4 + 3 bullets (demo sandbox `demo.example.com` / pilot 4–8 weeks / architecture review).
- Transition: "Thank you and welcome to the Q&A."

## 9. Slide Template HTML

```html
<section class="slide" id="slide-N">
  <div class="slide-number">N / 16</div>
  <h2 class="slide-title">[Slide Title]</h2>
  <div class="body">
    [Main content here, max 100 words, with one focal visual]
  </div>
  <aside class="speaker-notes">
    [What the presenter says — 2–3 sentences. Hidden by default; press 'S' to toggle.]
    <br><br>
    Transition: [1 sentence]
  </aside>
</html>
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

### 11.1 Slide 6 (Onboarding timeline) — GOLD STANDARD

CSS excerpt for the visual lifecycle timeline with task density bar:

```css
.onboarding-timeline { display: flex; gap: var(--space-16); margin-top: var(--space-32); align-items: stretch; }
.timeline-phase { flex: 1; padding: var(--space-24) var(--space-16); border-radius: 8px; text-align: center; background: var(--bg-even); border: 1px solid #e2e8f0; }
.timeline-phase .phase-name { font-size: 18px; font-weight: 600; color: var(--text); margin-bottom: var(--space-8); }
.timeline-phase .phase-density { display: flex; gap: 4px; justify-content: center; margin-top: var(--space-8); }
.timeline-phase .density-bar { width: 6px; height: 14px; border-radius: 1px; background: var(--accent); }
.timeline-phase .density-bar.empty { background: var(--bg-odd); }
```

### 11.2 Slide 12 (Onboarding Workflow checklist) — GOLD STANDARD

CSS excerpt for the 6-row checklist with status badges:

```css
.checklist { display: flex; flex-direction: column; gap: var(--space-8); margin-top: var(--space-24); max-width: 720px; }
.checklist-row { display: flex; align-items: center; gap: var(--space-16); padding: var(--space-12) var(--space-16); border: 1px solid #e2e8f0; border-radius: 6px; background: var(--bg-odd); }
.checklist-row.complete { background: #f0fdf4; border-color: #86efac; }
.checklist-row.in-progress { background: #fefce8; border-color: #fde047; }
.checklist-row.pending { background: var(--bg-odd); border-color: #e2e8f0; }
.task-name { flex: 1; font-size: 16px; color: var(--text); }
.task-status { font-size: 13px; font-weight: 600; padding: 4px 10px; border-radius: 12px; }
.task-status.complete { background: #16a34a; color: white; }
.task-status.in-progress { background: #eab308; color: white; }
.task-status.pending { background: var(--muted); color: white; }
```

## 12. Image / Diagram Placeholder (Slides 6, 8, 9, 10)

Slides 6, 8, 9, 10 may use inline form/timeline mockups (pure CSS). No external images.

## 13. Schema Flowchart (Slides 4 + 15)

Both slides 4 and 15 contain an inline SVG (740×320 viewBox). They share the same entity set + groupings but differ in annotation density.

### 13.1 Slide 4 variant — clean preview

- **6 entity boxes** (rect+text):
  - **Employee Onboarding** — mid-left (accent `#0ea5e9`, entry layer)
  - **Employee Promotion** — top-center (accent, growth layer)
  - **Employee Transfer** — top-right (accent, growth layer)
  - **Employee Separation** — bottom-center (primary `#1e40af`, exit layer)
  - **Employee Skill Map** — bottom-right (muted `#94a3b8`, supporting reference)
  - **Employee** — center (primary, slightly larger to indicate master anchor — 140×60 vs 120×40)
- **3 dashed grouping rectangles** (`stroke-dasharray="4,4"`, stroke="secondary", fill="none"):
  - **Entry** — wraps Employee Onboarding (left).
  - **Growth** — wraps Employee Promotion + Employee Transfer (top).
  - **Exit** — wraps Employee Separation (bottom).
- Skill Map is **outside** any grouping (supporting reference, not a stage).
- NO connector labels, NO field hints, NO legend box.
- Connector paths in slate (`#94a3b8`); all from lifecycle docs toward Employee (convergent flow).

### 13.2 Slide 15 variant — full spec

Same as Slide 4 PLUS:

- **Connector labels** (1–2 words each, font-size 11, fill="secondary"):
  - Employee Onboarding → Employee: `"starts"`
  - Employee Promotion → Employee: `"updates"`
  - Employee Transfer → Employee: `"moves"`
  - Employee Separation → Employee: `"ends"`
  - Employee Skill Map → Employee: `"maps to"` (dashed — supporting reference)
- **Field hints** below each entity name in smaller text (font-size 9, fill="muted"):
  - Employee Onboarding: `[employee, date_of_joining, status]`
  - Employee Promotion: `[employee, promotion_date, new_designation, new_grade]`
  - Employee Transfer: `[employee, transfer_date, new_department, new_branch]`
  - Employee Separation: `[employee, separation_date, reason, status]`
  - Employee Skill Map: `[employee, skill, proficiency]`
  - Employee: `[name, status, branch]`
- **Legend box** (120×80 rect, white fill, slate border, bottom-left of canvas, ~translate(15,180)):
  - Color swatches: accent = `Entry / Growth`; primary = `Exit / Master`; muted = `Supporting reference`.
  - Connector symbols: solid line = `lifecycle event`; dashed line = `supporting reference`.

### 13.3 SVG technical specs

- viewBox: `0 0 740 320`, width="740", height="320".
- Font family: `var(--font-main)` for entity names, `var(--font-mono)` for field hints.
- Entity box dimensions: 120×40 (rect+text); Employee is 140×60 (slightly larger master anchor).
- Dashed grouping rectangle stroke-width: 1.5.
- Layout coordinates (approx):
  - Employee: rect at `x=305 y=130 w=140 h=60`
  - Employee Onboarding: rect at `x=40 y=210 w=130 h=45`
  - Employee Promotion: rect at `x=305 y=30 w=130 h=45`
  - Employee Transfer: rect at `x=560 y=30 w=130 h=45`
  - Employee Separation: rect at `x=305 y=240 w=130 h=45`
  - Employee Skill Map: rect at `x=560 y=240 w=130 h=45`
  - Entry dashed group: `x=10 y=190 w=200 h=80`
  - Growth dashed group: `x=280 y=10 w=420 h=80`
  - Exit dashed group: `x=280 y=225 w=180 h=80`
- Reference the existing shift-mgmt v2 SVG for visual style consistency.

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened.
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **Onboarding image placeholder (v1 slide 12)** — replaced by inline SVG checklist visualization (§11.2 gold standard).
- **"Why choose ERPNext + Haritha" as standalone slide** — absorbed into Conclusion slide 16 (matches attendance v2.1 + org-mgmt v2.0 pattern).
- **Vendor-pitch framing** — kept to a 3-bullet sub-section in the closing slide.

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 2.0 · Date 2026-09-14).
- **No vendor-specific data** — no employee counts, no real customer names, no company-specific metrics.
- **Use generic illustrative examples** ("Employee A", "Cardiology → Emergency", "Grade 2 → Grade 3").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType", "Skill Map", "Onboarding Template").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content).

## 15. Quality Bar (10 checks — verify before declaring done)

1. Exactly **16** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 = Schema preview (6 entities + 3 dashed groupings + Skill Map outside groups — NO connector labels, NO legend, NO field hints).
4. Slide 15 = Schema full spec (6 entities + 5 labeled connectors + legend + field hints).
5. Per-slide timings sum to ~32 minutes.
6. Both SVGs render correctly (no broken tags, no overlap).
7. Print stylesheet works.
8. No filler phrases anywhere.
9. Slide 12 = Onboarding Workflow SVG checklist (6 tasks with status badges: ✓ complete / ⟳ in-progress / ○ pending) — NOT image placeholder, NOT plain table.
10. Slide 4 connector labels NOT present; Slide 15 connector labels present and read in order: "starts", "updates", "moves", "ends", "maps to".

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 16`.
4. **Match this prompt's slide-by-slide spec exactly.** Any drift between spec and generated HTML is a defect.
5. Only declare "done" when all 10 checks pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/lifecycle-management-presentation.html`

## 18. Prompt Maintenance Workflow

See `prompts/README.md` § Prompt Maintenance Workflow.

---

## Appendix A — Changelog

See `prompts/README.md` § Current Prompts table for version history.

---

## Appendix B — Lessons Applied (#151–#164)

See `prompts/README.md` § Shared Methodology (Lessons #151–#164).
