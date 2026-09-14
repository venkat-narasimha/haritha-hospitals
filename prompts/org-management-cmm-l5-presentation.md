## Organization Management in ERPNext HRMS — Deck Prompt (v1)

> **Status:** Canonical spec · **Version:** 1.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
> **Audience:** Anyone generating or auditing this presentation deck (LLM agent, technical writer, reviewer).
> **Output:** `docs/handbook/03-client/org-management-presentation.html` (single self-contained HTML).
> **Module:** Organization Management in ERPNext HRMS.
> **Reference:** https://docs.frappe.io/hr/employee

---

## 1. Role

You are a **technical writer + front-end developer** producing a single self-contained HTML presentation that explains **organization management in ERPNext HRMS** to a general audience. You follow CMM Level 5 documentation standards in your process (not in the deck content).

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

Produce an **18-slide** self-contained HTML presentation explaining organization management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

**Structural pattern (inherited from shift-mgmt v2):** the Schema: Organization Entities slide appears **twice** — early (slide 4) and at its original position (slide 16). The early copy previews the architecture so the audience has a mental model before they see the entities in depth later.

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
| `--primary` | `#1e40af` | Deep blue (titles, structural layer) |
| `--secondary` | `#64748b` | Slate (speaker notes, reference layer) |
| `--accent` | `#0ea5e9` | Sky (bullets, employee layer) |
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

**Slide 1 — Organization Management with ERPNext HRMS** (30s) — Title slide
- Subtitle: "A practical guide to master data, hierarchy, and structure of your workforce"
- Metadata block (bottom-right): Version 1.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Speaker notes: "Welcome the audience. Explain why organization data is the foundation of every downstream HRMS feature — attendance, payroll, leave, shift, expense. Brief mention only."
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "HRMS + Org Stack" / "Master Data Entities" / "Hierarchy & Relationships" / "Customization & Deployment".
- Numbers: 01 / 02 / 03 / 04.
- Speaker notes: "Walk through the four zones. Set expectations: we cover seven entities, their relationships, and how to extend the model."
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Speaker notes: "Position ERPNext HRMS as one module inside a larger ERP. The org-management entities live inside HRMS."
- Transition: "Now let's look at the data model — entities and their relationships."

### Early Schema Preview (slide 4 — DUPLICATE of slide 16)

**Slide 4 — Schema: Organization Entities** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13).
- Above: `<strong>Architecture:</strong> How organization entities relate across layers.`
- Below: "The relational model connects master data — Company, Department, Designation, Branch, Grade, Employment Type — to the Employee master."
- Speaker notes: "Employee sits at the center. Six master entities ring around it: Company (top), Department, Designation, Branch, Employee Grade, Employment Type. Mention only — recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the entities — why organization management matters."

### Why Organization Management Matters (slide 5)

**Slide 5 — Why organization management matters** (2 min)
- 3 bullets: scattered spreadsheets → inconsistent reporting / multi-branch, multi-role companies need a single source of truth / every downstream HR feature (leave, payroll, attendance) reads this structure.
- Visual: stacked-card icon row showing "Spreadsheets → Multiple Sources → One ERPNext Org Model" with arrows.
- Speaker notes: "Frame the pain: HR teams maintain org data in Excel, then payroll, leave, and shift tools each consume a different copy. Drift is inevitable. One model fixes this."
- Transition: "Let's start with the topmost master — Company."

### Master Data Entities (slides 6–11)

**Slide 6 — Company** (2 min)
- Lead paragraph: "A Company is the legal entity that owns every transaction in ERPNext. Every Employee, Department, and Branch links back to a Company."
- 3 entity cards: "Acme Healthcare" (multi-state hospital group), "Globex Manufacturing" (single-plant factory), "Initech Services" (consultancy with regional offices).
- Visual: `.entity-cards` row of three `.entity-card` blocks; color-bar = primary.
- Speaker notes: "Company is the top of the hierarchy. All transactional data — payroll, invoices, expenses — is scoped to a Company. In multi-company setups, each Company is fully isolated."
- Transition: "Inside a Company, work is grouped by Department."

