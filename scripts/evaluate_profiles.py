#!/usr/bin/env python3
"""Оценка профилей компонентов через O(1) set intersection с интентами пользователя.

Usage:
  python scripts/evaluate_profiles.py --intents "esports_1080p_360hz,heavy_compilation"
  python scripts/evaluate_profiles.py --intents "llm_inference_13b" --type gpu
  python scripts/evaluate_profiles.py --component catalog/gpu/nvidia-rtx-5070.md
  python scripts/evaluate_profiles.py --check-transitivity  # аудит консистентности

Контролируемый словарь интентов — см. concepts/epistemological-profiles.md
"""

import os, re, sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"


# ── Intent vocabulary (all valid intent IDs) ─────────────────────────

VALID_INTENTS = {
    # Gaming
    "esports_1080p_240hz", "esports_1080p_360hz",
    "aaa_1080p_ultra", "aaa_1440p_high", "aaa_4k_ultra", "aaa_4k_path_tracing",
    # AI/ML
    "llm_inference_7b", "llm_inference_13b", "llm_inference_20b",
    "llm_training_lora", "stable_diffusion", "ai_upscaling",
    # Productivity
    "heavy_compilation", "3d_rendering_cpu", "3d_rendering_gpu",
    "video_editing_4k", "video_editing_8k", "scientific_computing",
    "data_engineering", "software_development", "office_productivity",
    # Operational
    "silent_build", "sff_build", "home_server_24_7", "streaming", "virtualization",
}


# ── Frontmatter parser (PyYAML) ──────────────────────────────────────

def parse_frontmatter(filepath: Path) -> dict[str, Any]:
    text = filepath.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        # Fallback: no closing ---, use markdown heading as boundary
        heading = re.search(r"\n\n#+\s", text)
        if heading:
            raw = text[4:heading.start()]
        else:
            return {}
    else:
        raw = m.group(1)

    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}


# ── Profile evaluator ────────────────────────────────────────────────

def evaluate_component(
    filepath: Path, user_intents: set[str]
) -> dict[str, Any]:
    """Evaluate a single component against user intents. Returns conflicts."""
    fm = parse_frontmatter(filepath)
    profiles = fm.get("profiles", {})
    cmp_id = fm.get("id", filepath.stem)
    cmp_type = fm.get("type", "unknown")
    title = fm.get("title", cmp_id)

    rel_path = str(filepath.resolve().relative_to(ROOT.resolve()))
    result = {
        "id": cmp_id,
        "type": cmp_type,
        "title": title,
        "file": rel_path,
        "optimal": [],       # profiles where this component is optimal for user intents
        "warnings": [],      # WARN-severity conflicts
        "blocks": [],        # BLOCK-severity conflicts
        "irrelevant": [],    # profiles that don't intersect user intents
    }

    for profile_name, profile_data in profiles.items():
        optimal_for = set(profile_data.get("optimal_for_intents", []))
        failure_for = set(profile_data.get("failure_for_intents", []))
        severity = profile_data.get("failure_severity", "WARN")
        criteria_met = profile_data.get("criteria_met", False)

        if not criteria_met:
            continue

        # Check optimal match
        if optimal_for & user_intents:
            result["optimal"].append({
                "profile": profile_name,
                "matched_intents": sorted(optimal_for & user_intents),
                "steel_man": profile_data.get("steel_man_desc", ""),
            })

        # Check failure modes
        failure_match = failure_for & user_intents
        if failure_match:
            entry = {
                "profile": profile_name,
                "conflict_intents": sorted(failure_match),
                "failure_desc": profile_data.get("failure_mode_desc", ""),
                "severity": severity,
            }
            if severity == "BLOCK":
                result["blocks"].append(entry)
            else:
                result["warnings"].append(entry)

        # Profiles with no intersection
        if not (optimal_for & user_intents) and not (failure_for & user_intents):
            if criteria_met:
                result["irrelevant"].append(profile_name)

    return result


