## Shift Management with ERPNext HRMS — Deck Prompt (v2)

> **Status:** Draft for review · **Version:** 2.0 · **Date:** 2026-09-12 · **Author:** Venkat Narasimha
> **Audience:** Anyone generating or auditing this presentation deck (LLM agent, technical writer, reviewer).
> **Output:** `docs/handbook/03-client/shift-management-presentation-v2.html` (single self-contained HTML).

---

## 1. Role

You are a **technical writer + front-end developer** generating a single self-contained HTML presentation that explains **shift management in ERPNext HRMS** to a general audience. You follow CMM Level 5 documentation standards in your process (not in the deck content).

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

Produce an **18-slide** self-contained HTML presentation explaining shift management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

**Structural difference vs v1:** the Schema: Shift Management Entities slide appears **twice** — early (slide 4) and at its original position (slide 16). The early copy previews the architecture so the audience has a mental model before they see the entities in depth later.

## 4. Time Budget

- **Total: 40 minutes** (32 min content + 8 min Q&A).
- Per-slide timings sum to ~34 min — speaker can compress/expand as needed.
- See §8 for per-slide timings.

## 5. Output Specs

- **Format:** single `.html` file, fully self-contained (inline CSS, no external assets, no JavaScript libraries).
- **Slides:** exactly **18**, each `<section class="slide" id="slide-N">`.
- **Counter:** every slide shows `N / 18` (not 17, not 19 — must match exactly).
- **Navigation:** keyboard arrows (←/→) + click handlers.
- **Speaker notes:** hidden by default, toggle with `S` key.
- **Print:** include `@media print { ... }` for clean PDF export.
- **Accessibility:** semantic HTML, contrast ≥4.5:1 for body text, keyboard nav, ARIA labels.
- **No external images** — use inline SVG or pure CSS shapes.
- **No JavaScript libraries** — vanilla JS only.

## 6. Design Tokens (exact values — do not improvise)

### 6.1 Colors

| Token | Hex | Use |
|---|---|---|
| `--primary` | `#1e40af` | Deep blue (titles, schedule layer) |
| `--secondary` | `#64748b` | Slate (speaker notes, tracking layer) |
| `--accent` | `#0ea5e9` | Sky (bullets, execution layer) |
| `--text` | `#0f172a` | Near-black (body text) |
| `--muted` | `#94a3b8` | Muted (slide numbers, borders) |
| `--bg-odd` | `#ffffff` | Odd slides background |
| `--bg-even` | `#f8fafc` | Even slides background |
| `--code-bg` | `#f1f5f9` | Inline code background |
| `--code-text` | `#0f172a` | Inline code text |

### 6.2 Typography

- **Body:** `Inter, system-ui, -apple-system, sans-serif` at 18px / 1.6 line-height.
- **Headings:** same font, weight 600. Slide title 40px, h3 24px, h4 18px.
- **Code:** `JetBrains Mono, ui-monospace, monospace` at 14px.

### 6.3 Layout

- Max-width **960px**, centered.
- Padding: **64px top/bottom, 32px sides**.
- **Spacing scale:** 8 / 16 / 24 / 32 / 48 / 64 px — use these exact values, no other sizes.

### 6.4 Animation

- Slide-in: 200ms ease-out, `translateY(8px) → 0` + `opacity: 0 → 1`.

## 7. Slide Template (apply uniformly to all 18 slides)

Every slide MUST include:

1. `<div class="slide-number">N / 18</div>`
2. `<h2 class="slide-title">…</h2>`
3. `<div class="body">… main content (≤100 words), one focal visual …</div>`
4. `<aside class="speaker-notes">…</aside>` — hidden by default, toggle with `S` key.
5. **Transition note** (1 sentence) — included inside speaker notes.
6. **Timing note** — included inside speaker notes (e.g., "(2 min)").

## 8. Slide-by-Slide Specs (18 slides)

### Intro (slides 1–3)

