---
id: "nvme-index"
type: "index"
title: "NVMe SSD"
status: "draft"
last_updated: "2025-06-03"
---

# NVMe SSD

Твердотельные накопители с NVMe через PCIe. Только M.2 2280 — актуальный форм-фактор.

## Карта

| Файл | Модель | Поколение PCIe | Объём | Тип NAND | Цена (₽) |
|---|---|---|---|---|---|
| `kingston-nv3-1tb.md` | Kingston NV3 | 4.0 x4 | 1 TB | TLC (DRAM-less) | ~5 500 |

## Что ещё нужно заполнить

- **PCIe 4.0**: WD SN850X, Samsung 990 Pro, Kingston Fury Renegade — DRAM-кэш, для OS
- **PCIe 5.0**: T700, Samsung 9100 Pro — горячие, требуют радиатор
- **Бюджетный**: Kingston NV3 2TB (DRAM-less, но HMB компенсирует)

## Связи

- Требования к охлаждению (Gen5 греется) → `../../cooling/`
- Бюджет линий PCIe → `../../../concepts/pcie-lanes.md`
