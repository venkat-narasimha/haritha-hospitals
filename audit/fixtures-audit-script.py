"""Complete fixtures audit (READ-ONLY).

Uses raw SQL for clarity + avoids filter quirks on DocType/fields.

Outputs a comprehensive markdown-friendly report.
"""
import frappe

def H(s):
    print()
    print("=" * 70)
    print(s)
    print("=" * 70)

# ----- Installed apps -----
H("Installed apps")
print(frappe.get_installed_apps())

# ----- App ↔ Module mapping (from Module Def.app_name) -----
H("App → Module mapping (from Module Def.app_name)")
mod_app = frappe.db.sql(
    "SELECT app_name, name FROM `tabModule Def` "
    "WHERE app_name IS NOT NULL AND app_name != '' "
    "ORDER BY app_name, name",
    as_dict=True,
)
for m in mod_app:
    print(f"  {m['app_name']:15s} {m['name']}")

# Build module→app dict for categorization
mod2app = {m['name']: m['app_name'] for m in mod_app}

# Categories we consider core (3rd-party): frappe, erpnext, hrms
CORE = {"frappe", "erpnext", "hrms"}
CUSTOM = {"Haritha", "Custom", "haritha_hospital", "pb_material"}

def classify(module):
    """Return one of: 'core-frappe', 'core-erpnext', 'core-hrms', 'custom', 'unknown'."""
    if not module:
        return "custom"  # NULL/empty → user-added, not from any core module
    app = mod2app.get(module, "unknown")
    if app in CORE:
        return f"core-{app}"
    if module in CUSTOM or app in CUSTOM:
        return "custom"
    # Anything that maps to a known core app's module is "core"
    if app != "unknown":
        return f"core-{app}"
    return "unknown"

# ============================================================================
# STEP A — Counts (correct doctype names)
# ============================================================================
H("STEP A — Customization counts")

counts = {}
for dt, label, flt in [
    ("Custom Field", "Custom Fields", {}),
    ("Property Setter", "Property Setters", {}),
    ("Workflow", "Workflows", {}),
    ("Client Script", "Client Scripts", {}),
    ("Server Script", "Server Scripts", {}),
    ("Print Format", "Print Formats", {}),
    ("Web Form", "Web Forms", {}),
    ("Notification", "Notifications", {}),
    ("DocType", "Custom DocTypes", {"custom": 1}),
    ("DocPerm", "Custom DocPerm", {}),
    ("Workspace", "Workspaces (all)", {}),
    ("Dashboard Chart", "Dashboard Charts (all)", {}),
    ("Number Card", "Number Cards (all)", {}),
    ("Report", "Reports (all)", {}),
    ("Letter Head", "Letter Heads", {}),
]:
    try:
        c = frappe.db.count(dt, flt)
        counts[dt] = c
        print(f"  {label:30s} {c}")
    except Exception as e:
        counts[dt] = None
        print(f"  {label:30s} ERROR {str(e)[:60]}")

# Sub-count: custom/standard split
H("Sub-counts: custom vs standard")
print("  ---")
print(f"  Print Formats: standard={frappe.db.count('Print Format', {'standard': 'Yes'})}, "
      f"custom_format=1: {frappe.db.count('Print Format', {'custom_format': 1})}, "
      f"disabled=1: {frappe.db.count('Print Format', {'disabled': 1})}")
print(f"  Notifications: is_standard=1: {frappe.db.count('Notification', {'is_standard': 1})}, "
      f"is_standard=0: {frappe.db.count('Notification', {'is_standard': 0})}")
print(f"  Web Forms: is_standard=1: {frappe.db.count('Web Form', {'is_standard': 1})}, "
      f"is_standard=0: {frappe.db.count('Web Form', {'is_standard': 0})}")
print(f"  Reports: is_standard=1: {frappe.db.count('Report', {'is_standard': 1})}, "
      f"is_standard=0: {frappe.db.count('Report', {'is_standard': 0})}")
print(f"  Dashboard Charts: is_standard=1: {frappe.db.count('Dashboard Chart', {'is_standard': 1})}, "
      f"is_standard=0: {frappe.db.count('Dashboard Chart', {'is_standard': 0})}")
