## Shift Management with ERPNext HRMS — Deck Prompt (v2)

> **Status:** Pinned canonical spec · **Version:** 1.0 · **Date:** 2026-09-04 · **Author:** Venkat Narasimha
> **Audience:** Anyone generating or auditing this presentation deck (LLM agent, technical writer, reviewer).
> **Output:** `docs/handbook/03-client/shift-management-presentation-v2.html` (single self-contained HTML).

---

## 1. Role

You are a **technical writer + front-end developer** producing a single self-contained HTML presentation that explains **shift management in ERPNext HRMS** to a general audience. You follow CMM Level 5 documentation standards in your process (not in the deck content).

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

## 8. Slide-by-Slide Specs (18 slides) — pin to current v2.html

> The exact text of every slide, visual, and speaker-notes block is locked
> to the canonical v2.html. Regenerators MUST emit byte-for-byte content
> (use the embedded snapshot in `build_deck.py`).

### Intro (slides 1–3)

**Slide 1 — Shift Management with ERPNext HRMS** (30s) — Title slide
- Subtitle: "A practical guide to planning, scheduling, attendance & reporting"
- Metadata block (bottom-right): Version 1.0 · Date 2026-09-04 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "ERPNext + HRMS Stack" / "Shift Operations" / "Custom App & Schema" / "Why ERPNext + Haritha".
- Numbers: 01 / 02 / 03 / 04.
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Transition: "Now let's look at the data model — entities and their relationships."

### Early Schema Preview (slide 4 — DUPLICATE of slide 16)

**Slide 4 — Schema: Shift Management Entities** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13).
- Above: `<strong>Architecture:</strong> How shift management entities relate across layers.`
- Below: "The relational model connects schedule templates and raw checkins to generate clean attendance records."
- Speaker notes: "Employee sits at the center. … Brief mention only. Recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the entities — why shift management matters."

### Shift Management Operations (slides 5–14)

**Slide 5 — Why shift management matters** (2 min)
- 3 bullets: unstructured spreadsheets → coverage gaps / 24/7 sectors / continuous operations require automation.
- Visual: 24h pie-style clock with 3 colored arcs (Morning / Evening / Night).
- Transition: "Let's start with the foundation: Shift Type."

**Slide 6 — Shift Type** (2 min)
- Lead paragraph: "A Shift Type is a reusable template that defines when work happens. …"
- 3 shift cards: Morning 06:00–14:00, Evening 14:00–22:00, Night 22:00–06:00.
- Transition: "But work happens at a place — that's Shift Location."

**Slide 7 — Shift Location** (1.5 min)
- 3 bullets: physical deployment boundary / prevents buddy-punching / GPS + radial tolerances.
- Visual: SVG with dashed circle "Allowed Check-in Zone (200m radius)".
- Transition: "Templates are scheduled — Shift Schedule."

**Slide 8 — Shift Schedule** (2 min)
- 3 bullets: planned working patterns / recurrences / master template for assignments.
- Visual: 7-day calendar SVG (Mon–Sun) with M/E/N/OFF colored cells.
- Transition: "Employees can also request changes — Shift Request."

**Slide 9 — Shift Request** (2 min)
- 3 bullets: employee self-service portal / multi-tier approvals / auditable lifecycle.
- Visual: horizontal flow (1. Employee → 2. Supervisor → 3. HR / System).
- Transition: "Once approved, the assignment happens — Shift Assignment."

**Slide 10 — Shift Assignment** (2 min)
- 3 bullets: maps employee to shift type / validation prevents double-booking / notifications.
- Visual: `<table class="table-mockup">` with employee / shift type / date / Active status badge.
- Transition: "Now the bulk + UI features — Schedule Assignment + Tool."

**Slide 11 — Bulk Assignment + Tool** (2.5 min)
- 3 bullets: Shift Schedule Assignment / Shift Assignment Tool / time saving.
- Visual: mini matrix mockup (Team Member × Mon-Fri with MORN/EVEN/OFF code pills).
- Transition: "What does the result look like? The Roster."

**Slide 12 — Roster** (2 min) — IMAGE PLACEHOLDER (see §12)
- Lead paragraph + 2 bullets (filters / color-coded).
- Visual: `.image-placeholder` div with "Insert roster screenshot here" text.
- Transition: "Now let's track who's actually showing up — Attendance."

**Slide 13 — Attendance + Auto-attendance** (2 min)
- 3 bullets: hardware-agnostic sync / correlates check-ins / grace-period thresholds.
- Visual: horizontal flow (1. Telemetry → 2. Match Engine → 3. Ledger).
- Transition: "All this data feeds into Reports."

**Slide 14 — Reports & Analytics** (2 min)
- 4 stat cards: Coverage Today 98.5%, Late Arrivals 4, Overtime Hours 27h, Pending Swaps 7.
- Visual: `<svg>` polyline chart inside `.chart-placeholder`, Peak Attendance (99.2%) marker.
- Transition: "What if ERPNext out-of-box doesn't fit? Custom apps."

