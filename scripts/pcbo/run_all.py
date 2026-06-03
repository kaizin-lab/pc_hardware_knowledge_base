"""
Сквозной прогон всех 6 симуляций + L5 Gate.

Использование:
    python run_all.py '<build_json>'

build_json содержит все данные для Skills 1-7.
"""

import json, sys
from verify_structural_clearance import verify as skill1
from evaluate_pcie_topology import evaluate as skill2
from simulate_thermal_profiles import evaluate as skill3
from evaluate_marginal_value import evaluate as skill4
from calculate_power_states import evaluate as skill5
from assess_acoustic_class import evaluate as skill6
from validate_l5_rules import validate as skill7


def run_all(build: dict) -> dict:
    results = {}

    # Skill 1: Structural
    if all(k in build for k in ("case", "gpu", "cooler", "motherboard")):
        r1 = skill1(build["case"], build["gpu"], build["cooler"], build["motherboard"])
        results["structural_clearance"] = {
            "is_compatible": r1.is_compatible,
            "failures": r1.failures,
            "tolerances": r1.tolerances,
        }

    # Skill 2: PCIe
    if "pcie" in build:
        results["pcie_topology"] = skill2(build["pcie"])

    # Skill 3: Thermal
    if "thermal" in build:
        results["thermal_profile"] = skill3(build["thermal"])

    # Skill 4: MV (may be called multiple times per component)
    if "mv_candidates" in build:
        mv_results = {}
        for name, mv_input in build["mv_candidates"].items():
            mv_results[name] = skill4(**mv_input)
        results["marginal_value"] = mv_results

    # Skill 5: Power
    if "power" in build:
        results["power_state"] = skill5(build["power"])

    # Skill 6: Acoustic
    if "acoustic" in build:
        results["acoustic_class"] = skill6(build["acoustic"])

    # Skill 7: L5 Gate
    l5_input = {
        "structural_clearance": results.get("structural_clearance", {}),
        "power_state": results.get("power_state", {}),
        "thermal_profile": results.get("thermal_profile", {}),
        "acoustic_class": results.get("acoustic_class", {}),
        "pcie_topology": results.get("pcie_topology", {}),
        "budget": build.get("budget", {}),
    }
    results["l5_validation"] = skill7(l5_input)

    return results


if __name__ == "__main__":
    data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)
    output = run_all(data)
    print(json.dumps(output, ensure_ascii=False, indent=2))
