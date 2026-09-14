## Attendance Management with ERPNext HRMS — Deck Prompt (v2)

> **Status:** Active spec · **Version:** 2.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
> **Audience:** Anyone generating or auditing this presentation deck (LLM agent, technical writer, reviewer).
> **Output:** `docs/handbook/03-client/attendance-management-presentation.html` (single self-contained HTML).

---

## 1. Role

You are a **technical writer + front-end developer** producing a single self-contained HTML presentation that explains **attendance management in ERPNext HRMS** to a general audience. You follow CMM Level 5 documentation standards in your process (not in the deck content).

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

Produce a **16-slide** self-contained HTML presentation explaining attendance management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

**Structural difference vs shift-mgmt v2 (18 slides):** Attendance consolidates the bulk-input pair (Employee Attendance Tool + Upload Attendance) into narrative context rather than separate entity slides, since both serve the same operational job. Slide count reflects the actual entity count + concept coverage rather than the v2 default.

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
| `--primary` | `#1e40af` | Deep blue (titles, output/process layer) |
| `--secondary` | `#64748b` | Slate (speaker notes, reference layer) |
| `--accent` | `#0ea5e9` | Sky (raw input layer) |
| `--text` | `#0f172a` | Near-black (body text) |
| `--muted` | `#94a3b8` | Muted (optional/edge-case layer) |
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

**Slide 1 — Attendance Management with ERPNext HRMS** (30s) — Title slide
- Subtitle: "Daily presence tracking across biometrics, mobile, and manual input"
- Metadata block (bottom-right): Version 2.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "HRMS + Attendance Stack" / "Daily Tracking Methods" / "Auto-Attendance Engine" / "Reports & Edge Cases".
- Numbers: 01 / 02 / 03 / 04.
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNExt / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Transition: "Now let's look at the data model — entities and their relationships."

### Early Schema Preview (slide 4 — clean preview, no labels)

**Slide 4 — Schema: Attendance Entities** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13 § Schema Flowchart § Slide 4 variant).
- Above: `<strong>Architecture:</strong> How attendance entities relate across layers.`
- Below: "The relational model connects raw check-ins to attendance records via the Auto Attendance engine."
- Speaker notes: "Employee sits in the middle. Employee Checkin on the left (raw punches), Auto Attendance in the middle (the conversion process), Attendance on the right (the daily record). Holiday List + Shift Type are reference inputs at the top. Attendance Request is an optional flow at the bottom. Brief mention only. Recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the entities — why attendance management matters."

### Attendance Management Operations (slides 5–11)

**Slide 5 — Why attendance management matters** (2 min)
- 3 bullets: manual paper registers lose data / multiple input sources (biometric, mobile, manual) require unified tracking / automation reduces disputes and payroll errors.
- Visual: simple icon row (punch card, mobile phone, biometric scanner, ID card) showing input diversity.
- Transition: "Let's start with the foundation: the Attendance record itself."

**Slide 6 — Attendance (the daily record)** (2 min)
- Lead paragraph: "An Attendance row captures whether an employee was Present, Absent, On Leave, or Half Day for a specific date. It's the canonical ledger for daily presence."
- 3 key attributes: `attendance_date`, `employee`, `status` enum (Present / Absent / On Leave / Half Day).
- Visual: single-row mockup of an Attendance table row (status badge: Present in primary blue).
- Transition: "But attendance rows come from somewhere — raw check-ins."

**Slide 7 — Employee Checkin (raw IN/OUT punch)** (2 min)
- Lead paragraph: "An Employee Checkin is a single IN or OUT punch record. Source can be biometric device, mobile app, or manual."
- 3 bullets: biometric/RFID push / mobile app / manual entry.
- Visual: 3 card mockups (Biometric, Mobile, Manual) with sample timestamps.
- Transition: "Raw punches don't become attendance automatically — Auto Attendance does the matching."