**Slide 7 — Department** (2 min)
- Lead paragraph: "A Department is a functional unit within a Company — Nursing, Finance, IT. Departments group employees for reporting and approval routing."
- 3 key attributes: tree structure (parent + child departments) / approval authority per department / cost-center linkage.
- Visual: SVG tree showing "Operations → Nursing → ICU" / "Operations → Administration → HR".
- Speaker notes: "Departments form a tree, not a flat list. Useful for org charts, approval flows, and cost-center rollups. Define reporting line cleanly here."
- Transition: "Departments describe function — Designations describe role."

**Slide 8 — Designation** (2 min)
- Lead paragraph: "A Designation is the job title or role an Employee holds — Staff Nurse, Surgeon, HR Executive. It defines position-level expectations and salary bands."
- 3 key attributes: links to Employee Grade for compensation / drives approval limits / appears on payslips and reports.
- Visual: 3 entity cards: "Staff Nurse", "Senior Surgeon", "Operations Manager" — with a small "Grade: T4" tag.
- Speaker notes: "Designations are roles, not people. The same designation can be held by many employees. Keep the list tight — titles should reflect real job families, not individual career tracks."
- Transition: "Work happens in a place — Branch."

**Slide 9 — Branch** (2 min)
- Lead paragraph: "A Branch is a physical or logical location where work happens — a hospital site, a regional office, a warehouse. Employees are assigned to one Branch for attendance and headcount reporting."
- 3 key attributes: enables multi-site payroll / GPS-tagged check-in scope / per-branch holiday list override.
- Visual: SVG with dashed circle "Allowed Check-in Zone (200m radius)" around a building icon.
- Speaker notes: "Branch is the operational location. It separates Company (legal) from place (operational). The 200m check-in radius is illustrative — it is configurable per Branch."
- Transition: "Compensation levels live in Employee Grade."

**Slide 10 — Employee Grade** (2 min)
- Lead paragraph: "An Employee Grade is a pay band or seniority tier — T1, T2, T3, T4. It links a Designation to a compensation range and approval limit."
- 3 key attributes: drives payroll structure / default leave policy per grade / approval authority thresholds.
- Visual: 4 horizontal bars representing grades T1–T4, each with a salary range tag.
- Speaker notes: "Grades are the bridge between role (Designation) and money (Payroll). Keep grades few — 4 to 8 — so compensation review cycles stay clean."
- Transition: "How an Employee is engaged — Employment Type."

**Slide 11 — Employment Type** (2 min)
- Lead paragraph: "An Employment Type defines the contractual engagement — Full-time, Part-time, Contract, Intern. It governs which policies apply."
- 3 key attributes: leave accrual rules / probation period / contract end-date tracking.
- Visual: 4 entity cards: "Full-time", "Part-time", "Contract", "Intern" — each with a one-line policy note.
- Speaker notes: "Employment Type is the engagement lens. The same Designation (e.g., Engineer) can be Full-time or Contract with very different policies. Keep types few and mutually exclusive."
- Transition: "Now the master that ties them all together — the Employee."

### Employee Master + Reporting (slides 12–14)

**Slide 12 — Employee Master** (2 min) — IMAGE PLACEHOLDER (see §12)
- Lead paragraph: "The Employee DocType is the heart of HRMS. It links one person to a Company, Department, Designation, Branch, Grade, and Employment Type — and stores 200+ fields across personal, employment, payroll, and attendance tabs."
- 2 bullets: single source of truth for the workforce / every other HR DocType (Leave, Attendance, Payroll) references the Employee.
- Visual: `.image-placeholder` div with "Insert Employee form screenshot here" text (exact block in §12).
- Speaker notes: "Employee is the only required master — the six ring entities are optional references. Show how a clean Employee record unlocks every downstream feature."
- Transition: "Now the relationships between these entities."

**Slide 13 — Hierarchy & Relationships** (2 min)
- 3 bullets: Company → Department (one-to-many) / Employee → Branch (assignment) / Employee → Designation + Grade + Employment Type (linked dimensions).
- Visual: nested SVG tree — Company at root, three Departments below, each with one Branch and two Employees tagged with their Designation.
- Speaker notes: "Stress that hierarchy is enforced by links, not by inheritance. An Employee can move between Departments; the link updates and history is preserved."
- Transition: "All this data feeds into Reports."

**Slide 14 — Reports & Analytics** (2 min)
- 4 stat cards: Headcount 1,240, Departments 18, Branches 7, Open Positions 23.
- Visual: `<svg>` polyline chart inside `.chart-placeholder`, "Headcount Growth (Q3 peak 1,260)" marker.
- Speaker notes: "Standard HRMS reports run on this model out of the box: Employee Directory, Department-wise Headcount, Branch-wise Attendance, Grade-wise Payroll Cost. Custom reports add columns on top."
- Transition: "What if ERPNext out-of-box doesn't fit? Custom apps."

### Custom App + Schema (slides 15–16)

**Slide 15 — Extending ERPNext with Custom Apps** (2 min)
- 3 bullets: layer cleanly above core / add custom fields + DocTypes + workflows / deploy via Git + `bench`.
- Visual: 3-layer stack (Specialized App Layer on top, HRMS Core, ERPNext & Frappe base) — accent/primary/secondary.
- Speaker notes: "Custom fields let you add a `Cost Center Code` to Department without forking. Custom DocTypes add whole new entities — e.g., `Employee Skill Matrix` — linked to Employee."
- Transition: "Here's how the entities relate."

**Slide 16 — Schema: Organization Entities** (3 min) — full spec, identical SVG to slide 4
- Above: `<strong>Architecture:</strong> How organization entities relate across layers.`
- Below: same caption as slide 4.
- Speaker notes: "Walk the audience through each connection. Employee is the only mandatory DocType; the six surrounding entities are linked references. Optional entities can be disabled per Company."
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
- Speaker notes: "Recap the three takeaways. The next-step bullets give the audience a concrete path from this deck to a working deployment."
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

## 11. Concrete Example — Slide 6 (Company) — GOLD STANDARD

The body markup and CSS for Slide 6 must match the canonical `org-management-presentation.html` once generated. Every slide has a similar layout pattern (`.body` containing bullet list, paragraph, and one focal visual). Slide 6 specifically uses `.entity-cards` with three `.entity-card` blocks.

CSS excerpt:

```css
.entity-cards { display: flex; gap: var(--space-24); justify-content: center; margin-top: var(--space-32); }
.entity-card  { flex: 1; max-width: 220px; padding: var(--space-24) var(--space-16) var(--space-16); border-radius: 8px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border: 1px solid #e2e8f0; position: relative; }
.entity-color-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 8px 8px 0 0; }
.entity-name { font-size: 20px; font-weight: 600; color: var(--text); margin-top: var(--space-12, 12px); }
.entity-meta { font-size: 14px; color: var(--secondary); margin-top: var(--space-8); font-family: var(--font-mono); }
.entity-note { font-size: 13px; color: var(--secondary); margin-top: 4px; }
```

## 12. Employee Form Image Placeholder (Slide 12)

Slide 12 MUST contain exactly this placeholder block:

```html
<div class="image-placeholder" style="border: 2px dashed #94a3b8; padding: 48px 32px; text-align: center; color: #64748b; margin-top: 32px;">
  [Insert Employee form screenshot here]
  <br><small>Employee master — 200+ fields across tabs</small>
</div>
```

## 13. Schema Flowchart (Slides 4 and 16)

Both slides 4 and 16 contain the **same** inline SVG (740×320 viewBox). The SVG must include:

- **7 entity boxes** (rect+text): Company (top-center, primary), Employee (center, accent), Department / Designation / Branch / Employee Grade / Employment Type (ring around Employee, alternating primary/secondary).
- Connector paths in slate (`#94a3b8`); Employee is the only mandatory link target — the six surrounding entities all connect inward.
- One dashed line for an indirect relation (e.g., Designation → Employee Grade).

**Positioning (rough):** Employee at center (370, 150). Company top-center (370, 30). The five remaining entities arranged around Employee in a ring at radius ~140 px (Department, Designation, Branch, Employee Grade, Employment Type).

**Entities in the ring (suggested ordering, clockwise from top-left):** Department (top-left), Designation (top-right), Branch (right), Employee Grade (bottom-right), Employment Type (bottom-left).

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1 (org-management draft by Venkat, 2026-09-14)

- **Stale 2026-04-XX dates** — do not claim content is "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened. The deck does NOT talk about "Phase 6 docs / Tier 6 compliance".
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **Haritha-specific data from Venkat's discarded draft** — do not reuse any company name, employee count, department list, or branch from the discarded v1 prompt. All examples in the slides MUST be generic.

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 1.0 · Date 2026-09-14).
- **No Haritha-specific data** — no employee counts, no company-specific metrics, no real customer names.
- **Use generic illustrative examples** ("Acme Healthcare", "200m radius", "Department: Nursing", "Designation: Staff Nurse").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType: a database table in ERPNext", "Branch: a physical or logical location").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content) except where already established.

## 15. Quality Bar (10 checks — verify before declaring done)

1. All **18** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 == Schema (duplicate of slide 16, byte-identical SVG).
4. Slide 16 == Schema (original).
5. Per-slide timing sums to ~32 minutes.
6. SVG renders correctly (no broken tags).
7. Print stylesheet works.
8. No filler phrases.
9. Employee form image placeholder present (slide 12).
10. Schema flowchart present with all **7 entities** + relations (slides 4 and 16).

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 18`.
4. **Match the canonical org-management HTML byte-for-byte** — `prompts/build_deck.py` embeds the canonical snapshot and emits it directly. Any drift is a defect.
5. Only declare "done" when all 10 checks + byte-for-byte match pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/org-management-presentation.html`

## 18. Regeneration Workflow

`prompts/build_deck.py` is the single regenerator (same pattern as shift-mgmt v2):

1. Validates that the prompt describes 18 slides with Schema at #4 and #16.
2. Base64-decodes the embedded canonical snapshot.
3. Writes the bytes verbatim to the output path.

Re-running `python3 prompts/build_deck.py` is idempotent and produces a byte-for-byte match with the committed `org-management-presentation.html`. To update the deck:

1. Edit `docs/handbook/03-client/org-management-presentation.html` manually (Venkat-approved copy).
2. Re-embed its base64 in `prompts/build_deck.py` (one-line shell helper: `base64 -w0 path/to/org-management-presentation.html`).
3. Update the slide-by-slide spec in this prompt (`org-management-cmm-l5-presentation.md`) to match the new content.
4. Commit all three together.

---

## Appendix A — Changelog

- **v1.0** (2026-09-14) — Initial release based on shift-mgmt v2 pattern.
  - Adapted all 18 sections from `shift-management-cmm-l5-presentation-v2.md`.
  - Module: Organization Management in ERPNext HRMS.
  - 7 entities: Company, Employee, Department, Designation, Branch, Employee Grade, Employment Type.
  - Concrete gold standard: Slide 6 (Company) with `.entity-cards` CSS pattern.
  - Employee form image placeholder on slide 12.

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
- **#159** Continuous improvement — lessons from shift-mgmt v1 prompt are explicit drops in §14.
- **#160** Defect analysis — schema SVG character escaping (`&#39;` artifacts).
- **#161** Content freshness check — do not lie about dates; verify mtime vs claimed.
- **#162** Always do broad grep before claiming scope.
- **#163** "Up to date?" means BOTH structure AND metadata.
- **#164** Per-directory footers drift independently.

---

## Appendix C — Reference: `pberpprod` Data (Reference only)

> **Reference only — slides MUST use GENERIC examples per §14.** The following real data exists in the `pberpprod` bench and may be useful when auditing whether the deck's generic examples are reasonable. Do NOT cite these numbers or names in slide content.

The `pberpprod` bench (production-like environment) currently contains:

- **Company:** Haritha Hospitals (single Company record).
- **Departments:** a small set including HR, Finance, Operations.
- **Designations:** a short list of roles (executive and clinical tracks).
- **Branches:** 1 primary site.
- **Employee Grade:** ~3 grade tiers.
- **Employment Type:** Full-time is the dominant type; a handful of contract records.
- **Employees:** low double digits in this bench (this is a small test environment, NOT production scale).

If a slide's generic example (e.g., "Headcount 1,240, Departments 18, Branches 7, Open Positions 23" on slide 14) needs sanity-checking, this is the scale to compare against — but slides must use clearly illustrative numbers, not real ones.

**Reference URL:** https://docs.frappe.io/hr/employee
