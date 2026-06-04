---
id: "catalog-root"
type: "index"
title: "Каталог компонентов"
status: "verified"
last_updated: "2026-06-03"
links:
  intents: "catalog/intents/index.md"
  profiles: "concepts/epistemological-profiles.md"
  modifiers: "concepts/modifiers.md"
  physical_stereotypes: "concepts/physical-stereotypes.md"
---

# Каталог компонентов

Корень knowledge base. Все компоненты ПК-железа, организованные по типу.
Каждый компонент — через Iron Man Argument (объективно, без хейта).

## ⚠️ ДИРЕКТИВА ДЛЯ LLM-АГЕНТА

При встрече ссылки вида **`path/to/file.md#section-name`**:
1. Загрузи файл через read_file
2. Найди секцию — извлеки конкретику
3. Не делай расчётов без загрузки данных по ссылке

## Структура

| Директория | Entry | Охват |
|---|---|---|
| `cpu/` | **17** | AMD Zen 4 (8) + Zen 5 (3) + Intel Arrow Lake (6) |
| `gpu/` | **13** | NVIDIA 50xx (6) + 4060 + AMD RX 9000 (3) + 7600 + Intel Arc B (2) |
| `motherboard/` | **5** | AM5: Tomahawk B650, B650M S2H, B850 Riptide, X870 Steel Legend + LGA1851: Z890 Pro RS |
| `memory/` | **5** | DDR5: обзор + Ripjaws S5 (6000 CL30) + 6400 CL32 + 5200 JEDEC + DDR4-обзор |
| `storage/nvme/` | **4** | NVMe: Kingston NV3, Samsung 990 Pro, WD SN850X, Crucial T700 |
| `psu/` | **4** | Deepcool PN750D, PF650, PN850D, FSP Hydro PTM X Pro 1000W |
| `cooling/` | **4** | Air: AK400, AK620. Liquid: LF3 240, LF3 360 |
| `case/` | **2** | Deepcool CC560, Be Quiet Pure Base 500 |
| `intents/` | **5** | Esports 360Hz, AAA 4K, AI Inference, Data Eng, SFF Compact |

**Всего: 54 entry + 5 интентов = 59 артефактов**

## Прогресс наполнения

- ✅ **GPU** — полная линейка NVIDIA 50xx, AMD RX 9000/7000, Intel Arc Battlemage
- ✅ **CPU** — все актуальные Zen 4, Zen 5, Arrow Lake
- ✅ **Материнские платы** — AM5 (4) + LGA1851 (1)
- ✅ **Память** — DDR5 (4) + DDR4-обзор
- ✅ **Накопители** — NVMe Gen4/Gen5 (4)
- ✅ **БП** — ATX 3.x (3) + ATX 2.x бюджет (1)
- ✅ **Охлаждение** — воздушное (2) + СЖО (2)
- ✅ **Корпуса** — бюджет mesh (1) + sound-dampened (1)
- ✅ **Интенты** — 5 полярных (esports, 4K, AI, data, SFF)

**Все категории покрыты!** Дальнейшее наполнение — точечное, под конкретные gaps в intent coverage.

## Сквозные концепты

`../concepts/`:
- `epistemological-profiles.md` — словарь 26 поведенческих профилей v3.3
- `modifiers.md` — каталог модификаторов (+hardware_codec, +ecc, +dual_bios, +passive)
- `physical-stereotypes.md` — физические стереотипы (SFX, 8-layer PCB, ITX)
- `vrm-phases.md` — фазы питания, удвоители, real vs advertised
- `pcie-lanes.md` — линии PCIe, конфликты, sharing groups
- `memory-timings.md` — тайминги, ранги, MCLK:UCLK
- `power-budget.md` — бюджет мощности, пики потребления, ATX-спецификации

## Скрипты

`../scripts/`:
- `query.py` — поиск по тегам, vendor, socket, price range
- `evaluate_profiles.py` — профильный движок (BLOCK/WARN/optimal)
- `validate_physical_constraints.py` — Skill 9: бинарные физические проверки
- `audit_tags.py` — проверка статических предикатов
