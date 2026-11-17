---
id: "amd-ryzen-9000"
type: "cpu-family"
title: "AMD Ryzen 9000 (Zen 5)"
status: "draft"
last_updated: "2026-06-03"
links:
  index: "catalog/cpu/index.md"
  platform: "catalog/motherboard/am5/index.md"
  power: "concepts/power-budget.md"
---

# AMD Ryzen 9000 (Zen 5)

Настольная линейка Zen 5 на AM5. Платформа та же, что у Ryzen 7000, поэтому
апгрейд возможен без замены материнской платы и памяти.

## Что изменилось

- Выше IPC и заметно выше эффективность, чем у Zen 4.
- X3D-версии остаются лучшим выбором для игр с упором на frametime.
- DDR5 и PCIe 5.0 сохраняются.
- В многопоточных задачах прирост зависит от SKU и лимитов мощности.
- 9900X и 9950X — два CCD; для игр это компромисс, для рендера — преимущество.

## SKU в каталоге

| Модель | Ядра | TDP | X3D | Файл |
|---|---|---|---|---|
| Ryzen 5 9600X | 6C/12T | 65W | — | `amd-ryzen-5-9600x.md` |
| Ryzen 7 9700X | 8C/16T | 65W | — | `amd-ryzen-7-9700x.md` |
| Ryzen 7 9800X3D | 8C/16T | 120W | ✓ | `amd-ryzen-7-9800x3d.md` |
| Ryzen 9 9900X | 12C/24T | 120W | — | `amd-ryzen-9-9900x.md` |
| Ryzen 9 9950X | 16C/32T | 170W | — | `amd-ryzen-9-9950x.md` |

## Связи

- Все CPU → [`index.md`](index.md)
- Платформа → [`../motherboard/am5/index.md`](../motherboard/am5/index.md)
- 3D V-Cache → [`../../concepts/3d-v-cache.md`](../../concepts/3d-v-cache.md)
- Multi-CCD → [`../../concepts/dual-ccd.md`](../../concepts/dual-ccd.md)
