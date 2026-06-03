'''
Skill 5: calculate_power_states
Приоритет №5 — энергобаланс, ATX 3.0, transient spikes.

LLM складывают ватты сносно, но не проверяют микросекундные пики.
Этот навык предотвращает случайные перезагрузки под нагрузкой.
'''

import json, sys


def evaluate(data: dict) -> dict:
    cpu_tdp = data["cpu_tdp_W"]
    gpu_tgp = data["gpu_tgp_W"]
    overhead = data.get("platform_overhead_W", 50)
    psu = data["psu"]

    gaming_load = (cpu_tdp * 0.5) + (gpu_tgp * 0.9) + overhead
    full_load = cpu_tdp + gpu_tgp + overhead

    psu_headroom = psu["wattage"] / full_load if full_load > 0 else 999
    gaming_headroom = psu["wattage"] / gaming_load if gaming_load > 0 else 999

    # ATX 3.0 requirement: GPUs >= 250W need ATX 3.0 for transient spike handling
    atx3_required = gpu_tgp >= 250
    atx3_satisfied = psu.get("specification", "").upper() in ("ATX3.0", "ATX3.1") or not atx3_required

    # Status determination
    status = "PASS"
    messages = []

    # BLOCK: PSU < 110% of full load
    if psu_headroom < 1.1:
        status = "BLOCK"
        messages.append(
            f"BLOCK: БП {psu['wattage']}W недостаточен. "
            f"Full load: {full_load:.0f}W, нужно минимум {full_load * 1.1:.0f}W."
        )

    # BLOCK: ATX 3.0 required but not satisfied
    if atx3_required and not atx3_satisfied:
        if status != "BLOCK":
            status = "BLOCK"
        messages.append(
            f"BLOCK: GPU {gpu_tgp}W требует БП ATX 3.0/3.1 "
            f"(защита от transient spikes). Текущий: {psu.get('specification', 'не указан')}."
        )

    # WARN: gaming headroom < 1.5
    if status == "PASS" and gaming_headroom < 1.5:
        status = "WARN"
        messages.append(
            f"WARN: Запас по мощности для gaming ({gaming_headroom:.1f}×) "
            f"ниже рекомендуемого 1.5×. Пиковые нагрузки могут вызывать OCP-срабатывания."
        )

    if status == "PASS" and not messages:
        messages.append("PASS: Энергобаланс в норме.")

    return {
        "gaming_power_W": round(gaming_load),
        "full_load_power_W": round(full_load),
        "psu_headroom_factor": round(psu_headroom, 2),
        "gaming_headroom_factor": round(gaming_headroom, 2),
        "atx_3_spec_required": atx3_required,
        "atx_3_spec_satisfied": atx3_satisfied,
        "status": status,
        "messages": messages,
    }


if __name__ == "__main__":
    data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)
    print(json.dumps(evaluate(data), ensure_ascii=False, indent=2))
