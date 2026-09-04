## 1. Role

You are a **technical writer + front-end developer** generating a single self-contained HTML presentation. The presentation explains **shift management in ERPNext HRMS** to a general audience.

## 2. Audience (3 personas)

Generate content that resonates with all three:

1. **Priya — HR Manager (internal)**
   - Cares about: practical features, KPIs, ROI on deployment
   - Reads every slide for "can I actually use this?"
2. **Arjun — Operations Lead (internal)**
   - Cares about: workflow, error reduction, simplicity
   - Reads for "will this make my daily life easier?"
3. **Sarah — External Evaluator (external)**
   - Cares about: capabilities, cost, ease of deployment vs alternatives (SAP, Workday, BambooHR)
   - Reads for "is this the right product for my company?"

## 3. Goal

Generate a **17-slide** self-contained HTML presentation explaining shift management in ERPNext HRMS. Educational, general audience, light theme, professional + minimal + clean.

## 4. Time Budget

**Total: 40 minutes** (32 min content + 8 min Q&A)
Per-slide timing specified in §7. (Note: per-slide timings sum to ~34 min — content is flexible; speaker can compress/expand as needed.)

## 5. Output Specs

- **Format:** single `.html` file, fully self-contained (inline CSS, no external assets)
- **Slides:** exactly **17**, each `<section class="slide" id="slide-N">`
- **Navigation:** keyboard arrows (←/→) + click handlers + slide counter (e.g., "5 / 17")
- **Print:** include `@media print { ... }` for clean PDF export
- **No JavaScript libraries** — vanilla JS only
- **No external images** — use inline SVG or pure CSS shapes
- **Accessibility:** semantic HTML, sufficient color contrast (≥4.5:1 for body text), keyboard nav

## 6. Design Tokens (exact values)

### 6.1 Colors
- Primary `#1e40af` (deep blue)
- Secondary `#64748b` (slate)
- Accent `#0ea5e9` (sky)
- Text `#0f172a` (near-black)
- Muted `#94a3b8`
- Background `#ffffff` (odd slides) / `#f8fafc` (even slides)
- Code `#f1f5f9` background / `#0f172a` text

### 6.2 Typography
- Body: `Inter, system-ui, -apple-system, sans-serif` 18px / 1.6 line-height
- Headings: same font, weight 600, slide title 40px, h3 24px, h4 18px
- Code: `JetBrains Mono, ui-monospace, monospace` 14px

### 6.3 Layout
- Max-width 960px, centered
- Padding 64px top/bottom, 32px sides
- Spacing scale: 8 / 16 / 24 / 32 / 48 / 64px (use these, no other values)

### 6.4 Animation
- Slide-in: 200ms ease-out

## 7. Slide Template (apply uniformly to all 17)

Every slide must include:
1. `<div class="slide-number">N / 17</div>`
2. `<h2 class="slide-title">...</h2>`
3. `<div class="body">... main content (≤100 words) ...</div>`
4. **One focal visual element** (SVG, CSS shape, or structured list)
5. `<aside class="speaker-notes">...</aside>` (hidden by default, toggle with `S` key)
6. Transition note (1 sentence) in speaker notes

## 8. Slide-by-Slide Specs (17 slides)

### Intro (slides 1-2)

**Slide 1 — Title** (30s)
- Slide title: "Shift Management with ERPNext HRMS"
- Subtitle: "A practical guide to planning, scheduling, attendance & reporting"
- Display **metadata block** at bottom-right:
  - Version: 1.0
  - Date: 2026-09-04
  - Audience: General (HR, Operations, Evaluators)
- Visual: clean centered layout, no emoji
- Speaker notes: open with welcome, frame the 40-min talk, who it is for
- Transition: "Let's start with what we are covering today."

**Slide 2 — Agenda** (45s)
- Title: "Agenda"
- Visual: 4 numbered cards in a row:
  1. ERPNext + HRMS Stack
  2. Shift Management Operations
  3. Custom App + Schema
  4. Why ERPNext + Haritha
- Sub-bullets under each card (1-line each)
- Speaker notes: walk through the 4 sections, mention each is ~7 min
- Transition: "First, a quick foundation."

### Section 1 — Foundation (slide 3)

