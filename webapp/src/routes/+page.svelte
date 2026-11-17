<script>
  import { base } from '$app/paths';
  import { counts, intents, repoUrl } from '$lib/kb.js';
</script>

<svelte:head>
  <title>PCBO KB — база знаний о железе</title>
  <meta
    name="description"
    content="Файловая база знаний о PC-железе: карточки компонентов, профили поведения и конструктор сборки с проверкой совместимости."
  />
</svelte:head>

<section>
  <div class="eyebrow">PC Hardware Knowledge Base</div>
  <h1>Железо без<br /><span>галлюцинаций.</span></h1>
  <p class="lede">
    Карточки компонентов, профили поведения и детерминированная проверка сборки.
    Не «топ за свои деньги», а спецификации, ограничения и явные компромиссы.
  </p>
  <div class="actions">
    <a class="btn primary" href="{base}/build/">Собрать ПК</a>
    <a class="btn" href="{base}/catalog/">Открыть каталог</a>
    <a class="btn ghost" href={repoUrl} rel="noreferrer">Исходники на GitHub</a>
  </div>
</section>


<section class="stats" aria-label="Статистика базы">
  <div class="stat">
    <div class="stat-value">{counts.components}</div>
    <div class="stat-label">карточек компонентов</div>
  </div>
  <div class="stat">
    <div class="stat-value">{counts.profiles}</div>
    <div class="stat-label">профилей поведения</div>
  </div>
  <div class="stat">
    <div class="stat-value">{intents.length}</div>
    <div class="stat-label">интентов для проверки</div>
  </div>
  <div class="stat">
    <div class="stat-value">{counts.withProfiles}</div>
    <div class="stat-label">карточек с профилями</div>
  </div>
</section>

<section class="panel" style="margin-top:14px">
  <div class="panel-title">
    <h2>Как это работает</h2>
    <span class="panel-meta">без LLM в проверке</span>
  </div>
  <div class="steps">
    <div class="step">
      <div class="n">01 / DATA</div>
      <h3>Markdown + YAML</h3>
      <p>Карточки компонентов и концепты лежат в репозитории. При сборке они превращаются в JSON.</p>
    </div>
    <div class="step">
      <div class="n">02 / RULES</div>
      <h3>Детерминированные проверки</h3>
      <p>Сокет, тип памяти, форм-фактор, высота кулера, мощность БП и профили интента.</p>
    </div>
    <div class="step">
      <div class="n">03 / RESULT</div>
      <h3>PASS / WARN / FAIL</h3>
      <p>Каждое замечание объяснено. Неизвестные данные не считаются совместимыми.</p>
    </div>
  </div>
</section>



<section class="home-grid">
  <a class="feature" href="{base}/catalog/">
    <div class="num">01 / CATALOG</div>
    <h3>Каталог с фильтрами</h3>
    <p>{counts.components} карточек: процессоры, видеокарты, платы, память, БП, охлаждение, корпуса и аудиоинтерфейсы.</p>
  </a>
  <a class="feature" href="{base}/build/">
    <div class="num">02 / BUILD</div>
    <h3>Конструктор сборки</h3>
    <p>Выберите компоненты и интент. Проверка сокета, памяти, форм-фактора, высоты кулера, питания и профилей.</p>
  </a>
  <a class="feature" href="{base}/catalog/?type=cpu">
    <div class="num">03 / DATA</div>
    <h3>Markdown как источник</h3>
    <p>Все данные лежат в YAML frontmatter и обычном Markdown. Никакой отдельной CMS или базы данных.</p>
  </a>
</section>
