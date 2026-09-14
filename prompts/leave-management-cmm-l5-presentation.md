## Leave Management with ERPNext HRMS — Deck Prompt (v2)

> **Status:** Active spec · **Version:** 2.0 · **Date:** 2026-09-14 · **Author:** Venkat Narasimha
> **Audience:** Anyone generating or auditing this presentation deck (LLM agent, technical writer, reviewer).
> **Output:** `docs/handbook/03-client/leave-management-presentation.html` (single self-contained HTML).

---

## 1. Role

You are a **technical writer + front-end developer** producing a single self-contained HTML presentation that explains **leave management in ERPNext HRMS** to a general audience. You follow CMM Level 5 documentation standards in your process (not in the deck content).

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

Produce a **22-slide** self-contained HTML presentation explaining leave management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

**Structural choices (v2.0):**

- Leave is the most entity-rich module of the six (11+ concepts), so 22 slides (vs 16–18 for org/attendance/lifecycle) reflects actual content density.
- 3-layer schema: Config (top) → Policy (middle) → Action (bottom), with Employee + Leave Approver at center.
- Slide 12 = inline SVG leave approval workflow (Employee → Leave Approver → Approved/Rejected branch).
- "Why choose" framing absorbed into conclusion slide (matches attendance v2.1 + org-mgmt v2.0 + lifecycle v2.0 pattern).
- Schema full spec at slide 21 (immediately before Conclusion).

## 4. Time Budget

- **Total: 40 minutes** (32 min content + 8 min Q&A).
- Per-slide timings sum to ~32 min — speaker can compress/expand as needed.
- See §8 for per-slide timings.

## 5. Output Specs

- **Format:** single `.html` file, fully self-contained (inline CSS, no external assets, no JavaScript libraries).
- **Slides:** exactly **22**, each `<section class="slide" id="slide-N">`.
- **Counter:** every slide shows `N / 22` (not 21, not 23 — must match exactly).
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
| `--primary` | `#1e40af` | Deep blue (titles, config layer) |
| `--secondary` | `#64748b` | Slate (speaker notes, action layer) |
| `--accent` | `#0ea5e9` | Sky (policy layer) |
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

## 7. Slide Template (apply uniformly to all 22 slides)

Every slide MUST include:

1. `<div class="slide-number">N / 22</div>`
2. `<h2 class="slide-title">…</h2>`
3. `<div class="body">… main content (≤100 words), one focal visual …</div>`
4. `<aside class="speaker-notes">…</aside>` — hidden by default, toggle with `S` key.
5. **Transition note** (1 sentence) — included inside speaker notes.

## 8. Slide-by-Slide Specs (22 slides)

### Intro (slides 1–3)

**Slide 1 — Leave Management with ERPNext HRMS** (30s) — Title slide
- Subtitle: "Configurable leave policies, approvals, and audit trails for hospital operations"
- Metadata block (bottom-right): Version 2.0 · Date 2026-09-14 · Audience General (HR, Operations, Evaluators).
- Layout: `title-wrapper` flex column, `metadata-block` bottom-right.
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- 4-card grid. Card titles: "HRMS + Leave Stack" / "Leave Types & Policies" / "Allocation & Application" / "Edge Cases & Compliance".
- Numbers: 01 / 02 / 03 / 04.
- Transition: "First, a quick foundation."

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- 4 bullets: open-source Frappe/ERPNext / ~12 business domains / HRMS module / 5,000+ contributors.
- Visual: layered stack diagram (HRMS top, ERPNext mid, Frappe bottom).
- Transition: "Now let's look at the data model — entities and their relationships."

### Early Schema Preview (slide 4 — clean preview, no labels)

**Slide 4 — Schema: Leave Entities** (1.5 min) — EARLY PREVIEW
- Inline SVG entity-relationship diagram (740×320 viewBox; see §13 § Schema Flowchart § Slide 4 variant).
- Above: `<strong>Architecture:</strong> How leave entities relate across config, policy, and action layers.`
- Below: "The relational model layers configuration (types + periods + holidays), policy (bundles + assignments + allocations), and action (applications + ledger entries) around the Employee master."
- Speaker notes: "Three layers: Config at top (Holiday List, Leave Type, Leave Period), Policy in the middle (Leave Policy, Policy Assignment, Allocation), Action at the bottom (Leave Application, Leave Ledger Entry). Employee at the center with Leave Approver as a connector to Employee. Brief mention only. Recap: Schema shown earlier in the deck."
- Transition: "Now that you've seen the entities — why leave management matters."

### Leave Management Operations (slides 5–17)

**Slide 5 — Why leave management matters** (2 min)
- 3 bullets: manual registers create disputes / multiple leave types per policy / audit trail mandatory for compliance / accrual + encashment add complexity.
- Visual: bar chart SVG showing absence dispute resolution cases per year (descending when on a leave system).
- Transition: "Let's start with the foundation: the holiday calendar."

**Slide 6 — Holiday List (calendar foundation)** (2 min)
- Lead paragraph: "A Holiday List is the calendar of organizational + statutory holidays for a Company. It's the foundation for leave date calculations and Attendance 'On Leave' auto-creation."
- 3 bullets: org-level + statutory holidays / date range (from_date, to_date) / referenced by Attendance + Leave Module.
- Visual: calendar grid SVG (3 months × 4 weeks) with holidays marked.
- Transition: "Holiday Lists set the context — next, the kinds of leave available."

**Slide 7 — Leave Type (kinds of leave + rules)** (2 min)
- Lead paragraph: "A Leave Type defines a kind of leave (Sick, Casual, Privilege, Earned, Compensatory, etc.) with its own rules: paid/unpaid, carry-forward, encashable, max continuous days."
- 3 bullets: rules-based config (is_paid, carry_forward, encashable, max_continuous_days) / earned vs non-earned categories / max_days_allowed.
- Visual: 4 type card mockups (Sick 6/yr, Casual 12/yr, Earned 24/yr + carry, Compensatory).
- Transition: "Types need a cycle they live in — Leave Period."

**Slide 8 — Leave Period (annual cycle)** (2 min)
- Lead paragraph: "A Leave Period bounds the annual leave cycle (from_date to to_date). Allocations and applications are scoped to a period."
- 3 bullets: from_date / to_date / period name (e.g., "FY 2025–2026").
- Visual: timeline SVG (Jan 2026 — Dec 2026) with cycle indicator.
- Transition: "Types bundle into policies — Leave Policy."

**Slide 9 — Leave Policy (bundle of Leave Types + allocation rules)** (2 min)
- Lead paragraph: "A Leave Policy bundles multiple Leave Types with allocation rules. One Leave Policy per role-group is a common pattern (e.g., 'Staff Nurse Policy' = 12 CL + 6 SL + 24 EL)."
- 3 bullets: policy name / included Leave Types with allocation per type / assigned via Leave Policy Assignment.
- Visual: policy card mockup (Staff Nurse Policy: Casual 12, Sick 6, Earned 24, Comp-off 5).
- Transition: "Policies need to bind to employees — Leave Policy Assignment."

**Slide 10 — Leave Policy Assignment (per-employee binding)** (2 min)
- Lead paragraph: "A Leave Policy Assignment binds a specific Leave Policy + Leave Period to a specific Employee. One Assignment per (employee, period) pair typically."
- 3 bullets: employee + policy + period / effective_date / optionally role/grade filter.
- Visual: assignment form mockup (Employee A → Staff Nurse Policy → FY 2025-2026).
- Transition: "Assignment drives allocation — Leave Allocation."

**Slide 11 — Leave Allocation (granted days per type)** (2 min)
- Lead paragraph: "A Leave Allocation is the granted count of leaves for an Employee per Leave Type per Leave Period. Auto-generated when Leave Policy Assignment is created."
- 3 bullets: employee + leave_type + leave_period / total_leaves_allocated / supports carry-forward from prior period.
- Visual: allocation breakdown bar chart (Casual 12 + Sick 6 + Earned 24 = 42 leaves/year).
- Transition: "Here's the workflow when an employee actually requests leave."