**Slide 8 — Auto Attendance (the conversion engine)** (2 min)
- Lead paragraph: "Auto Attendance is a background process that converts raw Employee Checkin rows into Attendance rows by matching punch times against Shift Type configurations and Holiday List dates."
- 3 bullets: cron-driven / matches against Shift Type + Holiday List / respects grace period + late/early thresholds.
- Visual: SVG flow (Checkin rows → Match Engine → Attendance ledger).
- Transition: "Not all attendance comes from punches — sometimes HR needs to mark it manually."

**Slide 9 — Employee Attendance Tool (bulk marking)** (1.5 min)
- Lead paragraph: "The Employee Attendance Tool lets HR Admins bulk-mark attendance for a date range. Useful for non-biometric sites, off-team events, or catching up on missed entries."
- 3 bullets: bulk mark by department / exclude holidays toggle / apply status (Present / Absent / Half Day).
- Visual: tool screenshot mockup (date picker + employee list + action buttons).
- Transition: "For larger datasets, Upload Attendance handles CSV imports."

**Slide 10 — Attendance Request (employee regularisation)** (2 min)
- Lead paragraph: "An Attendance Request lets an employee regularise a missed check-in or dispute a recorded absence. Approval routes to the employee's leave approver."
- 3 bullets: self-service form / reason text + supporting attachment / approver workflow.
- Visual: 2-step approval flow (Employee → Leave Approver).
- Transition: "All these inputs roll up into the daily view your HR team reads."

**Slide 11 — Daily Attendance View (table mockup)** (2 min)
- Lead paragraph: "The Daily Attendance View is what HR uses to review and act on attendance data. Here's a representative day across a mixed-status team."
- 5-row table mockup: Employee + Shift + Check-in + Check-out + Status + Notes.
  - Aisha Khan · Morning 09:00–18:00 · 09:02 · 18:05 · Present · —
  - Biju Mathew · Morning 09:00–18:00 · 10:30 · 18:00 · Half Day · Traffic delay
  - Chen Yi · Evening 14:00–22:00 · — · — · On Leave · Approved SL
  - Diego Ruiz · Night 22:00–06:00 · 22:08 · 06:12 · Present · Grace -10 min
  - Elena Park · Morning 09:00–18:00 · — · — · Absent · Uninformed
- Visual: `<table class="attendance-table">` with status badges (Present/primary, Half Day/accent, On Leave/slate, Absent/muted).
- Transition: "Beyond daily view — what reports does this data feed?"

**Slide 12 — Reports & Analytics** (2 min)
- 3 cards: Monthly Attendance Details (built-in) / Late Arrivals summary (custom) / Absenteeism rate (derived).
- Visual: bar chart SVG showing attendance status distribution for one week.
- Transition: "What if out-of-box doesn't fit? Custom apps."

### Custom App + Schema (slides 13–14)

**Slide 13 — Extending ERPNext with Custom Apps** (2 min)
- 3 bullets: layer cleanly above core / add custom fields + DocTypes + workflows / deploy via Git.
- Visual: 3-layer stack (Specialized App Layer on top, HRMS Core, ERPNext & Frappe base) — accent/primary/secondary.
- Transition: "Here's how the entities relate in full."

**Slide 14 — Schema: Attendance Entities** (3 min) — full spec, ENHANCED over slide 4 (see §13 § Schema Flowchart § Slide 16 variant)
- Above: `<strong>Architecture:</strong> How attendance entities relate across layers — with relationship labels, field hints, and a legend for color and connector meanings.`
- Below: "Employee Checkin and Auto Attendance are the input-side. Attendance is the output. Holiday List + Shift Type are reference contexts. Attendance Request is an optional flow for employee-initiated regularisation."
- Speaker notes: "Walk the audience through each connection. Read the labels: 'raw punch' (Checkin → Auto Attendance), 'converts to' (Auto Attendance → Attendance), 'matches against' (Auto Attendance ← Holiday List + Shift Type), 'creates on approval' (Attendance Request → Attendance), 'approved via' (Employee → Attendance Request). The dashed group rectangles show Daily Tracking vs Reference Context layering."
- Transition: "Let's wrap up."

### Why Choose + Conclusion (slides 15–16)

