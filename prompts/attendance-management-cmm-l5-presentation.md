## Attendance Management with ERPNext HRMS — Deck Prompt (v1)

> **Status:** Pinned canonical spec · **Version:** 1.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
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

Produce an **18-slide** self-contained HTML presentation explaining attendance management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

**Structural pattern (mirrors shift-mgmt v2):** the Schema: Attendance Entities slide appears **twice** — early (slide 4) and at its original position (slide 16). The early copy previews the architecture so the audience has a mental model before they see the entities in depth later.

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

**Slide 1 — Attendance Management with ERPNext HRMS** (30s) — Title slide
- Subtitle: "A practical guide to daily tracking, auto-attendance, regularisation & reporting"
- Metadata block (bottom-right): Version 1.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "HRMS + Attendance Stack" / "Daily Tracking Methods" / "Auto-Attendance Engine" / "Reports & Edge Cases".
- Numbers: 01 / 02 / 03 / 04.
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Transition: "Now let's look at the data model — entities and their relationships."

### Early Schema Preview (slide 4 — DUPLICATE of slide 16)

**Slide 4 — Schema: Attendance Entities** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13).
- Above: `<strong>Architecture:</strong> How attendance management entities relate across layers.`
- Below: "The relational model converts raw check-ins into a clean daily status record."
- Speaker notes: "Employee sits at the center. … Brief mention only. Recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the entities — why attendance management matters."

### Attendance Management Operations (slides 5–14)

**Slide 5 — Why attendance management matters** (2 min)
- 3 bullets: manual registers lose data and drift / multiple input sources (biometric, RFID, mobile) / automation reduces disputes and payroll errors.
- Visual: 24h pie-style clock with 3 colored arcs (Morning / Evening / Night).
- Transition: "Let's start with the foundation: the daily record — Attendance."

**Slide 6 — Attendance (the daily record)** (2 min)
- Lead paragraph: "An Attendance row in ERPNext captures one employee's status for one day. …"
- Status table with badges: **Present** / **Absent** / **On Leave** / **Half Day**.
- Transition: "But the day starts with a raw punch — Employee Checkin."

**Slide 7 — Employee Checkin (raw IN/OUT punch)** (2 min)
- 3 bullets: each row is a single timestamped event (IN or OUT) / captured via biometric, RFID, mobile app or GPS / written to a single append-only log table.
- Visual: SVG with dashed circle "Allowed Check-in Zone (200m radius)" and a phone + reader icon.
- Transition: "Raw punches don't become attendance automatically — Auto Attendance does that."

**Slide 8 — Auto Attendance (the conversion engine)** (2 min)
- 3 bullets: scheduled background job (cron, typically every few minutes) / pairs the earliest IN and latest OUT per employee per shift / writes Attendance rows only when check-ins fall within shift windows.
- Visual: horizontal flow (1. Raw Checkins → 2. Auto Attendance Job → 3. Attendance Row).
- Transition: "Sometimes HR must mark attendance by hand — the Employee Attendance Tool."

**Slide 9 — Employee Attendance Tool (bulk marking)** (2 min)
- 3 bullets: HR admin form to mark an entire department for a date range / supports Present, Absent, Half Day and On Leave per employee / bypasses biometric dependency for sites without hardware.
- Visual: `.image-placeholder`-style mock grid (Department × Date × Status pills).
- Transition: "For large historical imports, use Upload Attendance."

**Slide 10 — Upload Attendance (bulk import)** (2 min)
- 3 bullets: CSV / Excel upload via the standard ERPNext Data Import Tool / columns map to Employee, Date, Status, Shift, Leave Type / validation rejects duplicates and out-of-range dates.
- Visual: `<table class="table-mockup">` with sample CSV columns and one error row highlighted.
- Transition: "Employees can also correct their own record — Attendance Request."

