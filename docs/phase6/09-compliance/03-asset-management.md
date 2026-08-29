# Asset Management Policy

**Policy ID:** HH-ISMS-03
**Version:** 1.0
**Effective Date:** 2026-08-29
**Owner:** Venkat Narasimha (Processbricks)
**Review Cycle:** Annual
**Last Reviewed:** 2026-08-29

## 1. Purpose

You cannot secure what you do not know you have. This policy maintains an accurate inventory of Haritha's hardware, software, and data assets, and assigns each a sensitivity classification that drives handling rules.

Without an inventory, the 2026-08-29 prod DB password drift (LEARNINGS #154) would have been invisible — we'd have been rotating a backup of a stale value. Without classification, every doc gets treated as confidential (paralysis) or as public (leak). This policy fixes both.

Three questions this policy answers:

1. **What do we have?** Hardware, software, data — all listed.
2. **How sensitive is it?** Confidential / Internal / Public.
3. **What do we do when an asset retires?** Secure wipe, documented decommission, audit trail.

## 2. Scope

### 2.1 Hardware

| Asset | Location | Owner | Notes |
|---|---|---|---|
| VPS host `vps-3248b821` (144.217.163.228) | OVH (or current provider) | Venkat | All ERPNext envs + OpenClaw host |
| Offsite backup VPS | 135.125.196.35 | Venkat | Receives daily rsync |
| Local dev laptops | Venkat + admin | Owner | Not used for prod data |
| Containers (logical assets) | VPS | Venkat | `erp-{env}-{backend,frontend,scheduler,redis,db,proxy}` per env |

### 2.2 Software

- **Frappe** v16 (vendored in `apps/frappe/`, do NOT modify per repo guidelines).
- **ERPNext** v16 (vendored, do NOT modify).
- **HRMS** v16 (vendored, do NOT modify).
- **haritha_hospital** custom app (`apps/haritha_hospital/`) — the only code we own.
- **Nginx** (in `erp-prod-frontend-1` and similar) — Let's Encrypt cert handling.
- **MariaDB** 10.x (in `erp-{env}-db-1`).
- **Redis** (queue + cache).
- **Gunicorn** (WSGI, with `--preload` — see LEARNINGS #153).
- **Certbot** (Let's Encrypt renewal).

### 2.3 Data

See §3.2 for classification. Inventory of data categories:

- Patient registration + visit records (PHI).
- Employee master + HR records (PII).
- Attendance, shift, roster (operational PII).
- Payroll + compensation (highly sensitive PII).
- Sales / billing / financial transactions.
- App configuration (hooks, custom fields, print formats, notifications).
- Audit logs (`tabVersion`, nginx logs, bench logs).
- Source code (haritha_hospital app).
- Backups (tarballs in `frappeclaw-data` + offsite).
- Documentation (this very file).

## 3. Policy Statement

### 3.1 Inventory

1. **Single source of truth.** Asset inventory lives in `docs/phase6/09-compliance/asset-inventory.md` (to be created — see §6 exceptions for the stub status).
2. **Every new asset is registered within 7 days** of acquisition, provisioning, or creation. This includes new containers, new apps, new domains, new DBs, new laptops.
3. **Every retired asset is marked `RETIRED` with date + reason + decommission evidence** (e.g., `wipe-complete-2026-08-29.txt`). Rows are not deleted — historical inventory is audit-relevant.
4. **Annual inventory audit.** Venkat walks the inventory end-to-end, verifies each asset exists (or was properly retired), and re-signs the doc.

### 3.2 Classification

We use three levels. When in doubt, classify up.

#### **Confidential**

Patient-identifiable health information (PHI), employee compensation, credentials, audit logs.

Examples:
- `tabPatient`, `tabPatient Encounter`, `tabPatient Medical Record`.
- `tabSalary Slip`, `tabSalary Structure` (net pay, components, bank account).
- DB root passwords, SSH private keys, API tokens.
- `tabVersion` audit trail (reveals who touched what).

Handling:
- Access requires explicit role grant (`Healthcare Practitioner`, `HR Manager`, `System Manager`).
- Never copied to local laptops, USB sticks, or unmanaged cloud drives.
- Never sent over unencrypted email or Slack DMs.
- Backups encrypted at rest (where supported; tracked as future improvement).
- Disposal: secure wipe + documented chain of custody.

#### **Internal**

Default for anything not explicitly Confidential or Public. Operational data, app configuration, runbooks, code.

Examples:
- Attendance (`tabAttendance`), Shift Assignment, Roster.
- App code (`apps/haritha_hospital/`).
- Custom fields, property setters, print formats.
- Runbooks (`docs/phase6/04-runbooks/*`), this policy set.
- Bench + nginx logs.

Handling:
- Access requires Haritha-team membership (current or former).
- May be shared with vendors under NDA (e.g., for support).
- Code may live in GitHub (private repo). Runbooks are public-on-GitHub for transparency.
- Disposal: standard delete is acceptable; archive before delete if the asset has historical value.

#### **Public**

Anything explicitly published.

Examples:
- Marketing copy on haritha.in.
- Generic ERPNext documentation not customized for Haritha.
- Open-source libraries we depend on (Frappe, ERPNext upstream code).

Handling:
- No restrictions.
- Verify nothing Confidential is accidentally attached before publishing.

### 3.3 Labeling

1. **Documents** in `docs/` get an inline classification footer in the first 50 lines:
   `> **Classification:** Confidential | Internal | Public`
   Skip only when the doc is a public-facing user manual.
2. **Database tables** are classified in `asset-inventory.md` (no per-table labels in MariaDB — relies on RBAC).
3. **Backups** are treated as Confidential regardless of source classification, because aggregate dumps magnify sensitivity.
4. **Source code** is Internal by default; specific files (e.g., a config with credentials) override to Confidential.

### 3.4 Disposal

1. **Hardware.** Vendor-provided secure wipe (e.g., `hdparm --security-erase` for SSDs, or physical destruction). Wipe evidence retained for 3 years.
2. **Containers.** `docker rm` is insufficient — anonymous volumes persist. Use `docker volume rm` or `docker-compose down -v` only when the contained data is intentionally disposable (see LEARNINGS #154 for the destructive footgun).
4. **Database tables.** `DROP TABLE` only after confirming the data is migrated to the successor schema. Retain backups per [04.3 Disaster Recovery](../04-runbooks/04.3-disaster-recovery.md) retention rules.
5. **Backups.** Old tarballs are deleted via `srm` or `shred` on local disk, then removed from offsite (rsync `--delete` after retention window).
6. **Documents.** Old policy versions archived (do not delete) — superseding version increments, prior versions move to `archive/`.

## 4. Responsibilities

| Role | Responsibilities |
|---|---|
| **Venkat (Owner)** | Maintains the inventory doc. Performs annual audit. Approves classification disputes. Approves disposal of Confidential assets. |
| **Processbricks admin** | Updates inventory on every provisioning change (new container, new app, new DB). Verifies disposal evidence. |
| **Users** | Handle data per its classification. Report mislabeled assets to Venkat. Don't bypass classification for "convenience". |
| **Vendors** | Bound by classification rules in their contract. Disposal of Haritha data on vendor hardware follows §3.4. |

## 5. Compliance Measurement

| Check | Frequency | Owner | Source |
|---|---|---|---|
| Inventory completeness | Continuous | admin | New-asset registration cadence |
| Inventory accuracy | Annually | Venkat | Walk-through vs reality |
| Mislabeled documents | Quarterly | admin | grep + review |
| Standing Confidential assets without active owner | Quarterly | Venkat | inventory |
| Disposal evidence completeness | Per disposal | admin | disposal log |
| Backups classified Confidential | Always | admin | §3.3 |

KPI target: 100% of assets registered within 7 days of creation. Zero `UNKNOWN` classifications in the inventory.

## 6. Exceptions

The `asset-inventory.md` stub is an in-progress exception — current state is "the inventory doc does not yet exist, but every asset is known informally to Venkat". Resolution: create `asset-inventory.md` in the next batch (or sooner if Venkat prioritizes). Until then, this policy is partially aspirational; classification rules + handling rules apply even without the doc.

Future-improvement exceptions (tracked, not blocking):

- **Encrypted backups at rest.** Current tarballs are unencrypted on local + offsite. Acceptable for v1 (single-operator + offsite is private VPS); revisit if we add a third party to the trust boundary.
- **DLP / labeling enforcement.** Currently relies on humans not misclassifying. Future: pre-commit hook that scans diffs for likely-Confidential patterns (e.g., Aadhaar-like 12-digit numbers, phone numbers in fixtures).

Other exceptions follow the flow in [01-info-security](01-info-security.md#6-exceptions).

## 7. Related Documents

- [01-info-security.md](01-info-security.md) — Umbrella + exception flow.
- [02-access-control.md](02-access-control.md) — RBAC roles map to classification.
- [04-cryptography.md](04-cryptography.md) — Encryption of Confidential data in transit + at rest.
- [../04-runbooks/04.3-disaster-recovery.md](../04-runbooks/04.3-disaster-recovery.md) — Backup retention rules.
- [../../../../MEMORY.md](../../../../MEMORY.md) — Container / env inventory + credential locations.
- [../../../../.learnings/LEARNINGS.md](../../../../.learnings/LEARNINGS.md) — Lesson #154 (DB password drift = inventory rot symptom).

## 8. Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-29 | venkat-narasimha | Initial |