---
id: "hybrid-architecture"
type: "concept"
title: "Гибридная архитектура Intel: P-ядра и E-ядра"
status: "draft"
last_updated: "2026-06-03"
links:
  cpu_index: "catalog/cpu/index.md"
  profiles: "concepts/epistemological-profiles.md"
---

# Гибридная архитектура Intel: P-ядра и E-ядра

Начиная с 12-го поколения Intel использует два типа ядер в одном CPU:

- **P-ядра** (Performance) — высокая частота, SMT, лучше в играх и
  latency-чувствительных задачах.
- **E-ядра** (Efficient) — меньше площадь и энергопотребление, лучше в
  многопоточном фоне и задачах, где важна пропускная способность на ватт.

## Что это значит на практике

- В играх активный поток должен попадать на P-ядро. Планировщик Windows это
  учитывает, но не идеально.
- Фоновые задачи и стриминг хорошо ложатся на E-ядра.
- В старых играх и ПО с плохим знанием топологии возможны просадки.
- Для рендера и компиляции гибридная схема работает хорошо: больше потоков на
  том же теплопакете.

## Где встречается

- Intel Core 12–14 gen (Alder Lake, Raptor Lake).
- Intel Core Ultra 200S (Arrow Lake) — Lion Cove + Skymont.

## Связи

- CPU → [`../catalog/cpu/index.md`](../catalog/cpu/index.md)
- Профили → [`epistemological-profiles.md`](epistemological-profiles.md)
