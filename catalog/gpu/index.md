---
id: "gpu-index"
type: "index"
title: "Видеокарты"
status: "verified"
last_updated: "2026-06-19"
---

# Видеокарты (GPU)

Актуальные видеокарты: NVIDIA Blackwell (50xx), AMD RDNA 3/4 (RX 7000/9000), Intel Battlemage (Arc B).

Все карты рассмотрены через Iron Man Argument — без хейта, с объективным балансом сильных и слабых сторон.

## Карта

### NVIDIA GeForce RTX 50 (Blackwell) — GDDR7, PCIe 5.0
| Файл | Модель | VRAM | TBP | Цена (₽) | Позиционирование |
|---|---|---|---|---|---|
| `nvidia-rtx-5060.md` | RTX 5060 | 8 GB | 145W | ~35 000 | 1080p High |
| `nvidia-rtx-5060-ti.md` | RTX 5060 Ti | 16 GB | 180W | ~52 000 | 1440p Entry |
| `nvidia-rtx-5070.md` | RTX 5070 | 12 GB | 250W | ~72 000 | 1440p High |
| `nvidia-rtx-5070-ti.md` | RTX 5070 Ti | 16 GB | 300W | ~74 000 | 4K Entry / 1440p Ultra |
| `nvidia-rtx-5080.md` | RTX 5080 | 16 GB | 360W | ~108 000 | 4K High |
| `nvidia-rtx-5090.md` | RTX 5090 | 32 GB | 575W | ~199 000 | 4K Max / AI 32GB |

### NVIDIA GeForce RTX 40 (Ada Lovelace) — остатки
| Файл | Модель | VRAM | TBP | Цена (₽) | Позиционирование |
|---|---|---|---|---|---|
| `nvidia-rtx-4060.md` | RTX 4060 | 8 GB | 115W | ~27 000 | 1080p бюджет |
| `nvidia-rtx-4060-ti.md` | RTX 4060 Ti | 16 GB | 165W | ~46 500 | 1080p AI/работа |
| `nvidia-rtx-4070.md` | RTX 4070 | 12 GB | 200W | ~45 000 | 1440p энергоэффективность |

### AMD Radeon RX 9000 (RDNA 4) — GDDR6, PCIe 5.0
| Файл | Модель | VRAM | TBP | Цена (₽) | Позиционирование |
|---|---|---|---|---|---|
| `amd-rx-9060-xt.md` | RX 9060 XT | 16 GB | ~200W | ~34 000 | 1440p, FPS/₽ king |
| `amd-rx-9070.md` | RX 9070 | 16 GB | 220W | ~51 000 | 1440p Ultra |
| `amd-rx-9070-xt.md` | RX 9070 XT | 16 GB | 304W | ~64 000 | 4K Entry, RT улучшен |

### AMD Radeon RX 7000 (RDNA 3) — остатки
| Файл | Модель | VRAM | TBP | Цена (₽) | Позиционирование |
|---|---|---|---|---|---|
| `amd-rx-7600.md` | RX 7600 | 8 GB | 165W | ~27 000 | 1080p FPS/₽ |

### Intel Arc B (Battlemage) — GDDR6, PCIe 4.0
| Файл | Модель | VRAM | TBP | Цена (₽) | Позиционирование |
|---|---|---|---|---|---|
| `intel-arc-b570.md` | Arc B570 | 10 GB | 150W | ~22 000 | 1080p / бюджет-король |
| `intel-arc-b580.md` | Arc B580 | 12 GB | 190W | ~26 000 | 1440p Entry |

## Iron Man Argument — ключевые тезисы

- **NVIDIA**: лидер по RT, DLSS, энергоэффективности. Слабые: цена, VRAM-голод на младших моделях (5060 — 8GB в 2026).
- **AMD**: лучший FPS/₽, щедрый VRAM (16GB на 9060 XT). Слабые: RT отстаёт, FSR пока хуже DLSS.
- **Intel Arc**: лучший бюджет (B570 за ~22k с 10GB), аппаратный AV1. Слабые: драйверы — остаточные проблемы в старых DX9/11, но Battlemage сильно лучше Alchemist.

## Как выбирать

1. **Бюджет 1080p** → Arc B570 (FPS/₽ чемпион) или RTX 4060 (RT + DLSS)
2. **1440p сбалансированно** → RX 9060 XT (16GB!) или RTX 5060 Ti 16GB
3. **1440p Ultra / RT** → RTX 5070 или RX 9070
4. **4K High / AI 32GB** → RTX 5090 (единственный выбор для LLM 32GB)
5. **Киберспорт 1080p 240Hz+** → RX 7600 или RTX 5060

## Связи

- Требования к PSU → `../psu/`
- PCIe-версия → `../../concepts/pcie-lanes.md`
- Бюджет мощности → `../../concepts/power-budget.md`
