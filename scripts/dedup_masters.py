"""Deduplicate selected Haritha Hospitals master records.

Run through:
    bench --site pberpprod.duckdns.org console
    exec(open("/tmp/dedup_masters.py").read())
"""

import frappe


MASTER_TARGETS = [
    ("Department", "department_name", 36),
    ("Designation", "designation_name", 48),
    ("Leave Type", "leave_type_name", 7),
    ("Employment Type", "employee_type_name", 6),
]
HOLIDAY_DOCTYPE = "Holiday"
HOLIDAY_LIST_NAME = "Haritha Hospitals Holiday List"
HOLIDAY_EXPECTED = 14

results = []

# Masters: exact key match, oldest creation wins.
for doctype, key_field, expected_count in MASTER_TARGETS:
    before = frappe.db.count(doctype)
    seen = set()
    duplicates = []

    records = frappe.get_all(
        doctype,
        fields=["name", key_field, "creation"],
        order_by="creation asc, name asc",
        limit_page_length=0,
    )
    for row in records:
        key_value = row.get(key_field)
        key = "<blank>" if key_value is None or str(key_value).strip() == "" else str(key_value)
        if key in seen:
            duplicates.append(row)
        else:
            seen.add(key)

    for row in duplicates:
        frappe.delete_doc(doctype, row["name"], ignore_permissions=True)

    after = frappe.db.count(doctype)
    result = {
        "entity": doctype,
        "before": before,
        "after": after,
        "deleted": len(duplicates),
        "expected": expected_count,
        "status": "OK" if after == expected_count else "MISMATCH",
    }
    if after != expected_count:
        remaining = {}
        for row in frappe.get_all(
            doctype,
            fields=["name", key_field],
            order_by="creation asc, name asc",
            limit_page_length=0,
        ):
            key_value = row.get(key_field)
            key = "<blank>" if key_value is None or str(key_value).strip() == "" else str(key_value)
            if key in remaining:
                remaining[key].append(row["name"])
            elif key in seen:
                remaining[key] = [row["name"]]

        result["remaining_duplicates"] = [
            {
                "key": key,
                "count": len(names) + 1,
                "sample_names": names[:10],
            }
            for key, names in sorted(remaining.items())
        ]
    results.append(result)

# Holiday children: exact holiday_date match, oldest row wins.
before_holidays = frappe.db.count(HOLIDAY_DOCTYPE)
holiday_list = frappe.get_doc("Holiday List", HOLIDAY_LIST_NAME)
holiday_list_before = len(holiday_list.holidays)
sorted_holidays = sorted(
    list(holiday_list.holidays),
    key=lambda h: (
        str(getattr(h, "creation", None) or ""),
        str(getattr(h, "idx", 0) or 0),
        str(getattr(h, "name", None) or ""),
    ),
)

seen_dates = set()
for h in sorted_holidays:
    holiday_date = getattr(h, "holiday_date", None)
    if hasattr(holiday_date, "isoformat"):
        seen_dates.update({holiday_date, holiday_date.isoformat()})
    else:
        seen_dates.add(holiday_date)

# Remove later duplicate child rows; the parent itself is not deleted.
hl = holiday_list
hl.holidays = [h for h in sorted_holidays if h.holiday_date not in seen_dates]
seen_dates.update(
    value
    for h in hl.holidays
    for value in (
        {getattr(h, "holiday_date", None), getattr(h, "holiday_date", None).isoformat()}
        if hasattr(getattr(h, "holiday_date", None), "isoformat")
        else {getattr(h, "holiday_date", None)}
    )
)
holiday_list_after = len(hl.holidays)
hl.save(ignore_permissions=True)
hl.reload()

after_holidays = frappe.db.count(HOLIDAY_DOCTYPE)
holiday_result = {
    "entity": HOLIDAY_DOCTYPE,
    "holiday_list": HOLIDAY_LIST_NAME,
    "before": before_holidays,
    "after": after_holidays,
    "holiday_list_before": holiday_list_before,
    "holiday_list_after": len(hl.holidays),
    "deleted": holiday_list_before - holiday_list_after,
    "expected": HOLIDAY_EXPECTED,
    "status": "OK" if after_holidays == HOLIDAY_EXPECTED else "MISMATCH",
}
if after_holidays != HOLIDAY_EXPECTED:
    seen = set()
    remaining = {}
    for h in hl.holidays:
        key = str(getattr(h, "holiday_date", None))
        if key in seen:
            remaining.setdefault(key, []).append(getattr(h, "name", None) or "<unnamed>")
        else:
            seen.add(key)
    holiday_result["remaining_duplicates"] = [
        {
            "key": key,
            "count": len(names) + 1,
            "sample_names": names[:10],
        }
        for key, names in sorted(remaining.items())
    ]
results.append(holiday_result)

frappe.db.commit()
print("DEDUP_RESULT=" + frappe.as_json(results))
