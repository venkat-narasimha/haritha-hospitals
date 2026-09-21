# HR Settings — Configuration Checklist

**Module:** HR
**Phase:** 5 — Configuration, Integrations & UAT
**DocType:** `HR Settings`
**Path:** Home → HR → HR Settings

## Pre-requisites

- [ ] Sandbox site provisioned
- [ ] All 15 master-data DocTypes imported and signed off
- [ ] Custom fields added via Customize Form (medical_council_reg_no, blood_group, etc.)

## Configuration items

### Employee naming and numbering

- [ ] **Employee Naming** — By Naming Series / By Employee Number / By First Name (default: By Naming Series)
- [ ] **Employee Number Series** — e.g., `HRH-EMP-.YYYY.-.#####`
- [ ] **Retiree Naming Series** (if applicable)

### Leave settings

- [ ] **Leave Approval Required** — Yes/No (default: Yes)
- [ ] **Leave Approval Mandatory Before Submission** — Yes/No (default: No)
- [ ] **Leave Status Notification** — Send to leave approver / leave applicant / both
- [ ] **Leave Allocation Required** — Yes (recommended)
- [ ] **Restrict Backdated Leaves** — Days allowed (e.g., 7 days)
- [ ] **Allow Negative Leave Balance** — Yes/No (default: No; recommended: No for hospital)

### Attendance settings

- [ ] **Allow Geolocation Tracking** — **YES (required for Shift Location geofencing)**
- [ ] **Shift Request Approval Required** — Yes (recommended for hospital)
- [ ] **Auto Assign Shift** — Yes/No
- [ ] **Default Holiday List** — link to your Hospital Holiday List
- [ ] **Default Working Hours** — e.g., 8 (used for attendance calculation)
- [ ] **Enable Check-in Auto Attendance** — Yes (for biometric-driven auto-attendance)
- [ ] **Check-in Validation Grace Period** — minutes (e.g., 15)

### Payroll link

- [ ] **Payroll Settings Link** — confirm Payroll Settings is configured (separate checklist)

### Standard working hours

- [ ] **Standard Working Hours** — e.g., 48 (rotational hospital) / 40 (admin) / 24 (on-call)
- [ ] **Work Days** — Mon–Sat / Mon–Sun / Custom

### Email and notifications

- [ ] **Send Notification for Leave Status** — Yes
- [ ] **Send Birthday Reminders** — Yes (nice-to-have)
- [ ] **Email Salary Slip to Employee** — Yes (if payroll in scope)

### Workflow for Leave Application

> **HRMS v16 gap** (Sep 17–21 audit, Item 7): HRMS v16 does **NOT** ship with a default Workflow for Leave Application. Without one, `Leave Application.submit()` is blocked by the controller until `status` is set to `"Approved"` or `"Rejected"`, and the web UI does **NOT** expose Approve / Reject buttons.

The Leave Application DocType relies on a Workflow document to drive its `status` field and expose the Approve / Reject actions. HRMS v16 ships only the DocType — you must create the Workflow manually.

**Workflow header** (Setup → Workflow → New):

| field | value |
|---|---|
| Workflow Name | `Leave Approval` (or your preferred label) |
| Document Type | `Leave Application` |
| Is Active | ✓ |
| Send Email Alert | optional — depends on **Email Account** (see below) |

**States** (in order):

| State | doc_status | allow_edit |
|---|---|---|
| Pending Approval | 0 | 1 |
| Approved | 1 | 0 |
| Rejected | 1 | 0 |
| Cancelled | 2 | 0 |

**Transitions:**

| from_state | to_state | action | allowed_role |
|---|---|---|---|
| Pending Approval | Approved | Approve | Leave Approver (or HR Manager) |
| Pending Approval | Rejected | Reject | Leave Approver (or HR Manager) |
| Approved | Cancelled | Cancel | Leave Applicant (or HR Manager) |
| Rejected | Cancelled | Cancel | Leave Applicant (or HR Manager) |

**After saving the Workflow**, the Leave Application form gains **Approve** / **Reject** buttons (top-right of the form) and the system can transition `status` correctly on submit. Without this Workflow, the only path to an Approved record is the console workaround below.

#### Console-path workaround (UAT / data-fix only)

If you cannot create the Workflow (e.g., permissions locked, UAT cycle), you can manipulate `status` directly via the Frappe console as a stopgap:

```python
import frappe
doc = frappe.get_doc("Leave Application", "HR-LAP-2026-00001")
doc.status = "Approved"
doc.flags.ignore_validate_update_after_submit = True
doc.save(ignore_permissions=True)
frappe.db.commit()
```

> **Warning:** This bypasses all approval audit trails. Use only for UAT / data-fix scenarios. Production approval must go through the Workflow.
>
> **Workbook dependency:** This Workflow pairs with Department → `leave_approvers` child table (see [`01_master_data/01_department.md`](../01_master_data/01_department.md) §Leave Approvers). The Workflow's `allowed_role` should match the Users you put in that child table.

### Email Account

> **HRMS v16 gap** (Sep 17–21 audit, Item 7): For `HR Settings.leave_approval_notification_template` (and other Leave / Payroll / Attendance email notifications) to actually send, at least **one** `Email Account` record must be configured. Without it, notifications are silently dropped — the email queue logs the failure but the user sees no error.

Path: Setup → Email Account → New Email Account.

| field | required | example | notes |
|---|---|---|---|
| Email Account ID | Y | `notifications@hospital.example` | unique per row |
| Email Address | Y | `notifications@hospital.example` | |
| Password / App Password | Y | (app password, not raw password) | use Gmail App Passwords for Gmail; SMTP creds for SES / SendGrid / Postmark |
| SMTP Server | Y | `smtp.gmail.com` | depends on provider |
| Port | Y | `587` (TLS) / `465` (SSL) | |
| Enable Outgoing | Y | ✓ | required to send; receiving is optional |
| Default Outgoing | Y | ✓ | required so HRMS uses this account for all notifications |
| Service | optional | `Gmail` / `SendGrid` / `SES` / `None` | pre-fills SMTP defaults |

**Validate after save:**

- Open the Email Account → click **Send Test Email** → enter a recipient → confirm receipt.
- If test fails: check SMTP creds, app-password vs raw-password, firewall egress on port 587/465, and the Email Domain whitelist in Setup → Email Domain.

**Without a working Email Account**, the following HR Settings toggles silently no-op:

- `leave_approval_notification_template`
- `send_notification_for_leave_status`
- `send_birthday_reminders`
- `email_salary_slip_to_employee`

### Role and permissions

- [ ] **HR User Role** — assigned to HR team
- [ ] **HR Manager Role** — assigned to HR Lead
- [ ] **Employee Self-Service Role** — assigned to all employees (read-only own records)

## Validation tests

After configuration, verify:

- [ ] Log in as HR Manager → can view/edit all Employee records
- [ ] Log in as Department Manager → can only view/edit Employees in own Department
- [ ] Log in as Employee → can view own record + apply for leave + view own attendance
- [ ] Apply for leave → routes to Leave Approver per Department
- [ ] Approve leave → balance decrements correctly
- [ ] Biometric check-in via mobile app → geofence validates against Shift Location
- [ ] Auto-attendance processes correctly after grace period
- [ ] Half-day and absent thresholds trigger correctly

## Sign-off

Configured by: _________________________  Date: ___________

Verified by:   _________________________  Date: ___________

Client HR Lead approval: _________________________  Date: ___________