**Slide 12 — Leave Approval Workflow (inline SVG)** (2 min)
- Lead paragraph: "When an employee submits a Leave Application, it routes to the Employee.leave_approver (a single User). Approval flips status to 'Approved' and posts to the Leave Ledger Entry."
- Inline SVG flowchart: Employee → [Submit Leave Application] → Leave Approver → {Approved → posts to Ledger / Rejected → notifies Employee}.
- 4 boxes: Employee (left), Leave Application (middle-left), Leave Approver (middle-right), Result branch (Approved / Rejected).
- 3 arrows with labels: "submits", "approved via", "posts" / "notifies".
- Visual: `<div class="approval-flow">` with 4 boxes arranged left-to-right.
- Transition: "The application itself — how it's structured."

**Slide 13 — Leave Application (employee request)** (2 min)
- Lead paragraph: "A Leave Application is the per-request record. It captures employee + leave_type + from_date + to_date + reason + half-day flag + supporting attachment."
- 3 bullets: per-request lifecycle (Open / Approved / Rejected / Cancelled) / half-day support / attachment for medical certificates.
- Visual: form mockup (Employee A, Sick Leave, 2025-12-01 → 2025-12-03, Half Day: No, Reason: Flu).
- Transition: "Bulk allocations via policy — but sometimes you need a control panel."

**Slide 14 — Leave Control Panel (bulk actions)** (2 min)
- Lead paragraph: "The Leave Control Panel is an admin tool for bulk-allocating leave across multiple employees at once, applying a policy to a department or grade in one action."
- 3 bullets: bulk assign by department / grade / location / live balance preview.
- Visual: control panel mockup (Department filter + Policy selector + Preview table + Apply button).
- Transition: "What if OT hours were converted to leave — Compensatory Leave Request."

**Slide 15 — Compensatory Leave Request** (2 min)
- Lead paragraph: "A Compensatory Leave Request converts extra hours worked (e.g., overtime, holiday duty) into leave credit. Approval posts to Leave Allocation as additional balance."
- 3 bullets: source: overtime / holiday duty / manual / approver workflow / addition to balance on approval.
- Visual: form mockup (Employee A, OT for 2025-11-15, 4 hours, Requesting 0.5 day Comp-off).
- Transition: "Exit side of leave — encashment."

**Slide 16 — Leave Encashment** (2 min)
- Lead paragraph: "Leave Encashment converts unused leave balance to cash at exit (or optionally during employment, per Leave Type rules). Pairs with Employee Separation."
- 3 bullets: encashment_date + leave_type + amount / payout via Salary Slip or Additional Salary / tied to Leave Ledger Entry.
- Visual: encashment form mockup (Employee A, Earned Leave, 10 days unutilized, Payout: 10 × daily rate).
- Transition: "Date-blocked leaves — Leave Block List."

**Slide 17 — Leave Block List** (2 min)
- Lead paragraph: "A Leave Block List prevents leave applications on specified dates (e.g., audit week, statutory event, busy season). Overlap with Holiday List gives full coverage."
- 3 bullets: block_dates field (date ranges) / applies to all or specific Leave Types / overlap with Holiday List.
- Visual: calendar SVG with blocked dates shaded red.
- Transition: "All this data leaves an audit trail — Leave Ledger Entry."

**Slide 18 — Leave Ledger Entry (append-only audit trail)** (2 min)
- Lead paragraph: "A Leave Ledger Entry is an append-only audit record of every leave movement: allocation, application, encashment. The source-of-truth for balance calculation."
- 3 bullets: append-only / per (employee, leave_type, period) / transaction_type: Allocation / Application / Encashment.
- Visual: ledger table mockup (Date / Type / Ref / Debit / Credit / Balance for one employee).
- Transition: "What does the data give us — Reports & Analytics."

### Custom App + Schema + Conclusion (slides 19–22)

**Slide 19 — Reports & Analytics** (2 min)
- 3 cards: Leave Balance (built-in, per employee) / Leave Ledger Audit (custom) / Leave Utilization by Department (custom).
- Visual: bar chart SVG showing utilization by department (Nurses, Doctors, Admin, Support).
- Transition: "What if out-of-box doesn't fit? Custom apps."