**Slide 1 — Title** (30s)
- Title: "Shift Management with ERPNext HRMS"
- Subtitle: "A practical guide to planning, scheduling, attendance & reporting"
- Metadata block (bottom-right): Version 2.0 · Date 2026-09-12 · Audience General
- Visual: clean centered layout, no emoji.
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- Title: "Agenda"
- Visual: 4 numbered cards in a row (ERPNext + HRMS Stack / Shift Management Operations / Custom App + Schema / Why ERPNext + Haritha).
- Each card has 1-line sub-bullet.
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- Title: "ERPNext + HRMS Stack"
- 4 bullets: open-source ERP / ~12 domains / HRMS = HR module installable on top / 5,000+ contributors.
- Visual: layered stack diagram (Frappe Framework → ERPNext → HRMS).
- Transition: "Before we go deeper, here is the architecture."

### Early Schema Preview (slide 4 — DUPLICATE of slide 16)

**Slide 4 — Schema: Shift Management Entities** (1.5 min) — **EARLY PREVIEW**
- Title: "Schema: Shift Management Entities"
- 1 bullet above the diagram: "Architecture: how shift management entities relate across layers."
- Visual: inline SVG entity-relationship diagram (same SVG as slide 16, see §13).
- 1 bullet below: "Schedule templates + raw checkins → clean attendance records."
- Speaker notes: "Employee sits at the center. We will revisit each entity in detail. Brief mention only."
- Transition: "Now that you've seen the entities — why shift management matters."

### Shift Management Operations (slides 5–14)

**Slide 5 — Why shift management matters** (2 min)
- Title: "Why shift management matters"
- 3 bullets: unstructured spreadsheets → coverage gaps / 24/7 sectors need systematic scheduling / continuous ops require automation.
- Visual: 24h clock divided into 3 colored arcs (morning / afternoon / night).
- Transition: "Let's start with the foundation: Shift Type."

**Slide 6 — Shift Type** (2 min) — **SEE §11 CONCRETE EXAMPLE (gold standard)**
- Title: "Shift Type"
- 3 bullets: definition / properties / naming conventions.
- Visual: 3 shift cards side-by-side (Morning / Evening / Night), each with color stripe, name, time range.
- Transition: "But work happens at a place — that's Shift Location."

**Slide 7 — Shift Location** (1.5 min)
- Title: "Shift Location"
- 3 bullets: definition / why it matters (prevents buddy punching) / setup (GPS + radius).
- Visual: simple map mockup — pin marker + 200m radius circle, label "Allowed check-in zone".
- Transition: "Templates are scheduled — Shift Schedule."

**Slide 8 — Shift Schedule** (2 min)
- Title: "Shift Schedule"
- 3 bullets: definition / recurrence / used as master template for Shift Assignment.
- Visual: calendar grid mockup — week view with colored cells per shift type.
- Transition: "Employees can also request changes — Shift Request."

**Slide 9 — Shift Request** (2 min)
- Title: "Shift Request"
- 3 bullets: employee-initiated (swap, leave, change) / multi-level approval workflow / tracks request state.
- Visual: flow diagram — Employee → Manager → HR.
- Transition: "Once approved, the assignment happens — Shift Assignment."

**Slide 10 — Shift Assignment** (2 min)
- Title: "Shift Assignment"
- 3 bullets: actual assignment of employee to specific shift instance / validation prevents double-booking / notifications.
- Visual: simple table mockup — Employee | Shift Type | Date | Status.
- Transition: "Now the bulk + UI features — Bulk Assignment + Tool."

**Slide 11 — Bulk Assignment + Tool** (2.5 min)
- Title: "Bulk Assignment + Tool"
- 3 bullets: Shift Schedule Assignment (apply to many) / Shift Assignment Tool (drag-drop UI) / time saving (monthly roster in minutes).
- Visual: drag-drop mockup — calendar grid with employee names as draggable cards.
- Transition: "What does the result look like? The Roster."

**Slide 12 — Roster** (2 min) — **IMAGE PLACEHOLDER RESERVED (see §12)**
- Title: "Roster"
- Top 60%: text content (visual calendar / filters / color-coded).
- Bottom 40%: reserved image area with placeholder HTML from §12.
- Transition: "Now let's track who's actually showing up — Attendance."

