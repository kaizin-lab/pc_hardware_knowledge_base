---
id: "intel-arc-b580"
type: "gpu"
title: "Intel Arc B580 12GB"
vendor: "intel"
status: "draft"
tags: ["intel", "battlemage", "bmg-g21-full", "xe2-hpg", "tsmc-n5", "192bit-honest-bus", "12gb-vram", "xmx-engines-192", "xess2-ml", "av1-encode", "pcie5.0-x8", "190w-tbp", "1x8pin-power", "rebar-mandatory", "dx12-vulkan-optimized", "dx11-penalty", "high-idle-power", "subsidized-pricing", "rt-surprisingly-good", "best-fps-per-dollar-budget", "no-cuda", "frametime-gaming-1080p"]
last_updated: "2026-06-03"
links:
  smaller_brother: "catalog/gpu/intel-arc-b570.md"
  competitor_amd: "catalog/gpu/amd-rx-9060-xt.md"
  competitor_nvidia: "catalog/gpu/nvidia-rtx-5060.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "BMG-G21 (Battlemage, полный чип)"
  lithography: "TSMC N5 (5nm)"
  xe_cores: 24
  rt_units: 24
  xmx_engines: 192
  boost_clock: "2.6 GHz"
  vram: "12 GB GDDR6 (192-bit)"
  vram_bandwidth: "456 GB/s"
  l2_cache: "18 MB"
  tbp: "190W"
  power_connector: "1× 8-pin"
  pcie: "PCIe 5.0 x8"
  display_outputs: "3× DP 2.1, 1× HDMI 2.1"
  msrp_usd: "$249"
  engineering_notes: "Полный BMG-G21: 24 Xe-ядра, 192-bit шина, 12GB через 6×2GB. 456 GB/s — лучшая сырая BW среди бюджетных карт (выше чем 448 GB/s у RTX 5060 Ti). XMX-движки (192) — XeSS 2 на уровне DLSS 3.5. RT неожиданно силён для $249. Но драйверы DX9/DX11 — ахиллесова пята, idle power 28-32W — в 3× выше NVIDIA. Лучшая инженерная эффективность (транзисторы/$/производительность) на рынке."
profiles:
  hardware_rt_accelerated_gen_3:
    criteria_met: true
    steel_man_desc: "Path Tracing в реальном времени. Аппаратное ускорение ×4–5 vs растеризация."
    failure_mode_desc: "DX11/OpenGL игры. RT-блоки простаивают — dark silicon."
    optimal_for_intents: ["aaa_4k_path_tracing", "3d_rendering_gpu"]
    failure_for_intents: []
    failure_severity: "WARN"
  tensor_matrix_accelerated:
    criteria_met: true
    steel_man_desc: "Локальное обучение/инференс нейросетей, Stable Diffusion, DLSS/XeSS."
    failure_mode_desc: "Традиционные FP32-вычисления. Тензорные блоки простаивают — паразитный нагрев."
    optimal_for_intents: ["llm_inference_7b", "llm_inference_13b", "stable_diffusion", "ai_upscaling", "llm_training_lora"]
    failure_for_intents: []
    failure_severity: "WARN"
price_ru:
  min: 28990
  median: 32000
  max: 37000
  source: "price.ru (оценка)"
  date: "2026-06-03"
verdict: "Лучший FPS/₽ на рынке бюджетных видеокарт. 12GB за $249 — это ответ Intel на жадность NVIDIA в сегменте до $300. В DX12/Vulkan — уровень RTX 5060 за $100 дешевле. XeSS 2 качественный, AV1-кодеки есть, RT неплох. Но драйверы всё ещё слабое звено для старых игр, idle power высок, а отсутствие high-end моделей ограничивает экосистему. Для современных игр — убийца бюджетного сегмента."
---

# Intel Arc B580 12GB

## Архитектура и позиционирование

Arc B580 — флагман архитектуры Battlemage (Xe2 HPG) на полном чипе BMG-G21. Все 24 Xe-ядра активированы, 192-битная шина, 12GB VRAM. Техпроцесс TSMC N5 — зрелый и эффективный.

Позиционируется Intel как «народная» карта для 1440p. $249 за 12GB — агрессивнейшее ценообразование. Intel продаёт карты с минимальной маржой (или даже в убыток) ради захвата доли рынка.

**Стратегия Intel:** купить аудиторию ценой, отшлифовать драйверы на живой базе пользователей, подготовить почву для Celestial (Xe3) — следующего поколения, где Intel планирует выйти в mid-range.

## Характеристики

- **GPU:** BMG-G21 (Battlemage, полный чип)
- **Техпроцесс:** TSMC N5 (5nm)
- **Xe-ядер:** 24
- **RT-блоков:** 24
- **XMX-движков (Xe Matrix Extensions):** 192
- **Boost Clock:** 2.6 GHz
- **VRAM:** 12 GB GDDR6
- **Шина:** 192-bit
- **Пропускная способность:** 456 GB/s
- **L2-кэш:** 18 MB
- **TBP:** 190W
- **Питание:** 1× 8-pin
- **PCIe:** 5.0 x8
- **Видеовыходы:** 3× DisplayPort 2.1, 1× HDMI 2.1
- **MSRP (USD):** $249

## 12GB за $249 — как Intel это делает

- **Рыночный контекст:** в 2026 году 12GB — это объём RTX 5070 за $549 и RTX 5060 (12GB) за $349. Intel предлагает тот же VRAM за $249 — на $100 дешевле чем NVIDIA и на $130 дешевле чем AMD (RX 9060 XT 16GB за $379, но с 16GB).
- **192-битная шина:** честная конфигурация без narrow bus компромиссов. 456 GB/s достаточно для 1440p.
- **Цена как оружие:** Intel теряет деньги на каждой карте, но строит экосистему. Для потребителя — подарок. Вопрос: как долго Intel готов subsidize?

## Сравнение с конкурентами (Iron Man Argument)

### Arc B580 12GB ($249) vs RTX 5060 12GB ($349)

**Где Arc B580 сильнее:**
- **Цена:** $249 vs $349 — экономия $100 (29%). В РФ: 32 000 ₽ vs 37 000 ₽ — разница 5 000 ₽ скромнее из-за меньшей конкуренции Intel в рознице.
- **VRAM-конфигурация:** 12GB / 192-bit vs 12GB / 128-bit. Пропускная способность: 456 GB/s vs 448 GB/s (GDDR7 у NVIDIA быстрее, но шина уже). В высоких разрешениях 192-bit B580 может выигрывать у 128-bit RTX 5060 несмотря на GDDR6 vs GDDR7.
- **FPS/₽ в DX12/Vulkan:** B580 на 85–95% производительности RTX 5060 за 71% цены. В абсолютных цифрах B580 медленнее, но соотношение цены и FPS — лучшее на рынке.
- **XeSS 2:** Intel догнал качество DLSS 3.5, хотя и уступает DLSS 4. XeSS 2 FG — работает. В играх с поддержкой XeSS 2 — опыт отличный.
- **AV1-кодеки:** полноценное аппаратное кодирование. Для Plex/Jellyfin-серверов — идеальная карта. NVIDIA тоже имеет AV1, но за $349+.
- **RT-производительность:** неожиданно конкурентная. В Cyberpunk 2077 RT Medium 1080p: B580 ~50 FPS vs RTX 5060 ~58 FPS — отставание всего 14%. Для $100 разницы — впечатляет.

**Где Arc B580 слабее:**
- **Драйверы (DX9/DX11) — главная проблема:** в старых играх потери могут достигать 20–30% относительно потенциала железа. Counter-Strike 2 (DX11/Vulkan hybrid) — карта недогружается на 15–20%. Старые MMO (WoW Classic, Lineage 2) — микростаттеры. Ситуация улучшается каждый драйвер, но до паритета с AMD/NVIDIA ещё годы.
- **Производительность в растре (абсолютная):** RTX 5060 всё же быстрее в среднем на 10–15% в DX12. В Call of Duty BO6 1080p: B580 ~125 FPS vs RTX 5060 ~140 FPS. Часть разницы покрывается ценой, но не вся.
- **Энергопотребление в простое:** ~28–32W. RTX 5060: ~8W. Разница в 20W × 24/7 = 14.4 kWh/мес (~100–150 ₽/мес). Для серверов — значимо.
- **Отсутствие high-end моделей:** B580 — потолок Intel в 2025–2026. Если через год захотите мощнее — придётся переходить на AMD/NVIDIA.
- **Процессорозависимость:** Resizable BAR обязателен. Без ReBAR потери достигают 20–25%. Проверьте поддержку в BIOS.
- **Доступность и экосистема:** карты Intel Arc менее доступны в рознице, выбор AIB-моделей ограничен. Реселл-стоимость ниже чем у NVIDIA.

### Arc B580 ($249) vs RX 7600 ($269)

- B580 быстрее на 15–20% в растре, имеет 12GB против 8GB, и дешевле.
- RX 7600 выигрывает только в стабильности драйверов для старых игр.
- **Если библиотека современная — B580 безоговорочно.**

### Arc B580 ($249) vs RTX 5060 8GB ($299)

- B580 быстрее или наравне, имеет 12GB против 8GB, дешевле на $50.
- NVIDIA выигрывает только в RT и DLSS 4.
- **Вывод:** в бюджетном сегменте B580 доминирует над RTX 5060 8GB. 8GB — просто недостаточно в 2026.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 28 990–37 000 ₽
- **Медиана:** ~32 000 ₽
- **Типичные модели:** ASRock Steel Legend, Sparkle Titan, Gunnir Photon, Acer Nitro

Рекомендация: ASRock Steel Legend (~30 000 ₽) — лучший вариант. Sparkle Titan (~33 000 ₽) — хороший кулер. Acer Nitro и Gunnir Photon — редкие, возможны проблемы с гарантией.

**Парадокс рынка:** в РФ разница между B580 (32 000 ₽) и RTX 5060 12GB (37 000 ₽) — всего 5 000 ₽. При такой маленькой дельте NVIDIA становится привлекательнее для не-энтузиастов. Но если найдёте B580 по 29 000 — берите не думая.

## Для кого

**Подходит:**
- Лучший бюджетный выбор для 1080p-ультра и 1440p-средних
- Современные игры на DX12/Vulkan (Cyberpunk 2077, Alan Wake 2, Call of Duty, Hogwarts Legacy)
- Бюджетные сборки до 80 000 ₽
- Стримеры-любители (AV1-кодирование)
- Plex/Jellyfin-серверы с транскодингом (AV1 + низкая цена)
- Апгрейд с GTX 1060 / 1650 / 1660 / RX 580 / RX 5500 XT
- Энтузиасты, готовые мириться с драйверными нюансами

**Не подходит:**
- Игры на старых API (DX9/DX11) — драйверы не готовы для daily-driver без компромиссов
- Киберспортсмены (CS2 — нестабильная производительность)
- Профессиональная работа (нет CUDA, слабая поддержка в Blender/Adobe)
- 4K-гейминг (12GB и производительность чипа недостаточны)
- Апгрейд с RTX 3060 12GB / RX 6700 XT — прирост недостаточен
- Системы без Resizable BAR (проверьте перед покупкой)
- Серверы 24/7 (idle power высок)

## Источники

1. TechPowerUp — «Intel Arc B580 Review: Battlemage Arrives» (2025)
2. Hardware Unboxed — «Arc B580 vs RTX 5060 vs RX 7600: Best Budget GPU?»
3. Gamers Nexus — «Intel Arc B580: $249 GPU Full Benchmark & Tear-Down»
4. Digital Foundry — «XeSS 2: Intel's DLSS Competitor Analyzed»
5. Tom's Hardware — «Arc B580 DX11 Performance Analysis & Driver Maturity»
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории
