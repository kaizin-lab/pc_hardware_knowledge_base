"""
Component Selector — STATE_2.0 through STATE_5.0 пайплайна PCBO.

Детерминированный подбор компонентов через evaluate_profiles + MAUT.
Агент НЕ «думает головой» — вызывает функции и получает ranked candidates.

Каждая функция:
  1. Загружает каталог (catalog/<type>/*.md)
  2. Вызывает evaluate_profiles для profile matching
  3. Фильтрует по constraints (VRAM, socket, form_factor, sustained_write)
  4. Сортирует по MAUT: capability × perf_weight + (1 − price/max_price) × budget_weight
  5. Возвращает ranked list с margin, price, rationale

Использование:
    from component_selector import select_gpu, select_cpu, select_ram, ...
    gpu_candidates = select_gpu(min_capability="balanced_performance_gpu",
                                 min_vram_gb=14, blocked_profiles=["sub_75w_slot_powered"],
                                 budget_remaining=120000, maut_cpu_weight=0.25)
"""

import os, re, sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent.parent  # scripts/pcbo → scripts → KB root
CATALOG = ROOT / "catalog"
SCRIPTS = ROOT / "scripts"

# Import evaluate_profiles functions
sys.path.insert(0, str(SCRIPTS))
from evaluate_profiles import (
    parse_frontmatter, evaluate_component, CAPABILITY_MAP_BY_TYPE,
    get_capability_level, VALID_INTENTS
)


@dataclass
class Candidate:
    id: str
    type: str
    title: str
    price: int
    specs: dict
    profiles: list
    margin: int = 0          # capability − min_capability (GPU only)
    maut_score: float = 0.0
    rationale: str = ""


def _margin_check(profiles: dict, cmp_type: str, min_capability: str | None) -> tuple[int, int]:
    """Return (comp_level, margin) for margin analysis. margin = level − min_level."""
    if not min_capability:
        return (0, 0)
    cap_map = CAPABILITY_MAP_BY_TYPE.get(cmp_type, {})
    if not cap_map:
        return (0, 0)
    comp_tiers = []
    for pname, pd in profiles.items():
        level = cap_map.get(pname)
        if level is not None and pd.get("criteria_met", True):
            comp_tiers.append(level)
    if not comp_tiers:
        return (0, 0)
    comp_level = max(comp_tiers)
    min_level = cap_map.get(min_capability, 1)
    return (comp_level, comp_level - min_level)

def select_gpu(
    min_capability: str,
    min_vram_gb: int,
    blocked_profiles: list[str],
    budget_remaining: int,
    maut_gpu_weight: float = 0.75,
    intents: list[str] | None = None,
) -> list[Candidate]:
    """
    STATE_2.0: подбор GPU.
    
    Фильтры:
      - VRAM ≥ min_vram_gb
      - capability_level ≥ min_capability (margin ≥ 0 = satisfies)
      - НЕ имеет blocked_profiles
      - Цена ≤ budget_remaining
    
    Сортировка: MAUT = (margin=0 → +1) × maut_gpu_weight + (1 − price/max_price) × (1−maut_gpu_weight)
    """
    candidates = []
    gpu_dir = CATALOG / "gpu"
    if not gpu_dir.exists():
        return candidates

    for f in sorted(gpu_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "gpu":
            continue

        specs = fm.get("specs", {})
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        # VRAM check
        vram_raw = specs.get("vram", "0")
        vram_match = re.search(r"(\d+)", str(vram_raw))
        vram_gb = int(vram_match.group(1)) if vram_match else 0
        if vram_gb < min_vram_gb:
            continue

        # Profile check
        profiles = fm.get("profiles", {})
        cap_map = CAPABILITY_MAP_BY_TYPE.get("gpu", {})
        comp_tiers = []
        for pname, pd in profiles.items():
            level = cap_map.get(pname)
            if level is not None and pd.get("criteria_met", True):
                comp_tiers.append((pname, level))

        if not comp_tiers:
            continue

        comp_level = max(t for _, t in comp_tiers)
        min_level = cap_map.get(min_capability, 1)
        margin = comp_level - min_level

        if margin < 0:
            continue  # FAIL

        # Blocked profiles check
        blocked = False
        for bp in blocked_profiles:
            bp_short = bp.split("#")[-1] if "#" in bp else bp
            if bp_short in profiles and profiles[bp_short].get("criteria_met", True):
                blocked = True
                break
        if blocked:
            continue

        # MAUT score: margin=0 → highest, higher margin → penalty
        # perfect = margin 0, цена минимальна
        maut = (1.0 / (1 + margin)) * maut_gpu_weight  # margin penalty
        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="gpu",
            title=fm.get("title", f.stem),
            price=price,
            specs={"vram": vram_gb, "bus": _extract_bus(specs), "tgp": _extract_tgp(specs)},
            profiles=[p for p, _ in comp_tiers],
            margin=margin,
            maut_score=0,  # filled below
            rationale=f"margin={margin:+d}, VRAM={vram_gb}GB"
        ))

    if not candidates:
        return []

    # Normalize MAUT with price component
    max_price = max(c.price for c in candidates)
    for c in candidates:
        price_score = 1.0 - (c.price / max_price) if max_price > 0 else 1.0
        margin_score = 1.0 / (1 + c.margin)  # margin=0 → 1.0, margin=1 → 0.5, margin=2 → 0.33
        c.maut_score = margin_score * maut_gpu_weight + price_score * (1 - maut_gpu_weight)

    candidates.sort(key=lambda c: c.maut_score, reverse=True)
    return candidates


