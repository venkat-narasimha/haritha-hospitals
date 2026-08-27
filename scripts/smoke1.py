print('=== Test 1: Shift Assignment docstatus=1 count ===')
submitted_sas = frappe.get_list("Shift Assignment", filters={"docstatus": 1}, limit=5, fields=["name", "employee", "shift_type", "start_date"])
print(f"Count: {frappe.db.count('Shift Assignment', {'docstatus': 1})}")
for sa in submitted_sas:
    print(f"  {sa.name} | emp={sa.employee} | shift={sa.shift_type} | start={sa.start_date}")
print('DONE')
exit