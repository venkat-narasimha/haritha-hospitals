"""
Phase 4.1: Fix Issues 1 + 4 on Shift Type.

Issue 1: Normalize end_time from 24h+ wrap to same-day format.
  Per Frappe HRMS docs (https://docs.frappe.io/hr/shift-type):
  "End Time less than Start Time => night shift, ends next calendar day."
  end_time must be in 00:00-23:59 range.

  NOTE: The original task spec referenced an `is_past_end_time` column,
  but that column does NOT exist on `tabShift Type` in this ERPNext/HRMS
  install (v16.5). Verified via SHOW COLUMNS + Property Setter + Custom
  Field — all empty. We therefore update ONLY `end_time`.

Issue 4: Replace literal "Blue" color with hex codes by prefix (G/M/A/N).
  Palette: G=#4C6EF5, M=#51CF66, A=#FFA94D, N=#7048E8.

Idempotent: re-runs are no-ops when values already match.
"""
import frappe
import sys

sys.stdout.flush()

# ---------- Issue 1: end_time wrap ----------
# Use TIME_FORMAT to compare as string, avoids Python-side timedelta issues.
end_time_fixes = [
    ("N2000R1200", "08:00:00"),  # was 32:00:00 (24h+ wrap)
    ("N1700S1600", "09:00:00"),  # was 33:00:00
    ("N2200R0800", "06:00:00"),  # was 30:00:00
    ("A1300S1230", "01:30:00"),  # was 25:30:00
]

issue1_updated = 0
issue1_skipped = 0
for name, new_end_time in end_time_fixes:
    # Read raw end_time (returns datetime.timedelta). Convert to HH:MM:SS string.
    # Handles >24h values like "32:00:00" naturally via total_seconds().
    raw = frappe.db.get_value("Shift Type", name, "end_time")
    if raw is None:
        current_str = ""
    else:
        total = int(raw.total_seconds())
        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60
        current_str = f"{h:02d}:{m:02d}:{s:02d}"
    if current_str == new_end_time:
        issue1_skipped += 1
        sys.stdout.flush()
        print(f"  [SKIP] {name}: end_time already {new_end_time}", flush=True)
        sys.stdout.flush()
        continue
    frappe.db.sql(
        "UPDATE `tabShift Type` SET end_time = %s WHERE name = %s",
        (new_end_time, name),
    )
    issue1_updated += 1
    sys.stdout.flush()
    print(f"  [UPDATE] {name}: end_time {current_str} -> {new_end_time}", flush=True)
    sys.stdout.flush()
frappe.db.commit()
sys.stdout.flush()
print(f"Issue 1: end_time updated={issue1_updated}, skipped={issue1_skipped}", flush=True)
sys.stdout.flush()

# ---------- Issue 4: color palette ----------
color_map = {
    "G": "#4C6EF5",  # General - blue
    "M": "#51CF66",  # Morning - green
    "A": "#FFA94D",  # Afternoon - orange
    "N": "#7048E8",  # Night - purple
}

sts = frappe.get_all("Shift Type", fields=["name", "color"])
sys.stdout.flush()
print(f"Issue 4: scanning {len(sts)} Shift Types for color update", flush=True)
sys.stdout.flush()

issue4_updated = 0
issue4_skipped = 0
issue4_no_prefix = 0
for st in sts:
    name = st["name"]
    prefix = name[0]
    new_color = color_map.get(prefix)
    if not new_color:
        issue4_no_prefix += 1
        sys.stdout.flush()
        print(f"  [WARN] {name}: no color mapping for prefix '{prefix}'", flush=True)
        sys.stdout.flush()
        continue
    if st["color"] == new_color:
        issue4_skipped += 1
        continue
    frappe.db.sql(
        "UPDATE `tabShift Type` SET color = %s WHERE name = %s",
        (new_color, name),
    )
    issue4_updated += 1
    sys.stdout.flush()
    print(f"  [UPDATE] {name}: color '{st['color']}' -> '{new_color}'", flush=True)
    sys.stdout.flush()
frappe.db.commit()
sys.stdout.flush()
print(
    f"Issue 4: color updated={issue4_updated}, skipped={issue4_skipped}, no_prefix={issue4_no_prefix}",
    flush=True,
)
sys.stdout.flush()

print("DONE", flush=True)
exit()