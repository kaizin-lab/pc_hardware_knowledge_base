---
id: "psu-index"
type: "index"
title: "Блоки питания"
status: "draft"
last_updated: "2026-06-03"
---

# Блоки питания (PSU)

Актуальный стандарт — ATX 3.0/3.1 с 12V-2x6 для NVIDIA RTX 50xx. Все современные PSU — с активным PFC и DC-DC.

## Карта

- `deepcool-pf650.md` — Deepcool PF650 — 650W — ATX 2.4 — 80 Plus Bronze — ~6 000 ₽
- `deepcool-pn750d.md` — Deepcool PN750D — 750W — ATX 3.1 — 80 Plus Gold — ~9 300 ₽
- `deepcool-pn850d.md` — Deepcool PN850D — 850W — ATX 3.1 — 80 Plus Gold — ~12 000 ₽
- `fsp-hydro-ptm-x-pro-1000w.md` — FSP Hydro PTM X Pro — 1000W — ATX 3.1 — 80 Plus Platinum — ~20 000 ₽

## Профили PSU

- **`atx_2x_budget_reliable`** — ATX 2.4, бюджетные Bronze-блоки. Для систем без мощных GPU (TGP < 200W). Риск: transient spike → OCP → выключение.
- **`atx_3x_transient_capable`** — ATX 3.1, Gold/Platinum. Держат пиковые нагрузки современных GPU. 12V-2x6 native.

## Что ещё нужно заполнить

- SFX: компактные корпуса

## Связи

- Бюджет мощности → `../../concepts/power-budget.md`
- Требования GPU → `../gpu/`
- Совместимость с корпусами → `../case/`