def find_entries(catalog_path: Path, entry_type: str | None = None) -> list[Path]:
    entries = []
    for root, dirs, files in os.walk(catalog_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.endswith(".md") or f == "index.md":
                continue
            filepath = Path(root) / f
            fm = parse_frontmatter(filepath)
            etype = fm.get("type", "unknown")
            if entry_type and etype != entry_type:
                continue
            # Only evaluate components that have profiles
            if fm.get("profiles"):
                entries.append(filepath)
    return sorted(entries)


# ── Transitivity check ───────────────────────────────────────────────

def check_transitivity(entries: list[Path]) -> list[str]:
    """Verify: if component A has profile X with optimal_for Y, 
    and component B has the same specs, B must also have profile X."""
    issues = []
    profiles_by_type: dict[str, list[tuple[Path, dict]]] = {}

    for fp in entries:
        fm = parse_frontmatter(fp)
        profiles = fm.get("profiles", {})
        for pname, pdata in profiles.items():
            if pdata.get("criteria_met"):
                profiles_by_type.setdefault(pname, []).append((fp, pdata))

    for pname, entries_list in profiles_by_type.items():
        # Check that optimal_for_intents are consistent across same-profile components
        first_optimal = set(entries_list[0][1].get("optimal_for_intents", []))
        first_failure = set(entries_list[0][1].get("failure_for_intents", []))
        for fp, pdata in entries_list[1:]:
            cur_optimal = set(pdata.get("optimal_for_intents", []))
            cur_failure = set(pdata.get("failure_for_intents", []))
            if cur_optimal != first_optimal:
                issues.append(
                    f"TRANSITIVITY: {pname} — {fp.stem} optimal={sorted(cur_optimal)} "
                    f"differs from {entries_list[0][0].stem} optimal={sorted(first_optimal)}"
                )
            if cur_failure != first_failure:
                issues.append(
                    f"TRANSITIVITY: {pname} — {fp.stem} failure={sorted(cur_failure)} "
                    f"differs from {entries_list[0][0].stem} failure={sorted(first_failure)}"
                )
    return issues


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    user_intents: set[str] = set()
    entry_type = None
    target_component = None
    do_transitivity = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--intents" and i + 1 < len(args):
            raw = args[i + 1]
            intents_list = [x.strip() for x in raw.split(",")]
            invalid = set(intents_list) - VALID_INTENTS
            if invalid:
                print(f"ERROR: Invalid intents: {invalid}")
                print(f"Valid intents: {sorted(VALID_INTENTS)}")
                sys.exit(1)
            user_intents = set(intents_list)
            i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            entry_type = args[i + 1]
            i += 2
        elif args[i] == "--component" and i + 1 < len(args):
            target_component = args[i + 1]
            i += 2
        elif args[i] == "--check-transitivity":
            do_transitivity = True
            i += 1
        else:
            i += 1

    # Transitivity audit mode
    if do_transitivity:
        entries = find_entries(CATALOG)
        if not entries:
            print("Нет компонентов с профилями для проверки транзитивности.")
            return
        issues = check_transitivity(entries)
        if issues:
            print(f"# Нарушения транзитивности ({len(issues)}):\n")
            for iss in issues:
                print(f"  ⚠ {iss}")
        else:
            print(f"# Транзитивность: OK ({len(entries)} компонентов, нарушения не обнаружены)")
        return

    # Single component mode
    if target_component:
        fp = Path(target_component)
        if not fp.exists():
            fp = ROOT / target_component
        if not fp.exists():
            print(f"ERROR: File not found: {target_component}")
            sys.exit(1)
        entries = [fp]
    else:
        entries = find_entries(CATALOG, entry_type)

    if not entries:
        print("Нет компонентов с профилями для оценки.")
        if not user_intents:
            print("Сначала присвойте профили компонентам через аудит.")
        return

    # Evaluation mode
    if not user_intents:
        print("Укажите интенты через --intents")
        print(f"Пример: --intents \"esports_1080p_360hz,heavy_compilation\"")
        print(f"\nДоступные интенты: {sorted(VALID_INTENTS)}")
        return

    print(f"# Оценка профилей для интентов: {sorted(user_intents)}\n")

    all_optimal = []
    all_warnings = []
    all_blocks = []

    for fp in entries:
        result = evaluate_component(fp, user_intents)

        if result["optimal"] or result["warnings"] or result["blocks"]:
            rel = str(fp.resolve().relative_to(ROOT.resolve()))
            print(f"## {result['title']} ({rel})")

            for opt in result["optimal"]:
                print(f"  ✓ optimal: {opt['profile']} → {opt['matched_intents']}")
                all_optimal.append((result["id"], opt))

            for warn in result["warnings"]:
                print(f"  ⚠ WARN:   {warn['profile']} → конфликтует с {warn['conflict_intents']}")
                print(f"           {warn['failure_desc'][:120]}...")
                all_warnings.append((result["id"], warn))

            for block in result["blocks"]:
                print(f"  ✗ BLOCK:  {block['profile']} → несовместим с {block['conflict_intents']}")
                print(f"           {block['failure_desc'][:120]}...")
                all_blocks.append((result["id"], block))

            print()

    # Summary
    print(f"# Сводка\n")
    print(f"  Оптимальных совпадений: {len(all_optimal)}")
    print(f"  Предупреждений (WARN):  {len(all_warnings)}")
    print(f"  Блокировок (BLOCK):     {len(all_blocks)}")

    if all_blocks:
        print(f"\n  ❌ Блокирующие конфликты:")
        for cid, block in all_blocks:
            print(f"     {cid}: {block['profile']} × {block['conflict_intents']}")

    if all_warnings:
        print(f"\n  ⚠ Предупреждения:")
        for cid, warn in all_warnings:
            print(f"     {cid}: {warn['profile']} × {warn['conflict_intents']}")


if __name__ == "__main__":
    main()
