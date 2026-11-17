#!/usr/bin/env python3
"""Validate the knowledge base structure.

Checks:
  - YAML frontmatter parses;
  - no duplicate top-level keys;
  - every path in `links:` exists (paths are relative to the repo root);
  - every relative Markdown link exists (paths are relative to the file);
  - every directory under catalog/ has an index.md.

Usage:
    pip install -r requirements.txt
    python scripts/check_links.py
"""

import re
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install: pip install -r requirements.txt")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"README.md", "AUDIT_REPORT.md"}

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")
TOP_KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):", re.MULTILINE)


def main() -> int:
    errors: list[str] = []
    checked = 0
    parsed = 0

    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts or path.name in SKIP:
            continue
        checked += 1
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")

        m = FM_RE.match(text)
        if not m:
            # Narrative arcs, reports and a few old entries have no frontmatter.
            continue
        parsed += 1

        raw = m.group(1)
        try:
            fm = yaml.safe_load(raw) or {}
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: YAML error: {exc}")
            continue

        keys = Counter(TOP_KEY_RE.findall(raw))
        for key, count in keys.items():
            if count > 1:
                errors.append(f"{rel}: duplicate top-level key '{key}' ({count})")

        links = fm.get("links") or {}
        if isinstance(links, dict):
            for name, target in links.items():
                values = target if isinstance(target, list) else [target]
                for value in values:
                    if not isinstance(value, str) or value.startswith(("http", "#")):
                        continue
                    if not (ROOT / value).exists():
                        errors.append(f"{rel}: links.{name} -> missing {value}")

        for target in MD_LINK_RE.findall(text):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http", "mailto:", "#")):
                continue
            if not (path.parent / target).exists():
                errors.append(f"{rel}: markdown link -> missing {target}")

    for directory in sorted((ROOT / "catalog").rglob("*")):
        if directory.is_dir() and not (directory / "index.md").exists():
            errors.append(f"{directory.relative_to(ROOT)}: missing index.md")

    print(f"checked {checked} markdown files, {parsed} with frontmatter")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("no broken links, duplicate keys, YAML errors, or missing indexes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
