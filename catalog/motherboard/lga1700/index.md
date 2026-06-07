---
id: "lga1700-index"
type: "index"
title: "Материнские платы LGA1700"
status: "draft"
last_updated: "2026-06-07"
links:
  platform_cpu: "catalog/cpu/intel-core-i9-14900k.md"
  dpc_concept: "concepts/dpc-latency.md"
---

# Материнские платы LGA1700

Платформа Intel 12/13/14-го поколения (Alder Lake / Raptor Lake / Raptor Lake Refresh). Несмотря на статус «завершённой», остаётся актуальной для DAW — аудио-требования не растут с поколениями CPU.

## Карта моделей

| Файл | Модель | Чипсет | Ключевое | Цена |
|---|---|---|---|---|
| `asus-proart-z790-e.md` | ASUS ProArt Z790-E Creator | Z790 | 10GbE + 2.5GbE, 2× TB4 | ~42 000 |
| `asrock-z790-taichi.md` | ASRock Z790 Taichi | Z790 | 24+1+2 (105A), 2× TB4 | ~40 000 |
| `msi-meg-z790-ace.md` | MSI MEG Z790 Ace | Z790 | 5× M.2 (2× Gen5), USB4 | ~48 000 |

## DPC-профиль платформы

Все три платы требуют отключения WiFi/BT в UEFI для аудио-использования. Intel I226-V 2.5GbE — проверять ревизию (v3 предпочтительна). Killer E3100G на Taichi — стабильнее для DPC.

## Связи

- CPU: `catalog/cpu/intel-core-i9-14900k.md`, `intel-core-i7-14700k.md`, `intel-core-i5-14600k.md`
- DPC Latency: `concepts/dpc-latency.md`
- Конкурентная платформа: `catalog/motherboard/am5/index.md`
