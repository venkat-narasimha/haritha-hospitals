# Branch — Intake Sheet

**DocType:** `Branch`
**Module:** HR (Stock/Accounts also use Branch)
**Required fields:** 1
**Optional fields:** 5+

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `branch` | Branch | Data | Y | "Main Hospital" | unique | The visible name |
| `company` | Company | Link → Company | N | "Haritha Hospitals Pvt Ltd" | must exist | Branch can belong to one company |

## Healthcare-specific fields (custom — recommended)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `branch_code` | Branch Code | Data | N | "MAIN" | Short code for reports (≤6 chars) |
| `branch_type` | Branch Type | Select | N | "Hospital" | Hospital / Clinic / Lab / Pharmacy / Office |
| `address_line_1` | Address Line 1 | Data | N | "123 MG Road" | For geofencing + statutory |
| `city` | City | Data | N | "Hyderabad" | – |
| `state` | State | Link → State | N | "Telangana" | Drives Holiday List selection |
| `pincode` | Pincode | Data | N | "500001" | 6-digit Indian pincode |
| `latitude` | Latitude | Float | N | 17.3850 | – |
| `longitude` | Longitude | Float | N | 78.4867 | – |
| `nabh_accredited` | NABH Accredited | Check | N | 1 | For quality reporting |
| `bed_count` | Bed Count | Int | N | 300 | Operational metric |

## Validation rules

- `branch` unique.
- `latitude`/`longitude` if set should be valid coordinates.

## Common client mistakes

- Confusing Branch with Department — Branch is a *location*, Department is a *function*.
- Missing `state` — breaks Holiday List assignment (drives per-state holiday list).

## Typical branches for a hospital chain

- Main Hospital (Hyderabad)
- North Wing / Annexe (if separate building)
- OPD Block
- Diagnostic Centre (separate location)
- Satellite Clinic 1, 2, 3 (if applicable)
