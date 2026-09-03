# PROMPT: Generate Single-File HTML Presentation — Shift Management with ERPNext HRMS, CMM Level 5

## Role
You are a technical writer + front-end developer generating a self-contained HTML presentation. The output explains shift management in ERPNext HRMS and is structured around **CMM Level 5 process areas** (Defect Prevention, Technology Change Management, Quantitative Process Management, Process Innovation). Suitable for general audience — internal teams (HR, ops, new hires) and external evaluators. No prior ERPNext knowledge assumed.

## Output Specs
- **Format:** single `.html` file, fully self-contained (inline CSS, no external assets)
- **Slides:** exactly 20, each in `<section class="slide" id="slide-N">`
- **Navigation:** keyboard arrows (←/→) + click handlers + slide counter (e.g., "5 / 20")
- **Print:** include `@media print { ... }` for clean PDF export
- **No JavaScript libraries** — vanilla JS only for nav
- **No external images** — use emoji, inline SVG, or pure CSS for all visuals

## Design (light theme only, minimal + professional + clean)
- **Palette:** primary `#1e40af` (deep blue), secondary `#64748b` (slate), accent `#0ea5e9` (sky), text `#0f172a`, muted `#94a3b8`, bg `#ffffff` with `#f8fafc` alternating slides
- **Typography:** `Inter, system-ui, -apple-system, sans-serif` body; headings bold 600; body 18px / 1.6 line-height; slide title 36-44px
- **Layout:** centered single column, max-width 960px, padding 64px 32px
- **Visuals:** inline SVG or CSS shapes only. Generous whitespace. One focal point per slide.
- **No emojis as decoration** — use sparingly only where they aid clarity

## Slide Structure (20 slides across 7 sections)

### Intro (slides 1-2)
**Slide 1 — Title**
- Title: "Shift Management with ERPNext HRMS"
- Subtitle: "A CMM Level 5 approach to planning, scheduling, attendance & continuous improvement"

**Slide 2 — Agenda**
- 7 sections visualized as a roadmap: Foundation → Operations → Quantitative Mgmt → Defect Prevention → Technology Change Mgmt → Process Innovation → Conclusion

### Section 1 — Foundation (slide 3)
**Slide 3 — ERPNext + HRMS Stack**
- Open-source ERP platform (Frappe framework + ERPNext apps layer)
- Visual: layered stack diagram
- ~12 business domains (accounting, inventory, sales, HR, payroll, projects, etc.)
- HRMS = HR module, installable as separate app on top
- 5,000+ contributors, web + mobile, multi-language

### Section 2 — Shift Management Operations (slides 4-11)
**Slide 4 — Why shift management matters**
- Visual: 24h clock divided into 3 shifts
- Pain points without proper shift mgmt: spreadsheets → errors, coverage gaps, payroll disputes, compliance risks
- Industries that need it: healthcare, manufacturing, retail, hospitality, BPOs, security, logistics

**Slide 5 — Shift Management Operations — Overview**
- 7 stages visualized: Plan → Schedule → Request → Assign → Check-in → Track → Report
- Each stage = one or more DocTypes in HRMS

**Slide 6 — Shift Type**
- Definition: template defining when work happens
- Visual: 3 cards (Morning 06:00-14:00 / Evening 14:00-22:00 / Night 22:00-06:00)
- Properties: name, start time, end time, color, grace period
- Naming conventions: location-based, time-based, role-based

**Slide 7 — Shift Location**
- Definition: physical place tied to a shift
- Visual: simple map mockup (pin + radius circle, e.g., 200m)
- Why: prevents buddy-punching (clocking in for someone else)
- Setup: GPS coords + allowed radius

**Slide 8 — Shift Schedule + Shift Request**
- Shift Schedule: planned shifts over a date range (template)
- Shift Request: employee-initiated swap request
- Visual: request flow (Employee → Manager → HR) + approval diagram
- Configurable multi-level approval workflow

**Slide 9 — Shift Assignment + Bulk + Tool**
- Shift Assignment: actual employee-to-shift assignment
- Shift Schedule Assignment: bulk apply schedule to many employees
- Shift Assignment Tool: drag-and-drop UI for fast scheduling
- Visual: drag-drop calendar grid mockup
- Time saving: monthly roster in minutes vs hours

**Slide 10 — Roster** *(image placeholder reserved)*
- Visual calendar of who's working when
- Top 60%: filters (department/role/location), week/month toggle, color legend
- **Bottom 40%: reserved image area** with caption "Insert roster screenshot here" — leave this space empty, do NOT fill it
- Mark this region with a dashed-border placeholder div for the user

**Slide 11 — Attendance + Reports**
- Auto-attendance: GPS check-in, biometric, mobile
- Visual: workflow diagram (check-in → match shift → mark present/late)
- Reports: daily summary, late arrivals, early departures, overtime, dept headcount, compliance

