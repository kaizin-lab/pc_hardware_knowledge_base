# Web app

SvelteKit-приложение поверх базы знаний: каталог компонентов и конструктор
сборки с детерминированной проверкой совместимости.

## Локально

```bash
cd webapp
npm install
npm run dev
```

`npm run dev` сначала собирает `src/lib/data/kb.json` из `../catalog`, потом
запускает Vite.

## Сборка

```bash
npm run build
npm run preview
```

Статический сайт кладётся в `webapp/build`.

Для project pages нужен base path:

```bash
BASE_PATH=/pc_hardware_knowledge_base npm run build
```

## Данные

`scripts/build-data.mjs` читает Markdown-карточки из `../catalog`, парсит YAML
frontmatter и генерирует `src/lib/data/kb.json`.

Что попадает в приложение:

- карточки компонентов (CPU, GPU, платы, память, накопители, БП, охлаждение,
  корпуса, аудиоинтерфейсы);
- спецификации, профили, ссылки и Markdown-тело;
- нормализованные поля для проверок: сокет, тип памяти, TDP/TBP, форм-фактор,
  высота кулера, клиренс корпуса, мощность БП;
- 26 интентов для профильного матчинга.

`src/lib/data/kb.json` не коммитится: он генерируется перед `dev` и `build`.

## Проверки совместимости

`src/lib/compat.js` проверяет:

- сокет CPU ↔ материнская плата;
- тип памяти CPU/плата ↔ модуль;
- форм-фактор платы ↔ поддержка корпуса;
- сокет и высота кулера;
- длину GPU, если она заведена в карточку;
- мощность БП против оценки `CPU TDP + GPU TBP + 100 W`;
- ATX 3.x для GPU от 250 W;
- `optimal` / `failure` профили для выбранного интента;
- бюджет.

Нет данных — это не «совместимо»: приложение показывает `INFO` и не повышает
вердикт до `PASS`.

## Деплой

`.github/workflows/pages.yml` собирает приложение и публикует его через
GitHub Pages Actions.

В настройках репозитория:

**Settings → Pages → Source: GitHub Actions**

После пуша в `main` workflow соберёт сайт и задеплоит его на
`https://kaizin-lab.github.io/pc_hardware_knowledge_base/`.
