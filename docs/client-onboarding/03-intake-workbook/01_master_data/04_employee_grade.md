# Employee Grade — Intake Sheet

**DocType:** `Employee Grade` (master)
**Module:** HR / Setup
**Autoname rule:** `field:grade_name`

**Required fields:** 1  |  **Optional fields:** 3

## Purpose

Pay band / seniority tier. Drives Salary Structure defaults + leave policy mapping + approval authority thresholds.

## Field reference

| fieldname | label | type | required | example | validation | notes |
|---|---|---|---|---|---|---|
| `grade_name` | Grade | Data | **Y** | `Grade A` | unique within company |  |
| `description` | Description | Text | **N** | `Pay band for [role group]` | free-form text |  |
| `currency` | Currency | Link→Currency | **N** | `INR` | must exist in tabCurrency |  |
| `default_salary_structure` | Default Salary Structure | Link→Salary Structure | **N** | `` | must exist in tabSalary Structure |  |

## Healthcare-specific extensions (optional, India-context)

- If client uses clinical ladders (e.g., Resident → Registrar → Consultant → Senior Consultant), define grades aligned to those ladders.

## When to use this sheet

| Scenario | Use this sheet? |
|---|---|
| Initial deployment | Yes |
| Mid-deployment grade addition | Yes — single insert |

## Common client mistakes

- Too-many-grades (10+) — breaks clean compensation bands.