### Section 3 — Quantitative Process Management (CMM L5 PA #1, slides 12-13)
**Slide 12 — QPM — KPIs**
- Key Performance Indicators for shift management:
  - Coverage rate (% shifts filled)
  - Attendance accuracy (% on-time check-ins)
  - Late arrival rate
  - Overtime hours per week
  - Roster publish lead time
  - Shift swap approval SLA

**Slide 13 — Baselines, Control Limits, Dashboards**
- For each KPI: baseline value, control limit, action threshold
- Example pattern: "Late arrivals <2% for 6 weeks → process stable; >5% → trigger review"
- Visual: control chart mockup with upper/lower limits marked

### Section 4 — Defect Prevention (CMM L5 PA #2, slides 14-16)
**Slide 14 — Common Pitfalls**
- Typical defects:
  - Double-booking employees (one person in 2 shifts same time)
  - Missed check-ins due to geo-fence errors
  - Wrong shift type assigned to wrong role
  - Payroll calculation errors (overtime, late deductions)
  - Compliance violations (overtime limits, rest periods)

**Slide 15 — Root Cause Analysis**
- 5 Whys methodology (iterative questioning to root cause)
- Fishbone / Ishikawa diagram (categories: Method, Machine, Material, Manpower, Measurement, Environment)
- Example walk-through: "Why did double-booking happen?" → drill 5 levels → root cause

**Slide 16 — Defect Prevention Process**
- Cycle: Detect → Analyze → Prevent → Verify
- Lessons learned repository
- Causal analysis meeting (who, when, agenda)
- Action item tracking + closure verification

### Section 5 — Technology Change Management (CMM L5 PA #3, slide 17)
**Slide 17 — Technology Change Management**
- Change request → staging environment → rollback procedures → communication plan
- Version control + CI/CD
- Real example: "Upgrading Frappe framework without downtime — blue/green deploy"
- Risk mitigation: pre-flight checklist, smoke test, post-deploy verification

### Section 6 — Process Innovation (CMM L5 PA #4, slide 18)
**Slide 18 — Process Innovation + PDCA**
- PDCA cycle (Plan-Do-Check-Act) applied to shift management
- Innovation pipeline: ideas → pilot → measure → scale or discard
- Quarterly reviews: which experiments worked, which didn't
- Continuous improvement is NOT a project — it's a habit

### Section 7 — Conclusion (slides 19-20)
**Slide 19 — Why Choose ERPNext + Haritha**
- Open source = no license fees (compare SAP / Oracle / Workday)
- 100% custom code ownership
- Healthcare-specific customizations available
- Active community + local partner support
- Flexibility wins: configure workflows, don't fight vendor defaults

**Slide 20 — Conclusion + Next Steps**
- 3 takeaways:
  1. ERPNext + HRMS = complete open-source stack
  2. Shift management covers full lifecycle (planning → assignment → attendance → reports)
  3. CMM L5 practices (QPM, Defect Prevention, TCM, Innovation) elevate ops from reactive to proactive
- Next steps: explore the demo, plan a pilot deployment, contact for custom development

## Special Accommodations (CRITICAL)

### Slide 10 — Roster Image Placeholder
The roster slide must reserve the bottom 40% of the slide for an image. Include a clearly-marked placeholder:
```html
<div class="image-placeholder" style="border: 2px dashed #94a3b8; padding: 32px; text-align: center; color: #64748b;">
  [Insert roster screenshot here]
  <br><small>Roster view from Haritha Hospitals — calendar of employee shifts</small>
</div>
```

### Slide 17 — Schema Flowchart (ERD)
Include an inline SVG entity-relationship diagram showing the relationships between shift management DocTypes. Required entities:
- Employee
- Shift Type
- Shift Location
- Shift Schedule
- Shift Assignment
- Shift Request
- Holiday List
- Attendance
- Employee Checkin

Show clear Link relationships (e.g., Shift Assignment → Employee, Shift Assignment → Shift Type, Shift Assignment → Shift Location). Use boxes for entities, arrows for relationships.

## Content Constraints (CRITICAL)
- **No Haritha-specific data** — no employee counts, no company-specific metrics, no real customer names
- **Use generic illustrative examples only** (e.g., "Morning shift 06:00-14:00", "Ward A", "200m radius")
- **Tone:** friendly but professional, never salesy
- **Per-slide length:** max ~100 words body text (keep slides scannable)
- **One focal point per slide** — don't cram multiple ideas
- **Define jargon on first use** (e.g., "DocType: a database table in ERPNext")
- **CMM L5 vocabulary must appear:** PDCA, 5 Whys, Fishbone, control limit, baseline, defect category, causal analysis, technology change management

## Quality Bar
- Slide title ≤ 8 words
- Body text scannable in <10 seconds
- Visuals (SVG/CSS) illustrate the concept, not just decorate
- No filler phrases ("It's important to note that...")
- Print stylesheet must produce usable PDF (no slide-cut-off issues)
- The presentation must read as professionally structured CMM L5 material — not a generic "what is shift management" deck
