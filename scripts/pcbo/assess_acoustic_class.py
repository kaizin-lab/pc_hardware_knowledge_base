'''
Skill 6: assess_acoustic_class
Приоритет №6 — математический класс шума вместо субъективного «тихий/громкий».

Также детектирует DPC latency risk от RGB-экосистем (софтверный конфликт).
'''

import json, sys

# Acoustic classes (idle / load)
# A0: неслышно (< 25 dBA)
# A1: ambient (25-30 dBA, фоновый шум)
# A2: low hum (30-35 dBA, слышно в тишине)
# A3: noticeable (35-42 dBA, мешает концентрации)
# A4: loud (> 42 dBA, требуется закрытый корпус / наушники)

# System power → minimum possible load acoustic class
POWER_ACOUSTIC_FLOOR = [
    (200, "A1"),   # < 200W: можно сделать A1
    (350, "A2"),   # 200-350W: минимум A2 под нагрузкой
    (500, "A3"),   # 350-500W: минимум A3
    (9999, "A4"),  # > 500W: A4
]

# Cooler type modifiers
COOLER_ACOUSTIC = {
    "air_dual_tower": {"idle": "A0", "load_floor": "A1"},
    "air_single_tower": {"idle": "A1", "load_floor": "A2"},
    "air_92mm": {"idle": "A1", "load_floor": "A3"},
    "aio_240mm": {"idle": "A0", "load_floor": "A1"},
    "aio_280mm": {"idle": "A0", "load_floor": "A1"},
    "aio_360mm": {"idle": "A0", "load_floor": "A1"},
    "box": {"idle": "A2", "load_floor": "A3"},
}

GPU_COOLER_ACOUSTIC = {
    "open_air_3fan": "A1",
    "open_air_2fan": "A2",
    "blower": "A3",
}

ACOUSTIC_ORDER = ["A0", "A1", "A2", "A3", "A4"]


def max_class(a: str, b: str) -> str:
    return a if ACOUSTIC_ORDER.index(a) >= ACOUSTIC_ORDER.index(b) else b


def evaluate(data: dict) -> dict:
    system_power = data["system_power_W"]
    components = data["components"]
    noise_constraint = data.get("noise_constraint", "moderate")

    # 1. Power-based floor
    load_floor = "A1"
    for threshold, floor_class in POWER_ACOUSTIC_FLOOR:
        if system_power < threshold:
            load_floor = floor_class
            break

    # 2. Cooler contribution
    cooler = COOLER_ACOUSTIC.get(
        components.get("cooler_type", "air_single_tower"),
        {"idle": "A1", "load_floor": "A2"},
    )
    idle_class = cooler["idle"]
    load_class = max_class(load_floor, cooler["load_floor"])

    # 3. GPU cooler contribution
    gpu_acoustic = GPU_COOLER_ACOUSTIC.get(
        components.get("gpu_cooler", "open_air_3fan"), "A2"
    )
    load_class = max_class(load_class, gpu_acoustic)

    # 4. PSU contribution
    if components.get("psu_mode") == "always_on":
        idle_class = max_class(idle_class, "A1")

    # 5. DPC latency risk from RGB ecosystems
    rgb_count = len(components.get("rgb_ecosystems", []))
    dpc_risk = rgb_count >= 3

    # 6. Compliance check
    CONSTRAINT_MAP = {
        "silent": "A1",
        "strict": "A2",
        "moderate": "A3",
        "none": "A4",
    }
    max_allowed = CONSTRAINT_MAP.get(noise_constraint, "A3")
    compliant = ACOUSTIC_ORDER.index(load_class) <= ACOUSTIC_ORDER.index(max_allowed)

    warnings = []
    if dpc_risk:
        warnings.append(
            f"DPC_LATENCY: {rgb_count} RGB-экосистем создают риск "
            f"конфликта фонового ПО → микрофризы/задержки аудио."
        )
    if not compliant:
        warnings.append(
            f"ACOUSTIC: Класс шума {load_class} превышает ограничение "
            f"{noise_constraint} (макс: {max_allowed})."
        )

    return {
        "predicted_acoustic_class_idle": idle_class,
        "predicted_acoustic_class_load": load_class,
        "high_dpc_latency_risk": dpc_risk,
        "is_compliant": compliant,
        "warnings": warnings,
    }


if __name__ == "__main__":
    data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)
    print(json.dumps(evaluate(data), ensure_ascii=False, indent=2))