**Slide 20 — Extending ERPNext with Custom Apps** (2 min)
- 3 bullets: layer cleanly above core / add custom fields + DocTypes + workflows / deploy via Git.
- Visual: 3-layer stack (Specialized App Layer on top, HRMS Core, ERPNext & Frappe base) — accent/primary/secondary.
- Transition: "Here's the full schema with relationship labels and field hints."

**Slide 21 — Schema: Leave Entities (full spec)** (3 min) — full spec, ENHANCED over slide 4 (see §13 § Schema Flowchart § Slide 21 variant)
- Above: `<strong>Architecture:</strong> How leave entities relate across config, policy, and action layers — with relationship labels, field hints, and a legend for color and connector meanings.`
- Below: "Configuration defines what leave is available. Policy binds available leave to employees and grants allocations. Action records every leave movement as an immutable ledger entry."
- Speaker notes: "Walk the audience through the 3-layer structure top-to-bottom. Config: Holiday List, Leave Type, Leave Period. Policy: Leave Policy, Leave Policy Assignment, Leave Allocation. Action: Leave Application, Leave Ledger Entry. Employee sits at center with Leave Approver as the connector role."
- Transition: "Let's wrap up."

**Slide 22 — Conclusion + Why choose + Next Steps** (2 min)
- "Key Takeaways" h3 + numbered list (3 items).
  - Leave is policy-driven + audit-tracked (not just a register).
  - 3-layer architecture: Config → Policy → Action.
  - Allocations + applications + encashments post to immutable ledger.
- "Why choose ERPNext + Haritha" h4 (absorbed from standalone slide):
  - 3 bullets (concise): Open source + code ownership / Hospital-specific leave patterns (e.g., nurse rotation, medical certificates) / Active community.
- "Next Steps" h4 + 3 bullets (demo sandbox `demo.example.com` / pilot 4–8 weeks / architecture review).
- Transition: "Thank you and welcome to the Q&A."

## 9. Slide Template HTML