print(f"  Number Cards: is_standard=1: {frappe.db.count('Number Card', {'is_standard': 1})}, "
      f"is_standard=0: {frappe.db.count('Number Card', {'is_standard': 0})}")

# Workspaces don't have is_standard → filter by module='Custom' or for_user='' (public)
ws_total = counts.get("Workspace")
ws_custom_mod = frappe.db.count("Workspace", {"module": "Custom"})
ws_public = frappe.db.count("Workspace", {"for_user": ("in", ("", None))})
ws_user_only = frappe.db.count("Workspace", {"for_user": ("not in", ("", None))})
print(f"  Workspaces: module='Custom': {ws_custom_mod}, public (for_user NULL/empty): {ws_public}, "
      f"user-private: {ws_user_only}, total: {ws_total}")

# ============================================================================
# STEP B — Per-type details with categorization
# ============================================================================

# ----- Custom Fields -----
H("STEP B1 — Custom Fields")
cf = frappe.db.sql(
    """SELECT name, dt, fieldname, label, fieldtype, module, creation
       FROM `tabCustom Field`
       ORDER BY dt, fieldname""",
    as_dict=True,
)
print(f"Total: {len(cf)}")
cats = {}
for f in cf:
    cat = classify(f.get("module"))
    cats.setdefault(cat, []).append(f)
for cat, items in sorted(cats.items()):
    print(f"\n  [{cat}] {len(items)}")
    for f in items[:60]:
        print(f"    {f['dt']:30s} {f['fieldname']:30s} "
              f"({f.get('fieldtype')}) mod='{f.get('module') or ''}'")
    if len(items) > 60:
        print(f"    ... +{len(items)-60} more")

# ----- Property Setters -----
H("STEP B2 — Property Setters")
ps = frappe.db.sql(
    """SELECT name, doc_type, field_name, property, value, property_type,
              module, creation
       FROM `tabProperty Setter`
       ORDER BY doc_type, field_name, property""",
    as_dict=True,
)
print(f"Total: {len(ps)}")
ps_cats = {}
for p in ps:
    cat = classify(p.get("module"))
    ps_cats.setdefault(cat, []).append(p)
for cat, items in sorted(ps_cats.items()):
    print(f"\n  [{cat}] {len(items)}")
    # Show a few per doc_type
    by_dt = {}
    for p in items:
        by_dt.setdefault(p["doc_type"], []).append(p)
    for dt_, lst in sorted(by_dt.items()):
        if len(lst) <= 4:
            for p in lst:
                val = (p.get("value") or "")[:35]
                print(f"    {dt_:30s} {p.get('field_name') or '-':18s} "
                      f"{p.get('property') or '-':20s} -> {val}")
        else:
            print(f"    {dt_:30s} ({len(lst)} property setters)")

# ----- Workflows -----
H("STEP B3 — Workflows")
wf = frappe.db.sql(
    """SELECT name, document_type, workflow_state_field, is_active, creation
       FROM `tabWorkflow`
       ORDER BY document_type, name""",
    as_dict=True,
)
print(f"Total: {len(wf)}")
for w in wf:
    print(f"  {w['name']:30s} dt={w.get('document_type'):30s} "
          f"active={w.get('is_active')}")

# ----- Client Scripts / Server Scripts -----
H("STEP B4 — Client Scripts")
cs = frappe.db.sql(
    """SELECT name, dt, view, enabled, module
       FROM `tabClient Script`
       ORDER BY dt, name""",
    as_dict=True,
)
print(f"Total: {len(cs)}")
for s in cs:
    print(f"  {s['name']:30s} dt={s.get('dt'):30s} view={s.get('view') or '-':8s} "
          f"enabled={s.get('enabled')} module={s.get('module') or ''}")

H("STEP B5 — Server Scripts")
ss = frappe.db.sql(
    """SELECT name, script_type, reference_doctype, disabled, module
       FROM `tabServer Script`
       ORDER BY name""",
    as_dict=True,
)
print(f"Total: {len(ss)}")
for s in ss:
    print(f"  {s['name']:35s} ref_dt={s.get('reference_doctype') or '-':25s} "
          f"type={s.get('script_type') or '-':12s} disabled={s.get('disabled')} "
          f"module={s.get('module') or ''}")

