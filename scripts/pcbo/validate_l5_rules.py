'''
Skill 7: validate_l5_rules
Финал — агрегатор результатов всех 6 симуляций.

Собирает выходы Skills 1-6 и выносит итоговый вердикт:
- PASS — все проверки пройдены
- PASS_WITH_WARNINGS — есть WARN, но не BLOCK
- FAIL — хотя бы один BLOCK → rollback
'''

import json, sys


def validate(data: dict) -> dict:
    structural = data.get("structural_clearance", {})
    power = data.get("power_state", {})
    thermal = data.get("thermal_profile", {})
    acoustic = data.get("acoustic_class", {})
    pcie = data.get("pcie_topology", {})
    budget = data.get("budget", {})

    failed_checks = []
    warnings = []

    # BLOCK checks
    if not structural.get("is_compatible", True):
        failed_checks.append("STRUCTURAL: Компоненты физически несовместимы.")

    if power.get("status") == "BLOCK":
        failed_checks.append(f"POWER: {power.get('messages', ['BLOCK'])[0]}")

    if thermal.get("cpu_thermal_state") in ("T_Throttle", "T_Critical"):
        failed_checks.append(
            f"THERMAL: CPU достигает {thermal.get('cpu_thermal_state')} "
            f"({thermal.get('predicted_cpu_temp_C', '?')}°C)."
        )

    if thermal.get("gpu_thermal_state") in ("T_Throttle", "T_Critical"):
        failed_checks.append(
            f"THERMAL: GPU достигает {thermal.get('gpu_thermal_state')}."
        )

    # WARN checks
    if power.get("status") == "WARN":
        warnings.extend(power.get("messages", []))

    if thermal.get("cpu_thermal_state") == "T_Hot":
        warnings.append(
            f"THERMAL: CPU {thermal.get('predicted_cpu_temp_C', '?')}°C — "
            f"близко к пределу."
        )

    if not acoustic.get("is_compliant", True):
        warnings.extend(acoustic.get("warnings", []))

    if pcie.get("warnings"):
        warnings.extend(pcie.get("warnings", []))

    if not pcie.get("storage_sustained_write_compliant", True):
        warnings.extend(pcie.get("warnings", []))

    # Budget check
    if budget:
        actual = budget.get("actual_cost", 0)
        ceiling = budget.get("ceiling", float("inf"))
        if actual > ceiling:
            failed_checks.append(
                f"BUDGET: {actual} превышает потолок {ceiling} "
                f"на {actual - ceiling}."
            )

    # Deduplicate
    warnings = list(dict.fromkeys(warnings))
    if failed_checks:
        status = "FAIL"
        action = "rollback"
    elif warnings:
        status = "PASS_WITH_WARNINGS"
        action = "proceed_to_document"
    else:
        status = "PASS"
        action = "proceed_to_document"

    return {
        "validation_status": status,
        "action_required": action,
        "failed_check_ids": failed_checks,
        "warnings": warnings,
        "summary": {
            "PASS": "Все проверки пройдены. Можно формировать Build Artifact.",
            "PASS_WITH_WARNINGS": "Есть предупреждения. Сборка допустима, но с оговорками.",
            "FAIL": "Критические ошибки. Необходим rollback и пересмотр.",
        }[status],
    }


if __name__ == "__main__":
    data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)
    print(json.dumps(validate(data), ensure_ascii=False, indent=2))
