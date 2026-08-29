# Information Security Policy

**Policy ID:** HH-ISMS-01
**Version:** 1.0
**Effective Date:** 2026-08-29
**Owner:** Venkat Narasimha (Processbricks)
**Review Cycle:** Annual
**Last Reviewed:** 2026-08-29

## 1. Purpose

Information security is not optional at a hospital. Haritha Hospitals stores personally identifiable health information (PHI), employee compensation data, and operational records that — if leaked, corrupted, or destroyed — cause direct harm to patients, staff, and the business.

Three failure modes we defend against:

- **Confidentiality loss.** Patient names + diagnoses or employee salaries landing on a USB stick or a public pastebin. Legal liability under IT Act 2000 + DPDP Act 2023. Reputational damage that survives the news cycle.
- **Integrity loss.** A clinician acting on a tampered medication record, or HR paying the wrong salary because attendance was silently corrupted. Both are clinical/financial incidents, not "data issues".
- **Availability loss.** Roster unavailable on shift-change morning, payroll unable to compute salaries on the 1st. Recovery from ransomware takes days, not minutes, without verified backups.

This policy is the umbrella under which all other ISMS documents exist. It states the rules; the other policies (access control, asset management, cryptography, operations security, etc.) state how we implement them.

## 2. Scope

Applies to **everything** that touches Haritha Hospitals information:

- **Systems.** Production (`pberpprod`, sites `pberpPROD.duckdns.org`), Dev (`pberpdev`), QA (`pberpqa`), plus the haritha_hospital custom app, all bench containers (`erp-{env}-{backend,frontend,db,redis,scheduler}`), the VPS host (`vps-3248b821`, 144.217.163.228), and Venkat's offsite backup VPS (135.125.196.35).
- **Data.** Patient records, employee records (HR, payroll, attendance), financial data, configuration, code, runbooks, credentials, audit logs.
- **People.** Venkat (owner/admin), any contracted developer, any intern with temporary access, and Processbricks staff acting on Haritha's behalf.
- **Vendors.** Anyone with read/write access to Haritha systems or data — currently limited to the duckdns dynamic-DNS provider and Let's Encrypt (see [04-cryptography](04-cryptography.md) for cert handling).
- **Environments.** Both container-attached (`frappeclaw-data` workspace) and the VPS-side `/home/vijay/frappeclaw/` compose trees.

## 3. Policy Statement

The following rules are non-negotiable:

1. **Patient data is confidential.** Never share, screenshot, dump, or export patient records without documented authorization. "Authorization" means a written ticket naming the records, the recipient, the purpose, and the expiry.
2. **All access must be authenticated and authorized.** Anonymous access to any data-bearing endpoint is a security incident, not a feature. See [02-access-control](02-access-control.md) for how.
3. **Security incidents must be reported within 1 hour of discovery.** Use the SEV classification in [04.4 Incident Response Plan](../04-runbooks/04.4-incident-response.md). Do not investigate first, do not fix first — **report first**. Slack DM Venkat, then triage.
4. **Backups are mandatory (3-2-1).** At least 3 copies of production data, on 2 different media, with 1 copy offsite. The offsite target is `venkat@135.125.196.35` (rsync, daily 03:30 IST cron). The third copy is the local backup volume. Verify weekly — see [04.3 Disaster Recovery](../04-runbooks/04.3-disaster-recovery.md) and [05-operations-security](05-operations-security.md).
5. **No production data on personal devices.** No laptop, no USB stick, no personal phone. Production data lives in the production container or in the production backup pipeline. Period.
6. **Annual security training is required.** Every person with access reads this policy set + the runbooks annually and signs off in the access register. New joiners complete this within their first 30 days.
8. **No secrets in git.** No DB passwords, SSH private keys, API tokens, or `.env` files. Even for dev. Even "temporarily". Pre-commit hook + manual review on every PR. See [04-cryptography](04-cryptography.md).
9. **Least privilege by default.** New users start with the minimum role that lets them do their job. Privilege escalation is explicit, time-boxed, and audited. See [02-access-control](02-access-control.md).
10. **Documented exceptions only.** Deviations from this policy require a written exception (see §6). "I was busy" or "we'll fix it later" is not an exception — it's an undocumented violation.

## 4. Responsibilities

| Role | Responsibilities |
|---|---|
| **Venkat Narasimha (Owner)** | Approves this policy + exceptions. Owns the risk register. Annual review. Final escalation point for SEV-1/SEV-2. |
| **Processbricks admin** | Implements access control, backup verification, secret rotation. Monitors logs daily. Reports anomalies within 1 hour. |
| **All users** | Read + acknowledge this policy annually. Comply with access control (don't share creds, don't bypass MFA). Report incidents within 1 hour. Protect credentials (no shoulder-surfing, no plain-text storage). |
| **Vendors** | Bound by contract to these rules. Read-only where possible. Any sub-processor they use gets the same treatment. |
| **Subagents / automation** | Read policy set before acting on prod data. Never run `bench console` against prod without an approved ticket. Never write to `tabSingles` or `tabDocType` directly — use fixtures + `frappe.get_doc().save()` (LEARNINGS #157). |

## 5. Compliance Measurement

We verify this policy on a recurring cadence:

- **Quarterly access review.** Pull `tabUser` + role assignments, reconcile against the access register. Any user without a current business need loses access within 24h. Owner: Venkat.
- **Monthly backup verification.** Restore the latest tarball to a scratch MariaDB, run a sanity query (`SELECT COUNT(*) FROM \`tabPatient\` etc.`), compare against prod counts. Owner: admin. Reference: [04.3 Disaster Recovery](../04-runbooks/04.3-disaster-recovery.md) restore checklist.
- **Annual penetration test.** Out of scope for v1 (no budget); planned once a second engineer joins. Until then, "internal audit" = Venkat + structured walk-through of the OWASP Top 10 against the running stack.
- **Weekly log review.** Tail `frappe-bench/logs/*.log`, nginx access log, and SSH auth log. Look for `auth failures`, `unauthorized`, `permission denied`, `4xx/5xx` spikes. Owner: admin.
- **Quarterly secret audit.** Verify no plaintext secrets in repo (`git grep -iE 'password|secret|token' -- ':!**/docs/**' | grep -v '\.md:'`). Verify `.env` files outside containers are gitignored. Owner: Venkat.
- **Annual policy review.** Re-read every policy in `09-compliance/`, update version + Last Reviewed fields, archive the diff. Triggered by Venkat.

KPI dashboard (informal, not a Grafana board):

| KPI | Target | Source |
|---|---|---|
| Offsite backup freshness | ≤ 26h lag | rsync target timestamp |
| Failed login rate | ≤ 5/day average | frappe-bench logs |
| Unresolved SEV-1/2 incidents | 0 | Slack #ops channel |
| Users without MFA on prod | 0 | tabUser + 2FA table |

## 6. Exceptions

Exceptions are **rare, documented, and time-boxed**. Process:

1. Requester opens an "Exception Request" doc (free-form: asana task or a Markdown file in `09-compliance/exceptions/`) naming the policy clause, the reason, the compensating control, and the expiry date.
2. Venkat reviews within 24h. Reject, approve, or modify.
3. Approved exceptions are logged in the access register / exception log with start + end dates.
4. On expiry: control reverts automatically. If extension is needed, a new request is filed (no silent renewals).
5. Emergency exceptions (e.g., "production is down and we need to share a DB password over Slack to recover") are pre-approved verbally, but the written exception must be filed within 24h of the incident close. Post-incident review covers what could have prevented the emergency.

## 7. Related Documents

- [02-access-control.md](02-access-control.md) — Who can access what, how, and for how long.
- [03-asset-management.md](03-asset-management.md) — Inventory and data classification.
- [04-cryptography.md](04-cryptography.md) — How we protect data in motion and at rest.
- [05-operations-security.md](05-operations-security.md) — Backups, patching, monitoring, change control.
- [07-incident-management.md](07-incident-management.md) — SEV classification + escalation.
- [08-business-continuity.md](08-business-continuity.md) — DR + RTO/RPO targets.
- [../04-runbooks/04.3-disaster-recovery.md](../04-runbooks/04.3-disaster-recovery.md) — Restore procedure.
- [../04-runbooks/04.4-incident-response.md](../04-runbooks/04.4-incident-response.md) — Triage flow.
- [../../../../.learnings/LEARNINGS.md](../../../../.learnings/LEARNINGS.md) — Lessons #114 (silent cron failures), #153 (gunicorn restart), #154 (DB password drift).

## 8. Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-29 | venkat-narasimha | Initial |