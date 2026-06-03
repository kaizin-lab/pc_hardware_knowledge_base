---
id: "cpu-index"
type: "index"
title: "Процессоры"
status: "verified"
last_updated: "2025-06-03"
---

# Процессоры (CPU)

Актуальные процессоры для настольных ПК. Только последние поколения: Zen 4/5 (AM5) и Arrow Lake (LGA1851).

## Карта

### AMD AM5 — Zen 4 (Raphael)
| Файл | Модель | Ядер | TDP | iGPU | X3D | Цена (₽) |
|---|---|---|---|---|---|---|
| `amd-ryzen-5-7500f.md` | R5 7500F | 6C/12T | 65W | — | — | ~14 000 |
| `amd-ryzen-5-7600.md` | R5 7600 | 6C/12T | 65W | RDNA2 | — | ~17 500 |
| `amd-ryzen-5-7600x.md` | R5 7600X | 6C/12T | 105W | RDNA2 | — | ~18 800 |
| `amd-ryzen-7-7700.md` | R7 7700 | 8C/16T | 65W | RDNA2 | — | ~25 600 |
| `amd-ryzen-7-7700x.md` | R7 7700X | 8C/16T | 105W | RDNA2 | — | ~28 000 |
| `amd-ryzen-7-7800x3d.md` | R7 7800X3D | 8C/16T | 120W | RDNA2 | ✓ | ~37 600 |
| `amd-ryzen-9-7900.md` | R9 7900 | 12C/24T | 65W | RDNA2 | — | ~34 000 |
| `amd-ryzen-9-7950x.md` | R9 7950X | 16C/32T | 170W | RDNA2 | — | ~50 600 |

### AMD AM5 — Zen 5 (Granite Ridge)
| Файл | Модель | Ядер | TDP | iGPU | X3D | Цена (₽) |
|---|---|---|---|---|---|---|
| `amd-ryzen-5-9600x.md` | R5 9600X | 6C/12T | 65W | RDNA2 | — | ~23 800 |
| `amd-ryzen-7-9700x.md` | R7 9700X | 8C/16T | 65W | RDNA2 | — | ~32 400 |
| `amd-ryzen-7-9800x3d.md` | R7 9800X3D | 8C/16T | 120W | RDNA2 | ✓ | ~51 400 |

### Intel LGA1851 — Arrow Lake
| Файл | Модель | Ядер | TDP | iGPU | Цена (₽) |
|---|---|---|---|---|---|
| `intel-core-ultra-5-225f.md` | Ultra 5 225F | 10C/10T | 65W | — | ~19 500 |
| `intel-core-ultra-5-245k.md` | Ultra 5 245K | 14C/14T | 125W | Xe | ~28 000 |
| `intel-core-ultra-7-265f.md` | Ultra 7 265F | 20C/20T | 65W | — | ~33 500 |
| `intel-core-ultra-7-265k.md` | Ultra 7 265K | 20C/20T | 125W | Xe | ~39 300 |
| `intel-core-ultra-9-285k.md` | Ultra 9 285K | 24C/24T | 125W | Xe | ~57 400 |

### Обзорные
| Файл | Охват |
|---|---|
| `amd-ryzen-7000.md` | Обзор всей линейки Zen 4 — архитектура, IO die, Infinity Fabric |

## Как выбирать

1. **Бюджетный гейминг** → R5 7500F (нет iGPU, но дешевле всех) или Ultra 5 225F
2. **Киберспорт/max FPS** → 7800X3D или 9800X3D (3D V-Cache — король frametime)
3. **AI/рабочая станция** → R9 7950X (16 ядер) или Ultra 9 285K (24 ядра)
4. **Тихая сборка** → TDP 65W: R5 7600, R7 7700, R9 7900, Ultra 5 225F, Ultra 7 265F

## Связи

- Все AM5 → `../motherboard/am5/`
- Все LGA1851 → `../motherboard/lga1851/` (если создана)
- Память → `../memory/`
- Сквозной → `../../concepts/power-budget.md`
