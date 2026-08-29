# Access Control Policy

**Policy ID:** HH-ISMS-02
**Version:** 1.0
**Effective Date:** 2026-08-29
**Owner:** Venkat Narasimha (Processbricks)
**Review Cycle:** Annual
**Last Reviewed:** 2026-08-29

## 1. Purpose

A hospital system that lets the wrong person in — or keeps the right person in after they leave — fails patients. We need:

- **Authentication**: proof that the person is who they say they are.
- **Authorization**: proof that the person is allowed to do what they're trying to do.
- **Accountability**: an audit trail that ties actions to identities.

Without all three, we cannot answer "who deleted this patient record?" or "who accessed this salary slip at 2 AM?". This policy defines how we grant, manage, and revoke access across every Haritha touchpoint.

The 2026-08-29 DB password drift incident (LEARNINGS #154) is a reminder: even the most basic access primitive — knowing the current prod DB password — can silently rot if we don't verify it. This policy treats credentials as living state, not constants.

## 2. Scope

Every identity-bearing system:

- **ERPNext / haritha_hospital app.** Production (`pberpprod`), Dev (`pberpdev`), QA (`pberpqa`). Each has its own `tabUser` table.
- **MariaDB.** `erp-prod-db-1`, `erp-dev-db-1`, `erp-qa-db-1` (VPS), plus `erpdev-mariadb-1` on Venkat's dev-erp box.
- **GitHub.** `venkat-narasimha/haritha-hospitals` (push), read-only collaborators.
- **VPS host (`vps-3248b821`).** User `vijay` (admin), SSH key from `/root/.openclaw/ssh_key`.
- **Container orchestration.** `docker` group membership, `docker exec` privileges.
- **Offsite backup.** `venkat@135.125.196.35`, SSH key from `/root/.openclaw/venkat_vps_key`.
- **Frappe Bench + scheduler.** Backend containers expose `bench` commands; access is via `docker exec` on the host.
- **DuckDNS.** Dynamic DNS update token (currently in `frappeclaw` compose env).
- **Let's Encrypt.** Cert issuance via certbot; renewal is automated.

## 3. Policy Statement

### 3.1 Principles

1. **Least privilege.** New users get the minimum role set that lets them do their job. Default for new app users: `Employee` role (read own records + submit attendance). Default for new DB users: no account (use root from inside the container network).
2. **Role-Based Access Control (RBAC).** Permissions are grouped into Frappe roles, then users are assigned roles. No per-document ACL hacks. Roles are defined in `apps/haritha_hospital/haritha_hospital/hooks.py` and exported as fixtures.
3. **No shared accounts.** Every human has their own `tabUser`. "Reception shift account" is forbidden; create per-user accounts instead. Service accounts (cron, integrations) are named after their function (`nightly-backup`, `duckdns-updater`), not shared.
4. **Defense in depth.** Two controls must fail before data leaks — e.g., MFA + VPN, or SSH key + IP allowlist, or RBAC role + row-level filter.

### 3.2 Authentication

1. **Passwords (Frappe app users).**
   - Minimum 12 characters.
   - Mix of upper + lower + digit + symbol (Frappe enforces this server-side).
   - Rotation every 90 days. Frappe's password expiry setting enforces this.
   - No reuse across Haritha and personal accounts.
2. **Multi-factor authentication (MFA).**
   - **Required** for any user with `System Manager` or `Administrator` role on production.
   - **Required** for any user with `ALL` role in Frappe.
   - TOTP preferred over SMS (no SMS delivery fee, no SIM swap risk).
3. **Database credentials.**
   - Stored in **container environment variables** (`MYSQL_ROOT_PASSWORD`), not in files on disk. LEARNINGS #154 documents why hardcoded values in `MEMORY.md` went stale.
   - Quarterly verification: `docker exec erp-prod-db-1 printenv MYSQL_ROOT_PASSWORD` must match the access register entry.
4. **SSH keys.**
   - `ed25519` or `4096-bit RSA`. No DSA, no 1024-bit RSA.
   - Passphrase-protected at rest. `ssh-agent` is fine for session use; raw key on disk without passphrase is forbidden.
   - Rotation annually. Old key remains valid for 7 days as overlap, then is revoked.
5. **GitHub.** Personal access tokens are fine for HTTPS; SSH key (the same `/root/.openclaw/ssh_key`) is preferred. Token rotation annually; tokens stored in OS keychain or container env, never in repo.
6. **API tokens.** Generated per-user in Frappe, scoped to specific API endpoints, rotated annually. Service-account tokens are rotated on every personnel change.

### 3.3 Authorization

1. **Production write access.** Limited to users with `System Manager` role. Currently: Venkat (only). All `INSERT`/`UPDATE`/`DELETE` against `tab*` tables by non-System-Managers go through standard form submissions (audit-logged).
2. **Direct DB write access.** Read-only `SELECT` is permitted for analysts via a dedicated DB user (`haritha_ro`). All `INSERT`/`UPDATE`/`DELETE` require explicit elevation, which is logged in `/var/log/erp-prod-db-access.log`.
3. **SSH to VPS.** `vijay` user has sudo. No other SSH users. Root login via SSH is disabled (`PermitRootLogin no` in `/etc/ssh/sshd_config`).
4. **Container exec.** Anyone with `docker` group membership can `docker exec` any container. Membership is `vijay` only. No passwordless `docker` for non-admins.
5. **Git push.** Direct push to `main` is restricted to Venkat. All other contributors PR from feature branches; CI runs lint + migrate-dry-run.

### 3.4 Lifecycle

1. **Provisioning.** New user request → Venkat creates `tabUser` with minimum role + sets password expiry + enrolls in MFA. Entry logged in `docs/phase6/09-compliance/access-register.md`.
2. **Modification.** Role changes require Venkat approval. Role additions/removals audited.
3. **Deprovisioning.** When a user leaves:
   - `tabUser.enabled = 0` within 1 hour of departure notification.
   - `tabUser.new_password` rotated (in case of stale session).
   - Personal SSH keys removed from `~/.ssh/authorized_keys` on VPS + offsite.
   - Personal API tokens revoked in Frappe.
   - Entry marked `INACTIVE` in access register.
4. **Quarterly review.** Venkat reviews the full access register. Anyone without a documented business need is removed.
5. **Failed login handling.** After 5 failed logins in 10 minutes, the account is locked for 30 minutes. Lockouts are alerted (admin reviews daily). Repeated lockouts for the same account trigger SEV-3 review.

## 4. Responsibilities

| Role | Responsibilities |
|---|---|
| **Venkat (Owner)** | Approves all role grants beyond defaults. Quarterly access reviews. Final escalation on account compromise. Owns the access register. |
| **Processbricks admin** | Implements Frappe role/permission changes (hooks.py + custom app). Monitors failed-login alerts. Verifies DB passwords quarterly. |
| **Users** | Protect their own credentials. Don't share. Don't bypass MFA. Don't leave sessions unattended on shared workstations. Report compromise within 1 hour. |
| **Vendors** | Use scoped service accounts, never their personal credentials. Rotate credentials on personnel change. |

## 5. Compliance Measurement

| Check | Frequency | Owner | Source of truth |
|---|---|---|---|
| Access register reconciled to `tabUser` | Quarterly | Venkat | `tabUser` table |
| DB passwords verified against container env | Quarterly | admin | `docker exec ... printenv MYSQL_ROOT_PASSWORD` |
| Failed login rate | Daily review | admin | `frappe-bench/logs/*.log` |
| Account lockouts | Daily review | admin | `tabUser` lock flags |
| SSH key age | Annually | Venkat | key creation timestamp |
| API token age | Annually | Venkat | `tabAPI Token` table |
| Users with `System Manager` role | Monthly | Venkat | `tabHasRole` |
| GitHub collaborators | Quarterly | Venkat | repo settings |

KPI target: zero standing privileges beyond what's documented in the access register. Zero plaintext credentials outside container envs.

## 6. Exceptions

Temporary elevated access (e.g., "I need System Manager for 4 hours to fix a payroll bug"):

1. Requester files a ticket naming the role, the reason, the time window, and the audit log they'll generate.
2. Venkat grants the role in Frappe (manual SQL or UI).
3. The role is **scheduled to auto-expire** — Frappe has no native TTL, so we use a calendar reminder + manual revocation. (Future: implement `valid_upto` field on `tabHasRole`; tracked as future improvement.)
4. All actions during the elevated window are logged and reviewed at the next access review.
5. Exceptions for production DB write access: the same flow, plus a post-window audit of every `INSERT`/`UPDATE`/`DELETE` against the affected tables.

Emergency access (e.g., production is down and Venkat is unreachable): the on-call admin may elevate themselves, log the action in `/var/log/erp-emergency-access.log` with a written justification, and notify Venkat within 1 hour of regaining contact. Post-incident review covers prevention.

## 7. Related Documents

- [01-info-security.md](01-info-security.md) — Umbrella policy.
- [03-asset-management.md](03-asset-management.md) — Data classification (drives role defaults).
- [04-cryptography.md](04-cryptography.md) — Secret storage + rotation.
- [../04-runbooks/04.4-incident-response.md](../04-runbooks/04.4-incident-response.md) — SEV-1 lockout / compromise response.
- [../../../../.learnings/LEARNINGS.md](../../../../.learnings/LEARNINGS.md) — Lesson #154 (DB password drift).
- [../../../../MEMORY.md](../../../../MEMORY.md) — Container naming + credential verification commands.

## 8. Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-29 | venkat-narasimha | Initial |