---
id: "nvidia-rtx-5060-ti"
type: "gpu"
title: "NVIDIA GeForce RTX 5060 Ti 16GB"
vendor: "nvidia"
status: "verified"
tags: ["blackwell", "rtx-50-series", "128-bit", "16gb-vram", "gddr7", "180w", "pcie-5.0"]
last_updated: "2026-06-19"
links:
  smaller_brother: "catalog/gpu/nvidia-rtx-5060.md"
  competitor_amd: "catalog/gpu/amd-rx-9060-xt.md"
  predecessor: "catalog/gpu/nvidia-rtx-4060-ti.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "GB206 (Blackwell)"
  lithography: "TSMC 4N (5nm)"
  cuda_cores: 4608
  boost_clock: "2.57 GHz"
  vram: "16 GB GDDR7 (128-bit)"
  vram_bandwidth: "448 GB/s"
  tbp: "180W"
  power_connector: "1× 8-pin (AIB) / 12V-2×6 опционально"
  pcie: "PCIe 5.0 x8"
  display_outputs: "3× DP 2.1b, 1× HDMI 2.1b"
  msrp_usd: "$429"
  msrp_8gb: "$379"
engineering_notes: "GB206 — полноценный чип Blackwell для 60-класса (4608 CUDA — все SM активны). GDDR7 28 Gbps на 128-битной шине даёт 448 GB/s — прирост 55.6% над RTX 4060 Ti (288 GB/s GDDR6) при той же ширине шины. Рост TBP до 180W (+20W vs 4060 Ti) обусловлен переходом GDDR7 и 4608 ядер. PCIe 5.0 x8 эквивалентен по пропускной способности PCIe 4.0 x16 (~32 GT/s) — на платах с PCIe 3.0 потеря до 5%. 12V-2×6 опционален: большинство AIB используют классический 8-pin. DP 2.1b поддерживает UHBR13.5 (54 Gbps на линию) — до 4K 480Hz с DSC."
profiles:
  balanced_performance_gpu:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Предсказуемое масштабирование производительности. Стандартные сборки ATX с БП 600-750W. Не требует специального охлаждения или инфраструктуры."
    failure_mode_desc: "Отсутствие специализации. Проигрывает enthusiast-картам в 4K, проигрывает low-power картам в SFF/тишине."
    optimal_for_intents: ["aaa_1440p_high", "aaa_1080p_ultra", "esports_1080p_240hz", "software_development", "streaming"]
    failure_for_intents: ["aaa_4k_path_tracing"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  bandwidth_constrained_vram_rich:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Локальный инференс LLM (7B-13B Q4_K_M). Карта позволяет загрузить модель полностью в VRAM без offload."
    failure_mode_desc: "Нативный 4K-гейминг на ультра. Узкая 128-bit шина становится bottleneck."
    optimal_for_intents: ["llm_inference_7b", "llm_inference_13b"]
    failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu"]
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
  hardware_rt_accelerated_gen_3:
    steel_man_desc: "Path Tracing в реальном времени. Аппаратное ускорение x4-5 vs растеризация."
    failure_mode_desc: "DX11/OpenGL игры. RT-блоки простаивают - dark silicon."
    optimal_for_intents: ["aaa_4k_path_tracing", "3d_rendering_gpu"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  tensor_matrix_accelerated:
    steel_man_desc: "Локальное обучение/инференс нейросетей, Stable Diffusion, DLSS/XeSS."
    failure_mode_desc: "Традиционные FP32-вычисления. Тензорные блоки простаивают - паразитный нагрев."
    optimal_for_intents: ["llm_inference_7b", "llm_inference_13b", "stable_diffusion", "ai_upscaling", "llm_training_lora"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 43990
  median: 52000
  max: 65640
  source: "price.ru"
  date: "2026-06-19"
observations:
  - id: "obs-001"
    source_id: "ts"
    source_confidence: 0.95
    observation_quality: 0.92
    gpu: "nvidia-rtx-5060-ti"
    game: "Cyberpunk 2077"
    game_version: "2.2 (Apr 2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 79
    p1_fps: 0
  - id: "obs-002"
    source_id: "kg"
    source_confidence: 0.95
    observation_quality: 0.90
    gpu: "nvidia-rtx-5060-ti"
    game: "Alan Wake 2"
    game_version: "1.2.x (Nov 2025)"
    config:
      resolution: "1920x1080"
      preset: "High"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 61
    p1_fps: 0
  - id: "obs-003"
    source_id: "kg"
    source_confidence: 0.95
    observation_quality: 0.90
    gpu: "nvidia-rtx-5060-ti"
    game: "Alan Wake 2"
    game_version: "1.2.x (Nov 2025)"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 43
    p1_fps: 0
  - id: "obs-004"
    source_id: "alk"
    source_confidence: 0.75
    observation_quality: 0.70
    gpu: "nvidia-rtx-5060-ti"
    game: "Black Myth: Wukong"
    game_version: "benchmark tool (2025)"
    config:
      resolution: "2560x1440"
      preset: "Cinematic"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 53
    p1_fps: 46
  - id: "obs-005"
    source_id: "ez"
    source_confidence: 0.70
    observation_quality: 0.65
    gpu: "nvidia-rtx-5060-ti"
    game: "Hogwarts Legacy"
    game_version: "2026 build"
    config:
      resolution: "1920x1080"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 120
    p1_fps: 90
  - id: "obs-006"
    source_id: "gn"
    source_confidence: 0.95
    observation_quality: 0.90
    gpu: "nvidia-rtx-5060-ti"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.x (Apr 2025)"
    config:
      resolution: "1920x1080"
      preset: "Ultra"
      rt: "Medium"
      upscaler: "None"
      framegen: false
    avg_fps: 63
    p1_fps: 0
  - id: "obs-007"
    source_id: "gn"
    source_confidence: 0.95
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060-ti"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.x (Apr 2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Medium"
      upscaler: "None"
      framegen: false
    avg_fps: 62
    p1_fps: 0
  - id: "obs-008"
    source_id: "ts"
    source_confidence: 0.95
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060-ti"
    game: "Cyberpunk 2077"
    game_version: "2.2 (Apr 2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Medium"
      upscaler: "None"
      framegen: false
    avg_fps: 62
    p1_fps: 0
    vram_usage: 10.3
    stutter_events: "no"
    notes: "16GB model; VRAM usage measured via GPU-Z during benchmark run; well within 16GB buffer — no stutter or texture streaming issues observed"
  - id: "obs-009"
    source_id: "ts"
    source_confidence: 0.95
    observation_quality: 0.88
    gpu: "nvidia-rtx-5060-ti-8gb"
    game: "Cyberpunk 2077"
    game_version: "2.2 (Apr 2025)"
    config:
      resolution: "2560x1440"
      preset: "Medium"
      rt: "Medium"
      upscaler: "None"
      framegen: false
    avg_fps: 0
    p1_fps: 0
    vram_usage: 7.9
    stutter_events: "yes"
    notes: "8GB model; VRAM capped at ~7.9 GB (hardware limit); TechSpot described the experience as 'an unplayable stuttering mess' with severe frametime spikes; the 16GB model was 62% faster in the same configuration"
  - id: "obs-010"
    source_id: "ts"
    source_confidence: 0.95
    observation_quality: 0.92
    gpu: "nvidia-rtx-5060-ti"
    game: "Cyberpunk 2077"
    game_version: "2.2 (Apr 2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 79
    p1_fps: 0
    notes: "Native raster baseline for DLSS/MFG scaling comparison"
  - id: "obs-011"
    source_id: "tt"
    source_confidence: 0.85
    observation_quality: 0.82
    gpu: "nvidia-rtx-5060-ti"
    game: "Cyberpunk 2077"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "DLSS Quality"
      framegen: false
    avg_fps: 118
    p1_fps: 0
    notes: "DLSS 4 Transformer model (Preset K); ~49% uplift over native 79 fps"
  - id: "obs-012"
    source_id: "tt"
    source_confidence: 0.85
    observation_quality: 0.82
    gpu: "nvidia-rtx-5060-ti"
    game: "Cyberpunk 2077"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "DLSS Quality"
      framegen: true
    avg_fps: 205
    p1_fps: 0
    notes: "DLSS 4 Quality + MFG 4x; ~2.6x multiplier over native 79 fps; latency increase from ~35ms to ~55ms per independent testing"
---

# NVIDIA GeForce RTX 5060 Ti

## Архитектура и позиционирование

RTX 5060 Ti — видеокарта среднего сегмента на архитектуре **Blackwell**, выпущенная 16 апреля 2025 года. Базируется на полноценном GPU **GB206** без отключения вычислительных блоков: все 4608 CUDA-ядер активны. Производится по техпроцессу **TSMC 4N** (оптимизированный 5-нм класс), общему для всей линейки RTX 50 [^fact-1] [^fact-2].

**Позиционирование:** между RTX 5060 (GB206-250-A1, 3840 CUDA) и RTX 5070 (GB205, 6144 CUDA). Доступна в двух вариантах: 16 GB ($429 MSRP) и 8 GB ($379 MSRP). Разница в $50 между 8GB и 16GB-версиями — вдвое меньше, чем у предшественника RTX 4060 Ti ($100) [^fact-3] [^fact-4].

**Ключевое изменение поколения:** переход с GDDR6 (288 GB/s на RTX 4060 Ti) на GDDR7 28 Gbps (448 GB/s) при той же ширине шины 128-bit — прирост bandwidth 55.6% [^fact-5].

## Характеристики

| Параметр | Значение |
|---|---|
| GPU | GB206 (Blackwell) [^fact-1] |
| Техпроцесс | TSMC 4N (5nm) [^fact-2] |
| CUDA-ядер | 4608 [^fact-1] |
| Boost Clock | 2.57 GHz (2572 MHz) [^fact-1] |
| VRAM | 16 GB GDDR7 (128-bit); также 8 GB вариант [^fact-1] [^fact-4] |
| Пропускная способность | 448 GB/s (28 Gbps × 128-bit / 8) [^fact-5] |
| TBP | 180W [^fact-1] [^fact-2] |
| Разъём питания | 1× 8-pin (стандарт AIB); 12V-2×6 опционально [^fact-6] |
| PCIe | PCIe 5.0 x8 (физический слот x16) [^fact-7] |
| Видеовыходы | 3× DisplayPort 2.1b, 1× HDMI 2.1b [^fact-6] |
| MSRP (16GB) | $429 [^fact-3] |
| MSRP (8GB) | $379 [^fact-3] |

## Performance Data — Raster

| Игра | Config | avg_fps | p1_fps | Источник |
|---|---|---|---|---|
| Cyberpunk 2077 | 1440p Ultra, RT Off, Native | 79 | — | TechSpot [^obs-1] |
| Alan Wake 2 | 1080p High, RT Off, Native | 61 | — | KitGuru [^obs-2] |
| Alan Wake 2 | 1440p High, RT Off, Native | 43 | — | KitGuru [^obs-2] |
| Black Myth: Wukong | 1440p Cinematic, RT Off, Native | 53 | 46 | ALKtech [^obs-3] |
| Hogwarts Legacy | 1080p Ultra, RT Off, Native | ~120 | ~90 | EVEzone [^obs-4] |

## Performance Data — RT

| Игра | Config | avg_fps | p1_fps | Источник |
|---|---|---|---|---|
| Cyberpunk 2077: Phantom Liberty | 1080p Ultra, RT Medium, Native | 63 | — | Gamers Nexus [^obs-6] |
| Cyberpunk 2077: Phantom Liberty | 1440p Ultra, RT Medium, Native | 62 | — | Gamers Nexus [^obs-7] |

## Performance Data — VRAM Pressure

| Игра | GPU Variant | Config | avg_fps | VRAM Usage | Stutter | Источник |
|---|---|---|---|---|---|---|
| Cyberpunk 2077 | 16GB | 1440p Ultra, RT Medium, Native | 62 | 10.3 GB | No | TechSpot [^obs-8] |
| Cyberpunk 2077 | 8GB | 1440p Medium, RT Medium, Native | — | 7.9 GB (capped) | Yes | TechSpot [^obs-9] |

## Performance Data — DLSS/MFG Scaling

| Игра | Config | avg_fps | Множитель vs Native | Источник |
|---|---|---|---|---|
| Cyberpunk 2077 | 1440p Ultra, Native | 79 | 1.0× (baseline) | TechSpot [^obs-10] |
| Cyberpunk 2077 | 1440p Ultra, DLSS Quality, FG Off | 118 | ~1.5× | TweakTown [^obs-11] |
| Cyberpunk 2077 | 1440p Ultra, DLSS Quality, MFG 4x | 205 | ~2.6× | TweakTown [^obs-12] |

## Сравнение

| Параметр | RTX 5060 Ti 16GB | RTX 4060 Ti 16GB | RTX 5060 8GB |
|---|---|---|---|
| GPU | GB206 (Blackwell) | AD106 (Ada Lovelace) | GB206-250 (Blackwell) |
| CUDA-ядер | 4608 | 4352 | 3840 |
| VRAM | 16 GB GDDR7 | 16 GB GDDR6 | 8 GB GDDR7 |
| Шина | 128-bit | 128-bit | 128-bit |
| Bandwidth | 448 GB/s | 288 GB/s | 448 GB/s |
| TBP | 180W | 165W | 145W |
| PCIe | 5.0 x8 | 4.0 x8 | 5.0 x8 |
| MSRP | $429 | $499 | $299 |

## Epistemic Notes

[^fact-1]: TechPowerUp GPU Database — NVIDIA GeForce RTX 5060 Ti 8 GB (c4246) и 16 GB (c4292): GB206, 4608 CUDA, 2407/2572 MHz, 128-bit GDDR7. https://www.techpowerup.com/gpu-specs/geforce-rtx-5060-ti-8-gb.c4246

[^fact-2]: Notebookcheck Tech — GeForce RTX 5060 Ti Benchmarks and Specs: GB206, TSMC 4N FinFET (5nm), 180W TGP. https://www.notebookcheck.net/Nvidia-GeForce-RTX-5060-Ti-Benchmarks-and-Specs.935681.0.html

[^fact-3]: Wikipedia — GeForce RTX 50 series: MSRP $379 (8GB) / $429 (16GB), $50 difference vs $100 for 4060 Ti. https://en.wikipedia.org/wiki/GeForce_RTX_50_series

[^fact-4]: NVIDIA Official — GeForce RTX 5060 Family: 8GB/16GB GDDR7, Blackwell architecture. https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5060-family/

[^fact-5]: Guru3D — MSI RTX 5060 Ti TRIO OC review: 128-bit, 28 Gbps GDDR7 → 448 GB/s bandwidth. PCGamesN — RTX 5060 Ti review: memory bandwidth increase from 288 to 448 GB/s. https://www.guru3d.com/review/msi-geforce-rtx-5060-ti-trio-oc-review/

[^fact-6]: PNY product listing (Newegg) — RTX 5060 Ti: 1× 8-pin power, 3× DP 2.1b, 1× HDMI 2.1b, PCIe 5.0 x8. Reddit r/hardware RTX 5060 Ti roundup — 12V-2×6 on select models. https://www.reddit.com/r/hardware/comments/1k1e6b1/rtx_5060_ti_roundup_5_models_tested_compared/

[^fact-7]: TechPowerUp — NVIDIA GeForce RTX 5060 Ti PCI-Express x8 Scaling: PCIe 5.0 x8 interface. https://www.techpowerup.com/review/nvidia-geforce-rtx-5060-ti-pci-express-x8-scaling/3.html

[^obs-1]: TechSpot — Nvidia GeForce RTX 5060 Ti 16GB Review (Apr 2025): Cyberpunk 2077, 1440p Ultra, 79 fps avg, matching RTX 4070 and RX 7700 XT. https://www.techspot.com/review/2979-nvidia-geforce-rtx-5060-ti-16gb/

[^obs-2]: KitGuru — Nvidia RTX 5060 Ti 16GB Review (Nov 2025): Alan Wake 2, 1080p: 61 fps avg (17% faster than 4060 Ti 16GB), 1440p: 43 fps avg. https://www.kitguru.net/components/graphic-cards/dominic-moass/nvidia-rtx-5060-ti-16gb-review-ft-gigabyte-palit/all/1/

[^obs-3]: ALKtech — MSI GeForce RTX 5060 Ti 16G GAMING TRIO OC Review: Black Myth Wukong Benchmark Tool, 53 avg / 46 min / 60 max fps (1440p). https://www.alktech.co/articles/review-msi-geforce-rtx-5060-ti-16g-gaming-trio-oc

[^obs-4]: EVEzone — RTX 5060 Ti Hogwarts Legacy FPS Performance Benchmark (May 2026): 1080p Ultra, above 120 fps avg, 1% lows above 90 fps. https://evezone.evetech.co.za/performance-pulse/rtx-5060-ti-hogwarts-legacy-fps-performance-benchmark-best-settings/

[^obs-6]: Gamers Nexus — NVIDIA GeForce RTX 5060 Ti Review & Benchmarks (Apr 2025): Cyberpunk 2077 Phantom Liberty, 1080p RT Medium, 63 FPS AVG, between 7900 GRE and 7900 XT. https://gamersnexus.net/gpus/more-marketing-bs-nvidia-geforce-rtx-5060-ti-review-benchmarks-vs-gtx-1060-4060-ti-more

[^obs-7]: Gamers Nexus — NVIDIA GeForce RTX 5060 Ti Review & Benchmarks (Apr 2025): Cyberpunk 2077 Phantom Liberty, 1440p with RT, 62 FPS AVG, consistent frametimes. https://gamersnexus.net/gpus/more-marketing-bs-nvidia-geforce-rtx-5060-ti-review-benchmarks-vs-gtx-1060-4060-ti-more

[^obs-8]: TechSpot — Nvidia GeForce RTX 5060 Ti 16GB Review (Apr 2025): Cyberpunk 2077 1440p Ultra RT Medium, VRAM usage ~10.3 GB (within 16GB buffer), no stutter observed. https://www.techspot.com/review/2979-nvidia-geforce-rtx-5060-ti-16gb/

[^obs-9]: TechSpot — Instantly Obsolete: Nvidia RTX 5060 Ti 8GB Review (Apr 2025): Cyberpunk 2077 1440p Native Medium RT Medium, VRAM capped at ~7.9 GB, 'unplayable stuttering mess', 16GB model 62% faster. https://www.techspot.com/review/2980-nvidia-geforce-rtx-5060-ti-8gb/

[^obs-10]: TechSpot — Nvidia GeForce RTX 5060 Ti 16GB Review (Apr 2025): Cyberpunk 2077, 1440p Ultra, 79 fps avg native (baseline for DLSS/MFG scaling). https://www.techspot.com/review/2979-nvidia-geforce-rtx-5060-ti-16gb/

[^obs-11]: TweakTown — MSI GeForce RTX 5060 Ti Ventus 2X 16GB Review (Apr 2025): Cyberpunk 2077 1440p Ultra, DLSS 4 Quality (Transformer, no FG), ~118 FPS (~1.5x native). https://www.tweaktown.com/reviews/11029/msi-geforce-rtx-5060-ti-ventus-2x-16gb-dlss-4-goes-mainstream/index.html

[^obs-12]: TweakTown — MSI GeForce RTX 5060 Ti Ventus 2X 16GB Review (Apr 2025): Cyberpunk 2077 1440p Ultra, DLSS 4 Quality + MFG 4x, ~205 FPS (~2.6x native), latency 55ms. https://www.tweaktown.com/reviews/11029/msi-geforce-rtx-5060-ti-ventus-2x-16gb-dlss-4-goes-mainstream/index.html
