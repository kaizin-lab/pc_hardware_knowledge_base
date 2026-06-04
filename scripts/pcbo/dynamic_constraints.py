"""
Dynamic Constraints Engine — STATE_0.7 пайплайна PCBO.

Параметризует абстрактные интенты под конкретные resolution/settings/target_fps.
Все числа — из YAML-конфига интента. Python-функции — blind executors.

Использование:
    from dynamic_constraints import evaluate_dynamic_constraints
    result = evaluate_dynamic_constraints(intent_yaml_path, params)

    params = {
        "resolution": "1440p",
        "settings": "ultra",
        "target_fps": 60
    }

    result = {
        "resolved_mandatory_profiles": ["balanced_performance_gpu"],
        "resolved_block_profiles": ["bandwidth_constrained_vram_rich"],  # если 1440p ultra
        "resolved_warn_profiles": [],
        "min_vram_gb": 14,          # 12 + 2 (ultra)
        "maut_weights": {...},
        "noise_load": "A2",
        "thermal_state": "T_Safe",
        "effective_params": {...}    # что было применено
    }
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


def evaluate_dynamic_constraints(
    intent_path: str,
    params: dict
) -> dict:
    """
    Главная точка входа. Берёт путь к YAML-файлу абстрактного интента и
    параметры (resolution, settings, target_fps) — возвращает конкретные
    профили и constraints для этого разрешения.

    Args:
        intent_path: путь к YAML-файлу интента (например,
                     'catalog/intents/aaa_gaming_base.yaml')
        params: {
            "resolution": "1080p"|"1440p"|"4K",
            "settings": "medium"|"high"|"ultra"|"path_tracing",
            "target_fps": 60|120|240  (опционально, default=60)
        }

    Returns:
        dict с resolved_mandatory_profiles, resolved_block_profiles,
        min_vram_gb, maut_weights, noise_load, thermal_state
    """
    # Загрузить YAML
    base_dir = Path(__file__).parent.parent.parent  # scripts/pcbo/ → scripts/ → корень KB
    full_path = base_dir / intent_path

    with open(full_path) as f:
        intent = yaml.safe_load(f)

    dynamic = intent.get("dynamic_constraints", {})
    if not dynamic:
        # Не абстрактный интент — вернуть как есть
        return _static_fallback(intent)

    resolution = params.get("resolution", "1080p")
    settings = params.get("settings", "high")
    target_fps = params.get("target_fps", 60)

    # 1. Вычислить минимальный VRAM
    min_vram = _evaluate_vram(dynamic, resolution, settings)

    # 2. Определить профиль GPU
    gpu_profile_ref = _evaluate_gpu_profile(dynamic, resolution, target_fps)

    # 3. Скорректировать MAUT-веса
    maut_result = _adjust_maut(dynamic, resolution)

    # 4. Определить BLOCK/WARN для bandwidth_constrained_vram_rich
    bandwidth_block = _evaluate_bandwidth_block(dynamic, resolution, settings)

    # 5. Собрать статические block (из profile_interaction_matrix)
    profile_matrix = intent.get("profile_interaction_matrix", {})

    # mandatory: пустой в абстрактном интенте — заполняем из dynamic
    resolved_mandatory = [gpu_profile_ref] if gpu_profile_ref else []

    # block: статические (sub_75w — всегда) + динамические (bandwidth на высоких)
    static_block = [b["profile"] for b in profile_matrix.get("strict_block", [])]

    # sub_75w_slot_powered — всегда BLOCK. bandwidth_constrained — динамически.
    resolved_block = [
        p for p in static_block
        if "bandwidth_constrained" not in p  # bandwidth — отдельно
    ]
    if bandwidth_block == "BLOCK":
        resolved_block.append("concepts/epistemological-profiles.md#bandwidth_constrained_vram_rich")

    # warn: bandwidth на низких разрешениях
    resolved_warn = []
    if bandwidth_block == "WARN":
        resolved_warn.append("concepts/epistemological-profiles.md#bandwidth_constrained_vram_rich")
    # Добавить статические warn (кроме bandwidth если он уже в BLOCK)
    static_warn = [w["profile"] for w in profile_matrix.get("warn", [])]
    for pw in static_warn:
        if pw not in resolved_warn and pw not in resolved_block:
            resolved_warn.append(pw)
    if bandwidth_block == "BLOCK":
        # Удалить bandwidth из warn если он в block
        resolved_warn = [w for w in resolved_warn if "bandwidth_constrained" not in w]

    return {
        "resolved_mandatory_profiles": resolved_mandatory,
        "resolved_block_profiles": resolved_block,
        "resolved_warn_profiles": resolved_warn,
        "min_vram_gb": min_vram,
        "maut_weights": maut_result["maut_weights"],
        "noise_load": maut_result.get("noise_load", "A2"),
        "thermal_state": maut_result.get("thermal_state", "T_Safe"),
        "effective_params": {
            "resolution": resolution,
            "settings": settings,
            "target_fps": target_fps,
            "gpu_profile": gpu_profile_ref,
            "bandwidth_rule": bandwidth_block,
        }
    }


def _evaluate_vram(dynamic: dict, resolution: str, settings: str) -> int:
    """Вычислить минимальный VRAM. Все числа из конфига."""
    vram_cfg = dynamic.get("vram_minimum_gb", {}).get("config", {})
    base = vram_cfg.get("base", {}).get(resolution, 8)
    modifier = vram_cfg.get("modifiers", {}).get(settings, 0)
    return base + modifier


def _evaluate_gpu_profile(dynamic: dict, resolution: str, target_fps: int) -> str:
    """Определить mandatory GPU-профиль. Конфиг из YAML."""
    gpu_cfg = dynamic.get("target_gpu_profile", {}).get("config", {})

    # Сначала точное совпадение: "1080p_60fps"
    exact_key = f"{resolution}_{target_fps}fps"
    if exact_key in gpu_cfg and not exact_key.endswith("_note"):
        return gpu_cfg[exact_key]

    # Ближайший FPS: ищем ключ с тем же разрешением
    candidates = []
    for key, val in gpu_cfg.items():
        if key.endswith("_note"):
            continue
        if key.startswith(resolution):
            try:
                key_fps = int(key.split("_")[-1].replace("fps", ""))
                candidates.append((key_fps, val))
            except (ValueError, IndexError):
                continue

    if not candidates:
        # Fallback: самый низкий профиль
        return gpu_cfg.get("1080p_60fps",
            "concepts/epistemological-profiles.md#mainstream_efficiency_gpu")

    # Выбрать ближайший ≥ target_fps
    candidates.sort()
    for fps, profile in candidates:
        if fps >= target_fps:
            return profile

    # Если target_fps выше всех — вернуть максимальный
    return candidates[-1][1]


def _adjust_maut(dynamic: dict, resolution: str) -> dict:
    """Скорректировать MAUT-веса под разрешение. Числа из конфига."""
    maut_cfg = dynamic.get("maut_weights", {}).get("config", {})
    res_cfg = maut_cfg.get(resolution, maut_cfg.get("1080p", {}))

    return {
        "maut_weights": {
            "cpu_weight": res_cfg.get("cpu_weight", 0.4),
            "gpu_weight": res_cfg.get("gpu_weight", 0.6),
        },
        "noise_load": res_cfg.get("noise_load", "A2"),
        "thermal_state": res_cfg.get("thermal_state", "T_Safe"),
    }


def _evaluate_bandwidth_block(dynamic: dict, resolution: str, settings: str) -> str:
    """
    Определить, является ли 128-bit шина BLOCK или WARN
    для данного разрешения и настроек.
    """
    bw_cfg = dynamic.get("bandwidth_block_rule", {}).get("config", {})

    scenario = f"{resolution}_{settings}"

    block_at = bw_cfg.get("block_at", [])
    if scenario in block_at:
        return "BLOCK"

    warn_at = bw_cfg.get("warn_at", [])
    if scenario in warn_at:
        return "WARN"

    # Если сценарий не описан явно — безопасное предположение
    # На 4K и 1440p с высокими настройками → BLOCK
    if resolution == "4K" and settings in ("high", "ultra", "path_tracing"):
        return "BLOCK"
    if resolution == "1440p" and settings in ("ultra", "path_tracing"):
        return "BLOCK"

    return "WARN"


def _static_fallback(intent: dict) -> dict:
    """Fallback для неабстрактных интентов."""
    matrix = intent.get("profile_interaction_matrix", {})
    return {
        "resolved_mandatory_profiles": [
            m["profile"] for m in matrix.get("mandatory_steel_man", [])
        ],
        "resolved_block_profiles": [
            b["profile"] for b in matrix.get("strict_block", [])
        ],
        "resolved_warn_profiles": [
            w["profile"] for w in matrix.get("warn", [])
        ],
        "min_vram_gb": 0,
        "maut_weights": {},
        "noise_load": "A2",
        "thermal_state": "T_Safe",
        "effective_params": {"note": "static intent — no dynamic resolution"},
    }


# --- Self-test ---
if __name__ == "__main__":
    import sys

    intent_file = sys.argv[1] if len(sys.argv) > 1 else "catalog/intents/aaa_gaming_base.yaml"

    test_cases = [
        {"resolution": "1080p", "settings": "high", "target_fps": 60,
         "desc": "Cyberpunk 1080p high 60fps"},
        {"resolution": "1080p", "settings": "ultra", "target_fps": 120,
         "desc": "Cyberpunk 1080p ultra 120fps"},
        {"resolution": "1440p", "settings": "high", "target_fps": 60,
         "desc": "Cyberpunk 1440p high 60fps"},
        {"resolution": "1440p", "settings": "ultra", "target_fps": 60,
         "desc": "Cyberpunk 1440p ultra 60fps"},
        {"resolution": "4K", "settings": "high", "target_fps": 60,
         "desc": "Cyberpunk 4K high 60fps"},
        {"resolution": "4K", "settings": "ultra", "target_fps": 60,
         "desc": "Cyberpunk 4K ultra 60fps"},
        {"resolution": "4K", "settings": "path_tracing", "target_fps": 60,
         "desc": "Cyberpunk 4K path tracing 60fps"},
    ]

    for tc in test_cases:
        result = evaluate_dynamic_constraints(intent_file, {
            "resolution": tc["resolution"],
            "settings": tc["settings"],
            "target_fps": tc["target_fps"],
        })
        print(f"\n{'='*60}")
        print(f"  {tc['desc']}")
        print(f"  {'='*60}")
        print(f"  VRAM min:      {result['min_vram_gb']} GB")
        print(f"  GPU profile:   {result['resolved_mandatory_profiles']}")
        print(f"  BLOCK:         {result['resolved_block_profiles']}")
        print(f"  WARN:          {result['resolved_warn_profiles']}")
        print(f"  MAUT CPU/GPU:  {result['maut_weights']}")
        print(f"  Noise/Thermal: {result['noise_load']} / {result['thermal_state']}")
        bw = result['effective_params']['bandwidth_rule']
        if bw != "WARN":
            print(f"  ⚠️  Bandwidth:  {bw}")
