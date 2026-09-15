# Leave Policy — Intake Sheet

**DocType:** Leave Policy (not submittable)
**Module:** HR / Leaves
**Required fields:** 2 (`title` + child `leave_policy_details`)
**Optional fields:** 1

A Leave Policy bundles one or more Leave Types with allocation rules into a named package (e.g. "Standard Policy", "Senior Policy"). Employees are assigned a Policy via Leave Policy Assignment (a separate DocType, out of P5 scope).

> **Import flow:** This CSV imports the **parent** Leave Policy record. The child `leave_policy_details` rows (one per Leave Type assigned to this policy) are imported **separately** via Data Import on the `Leave Policy Detail` child DocType OR via the Frappe web UI.

## Field reference (parent — Leave Policy)

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| title | Title | Data | Y | Standard Policy | unique | autoname=field:title |
| leave_policy_details | Leave Policy Details | Table | N |  | child rows required | child table Leave Policy Detail - see Migration notes; do NOT add in this CSV (Data Import handles via separate upload) |
| amended_from | Amended From | Link→Leave Policy | N |  | must exist if set | for amendment workflow only |

## Child table: leave_policy_details (separate Data Import)

The `leave_policy_details` child table is a Table field on Leave Policy, pointing at the `Leave Policy Detail` child DocType. **One row per Leave Type included in this policy.** Recommended CSV columns for the child import:

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| leave_type | Leave Type | Link | Y | Casual Leave | must exist | the Leave Type this policy grants |
| annual_allocation | Annual Allocation | Float | Y | 12 | >= 0 | leaves granted per year |
| parent | Parent Leave Policy | Link | Y | Standard Policy | must exist | reference back to the parent record |
| parenttype | Parent Type | Data | Y | Leave Policy | = "Leave Policy" | constant for this child table |

> **Pattern:** For a "Standard Policy" with 12 Casual + 6 Sick + 0 Earned, you would import 3 child rows.

## Migration notes (from research §7)

- **Gotcha #14 — leave module is configured but unpopulated:** Single-site deployments typically have 0 Leave Policies. The template exists for forward-compatibility when leave transactions begin.
- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Leave Policy", ...}` before constructing the document.
- Leave Policy has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.

## Healthcare-specific fields

None. Leave Policy has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

## When to use this sheet

| Scenario | Use Leave Policy template? |
|---|---|
| Setting up structured leave grants by employee class | YES — one row per policy |
| Single uniform leave grant for all employees | YES — one row only with child rows for each leave type |
| Granular per-employee leave amounts | NO — use Leave Allocation template |

## Common client mistakes

- Omitting the child `leave_policy_details` rows — policy exists but assigns zero leaves. Always populate children.
- Setting `annual_allocation = 0` for a Leave Type the policy is supposed to grant — defeats the purpose. Use a positive value or omit that Leave Type from the policy.
- Linking to a `Leave Type` that does not exist — fails LinkValidationError. Import Leave Types first.
- Creating two policies with the same `title` — autoname collision.

## Related

- **Leave Type** is referenced in the `leave_policy_details` child table.
- **Leave Allocation** template's `leave_policy` Link points here (optional).
- **Leave Policy Assignment** (separate DocType, OUT OF P5 SCOPE) is the linking record between an Employee and a Policy.