# ----- Print Formats -----
H("STEP B6 — Print Formats")
pf = frappe.db.sql(
    """SELECT name, doc_type, module, standard, custom_format, disabled, creation
       FROM `tabPrint Format`
       ORDER BY doc_type, name""",
    as_dict=True,
)
print(f"Total: {len(pf)}")
pf_cats = {}
for p in pf:
    # Print Formats: standard=Yes → 3rd-party, custom_format=1 → custom
    if p.get("standard") == "Yes":
        cat = "core-standard"
    else:
        cat = classify(p.get("module"))
    pf_cats.setdefault(cat, []).append(p)
for cat, items in sorted(pf_cats.items()):
    print(f"\n  [{cat}] {len(items)}")
    for p in items:
        flags = []
        if p.get("standard") == "Yes":
            flags.append("STD")
        if p.get("custom_format"):
            flags.append("CUSTOM")
        if p.get("disabled"):
            flags.append("DISABLED")
        print(f"    {p['name']:40s} dt={(p.get('doc_type') or '-'):30s} "
              f"{','.join(flags):15s} mod='{p.get('module') or ''}'")

# ----- Notifications -----
H("STEP B7 — Notifications")
noti = frappe.db.sql(
    """SELECT name, document_type, event, enabled, channel, module,
              is_standard, creation
       FROM `tabNotification`
       ORDER BY document_type, name""",
    as_dict=True,
)
print(f"Total: {len(noti)}")
for n in noti:
    print(f"  {n['name']:40s} dt={n.get('document_type'):30s} "
          f"event={n.get('event') or '-':12s} enabled={n.get('enabled')} "
          f"channel={n.get('channel') or '-':8s} std={n.get('is_standard')} "
          f"mod='{n.get('module') or ''}'")

# ----- Web Forms -----
H("STEP B8 — Web Forms")
webf = frappe.db.sql(
    """SELECT name, title, route, doc_type, module, is_standard, published
       FROM `tabWeb Form`
       ORDER BY doc_type, name""",
    as_dict=True,
)
print(f"Total: {len(webf)}")
for w in webf:
    print(f"  {w['name']:30s} dt={w.get('doc_type'):30s} "
          f"route={w.get('route') or '-':40s} std={w.get('is_standard')} "
          f"mod='{w.get('module') or ''}'")

# ----- Custom DocTypes -----
H("STEP B9 — Custom DocTypes")
dt_list = frappe.db.sql(
    """SELECT name, module, app, istable, custom, creation
       FROM `tabDocType`
       WHERE custom = 1
       ORDER BY module, name""",
    as_dict=True,
)
print(f"Total: {len(dt_list)}")
for d in dt_list:
    print(f"  {d['name']:40s} module={d.get('module') or '-':20s} "
          f"app={d.get('app') or '-':15s} istable={d.get('istable')}")

# ----- Custom DocPerm -----
H("STEP B10 — DocPerm (all)")
dp = frappe.db.sql(
    """SELECT name, parent, role, permlevel, `read`, `write`, `create`, submit,
              cancel, amend, `delete`, if_owner, share, print, email
       FROM `tabDocPerm`
       ORDER BY parent, role, permlevel""",
    as_dict=True,
)
print(f"Total: {len(dp)}")
# Group by parent
by_parent = {}
for d in dp:
    by_parent.setdefault(d.get("parent") or "?", []).append(d)
print(f"Distinct DocTypes with DocPerm: {len(by_parent)}")
# Show DocPerms on custom-typed DocTypes
print("\nDocPerms grouped by parent (top 30):")
for parent, lst in sorted(by_parent.items(), key=lambda x: -len(x[1]))[:30]:
    roles = sorted({d["role"] for d in lst})
    print(f"  {parent:40s} {len(lst)} perms, roles={roles}")

# ----- Workspaces -----
H("STEP B11 — Workspaces")
ws = frappe.db.sql(
    """SELECT name, module, app, public, for_user, creation
       FROM `tabWorkspace`
       ORDER BY module, name""",
    as_dict=True,
)
print(f"Total: {len(ws)}")
for w in ws:
    print(f"  {w['name']:35s} module={w.get('module') or '-':20s} "
          f"app={w.get('app') or '-':15s} public={w.get('public')} "
          f"for_user='{w.get('for_user') or ''}'")

