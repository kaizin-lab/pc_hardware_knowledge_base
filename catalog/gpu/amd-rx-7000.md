---
id: "amd-rx-7000"
type: "gpu-architecture"
title: "AMD RDNA 3 — Radeon RX 7000"
status: "draft"
last_updated: "2026-06-03"
links:
  index: "catalog/gpu/index.md"
  pcie: "concepts/pcie-lanes.md"
  power: "concepts/power-budget.md"
---

# AMD RDNA 3 — Radeon RX 7000

Архитектура AMD, которая всё ещё встречается в бюджетном сегменте. В каталоге
представлена одной картой — RX 7600.

## Что важно

- Чиплетная компоновка у старших моделей, монолитная у Navi 33.
- Большой Infinity Cache компенсирует узкую шину памяти.
- RDNA 3 заметно слабее в трассировке лучей, чем Ada и Blackwell.
- FSR работает, но по качеству уступает DLSS.
- RX 7600 использует PCIe 4.0 ×8 — на старых платах возможна небольшая потеря.

## Карты в каталоге

| Модель | VRAM | TBP | PCIe | Файл |
|---|---|---|---|---|
| RX 7600 | 8 GB | 165W | 4.0 ×8 | `amd-rx-7600.md` |

## Связи

- Все GPU → [`index.md`](../gpu/index.md)
- PCIe → [`../../concepts/pcie-lanes.md`](../../concepts/pcie-lanes.md)
- Питание → [`../../concepts/power-budget.md`](../../concepts/power-budget.md)
