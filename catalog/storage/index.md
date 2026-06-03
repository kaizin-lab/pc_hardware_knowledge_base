---
id: "storage-index"
type: "index"
title: "Накопители"
status: "verified"
last_updated: "2025-06-03"
---

# Накопители

## Карта

| Файл/Директория | Тип | Интерфейс | Скорость |
|---|---|---|---|
| `nvme/index.md` | NVMe SSD | PCIe | 3.5–14 ГБ/с |
| `sata-ssd.md` | SATA SSD | SATA III | 560 МБ/с |
| `hdd.md` | HDD | SATA III | 150–250 МБ/с |

## NVMe — по поколениям PCIe

| Директория | Поколение | Макс. пропускная способность |
|---|---|---|
| `nvme/pcie-gen4.md` | PCIe 4.0 x4 | ~7 ГБ/с |
| `nvme/pcie-gen5.md` | PCIe 5.0 x4 | ~14 ГБ/с |

## Связи

- PCIe-линии → `../../concepts/pcie-lanes.md`
- Конфликты с SATA-портами → `../motherboard/`
