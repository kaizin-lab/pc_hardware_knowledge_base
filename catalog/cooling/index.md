---
id: "cooling-index"
type: "index"
title: "Охлаждение"
status: "draft"
last_updated: "2025-06-03"
---

# Охлаждение

## Типы

| Директория | Тип | Принцип | Целевые CPU |
|---|---|---|---|
| `air/` | Воздушное | Теплотрубки + радиатор + вентилятор(ы) | До 200W TDP |
| `liquid/` | Жидкостное (AIO) | Помпа + радиатор + вентиляторы | 150W+ TDP, эстетика |

## Что нужно заполнить

- **Air**: Deepcool AK620, Thermalright Peerless Assassin, Noctua NH-D15 — лучшие башни
- **Liquid**: Arctic Liquid Freezer III, Deepcool LT/LS — лучшие AIO по цене/производительности

## Связи

- Тепловые пакеты CPU → `../cpu/`
- Требования к корпусу (клиренс, поддержка радиаторов) → `../case/`
- Бюджет мощности (помпа AIO) → `../../concepts/power-budget.md`
