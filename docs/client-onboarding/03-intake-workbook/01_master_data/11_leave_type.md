# Leave Type — Intake Sheet

**DocType:** Leave Type (not submittable)
**Module:** HR / Leaves
**Required fields:** 1
**Optional fields:** 22+

Leave Type is a master defining each category of leave (Casual, Sick, Earned, etc.). It carries the policy flags (carry-forward, LWP, optional, compensatory, earned, encashment, etc.) that govern Leave Allocation and Leave Application behavior.

> **Production note:** Standard Indian-employer set is 6-7 types: Casual Leave (carry-forward=1), Sick Leave, Earned Leave, Leave Without Pay (lwp=1), Maternity Leave, Paternity Leave, Compensatory Leave.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| leave_type_name | Leave Type Name | Data | Y | Casual Leave | unique | autoname=field:leave_type_name |
| max_leaves_allowed | Maximum Leave Allocation Allowed per Leave Period | Float | N | 12 | >= 0 | per-period cap (0 = unlimited at type level) |
| applicable_after | Allow Leave Application After (Working Days) | Int | N | 0 | >= 0 | min service days before request |
| max_continuous_days_allowed | Maximum Consecutive Leaves Allowed | Int | N | 0 | >= 0 | 0 = unlimited |
| is_carry_forward | Is Carry Forward | Check | N | 0 | 0/1 | 1 if unused leaves carry to next period |
| is_lwp | Is Leave Without Pay | Check | N | 0 | 0/1 | 1 marks this as unpaid leave |
| is_optional_leave | Is Optional Leave | Check | N | 0 | 0/1 | 1 for optional/restricted holidays |
| allow_negative | Allow Negative Balance | Check | N | 0 | 0/1 | 1 allows over-draw |
| include_holiday | Include holidays within leaves as leaves | Check | N | 0 | 0/1 | 1 counts holidays inside leave span |
| is_compensatory | Is Compensatory | Check | N | 0 | 0/1 | 1 marks this as comp-off |
| expire_carry_forwarded_leaves_after_days | Expire Carry Forwarded Leaves (Days) | Int | N | 0 | >= 0 | 0 = never expire |
| allow_encashment | Allow Encashment | Check | N | 0 | 0/1 | 1 allows encashment on exit |
| earning_component | Earning Component | Link→Salary Component | N |  | must exist if set | link to Salary Component for payroll |
| is_earned_leave | Is Earned Leave | Check | N | 0 | 0/1 | 1 marks this as accrual-based |
| earned_leave_frequency | Earned Leave Frequency | Select | N |  | Monthly / Quarterly / Half-Yearly / Yearly | only meaningful if is_earned_leave=1 |
| rounding | Rounding | Select | N |  | 0.25 / 0.5 / 1.0 | leave-day rounding granularity |
| maximum_carry_forwarded_leaves | Maximum Carry Forwarded Leaves | Float | N | 0 | >= 0 | 0 = no cap |
| is_ppl | Is Partially Paid Leave | Check | N | 0 | 0/1 | 1 for partially-paid leaves |
| fraction_of_daily_salary_per_leave | Fraction of Daily Salary per Leave | Float | N | 0 | 0 to 1 | only if is_ppl=1 |
| allow_over_allocation | Allow Over Allocation | Check | N | 0 | 0/1 | 1 to bypass allocation cap |
| allocate_on_day | Allocate on Day | Select | N | First Day | First Day / Last Day / Date of Joining | allocation timing |
| max_encashable_leaves | Maximum Encashable Leaves | Int | N | 0 | >= 0 | 0 = unlimited |
| non_encashable_leaves | Non-Encashable Leaves | Int | N | 0 | >= 0 | floor of non-encashable balance |

## Migration notes (from research §7)

- **Gotcha #14 — leave module is configured but unpopulated:** 7 Leave Types typically exist at single-site deployments (Casual, Sick, Earned, LWP, Maternity, Paternity, Compensatory), but 0 Leave Policies / Leave Periods / Leave Allocations / Leave Applications. Leave Allocation / Application / Ledger templates will become useful only when leave transactions begin.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Leave Type", ...}` before constructing the document.
- Leave Type has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.

## Healthcare-specific fields

None. Leave Type has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Leave Type template? |
|---|---|
| First-time leave-module setup | YES — populate standard 6-7 types |
| Adding a new leave category | YES — append row |
| Renaming an existing category | NO — rename via web UI (breaks Links) |
| Setting per-employee allocations | NO — use Leave Allocation template |

## Common client mistakes

- Setting `max_leaves_allowed = 0` expecting it to mean "unlimited" — actually means "0 days allowed". Use a large number or leave at 0 only if Leave Allocation sets the actual cap per employee.
- Setting `is_lwp = 1` AND `is_carry_forward = 1` together — contradictory. LWP leaves don't carry forward (they're unpaid).
- Setting `is_earned_leave = 1` without setting `earned_leave_frequency` — accrual logic fails silently.
- Setting `is_ppl = 1` without setting `fraction_of_daily_salary_per_leave` — partial-pay calculation divides by zero.
- Linking to an `earning_component` Salary Component that does not exist — fails LinkValidationError.

## Related

- **Leave Policy** template's `leave_policy_details` child references Leave Type.
- **Leave Allocation** template's `leave_type` Link points here.
- **Leave Application** template's `leave_type` Link points here.
