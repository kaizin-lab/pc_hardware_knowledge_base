---
id: "intents-root"
type: "index"
title: "Каталог интентов PCBO"
status: "draft"
last_updated: "2026-06-03"
links:
  profiles_dictionary: "concepts/epistemological-profiles.md"
  modifiers_catalog: "concepts/modifiers.md"
---

# Каталог интентов PCBO

**Навигационная карта** — 5 полярных интентов, покрывающих все технологические домены.
Каждый интент — формальный YAML-файл, определяющий граничные условия и профильные
требования для синтеза сборки ПК.

## ⚠️ ДИРЕКТИВА ДЛЯ LLM-АГЕНТА

При встрече ссылки вида **`path/to/file.md#section-name`** в YAML-файлах интентов:

1. **Загрузи** указанный файл через read_file
2. **Найди** секцию `## section-name` или `### section-name` в файле
3. **Извлеки** определение профиля/концепта: steel-man, failure-mode, intents
4. **Не выполняй расчёты или выбор компонентов без загрузки конкретики из файла по ссылке**

Физический путь ведёт к реальному .md-файлу в репозитории `pc_hardware_knowledge_base/`.
Это не абстрактный URI — это navigable reference.

**Пример:** `concepts/epistemological-profiles.md#cache_dominant_gaming`
→ read_file("concepts/epistemological-profiles.md") → найти `## cache_dominant_gaming` → извлечь steel_man_desc, failure_mode_desc, optimal_for_intents, failure_for_intents.

## Карта интентов

| Интент | Домен | Файл | Ключевое ограничение |
|---|---|---|---|
| Киберспорт 360Hz | A: Гейминг | `esports_competitive_360hz.yaml` | CPU frame time, 3D V-Cache mandatory |
| AAA 4K Unrestricted | A: Гейминг | `aaa_gaming_4k_unrestricted.yaml` | VRAM ≥16GB, 256-bit bus minimum |
| AI Inference Local | B: Compute | `ai_inference_local_pro.yaml` | VRAM ≥12GB, тензорные ядра |
| Data Engineering | B: Compute | `data_engineering_spark_local.yaml` | RAM ≥64GB, DRAM SSD mandatory |
| SFF Compact Portable | C: Physical | `sff_compact_itx_portable.yaml` | SFX PSU, GPU ≤320mm, cooler ≤155mm |

## Как использовать

1. **Загрузи** YAML-файл интента
2. **Пройди по ссылкам** в `profile_interaction_matrix.mandatory_steel_man_profiles` и `strict_block_failure_profiles` — каждая ссылка ведёт к физическому .md-файлу
3. **Извлеки constraints** — максимальный шум, термальное состояние, минимальный объём RAM/Storage
4. **Примени MAUT-веса** для многокритериального ранжирования компонентов
5. **Вызови Python-навыки** (`evaluate_profiles.py`, `validate_physical_constraints.py`) для детерминированной проверки

## Связи

- **Профили компонентов:** `../concepts/epistemological-profiles.md` — полный словарь из 26 профилей с steel-man/failure-mode
- **Модификаторы:** `../concepts/modifiers.md` — каталог модификаторов для конструирования производных профилей
- **Физические стереотипы:** проверяются через `scripts/validate_physical_constraints.py`
