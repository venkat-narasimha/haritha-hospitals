## Organization Management in ERPNext HRMS — Deck Prompt (v2)

> **Status:** Pinned canonical spec · **Version:** 2.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
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

Produce a **17-slide** self-contained HTML presentation explaining organization management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

**Structural difference vs v1:** slide count reduced from 18 to 17 by removing the vendor-pitch slide. Slide 12 changed from an image placeholder to a 6-row data-table mockup of Employee key fields — the data table communicates more structural information than a screenshot. The Schema: Organization Entities slide still appears **twice** — early (slide 4, clean preview) and at its original position (slide 16, full spec with relationship labels + legend). The early copy previews the architecture so the audience has a mental model before they see the entities in depth later.

## 4. Time Budget

- **Total: 40 minutes** (32 min content + 8 min Q&A).
- Per-slide timings sum to ~32 min — speaker can compress/expand as needed.
- See §8 for per-slide timings.

## 5. Output Specs

- **Format:** single `.html` file, fully self-contained (inline CSS, no external assets, no JavaScript libraries).
- **Slides:** exactly **17**, each `<section class="slide" id="slide-N">`.
- **Counter:** every slide shows `N / 17` (not 16, not 18 — must match exactly).
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
| `--accent` | `#0ea5e9` | Sky (bullets, employee attribute layer) |
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

## 7. Slide Template (apply uniformly to all 17 slides)

Every slide MUST include:

1. `<div class="slide-number">N / 17</div>`
2. `<h2 class="slide-title">…</h2>`
3. `<div class="body">… main content (≤100 words), one focal visual …</div>`
4. `<aside class="speaker-notes">…</aside>` — hidden by default, toggle with `S` key.
5. **Transition note** (1 sentence) — included inside speaker notes.

## 8. Slide-by-Slide Specs (17 slides)

### Intro (slides 1–3)

**Slide 1 — Organization Management with ERPNext HRMS** (30s) — Title slide
- Subtitle: "A practical guide to master data, hierarchy, and structure of your workforce"
- Metadata block (bottom-right): Version 2.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Speaker notes: "Welcome the audience. Explain why organization data is the foundation of every downstream HRMS feature — attendance, payroll, leave, shift, expense. Brief mention only."
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "HRMS + Org Stack" / "Master Data Entities" / "Hierarchy & Relationships" / "Customization & Deployment".
- Numbers: 01 / 02 / 03 / 04.
- Speaker notes: "Walk through the four zones. Set expectations: we cover seven entities — Company, Department, Branch, Designation, Grade, Employment Type, Employee — their relationships, and how to extend the model."
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Speaker notes: "Position ERPNext HRMS as one module inside a larger ERP. The org-management entities live inside HRMS."
- Transition: "Now let's look at the data model — entities and their relationships."

### Early Schema Preview (slide 4 — clean preview, no labels)

**Slide 4 — Schema: Organization Entities** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13 for slide 4 variant).
- Above: `<strong>Architecture:</strong> How organization entities relate across layers.`
- Below: "The relational model connects master data — Company, Department, Branch, Designation, Grade, Employment Type — to the Employee master."
- Speaker notes: "Employee sits at the center. Six reference entities ring around it: Company (legal, top), Department and Branch (org structure, mid), Designation, Grade, and Employment Type (employee attributes, lower). Two dashed groups show the layering. Brief mention only — recap: Schema shown earlier in the deck."
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
- Transition: "Compensation levels live in Grade."

**Slide 10 — Grade** (2 min)
- Lead paragraph: "A Grade is a pay band or seniority tier — T1, T2, T3, T4. It links a Designation to a compensation range and approval limit."
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

**Slide 12 — Employee Master: Key Fields** (2 min) — TABLE MOCKUP (see §11.2 and §12)
- Lead paragraph: "The Employee DocType is the heart of HRMS. It links one person to a Company, Department, Branch, Designation, Grade, and Employment Type — and captures the field groups below."
- Visual: 3-column × 6-row `<table class="field-table">` mockup with the field groups from §12.
- Speaker notes: "Employee is the only required master — the six ring entities are optional references. Walk the audience through each row of the table: personal identity, joining tenure, employment structure, who approves what, statutory identifiers for payroll, and the offboarding trail."
- Transition: "Now the relationships between these entities."

**Slide 13 — Hierarchy & Relationships** (2 min)
- 3 bullets: Company → Department (one-to-many) / Employee → Branch (operational assignment) / Employee → Designation + Grade + Employment Type (linked dimensions).
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
- Transition: "Here's the full schema, now with relationship labels."

**Slide 16 — Schema: Organization Entities** (3 min) — full spec, ENHANCED over slide 4 (see §13 for slide 16 variant)
- Above: `<strong>Architecture:</strong> How organization entities relate across layers — with relationship labels, field hints, and a legend for color and connector meanings.`
- Below: "Employee is the only mandatory DocType; the six surrounding entities are linked references. Direct connectors are solid lines; hierarchical relations are dashed."
- Speaker notes: "Walk the audience through each connection. Read the labels: 'belongs to' (Department), 'located at' (Branch), 'has role' (Designation), 'has grade' (Grade), 'contract type' (Employment Type), 'employed by' (Company). The dashed group rectangles show the Org Hierarchy vs Employee Attributes layering. Optional entities can be disabled per Company."
- Transition: "Let's wrap up."

### Conclusion (slide 17)

**Slide 17 — Conclusion + Next Steps** (2 min)
- "Key Takeaways" h3 + numbered list (3 items).
- "Next Steps" h4 + 3 bullets (demo sandbox `demo.example.com` / pilot 4-8 weeks / architecture review).
- "Why this deck exists" short paragraph framing open-source HRMS as a credible alternative to proprietary suites — without vendor pitch specifics.
- Speaker notes: "Recap the three takeaways. The next-step bullets give the audience a concrete path from this deck to a working deployment."
- Transition: "Thank you and welcome to the Q&A."

## 9. Slide Template HTML

```html
<section class="slide" id="slide-N">
  <div class="slide-number">N / 17</div>
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

### 11.1 Slide 6 (Company) — `.entity-cards` pattern

The body markup and CSS for Slide 6 must match the canonical `org-management-presentation.html` once generated. Every slide has a similar layout pattern (`.body` containing paragraph, then one focal visual). Slide 6 specifically uses `.entity-cards` with three `.entity-card` blocks.

CSS excerpt:

```css
.entity-cards { display: flex; gap: var(--space-24); justify-content: center; margin-top: var(--space-32); }
.entity-card  { flex: 1; max-width: 220px; padding: var(--space-24) var(--space-16) var(--space-16); border-radius: 8px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border: 1px solid #e2e8f0; position: relative; }
.entity-color-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 8px 8px 0 0; }
.entity-name { font-size: 20px; font-weight: 600; color: var(--text); margin-top: var(--space-12, 12px); }
.entity-meta { font-size: 14px; color: var(--secondary); margin-top: var(--space-8); font-family: var(--font-mono); }
.entity-note { font-size: 13px; color: var(--secondary); margin-top: 4px; }
```

### 11.2 Slide 12 (Employee Key Fields) — `.field-table` pattern

Slide 12 uses `.field-table` (3-column data table) for the Employee key-fields mockup. The table is the central artifact for the Employee master — more useful than a screenshot because it makes the field-group structure explicit.

CSS excerpt:

```css
.field-table { width: 100%; border-collapse: collapse; margin-top: var(--space-24); font-size: 15px; }
.field-table thead th { background: var(--primary); color: #ffffff; text-align: left; padding: var(--space-12) var(--space-16); font-weight: 600; font-size: 14px; }
.field-table tbody td { padding: var(--space-12) var(--space-16); border-bottom: 1px solid #e2e8f0; vertical-align: top; color: var(--text); }
.field-table tbody tr:nth-child(even) { background: var(--bg-even); }
.field-table .field-group { font-weight: 600; color: var(--primary); width: 22%; }
.field-table .field-keys  { font-family: var(--font-mono); font-size: 13px; color: var(--secondary); width: 38%; }
.field-table .field-purpose { color: var(--text); width: 40%; }
```

## 12. Employee Key Fields Table (Slide 12)

Slide 12 MUST contain exactly this `<table class="field-table">` block — 3 columns × 6 rows:

```html
<table class="field-table">
  <thead>
    <tr>
      <th>Field Group</th>
      <th>Key Fields</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="field-group">Personal</td>
      <td class="field-keys">name, date_of_birth, contact</td>
      <td class="field-purpose">Identification, emergency contact, statutory age checks.</td>
    </tr>
    <tr>
      <td class="field-group">Joining</td>
      <td class="field-keys">date_of_joining, confirmation_date, probation</td>
      <td class="field-purpose">Tenure tracking, probation completion, anniversary triggers.</td>
    </tr>
    <tr>
      <td class="field-group">Employment</td>
      <td class="field-keys">employment_type, grade, branch, department</td>
      <td class="field-purpose">Day-to-day reporting structure and policy scope.</td>
    </tr>
    <tr>
      <td class="field-group">Approvers</td>
      <td class="field-keys">leave_approver, expense_approver, shift_request_approver</td>
      <td class="field-purpose">Auto-populated on request documents; routed for approval.</td>
    </tr>
    <tr>
      <td class="field-group">Statutory</td>
      <td class="field-keys">PAN, IFSC, PF_account_number</td>
      <td class="field-purpose">Payroll, bank disbursal, statutory filings.</td>
    </tr>
    <tr>
      <td class="field-group">Exit</td>
      <td class="field-purpose">relieving_date, exit_status, final_settlement</td>
      <td class="field-purpose"></td>
    </tr>
  </tbody>
</table>
```

> NOTE: The last row's second cell intentionally uses `field-purpose` class for the date/status values and the third cell is a separate `field-purpose` rendered blank — this matches the canonical screenshot.

## 13. Schema Flowchart (Slides 4 and 16)

Slides 4 and 16 contain **different** inline SVG variants (740×320 viewBox). Slide 4 is the clean preview; slide 16 is the enhanced full spec.

### 13.1 Slide 4 (clean preview) — entities + groupings, NO labels

- **7 entity boxes** (rect + 1-line text):
  - **Company** — top-center (primary `#1e40af`)
  - **Department** — mid-left (primary)
  - **Branch** — mid-right (primary)
  - **Employee** — center (primary, slightly larger)
  - **Employment Type** — bottom-left (accent `#0ea5e9`)
  - **Grade** — bottom-center (accent)
  - **Designation** — bottom-right (accent)
- **2 dashed group rectangles** (`stroke-dasharray="4 4"`, slate stroke), each with small label outside the upper-left corner:
  - **Org Hierarchy** — encloses Company + Department + Branch (top half of canvas).
  - **Employee Attributes** — encloses Employment Type + Grade + Designation (bottom strip of canvas).
- **7 connectors** — plain slate (`#94a3b8`) lines. One dashed line for the hierarchical Department→Company edge. **NO connector labels, NO field hints, NO legend.**

### 13.2 Slide 16 (enhanced full spec) — entities + labels + hints + legend

Same 7 entities + 2 groupings as slide 4, with these additions:

- **Field hints** in each entity box (smaller second line, light-tinted to box's fill):
  - Company → "name, tax_id"
  - Department → "name, parent_dept"
  - Branch → "name, location"
  - Employee → "name, status, branch" (slightly larger box)
  - Employment Type → "name, duration"
  - Grade → "name, pay_band"
  - Designation → "name, description"
- **Relationship labels on each connector** (white-fill rect + small grey text, near midpoint):
  - Employee → Company → `"employed by"`
  - Employee → Department → `"belongs to"`
  - Employee → Branch → `"located at"`
  - Employee → Designation → `"has role"`
  - Employee → Grade → `"has grade"`
  - Employee → Employment Type → `"contract type"`
  - Department → Company → `"part of"` (dashed hierarchical line)
- **Legend box** (130×36 px, white fill, slate border, bottom-left of canvas, ~translate(15,180)):
  - Color swatches: primary square = `Master / Config`; accent square = `Attribute`.
  - Connector symbols: solid line = `direct`; dashed line = `hierarchical`.

### 13.3 Positioning (shared by both variants)

- Employee (center): rect at `x=305 y=130 w=130 h=60`.
- Company (top): rect at `x=310 y=55 w=120 h=45`.
- Department (mid-left): rect at `x=40 y=105 w=130 h=50`.
- Branch (mid-right): rect at `x=560 y=105 w=130 h=50`.
- Employment Type (bottom-left): rect at `x=40 y=235 w=130 h=50`.
- Grade (bottom-center): rect at `x=305 y=240 w=130 h=50`.
- Designation (bottom-right): rect at `x=560 y=235 w=130 h=50`.
- Org Hierarchy dashed group: `x=10 y=20 w=720 h=155`.
- Employee Attributes dashed group: `x=10 y=220 w=720 h=90`.

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim content is "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened. The deck does NOT talk about "Phase 6 docs / Tier 6 compliance".
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **Vendor-pitch slide ("Why choose ERPNext + Haritha")** — dropped in v2.0; replaced by a neutral closing paragraph on slide 17.
- **Employee-form image placeholder (v1 slide 12)** — dropped in v2.0; replaced by the field-group table mockup in §12.

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 2.0 · Date 2026-09-14).
- **No vendor-specific data** — no employee counts, no real customer names, no company-specific metrics.
- **Use generic illustrative examples** ("Acme Healthcare", "200m radius", "Department: Nursing", "Designation: Staff Nurse", "Headcount 1,240").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType: a database table in ERPNext", "Branch: a physical or logical location", "Grade: a pay band or seniority tier").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content).

## 15. Quality Bar (10 checks — verify before declaring done)

1. Exactly **17** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 = Schema preview (7 entities + 2 dashed groupings only — NO connector labels, NO legend).
4. Slide 16 = Schema full spec (7 entities + 7 labeled connectors + legend + field hints).
5. Per-slide timings sum to ~32 minutes.
6. Both SVGs render correctly (no broken tags, no overlap).
7. Print stylesheet works.
8. No filler phrases anywhere.
9. Slide 12 = Employee key fields **table** mockup (3 columns × 6 rows) — NOT an image placeholder.
10. Slide 16 connector labels present and read in order: "employed by", "belongs to", "located at", "has role", "has grade", "contract type", "part of".

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 17`.
4. **Match this prompt's slide-by-slide spec exactly.** Any drift between the spec and the generated HTML is a defect (per-deck decisions are locked; see prompt header).
5. Only declare "done" when all 10 checks pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/org-management-presentation.html`

## 18. Prompt Maintenance Workflow

See `prompts/README.md` § Prompt Maintenance Workflow.

---

## Appendix A — Changelog

See `prompts/README.md` § Current Prompts table for version history.

---

## Appendix B — Lessons Applied (#151–#164)

See `prompts/README.md` § Shared Methodology (Lessons #151–#164).
