# Payroll Settings — Configuration Checklist

**Module:** Payroll (HRMS)
**Phase:** 5 — Configuration, Integrations & UAT
**DocType:** `Payroll Settings`
**Path:** Home → Payroll → Payroll Settings

> **Scope note:** If Payroll module is **not** in initial deployment scope, mark all items as "Deferred to Phase 2" and skip. This checklist is still useful for future reference.

## Pre-requisites

- [ ] HRMS Payroll app installed and enabled
- [ ] Company set up with currency and country
- [ ] Salary Components defined (basic, HRA, allowances, deductions)
- [ ] Tax slabs configured for India (old + new regime)
- [ ] Employee records have salary structure assigned (or pending)

## Configuration items

### Currency and exchange

- [ ] **Currency** — INR (or relevant)
- [ ] **Exchange Rate Source** — Manual / API (e.g., Frankfurter for multi-currency)
- [ ] **Default Currency Exchange Rate** — if Manual
- [ ] **Currency Precision** — e.g., 2 decimal places

### Payroll frequency

- [ ] **Payroll Frequency** — Monthly / Bi-weekly / Weekly
- [ ] **Payroll Date** — e.g., last working day of month
- [ ] **Payroll Cut-off Date** — e.g., 25th of month (for attendance cutoff)

### Salary components and structure

- [ ] **Earnings Components** — Basic, HRA, Conveyance, Medical Allowance, Special Allowance, Night-Shift Allowance, On-Call Allowance
- [ ] **Deduction Components** — PF (Employee), ESI (Employee), Professional Tax, Income Tax (TDS), Loan Repayment
- [ ] **Employer Contributions** — PF (Employer), ESI (Employer), Gratuity provision
- [ ] **Salary Structure Templates** — per Employee Grade

### Statutory components (India-specific)

- [ ] **PF Settings** — PF Number format, UAN enabled, VPF option
- [ ] **ESI Settings** — ESI Number format, applicability threshold (gross ≤₹21,000/month)
- [ ] **Professional Tax** — State-wise (e.g., State A: ₹200 if gross >₹15,000/month)
- [ ] **TDS / Income Tax** — Old regime / New regime / Both (let employee choose)
- [ ] **Gratuity** — Provision rate (e.g., 4.81% of basic)
- [ ] **Bonus / Ex-gratia** — Per Payment of Bonus Act

### Hospital-specific components

- [ ] **Night-Shift Allowance** — Per-hour or per-shift amount; link to Shift Type
- [ ] **On-Call Allowance** — Per-shift amount
- [ ] **Overtime Rate** — Per-hour or per-shift; link to Overtime Type
- [ ] **Uniform / Laundry Allowance** — Monthly fixed
- [ ] **Medical Benefit** — For employees + dependents (per hospital policy)
- [ ] **Travel Allowance** — For visiting consultants
- [ ] **Risk Allowance** — For ER / ICU / Casualty staff (hazard pay)

### Payroll processing

- [ ] **Payroll Entry** — Bulk salary slip generation per department
- [ ] **Salary Slip Email** — Auto-send to employee email
- [ ] **Bank Remittance** — Salary slip → bank file generation (NEFT/RTGS format)
- [ ] **Payslip PDF Template** — Customize with hospital branding
- [ ] **Loan Management** — Salary advances + recovery schedule
- [ ] **Period Closing** — Auto-close payroll periods for audit

### Reports

- [ ] **Salary Register** — Monthly department-wise
- [ ] **Bank Advice** — For bulk bank transfers
- [ ] **PF / ESI / PT Challan** — Monthly statutory returns
- [ ] **Form 16 / 12BA** — Annual TDS certificate
- [ ] **Payroll Variance** — Compare actual vs budgeted

## Validation tests

- [ ] Run payroll for one employee (test case) → verify salary slip calculates correctly
- [ ] Run payroll for one department → verify all statutory deductions + employer contributions
- [ ] Generate bank file → verify format matches bank's requirement
- [ ] Send salary slip via email → verify email template and PDF
- [ ] Cancel and re-run payroll → verify reversibility
- [ ] Generate PF/ESI/PT challan → verify format accepted by government portal

## Sign-off

Configured by: _________________________  Date: ___________

Verified by:   _________________________  Date: ___________

Client Finance Lead approval: _________________________  Date: ___________

Client HR Lead approval:      _________________________  Date: ___________
