---
id: "nvidia-rtx-4000"
type: "gpu-architecture"
title: "NVIDIA Ada Lovelace — GeForce RTX 40"
status: "draft"
last_updated: "2026-06-03"
links:
  index: "catalog/gpu/index.md"
  pcie: "concepts/pcie-lanes.md"
  power: "concepts/power-budget.md"
---

# NVIDIA Ada Lovelace — GeForce RTX 40

Предыдущее поколение NVIDIA, всё ещё актуальное в бюджетном и среднем
сегменте. В каталоге три карты: RTX 4060, 4060 Ti и 4070.

## Что важно

- Энергоэффективность заметно выше, чем у Ampere.
- DLSS 3.5 и Frame Generation — сильный аргумент там, где они поддерживаются.
- Трассировка лучей остаётся лучшей в классе.
- Младшие карты страдают от 128-битной шины и 8 GB VRAM.
- RTX 4060/4060 Ti используют PCIe 4.0 ×8; на Gen3 теряют несколько процентов.

## Карты в каталоге

| Модель | VRAM | TGP | PCIe | Файл |
|---|---|---|---|---|
| RTX 4060 | 8 GB | 115W | 4.0 ×8 | `nvidia-rtx-4060.md` |
| RTX 4060 Ti | 8/16 GB | 165W | 4.0 ×8 | `nvidia-rtx-4060-ti.md` |
| RTX 4070 | 12 GB | 200W | 4.0 ×16 | `nvidia-rtx-4070.md` |

## Связи

- Все GPU → [`index.md`](../gpu/index.md)
- PCIe → [`../../concepts/pcie-lanes.md`](../../concepts/pcie-lanes.md)
- Питание → [`../../concepts/power-budget.md`](../../concepts/power-budget.md)
