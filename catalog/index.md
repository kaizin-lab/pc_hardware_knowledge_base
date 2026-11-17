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
Каждый компонент — через Iron Man Argument: объективно, без хейта.

> Цены в индексах — ориентир. Актуальная цена, источник и дата — в карточке.

## ⚠️ ДИРЕКТИВА ДЛЯ LLM-АГЕНТА

При встрече ссылки вида **`path/to/file.md#section-name`**:

1. Загрузи файл через `read_file`.
2. Найди секцию — извлеки конкретику.
3. Не делай расчётов без загрузки данных по ссылке.

## Структура

| Директория | Карточек | Охват |
|---|---|---|
| `cpu/` | **24** | AMD Zen 4 (8) + Zen 5 (5) + Intel Arrow Lake (5) + Raptor Lake (3) + Alder Lake (3) |
| `gpu/` | **15** | NVIDIA RTX 50xx (6) + RTX 40xx (3) + AMD RX 9000 (3) + RX 7600 + Intel Arc B (2) |
| `motherboard/` | **22** | AM5 (11), LGA1700 (9), LGA1851 (2) |
| `memory/` | **8** | DDR5 (6) + DDR4 (2) |
| `storage/nvme/` | **9** | NVMe Gen4 и Gen5 |
| `psu/` | **10** | ATX 3.x (7) + ATX 2.x (3) |
| `cooling/` | **10** | Air (7) + Liquid (3) |
| `case/` | **5** | Mesh и sound-dampened |
| `audio-interface/` | **8** | RME, MOTU, Focusrite, UA — T0–T3 |
| `monitor/` | **0** | Только индекс, карточек нет |
| `intents/` | **6** | AAA, AI inference, data engineering, esports, SFF, DAW |

**Всего: 111 карточек + 6 интентов + 14 концептов.**

## Прогресс наполнения

- ✅ **GPU** — RTX 50xx/40xx, RX 9000/7000, Arc B.
- ✅ **CPU** — Zen 4/5, Arrow Lake, Raptor Lake, Alder Lake.
- ✅ **Материнские платы** — AM5, LGA1700, LGA1851.
- ✅ **Память** — DDR5 и DDR4, включая бюджетные комплекты.
- ✅ **Накопители** — NVMe Gen4/Gen5.
- ✅ **БП** — ATX 3.x и ATX 2.x.
- ✅ **Охлаждение** — воздух и СЖО.
- ✅ **Корпуса** — mesh и sound-dampened.
- ✅ **Аудиоинтерфейсы** — T0–T3, USB и Thunderbolt.
- ⬜ **Мониторы** — только индекс.

## Сквозные концепты

`../concepts/`:

- `epistemological-profiles.md` — словарь профилей и интентов.
- `modifiers.md` — каталог модификаторов.
- `physical-stereotypes.md` — физические стереотипы.
- `vrm-phases.md` — фазы питания и удвоители.
- `pcie-lanes.md` — линии PCIe и sharing groups.
- `memory-timings.md` — тайминги, ранги, MCLK:UCLK.
- `power-budget.md` — бюджет мощности и ATX-спецификации.
- `3d-v-cache.md` — 3D V-Cache.
- `dual-ccd.md` — multi-CCD и межкристальная задержка.
- `hybrid-architecture.md` — P-ядра и E-ядра Intel.
- `dpc-latency.md` — DPC latency в аудио-домене.
- `audio-interface-drivers.md` — классификация драйверов T0–T3.
- `daw-acoustic-class.md` — акустическая модель A0_Studio.
- `engineering-tags.md` — статические предикаты (legacy).

## Скрипты

`../scripts/`:

- `query.py` — поиск по типу, vendor, тегам, ссылкам.
- `evaluate_profiles.py` — профильный матчинг.
- `validate_physical_constraints.py` — физические предикаты.
- `audit_tags.py` — проверка статических предикатов.
- `check_links.py` — целостность базы.
- `pcbo/` — экспериментальный подбор сборки и динамические ограничения.
