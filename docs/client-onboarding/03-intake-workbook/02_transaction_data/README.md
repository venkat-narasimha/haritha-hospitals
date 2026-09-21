# Transactional Data Templates

This directory contains templates for **per-employee / per-record** transactional data:

| # | Template | Description |
|---|---|---|
| 14 | `14_leave_allocation` | Per-employee annual leave balance setup |
| 15 | `15_shift_assignment` | Per-employee shift assignment (active period) |
| 16 | `16_attendance` | Per-employee per-day attendance record |
| 17 | `17_employee_checkin` | Per-employee punch (IN/OUT) record |
| 18 | `18_leave_application` | Per-employee leave request |
| 19 | `19_leave_ledger_entry` | System-generated leave ledger (auto-created on allocation/leave submission) |

These templates document **multi-row data** that HRMS holds per employee or per record. They complement the one-time setup templates in `../01_master_data/` (Company, Department, Holiday List, Skill, etc.).

## Import guidance

Use **Data Import** tool (Setup → Data Import → New Import) or the per-DocType bulk-create tool (e.g., "Mark Attendance" for Attendance). CSV columns match the DocType's actual field names.

See `../01_master_data/` for one-time setup templates.