### Custom App + Schema (slides 15–16)

**Slide 15 — Extending ERPNext with Custom Apps** (2 min)
- 3 bullets: layer cleanly above core / add custom fields + DocTypes + workflows / deploy via Git + `bench`.
- Visual: 3-layer stack (Specialized App Layer on top, HRMS Core, ERPNext & Frappe base) — accent/primary/secondary.
- Transition: "Here's how the entities relate."

**Slide 16 — Schema: Shift Management Entities** (3 min) — full spec, identical SVG to slide 4
- Above: `<strong>Architecture:</strong> How shift management entities relate across layers.`
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

## 11. Concrete Example — Slide 6 (Shift Type) — GOLD STANDARD

The body markup and CSS for Slide 6 must match the canonical v2.html. Every slide has a similar layout pattern (`.body` containing bullet list, paragraph, and one focal visual). Slide 6 specifically uses `.shift-cards` with three `.shift-card` blocks.

CSS excerpt:

```css
.shift-cards { display: flex; gap: var(--space-24); justify-content: center; margin-top: var(--space-32); }
.shift-card  { flex: 1; max-width: 220px; padding: var(--space-24) var(--space-16) var(--space-16); border-radius: 8px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border: 1px solid #e2e8f0; position: relative; }
.shift-color-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 8px 8px 0 0; }
.shift-name { font-size: 20px; font-weight: 600; color: var(--text); margin-top: var(--space-12, 12px); }
.shift-time { font-size: 16px; color: var(--primary); margin-top: var(--space-8); font-family: var(--font-mono); }
.shift-hours { font-size: 13px; color: var(--secondary); margin-top: 4px; }
```

## 12. Roster Image Placeholder (Slide 12)

Slide 12 MUST contain exactly this placeholder block:

```html
<div class="image-placeholder" style="border: 2px dashed #94a3b8; padding: 48px 32px; text-align: center; color: #64748b; margin-top: 32px;">
  [Insert roster screenshot here]
  <br><small>Roster view — calendar of employee shifts</small>
</div>
```

## 13. Schema Flowchart (Slides 4 and 16)

Both slides 4 and 16 contain the **same** inline SVG (740×320 viewBox). The SVG must include:

- 9 entity boxes (rect+text): Holiday List (top-center, slate), Employee (center, primary), Attendance (bottom-center, slate), Shift Type / Shift Schedule / Shift Location (right column, primary), Shift Request / Shift Assignment / Employee Checkin (left column, accent).
- Connector paths in slate (`#94a3b8`), one dashed line for indirect relation.
- Reference the existing slide-4 / slide-16 SVG in `docs/handbook/03-client/shift-management-presentation-v2.html` for exact byte-for-byte layout.

**Positioning (rough):** Employee at center (370, 150). Holiday List top-center. Attendance bottom-center. Shift Type / Schedule / Location on the right column. Shift Request / Assignment / Checkin on the left column.

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim content is "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened. The deck does NOT talk about "Phase 6 docs / Tier 6 compliance".
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 1.0 · Date 2026-09-04).
- **No Haritha-specific data** — no employee counts, no company-specific metrics, no real customer names.
- **Use generic illustrative examples** ("Morning shift 06:00-14:00", "200m radius").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType: a database table in ERPNext").
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
9. Roster image placeholder present (slide 12).
10. Schema flowchart present with all 9 entities + relations (slides 4 and 16).

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 18`.
4. **Match the canonical v2.html byte-for-byte** — `prompts/build_deck.py` embeds the canonical snapshot and emits it directly. Any drift is a defect.
5. Only declare "done" when all 10 checks + byte-for-byte match pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/shift-management-presentation-v2.html`

## 18. Regeneration Workflow

`prompts/build_deck.py` is the single regenerator:

1. Validates that v2.md describes 18 slides with Schema at #4 and #16.
2. Base64-decodes the embedded canonical snapshot.
3. Writes the bytes verbatim to the output path.

Re-running `python3 prompts/build_deck.py` is idempotent and produces a byte-for-byte match with the committed v2.html. To update the deck:

1. Edit `docs/handbook/03-client/shift-management-presentation-v2.html` manually (Venkat-approved copy).
2. Re-embed its base64 in `prompts/build_deck.py` (one-line shell helper: `base64 -w0 path/to/v2.html`).
3. Update the slide-by-slide spec in v2.md to match the new content.
4. Commit all three together.

---

## Appendix A — Changelog

- **v2.0** (2026-09-04) — Initial v2 release.
  - Added Schema duplicate at slide 4 (early preview).
  - Renumbered slides 4–13 → 5–14.
  - Added slides 15 (Extending ERPNext) and 16 (Schema full spec).
  - Renumbered slides 16–17 → 17–18.
  - Counter changed from `N / 17` to `N / 18`.
  - Slide 1 metadata: Version 1.0, Date 2026-09-04, Audience General.
  - Concrete gold standard: Slide 6 (Shift Type).

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