**Slide 15 — Why choose ERPNext + Haritha** (2 min)
- 5 bullets: Open source / Complete code ownership / Operational readiness for hospital shift patterns / Active community / Workflow flexibility.
- Visual: `<table class="comp-table">` (4 columns: Parameter / ERPNext + Haritha / SAP / Oracle / Workday) with `.comp-highlight` column.
- Transition: "Let's wrap up."

**Slide 16 — Conclusion + Next Steps** (2 min)
- "Key Takeaways" h3 + numbered list (3 items).
  - Daily presence is the foundation for shift + leave + payroll accuracy.
  - Biometric + mobile + manual inputs converge through Auto Attendance.
  - Built-in reports + custom apps extend without core changes.
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

## 11. Concrete Example — Slide 6 (Attendance) — GOLD STANDARD

The body markup and CSS for Slide 6 must match the canonical pattern. Uses an Attendance row mockup with a status badge.

CSS excerpt:

```css
.attendance-row { display: flex; gap: var(--space-16); align-items: center; padding: var(--space-16); border: 1px solid #e2e8f0; border-radius: 8px; background: white; max-width: 720px; margin: var(--space-32) auto 0; }
.attendance-row .field { flex: 1; }
.attendance-row .field-label { font-size: 12px; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.5px; }
.attendance-row .field-value { font-size: 18px; color: var(--text); font-weight: 600; margin-top: 2px; }
.status-badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 13px; font-weight: 600; }
.status-badge.present { background: var(--primary); color: white; }
.status-badge.absent { background: var(--muted); color: white; }
.status-badge.leave  { background: var(--secondary); color: white; }
.status-badge.half   { background: var(--accent); color: white; }
```

### 11.2 Slide 12 (Daily Attendance View Table) — GOLD STANDARD

CSS excerpt for the 6-column table with status badges per row:

```css
.attendance-table { width: 100%; border-collapse: collapse; margin-top: var(--space-24); font-size: 14px; }
.attendance-table thead { background: var(--bg-even); }
.attendance-table th { padding: var(--space-12) var(--space-16); text-align: left; font-weight: 600; color: var(--secondary); text-transform: uppercase; font-size: 12px; letter-spacing: 0.5px; }
.attendance-table td { padding: var(--space-12) var(--space-16); border-top: 1px solid #e2e8f0; color: var(--text); }
.attendance-table tbody tr:hover { background: var(--bg-even); }
```

## 12. Image / Diagram Placeholder (Slide 9, 11)

Slide 9 may contain an inline tool screenshot mockup (using pure CSS); Slide 11 contains the attendance table (spec in §11.2). No external images.

## 13. Schema Flowchart (Slides 4 + 16)

Both slides 4 and 16 contain an inline SVG (740×320 viewBox). They share the same entity set + groupings but differ in annotation density.

### 13.1 Slide 4 variant — clean preview

- **6 entity boxes** (rect+text):
  - **Employee Checkin** — left (accent `#0ea5e9`, raw input layer)
  - **Auto Attendance** — middle-center (primary `#1e40af`, slightly larger to indicate process — 140×60 vs 120×40)
  - **Attendance** — right (primary, output layer)
  - **Holiday List** — top-left (secondary `#64748b`, reference)
  - **Shift Type** — top-right (secondary, reference)
  - **Attendance Request** — bottom-right (muted `#94a3b8`, optional layer)
- **2 dashed grouping rectangles** (`stroke-dasharray="4,4"`, stroke="secondary", fill="none"):
  - **Daily Tracking** — wraps Employee Checkin + Auto Attendance + Attendance (main horizontal flow across center).
  - **Reference Context** — wraps Holiday List + Shift Type (top strip).
- NO connector labels, NO field hints, NO legend box.
- Connector paths in slate (`#94a3b8`); Attendance Request connector dashed (optional/edge case).

### 13.2 Slide 16 variant — full spec

Same as Slide 4 PLUS:

- **Connector labels** (1–2 words each, font-size 11, fill="secondary"):
  - Employee Checkin → Auto Attendance: `"raw punch"`
  - Auto Attendance → Attendance: `"converts to"`
  - Auto Attendance ← Holiday List: `"matches against"`
  - Auto Attendance ← Shift Type: `"references"`
  - Attendance Request → Attendance: `"creates on approval"` (dashed connector)
  - Employee → Attendance Request: `"approved via"`