**Slide 13 — Attendance + Auto-attendance** (2 min)
- Title: "Attendance + Auto-attendance"
- 3 bullets: auto-attendance (GPS / biometric / mobile) / manual override / real-time late-arrival detection.
- Visual: workflow diagram — Check-in → Match Shift → Mark Present/Late.
- Transition: "All this data feeds into Reports."

**Slide 14 — Reports & Analytics** (2 min)
- Title: "Reports & Analytics"
- 4 bullets: daily attendance summary / late arrivals + early departures / overtime tracking / department-wise headcount.
- Visual: dashboard mockup — 4 small stat cards + 1 line chart.
- Transition: "What if ERPNext out-of-box doesn't fit? Custom apps."

### Custom App + Schema (slides 15–16)

**Slide 15 — Extending ERPNext with Custom Apps** (2 min)
- Title: "Extending ERPNext with Custom Apps"
- 3 bullets: when ERPNext out-of-box doesn't fit (build a custom app) / extend via custom fields + custom DocTypes + custom workflows / version-controlled via Git, deployable via `bench install-app`.
- Visual: layered architecture — ERPNext base + Custom app layer on top.
- Transition: "Here's how the entities relate in detail."

**Slide 16 — Schema: Shift Management Entities** (3 min) — **SEE §13 SCHEMA DETAILS (full spec)**
- Title: "Schema: Shift Management Entities"
- Visual: inline SVG entity-relationship diagram (see §13 for full spec).
- 1 bullet above: "How shift management entities relate"
- 1 bullet below: "ERPNext's open schema means you can extend with custom fields/tables"
- Speaker notes: walk through central entity (Employee) and relations.
- Transition: "Why choose ERPNext + Haritha for your deployment."

### Why Choose + Conclusion (slides 17–18)

**Slide 17 — Why Choose ERPNext + Haritha** (2 min)
- Title: "Why choose ERPNext + Haritha"
- 5 bullets: open source / 100% custom code ownership / healthcare-ready / active community / flexibility wins.
- Visual: comparison table (3 columns: ERPNext + Haritha / SAP / Workday) for top 3 differentiators.
- Transition: "Let's wrap up."

**Slide 18 — Conclusion + Next Steps** (2 min)
- Title: "Conclusion + Next Steps"
- 3 takeaways (numbered): ERPNext + HRMS = complete open-source stack / shift mgmt covers full lifecycle / custom apps adapt ERPNext to your industry.
- Next steps (3 bullets): explore the demo / plan a pilot (4–8 weeks) / contact for custom development.
- Visual: simple centered list, no chart.
- Transition: "Thank you" + Q&A starts.

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
    <br><br><strong>Transition:</strong> [1 sentence]
    <br><br><strong>Timing:</strong> [N min]
  </aside>
</section>
```

## 10. Speaker Notes Toggle (vanilla JS)

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 's' || e.key === 'S') {
    document.body.classList.toggle('show-speaker-notes');
  }
  if (e.key === 'ArrowRight' || e.key === ' ') { /* next slide */ }
  if (e.key === 'ArrowLeft')  { /* prev slide */ }
});
```

CSS:

```css
.speaker-notes { display: none; font-size: 14px; color: var(--secondary); border-left: 3px solid var(--accent); padding: 8px 16px; margin-top: 24px; font-style: italic; background: rgba(241,245,249,0.6); }
.show-speaker-notes .speaker-notes { display: block; }
```

## 11. Concrete Example — Slide 6 (Shift Type) — GOLD STANDARD

This slide must follow this exact pattern (every other slide follows §9):

```html
<section class="slide" id="slide-6">
  <div class="slide-number">6 / 18</div>
  <h2 class="slide-title">Shift Type</h2>
  <div class="body">
    <p>A Shift Type is a reusable template that defines when work happens. You define Morning, Evening, and Night once, then assign employees to instances of these templates on specific dates.</p>
    <div class="shift-cards">
      <div class="shift-card">
        <div class="shift-color-bar" style="background:#1e40af;"></div>
        <div class="shift-name">Morning</div>
        <div class="shift-time">06:00 – 14:00</div>
        <div class="shift-hours">8 hours</div>
      </div>
      <div class="shift-card">
        <div class="shift-color-bar" style="background:#0ea5e9;"></div>
        <div class="shift-name">Evening</div>
        <div class="shift-time">14:00 – 22:00</div>
        <div class="shift-hours">8 hours</div>
      </div>
      <div class="shift-card">
        <div class="shift-color-bar" style="background:#64748b;"></div>
        <div class="shift-name">Night</div>
        <div class="shift-time">22:00 – 06:00</div>
        <div class="shift-hours">8 hours</div>
      </div>
    </div>
  </div>
  <aside class="speaker-notes">
    Shift Types are templates, not specific dates. You define Morning, Evening, Night once, then assign employees to instances on actual dates. Real example: a hospital uses "Doctor Morning" (07:00-15:00) and "Nurse Night" (22:00-06:00) as recurring shift types. Press 'S' to hide these notes during the talk.
    <br><br><strong>Transition:</strong> But work happens at a place — that's Shift Location.
    <br><br><strong>Timing:</strong> 2 min
  </aside>
</section>
```

CSS:

```css
.shift-cards { display: flex; gap: 24px; justify-content: center; margin-top: 32px; }
.shift-card  { flex: 1; max-width: 220px; padding: 24px 16px 16px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border: 1px solid #e2e8f0; position: relative; }
.shift-color-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 8px 8px 0 0; }
.shift-name  { font-size: 20px; font-weight: 600; color: #0f172a; margin-top: 12px; }
.shift-time  { font-size: 16px; color: #1e40af; margin-top: 8px; font-family: 'JetBrains Mono', monospace; }
.shift-hours { font-size: 13px; color: #64748b; margin-top: 4px; }
```

**This is the gold standard** — every other slide matches this structure.

## 12. Roster Image Placeholder (Slide 12)

Bottom 40% of slide 12 MUST contain exactly:

```html
<div class="image-placeholder" style="border: 2px dashed #94a3b8; padding: 48px 32px; text-align: center; color: #64748b; margin-top: 32px;">
  [Insert roster screenshot here]
  <br><small>Roster view — calendar of employee shifts</small>
</div>
```

## 13. Schema Flowchart Details (Slides 4 and 16)

Both slides 4 and 16 contain the **same** inline SVG. Full entity table (from `docs/handbook/01-schema/01.2-schema-diagram.md`):

| Entity | Key fields | Links to |
|---|---|---|
| Employee | name, employee_name, company, department, designation | (root) |
| Shift Type | name, start_time, end_time, color | (root) |
| Shift Location | location_name, latitude, longitude, radius | (root) |
| Shift Schedule | shift_type, from_date, to_date, frequency | Shift Type |
| Shift Assignment | employee, shift_type, start_date, end_date, status, shift_location | Employee, Shift Type, Shift Location, Shift Schedule |
| Shift Request | employee, shift_type, from_date, to_date, status | Employee, Shift Type |
| Holiday List | holiday_date, description | (root, applies via holiday_list field) |
| Attendance | employee, attendance_date, status, shift | Employee, Shift Type |
| Employee Checkin | employee, time, log_type, latitude, longitude | Employee |

**SVG structure:**

- 9 entity boxes (rounded rectangles).
- Arrows showing Link fields (label each with field name).
- Group entities by function:
  - **Schedule layer (primary `#1e40af`):** Shift Type, Shift Schedule, Shift Location.
  - **Execution layer (accent `#0ea5e9`):** Shift Assignment, Shift Request, Employee Checkin.
  - **Tracking layer (secondary `#64748b`):** Attendance, Holiday List.
  - **Core:** Employee in the center (primary `#1e40af`), connects to all.
- The SVG must fit in a 740×320 viewBox and use the design tokens for fills/strokes.
- Reference the existing slide-4 / slide-16 SVG in the v2.html for exact layout.

