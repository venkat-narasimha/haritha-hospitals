# Holiday List — Intake Sheet

**DocType:** `Holiday List` (parent) + `Holiday` (child table)
**Module:** HR
**Required fields:** 3 (parent) + 1 (per child row)
**Optional fields:** 5

## Parent DocType field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `holiday_list_name` | Holiday List Name | Data | Y | "Telangana 2026" | unique | Visible name |
| `from_date` | From Date | Date | Y | "2026-01-01" | YYYY-MM-DD | Start of period |
| `to_date` | To Date | Date | Y | "2026-12-31" | YYYY-MM-DD, ≥from_date | End of period |
| `country` | Country | Link → Country | N | "India" | auto-fills state list | For auto-helper |
| `subdivision` | Subdivision | Link | N | "Telangana" | Indian state | For auto-helper |
| `weekly_off` | Weekly Off | Select | N | "Sunday" | Sun–Sat | One-click fill (uses `holidays` PyPI) |
| `holidays` | Holidays (child table) | Table | Y | (see below) | each row: date + description | REQUIRED child table |

## Child table row fields (`Holiday` child)

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `holiday_date` | Date | Date | Y | "2026-01-26" | YYYY-MM-DD; must be within parent from/to |
| `description` | Description | Data | Y | "Republic Day" | Visible in calendar |
| `weekly_off` | Weekly Off | Check | N | 0 | Auto-marked if matches `weekly_off` setting |

## Healthcare-specific fields

| fieldname | label | type | required | example | notes |
|---|---|---|---|---|---|
| `applicable_to` | Applicable To | Select | N | "All Staff" | All Staff / Doctors Only / Nurses Only / Admin Only |

## Validation rules

- Each `holiday_date` in child table must be unique within the list.
- `to_date ≥ from_date`.
- One Holiday List per state if multi-state operations.

## Common client mistakes

- Forgetting to include Republic Day, Independence Day, Gandhi Jayanti, state-specific holidays.
- Using one Holiday List for multi-state — assign per Branch or per Department.
- Mixing weekly off into the list (use `weekly_off` setting instead).
- Importing 2025 holidays for a 2026 deployment — confirm period alignment with go-live.

## Standard holidays for Indian hospitals (Telangana 2026 example)

1. Republic Day (Jan 26)
2. Maha Shivaratri (Feb)
3. Holi (Mar)
4. Good Friday (Mar/Apr)
5. Ugadi / Telugu New Year (Mar/Apr)
6. Dr. B.R. Ambedkar's Birthday (Apr 14)
7. May Day (May 1)
8. Ramzan Eid (varies — lunar)
9. Independence Day (Aug 15)
10. Ganesh Chaturthi (Aug/Sep)
11. Bathukamma (Oct, Telangana-specific)
12. Diwali (Oct/Nov)
13. Christmas (Dec 25)
+ weekly off: Sunday