```html
<section class="slide" id="slide-N">
  <div class="slide-number">N / 22</div>
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

### 11.1 Slide 7 (Leave Type cards) — GOLD STANDARD

CSS excerpt for the 4-card leave type mockup:

```css
.leave-type-cards { display: flex; gap: var(--space-16); margin-top: var(--space-32); flex-wrap: wrap; justify-content: center; }
.leave-type-card { flex: 1; min-width: 140px; max-width: 180px; padding: var(--space-24) var(--space-16); border-radius: 8px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border: 1px solid #e2e8f0; text-align: center; position: relative; }
.leave-type-card .type-name { font-size: 16px; font-weight: 600; color: var(--text); }
.leave-type-card .type-quota { font-size: 28px; font-weight: 700; color: var(--primary); margin: var(--space-12) 0; }
.leave-type-card .type-note { font-size: 12px; color: var(--secondary); }
```

### 11.2 Slide 12 (Leave Approval Workflow SVG) — GOLD STANDARD

CSS excerpt for the 4-box approval flow with branching:

```css
.approval-flow { display: flex; gap: var(--space-16); align-items: center; margin-top: var(--space-32); flex-wrap: wrap; justify-content: center; }
.flow-step { flex: 1; min-width: 140px; max-width: 180px; padding: var(--space-24) var(--space-16); border-radius: 8px; background: var(--bg-even); border: 1px solid #e2e8f0; text-align: center; }
.flow-step.decision { background: #fefce8; border-color: #fde047; }
.flow-step.outcome-approved { background: #f0fdf4; border-color: #86efac; }
.flow-step.outcome-rejected { background: #fef2f2; border-color: #fca5a5; }
.flow-arrow { font-size: 24px; color: var(--muted); }
.flow-step .step-label { font-size: 12px; text-transform: uppercase; color: var(--secondary); letter-spacing: 0.5px; }
.flow-step .step-action { font-size: 16px; font-weight: 600; color: var(--text); margin-top: var(--space-4); }
```

## 12. Image / Diagram Placeholder (Slides 6, 7, 13, 14, 15, 16, 17)

Slides with inline form/timeline mockups use pure CSS (no external images).

## 13. Schema Flowchart (Slides 4 + 21)

Both slides 4 and 21 contain an inline SVG (740×320 viewBox). They share the same entity set + groupings but differ in annotation density.

### 13.1 Slide 4 variant — clean preview

- **8 entity boxes** (rect+text) arranged in **3 layers top-down**:
  - **Config layer (top, primary `#1e40af`)**:
    - **Holiday List** — top-left
    - **Leave Type** — top-center (slightly larger, 140×50 — it's the most important config)
    - **Leave Period** — top-right
  - **Policy layer (middle, accent `#0ea5e9`)**:
    - **Leave Policy** — mid-left
    - **Leave Policy Assignment** — mid-center (slightly wider, 160×40 — binds employee + policy + period)
    - **Leave Allocation** — mid-right
  - **Action layer (bottom, secondary `#64748b`)**:
    - **Leave Application** — bottom-left
    - **Leave Ledger Entry** — bottom-right (slightly wider, 150×40 — multi-field transaction record)
  - **Employee** — center (primary, 140×60 — master anchor)
- **3 dashed grouping rectangles** (`stroke-dasharray="4,4"`, stroke="secondary", fill="none"):
  - **Config** — wraps Holiday List + Leave Type + Leave Period (top strip).
  - **Policy** — wraps Leave Policy + Leave Policy Assignment + Leave Allocation (middle strip).
  - **Action** — wraps Leave Application + Leave Ledger Entry (bottom strip).
- Leave Approver is a **connector label reference** on Employee — no separate box (it's a User role, not a doc).
- NO connector labels, NO field hints, NO legend box.
- Connector paths in slate (`#94a3b8`); directional flow top-down (Config → Policy → Action), with Employee + Leave Approver as the central anchor for Action items.

### 13.2 Slide 21 variant — full spec

Same as Slide 4 PLUS:

- **Connector labels** (1–2 words each, font-size 11, fill="secondary"):
  - Leave Type → Leave Policy: `"bundled in"`
  - Leave Period → Leave Policy: `"scopes"`
  - Leave Policy → Leave Policy Assignment: `"applied via"`
  - Leave Policy Assignment → Leave Allocation: `"grants"`
  - Leave Policy Assignment → Employee: `"binds"`
  - Employee → Leave Application: `"submits"`
  - Leave Application → Leave Approver (on Employee): `"approved via"`
  - Leave Application → Leave Ledger Entry: `"posts allocation / application / encashment"` (multi-segment label)
  - Leave Application ← Holiday List: `"excludes holidays"`
- **Field hints** below each entity name in smaller text (font-size 9, fill="muted"):
  - Holiday List: `[holiday_date, holiday_name]`
  - Leave Type: `[name, max_continuous_days, carry_forward, encashable]`
  - Leave Period: `[from_date, to_date]`
  - Leave Policy: `[title, leave_types]`
  - Leave Policy Assignment: `[employee, leave_policy, leave_period, assignment_date]`
  - Leave Allocation: `[employee, leave_type, leave_period, total_leaves_allocated]`
  - Leave Application: `[employee, leave_type, from_date, to_date, status]`
  - Leave Ledger Entry: `[employee, leave_type, transaction_type, amount]`
- **Legend box** (120×80 rect, white fill, slate border, bottom-left of canvas, ~translate(15,180)):
  - Color swatches: primary = `Config / Master`; accent = `Policy`; secondary = `Action`.
  - Connector symbols: solid line = `direct / lifecycle`; dashed line = `reference / exclusion`.

### 13.3 SVG technical specs

- viewBox: `0 0 740 320`, width="740", height="320".
- Font family: `var(--font-main)` for entity names, `var(--font-mono)` for field hints.
- Entity box dimensions: 120×40 standard; Leave Type is 140×50 (most important config); Leave Policy Assignment is 160×40 (wider for 3-field binding); Leave Ledger Entry is 150×40 (wider for multi-field transaction); Employee is 140×60 (master anchor).
- Dashed grouping rectangle stroke-width: 1.5.
- Layout coordinates (approx):
  - Config layer (top):
    - Holiday List: rect at `x=40 y=30 w=120 h=40`
    - Leave Type: rect at `x=295 y=25 w=140 h=50`
    - Leave Period: rect at `x=560 y=30 w=120 h=40`
  - Middle (Employee master + Policy row):
    - Employee: rect at `x=295 y=130 w=140 h=60` (centered)
    - Leave Policy: rect at `x=30 y=210 w=120 h=40` (mid-left in Policy strip)
    - Leave Policy Assignment: rect at `x=200 y=210 w=160 h=40` (Policy center)
    - Leave Allocation: rect at `x=420 y=210 w=140 h=40` (mid-right)
  - Action layer (bottom):
    - Leave Application: rect at `x=40 y=270 w=140 h=40`
    - Leave Ledger Entry: rect at `x=470 y=270 w=170 h=40`
  - Config dashed group: `x=10 y=10 w=720 h=85`
  - Policy dashed group: `x=10 y=190 w=720 h=80`
  - Action dashed group: `x=10 y=255 w=720 h=70`
- Reference the existing shift-mgmt v2 SVG for visual style consistency.

## 14. Content Constraints (CMM L5 — Lessons #151–#164)

### Dropped from v1

- **Stale 2026-04-XX dates** — do not claim "up to date as of April 2026".
- **Stale "Phase 6 / Tier 6" content** — handbook/ rename happened.
- **Stale `2026-08-29` MTM/outage mentions** — use accurate dates only.
- **Leave workflow image placeholder (v1 slide 12)** — replaced by inline SVG approval flow (§11.2 gold standard).
- **"Why choose ERPNext + Haritha" as standalone slide** — absorbed into Conclusion slide 22 (matches attendance v2.1 + org-mgmt v2.0 + lifecycle v2.0 pattern).

### Required

- **"Up to date?" means BOTH structure AND metadata.** Cover slide 1 metadata block (Version 2.0 · Date 2026-09-14).
- **No vendor-specific data** — no employee counts, no real customer names, no company-specific metrics.
- **Use generic illustrative examples** ("Employee A", "Staff Nurse Policy: 12 CL + 6 SL + 24 EL", "FY 2025–2026").
- **Tone:** friendly but professional, never salesy.
- **Per-slide body:** ≤100 words.
- **One focal point per slide** — don't cram.
- **Define jargon on first use** ("DocType", "Leave Ledger Entry", "Encashment").
- **No filler phrases** ("It's important to note that...", "As we can see...", "In this slide we will...").
- **Tight, professional, clean** — no emoji in the deck (slide content).

## 15. Quality Bar (10 checks — verify before declaring done)

1. Exactly **22** slides present in correct order.
2. Each slide has title, body (≤100 words), visual, speaker notes.
3. Slide 4 = Schema preview (8 entities + 3 dashed groupings — NO connector labels, NO legend, NO field hints).
4. Slide 21 = Schema full spec (8 entities + 9 labeled connectors + legend + field hints).
5. Per-slide timings sum to ~32 minutes.
6. Both SVGs render correctly (no broken tags, no overlap).
7. Print stylesheet works.
8. No filler phrases anywhere.
9. Slide 12 = Leave Approval Workflow **inline SVG flowchart** (Employee → Leave Application → Leave Approver → Approved/Rejected branch) — NOT image placeholder.
10. Slide 4 connector labels NOT present; Slide 21 connector labels present and read in order: "bundled in", "scopes", "applied via", "grants", "binds", "submits", "approved via", "posts allocation / application / encashment", "excludes holidays".

## 16. Self-Review Step (MANDATORY)

Before declaring the generated HTML "done":

1. Read the output file.
2. Verify against all 10 checks in §15.
3. For each slide, confirm: title present, body ≤100 words, visual non-trivial, speaker notes present, counter shows `N / 22`.
4. **Match this prompt's slide-by-slide spec exactly.** Any drift between spec and generated HTML is a defect.
5. Only declare "done" when all 10 checks pass.

## 17. Output Filename

Save as: `docs/handbook/03-client/leave-management-presentation.html`

## 18. Prompt Maintenance Workflow

See `prompts/README.md` § Prompt Maintenance Workflow.

---

## Appendix A — Changelog

See `prompts/README.md` § Current Prompts table for version history.

---

## Appendix B — Lessons Applied (#151–#164)

See `prompts/README.md` § Shared Methodology (Lessons #151–#164).
