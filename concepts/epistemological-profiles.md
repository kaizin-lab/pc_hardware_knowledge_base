---
id: "epistemological-profiles"
type: "concept"
title: "PCBO Epistemological Profiles Dictionary v3.2"
status: "draft"
last_updated: "2026-06-03"
---

# PCBO Epistemological Profiles Dictionary v3.2

Переход от бинарных тегов к поведенческим профилям. Каждый профиль = трёхфазная
микро-симуляция поведения компонента: критерии входа → optimal сценарий → failure mode.

## Схема профиля (YAML Schema v3.2)

```yaml
profiles:
  profile_name:
    criteria_met: true|false  # per-component, заполняется при аудите
    # --- LLM layer (prose) ---
    steel_man_desc: "Оптимальный сценарий применения"
    failure_mode_desc: "При каких условиях компонент терпит крах"
    # --- Python layer (deterministic) ---
    optimal_for_intents: ["intent_a", "intent_b"]     # O(1) set intersection
    failure_for_intents: ["intent_x", "intent_y"]
    failure_severity: "WARN"|"BLOCK"                  # BLOCK = жёсткая несовместимость
```

---

## Контролируемый словарь интентов (Intents Vocabulary)

### Гейминг
| Intent ID | Описание |
|---|---|
| `esports_1080p_240hz` | Киберспорт: CS2, Valorant, 240Hz+, низкие настройки |
| `esports_1080p_360hz` | Киберспорт: 360Hz+, минимизация frametime |
| `aaa_1080p_ultra` | AAA-игры, 1080p, ультра-настройки |
| `aaa_1440p_high` | AAA-игры, 1440p, высокие/ультра |
| `aaa_4k_ultra` | AAA-игры, 4K, ультра, без RT |
| `aaa_4k_path_tracing` | AAA-игры, 4K, Path Tracing |

### AI / ML
| Intent ID | Описание |
|---|---|
| `llm_inference_7b` | Локальный инференс LLM 7B (Q4_K_M) |
| `llm_inference_13b` | Локальный инференс LLM 13B (Q4_K_M) |
| `llm_inference_20b` | Локальный инференс LLM 20B+ |
| `llm_training_lora` | Файнтюнинг LoRA (требует ×3 VRAM vs инференс) |
| `stable_diffusion` | Генерация изображений (SD, SDXL, Flux) |
| `ai_upscaling` | DLSS / XeSS / FSR — аппаратный апскейлинг |

### Продуктивность
| Intent ID | Описание |
|---|---|
| `heavy_compilation` | Компиляция крупных проектов (C++, Rust, Go monorepo) |
| `3d_rendering_cpu` | CPU-рендеринг: Blender, Cinema 4D, V-Ray |
| `3d_rendering_gpu` | GPU-рендеринг: Octane, Redshift, Cycles |
| `video_editing_4k` | Видеомонтаж 4K: DaVinci Resolve, Premiere |
| `video_editing_8k` | Видеомонтаж 8K / RAW |
| `scientific_computing` | CFD, FEA, математическое моделирование |
| `data_engineering` | ETL, базы данных, аналитика |
| `software_development` | IDE, Docker, веб-серверы, компиляция мелких проектов |
| `office_productivity` | Офис: браузер, документы, почта |

### Операционные
| Intent ID | Описание |
|---|---|
| `silent_build` | Бесшумная работа: <30 dBA под нагрузкой |
| `sff_build` | Компактная сборка: ITX, длина GPU ≤260мм, высота ≤2.2 слота |
| `home_server_24_7` | Сервер 24/7: низкий idle power, стабильность |
| `streaming` | Стриминг: OBS, NVENC, аппаратное кодирование |
| `virtualization` | Виртуализация: Proxmox, ESXi, множество VM |

---

## 1. CPU Profiles

### cache_dominant_gaming
**Физический критерий (L1/L2):** L3-кэш ≥ 64 МБ (3D V-Cache). Снижает L3 cache miss rate на 30–50% в игровых циклах.

```yaml
cache_dominant_gaming:
  steel_man_desc: "Киберспорт 1080p на низких настройках. Минимизация CPU frame time — 1% Low FPS стабильно выше частоты монитора (240/360 Hz)."
  failure_mode_desc: "Тяжёлые многопоточные FP32/AVX-512 вычисления: 3D-рендеринг, компиляция. Тепловое сопротивление bonding layer 3D-кэша снижает тактовую частоту на 300–500 МГц. Производительность на 15–20% ниже при равной стоимости."
  optimal_for_intents: ["esports_1080p_240hz", "esports_1080p_360hz"]
  failure_for_intents: ["3d_rendering_cpu", "heavy_compilation", "scientific_computing"]
  failure_severity: "WARN"
```

