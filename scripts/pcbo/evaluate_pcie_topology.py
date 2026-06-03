'''
Skill 2: evaluate_pcie_topology
Приоритет №2 — «тихий убийца» производительности.

LLM не читают таблицы бифуркации из мануалов. Этот навык детектирует:
- Потерю линий GPU при установке 2+ M.2 (x16 → x8)
- DRAM-less SSD под data engineering (скорость упадёт до HDD)
- Падение offload bandwidth для AI-нагрузок
'''

import json, sys
from dataclasses import dataclass

# MB chipsets that steal GPU lanes when 2+ M.2 slots are occupied
BIFURCATION_CHIPSETS = {"B650", "B650M", "B760", "B760M", "B660", "B660M", "H610", "H670"}

# Chipsets that keep full x16 regardless
FULL_X16_CHIPSETS = {"X670", "X670E", "X870", "X870E", "Z790", "Z690", "Z890"}


def evaluate(data: dict) -> dict:
    platform = data["platform"]
    chipset = data.get("motherboard_chipset", "")
    m2_count = data.get("m2_drives_count", 1)
    gpu = data["gpu"]
    storage = data.get("storage_target", {})
    intent = data.get("intent", "")

    warnings = []
    gpu_effective_lanes = gpu["pcie_width"]

    # 1. Bifurcation check
    if chipset in BIFURCATION_CHIPSETS and m2_count >= 2:
        gpu_effective_lanes = 8
        warnings.append(
            f"BIFURCATION: На чипсете {chipset} при {m2_count} M.2-накопителях "
            f"GPU переходит в режим x{gpu_effective_lanes} (вместо x{gpu['pcie_width']}). "
            f"Линии чипсета разделены между M.2 и PCIe-слотом."
        )

    if chipset in FULL_X16_CHIPSETS:
        # Full x16 chipsets — no bifurcation risk
        pass

    # 2. AI workload bandwidth impact
    offload_bandwidth_gbs = None
    if gpu_effective_lanes < gpu["pcie_width"] and intent == "ai_inference_local":
        # PCIe gen × lanes × encoding
        pcie_gen = gpu.get("pcie_generation", 4)
        bw_per_lane = {3: 0.985, 4: 1.969, 5: 3.938}[pcie_gen]
        offload_bandwidth_gbs = gpu_effective_lanes * bw_per_lane
        warnings.append(
            f"AI_OFFLOAD: RAM Offload bandwidth снижен до {offload_bandwidth_gbs:.1f} GB/s "
            f"(x{gpu_effective_lanes} вместо x{gpu['pcie_width']}). "
            f"LLM 70B offload будет в 2× медленнее."
        )

    # 3. DRAM-less SSD under data engineering
    storage_compliant = True
    if storage.get("workload_type") == "data_engineering" and not storage.get("has_dram", True):
        storage_compliant = False
        warnings.append(
            "VAL-DATA-01: DRAM-less SSD (HMB) непригоден для data engineering. "
            "После исчерпания SLC-кэша скорость записи упадёт до 200-400 MB/s "
            "(уровень HDD). Требуется SSD с DRAM-буфером или TLC с устойчивой записью."
        )

    return {
        "gpu_effective_pcie_lanes": gpu_effective_lanes,
        "offload_bandwidth_gbs": round(offload_bandwidth_gbs, 1) if offload_bandwidth_gbs else None,
        "storage_sustained_write_compliant": storage_compliant,
        "warnings": warnings,
        "original_gpu_lanes": gpu["pcie_width"],
        "lane_loss": gpu["pcie_width"] - gpu_effective_lanes,
    }


if __name__ == "__main__":
    data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)
    print(json.dumps(evaluate(data), ensure_ascii=False, indent=2))