# ═══════════════════ CPU ═══════════════════

def select_cpu(
    socket: str = "AM5",
    budget_remaining: int = 999999,
    maut_cpu_weight: float = 0.25,
    min_capability: str | None = None,
    preferred_profiles: list[str] | None = None,
    blocked_profiles: list[str] | None = None,
) -> list[Candidate]:
    """
    STATE_3.0: подбор CPU под сокет, бюджет и profile matching.
    """
    candidates = []
    cpu_dir = CATALOG / "cpu"
    if not cpu_dir.exists():
        return candidates

    for f in sorted(cpu_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "cpu":
            continue
        specs = fm.get("specs", {})
        if socket.upper() not in specs.get("socket", "").upper():
            continue

        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        profiles = fm.get("profiles", {})
        profile_list = [p for p, pd in profiles.items() if pd.get("criteria_met", True)]

        # Margin analysis (v4.1)
        comp_level, margin = _margin_check(profiles, "cpu", min_capability)
        if margin < 0:
            continue  # FAIL

        # Check blocked
        if blocked_profiles:
            if any(bp.split("#")[-1] in profiles for bp in blocked_profiles):
                continue

        cores = _extract_cores(specs)
        perf_score = min(cores / 16, 1.0)
        margin_penalty = 1.0 / (1 + margin) if margin > 0 else 1.0

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="cpu",
            title=fm.get("title", f.stem),
            price=price,
            specs={"cores": cores, "tdp": _extract_tdp(specs), "socket": socket},
            profiles=profile_list,
            margin=margin,
            maut_score=0,
            rationale=f"{cores} ядер, TDP {_extract_tdp(specs)}W, margin={margin:+d}"
        ))

    if not candidates:
        return []

    max_price = max(c.price for c in candidates) if candidates else 1
    for c in candidates:
        cores = c.specs.get("cores", 1)
        perf_score = min(cores / 16, 1.0)
        price_score = 1.0 - (c.price / max_price) if max_price > 0 else 1.0
        margin_score = 1.0 / (1 + c.margin) if c.margin >= 0 else 0
        c.maut_score = margin_score * 0.3 + perf_score * maut_cpu_weight + price_score * (1 - maut_cpu_weight - 0.3)

    candidates.sort(key=lambda c: c.maut_score, reverse=True)
    return candidates


# ═══════════════════ RAM ═══════════════════

