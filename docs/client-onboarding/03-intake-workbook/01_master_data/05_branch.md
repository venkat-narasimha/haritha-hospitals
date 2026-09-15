# Branch — Intake Sheet

**DocType:** Branch (not submittable)
**Module:** Setup / Organization
**Required fields:** 1
**Optional fields:** 0

Branch represents a physical site (e.g. Main Hospital, North Clinic, Lab Annex). It is a one-row-per-site master.

> **NOTE for this deployment:** Branch is a **stock DocType but is not populated at single-site hospital deployments** (e.g. the reference deployment has 0 Branch records; every Employee has `branch=None`). See Gotcha #12.
>
> **Recommendation:** Use this template only if the client operates multiple physical sites. Single-site hospitals do NOT need to populate Branch — leave `branch` blank on every Employee.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| branch | Branch | Data | Y | Branch A | unique | autoname=field:branch; NOTE: DocType unused at single-site deployments (see gotcha #12); template still applies for multi-site clients |

## Migration notes (from research §7)

- **Gotcha #1 — `get_doc()` doctype key:** Any future custom import script must inject `{"doctype": "Branch", ...}` before constructing the document.
- **Gotcha #12 — Branch is unused at single-site:** Branch has 0 custom fields and 0 records at single-site deployments. The template still exists for multi-site clients.
- Branch has **zero custom fields** in `haritha_hospital/fixtures/custom_field.json`.
- Import is unconditional — no FK dependencies. Safe to import in any order.

## Healthcare-specific fields

None. Branch has no custom fields in the `haritha_hospital` custom app. (Per Section 1 of research.)

> Note: The `Address` DocType (a separate DocType, not in P5 scope) DOES carry site-level custom fields (geo coordinates, contact info). For site-level details beyond a name, use Address + Link from Branch on a custom-app extension. **For the standard P5 scope, this is out of scope.**

## When to use this sheet

| Scenario | Use Branch template? |
|---|---|
| Multi-site hospital (Main + Branch clinics) | YES — one row per physical site |
| Single-site hospital | NO — skip entirely; leave `branch` blank on Employees |
| Lab/Annex separate from main building | YES — each physical location is a Branch |
| Department within a building | NO — use Department template instead |

## Common client mistakes

- Confusing Branch with Department — Branch = building/site, Department = org unit. A single Branch can contain many Departments.
- Leaving `branch` blank on Employees at multi-site deployments — defeats the purpose of the Branch master. Always populate for multi-site.
- Trying to add geo-coordinates as CSV columns — Branch has no lat/long field. Use Address DocType (out of P5 scope) for geo data.
- Renaming a Branch after Employees link to it — Links break. Rename via web UI only with cascade-update.

## Related

- **Employee** template has a stock `branch` Link (optional, leave blank at single-site).
- **Department** is the org-unit equivalent (always populated).
- For site-level geo coordinates (used by Shift Location geofencing), see `08_shift_location.csv`.
