#!/usr/bin/env python3
"""
update_tracker.py — Apply structured updates to TRACKER.md from a JSON spec.

Replaces manual sed/edit of TRACKER.md for repetitive updates.

Usage:
  python3 update_tracker.py --input update.json [--tracker TRACKER.md] [--dry-run]

JSON spec format:
{
  "status_date": "2026-08-25 22:46 IST",                    # replaces Project Status header date
  "status_subtitle": "Phase 2 Step A complete",             # optional, replaces subtitle
  "footer_text": "Phase 1.5 + A1-A5 done; awaiting B",      # replaces footer "Last updated:" line
  "sections": [                                             # inserted before "## Known Issues / Lessons Learned"
    {
      "title": "## Phase 2: Step A1-A5 (2026-08-25 22:27 IST) ✅",
      "body": "Markdown content here. Can be multi-line."
    }
  ],
  "decisions": [                                            # appended to Decisions Log table
    {"date": "2026-08-25", "name": "...", "rationale": "..."}
  ],
  "lessons": [                                              # appended to Known Issues table
    {"issue": "...", "lesson": "..."}
  ],
  "pending_done": ["item text to mark ✅ done"],            # adds ✅ prefix if not present (idempotent)
  "pending_add": ["new pending item"]                       # appended to immediate gated section
}

Idempotency:
  - Sections deduped by exact title match (skip if already present)
  - Decisions deduped by date+name
  - Lessons deduped by issue text
  - pending_done: skip if already marked done (✅ present)
  - pending_add: skip if exact text already present

Exit codes:
  0 = success (changes applied or no changes needed)
  1 = error (file not found, JSON invalid, etc.)
  2 = dry-run with changes that would be applied (informational)
"""
import argparse
import json
import re
import sys
from pathlib import Path