**Slide 11 — Attendance Request (employee regularisation)** (2 min)
- 3 bullets: employee self-service for missed check-ins / workflow approval routed to Reporting Manager then HR / auditable lifecycle with reason, before/after timestamps, status.
- Visual: horizontal flow (1. Employee → 2. Reporting Manager → 3. HR).
- Transition: "Attendance overlays the roster — Roster Integration."

**Slide 12 — Roster Integration** (2 min) — IMAGE PLACEHOLDER (see §12)
- Lead paragraph + 2 bullets (planned vs actual overlay / colour-coded exceptions).
- Visual: `.image-placeholder` div with "Insert attendance overlay screenshot here" text.
- Transition: "Once recorded, attendance flows through an approval workflow."

**Slide 13 — Attendance Workflow & Approval** (2 min)
- 3 bullets: status transitions driven by Attendance Request + Leave Application / auto-attendance writes skip approval and feed payroll directly / manager dashboard highlights anomalies (no show, late-in, early-out).
- Visual: 4-stage flow (Check-in → Auto Attendance → Manager Review → Payroll-ready).
- Transition: "All this data feeds into Reports."

**Slide 14 — Reports & Analytics** (2 min)
- 4 stat cards: Present Today 96%, Late Arrivals 4, Half Days 2, Pending Regularisations 3.
- Visual: `<svg>` polyline chart inside `.chart-placeholder`, Peak Attendance marker.
- Transition: "What if ERPNext out-of-box doesn't fit? Custom apps."

### Custom App + Schema (slides 15–16)

**Slide 15 — Extending ERPNext with Custom Apps** (2 min)
- 3 bullets: layer cleanly above core / add custom fields + DocTypes + workflows / deploy via Git + `bench`.
- Visual: 3-layer stack (Specialized App Layer on top, HRMS Core, ERPNext & Frappe base) — accent/primary/secondary.
- Transition: "Here's how the entities relate."

**Slide 16 — Schema: Attendance Entities** (3 min) — full spec, identical SVG to slide 4
- Above: `<strong>Architecture:</strong> How attendance management entities relate across layers.`
- Below: same caption as slide 4.
- Speaker notes: "Employee sits at the center. … Transition: Why choose ERPNext + Haritha for your deployment."

### Why Choose + Conclusion (slides 17–18)

**Slide 17 — Why choose ERPNext + Haritha** (2 min)
- 5 bullets: Open source / Complete code ownership / Clinical operational readiness / Active community / Workflow flexibility.
- Visual: `<table class="comp-table">` (4 columns: Parameter / ERPNext + Haritha / SAP / Oracle / Workday) with `.comp-highlight` column.
- Transition: "Let's wrap up."

**Slide 18 — Conclusion + Next Steps** (2 min)
- "Key Takeaways" h3 + numbered list (3 items).
- "Next Steps" h4 + 3 bullets (demo sandbox `demo.example.com` / pilot 4-8 weeks / architecture review).
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

## 11. Concrete Example — Slide 6 (Attendance) — GOLD STANDARD

The body markup and CSS for Slide 6 must use the canonical status badge / table pattern. Every slide has a similar layout pattern (`.body` containing a lead paragraph, a status table, and one focal visual). Slide 6 specifically uses `.status-table` with `.status-badge` pills.

CSS excerpt:

```css
.status-table { width: 100%; border-collapse: collapse; margin-top: var(--space-32); box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border-radius: 8px; overflow: hidden; }
.status-table th { background: var(--primary); color: white; padding: var(--space-16); text-align: left; font-weight: 600; font-size: 15px; }
.status-table td { padding: var(--space-16); border-top: 1px solid #e2e8f0; font-size: 15px; color: var(--text); }
.status-badge { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 13px; font-weight: 600; }
.status-badge.present  { background: #dcfce7; color: #166534; }
.status-badge.absent   { background: #fee2e2; color: #991b1b; }
.status-badge.on-leave { background: #fef3c7; color: #92400e; }
.status-badge.half-day { background: #dbeafe; color: #1e40af; }
```

## 12. Roster Integration Image Placeholder (Slide 12)

