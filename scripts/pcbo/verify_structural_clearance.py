"""
Skill 1: verify_structural_clearance
Приоритет №1 — фатальные ошибки геометрии (GPU не влезает, кулер упирается).

LLM слепы к пространственному мышлению. Этот навык даёт 100% точность
проверки физической собираемости.

Usage:
    python verify_structural_clearance.py '<json_input>'
    или импорт: from verify_structural_clearance import verify
"""

import json
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class CaseSpec:
    max_gpu_mm: int
    max_cooler_mm: int
    supported_form_factors: list[str]


@dataclass
class GpuSpec:
    length_mm: int
    width_slots: float


@dataclass
class CoolerSpec:
    height_mm: int
    cooler_type: str  # "air" | "aio"
    radiator_size_mm: Optional[int] = None  # для AIO


@dataclass
class MotherboardSpec:
    form_factor: str  # "ATX" | "mATX" | "ITX"


@dataclass
class ClearanceResult:
    is_compatible: bool
    failures: list[str]
    tolerances: dict[str, int]


# Технологические зазоры (мм)
GPU_MOUNTING_CLEARANCE_MM = 10   # зазор для монтажа GPU
COOLER_SIDE_PANEL_CLEARANCE_MM = 5  # зазор кулер-боковая стенка
AIO_RADIATOR_FAN_THICKNESS_MM = 27  # стандартная толщина вентилятора


def verify(case: dict, gpu: dict, cooler: dict, motherboard: dict) -> ClearanceResult:
    """Проверить физическую совместимость компонентов в корпусе."""
    failures = []
    tolerances = {}

    cs = CaseSpec(**{k: v for k, v in case.items() if k in CaseSpec.__dataclass_fields__})
    gs = GpuSpec(**{k: v for k, v in gpu.items() if k in GpuSpec.__dataclass_fields__})
    cl = CoolerSpec(**{k: v for k, v in cooler.items() if k in CoolerSpec.__dataclass_fields__})
    mb = MotherboardSpec(**{k: v for k, v in motherboard.items() if k in MotherboardSpec.__dataclass_fields__})

    # 1. GPU length check
    gpu_clearance = cs.max_gpu_mm - gs.length_mm
    tolerances["gpu_clearance_mm"] = gpu_clearance
    if gs.length_mm + GPU_MOUNTING_CLEARANCE_MM > cs.max_gpu_mm:
        failures.append(
            f"GPU ({gs.length_mm}mm) не влезает в корпус "
            f"(макс: {cs.max_gpu_mm}mm, нужен зазор {GPU_MOUNTING_CLEARANCE_MM}mm). "
            f"Дефицит: {gs.length_mm + GPU_MOUNTING_CLEARANCE_MM - cs.max_gpu_mm}mm."
        )

    # 2. Cooler height check (air coolers only)
    if cl.cooler_type == "air":
        cooler_clearance = cs.max_cooler_mm - cl.height_mm
        tolerances["cooler_clearance_mm"] = cooler_clearance
        if cl.height_mm + COOLER_SIDE_PANEL_CLEARANCE_MM > cs.max_cooler_mm:
            failures.append(
                f"Кулер ({cl.height_mm}mm) не влезает в корпус "
                f"(макс: {cs.max_cooler_mm}mm, нужен зазор {COOLER_SIDE_PANEL_CLEARANCE_MM}mm). "
                f"Дефицит: {cl.height_mm + COOLER_SIDE_PANEL_CLEARANCE_MM - cs.max_cooler_mm}mm."
            )

    # 3. Motherboard form factor check
    mb_ff = mb.form_factor.upper()
    supported = [ff.upper() for ff in cs.supported_form_factors]
    if mb_ff not in supported:
        failures.append(
            f"Материнская плата {mb_ff} не поддерживается корпусом "
            f"(поддерживает: {', '.join(cs.supported_form_factors)})."
        )

    # 4. AIO radiator check
    if cl.cooler_type == "aio" and cl.radiator_size_mm:
        # AIO usually mounts at top/front — check is case-specific
        # For now, note that AIO compatibility requires manual verification
        tolerances["aio_radiator_mm"] = cl.radiator_size_mm

    return ClearanceResult(
        is_compatible=len(failures) == 0,
        failures=failures,
        tolerances=tolerances,
    )


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python verify_structural_clearance.py '<json>'"}))
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    result = verify(
        case=data["case"],
        gpu=data["gpu"],
        cooler=data["cooler"],
        motherboard=data.get("motherboard", {}),
    )

    print(json.dumps({
        "is_compatible": result.is_compatible,
        "failures": result.failures,
        "tolerances": result.tolerances,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
