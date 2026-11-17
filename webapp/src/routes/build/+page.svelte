<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { base } from '$app/paths';
  import { BUILD_CATEGORIES, bySlug, componentsOf, formatPrice, intents } from '$lib/kb.js';
  import { STATUS_TEXT, validateBuild } from '$lib/compat.js';

  const EMPTY = {
    cpu: '',
    motherboard: '',
    gpu: '',
    memory: '',
    storage: '',
    psu: '',
    cooling: '',
    case: ''
  };
  const STORAGE_KEY = 'pcbo-build-v1';

  const domains = [...new Set(intents.map((intent) => intent.domain))];

  let selection = $state({ ...EMPTY });
  let intentId = $state('aaa_1440p_high');
  let budget = $state(150000);
  let loaded = $state(false);

  let result = $derived(validateBuild(selection, intentId, budget));

  const colors = { PASS: 'var(--green)', WARN: 'var(--amber)', FAIL: 'var(--red)' };

  onMount(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (saved?.selection) selection = { ...EMPTY, ...saved.selection };
      if (saved?.intentId) intentId = saved.intentId;
      if (Number.isFinite(saved?.budget)) budget = saved.budget;
    } catch {
      // ignore malformed local state
    }
    loaded = true;
  });

  $effect(() => {
    if (!browser || !loaded) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ selection, intentId, budget }));
  });

  function reset() {
    selection = { ...EMPTY };
    intentId = 'aaa_1440p_high';
    budget = 150000;
  }

  function picked(key) {
    return selection[key] ? bySlug.get(selection[key]) : null;
  }
</script>

<svelte:head>
  <title>Конструктор сборки — PCBO KB</title>
  <meta
    name="description"
    content="Соберите ПК и проверьте совместимость: сокет, память, форм-фактор, охлаждение, питание и профили."
  />
</svelte:head>

<div class="page-head">
  <div>
    <div class="eyebrow">Build / compatibility</div>
    <h1 style="font-size:clamp(32px,4vw,48px)">Конструктор сборки</h1>
    <p>
      Выберите компоненты и интент. Проверка детерминированная: спецификации из карточек,
      без LLM и без «вероятно, совместимо».
    </p>
  </div>
  <span class="panel-meta">данные: Markdown + YAML</span>
</div>

<div class="build-layout">
  <div class="panel">
    <div class="panel-title">
      <h2>Конфигурация</h2>
      <button class="btn ghost" onclick={reset}>сбросить</button>
    </div>

    <div class="build-row">
      <div class="build-label">Интент<small>под какую задачу</small></div>
      <select class="select build-select" bind:value={intentId}>
        {#each domains as domain}
          <optgroup label={domain}>
            {#each intents.filter((intent) => intent.domain === domain) as intent}
              <option value={intent.id}>{intent.label}</option>
            {/each}
          </optgroup>
        {/each}
      </select>
    </div>

    {#each BUILD_CATEGORIES as category}
      {@const component = picked(category.key)}
      <div class="build-row">
        <div class="build-label">
          {category.label}
          <small>{category.hint}</small>
        </div>
        <div>
          <select
            class="select build-select"
            value={selection[category.key]}
            onchange={(event) => (selection[category.key] = event.currentTarget.value)}
          >
            <option value="">— не выбрано —</option>
            {#each componentsOf(category.type).filter((item) => item.selectable !== false) as item}
              <option value={item.slug}>
                {item.title}{item.price ? ` · ${formatPrice(item.price)}` : ''}
              </option>
            {/each}
          </select>
          {#if component}
            <div class="build-picked">
              <strong>{component.status}</strong> · {formatPrice(component.price)}
              {#if component.norm.socket} · {component.norm.socket}{/if}
              {#if component.norm.memoryType} · {component.norm.memoryType}{/if}
              · <a href="{base}/catalog/{component.slug}/">карточка ↗</a>
            </div>
          {/if}
        </div>
      </div>
    {/each}

    <div class="build-row">
      <div class="build-label">Бюджет<small>потолок, ₽</small></div>
      <input class="input" type="number" min="0" step="1000" bind:value={budget} />
    </div>
  </div>

  <aside>
    <div class="verdict" style="--status:{colors[result.status]}">
      <div class="verdict-label">итоговый вердикт</div>
      <div class="verdict-status">{STATUS_TEXT[result.status]}</div>
      <div class="verdict-summary">
        {#if result.status === 'PASS'}
          Блокирующих проблем не найдено. Проверьте предупреждения и данные, которых нет в карточках.
        {:else if result.status === 'WARN'}
          Сборка возможна, но есть замечания. Прочитайте их до покупки.
        {:else}
          Есть несовместимость. Поменяйте компоненты или интент.
        {/if}
      </div>

      <div class="verdict-stats">
        <div class="verdict-stat">
          <div class="v">{formatPrice(result.total)}</div>
          <div class="l">известная сумма</div>
        </div>
        <div class="verdict-stat">
          <div class="v">{result.estimatedPower ? `${result.estimatedPower} W` : '—'}</div>
          <div class="l">оценка нагрузки</div>
        </div>
        <div class="verdict-stat">
          <div class="v">{result.optimalCount}</div>
          <div class="l">optimal-профилей</div>
        </div>
        <div class="verdict-stat">
          <div class="v">{result.missing.length}</div>
          <div class="l">не хватает</div>
        </div>
      </div>

      <div class="issues">
        {#if result.issues.length === 0}
          <div class="empty" style="padding:18px">Проблем не найдено.</div>
        {:else}
          {#each result.issues as item}
            <div class="issue {item.severity}">
              <div class="issue-head">
                <span class="issue-title">{item.title}</span>
                <span class="issue-sev">{item.severity === 'fail' ? 'block' : item.severity === 'warn' ? 'warn' : 'info'}</span>
              </div>
              <div class="issue-detail">{item.detail}</div>
              <div class="issue-comp">{item.component}</div>
            </div>
          {/each}
        {/if}
      </div>
    </div>

    <div class="panel" style="margin-top:14px">
      <div class="panel-meta">
        Проверки: сокет, тип памяти, форм-фактор, сокет и высота кулера, длина GPU (если есть),
        мощность БП, ATX 3.x, профили интента и бюджет. Неизвестные поля не считаются
        совместимыми — они отмечаются отдельно.
      </div>
    </div>
  </aside>
</div>
