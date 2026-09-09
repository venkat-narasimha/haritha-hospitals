# Leave Type — Intake Sheet

**DocType:** `Leave Type`
**Module:** HR / Leave Management
**Required fields:** 1
**Optional fields:** 15+

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `name` | Leave Type Name | Data | Y | "Casual Leave" | unique | autoname from this field |
| `max_leave_allocation_allowed` | Max Allocation Allowed | Int | N | 12 | ≥0 | Cap per leave period |
| `applicable_after` | Applicable After (working days) | Int | N | 0 | ≥0 | Min tenure before eligible |
| `max_consecutive_leaves_allowed` | Max Consecutive Leaves | Int | N | 3 | ≥0 | Over-limit ⇒ LWP |
| `is_carry_forward` | Is Carry Forward | Check | N | 0 | 0/1 | Carry forward unused leaves |
| `carry_forward_leaves_limit` | Carry Forward Limit | Int | N | 0 | ≥0 | Max leaves carried forward |
| `earned_leave` | Is Earned Leave | Check | N | 0 | 0/1 | Earned/credited monthly |
| `earned_leave_frequency` | Earned Leave Frequency | Select | N | "Monthly" | Monthly/Quarterly/Half-Yearly/Yearly | If earned_leave=1 |
| `is_leave_without_pay` | Is Leave Without Pay | Check | N | 0 | 0/1 | LWP flag; mutually exclusive with partially_paid |
| `is_partially_paid_leaves` | Is Partially Paid Leave | Check | N | 0 | 0/1 | Mutually exclusive with LWP |
| `fraction_of_daily_salary_per_leave` | Fraction of Daily Salary | Float | N | 0.5 | 0-1 | If partially_paid=1 |
| `is_optional_leaves` | Is Optional Leave | Check | N | 0 | 0/1 | Optional leave (e.g., restricted holidays) |
| `max_days_leave_allowed` | Max Optional Leaves | Int | N | 0 | ≥0 | If optional_leave=1 |
| `allow_negative_balance` | Allow Negative Balance | Check | N | 0 | 0/1 | Negative balance permitted |
| `allow_over_allocation` | Allow Over Allocation | Check | N | 0 | 0/1 | Does NOT override max_allocation |
| `include_holidays_within_leaves_as_leaves` | Include Holidays Within Leaves | Check | N | 0 | 0/1 | Holiday counts as leave |
| `is_compensatory` | Is Compensatory Leave | Check | N | 0 | 0/1 | Pairs with Compensatory Leave Request |
| `allow_encashment` | Allow Encashment | Check | N | 0 | 0/1 | Last-month-of-period encashment |
| `non_encashable_leaves` | Non-Encashable Leaves | Int | N | 0 | ≥0 | Min leaves retained |
| `earning_component` | Earning Component | Link → Salary Component | N | "" | must exist if encash | – |
| `leave_quota` | Leave Quota (for earned) | Float | N | 1.5 | – | Earned quota per period |
| `leave_quota_as_per` | Quota Calculated On | Select | N | "Monthly" | Monthly/Yearly | – |

## Healthcare-specific fields (custom)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `applicable_to` | Applicable To | Select | N | "All Staff" | All / Doctors / Nurses / Support |
| `requires_medical_certificate` | Requires Medical Certificate | Check | N | 0 | For Sick Leave > 2 days |
| `mc_required_after_days` | MC Required After (days) | Int | N | 2 | Threshold for requiring MC |

## Validation rules

- `name` unique.
- `is_leave_without_pay` and `is_partially_paid_leaves` are mutually exclusive (Client Script enforces).
- If `earned_leave=1`, `earned_leave_frequency` required.
- `max_consecutive_leaves_allowed ≥ 0`; setting to 0 means unlimited.

## Common client mistakes

- Setting `is_leave_without_pay=1` on Casual Leave — should be paid.
- Forgetting `earned_leave=1` on Earned Leave — earned leaves won't be credited automatically.
- Setting `max_leave_allocation_allowed=0` and `allow_over_allocation=1` — confusing; `allow_over_allocation` does NOT override `max_allocation_allowed`.
- Mixing `is_partially_paid_leaves` and `is_leave_without_pay` — invalid combination.
- Forgetting `include_holidays_within_leaves_as_leaves=1` for maternity leave (else weekends don't count).

## Standard hospital leave types to import

| name | max_leave_allocation_allowed | is_carry_forward | earned_leave | is_leave_without_pay | notes |
|---|---|---|---|---|---|
| Casual Leave (CL) | 12 | 0 | 0 | 0 | Paid short leave |
| Sick Leave (SL) | 12 | 0 | 0 | 0 | Paid; MC required >2 days |
| Earned Leave (EL) | 30 | 1 | 1 | 0 | Earned monthly; carry forward |
| Maternity Leave | 180 | 0 | 0 | 0 | 26 weeks per Indian law (for women) |
| Paternity Leave | 15 | 0 | 0 | 0 | For new fathers |
| Compensatory Off | 0 | 0 | 0 | 0 | Earned via overtime; no quota |
| Leave Without Pay (LWP) | 0 | 0 | 0 | 1 | For over-quota absence |
| Restricted Holiday | 2 | 0 | 0 | 0 | Optional; max 2 per year |
| Bereavement Leave | 5 | 0 | 0 | 0 | For family death |