**Positioning (rough):** Employee at center (370, 150). Holiday List top-center. Attendance bottom-center. Shift Type / Schedule / Location on the right column. Shift Request / Assignment / Checkin on the left column.

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim content is "up to date as of April 2026". Use only verified dates. (Lesson #161: Content freshness check — don't lie about dates; verify mtime vs claimed.)
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened (commit `9f6a97e`). The deck content does NOT talk about "Phase 6 docs / Tier 6 compliance". The deck talks about shift management in ERPNext. (Lesson #162: Always do broad grep before claiming scope.)
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **The "v2.1" metadata claim** — this prompt is v2.0; do not claim any other version.

### Required

- **"Up to date?" means BOTH structure AND metadata.** (Lesson #163.)
- **Per-directory footers drift independently.** When referencing external files, note their last-modified date if it matters. (Lesson #164.)
- **No Haritha-specific data** — no employee counts (e.g., "210 employees"), no company-specific metrics, no real customer names.
- **Use generic illustrative examples** ("Morning shift 06:00-14:00", "Ward A", "200m radius").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType: a database table in ERPNext").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content) except where already established.

## 15. Quality Bar (10 checks — verify before declaring done)

1. All **18** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 == Schema (duplicate of slide 16).
4. Slide 16 == Schema (original).
5. Per-slide timing sums to ~32 minutes.
6. SVG renders correctly (no broken tags).
7. Print stylesheet works (test with browser print preview).
8. No filler phrases (run a search for "important", "as we can see", "in this slide", "It is worth noting", "essentially").
9. Roster image placeholder present (slide 12).
10. Schema flowchart present with all 9 entities + relations (slides 4 and 16).

## 16. Self-Review Step (MANDATORY)

Before returning the generated HTML:

1. Read your own output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual is non-trivial, speaker notes present, counter shows `N / 18`.
4. **Note any deviations** in a final `<!-- REVIEW NOTES -->` HTML comment block at end of file.
5. Only declare "done" when all 10 checks pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/shift-management-presentation-v2.html`

---

## Appendix A — Lessons Applied (#151–#164)

These lessons came from prior prompt and doc work; this prompt embeds them so the deck generation cannot regress.

- **#151** Quantitative process management — every spec has a measurable check (§15).
- **#152** Defect prevention — verify before declaring done (§16).
- **#153** Change management — version this prompt (v2.0), document changes in changelog.
- **#154** Technology change management — design tokens frozen (§6), no improvisation.
- **#155** Peer review — generator output goes through self-review before "done".
- **#156** Process measurement — counter `N / 18` must match exactly across all slides.
- **#157** Process analysis — single root cause for duplicates (Schema preview), not arbitrary.
- **#158** Process innovation — speaker notes pattern reusable across all 18 slides.
- **#159** Continuous improvement — lessons from v1 prompt are explicit drops in §14.
- **#160** Defect analysis — schema SVG had `&#39;` artifacts; this prompt specifies SVG character escaping.
- **#161** Content freshness check — do not lie about dates; verify mtime vs claimed.
- **#162** Always do broad grep before claiming scope — covers stale "Phase 6 / Tier 6" mentions.
- **#163** "Up to date?" means BOTH structure AND metadata — covers prompt header + slide 1 metadata block.
- **#164** Per-directory footers drift independently — covers external file references.

---

## Appendix B — Changelog

- **v2.0** (2026-09-12) — Initial v2 release.
  - Added Schema duplicate at slide 4 (early preview).
  - Renumbered slides 4–13 → 5–14 (10 slides).
  - Added slides 15 (Extending ERPNext) and 16 (Schema full spec) preserving original positions +1.
  - Renumbered slides 16–17 → 17–18.
  - Counter changed from `N / 17` to `N / 18`.
  - Embedded CMM L5 lessons #151–#164.
  - Dropped stale dates, dropped stale "Phase 6 / Tier 6" content references, dropped stale MTM mentions.
  - Concrete example moved from slide 5 → slide 6 (Shift Type).
