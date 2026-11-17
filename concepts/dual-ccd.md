---
id: "dual-ccd"
type: "concept"
title: "Multi-CCD и межкристальная задержка"
status: "draft"
last_updated: "2026-06-03"
links:
  cpu_index: "catalog/cpu/index.md"
  profiles: "concepts/epistemological-profiles.md"
---

# Multi-CCD и межкристальная задержка

AMD собирает потребительские CPU из нескольких вычислительных кристаллов (CCD)
и одного I/O-кристалла. Это позволяет масштабировать число ядер, но добавляет
межкристальную задержку.

## Что это значит на практике

- Внутри одного CCD ядра общаются быстро.
- Переход между CCD идёт через Infinity Fabric: задержка достигает десятков
  наносекунд.
- Планировщик ОС не всегда знает, какой поток важнее. Активная игра может
  «переехать» на другой CCD и получить frametime spike.
- В рендере и компиляции это почти не заметно: важна суммарная пропускная
  способность, а не задержка одного потока.

## Примеры

- Ryzen 9 7900/7950X — два CCD, 12–16 ядер.
- Ryzen 9 9900X/9950X — два CCD, Zen 5.
- Ryzen 7 7800X3D/9800X3D — один CCD с 3D V-Cache, поэтому хороши в играх.

## Связи

- CPU → [`../catalog/cpu/index.md`](../catalog/cpu/index.md)
- 3D V-Cache → [`3d-v-cache.md`](3d-v-cache.md)
- Профили → [`epistemological-profiles.md`](epistemological-profiles.md)