Slide 12 MUST contain exactly this placeholder block:

```html
<div class="image-placeholder" style="border: 2px dashed #94a3b8; padding: 48px 32px; text-align: center; color: #64748b; margin-top: 32px;">
  [Insert attendance overlay screenshot here]
  <br><small>Roster calendar with attendance overlay — planned vs actual</small>
</div>
```

## 13. Schema Flowchart (Slides 4 and 16)

Both slides 4 and 16 contain the **same** inline SVG (740×320 viewBox). The SVG must include:

- 5–6 entity boxes (rect+text): **Employee** (center, primary), **Attendance** (bottom-center, slate), **Employee Checkin** (left, accent — raw punches), **Auto Attendance** (between Employee Checkin and Attendance, accent — processing node), **Holiday List** (top-center, slate — reference), **Attendance Request** (right, accent — optional regularisation flow).
- Connector paths in slate (`#94a3b8`), one dashed line for the optional Attendance Request path.
- Reference the slide-4 / slide-16 SVG in `docs/handbook/03-client/shift-management-presentation-v2.html` for byte-for-byte layout style (same canvas size, same font, same colour palette).

**Positioning (rough):** Employee at center (370, 150). Holiday List top-center (~370, 50). Attendance bottom-center (~370, 270). Employee Checkin left (~140, 150). Auto Attendance between (~260, 210). Attendance Request right (~600, 150).

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim content is "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened. The deck does NOT talk about "Phase 6 docs / Tier 6 compliance".
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 1.0 · Date 2026-09-14).
- **No Haritha-specific data** — no employee counts, no company-specific metrics, no real customer names.
- **Use generic illustrative examples** ("Morning shift 06:00–14:00", "200m radius check-in zone", "Daily status: Present").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType: a database table in ERPNext", "Employee Checkin: a single IN or OUT punch record", "Auto Attendance: a background job that converts raw checkins into Attendance rows").
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
9. Roster Integration image placeholder present (slide 12).
10. Schema flowchart present with all 5–6 attendance entities + relations (slides 4 and 16): Employee, Attendance, Employee Checkin, Auto Attendance, Holiday List, Attendance Request.

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 18`.
4. **Match the canonical v2.html byte-for-byte** — `prompts/build_deck.py` embeds the canonical snapshot and emits it directly. Any drift is a defect.
5. Only declare "done" when all 10 checks + byte-for-byte match pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/attendance-management-presentation.html`

## 18. Regeneration Workflow

`prompts/build_deck.py` is the single regenerator:

1. Validates that v1.md describes 18 slides with Schema at #4 and #16.
2. Base64-decodes the embedded canonical snapshot.
3. Writes the bytes verbatim to the output path.

Re-running `python3 prompts/build_deck.py` is idempotent and produces a byte-for-byte match with the committed v1.html. To update the deck:

1. Edit `docs/handbook/03-client/attendance-management-presentation.html` manually (Venkat-approved copy).
2. Re-embed its base64 in `prompts/build_deck.py` (one-line shell helper: `base64 -w0 path/to/v1.html`).
3. Update the slide-by-slide spec in v1.md to match the new content.
4. Commit all three together.

---

## Appendix A — Changelog

- **v1.0** (2026-09-14) — Initial release based on shift-mgmt v2 pattern.
  - Added Schema duplicate at slide 4 (early preview).
  - Renumbered concept slots 4–13 → 5–14 (Why-it-matters → Reports).
  - Added slide 15 (Extending ERPNext) and slide 16 (Schema full spec).
  - Renumbered closing slots 16–17 → 17–18.
  - Counter `N / 18` matches shift-mgmt v2.
  - Slide 1 metadata: Version 1.0, Date 2026-09-14, Audience General.
  - Six attendance-specific concept slides (Attendance, Employee Checkin, Auto Attendance, Employee Attendance Tool, Upload Attendance, Attendance Request).
  - Concrete gold standard: Slide 6 (Attendance) with status badge / table pattern.

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