### monolithic_low_latency
**Физический критерий (L1/L2):** Все ядра на едином кристалле (1 CCD / unified compute tile). Межъядерная задержка (inter-core latency) ≤ 30 нс.

```yaml
monolithic_low_latency:
  steel_man_desc: "Смешанные интерактивные нагрузки, чувствительные к задержкам: веб-сёрфинг, игры с одним тяжёлым потоком, компиляция мелких файлов. Отзывчивый UI."
  failure_mode_desc: "Параллельные вычисления с массивным рендерингом. Физический предел площади кристалла ограничивает число ядер до 8–10. Проигрывает multi-CCD системам по удельной стоимости ядра."
  optimal_for_intents: ["software_development", "office_productivity", "aaa_1080p_ultra", "aaa_1440p_high"]
  failure_for_intents: ["3d_rendering_cpu", "scientific_computing", "virtualization"]
  failure_severity: "WARN"
```

### multi_ccd_disaggregated
**Физический критерий (L1/L2):** ≥ 2 физических кристалла (CCD), соединённых через Infinity Fabric / EMIB. Межкристальная задержка (inter-CCD latency) ≥ 70 нс.

```yaml
multi_ccd_disaggregated:
  steel_man_desc: "Параллельные многопоточные вычисления: 3D-рендеринг, неинтерактивная компиляция больших проектов. 12–16 ядер на потребительской платформе без HEDT-тарифа."
  failure_mode_desc: "Игры и реалтайм-задачи. ОС может перебросить активный поток с CCD0 на CCD1 — межчиплетная задержка 70 нс вызывает frametime spike и микростаттеры."
  optimal_for_intents: ["3d_rendering_cpu", "scientific_computing", "heavy_compilation"]
  failure_for_intents: ["esports_1080p_240hz", "esports_1080p_360hz"]
  failure_severity: "WARN"
```

### dense_thermal_concentration
**Физический критерий (L1/L2):** Плотность теплового потока ≥ 1.5 Вт/мм² + толщина IHS ≥ 1.7 мм (архитектура AM5).

```yaml
dense_thermal_concentration:
  steel_man_desc: "Импульсные однопоточные нагрузки (burst): открытие страниц, компиляция скриптов. CPU сбрасывает частоту до того как тепло преодолеет сопротивление IHS — максимальный буст на 2–3 секунды."
  failure_mode_desc: "Длительная нагрузка (рендеринг, компиляция). Тепловое сопротивление IHS ограничивает теплоотвод — температура мгновенно достигает 89–95°C даже под СЖО 360мм. Thermal throttling на 5–8%."
  optimal_for_intents: ["office_productivity", "software_development"]
  failure_for_intents: ["3d_rendering_cpu", "scientific_computing", "heavy_compilation"]
  failure_severity: "WARN"
```

### hybrid_asymmetric_efficiency
**Физический критерий (L1/L2):** Гетерогенная архитектура: P-ядра (высокий IPC, SMT) + E-ядра (малая площадь, низкое энергопотребление).

```yaml
hybrid_asymmetric_efficiency:
  steel_man_desc: "Стриминг игр и тяжёлая фоновая многозадачность. OBS/Discord/антивирус — на E-ядрах, игра/рендер — на P-ядрах. Стабильный frametime."
  failure_mode_desc: "Среды без аппаратного планировщика (старые версии Windows, Linux без Intel Thread Director). Софт с жёсткой привязкой потоков может ошибочно назначать realtime-потоки на слабые E-ядра — падение производительности в 2–3×."
  optimal_for_intents: ["streaming", "software_development", "video_editing_4k"]
  failure_for_intents: []  # нет жёстких блокирующих сценариев при современном ПО
  failure_severity: "WARN"
```

### hedt_multi_channel
**Физический критерий (L1/L2):** Контроллер памяти ≥ 4 каналов (BW ≥ 200 ГБ/с), линий PCIe от CPU ≥ 64.