def load_spec(path: Path) -> dict:
    if not path.exists():
        print(f"ERROR: spec file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)


def load_tracker(path: Path) -> str:
    if not path.exists():
        print(f"ERROR: tracker file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text()


# --- Operations ---

def update_status_date(text: str, new_date: str, new_subtitle: str = None) -> tuple[str, bool]:
    """Update Project Status header date. Returns (text, changed)."""
    pattern = r"(## 🔄 Project Status \()([^)]+)(\)( — [^—\n]*)?)"
    new_subtitle_str = f" — {new_subtitle}" if new_subtitle else ""
    replacement = rf"\g<1>{new_date}\g<3>{new_subtitle_str}"
    new_text, count = re.subn(pattern, replacement, text, count=1)
    return new_text, count > 0


def update_footer(text: str, new_footer: str) -> tuple[str, bool]:
    """Replace the '*Last updated: ...*' footer line."""
    pattern = r"\*Last updated: [^\n*]+\*"
    replacement = f"*Last updated: {new_footer}*"
    new_text, count = re.subn(pattern, replacement, text, count=1)
    if count == 0:
        # No footer found — append at end
        new_text = text.rstrip() + f"\n\n*Last updated: {new_footer}*\n"
        return new_text, True
    return new_text, True


def insert_section(text: str, title: str, body: str) -> tuple[str, bool]:
    """Insert a new section before '## Known Issues / Lessons Learned'.
    Idempotent: skip if title already in tracker.
    """
    if title in text:
        return text, False

    marker = "## Known Issues / Lessons Learned"
    if marker not in text:
        print(f"ERROR: marker '{marker}' not found in tracker", file=sys.stderr)
        sys.exit(1)

    section_content = f"\n{title}\n\n{body.strip()}\n\n"
    # Insert section before the marker
    new_text = text.replace(marker, section_content + marker, 1)
    return new_text, True


def append_decision(text: str, date: str, name: str, rationale: str) -> tuple[str, bool]:
    """Append row to Decisions Log table. Idempotent on date+name."""
    # Check if already present (date + name match)
    # The table format is: | YYYY-MM-DD | name | rationale |
    pattern_check = rf"\|\s*{re.escape(date)}\s*\|\s*{re.escape(name)}\s*\|"
    if re.search(pattern_check, text):
        return text, False

    # Find the Decisions Log table — last row before "## Subagent Log" or next section
    marker = "## Subagent Log"
    if marker not in text:
        # Try alternative markers
        for alt in ["## Open Questions", "## Pending Actions", "## Known Issues"]:
            if alt in text:
                marker = alt
                break

    # Find the last table row in Decisions Log
    # Strategy: find the table, get its end, insert new row there
    decisions_marker = "## Decisions Log"
    if decisions_marker not in text:
        print(f"ERROR: marker '{decisions_marker}' not found", file=sys.stderr)
        sys.exit(1)

    # Find table boundaries
    decisions_start = text.index(decisions_marker)
    next_section_start = text.find("\n## ", decisions_start + len(decisions_marker))
    if next_section_start < 0:
        next_section_start = len(text)
    decisions_block = text[decisions_start:next_section_start]

    # Find last row (starts with |) in decisions_block
    # Walk backwards from end of block to find last row
    lines = decisions_block.split("\n")
    last_row_idx = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("|") and "---" not in lines[i] and "Date" not in lines[i]:
            last_row_idx = i
            break

    if last_row_idx is None:
        print("ERROR: could not find last row in Decisions Log", file=sys.stderr)
        sys.exit(1)

    # Insert new row after the last row
    new_row = f"| {date} | {name} | {rationale} |"
    lines.insert(last_row_idx + 1, new_row)
    new_block = "\n".join(lines)

    new_text = text[:decisions_start] + new_block + text[next_section_start:]
    return new_text, True


def append_lesson(text: str, issue: str, lesson: str) -> tuple[str, bool]:
    """Append row to Known Issues / Lessons Learned table. Idempotent on issue text."""
    if issue in text:
        return text, False

    marker = "## Known Issues / Lessons Learned"
    if marker not in text:
        print(f"ERROR: marker '{marker}' not found", file=sys.stderr)
        sys.exit(1)

    # Find footer pattern at end (|*Last updated: ...*|)
    footer_pattern = r"\n\*Last updated: [^\n*]+\*\n*$"
    footer_match = re.search(footer_pattern, text)
    if footer_match:
        footer = footer_match.group(0)
        text_before_footer = text[:footer_match.start()]
    else:
        text_before_footer = text.rstrip() + "\n"
        footer = ""

    # Find the last row in Known Issues table
    issues_start = text_before_footer.rindex(marker)
    lines_after = text_before_footer[issues_start:].split("\n")
    last_row_idx = None
    for i in range(len(lines_after) - 1, -1, -1):
        if lines_after[i].startswith("|") and "---" not in lines_after[i] and "Issue" not in lines_after[i]:
            last_row_idx = i
            break

    if last_row_idx is None:
        print("ERROR: could not find last row in Known Issues", file=sys.stderr)
        sys.exit(1)

    new_row = f"| {issue} | {lesson} |"
    lines_after.insert(last_row_idx + 1, new_row)
    new_block = "\n".join(lines_after)
    new_text = text_before_footer[:issues_start] + new_block + footer
    return new_text, True


def mark_pending_done(text: str, item_text: str) -> tuple[str, bool]:
    """Mark a Pending Actions item as ✅ done (idempotent)."""
    # Look for item in numbered list or as plain text
    # Pattern 1: `N. **item_text**` or `N. ✅ **item_text**` or `N. item_text`
    patterns = [
        rf"(\d+\.\s+)(\*\*)?{re.escape(item_text)}(\*\*)?\s*[—:]",
        rf"(\d+\.\s+)(\*\*)?{re.escape(item_text)}(\*\*)?\s*$",
    ]

    # First check if already marked done (✅ in front of item)
    for pat in patterns:
        m = re.search(pat, text, re.MULTILINE)
        if m:
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.end())
            if line_end < 0:
                line_end = len(text)
            line = text[line_start:line_end]
            if "✅" in line:
                return text, False  # already done
            # Mark as done by prepending ✅
            new_line = line.replace(m.group(0), f"{m.group(1)}✅ **{item_text}**{m.group(3) or ''}{m.group(4) or ''}", 1)
            if not new_line.startswith(f"{m.group(1)}✅"):
                # Fallback: insert ✅ after number prefix
                new_line = f"{m.group(1)}✅ {item_text}"
            new_text = text[:line_start] + new_line + text[line_end:]
            return new_text, True

    # Item not found — append to Pending Actions as new entry (treat as add)
    return text, False


def add_pending_item(text: str, item_text: str) -> tuple[str, bool]:
    """Append a new pending action. Idempotent on exact text."""
    if item_text in text:
        return text, False

    marker = "## Pending Actions"
    if marker not in text:
        print(f"ERROR: marker '{marker}' not found", file=sys.stderr)
        sys.exit(1)

    # Find the immediate section (after Pending Actions header, before next ##)
    pending_start = text.index(marker)
    next_section = text.find("\n## ", pending_start + len(marker))
    if next_section < 0:
        next_section = len(text)

    pending_block = text[pending_start:next_section]
    lines = pending_block.split("\n")

    # Find max number in numbered list
    max_n = 0
    for line in lines:
        m = re.match(r"^\s*(\d+)\.\s+", line)
        if m:
            max_n = max(max_n, int(m.group(1)))

    new_n = max_n + 1
    new_line = f"{new_n}. {item_text}"
    lines.append("")  # blank
    lines.append(new_line)
    new_block = "\n".join(lines)

    new_text = text[:pending_start] + new_block + text[next_section:]
    return new_text, True


def apply_spec(text: str, spec: dict) -> tuple[str, dict]:
    """Apply all spec operations to text. Returns (new_text, change_summary)."""
    changes = {"applied": [], "skipped": []}

    if "status_date" in spec:
        text, changed = update_status_date(text, spec["status_date"], spec.get("status_subtitle"))
        changes["applied" if changed else "skipped"].append("status_date")

    if "footer_text" in spec:
        text, changed = update_footer(text, spec["footer_text"])
        changes["applied"].append("footer_text")

    for section in spec.get("sections", []):
        text, changed = insert_section(text, section["title"], section["body"])
        changes["applied" if changed else "skipped"].append(f"section: {section['title'][:50]}")

    for decision in spec.get("decisions", []):
        text, changed = append_decision(text, decision["date"], decision["name"], decision["rationale"])
        changes["applied" if changed else "skipped"].append(f"decision: {decision['date']} {decision['name'][:40]}")

    for lesson in spec.get("lessons", []):
        text, changed = append_lesson(text, lesson["issue"], lesson["lesson"])
        changes["applied" if changed else "skipped"].append(f"lesson: {lesson['issue'][:50]}")

    for item in spec.get("pending_done", []):
        text, changed = mark_pending_done(text, item)
        if changed:
            changes["applied"].append(f"pending_done: {item[:50]}")
        else:
            # Try as add if not found as existing
            text, changed = add_pending_item(text, item)
            if changed:
                changes["applied"].append(f"pending_add (fallback): {item[:50]}")
            else:
                changes["skipped"].append(f"pending_done: {item[:50]}")

    for item in spec.get("pending_add", []):
        text, changed = add_pending_item(text, item)
        changes["applied" if changed else "skipped"].append(f"pending_add: {item[:50]}")

    return text, changes


def main():
    parser = argparse.ArgumentParser(description="Apply structured updates to TRACKER.md")
    parser.add_argument("--input", "-i", required=True, help="JSON spec file")
    parser.add_argument("--tracker", "-t", default="TRACKER.md", help="TRACKER.md path (default: ./TRACKER.md)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would change without writing")
    args = parser.parse_args()

    spec = load_spec(Path(args.input))
    tracker_path = Path(args.tracker)
    text = load_tracker(tracker_path)

    new_text, changes = apply_spec(text, spec)

    if args.dry_run:
        print("=== DRY RUN — no changes written ===")
        for c in changes["applied"]:
            print(f"  APPLY: {c}")
        for c in changes["skipped"]:
            print(f"  SKIP:  {c}")
        sys.exit(2 if changes["applied"] else 0)

    if changes["applied"]:
        tracker_path.write_text(new_text)
        print(f"✓ Updated {tracker_path}")
        for c in changes["applied"]:
            print(f"  + {c}")
        for c in changes["skipped"]:
            print(f"  - skipped: {c}")
    else:
        print(f"No changes needed (all operations already applied)")
        for c in changes["skipped"]:
            print(f"  = {c}")

    sys.exit(0)


if __name__ == "__main__":
    main()
