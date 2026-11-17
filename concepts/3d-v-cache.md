---
id: "3d-v-cache"
type: "concept"
title: "3D V-Cache"
status: "draft"
last_updated: "2026-06-03"
links:
  cpu_index: "catalog/cpu/index.md"
  power: "concepts/power-budget.md"
  profiles: "concepts/epistemological-profiles.md"
---

# 3D V-Cache

Технология AMD, которая добавляет дополнительный кристалл L3-кэша поверх
вычислительного CCD. В потребительских CPU даёт 64 MB сверху — суммарно до
96 MB L3.

## Почему это важно для игр

Игры обращаются к памяти нерегулярно. Большой L3 снижает число промахов и
задержку доступа к DRAM. В киберспорте и симуляторах это даёт заметный прирост
1% Low FPS и уменьшает frametime spikes.

## Цена

- Дополнительный кэш-кристалл ухудшает теплоотвод.
- Из-за этого снижены boost-частоты и TJmax.
- В тяжёлом многопотоке X3D-версия может проигрывать обычной при равной цене.

## Где встречается

- Ryzen 7 7800X3D — Zen 4, 96 MB L3.
- Ryzen 7 9800X3D — Zen 5, 96 MB L3.

## Связи

- CPU → [`../catalog/cpu/index.md`](../catalog/cpu/index.md)
- Профили → [`epistemological-profiles.md`](epistemological-profiles.md)
- Питание и тепло → [`power-budget.md`](power-budget.md)