def select_ram(
    min_capacity_gb: int = 32,
    budget_remaining: int = 999999,
    ecc: bool = False,
) -> list[Candidate]:
    """STATE_4a: подбор RAM."""
    candidates = []
    ram_dir = CATALOG / "memory"
    if not ram_dir.exists():
        return candidates

    for f in sorted(ram_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "memory":
            continue
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        specs = fm.get("specs", {})
        cap = _extract_ram_capacity(specs)
        if cap < min_capacity_gb:
            continue

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="memory",
            title=fm.get("title", f.stem),
            price=price,
            specs={"capacity": int(cap), "speed": specs.get("speed", ""), "type": specs.get("type", "DDR5")},
            profiles=[],
            rationale=f"{int(cap)}GB {specs.get('speed', '')}"
        ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Storage ═══════════════════

def select_storage(
    sustained_write_required: bool = False,
    budget_remaining: int = 999999,
) -> list[Candidate]:
    """STATE_4b: подбор SSD. Если sustained_write — исключает DRAM-less и QLC."""
    candidates = []
    storage_dir = CATALOG / "storage" / "nvme"
    if not storage_dir.exists():
        return candidates

    for f in sorted(storage_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "storage":
            continue
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        profiles = fm.get("profiles", {})
        if sustained_write_required:
            # Exclude DRAM-less and QLC
            if "dram_less_hmb_cached" in profiles and profiles["dram_less_hmb_cached"].get("criteria_met", True):
                continue
            if "read_heavy_static" in profiles and profiles["read_heavy_static"].get("criteria_met", True):
                continue

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="storage",
            title=fm.get("title", f.stem),
            price=price,
            specs={"capacity": fm.get("specs", {}).get("capacity", "")},
            profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
            rationale="sustained_write OK" if sustained_write_required else "client use"
        ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Motherboard ═══════════════════

def select_mb(
    socket: str = "AM5",
    form_factor: str = "ATX",
    budget_remaining: int = 999999,
    ecc_required: bool = False,
    no_bifurcation_required: bool = False,  # для AI-инференса
) -> list[Candidate]:
    """STATE_5a: подбор материнской платы."""
    candidates = []
    mb_dir = CATALOG / "motherboard"
    if not mb_dir.exists():
        return candidates

    for root, dirs, files in os.walk(mb_dir):
        for fname in files:
            if not fname.endswith(".md") or fname == "index.md":
                continue
            f = Path(root) / fname
            fm = parse_frontmatter(f)
            if not fm or fm.get("type") != "motherboard":
                continue
            specs = fm.get("specs", {})
            if socket.upper() not in specs.get("socket", "").upper():
                continue

            price_data = fm.get("price_ru", {})
            price = price_data.get("median", 0)
            if not price or price > budget_remaining:
                continue

            profiles = fm.get("profiles", {})
            # No-bifurcation check
            if no_bifurcation_required:
                bif = profiles.get("bifurcation_shared_lanes", {})
                if bif.get("criteria_met", False):
                    continue  # BLOCK: эта плата отнимает линии

            candidates.append(Candidate(
                id=fm.get("id", f.stem),
                type="motherboard",
                title=fm.get("title", f.stem),
                price=price,
                specs={"socket": socket, "form_factor": specs.get("form_factor", "ATX")},
                profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
                rationale=f"{specs.get('chipset', '')} {specs.get('form_factor', '')}"
            ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ PSU ═══════════════════

def select_psu(
    min_wattage: int = 550,
    atx3x_required: bool = False,
    sfx_required: bool = False,
    budget_remaining: int = 999999,
) -> list[Candidate]:
    """STATE_5b: подбор БП."""
    candidates = []
    psu_dir = CATALOG / "psu"
    if not psu_dir.exists():
        return candidates

    for f in sorted(psu_dir.glob("*.md")):
        if f.name == "index.md":
            continue
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "psu":
            continue
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        specs = fm.get("specs", {})
        wattage = _extract_number(specs.get("wattage", "0"))
        if wattage < min_wattage:
            continue

        profiles = fm.get("profiles", {})
        if atx3x_required:
            if "atx_3x_transient_capable" not in profiles:
                continue

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="psu",
            title=fm.get("title", f.stem),
            price=price,
            specs={"wattage": int(wattage), "atx_version": specs.get("atx_version", "")},
            profiles=[p for p in profiles if profiles[p].get("criteria_met", True)],
            rationale=f"{int(wattage)}W {specs.get('atx_version', '')}"
        ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Cooling ═══════════════════

def select_cooler(
    cpu_tdp_w: int = 65,
    max_height_mm: int = 999,
    budget_remaining: int = 999999,
) -> list[Candidate]:
    """STATE_5c: подбор кулера."""
    candidates = []
    for sub in ["air", "liquid"]:
        cool_dir = CATALOG / "cooling" / sub
        if not cool_dir.exists():
            continue
        for f in sorted(cool_dir.glob("*.md")):
            if f.name == "index.md":
                continue
            fm = parse_frontmatter(f)
            if not fm or fm.get("type") != "cooling":
                continue
            price_data = fm.get("price_ru", {})
            price = price_data.get("median", 0)
            if not price or price > budget_remaining:
                continue

            specs = fm.get("specs", {})
            tdp_rating = _extract_number(specs.get("tdp_rating_w", specs.get("tdp", "0")))
            height = _extract_number(specs.get("height_mm", "0"))
            if height > max_height_mm:
                continue
            if tdp_rating < cpu_tdp_w:
                continue

            candidates.append(Candidate(
                id=fm.get("id", f.stem),
                type="cooling",
                title=fm.get("title", f.stem),
                price=price,
                specs={"tdp_rating": int(tdp_rating), "height_mm": int(height), "type": sub},
                profiles=[],
                rationale=f"TDP {int(tdp_rating)}W, {int(height)}mm, {sub}"
            ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Case ═══════════════════

def select_case(
    gpu_length_mm: int = 300,
    cooler_height_mm: int = 155,
    form_factor: str = "ATX",
    budget_remaining: int = 999999,
) -> list[Candidate]:
    """STATE_5d: подбор корпуса."""
    candidates = []
    case_dir = CATALOG / "case"
    if not case_dir.exists():
        return candidates

    for f in sorted(case_dir.glob("*.md")):
        if f.name == "index.md":
            continue
        fm = parse_frontmatter(f)
        if not fm or fm.get("type") != "case":
            continue
        price_data = fm.get("price_ru", {})
        price = price_data.get("median", 0)
        if not price or price > budget_remaining:
            continue

        specs = fm.get("specs", {})
        max_gpu = _extract_number(specs.get("max_gpu_mm", "0"))
        max_cooler = _extract_number(specs.get("max_cooler_mm", "0"))
        if max_gpu < gpu_length_mm:
            continue
        if max_cooler < cooler_height_mm:
            continue

        candidates.append(Candidate(
            id=fm.get("id", f.stem),
            type="case",
            title=fm.get("title", f.stem),
            price=price,
            specs={"max_gpu_mm": int(max_gpu), "max_cooler_mm": int(max_cooler)},
            profiles=[],
            rationale=f"GPU ≤{int(max_gpu)}mm, cooler ≤{int(max_cooler)}mm"
        ))

    candidates.sort(key=lambda c: c.price)
    return candidates


# ═══════════════════ Helpers ═══════════════════

def _extract_number(raw: Any) -> float:
    if raw is None:
        return 0
    if isinstance(raw, (int, float)):
        return float(raw)
    m = re.search(r"(\d+(?:\.\d+)?)", str(raw))
    return float(m.group(1)) if m else 0


def _extract_ram_capacity(specs: dict) -> int:
    """Extract total RAM capacity in GB from specs.
    Handles '32 GB (2×16 GB)', '2×16 GB (32 GB)', '32GB', etc.
    """
    raw = specs.get("capacity_gb", specs.get("capacity", "0"))
    if isinstance(raw, (int, float)):
        return int(raw)
    s = str(raw)
    # Try to find number in parentheses first (total capacity)
    m = re.search(r"\((\d+)\s*GB\)", s, re.IGNORECASE)
    if m:
        return int(m.group(1))
    # Then try "XX GB" pattern
    m = re.search(r"(\d+)\s*GB", s, re.IGNORECASE)
    if m:
        return int(m.group(1))
    # Fallback: first number
    return int(_extract_number(s))


def _extract_bus(specs: dict) -> int:
    bus_raw = specs.get("vram_bandwidth", specs.get("bus", ""))
    m = re.search(r"(\d+)-bit", str(bus_raw))
    return int(m.group(1)) if m else 0


def _extract_tgp(specs: dict) -> int:
    return int(_extract_number(specs.get("tbp") or specs.get("tgp") or specs.get("tdp") or 0))


def _extract_tdp(specs: dict) -> int:
    return int(_extract_number(specs.get("tdp") or 0))


def _extract_cores(specs: dict) -> int:
    cores_raw = specs.get("cores", specs.get("core_count", "0"))
    return int(_extract_number(cores_raw))


# ═══════════════════ Self-test ═══════════════════

if __name__ == "__main__":
    print("=== GPU (1440p ultra, 120K) ===")
    gpus = select_gpu(
        min_capability="balanced_performance_gpu",
        min_vram_gb=14,
        blocked_profiles=["sub_75w_slot_powered"],
        budget_remaining=120000,
        maut_gpu_weight=0.75
    )
    for g in gpus:
        print(f"  [{g.maut_score:.3f}] {g.id:25s} {g.price:>7,d}₽  margin={g.margin:+d}  {g.rationale}")

    print("\n=== CPU (AM5, 58K budget) ===")
    cpus = select_cpu(socket="AM5", budget_remaining=58000, maut_cpu_weight=0.25)
    for c in cpus[:5]:
        print(f"  [{c.maut_score:.3f}] {c.id:25s} {c.price:>7,d}₽  {c.rationale}")

    print("\n=== Storage (no sustained write, 10K) ===")
    ssds = select_storage(sustained_write_required=False, budget_remaining=10000)
    for s in ssds:
        print(f"  {s.id:30s} {s.price:>7,d}₽  {s.rationale}")

    print("\n=== PSU (750W+, ATX 3.x, 12K) ===")
    psus = select_psu(min_wattage=700, atx3x_required=False, budget_remaining=12000)
    for p in psus:
        print(f"  {p.id:30s} {p.price:>7,d}₽  {p.rationale}")
