'''
Skill 3: simulate_thermal_profiles
Приоритет №3 — взаимный нагрев и учёт ambient temperature.

LLM считают температуры качественно («кулер хороший — холодно»).
Этот навык даёт численное предсказание с учётом:
- Температуры в помещении (ambient)
- Класса airflow корпуса (restricted/normal/high_airflow)
- Взаимного нагрева GPU→CPU (Airflow Topology)
'''

import json, sys
from dataclasses import dataclass

# Airflow delta (нагрев воздуха внутри корпуса относительно ambient)
AIRFLOW_DELTA = {
    "restricted": 15.0,
    "normal": 8.0,
    "high_airflow": 3.0,
}

# GPU-CPU mutual heating threshold
GPU_MUTUAL_HEATING_THRESHOLD_W = 200  # если GPU > 200W, греет CPU-кулер
GPU_MUTUAL_HEATING_FACTOR = 0.05     # 5% TGP добавляется к internal ambient

# Typical cooler efficiency (Δ°C per Watt)
COOLER_EFFICIENCY = {
    "air_tower_120mm": 0.25,    # 120mm башня: +1°C за 4W
    "air_tower_140mm": 0.20,    # 140mm башня: +1°C за 5W
    "air_92mm": 0.45,           # 92mm кулер: +1°C за 2.2W
    "aio_240mm": 0.15,          # 240mm AIO
    "aio_280mm": 0.12,          # 280mm AIO
    "aio_360mm": 0.10,          # 360mm AIO
    "box": 0.60,                # Боксовый кулер
}

# Thermal state thresholds
THERMAL_STATES = [
    ("T_Cool", 55),
    ("T_Warm", 75),
    ("T_Hot", 85),
    ("T_Throttle", 95),
]


def classify_thermal(temp_c: float) -> str:
    for state, threshold in THERMAL_STATES:
        if temp_c < threshold:
            return state
    return "T_Critical"


def evaluate(data: dict) -> dict:
    ambient = data["ambient_temp_C"]
    cpu = data["cpu"]
    gpu = data["gpu"]
    cooler = data["cooler"]
    case = data["case"]

    # 1. Case internal delta
    case_delta = AIRFLOW_DELTA.get(case["airflow_class"], 8.0)
    internal_ambient = ambient + case_delta

    # 2. GPU-CPU mutual heating (Airflow Topology)
    gpu_effective_w = gpu["tgp_W"] * gpu.get("load_factor", 0.9)
    if cooler.get("cooler_type", "air") == "air" and gpu_effective_w > GPU_MUTUAL_HEATING_THRESHOLD_W:
        gpu_heat_contribution = gpu_effective_w * GPU_MUTUAL_HEATING_FACTOR
        internal_ambient += gpu_heat_contribution

    # 3. CPU temperature
    efficiency = COOLER_EFFICIENCY.get(
        cooler.get("efficiency_class", "air_tower_120mm"), 0.25
    )
    cpu_effective_w = cpu["tdp_W"] * cpu.get("load_factor", 0.8)
    cpu_temp = internal_ambient + (cpu_effective_w / (1.0 / efficiency))

    # 4. GPU temperature estimation
    gpu_temp = ambient + case_delta * 0.7  # GPU has direct airflow usually

    return {
        "ambient_temp_C": ambient,
        "case_delta_C": round(case_delta, 1),
        "internal_case_ambient_C": round(internal_ambient, 1),
        "predicted_cpu_temp_C": round(cpu_temp, 1),
        "predicted_gpu_temp_C": round(gpu_temp, 1),
        "cpu_thermal_state": classify_thermal(cpu_temp),
        "gpu_thermal_state": classify_thermal(gpu_temp),
        "is_mutual_heating_active": cooler.get("cooler_type", "air") == "air"
                                     and gpu_effective_w > GPU_MUTUAL_HEATING_THRESHOLD_W,
    }


if __name__ == "__main__":
    data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(sys.stdin)
    print(json.dumps(evaluate(data), ensure_ascii=False, indent=2))
