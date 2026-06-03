---
id: "nvme-index"
type: "index"
title: "NVMe SSD"
status: "verified"
last_updated: "2025-06-03"
---

# NVMe SSD

Твердотельные накопители с интерфейсом NVMe (Non-Volatile Memory Express) через PCIe.

## По поколениям PCIe

| Файл | Поколение | Скорость (seq. read) | Типичные контроллеры |
|---|---|---|---|
| `pcie-gen4.md` | PCIe 4.0 x4 | до 7 400 МБ/с | Phison E18, WD Black G2, Samsung Elpis |
| `pcie-gen5.md` | PCIe 5.0 x4 | до 14 000 МБ/с | Phison E26, Samsung Presto |

## Связи

- Требования к охлаждению (Gen5 греется сильно) → `../../cooling/`
- Бюджет линий PCIe → `../../../concepts/pcie-lanes.md`
