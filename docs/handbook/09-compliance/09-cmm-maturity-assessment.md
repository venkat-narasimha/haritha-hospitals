# CMM L5 Maturity Assessment

**Doc ID:** HH-CMM-01
**Version:** 1.0
**Effective Date:** 2026-08-29
**Owner:** Venkat Narasimha (Processbricks)
**Review Cycle:** Annual (next: 2027-08-29)
**Last Reviewed:** 2026-08-29

> **Classification:** Internal
> **Honest read:** Haritha is **Level 3 (Defined) with Level 4 aspirations**. Not Level 4 yet, and nowhere near Level 5. This document records both where we are and where we are not.

## 1. Purpose

Without a maturity model, "we are getting better" is a feeling, not a fact. We can't tell whether a new runbook moves us up a level, or whether we're stuck at the same place despite writing more docs. This assessment exists so that, once a year, Venkat (and anyone else who reads this) can answer: *what level are we actually at, and what would it take to move up one?*

The CMM (Capability Maturity Model) is a public, well-understood 5-level scale. Using it — instead of inventing our own — means a future operator, auditor, or new hire can map our claims to a benchmark the rest of the industry recognises. The downside of CMM is that it was designed for large DoD contractors in the 1980s and carries some 1980s assumptions. We use the **spirit** of the model (5 levels, observable evidence per level, level-3 floor before level-4 metrics), not the letter (no "SEI appraisal", no process-area checklists, no staged representation).

This is the first formal assessment. It establishes the baseline; subsequent years compare against it. If we go two consecutive years without measurable progress on any gap below, that's a signal this whole exercise has become theatre.

## 2. Scope

### 2.1 In scope

- **What CMM is** — origin, 5 levels, key characteristic of each, with our honest scoring.
- **Self-assessment table** — current state per level, target state, gap.
- **Evidence per level** — specific LEARNINGS.md entries, runbooks, policies that prove (or fail to prove) the level.
- **Gap analysis to Level 4** — concrete, dated steps that would move us from "Defined" to "Managed".
- **Gap analysis to Level 5** — concrete, dated steps for "Optimizing" once Level 4 is achieved.
- **Honest assessment summary** — one paragraph, no hedging.

### 2.2 Out of scope

- **Detailed metrics per metric** — see [11-quantitative-management.md](11-quantitative-management.md) (HH-CMM-03).
- **Specific PDCA cycles in flight** — see [10-process-improvement.md](10-process-improvement.md) (HH-CMM-02).
- **Specific defect-prevention techniques** — see [12-defect-prevention.md](12-defect-prevention.md) (HH-CMM-04).
- **Process-area checklists (PA checklists)** — the original CMM v1.1 had 18 process areas. We don't use them; the 4 doc set (this + 10/11/12) covers the CMM-L5-relevant practices we actually need.

## 3. Policy Statement

### 3.1 What we commit to

Haritha Hospitals commits to:

1. **Annual self-assessment.** Venkat (or a designated reviewer) reads this document and the three companion docs each year, scores Haritha against the CMM levels using the §3a evidence table, and updates the "Last Reviewed" date.
2. **Honest scoring.** The score goes in the document regardless of whether it moved up. Inflating scores to look mature is the same class of failure as a backup that claims success without verifying (LEARNINGS #113, #114). We prefer a low score that triggers action to a high score that hides a gap.
3. **At least one gap closed per year.** The annual review must result in at least one gap being closed or measurably advanced. If a year ends with the gap list unchanged, the assessment was theatre and the next year's review should ask why.
4. **Public-style scoring, not theatrical.** This document lives in a public GitHub repo. Anyone with the URL can read our self-assessment. That is the point.
5. **Re-assessment triggers.** Beyond the annual cycle, this assessment is re-run if any of: (a) a SEV-1 incident reveals a missing process area, (b) a new environment joins (e.g., staging), (c) we add a second operator.

### 3.2 What this is NOT

- **Not a certification claim.** CMM is not a certifiable framework post-CMM v1.1; CMMI is the successor, and we are not pursuing CMMI appraisal. This document is internal hygiene, not external audit.
- **Not a maturity theatre checklist.** "We have a LEARNINGS.md" ≠ Level 5. The level a system is at is what happens *in practice* when nobody is watching, not what the docs claim.
- **Not a replacement for incident response.** The policies in this folder (07-incident-management, 08-business-continuity) are how we react to events. This assessment is how we judge whether the reaction is at the right maturity.

## 3a. Current State (as of 2026-08-29)

### 3a.1 CMM at a glance — origin and levels

CMM was developed by the Software Engineering Institute (SEI) at Carnegie Mellon University starting in the mid-1980s, published as CMM v1.1 in 1993, and superseded by CMMI in 2002. It describes 5 maturity levels for software organisations, each level building on the prior:

| Level | Name | Key characteristic | One-line summary |
|---|---|---|---|
| 1 | **Initial** | The process is whatever the individual does today. Often successful by heroic effort, often fails by the same. | "We get it done by whoever is awake." |
| 2 | **Repeatable** | Basic project management exists; successes can be repeated by the same person/process. | "The last success wasn't an accident." |
| 3 | **Defined** | The process is documented, standardised, and followed across the organisation. | "There's a written way; we follow it." |
| 4 | **Managed** | The process is quantitatively measured; control limits and statistical process control exist. | "We know when the numbers are wrong." |
| 5 | **Optimizing** | The organisation continuously improves the process from measured defects and innovation. | "We change the process because the data says to." |

**Key insight (not in original CMM):** levels 2-3 are about *codifying* what works; levels 4-5 are about *measuring* and *changing* what works. Jumping from 3 to 5 is not possible — Level 4 is the floor of "we have evidence, not opinion".

### 3a.2 Honest Haritha scoring — 2026-08-29 baseline

| Level | Target characteristic | Haritha today | Score (1-5) | Evidence (highlights) |
|---|---|---|---|---|
| **1 — Initial** | Heroic individual effort; ad-hoc; often missed | **Yes, sometimes.** Some work still depends on Venkat being available. | **1.5** | LEARNINGS #72 (verify-before-acting was an individual habit before policy), single-responder model per [07 §3.8](07-incident-management.md) |
| **2 — Repeatable** | Basic project management; successes repeatable | **Partial.** We have git, branching, deployment scripts, runbooks — but a "project" is a fix-driven thing, not a planned one. | **2.5** | Runbooks in `04-runbooks/`, git identity (MEMORY rule #11), 3-env model (dev/qa/prod), backup scripts proven to work after LEARNINGS #113 fix |
| **3 — Defined** | Process is documented and followed | **Yes, mostly.** 8 ISO policies + 4 CMM docs + 6 ops docs + LEARNINGS.md + MEMORY.md. Followed in practice (e.g., 2026-08-29 outage ran the playbook). | **3.0** | This folder, [LEARNINGS.md](../../../../.learnings/LEARNINGS.md), [MEMORY.md](../../../../MEMORY.md), [04-runbooks/](../04-runbooks/), the 2026-08-29 post-mortem in [05.2](../05-process/05.2-post-mortem.md) |
| **4 — Managed** | Quantitative measurement; control limits; SPC | **Partial.** We have *metrics* (heartbeat, MTTR from post-mortems) but no control limits, no SPC charts, no automated alerting on metric drift. | **2.0** | Heartbeat probes (LEARNINGS #90), daily ops doc, post-mortem timelines. **Gap:** no metric dashboards, no alert thresholds. |
| **5 — Optimizing** | Continuous improvement; defect prevention; tech innovation | **Emerging.** Some PDCA happening informally (backup hardening iterations), LEARNINGS.md is a defect-prevention repo in spirit. No formal PDCA cycle tracking. | **2.0** | LEARNINGS #157 (migration idempotency via PDCA), LEARNINGS #113/114 (backup hardening iterations), post-mortems feeding LEARNINGS.md. **Gap:** no formal PDCA log, no defect-categorisation taxonomy. |

**Composite honest score: Level 3 (Defined), with emerging Level 4 evidence and pre-Level-5 practice.** Translation: a new operator reading this folder would find clear instructions for most work, would not have quantitative signals about whether the work is going wrong, and would have to rediscover some improvements on their own.

### 3a.3 Level-by-level evidence detail

#### Level 1 evidence — initial mode still happens

- LEARNINGS #72: "Verify before claiming" was an *individual* habit before being codified in [07-incident-management §3.2](07-incident-management.md) and [05.1-change-management](../05-process/05.1-change-management.md). The fact it had to be codified means the level-1 default (assume-success) was the prior baseline.
- [07-incident-management §3.8](07-incident-management.md) admits the single-responder model. A single responder is a Level-1 organisation by definition — when they're gone, the process is gone.
- The 2026-08-29 outage resolution *did* follow the playbook, but the playbook only existed because that one incident (plus LEARNINGS #72 from a 2026-08-14 near-miss) forced its creation. Before 2026-08-29, the 15-minute triage lived in Venkat's head.

**Verdict:** Level 1 still happens. We've just contained it.

#### Level 2 evidence — repeatable exists in narrow scope

- **3-environment model (dev/qa/prod)** per MEMORY rule #1 — explicit, repeatable.
- **Git identity** per MEMORY rule #11 — venkat-narasimha / srivenkatnarasimha@gmail.com on every repo.
- **Backup scripts** that, after LEARNINGS #113/#114 fix, produce a sentinel line every successful run, retry on transient failures, and rsync offsite deterministically. Repeatable by a subagent without Venkat.
- **Deployment script** at [../04-runbooks/04.1-deployment.md](../04-runbooks/04.1-deployment.md) with hotfix branch convention.

**Verdict:** Level 2 holds for backup, deploy, restore-subset-drill, and git workflow. It does NOT hold for "what should we work on next?" — that's still ad-hoc per incident.

#### Level 3 evidence — defined and followed

- **8 ISO policies** in this folder, all written, all cross-referenced, all with revision history, all with `Lessons cited` (implicit through [07](07-incident-management.md) §7 footer).
- **LEARNINGS.md** with 157+ numbered lessons (LEARNINGS #41-#157 plus lower-numbered rules). New lessons cite runbooks; runbooks cite lessons. Closed loop documented.
- **MEMORY.md** as the single source of truth for tech-stack, container names, standing rules, subagent orchestration patterns.
- **Runbooks** (4.1 deploy, 4.2 daily ops, 4.3 DR, 4.4 incident response) with consistent format and "verify before acting" rules.
- **Process docs** (5.1 change management, 5.2 post-mortem) with template + filled example.
- **The 2026-08-29 outage followed the playbook** end-to-end: detection → triage → hypothesis → parent-verify (LEARNINGS #72) → Venkat YES → restart → all-clear → post-mortem → LEARNINGS #153/#154 → runbook updates. No heroics, no shortcuts. This is what Level 3 looks like in practice.

**Verdict:** Level 3 is real. We have a defined process and we follow it.

#### Level 4 evidence — managed but partial

What we have:

- **Heartbeat** at 08:30 IST daily — probes disk, containers, cron, backups. Catches drift (LEARNINGS #90).
- **Post-mortem timelines** record MTTR for every SEV-1/2. The 2026-08-29 outage was ~10 min detection-to-resolution.
- **Backup success rate** measurable via the BACKUP_OK sentinel line per LEARNINGS #113.

What we lack:

- **Control limits.** "99.9% uptime target" is stated but never measured against a chart; we don't know if 99.5% would be alarming or normal.
- **Statistical process control.** No SPC charts, no Western Electric / Nelson rules, no anomaly detection beyond "heartbeat failed".
- **Metric dashboards.** No Grafana, no Prometheus, no Frappe built-in monitoring dashboards configured. (Frappe has them; we haven't turned them on.)
- **Automated alerting on metric drift.** "Disk > 90%" → alert? Not wired.
- **Deployment frequency / change failure rate** — never measured. We don't know if the last 30 deploys had 0, 1, or 10 incidents.

**Verdict:** Level 4 is *aspirational*. We have the data sources; we don't have the dashboards and limits that turn data into control.

#### Level 5 evidence — optimizing but informal

What we have:

- **LEARNINGS.md as a defect-prevention repo.** Every SEV-1/2 writes a lesson; lessons get cited in runbooks; the next incident hits a faster MTTR. This is defect prevention in practice.
- **Post-mortem-driven improvement.** The 2026-08-29 post-mortem produced lessons #153, #154 AND runbook updates AND policy updates — all in one cycle.
- **PDCA happening informally.** Backup hardening went through multiple Plan→Do→Check→Act iterations (LEARNINGS #79, #80, #113, #114).

What we lack:

- **No formal PDCA log.** Improvements happen, but we don't track them as PDCA cycles with explicit hypothesis, metric, and learning.
- **No defect categorisation.** Defects are catalogued by date in LEARNINGS.md, not by class (schema, infra, code, process) or severity (cosmetic/minor/major/critical).
- **No technology innovation cadence.** We don't schedule time to ask "could we be doing this differently?" — it happens when an incident forces it.
- **No causal analysis meeting structure.** Post-mortems are blameless prose, but we don't have a structured "5 Whys" or "Fishbone" exercise per incident.

**Verdict:** Level 5 is *emergent*. The practices exist; the structure doesn't.

### 3a.4 Composite picture

| Dimension | Today | Gap |
|---|---|---|
| Codified process (Level 3) | ✅ Solid | None at this level; next focus is Level 4 |
| Measurement (Level 4) | ⚠️ Partial data, no control | [11-quantitative-management](11-quantitative-management.md) defines what to add |
| Improvement loop (Level 5) | ⚠️ Informal | [10-process-improvement](10-process-improvement.md) + [12-defect-prevention](12-defect-prevention.md) define what to add |

## 3b. Concrete Examples (Haritha history)

Each example proves or disproves a specific level. Read the examples, not just the table.

### Example 1 — Level 3 PROOF: the 2026-08-29 500-outage playbook execution

Already documented in [07-incident-management §3b Example 1](07-incident-management.md). What makes it Level 3: a brand-new operator, reading [07-incident-management](07-incident-management.md) and [04.4-incident-response](../04-runbooks/04.4-incident-response.md), could resolve the same outage. The process is in the docs, not in the operator.

**Lesson it proves:** [HH-CMM-01](../../../../.learnings/LEARNINGS.md) — at least one full incident has been resolved using only the documented process.

### Example 2 — Level 3 PROOF: backup hardening after the silent-failure streak

The 2026-08-10..18 backup silent-failure streak (LEARNINGS #79, #80, #113, #114) resulted in:

1. New version of `prod_backup.sh` with `timeout 900`, sentinel line, deterministic tarball naming.
2. New cron probe at 09:00 IST daily that tails the actual log file, not just exit codes.
3. LEARNINGS entries cited in the DR runbook.
4. A second DR drill scheduled (see [08 §9](08-business-continuity.md)).

**Lesson it proves:** [HH-CMM-01](../../../../.learnings/LEARNINGS.md) — improvement from a documented incident is itself a documented practice.

### Example 3 — Level 2 PROOF (and Level 4 gap): idempotent migration script

LEARNINGS #157 documents the upsert pattern (`frappe.get_doc().save()`). A subagent can re-run this script safely; it's repeatable. But: *we don't measure how often it has to be re-run*, and we don't have an alert for "this migration was run > N times this month" — which would be a Level 4 metric. **Lesson it proves:** Level 2 holds for migration; Level 4 is missing.

### Example 4 — Level 1 RESIDUE: Venkat's "will restart clear the data?" instinct

The 2026-08-29 incident response included Venkat asking the canonical LEARNINGS #72 question. The instinct was Venkat's; the policy ([07 §3.2 hard rule](07-incident-management.md)) now codifies it. Before the policy existed, an operator without that instinct could have executed `docker restart` blindly on a container with an ephemeral writeable layer and lost data. **Lesson it proves:** [HH-CMM-01](../../../../.learnings/LEARNINGS.md) — Level 1 instinct is being actively replaced by Level 3 policy, but the policy is only as good as the operator who reads it.

### Example 5 — Level 5 EMERGENCE: backup hardening PDCA (informal)

Cycle: backup failed silently (LEARNINGS #113) → fix deployed → verified 2 consecutive slots → still failed (LEARNINGS #114) → fix added tail-the-log probe → verified → succeeded for 8 days straight. This is PDCA. It's just not *called* PDCA anywhere in the docs. **Lesson it proves:** Level 5 happens; we just don't track it as such. [10-process-improvement](10-process-improvement.md) formalises this.

### Example 6 — Level 4 GAP: no deployment-frequency metric

The `haritha_hospital` custom app install (2026-08-29) was a deployment that caused a SEV-1. The question "how often do our deployments cause incidents?" has no answer in our docs. We could compute it from git log + LEARNINGS.md, but no one has. **Lesson it proves:** [HH-CMM-01](../../../../.learnings/LEARNINGS.md) — the data exists for Level 4; we don't measure it.

### Example 7 — Level 5 GAP: the mea culpa on CapitalCase colors

Phase 4.10 of the haritha build had three fix attempts for a Roster crash: "submit draft SAs" (wrong root cause, dismissed by Venkat even though subagent flagged it), "hex codes → Tailwind CapitalCase" (half-fix), "CapitalCase → lowercase" (actual fix). This is a defect-class case study for [12-defect-prevention §3b](12-defect-prevention.md), but at the time it happened we had no causal-analysis-meeting structure; the lessons-learned entry was added later from memory. **Lesson it proves:** [HH-CMM-01](../../../../.learnings/LEARNINGS.md) — defect prevention happens retrospectively, not proactively.

## 4. Responsibilities

| Role | Responsibilities |
|---|---|
| **Venkat Narasimha (Owner)** | Performs the annual self-assessment. Updates the §3a scoring table. Approves all "maturity level" claims made externally (e.g., to a future auditor). Owns the gap analysis; closes at least one gap per year. |
| **Processbricks admin** | Maintains the evidence links (LEARNINGS.md, runbook footers, post-mortem index) so the assessment can be re-verified. Flags new gaps as they appear in incidents. Co-owns the [10-process-improvement](10-process-improvement.md) PDCA log. |
| **Subagents (automation)** | Do not score maturity directly. Run probes, surface metrics, and write lessons; humans score the level. |
| **Future auditors / new operators** | Read this document first. Compare current §3a to last year's. Ask "what gap was closed this year?". |

## 5. Compliance Measurement

| Check | Frequency | Owner | Source of truth |
|---|---|---|---|
| This document re-read, scored, dated | Annually | VN | "Last Reviewed" date in header |
| At least one §3a gap closed per year | Annually | VN | diff of §3a across years |
| Composite score moved OR gap list shrank | Annually | VN | this document version |
| Runbooks cite all Level-3 claims | Continuous | PA | grep runbook footers vs §3a evidence column |
| Level-4 metric definitions match [11](11-quantitative-management.md) | Continuous | PA | cross-doc consistency |
| PDCA cycles match [10](10-process-improvement.md) | Continuous | PA | cross-doc consistency |
| Causal analyses match [12](12-defect-prevention.md) | Continuous | PA | cross-doc consistency |

**KPI dashboard (informal):**

| KPI | Target | Today | Source |
|---|---|---|---|
| Composite maturity score (sum of 5 level scores, max 25) | Year-over-year ≥ +1 | baseline 13.0 (1.5+2.5+3+2+2) | this document §3a |
| Open gaps count | Year-over-year ≤ −2 (fewer gaps) | baseline (count from §3a.2 + 4 gap docs) | this document |
| Runbook-citation lag for new lessons | ≤ 7 days | measured in [07 §5](07-incident-management.md) | runbook footers |
| PDCA cycles logged per quarter | ≥ 1 | 0 formal, several informal | [10](10-process-improvement.md) |
| Defect categorisation coverage | 100% of SEV-1/2 | 0% (none categorised yet) | [12](12-defect-prevention.md) |

## 6. Exceptions

1. **No external certification claim.** This document is internal; making it externally available does not mean we are "CMM Level N" in any contractual sense.
2. **Single-operator model** ([07 §3.8](07-incident-management.md)) prevents reaching Level 2 in some dimensions — there is no "across the organisation" if the organisation is one person. Acknowledged limit; not a maturity failure per se.
3. **Annual cycle may slip** if a SEV-1 absorbs Venkat's time. The re-assessment is documented within 30 days of slip, not silently skipped.
4. **All other exceptions** follow [01-info-security §6](01-info-security.md#6-exceptions).

## 6a. Edge Cases & Decision Matrix

### Edge case 1 — Scoring is borderline between two levels

- **Trigger.** Some practices look Level 3 but a specific aspect looks Level 4 (or vice versa).
- **Decision matrix.** Score at the **lower** of the two. The point of maturity levels is the floor, not the ceiling. A 3.5 that gets scored as 3 is more honest than a 3.5 scored as 4 and missed.

| Aspect | If L3 evidence is solid and L4 evidence is partial | If L3 is borderline and L4 is missing | If L3 is solid AND L4 is solid |
|---|---|---|---|
| Score | 3 | 2 | 4 |
| Why | Level 4 is unproven | Level 3 not yet complete | Move up |

### Edge case 2 — A new incident reveals a missing process area

- **Trigger.** 2026-Q4 incident reveals we had no process for, say, "vendor CVE patch within 7 days".
- **Decision matrix.** This is a re-assessment trigger per §3.1.5. Update §3a within 30 days; add a gap to the relevant ISO policy; close the gap within the next cycle.

### Edge case 3 — Second operator joins

- **Trigger.** Haritha hires a second admin/operator.
- **Decision matrix.** This is the biggest Level-2-into-Level-3 test we have. Re-assess within 60 days; specifically score the Level-2 dimensions (repeatable across people, not just one person's habits).

### Edge case 4 — Composite score claims we are at Level 4 when we are clearly at 3

- **Trigger.** Someone reads §3a.2 and says "we scored 13/25; that's over 60% which is close to Level 4".
- **Decision matrix.** Maturity levels are **not averages**. CMM is staged: you must clear each level's floor to claim the level. A 13/25 score with Level 3 met but Level 4 not met is a Level 3 organisation, period. Composite scores are for tracking year-over-year movement, not for level claims.

### Edge case 5 — Subagent tries to score maturity directly

- **Trigger.** A subagent session decides to compute the maturity level from the docs.
- **Decision matrix.** Subagents don't score. Humans do. The composite score is a Venkat (or designated reviewer) judgment call based on the §3a evidence table. Subagents can *populate* the evidence column (cite lessons, link runbooks) but the final score is human.

### Edge case 6 — The annual review finds no progress

- **Trigger.** 2027-08-29 review: same gaps as 2026-08-29, same composite score.
- **Decision matrix.** Document it. Then ask: is this assessment theatre? Two consecutive years of zero movement means the assessment isn't driving action. Options: (a) tighten the gap list to what we can actually close, (b) drop the annual cycle to biannual, (c) accept that maturity isn't a priority this year. None of these is comfortable; all are honest.

### Edge case 7 — A runbook "fixes" a gap without changing the score

- **Trigger.** We add a runbook for X; the gap list still says "no runbook for X".
- **Decision matrix.** The gap list updates when the gap is *closed*, not when work is started. "Work in progress" is a state on the gap, not a removal.

### Edge case 8 — An external party asks "what CMM level are you?"

- **Trigger.** A future hospital partner or auditor asks.
- **Decision matrix.** Answer: "Internal self-assessment as of 2026-08-29 places us at Level 3 (Defined) with emerging Level 4 practices; this is not a certified appraisal and we do not represent it as such." Link to this document. Do not oversell.

## 7. Related Documents

- [10-process-improvement.md](10-process-improvement.md) — HH-CMM-02 — PDCA framework; the Level-5 practice.
- [11-quantitative-management.md](11-quantitative-management.md) — HH-CMM-03 — QPM / metrics; the Level-4 practice.
- [12-defect-prevention.md](12-defect-prevention.md) — HH-CMM-04 — Defect prevention / RCA; the Level-5 critical practice.
- [01-info-security.md](01-info-security.md) — Umbrella; this doc fits under the maturity umbrella, not the ISMS.
- [05-process/05.1-change-management.md](../05-process/05.1-change-management.md) — How changes happen; the input to maturity assessment.
- [05-process/05.2-post-mortem.md](../05-process/05.2-post-mortem.md) — How incidents translate to lessons; the primary evidence source.
- [04-runbooks/](../04-runbooks/) — The operational evidence for Level 3.
- [../../../../.learnings/LEARNINGS.md](../../../../.learnings/LEARNINGS.md) — All numbered lessons; primary evidence source.
- [../../../../MEMORY.md](../../../../MEMORY.md) — Standing rules, tech stack, subagent patterns; the Level-3 codified state.

## 8. Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-29 | venkat-narasimha | Initial baseline assessment |

## 9. Implementation Checklist

Concrete actions derived from this assessment. Owner initials: VN = Venkat Narasimha; PA = Processbricks admin. Status as of 2026-08-29.

### Immediate (this week)

- [ ] **Review the §3a.2 scoring** with Venkat; agree on the 13/25 composite. Owner: VN. Target: 2026-09-05. Status: Not Started.
- [ ] **Pick the first gap to close** (recommend: deployment-frequency metric per [11](11-quantitative-management.md)). Owner: VN. Target: 2026-09-05. Status: Not Started.
- [ ] **Cross-link this assessment from MEMORY.md** so the "current state" line in MEMORY can reference maturity score. Owner: PA. Target: 2026-09-05. Status: Not Started.

### Short-term (2026-Q3)

- [ ] **Deploy the first metric dashboard** (Frappe built-in Monitoring module + custom Daily Ops card per [11](11-quantitative-management.md)). Owner: PA. Target: 2026-09-30. Status: Not Started.
- [ ] **Define control limits** for at least 3 metrics (uptime, backup success, MTTR) per [11](11-quantitative-management.md). Owner: VN. Target: 2026-09-30. Status: Not Started.
- [ ] **Open the first formal PDCA cycle log** at `docs/phase6/06-process-improvements/` per [10](10-process-improvement.md). Owner: PA. Target: 2026-09-30. Status: Not Started.
- [ ] **First causal analysis meeting** structured per [12](12-defect-prevention.md) §3. Owner: VN. Target: 2026-09-30. Status: Not Started.

### Medium-term (2026-Q4)

- [ ] **First re-assessment** (this document, version 1.1). Owner: VN. Target: 2027-08-29 (annual) or earlier if a SEV-1 forces it. Status: Not Started.
- [ ] **Re-score with Level-4 metrics** populated (deployment frequency, change failure rate, MTTR by SEV). Owner: VN. Target: 2026-12-31. Status: Not Started.
- [ ] **Add defect categorisation to LEARNINGS.md entries** (per [12](12-defect-prevention.md) §5). Owner: PA. Target: 2026-11-30. Status: Not Started.
- [ ] **At least 4 PDCA cycles completed** in 2026-Q4. Owner: PA. Target: 2026-12-31. Status: Not Started.

### Long-term (2027+)

- [ ] **Reach composite score ≥ 17/25** (i.e., solidly Level 3 with Level 4 emerging). Owner: VN. Target: 2027-12-31. Status: Not Started.
- [ ] **Add a second operator** (breaks the single-responder ceiling on Level 2). Owner: VN. Target: TBD. Status: Not Started.
- [ ] **Sponsor an external maturity review** (optional; confirms our self-assessment isn't blind-spotting). Owner: VN. Target: TBD. Status: Not Started.

### Recurring verification (runs forever)

- [ ] **Annual self-assessment** — re-read this document, update §3a, increment version. Owner: VN. Frequency: annually. Status: Done (this revision).
- [ ] **Quarterly gap-status check** — review the §3a gap list; close any that are closed. Owner: VN. Frequency: quarterly. Status: Not Started.
- [ ] **Cross-doc consistency check** — verify this doc's claims match [10](10-process-improvement.md), [11](11-quantitative-management.md), [12](12-defect-prevention.md). Owner: PA. Frequency: quarterly. Status: Not Started.

*Score honestly. A Level 3 with documented gaps is more useful than a Level 5 with hidden failures. Document or repeat.*