```yaml
hedt_multi_channel:
  steel_man_desc: "ML-станции с 3–4 GPU, серверы виртуализации, научные CFD/FEA-симуляции. Производительность ограничена bandwidth памяти — дополнительные каналы снимают bottleneck."
  failure_mode_desc: "Потребительские малопоточные нагрузки. Высокий idle power (≥ 90 Вт платформа), NUMA-латентность снижает FPS в играх по сравнению с дешёвыми десктопными аналогами."
  optimal_for_intents: ["llm_training_lora", "scientific_computing", "virtualization", "llm_inference_20b"]
  failure_for_intents: ["esports_1080p_240hz", "esports_1080p_360hz", "office_productivity", "silent_build"]
  failure_severity: "BLOCK"
```

### sub_5nm_lithography
**Физический критерий (L1/L2):** Плотность транзисторов ≥ 130 млн/мм² (TSMC N5/N3). Рабочее напряжение под нагрузкой ≤ 1.2 В.

```yaml
sub_5nm_lithography:
  steel_man_desc: "Компактные ITX-сборки с жёстким лимитом энергопотребления. Максимальная производительность на ватт."
  failure_mode_desc: "Повышенная чувствительность к деградации кремния при статическом напряжении. Разгон с V > 1.35 В вызывает ускоренную электромиграцию и необратимый выход из строя — быстрее чем на 7nm/14nm."
  optimal_for_intents: ["sff_build", "silent_build"]
  failure_for_intents: []  # информационный профиль
  failure_severity: "WARN"
```

---

## 2. GPU Profiles

### bandwidth_constrained_vram_rich
**Физический критерий (L1/L2):** VRAM ≥ 16 ГБ при ширине шины ≤ 128-bit, BW ≤ 300 ГБ/с (для GDDR6).

```yaml
bandwidth_constrained_vram_rich:
  steel_man_desc: "Локальный инференс LLM (7B–13B Q4_K_M). Карта позволяет загрузить модель полностью в VRAM без offload в системную RAM. Интерактивная скорость > 30 t/s."
  failure_mode_desc: "Нативный 4K-гейминг на ультра-настройках. Узкая 128-bit шина становится bottleneck: fillrate падает, texture pop-in, фризы — даже при заполнении VRAM наполовину."
  optimal_for_intents: ["llm_inference_7b", "llm_inference_13b"]
  failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu"]
  failure_severity: "BLOCK"
```

### transient_spike_heavy
**Физический критерий (L1/L2):** Скачки тока (≤ 10 мс) ≥ 150% от номинального TGP.

```yaml
transient_spike_heavy:
  steel_man_desc: "Динамичный 3D-рендеринг и гейминг с резким изменением сложности сцены. Мгновенный переход в максимальное P-state позволяет избежать микрофризов."
  failure_mode_desc: "Блоки питания ATX 2.4 (без ATX 3.0). Микросекундный скачок тока триггерит OCP/OPP защиту — внезапное аварийное выключение (чёрный экран) под нагрузкой."
  optimal_for_intents: ["aaa_1440p_high", "aaa_4k_ultra", "3d_rendering_gpu"]
  failure_for_intents: ["sff_build"]  # SFF-БП часто не имеют запаса под пики
  failure_severity: "BLOCK"
```

### hbm_stacked_bus
**Физический критерий (L1/L2):** Память HBM2/HBM3 на интерпозере, ширина шины ≥ 2048-bit, пропускная способность ≥ 1 ТБ/с.

```yaml
hbm_stacked_bus:
  steel_man_desc: "Сверхтяжёлые параллельные вычисления: обучение нейросетей, научные задачи. Объём передаваемых данных в секунду важнее объёма памяти."
  failure_mode_desc: "Коммерческий гейминг. Экстремальная стоимость интерпозера + риск термического повреждения (разное тепловое расширение чипа и HBM). Экономически и физически нецелесообразно."
  optimal_for_intents: ["llm_training_lora", "scientific_computing"]
  failure_for_intents: ["aaa_4k_ultra", "esports_1080p_240hz", "office_productivity"]
  failure_severity: "BLOCK"
```

### hardware_rt_accelerated_gen_3
**Физический критерий (L1/L2):** Аппаратные RT-блоки 3-го поколения (BVH traversal).

```yaml
hardware_rt_accelerated_gen_3:
  steel_man_desc: "Path Tracing в реальном времени, архитектурная визуализация (Octane/Cycles). Аппаратное ускорение сокращает время рендера кадра в 4–5× по сравнению с растеризацией."
  failure_mode_desc: "Классические игры на DirectX 11 / OpenGL. RT-блоки простаивают — dark silicon, за который пользователь переплатил, не получая производительности в растровых сценах."
  optimal_for_intents: ["aaa_4k_path_tracing", "3d_rendering_gpu"]
  failure_for_intents: []  # не вредит, просто не используется
  failure_severity: "WARN"
```

### tensor_matrix_accelerated
**Физический критерий (L1/L2):** Тензорные ядра с поддержкой FP16/INT8/FP4 и аппаратной sparsity.

```yaml
tensor_matrix_accelerated:
  steel_man_desc: "Локальное обучение/инференс нейросетей, Stable Diffusion, DLSS/XeSS-апскейлинг. Матричное перемножение на тензорных ядрах в разы быстрее FP32."
  failure_mode_desc: "Традиционные FP32-вычисления без матричной математики. Тензорные блоки не загружены инструкциями — паразитный нагрев кристалла в простое."
  optimal_for_intents: ["llm_inference_7b", "llm_inference_13b", "stable_diffusion", "ai_upscaling", "llm_training_lora"]
  failure_for_intents: []  # не вредит, просто не используется
  failure_severity: "WARN"
```

### main-stream_efficiency_tgp_150w
**Физический критерий (L1/L2):** TGP в диапазоне 100–180 Вт, питание через 1× 8-pin.

```yaml
mainstream_efficiency_tgp_150w:
  steel_man_desc: "Массовые игровые ПК среднего класса: 1080p/1440p. Блоки питания 500–550 Вт. Минимальные требования к вентиляции, низкий шум из коробки."
  failure_mode_desc: "Нативный 4K-гейминг. Недостаток вычислительных блоков (CUDA-ядер/CU) не позволяет выдать 60 FPS даже при полной загрузке — требуется снижение до Medium/Low."
  optimal_for_intents: ["aaa_1080p_ultra", "aaa_1440p_high", "esports_1080p_240hz", "silent_build", "sff_build"]
  failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing"]
  failure_severity: "BLOCK"
```

### enthusiast_unrestricted_tgp_300w
**Физический критерий (L1/L2):** TGP ≥ 280 Вт (пики до 450 Вт). Питание: 12V-2×6 или ≥ 3× 8-pin.

```yaml
enthusiast_unrestricted_tgp_300w:
  steel_man_desc: "Нативный 4K-гейминг на максималках, профессиональный рендеринг, высокопроизводительный AI-инференс."
  failure_mode_desc: "Компактные корпуса с плохой вентиляцией (airflow sound_dampened_restricted). 300–450 Вт тепла быстро нагревают внутренний воздух до 55°C — перегрев CPU и троттлинг всей системы."
  optimal_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu", "llm_inference_20b", "video_editing_8k"]
  failure_for_intents: ["silent_build", "sff_build"]
  failure_severity: "BLOCK"
```

### sub_75w_slot_powered
**Физический критерий (L1/L2):** TGP ≤ 75 Вт, питание только через слот PCIe x16, без разъёмов дополнительного питания.

```yaml
sub_75w_slot_powered:
  steel_man_desc: "Апгрейд брендовых офисных ПК (Dell, HP) с проприетарными БП ≤ 240 Вт без кабелей GPU. Компактные 1U-серверы."
  failure_mode_desc: "Гейминг ≥ 1080p с DX12. Лимит 75 Вт заставляет контроллер сбрасывать частоты GPU до минимума при любой сложной сцене — FPS падает до неиграбельных значений."
  optimal_for_intents: ["office_productivity", "home_server_24_7"]
  failure_for_intents: ["aaa_1080p_ultra", "aaa_1440p_high", "esports_1080p_240hz"]
  failure_severity: "BLOCK"
```

### multi_gpu_interconnect_capable
**Физический критерий (L1/L2):** Физический интерфейс межчиповой связи (NVLink ≥ 112 ГБ/с), объединение VRAM 2+ карт в единый адресный пул.

```yaml
multi_gpu_interconnect_capable:
  steel_man_desc: "Локальное обучение LLM >70B. Объединение памяти 2× RTX 3090 = 48 ГБ VRAM — избегает медленного offload в системное ОЗУ."
  failure_mode_desc: "Потребительский гейминг. SLI/Multi-GPU удалены из современных игровых движков и драйверов. Вторая карта простаивает, перекрывая airflow первой и добавляя 30–45 Вт idle."
  optimal_for_intents: ["llm_training_lora", "llm_inference_20b"]
  failure_for_intents: ["aaa_4k_ultra", "esports_1080p_240hz", "aaa_1440p_high"]
  failure_severity: "BLOCK"
```

---

## 3. Storage Profiles

### dram_less_hmb_cached
**Физический критерий (L1/L2):** Нет физического чипа DRAM на плате SSD. HMB ≤ 64 МБ системной RAM по PCIe DMA + динамический пул pseudo-SLC кэша.

```yaml
dram_less_hmb_cached:
  steel_man_desc: "Клиентская ОС: запуск браузера, загрузка игр. Короткие записи до 20–30 ГБ поглощаются SLC-кэшем — скорости уровня премиум-дисков при цене на 30–40% ниже."
  failure_mode_desc: "Непрерывная многопоточная запись (СУБД, импорт RAW-видео). После исчерпания SLC-кэша контроллер одновременно уплотняет TLC-данные и принимает новый поток. Без DRAM для адресации — задержки до 40 мс, скорость падает до уровня SATA III (≤ 350 МБ/с)."
  optimal_for_intents: ["office_productivity", "software_development", "aaa_1080p_ultra"]
  failure_for_intents: ["video_editing_4k", "video_editing_8k", "data_engineering"]
  failure_severity: "WARN"
```

---

## 4. Motherboard Profiles

### bifurcation_shared_lanes
**Физический критерий (L1/L2):** Пассивные мультиплексоры на плате, перенаправляющие 8 линий PCIe от слота x16 на слоты M.2 NVMe при их заполнении.

```yaml
bifurcation_shared_lanes:
  steel_man_desc: "Высокоплотные дисковые хранилища: 3–4 диска Gen4 NVMe в RAID-0. Скорость дисковой подсистемы важнее bandwidth GPU."
  failure_mode_desc: "Локальные AI-вычисления с RAM offload. Когда модель не влезает в VRAM, падение слота x16 → x8 урезает bandwidth шины с 32 до 16 ГБ/с — скорость инференса падает в 2 раза."
  optimal_for_intents: ["video_editing_4k", "data_engineering", "virtualization"]
  failure_for_intents: ["llm_inference_13b", "llm_inference_20b", "llm_training_lora"]
  failure_severity: "BLOCK"
```

---

## 5. RAM Profiles

### jedec_native_safe
**Физический критерий (L1/L2):** Работа на базовых спецификациях JEDEC (DDR5-4800/5200 при 1.1V, тайминги CL40).

```yaml
jedec_native_safe:
  steel_man_desc: "Серверы баз данных, рабочие станции 24/7 для рендеринга и научного моделирования. Стабильность — приоритет №1. Нулевой уровень soft-bit errors."
  failure_mode_desc: "Киберспорт с целевым FPS > 200. Latency > 85 нс ограничивает 1% Low — GPU уровня RTX 4080 простаивает на 20–30% в ожидании данных от ОЗУ."
  optimal_for_intents: ["home_server_24_7", "scientific_computing", "virtualization", "data_engineering"]
  failure_for_intents: ["esports_1080p_240hz", "esports_1080p_360hz", "aaa_1440p_high"]
  failure_severity: "WARN"
```

---

## 6. Case Profiles

### sound_dampened_thermal_trap
**Физический критерий (L1/L2):** Глухие стальные панели с битумными/войлочными шумопоглощающими матами. Боковые воздухозаборники шириной ≤ 20 мм.

```yaml
sound_dampened_thermal_trap:
  steel_man_desc: "Сборки средней мощности (TDP системы ≤ 200W). Полное поглощение высокочастотного писка дросселей и шелеста вентиляторов. Абсолютная тишина в простое и под лёгкой нагрузкой."
  failure_mode_desc: "Системы > 400W (Core i7 + RTX 4080). Узкие воздухозаборники не обеспечивают приток холодного воздуха. Температура внутри достигает 50–55°C. Вентиляторы GPU/CPU выходят на PWM > 80% — шум превышает открытый mesh-корпус, где хватает 40% PWM."
  optimal_for_intents: ["silent_build", "office_productivity", "home_server_24_7"]
  failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu", "llm_training_lora"]
  failure_severity: "BLOCK"
```

---

## Использование

1. **LLM layer** — `steel_man_desc` и `failure_mode_desc` используются для генерации prose-обоснований в артефактах сборок
2. **Python layer** — `optimal_for_intents` и `failure_for_intents` используются в `evaluate_profiles.py` для O(1) проверки конфликтов через set intersection
3. **Resolution** — при конфликте `failure_severity: WARN` пользователь получает предупреждение с Trade-off; `BLOCK` останавливает сборку