**Slide 3 — ERPNext + HRMS Stack** (2 min)
- Title: "ERPNext + HRMS Stack"
- 4 bullets:
  - Open-source ERP platform (Frappe framework + ERPNext apps)
  - ~12 business domains (accounting, inventory, sales, HR, payroll, projects, etc.)
  - HRMS = HR module, installable as a separate app on top of ERPNext
  - 5,000+ contributors, web + mobile, multi-language
- Visual: **layered stack diagram (3 layers)**:
  - Bottom: "Frappe Framework (Python + JS)"
  - Middle: "ERPNext (apps layer)"
  - Top: "HRMS (HR module)"
- Speaker notes: explain the open-source advantage (no license fees, code ownership)
- Transition: "Now let's dive into shift management."

### Section 2 — Shift Management Operations (slides 4-13)

**Slide 4 — Why shift management matters** (2 min)
- Title: "Why shift management matters"
- 3 bullets:
  - Without it: spreadsheets → errors, coverage gaps, payroll disputes, compliance risks
  - Industries needing shift mgmt: healthcare, manufacturing, retail, hospitality, BPOs, security, logistics
  - 24/7 operations require systematic scheduling
- Visual: **24h clock divided into 3 colored arcs** (morning/afternoon/night)
- Speaker notes: frame the problem space before solutions
- Transition: "Let's start with the foundation: Shift Type."

**Slide 5 — Shift Type** (2 min) — **SEE §11 CONCRETE EXAMPLE**
- Title: "Shift Type"
- 3 bullets:
  - Definition: reusable template defining when work happens
  - Properties: name, start time, end time, color (for visual ID), grace period
  - Naming conventions: location-based ("Ward A"), time-based ("Morning"), role-based ("Doctor")
- Visual: **3 shift cards** side-by-side, each showing:
  - Color stripe on top
  - Name (Morning / Evening / Night)
  - Time range (06:00-14:00 / 14:00-22:00 / 22:00-06:00)
- Speaker notes: shift types are templates, not specific dates
- Transition: "But work happens at a place — that's Shift Location."

**Slide 6 — Shift Location** (1.5 min)
- Title: "Shift Location"
- 3 bullets:
  - Definition: physical place tied to a shift (e.g., a specific ward, factory floor)
  - Why it matters: prevents "buddy punching" (clocking in for absent colleagues)
  - Setup: GPS coordinates + allowed radius (e.g., 200m)
- Visual: **simple map mockup** — pin marker + 200m radius circle around it, label "Allowed check-in zone"
- Speaker notes: especially relevant for healthcare and field work
- Transition: "Templates are scheduled — Shift Schedule."

**Slide 7 — Shift Schedule** (2 min)
- Title: "Shift Schedule"
- 3 bullets:
  - Definition: planned shifts over a date range (template)
  - Recurrence: weekly, monthly, or one-off patterns
  - Used as the master template for Shift Assignment
- Visual: **calendar grid mockup** — week view with colored cells per shift type
- Speaker notes: "schedule" = template, "assignment" = actual (next slides)
- Transition: "Employees can also request changes — Shift Request."

**Slide 8 — Shift Request** (2 min)
- Title: "Shift Request"
- 3 bullets:
  - Employee-initiated: swap, leave, or change request
  - Multi-level approval workflow (configurable)
  - Tracks request state (Pending → Approved/Rejected)
- Visual: **flow diagram** — Employee → Manager → HR (arrows)
- Speaker notes: emphasize configurability of approval chains
- Transition: "Once approved, the assignment happens — Shift Assignment."

**Slide 9 — Shift Assignment** (2 min)
- Title: "Shift Assignment"
- 3 bullets:
  - Actual assignment of employee to specific shift instance (date + slot)
  - Validation: prevents double-booking, validates against schedule
  - Notifications: employee notified automatically
- Visual: **simple table mockup** — columns: Employee | Shift Type | Date | Status
- Speaker notes: "assignment" = real, specific (vs "schedule" = template)
- Transition: "Now the bulk + UI features — Schedule Assignment + Tool."

**Slide 10 — Shift Schedule Assignment + Tool (merged)** (2.5 min)
- Title: "Bulk Assignment + Tool"
- 3 bullets:
  - **Shift Schedule Assignment:** apply a schedule to many employees at once
  - **Shift Assignment Tool:** drag-and-drop UI for fast monthly scheduling
  - Time saving: monthly roster in minutes vs hours (not hours of manual work)
- Visual: **drag-drop mockup** — calendar grid with employee names as draggable cards
- Speaker notes: "this is where supervisors save hours per month"
- Transition: "What does the result look like? The Roster."

**Slide 11 — Roster** (2 min) — **IMAGE PLACEHOLDER RESERVED**
- Title: "Roster"
- Top 60%: text content:
  - Visual calendar of who's working when
  - Filters: department, role, location, week/month toggle
  - Color-coded by shift type
- **Bottom 40%: reserved image area** — must include the placeholder HTML from §12
- Speaker notes: explain filters and color coding
- Transition: "Now let's track who's actually showing up — Attendance."

**Slide 12 — Attendance + Auto-attendance** (2 min)
- Title: "Attendance + Auto-attendance"
- 3 bullets:
  - Auto-attendance via GPS check-in, biometric, or mobile
  - Manual override for missed check-ins
  - Real-time late-arrival detection
- Visual: **workflow diagram** — Check-in → Match Shift → Mark Present/Late
- Speaker notes: geo-fence + biometric tie back to Shift Location (slide 6)
- Transition: "All this data feeds into Reports."

**Slide 13 — Reports & Analytics** (2 min)
- Title: "Reports & Analytics"
- 4 bullets:
  - Daily attendance summary
  - Late arrivals, early departures
  - Overtime tracking
  - Department-wise headcount + compliance reports
- Visual: **dashboard mockup** — 4 small stat cards + 1 line chart
- Speaker notes: KPIs feed into HR decisions
- Transition: "What if ERPNext out-of-box doesn't fit? Custom apps."

### Section 3 — Custom App + Schema (slides 14-15)

**Slide 14 — Custom App Concept** (2 min)
- Title: "Extending ERPNext with Custom Apps"
- 3 bullets:
  - When ERPNext out-of-box doesn't fit: build a custom app (no fork needed)
  - Extend via: custom fields, custom DocTypes, custom workflows, custom scripts
  - Version-controlled via Git, deployable via `bench install-app`
- Visual: **layered architecture** — ERPNext base + Custom app layer on top
- Speaker notes: ownership stays with you, not locked to vendor
- Transition: "Here's how the entities relate."

**Slide 15 — Schema Flowchart** (3 min) — **SEE §13 SCHEMA DETAILS**
- Title: "Schema: Shift Management Entities"
- Visual: **inline SVG entity-relationship diagram** (see §13 for full spec)
- 1 bullet above the diagram: "How shift management entities relate"
- 1 bullet below: "ERPNext's open schema means you can extend with custom fields/tables"
- Speaker notes: walk through the central entity (Shift Assignment) and its relations
- Transition: "Why choose ERPNext + Haritha for your deployment."

### Section 4 — Why Choose + Conclusion (slides 16-17)

**Slide 16 — Why Choose ERPNext + Haritha** (2 min)
- Title: "Why choose ERPNext + Haritha"
- 5 bullets (one per row):
  - **Open source** — no license fees vs SAP / Oracle / Workday
  - **100% custom code ownership** — your code, your data, your control
  - **Healthcare-ready** — extensions available for clinical workflows
  - **Active community** — 5,000+ contributors + local partner support
  - **Flexibility wins** — configure workflows, don't fight vendor defaults
- Visual: **comparison table** (3 columns: ERPNext+Haritha / SAP / Workday) for the top 3 differentiators
- Speaker notes: emphasize ROI for each persona (Priya / Arjun / Sarah)
- Transition: "Let's wrap up."

**Slide 17 — Conclusion + Next Steps** (2 min)
- Title: "Conclusion + Next Steps"
- 3 takeaways (numbered list):
  1. ERPNext + HRMS = complete open-source stack for shift management
  2. Shift management covers full lifecycle (planning → scheduling → assignment → attendance → reports)
  3. Custom apps adapt ERPNext to your industry without forking
- Next steps (3 bullets):
  - Explore the demo (link placeholder)
  - Plan a pilot deployment (4-8 weeks typical)
  - Contact for custom development (placeholder)
- Visual: simple centered list, no chart
- Speaker notes: invite Q&A, mention how to reach for follow-ups
- Transition: "Thank you" + Q&A starts

## 9. Slide Template (HTML structure — apply uniformly)

```html
<section class="slide" id="slide-N">
  <div class="slide-number">N / 17</div>
  <h2 class="slide-title">[Slide Title]</h2>
  <div class="body">
    [Main content here, max 100 words, with one focal visual]
  </div>
  <aside class="speaker-notes">
    [What the presenter says — 2-3 sentences. Hidden by default; press 'S' to toggle.]
  </aside>
</section>
```

## 10. Speaker Notes Toggle (vanilla JS)

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 's' || e.key === 'S') {
    document.body.classList.toggle('show-speaker-notes');
  }
});
```

CSS:
```css
.speaker-notes { display: none; font-size: 14px; color: #64748b; border-left: 3px solid #0ea5e9; padding-left: 16px; margin-top: 24px; font-style: italic; }
.show-speaker-notes .speaker-notes { display: block; }
```

## 11. Concrete Example — Slide 5 (Shift Type)

Use this as the gold standard for every slide:

```html
<section class="slide" id="slide-5">
  <div class="slide-number">5 / 17</div>
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
  </aside>
</section>
```

CSS:
```css
.shift-cards { display: flex; gap: 24px; justify-content: center; margin-top: 32px; }
.shift-card { flex: 1; max-width: 220px; padding: 24px 16px 16px; border-radius: 8px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); background: white; border: 1px solid #e2e8f0; position: relative; }
.shift-color-bar { position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 8px 8px 0 0; }
.shift-name { font-size: 20px; font-weight: 600; color: #0f172a; margin-top: 12px; }
.shift-time { font-size: 16px; color: #1e40af; margin-top: 8px; font-family: 'JetBrains Mono', monospace; }
.shift-hours { font-size: 13px; color: #64748b; margin-top: 4px; }
```

**Notice this example:**
- Follows the slide template (§9)
- Uses design tokens (§6) — exact colors, fonts, spacing
- Speaker notes are hidden by default (§10)
- One focal visual (3 shift cards), max 100 words body
- Concrete example in speaker notes

Apply this exact pattern to all 17 slides.

## 11.5. Concrete Example #2 — Slide 13 (Reports & Analytics)

Apply same pattern as §11 — here's a dashboard mockup:

```html
<section class="slide" id="slide-13">
  <div class="slide-number">13 / 17</div>
  <h2 class="slide-title">Reports & Analytics</h2>
  <div class="body">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Coverage Today</div>
        <div class="stat-value">98.5%</div>
        <div class="stat-trend positive">+1.2%</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Late Arrivals</div>
        <div class="stat-value">4</div>
        <div class="stat-trend negative">+2</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Overtime Hours</div>
        <div class="stat-value">27h</div>
        <div class="stat-trend neutral">—</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Pending Swaps</div>
        <div class="stat-value">7</div>
        <div class="stat-trend neutral">—</div>
      </div>
    </div>
    <div class="chart-placeholder">
      <svg viewBox="0 0 600 200"><!-- line chart showing attendance over 7 days --></svg>
    </div>
  </div>
  <aside class="speaker-notes">
    These KPIs feed into HR decisions daily. Coverage rate drives staffing. Late arrivals trigger manager follow-up. Overtime flags compliance risks. The data updates in real-time as check-ins come in. Customize which KPIs appear per role.
  </aside>
</section>
```

CSS:
```css
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
.stat-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }
.stat-label { font-size: 13px; color: #64748b; }
.stat-value { font-size: 32px; font-weight: 700; color: #0f172a; margin-top: 8px; }
.stat-trend { font-size: 12px; margin-top: 4px; }
.stat-trend.positive { color: #10b981; }
.stat-trend.negative { color: #ef4444; }
.stat-trend.neutral { color: #64748b; }
.chart-placeholder { background: #f8fafc; border-radius: 8px; padding: 16px; height: 200px; }
```

**Notice:**
- 4 stat cards in grid + 1 chart placeholder = dashboard mockup
- Color-coded trend indicators (green/red/neutral)
- Concrete example in speaker notes
- Apply same pattern as §11 to all 17 slides

## 12. Roster Image Placeholder (Slide 11)

Bottom 40% of slide 11 MUST be:

```html
<div class="image-placeholder" style="border: 2px dashed #94a3b8; padding: 48px 32px; text-align: center; color: #64748b; margin-top: 32px;">
  [Insert roster screenshot here]
  <br><small>Roster view — calendar of employee shifts</small>
</div>
```

## 13. Schema Flowchart Details (Slide 15)

Required entities (from `docs/phase6/01-schema/01.2-schema-diagram.md`):

| Entity | Key fields | Links to |
|---|---|---|
| Employee | name, employee_name, company, department, designation | (root) |
| Shift Type | name, start_time, end_time, color | (root) |
| Shift Location | location_name, latitude, longitude, radius | (root) |
| Shift Schedule | shift_type, from_date, to_date, frequency | Shift Type |
| Shift Assignment | employee, shift_type, start_date, end_date, status, shift_location | Employee, Shift Type, Shift Location, Shift Schedule |
| Shift Request | employee, shift_type, from_date, to_date, status | Employee, Shift Type |
| Holiday List | holiday_date, description | (root, applies to dept via holiday_list field) |
| Attendance | employee, attendance_date, status, shift | Employee, Shift Type |
| Employee Checkin | employee, time, log_type, latitude, longitude | Employee |

**SVG structure:**
- 9 entity boxes (rounded rectangles)
- Arrows showing Link fields (label each with field name)
- Group entities by function:
  - **Schedule layer:** Shift Type, Shift Schedule, Shift Location
  - **Execution layer:** Shift Assignment, Shift Request, Employee Checkin
  - **Tracking layer:** Attendance, Holiday List
  - **Core:** Employee (in center, connects to all)
- Use color coding: schedule = blue, execution = sky, tracking = slate, core = primary blue

**ASCII layout (rough positioning):**
```
                Holiday List
                     |
   Shift Location ── Employee ── Shift Type
                     |            |
                     |       Shift Schedule
                     |            |
   Employee Checkin ──┤            |
                     |            |
              Shift Request ──────┤
                     |            |
              Shift Assignment ───┘
                     |
                 Attendance
```
Central entity: **Employee** (in middle). Schedule layer (Shift Type, Shift Schedule, Shift Location) on the right. Execution layer (Shift Assignment, Shift Request, Employee Checkin) on the left. Tracking (Attendance, Holiday List) at top/bottom. Group visually with colored backgrounds matching §13 color scheme.

## 14. Content Constraints (CRITICAL)

- **No Haritha-specific data** — no employee counts (e.g., "210 employees"), no company-specific metrics, no real customer names
- **Use generic illustrative examples** ("Morning shift 06:00-14:00", "Ward A", "200m radius")
- **Tone:** friendly but professional, never salesy
- **Per-slide body:** ≤100 words
- **One focal point per slide** — don't cram
- **Define jargon on first use** ("DocType: a database table in ERPNext")
- **No filler phrases** ("It's important to note that...", "As we can see...")
- **Never start slides with "In this slide we will..."** — jump into the content

## 15. Quality Bar (10 checks — verify before declaring done)

1. All 17 slides present in correct order
2. Each slide has title, body, visual, speaker notes
3. Per-slide timing sums to ~32 minutes
4. SVG renders correctly (no broken tags)
5. Print stylesheet works (test with browser print preview)
6. No filler phrases (run a search for "important", "as we can see", "in this slide", "It is worth noting", "essentially")
7. Roster image placeholder present (slide 11)
8. Schema flowchart present with all 9 entities + relations (slide 15)
9. Keyboard nav works (arrow keys + S for speaker notes)
10. Self-review done (see §16)

## 16. Self-Review Step (MANDATORY)

Before returning the generated HTML:

1. Read your own output file
2. Verify against all 10 checks in §15
3. For each slide, confirm: title present, body ≤100 words, visual is non-trivial, speaker notes present
4. **Note any deviations** in a final `<!-- REVIEW NOTES -->` HTML comment block at end of file
5. Only declare "done" when all 10 checks pass

## 17. Output Filename

Save as: `shift-management-presentation.html`