# ----- Custom Dashboard Charts -----
H("STEP B12 — Dashboard Charts (is_standard=0)")
ch = frappe.db.sql(
    """SELECT name, chart_type, document_type, module, is_standard, creation
       FROM `tabDashboard Chart`
       WHERE is_standard = 0
       ORDER BY module, name""",
    as_dict=True,
)
print(f"Total: {len(ch)}")
for c in ch:
    print(f"  {c['name']:40s} type={c.get('chart_type') or '-':10s} "
          f"dt={c.get('document_type') or '-':30s} mod='{c.get('module') or ''}'")

# ----- Custom Number Cards -----
H("STEP B13 — Number Cards (is_standard=0)")
nc = frappe.db.sql(
    """SELECT name, document_type, module, is_standard, creation
       FROM `tabNumber Card`
       WHERE is_standard = 0
       ORDER BY module, name""",
    as_dict=True,
)
print(f"Total: {len(nc)}")
for c in nc:
    print(f"  {c['name']:40s} dt={c.get('document_type') or '-':30s} "
          f"mod='{c.get('module') or ''}'")

# ----- Custom Reports -----
H("STEP B14 — Reports (is_standard=0)")
rep = frappe.db.sql(
    """SELECT name, report_type, ref_doctype, module, is_standard, creation
       FROM `tabReport`
       WHERE is_standard = 0
       ORDER BY module, name""",
    as_dict=True,
)
print(f"Total: {len(rep)}")
for r in rep:
    print(f"  {r['name']:50s} type={r.get('report_type') or '-':12s} "
          f"dt={r.get('ref_doctype') or '-':30s} mod='{r.get('module') or ''}'")

# ----- Letter Heads -----
H("STEP B15 — Letter Heads")
lh = frappe.db.sql(
    "SELECT name, letter_head_name, is_default, disabled "
    "FROM `tabLetter Head` ORDER BY name",
    as_dict=True,
)
print(f"Total: {len(lh)}")
for h in lh:
    print(f"  {h['name']:40s} title='{h.get('letter_head_name') or ''}' "
          f"default={h.get('is_default')} "
          f"disabled={h.get('disabled')}")

# ============================================================================
# STEP C — Final aggregation by category
# ============================================================================
H("STEP C — Categorization summary")

# Aggregate Custom Field + Property Setter by category
agg = {}
for f in cf:
    cat = classify(f.get("module"))
    agg[cat] = agg.get(cat, 0) + 1
for p in ps:
    cat = classify(p.get("module"))
    agg[cat] = agg.get(cat, 0) + 1

print("Custom Field + Property Setter totals by category:")
for cat, n in sorted(agg.items(), key=lambda x: -x[1]):
    print(f"  {cat:25s} {n}")

# Other totals
print(f"\nPrint Formats: total={len(pf)}, standard={sum(1 for p in pf if p.get('standard')=='Yes')}, "
      f"custom={sum(1 for p in pf if p.get('standard')!='Yes')}")
print(f"Notifications: total={len(noti)}, standard={sum(1 for n in noti if n.get('is_standard')==1)}, "
      f"custom={sum(1 for n in noti if n.get('is_standard')!=1)}")
print(f"Web Forms: total={len(webf)}, standard={sum(1 for w in webf if w.get('is_standard')==1)}, "
      f"custom={sum(1 for w in webf if w.get('is_standard')!=1)}")
print(f"Custom DocTypes: {len(dt_list)}")
print(f"Workspaces: {len(ws)} (Custom module: {ws_custom_mod}, public: {ws_public})")
print(f"Custom Dashboard Charts: {len(ch)}")
print(f"Custom Number Cards: {len(nc)}")
print(f"Custom Reports: {len(rep)}")
print(f"Letter Heads: {len(lh)}")
print(f"DocPerm: {len(dp)} on {len(by_parent)} DocTypes")
print(f"Workflows: {len(wf)}")
print(f"Client Scripts: {len(cs)}")
print(f"Server Scripts: {len(ss)}")

print()
print("---DONE---")
