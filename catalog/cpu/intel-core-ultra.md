---
id: "intel-core-ultra"
type: "cpu-family"
title: "Intel Core Ultra 200S (Arrow Lake)"
status: "draft"
last_updated: "2026-06-03"
links:
  index: "catalog/cpu/index.md"
  platform: "catalog/motherboard/lga1851/index.md"
  power: "concepts/power-budget.md"
---

# Intel Core Ultra 200S (Arrow Lake)

Настольное семейство Intel на LGA1851. Гибридная схема: P-ядра Lion Cove и
E-ядра Skymont, вычисления вынесены на отдельный TSMC N3B tile.

## Что важно

- Новый сокет LGA1851 — платы LGA1700 не подходят.
- DDR5 only.
- Ниже энергопотребление в многопотоке, чем у Raptor Lake.
- В играх поколение неровное: результат зависит от планировщика и памяти.
- Десктопный Arrow Lake-S не имеет NPU, несмотря на маркетинг платформы.

## SKU в каталоге

| Модель | Ядра | TDP | iGPU | Файл |
|---|---|---|---|---|
| Ultra 5 225F | 10C/10T | 65W | — | `intel-core-ultra-5-225f.md` |
| Ultra 5 245K | 14C/14T | 125W | Xe | `intel-core-ultra-5-245k.md` |
| Ultra 7 265F | 20C/20T | 65W | — | `intel-core-ultra-7-265f.md` |
| Ultra 7 265K | 20C/20T | 125W | Xe | `intel-core-ultra-7-265k.md` |
| Ultra 9 285K | 24C/24T | 125W | Xe | `intel-core-ultra-9-285k.md` |

## Связи

- Все CPU → [`index.md`](index.md)
- Платформа → [`../motherboard/lga1851/index.md`](../motherboard/lga1851/index.md)
- Гибридная архитектура → [`../../concepts/hybrid-architecture.md`](../../concepts/hybrid-architecture.md)
