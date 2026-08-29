# Cryptography & Key Management Policy

**Policy ID:** HH-ISMS-04
**Version:** 1.0
**Effective Date:** 2026-08-29
**Owner:** Venkat Narasimha (Processbricks)
**Review Cycle:** Annual
**Last Reviewed:** 2026-08-29

## 1. Purpose

Cryptography is the last line of defense when access control fails. If a backup tarball leaks, encryption makes it useless. If a session is hijacked, TLS keeps the contents out of reach. If a DB password ends up in a Slack channel, the encryption keys determine the blast radius.

This policy defines **what** we encrypt, **with what**, **where keys live**, and **how we rotate**. It also documents the gap between current state and ideal state, because pretending everything is encrypted when it isn't would be worse than acknowledging the gap.

The 2026-08-29 prod DB password drift (LEARNINGS #154) and the related 401 incident are the cautionary tale: secrets are not constants. They live in container env vars, drift across `MEMORY.md` docs, and break in production when nobody verified. This policy treats secrets as state that must be actively maintained.

## 2. Scope

### 2.1 In scope

- **Database credentials.** MariaDB root passwords for `erp-{prod,dev,qa}-db-1`, `erpdev-mariadb-1`, and any future DBs.
- **SSH keys.** `/root/.openclaw/ssh_key` (VPS access), `/root/.openclaw/venkat_vps_key` (offsite), and any future per-host keys.
- **API tokens.** Frappe API tokens, GitHub PATs, duckdns update tokens.
- **SSL/TLS certificates.** Let's Encrypt certs for `*.duckdns.org` subdomains (`pberpPROD.duckdns.org`, `pberpDEV.duckdns.org`, `pberpQA.duckdns.org`).
- **Sensitive fields at rest** (target — see §3.6 future improvement).
- **Backup tarballs** (target — see §3.6 future improvement).

### 2.2 Out of scope

- Production HTTPS termination is handled by Frappe/Nginx with Let's Encrypt certs — the cryptographic primitives are upstream's responsibility.
- Disk-level encryption of the VPS — depends on hosting provider; not currently enabled.
- Email encryption (PGP/SMIME) — we don't send Confidential data over email by policy.

## 3. Policy Statement

### 3.1 Storage of secrets

1. **Database passwords** live in **container environment variables**, not files on disk. Specifically:
   - `MYSQL_ROOT_PASSWORD` on `erp-{env}-db-1`.
   - Set via `docker-compose.yml` `environment:` blocks under `frappeclaw/frappeclaw-data` workspace.
   - **Never** written to `MEMORY.md`, runbooks, Slack, or git (even temporarily).
   - **Verification pattern** (per LEARNINGS #154): `docker exec erp-prod-db-1 printenv MYSQL_ROOT_PASSWORD` → compare to access register. Run quarterly.
2. **SSH private keys** live in `/root/.openclaw/ssh_key` (or per-host equivalent), passphrase-protected, mode `0600`. **Not** copied to other machines. **Not** checked into git. **Not** transmitted over email/Slack.
3. **API tokens** live in:
   - OS keychain on Venkat's machine, **or**
   - Container env vars (for service-account tokens used by cron/automation), **or**
   - The `apps/haritha_hospital/haritha_hospital/.env` file (gitignored, mode `0600`) for app config.
   - **Never** in source code, **never** in fixtures, **never** in `bench site-config` (the site_config.json is itself checked, so tokens go in `.env` not there).
4. **TLS private keys** live in `/etc/letsencrypt/live/{domain}/privkey.pem` (managed by certbot). Read by Nginx only. Mode `0600`.

### 3.2 Cryptographic algorithms

1. **SSH keys:** `ed25519` preferred; `4096-bit RSA` acceptable. No DSA, no 1024/2048-bit RSA, no ECDSA with weak curves.
2. **TLS:** TLS 1.2+ only. TLS 1.0/1.1 disabled at the Nginx level. Strong ciphers only (Mozilla "Intermediate" or "Modern" profile).
3. **Hashing:** SHA-256 for fingerprints and integrity checks. MD5 forbidden even for non-security checks (build collisions cause confusion).
4. **Password storage (in-app):** Frappe uses `bcrypt`-equivalent via `werkzeug.security.generate_password_hash`. We do not implement our own.
5. **Symmetric encryption** (for backup tarballs — future): `aes-256-gcm` with key from a passphrase-protected key file.

### 3.3 TLS in transit

1. **Public sites** (`*.duckdns.org`): TLS via Let's Encrypt. Cert renewal automated (certbot timer or equivalent). 30-day expiry alarm via daily heartbeat.
2. **Internal services** (backend ↔ db, backend ↔ redis): TLS is **not** used; isolation relies on Docker network namespace (`172.27.0.0/16` for prod). Acceptable because the network is single-tenant. If a second operator joins, we re-evaluate.
3. **Admin web UI** (`/desk`, `/api`): fronted by Nginx with TLS. Admin operations over HTTP are refused (HSTS preload eventually).
4. **No `http://` for production endpoints.** A redirect from `http://` to `https://` is fine; serving data over HTTP is not.

### 3.4 SSH key management

1. **Generation:** `ssh-keygen -t ed25519 -a 100 -C "haritha-<purpose>-<date>"`. Passphrase required.
2. **Distribution:** Public key only, out-of-band (paper, voice, signed email — never the same channel we're using SSH for).
3. **Rotation:** Annually. Old key remains in `authorized_keys` for 7 days as overlap, then removed.
4. **Revocation on personnel change:** Within 1 hour of role termination, remove from all `authorized_keys` files (VPS + offsite + any other host).
5. **Compromise response:** Treat as SEV-1. Generate replacement, distribute, revoke old, audit recent usage (`last`, `auth.log`). See [07-incident-management.md](07-incident-management.md) and [../04-runbooks/04.4-incident-response.md](../04-runbooks/04.4-incident-response.md).

### 3.5 API token management

1. **Per-user tokens** (GitHub PATs, Frappe user tokens): scoped to minimum permissions. Rotation annually. Revoked immediately on personnel change.
2. **Service-account tokens** (cron, integrations): scoped to a single endpoint or operation. Rotation annually or on personnel change of the responsible engineer. Stored in container env vars (see §3.1.3).
3. **Pre-commit secret scanning** blocks any pattern resembling `password=`, `token=`, `BEGIN RSA PRIVATE KEY`, etc. in staged diffs. Bypass requires Venkat's per-PR approval.

### 3.6 Encryption at rest — current state + future

**Current state (v1):**

- Database at rest: MariaDB data directory on a host volume. **Not encrypted** (relies on disk + host access control).
- Backup tarballs: stored on local backup volume + offsite VPS. **Not encrypted** (reliance is on the privacy of those hosts).
- Sensitive fields in tables (salary, patient diagnosis details): **not encrypted at column level**.

**Why this is acceptable for now:**

- Single-operator trust model. Both VPS providers are reputable; offsite VPS is in Venkat's name.
- No portable devices touch the data (per [01-info-security](01-info-security.md) §3.5).

**Future improvements** (tracked, prioritized post-Batch 2):

1. Encrypt backup tarballs with `age` or `gpg --symmetric` using a key stored in a sealed envelope + offsite. Cost: low. Risk reduction: high (if offsite VPS is compromised, data still protected).
2. MariaDB transparent data encryption (`aria_encrypt_tables` for Aria, `innodb_encrypt_tables` for InnoDB). Cost: medium (requires key management). Risk reduction: medium.
3. Column-level encryption for `tabSalary Slip.net_pay` and patient diagnosis fields. Cost: high (schema change, search/compliance tradeoffs). Risk reduction: high if disk is reused.

### 3.7 No secrets in git

1. **Pre-commit hook** blocks patterns matching `password=`, `secret=`, `token=`, `BEGIN.* PRIVATE KEY`, Aadhaar-like 12-digit numbers, 16-digit debit card numbers. Hook lives in `scripts/hooks/pre-commit` and is wired via `.git/hooks/pre-commit`.
2. **`.gitignore`** excludes `*.env`, `*.pem`, `*.key`, `secrets/`, `frappe-bench/sites/*/site_config.json`.
3. **PR review** includes a "secrets in diff" check by the reviewer. (Future: a CI job that runs `git-secrets` against the merge commit.)
4. **History rewrite** if a secret ever lands: rotate the secret first (assume it's leaked), then `git filter-repo` to scrub history, then force-push with a security advisory in the PR.

### 3.8 No secrets in plain text on Slack / email

1. **DB passwords:** Never typed in Slack, even in private DMs. Use the container env pattern. If you need to share an env var value, share the `docker exec ... printenv` command, not the output.
2. **SSH keys:** Never shared over chat. Public keys go in repos or via signed email.
3. **API tokens:** Same — share the source (`docker exec ... printenv`) or the env-var name, not the value.
4. **Exception:** True emergencies (prod is down, no other way). Verbal handoff via phone, then rotate the secret within 24h. Post-incident review covers prevention.

## 4. Responsibilities

| Role | Responsibilities |
|---|---|
| **Venkat (Owner)** | Owns the secret register (where each secret lives, last rotation date). Approves emergency secret rotation. Performs annual key audit. Owns the offsite backup VPS access. |
| **Processbricks admin** | Implements secret rotation (rotates DB password, regenerates API tokens). Runs the pre-commit hook scan monthly. Verifies container env vars quarterly (LEARNINGS #154 pattern). |
| **Users** | Never request a secret over Slack/email. Never store a secret on a personal device. Report a suspected leak within 1 hour. |
| **Vendors** | Bound by §3.1 + §3.7. No secret in vendor-controlled systems without written approval + rotation cadence. |

## 5. Compliance Measurement

| Check | Frequency | Owner | Source |
|---|---|---|---|
| Container env vars match access register | Quarterly | admin | `docker exec ... printenv` vs register |
| TLS cert expiry > 14 days | Daily | admin | certbot + heartbeat |
| Pre-commit hook active on all clones | Continuous | admin | `git config core.hooksPath` |
| SSH key age ≤ 365 days | Annually | Venkat | key creation date |
| API token age ≤ 365 days | Annually | admin | token issuance date |
| Backup tarballs encrypted (future) | n/a | n/a | when §3.6 implemented |
| `git secrets` scan clean | Monthly | admin | `git grep -iE 'password|secret|token' -- ':!**/docs/**'` |
| TLS grade (ssllabs / equivalent) ≥ A | Annually | admin | external scan |

KPI target: zero secrets in git history; zero plaintext secrets in Slack/email; zero stale (un-rotated) secrets older than the policy max.

## 6. Exceptions

1. **Emergency credential access.** When prod is down and we need to read the current DB password, follow the emergency-access flow in [02-access-control §6](02-access-control.md#6-exceptions): log the action, rotate within 24h, post-incident review.
2. **Vendor-bound systems** that require a secret to be embedded (e.g., a SaaS integration with no env-var hook). Documented case-by-case in the secret register with rotation cadence; quarterly audit.
3. **Encrypted backups at rest** is a tracked exception (§3.6) — accepted risk for v1, scheduled for v2.
4. **All other exceptions** follow [01-info-security §6](01-info-security.md#6-exceptions).

## 7. Related Documents

- [01-info-security.md](01-info-security.md) — Umbrella + emergency flow.
- [02-access-control.md](02-access-control.md) — How authentication secrets are protected.
- [03-asset-management.md](03-asset-management.md) — What is Confidential (drives what must be encrypted).
- [../04-runbooks/04.3-disaster-recovery.md](../04-runbooks/04.3-disaster-recovery.md) — Backup storage + restoration.
- [../04-runbooks/04.4-incident-response.md](../04-runbooks/04.4-incident-response.md) — Compromise response.
- [../../../../.learnings/LEARNINGS.md](../../../../.learnings/LEARNINGS.md) — Lesson #154 (DB password drift = the canonical case for this policy).
- [../../../../MEMORY.md](../../../../MEMORY.md) — **CAUTION:** `MEMORY.md` has historical (now stale) hardcoded DB passwords — never trust literals from MEMORY.md without re-verifying via container env.

## 8. Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-29 | venkat-narasimha | Initial |