- **Field hints** below each entity name in smaller text (font-size 9, fill="muted"):
  - Employee Checkin: `[employee, time, log_type, device_id]`
  - Auto Attendance: `[shift, working_hours, late_entries, early_exits]`
  - Attendance: `[employee, attendance_date, status, shift]`
  - Holiday List: `[holiday_date, holiday_name]`
  - Shift Type: `[name, start_time, end_time, grace_period]`
  - Attendance Request: `[employee, from_date, to_date, reason, status]`
- **Legend box** (120×80 rect, white fill, slate border, bottom-left of canvas, ~translate(15,180)):
  - Color swatches: accent = `Raw input`; primary = `Process/Output`; secondary = `Reference`; muted = `Optional flow`.
  - Connector symbols: solid line = `direct`; dashed line = `optional / edge case`.

### 13.3 SVG technical specs

- viewBox: `0 0 740 320`, width="740", height="320".
- Font family: `var(--font-main)` for entity names, `var(--font-mono)` for field hints.
- Entity box dimensions: 120×40 (rect+text); Auto Attendance is 140×60 (slightly larger process node).
- Dashed grouping rectangle stroke-width: 1.5.
- Layout coordinates (approx):
  - Employee Checkin: rect at `x=40 y=140 w=120 h=40`
  - Auto Attendance: rect at `x=300 y=125 w=140 h=60`
  - Attendance: rect at `x=580 y=140 w=120 h=40`
  - Holiday List: rect at `x=40 y=30 w=120 h=40`
  - Shift Type: rect at `x=580 y=30 w=120 h=40`
  - Attendance Request: rect at `x=580 y=240 w=120 h=40`
  - Employee (ghost reference, small): rect at `x=710 y=290 w=20 h=20` (or omit — shown via connector only)
  - Daily Tracking dashed group: `x=10 y=110 w=720 h=120`
  - Reference Context dashed group: `x=10 y=10 w=720 h=80`
- Reference the existing shift-mgmt v2 SVG for visual style consistency.

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened.
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **Upload Attendance as a standalone slide** — merged into §8 narrative (bulk input pair) since functionally equivalent to Employee Attendance Tool for deck purposes.
- **Roster image placeholder (v1 slide 12)** — replaced by Daily Attendance View table (§8 slide 11 + §11.2 gold standard).

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 2.0 · Date 2026-09-14).
- **No vendor-specific data** — no employee counts, no real customer names, no company-specific metrics.
- **Use generic illustrative examples** ("Aisha Khan", "Morning 09:00–18:00", "Approved SL").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType", "Auto Attendance", "Shift Type").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content).

## 15. Quality Bar (10 checks — verify before declaring done)

1. Exactly **16** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 = Schema preview (6 entities + 2 dashed groupings only — NO connector labels, NO legend, NO field hints).
4. Slide 16 = Schema full spec (6 entities + 6 labeled connectors + legend + field hints).
5. Per-slide timings sum to ~32 minutes.
6. Both SVGs render correctly (no broken tags, no overlap).
7. Print stylesheet works.
8. No filler phrases anywhere.
9. Slide 12 = Daily Attendance View **table** mockup (6 columns × 5 rows) — NOT image placeholder, NOT roster overlay.
10. Slide 4 connector labels NOT present; Slide 16 connector labels present and read in order: "raw punch", "converts to", "matches against", "references", "creates on approval", "approved via".

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 16`.
4. **Match this prompt's slide-by-slide spec exactly.** Any drift between spec and generated HTML is a defect.
5. Only declare "done" when all 10 checks pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/attendance-management-presentation.html`

## 18. Prompt Maintenance Workflow

See `prompts/README.md` § Prompt Maintenance Workflow.

---

## Appendix A — Changelog

See `prompts/README.md` § Current Prompts table for version history.

---

## Appendix B — Lessons Applied (#151–#164)

See `prompts/README.md` § Shared Methodology (Lessons #151–#164).
