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
