---
id: "catalog-root"
type: "index"
title: "Каталог компонентов"
status: "verified"
last_updated: "2025-06-03"
---

# Каталог компонентов

Корень каталога. Все компоненты ПК-железа, организованные по типу. Только актуальные поколения (последние 2 года). Каждый компонент — через Iron Man Argument (объективно, без хейта).

## Структура

| Директория | Entry | Охват |
|---|---|---|
| `cpu/` | **17** | AMD Zen 4 (8 SKU) + Zen 5 (3) + Intel Arrow Lake (5) + обзор Zen 4 |
| `gpu/` | **13** | NVIDIA 50xx (6) + 4060 + AMD RX 9000 (3) + 7600 + Intel Arc B (2) |
| `motherboard/` | **2** | AM5: Tomahawk B650, B650M S2H |
| `memory/` | **3** | DDR5-обзор + Ripjaws S5 6000 + DDR5-5600 |
| `storage/` | **1** | NVMe: Kingston NV3 1TB |
| `psu/` | **1** | Deepcool PN750D |
| `cooling/` | — | Индексы air/liquid, entry не заведены |
| `case/` | — | Индекс, entry не заведены |
| `monitor/` | — | Индекс, entry не заведены |

**Всего: 37 entry**

## Прогресс наполнения

- ✅ **GPU** — полная линейка NVIDIA 50xx, AMD RX 9000/7000, Intel Arc Battlemage
- ✅ **CPU** — все актуальные Zen 4, Zen 5, Arrow Lake (Consumer)
- ⬜ **Материнские платы** — только 2 AM5, нет B850/X870, нет LGA1851
- ⬜ **Память** — только обзор DDR5 + 2 конкретных комплекта
- ⬜ **Накопители** — 1 NVMe Gen4
- ⬜ **БП** — 1 модель
- ⬜ **Охлаждение, корпуса, мониторы** — пустые индексы

## Как искать

1. **Загрузи `index.md` нужной поддиректории** — он покажет таксономию, связи, и все entry с ключевыми параметрами
2. **Используй `scripts/query.py`** для выборок по vendor, socket, tags, price range
3. **Каждый entry** — самодостаточный файл с frontmatter (id, type, vendor, socket, tdp, tags) и prose-телом

## Сквозные концепты

`../concepts/`:
- `vrm-phases.md` — фазы питания, удвоители, real vs advertised
- `pcie-lanes.md` — линии PCIe, конфликты, sharing groups
- `memory-timings.md` — тайминги, ранги, MCLK:UCLK
- `power-budget.md` — бюджет мощности, пики потребления, ATX-спецификации
