## Phase 3.7: Property Setter Recreate Script (✅ DONE 2026-08-27 15:06 IST)

**Status:** ✅ Complete — idempotent `recreate_property_setters.py` committed + pushed.

**Why this section exists:** Phase 3.6 bulk-submit (commit c13753b) created the `Attendance-status-options` Property Setter at runtime (added 'Holiday' + 'Weekly Off' to Attendance.meta.get_field('status').options). Per Rule #9 SOUL: ANY Custom Field / Property Setter / Custom DocType / Workflow / Print Format / Client Script / Server Script → `bench export-fixtures` → commit. But:

1. `bench export-fixtures --app hrms` produced no `apps/hrms/fixtures/property_setter.json` because HRMS' `hooks.py` does NOT list 'Property Setter' as a fixture — the export silently skips it.
2. Even if the fixture file existed, committing to `apps/hrms/` violates SOUL NEVER rule #3 (third-party code is read-only, would clobber on `bench update`).
3. PROD bench has no custom app (`apps/` = {erpnext, frappe, hrms} only) — can't host fixtures under a custom app hooks.py.

**Resolution (Option 2 — scripted recreate):**

- Script: `scripts/recreate_property_setters.py` (7.2 KB)
- Pattern: `frappe.make_property_setter(args_dict, validate_fields_for_doctype=False)` — the wrapper takes a dict with `doctype`/`fieldname`/`property`/`value`/`property_type` keys, NOT keyword args. The lower-level `frappe.custom.doctype.property_setter.property_setter.make_property_setter(doctype, fieldname, property, value, property_type, ...)` uses positional args + `for_doctype` kwarg — different signature.
- `frappe.make_property_setter` is idempotent: it deletes existing (doctype, field, property) and creates fresh, OR overwrites if exists (verified).
- Invoked via `bench --site <site> console < <(docker exec wrapper)` pattern with `importlib.util.spec_from_file_location()` to load the script (because `bench execute <name>` requires the module to live in an app dir, which scripts in /tmp are not).

**Property Setters defined in script (PROPERTY_SETTERS list):**

```python
[
    {
        "doctype": "Attendance",
        "field_name": "status",
        "property": "options",
        "value": "\nPresent\nAbsent\nOn Leave\nHalf Day\nWork From Home\nHoliday\nWeekly Off",
        "property_type": "Text",
    },
]
```

**Idempotency test (passed on pberpprod 2026-08-27 15:05 IST):**

| Step | Result |
|---|---|
| 1. Initial state: PS exists, meta.options = 7 values | ✅ |
| 2. DELETE PS, meta falls back to default (5 values, no Holiday/Weekly Off) | ✅ confirms PS really controls meta |
| 3. Run script → PS recreated, meta restored to 7 values | ✅ |
| 4. Run script again → no duplicate rows, value unchanged | ✅ exactly 1 PS row, value identical |

**How to apply on any env (migration recipe):**

```bash
# 1. Copy script into the bench container
docker cp recreate_property_setters.py erp-<env>-backend-1:/tmp/

# 2. Run via bench console + importlib pattern
docker exec erp-<env>-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench --site <site> console < <(echo '
import importlib.util
spec = importlib.util.spec_from_file_location(\"rps\", \"/tmp/recreate_property_setters.py\")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
result = mod.run(dry_run=False)
print(\"applied:\", result[\"applied\"], \"failed:\", result[\"failed\"])
')"

# 3. Verify
docker exec erp-<env>-backend-1 bash -c "cd /home/frappe/frappe-bench && \
  bench --site <site> console < <(echo '
import frappe
print(frappe.db.get_value(\"Property Setter\", {\"doc_type\": \"Attendance\", \"field_name\": \"status\", \"property\": \"options\"}, [\"name\", \"value\"]))
')"
```

**Alternative invocation (cleaner, what we'll wire into env setup playbook):**

A wrapper script in sites/ dir, copy-able to any container, that calls run() directly. Not done yet — current pattern is documented above.

**Rule #9 status:** RESOLVED for this Property Setter. The DB-only Property Setter is now reproducible on any env via the script. Pattern: any future PS/Custom Field created at runtime on pberpprod should be added to `PROPERTY_SETTERS` / `CUSTOM_FIELDS` in `recreate_property_setters.py` (or split into a separate `recreate_custom_fields.py`).

**Ref:** Lesson #105 (Property Setter doesn't bypass controller-level checks), #106 (3-run pattern), and the Rule #9 gap surfaced by Phase 3.6 bulk-submit 2026-08-27.

