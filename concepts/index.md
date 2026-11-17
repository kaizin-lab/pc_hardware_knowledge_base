---
id: "concepts-index"
type: "index"
title: "Сквозные концепты"
status: "verified"
last_updated: "2026-06-03"
---

# Сквозные концепты

Знания, не привязанные к одному типу компонентов. Объясняют *как работает*,
а не *что купить*.

## Карта

| Файл | Концепт | Связанные компоненты |
|---|---|---|
| `epistemological-profiles.md` | Словарь профилей и интентов | все |
| `modifiers.md` | Модификаторы требований | cpu, gpu, mb, psu |
| `physical-stereotypes.md` | Физические стереотипы | mb, psu, case, cooling |
| `vrm-phases.md` | Фазы питания, удвоители, real vs advertised | motherboard, cpu |
| `pcie-lanes.md` | Линии PCIe, sharing groups, конфликты | motherboard, gpu, storage |
| `memory-timings.md` | Тайминги, ранги, MCLK:UCLK, Gear-режимы | memory, cpu, motherboard |
| `power-budget.md` | Бюджет мощности, пики, ATX-спецификации | psu, cpu, gpu |
| `3d-v-cache.md` | 3D V-Cache и его цена | cpu |
| `dual-ccd.md` | Multi-CCD и межкристальная задержка | cpu |
| `hybrid-architecture.md` | P-ядра и E-ядра Intel | cpu |
| `dpc-latency.md` | DPC latency: пороги, источники, измерение | motherboard, cpu, gpu, audio_interface |
| `audio-interface-drivers.md` | Driver Quality Taxonomy T0–T3 | audio_interface |
| `daw-acoustic-class.md` | A0_Studio для студийной тишины | cooler, psu, case, audio_interface |
| `engineering-tags.md` | Статические предикаты (legacy) | cpu, gpu |

## Как использовать

Загрузи концепт, когда entry-файл ссылается на него через `links:`. Концепт —
это разовый ликбез. LLM загружает один раз и применяет ко всем компонентам.
