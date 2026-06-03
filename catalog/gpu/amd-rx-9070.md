---
id: "amd-rx-9070"
type: "gpu"
title: "AMD Radeon RX 9070 16GB"
vendor: "amd"
status: "draft"
tags: ["amd", "rdna4", "navi48", "cut-die", "tsmc-n5", "256bit-honest-bus", "16gb-vram-safe", "infinity-cache-64mb", "pcie5.0-x16", "fsr4-ml-based", "rt-3rd-gen-improved", "240w-tbp", "2x8pin-power", "dp2.1-uhbr13.5", "4k-entry", "1440p-ultra", "raster-optimized", "rt-mid", "local-llm-viable", "frametime-gaming-1440p"]
last_updated: "2026-06-03"
links:
  bigger_brother: "catalog/gpu/amd-rx-9070-xt.md"
  smaller_brother: "catalog/gpu/amd-rx-9060-xt.md"
  competitor_nvidia: "catalog/gpu/nvidia-rtx-5070.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "Navi 48 (RDNA 4)"
  lithography: "TSMC N5 (5nm)"
  stream_processors: 5632
  compute_units: 88
  ray_accelerators: 88 (3-е поколение)
  ai_accelerators: 176
  boost_clock: "2.8 GHz (Game Clock ~2.45 GHz)"
  vram: "16 GB GDDR6 (256-bit)"
  vram_bandwidth: "640 GB/s"
  infinity_cache: "64 MB"
  tbp: "240W"
  power_connector: "2× 8-pin (референс)"
  pcie: "PCIe 5.0 x16"
  display_outputs: "3× DP 2.1 UHBR 13.5, 1× HDMI 2.1b"
  msrp_usd: "$499"
  engineering_notes: "Navi 48 — урезанный чип (88/96 CU), но с сохранением полной 256-bit шины и 64MB Infinity Cache. Критическое решение AMD: memory subsystem не трогают (в отличие от NVIDIA где 5070 получает 192-bit вместо 256-bit). 640 GB/s как у XT-версии. Потеря 8 CU = -6-8% FPS. Позиционируется против RTX 5070 ($549, 12GB, 192-bit) и бьёт аргументом 16GB+256-bit за $499."
price_ru:
  min: 55990
  median: 64000
  max: 78000
  source: "price.ru (оценка)"
  date: "2026-06-03"
verdict: "Самый рациональный выбор для 1440p и начального 4K. 16GB на 256-bit — честная конфигурация без компромиссов. Быстрее RTX 5070 в чистом растре на 10%, при этом на $50 дешевле и с бóльшим VRAM. Главный минус — RT отстаёт от NVIDIA и нет DLSS 4 MFG. Но FSR 4 уже хорош настолько, что это перестаёт быть dealbreaker."
---

# AMD Radeon RX 9070 16GB

## Архитектура и позиционирование

RX 9070 построена на GPU Navi 48 — чипе среднего звена архитектуры RDNA 4. В отличие от флагманского Navi 48 XT (RX 9070 XT), здесь часть вычислительных блоков отключена, но сохранена полная 256-битная шина памяти — ключевое преимущество над NVIDIA RTX 5070 с её 192-bit.

Позиционируется как прямой конкурент RTX 5070 с чётким посылом: «те же деньги — больше FPS и больше VRAM». AMD агрессивно бьёт в слабое место NVIDIA (12GB) своим 16GB.

**Стратегия AMD:** выиграть raster war и VRAM war, пока RDNA 4 догоняет NVIDIA в RT и апскейлинге.

## Характеристики

- **GPU:** Navi 48 (RDNA 4)
- **Техпроцесс:** TSMC N5 (5nm)
- **Потоковых процессоров:** 5632 (88 CU)
- **RT-ускорителей:** 88 (3-е поколение)
- **AI-ускорителей:** 176
- **Game Clock:** ~2.45 GHz
- **Boost Clock:** 2.8 GHz
- **VRAM:** 16 GB GDDR6
- **Шина:** 256-bit
- **Пропускная способность:** 640 GB/s
- **Infinity Cache:** 64 MB
- **TBP:** 240W
- **Питание:** 2× 8-pin (референс)
- **PCIe:** 5.0 x16
- **Видеовыходы:** 3× DisplayPort 2.1 UHBR 13.5, 1× HDMI 2.1b
- **MSRP (USD):** $499

## 256-bit + 16GB — конфигурация без бутылочных горлышек

В отличие от RTX 5070 (192-bit, 12GB), у RX 9070 нет искусственных ограничений:

- **Пропускная способность:** 640 GB/s — достаточно для 4K-текстур без просадок.
- **VRAM:** 16GB — запас на 3+ года. Ни одна игра 2025–2026 не упирается в 16GB даже в 4K (кроме Path Tracing).
- **Шина:** 256-bit не режет производительность на высоких разрешениях.

**Сравнение с RTX 5070 (12GB, 192-bit, $549):** AMD предлагает лучшую «бумажную» конфигурацию памяти за меньшие деньги. Разница проявится не сегодня, а через 2 года, когда 12GB станет узким местом.

## Сравнение с конкурентами (Iron Man Argument)

### RX 9070 16GB ($499) vs RTX 5070 12GB ($549)

**Где RX 9070 сильнее:**
- **Чистый растр (без RT/апскейлеров, 1440p):** RX 9070 на 8–12% быстрее. Call of Duty BO6: RX 9070 ~155 FPS vs RTX 5070 ~140 FPS. Horizon Forbidden West: RX 9070 ~98 FPS vs RTX 5070 ~88 FPS. Cyberpunk 2077 Ultra no RT: RX 9070 ~92 FPS vs RTX 5070 ~84 FPS.
- **VRAM и шина:** 16GB / 256-bit vs 12GB / 192-bit. В 4K с текстурами ультра RX 9070 имеет ощутимый запас. Indiana Jones 1440p Supreme: RTX 5070 на грани по VRAM, RX 9070 — комфортно.
- **Цена:** $499 vs $549 — экономия $50. В РФ разница ~8 000–12 000 ₽.
- **DisplayPort 2.1 UHBR 13.5:** полноценный стандарт. NVIDIA использует DP 2.1b с урезанной пропускной способностью.
- **FSR 4:** ML-based апскейлинг нового поколения — качество картинки вплотную к DLSS 4. Артефакты минимальны даже в движении. Да, DLSS 4 всё ещё эталон, но FSR 4 уже «достаточно хорош» для 90% игроков.
- **Экосистема AMD:** SAM (Smart Access Memory) с Ryzen, HYPR-RX (one-click оптимизация), AFMF 2 (драйверный frame gen для любых игр).

**Где RX 9070 слабее:**
- **Трассировка лучей:** RT-ускорители RDNA 4 улучшены, но NVIDIA RT-ядра 4-го поколения всё ещё впереди на 35–50%. Cyberpunk 2077 RT Ultra 1440p: RX 9070 ~44 FPS vs RTX 5070 ~62 FPS. Alan Wake 2 Path Tracing — игровой опыт на RX 9070 компромиссный.
- **DLSS 4 MFG vs FSR 4 FG:** MFG генерирует до 3 кадров, FSR 4 FG — один. В играх где MFG поддерживается, NVIDIA обеспечивает лучшую плавность.
- **CUDA-экосистема:** Blender — в 1.8 раза медленнее чем RTX 5070. AI/ML (Stable Diffusion, LLM) — работает через ROCm, но с танцами. Критично для профессионалов.
- **NVENC:** кодировщик NVIDIA 9-го поколения лучше для стриминга при низком битрейте. AMD AMF улучшился, но до NVENC не дотягивает.
- **Поколенческий прирост над RX 7800 XT:** +25–30% в растре — хорошо, но не революционно. RTX 5070 над RTX 4070: +15–20% — хуже.

### Вердикт

- **1440p ультра, 4K без RT, FPS/₽ → RX 9070.** Лучшая карта в $500-сегменте для чистого растра. 16GB — страховка на будущее.
- **RT-игры, CUDA-работа, стриминг → RTX 5070.** $50 переплаты за DLSS 4 MFG и RT-лидерство оправданы, если эти фичи используются ежедневно.
- **4K RT gaming → ни одна.** Нужна RTX 5070 Ti или RX 9070 XT.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 55 990–78 000 ₽
- **Медиана:** ~64 000 ₽
- **Типичные модели:** Sapphire Nitro+, PowerColor Red Devil, XFX Mercury, ASRock Steel Legend

Рекомендация: Sapphire Nitro+ (~62 000 ₽) — лучший кулер в классе. PowerColor Red Devil (~65 000 ₽) — для любителей тишины. XFX Mercury (~68 000 ₽) — переоценён за заводской разгон.

## Для кого

**Подходит:**
- 1440p-гейминг на ультра-настройках в любых современных играх
- Начальный 4K-гейминг со средними/высокими настройками + FSR 4
- Сборки Ryzen + Radeon (SAM даёт +5–7% бесплатно)
- Апгрейд с RX 5700 XT / RX 6700 XT / RTX 2070 Super
- Игры с активным моддингом (16GB VRAM — запас)

**Не подходит:**
- Игры с трассировкой лучей как приоритетом → RTX 5070
- Профессиональная работа с CUDA (Blender, AI/ML, Adobe)
- 4K-ультра с RT (нужна RX 9070 XT / RTX 5070 Ti)
- Стриминг с упором на качество кодирования (NVENC предпочтительнее)
- Владельцы RX 7800 XT — прирост +25% недостаточен для апгрейда

## Источники

1. TechPowerUp — «AMD Radeon RX 9070 Review» (2025)
2. Hardware Unboxed — «RX 9070 vs RTX 5070: 50 Game Benchmark»
3. Gamers Nexus — «RDNA 4 Navi 48: RX 9070 Deep Dive»
4. Digital Foundry — «FSR 4 vs DLSS 4: Quality Comparison 2025»
5. AMD GPUOpen — RDNA 4 Ray Tracing & AI Architecture
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории
