<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import { assessBuild, decodeBuild, encodeBuild, STATUS_TEXT } from '$lib/compat.js';
  import { formatPrice } from '$lib/kb.js';

  const CHECKLIST = [
    'BIOS обновлён до версии с поддержкой выбранного CPU',
    'XMP/EXPO включён, память проверена memtest',
    'Кулер/радиатор закреплён, вентиляторы не задевают RAM и кожух',
    'GPU плотно сидит в слоте, фиксатор закрыт',
    'Питание GPU (8-pin / 12V-2x6) вставлено до щелчка',
    'M.2 закреплён, радиатор и термопрокладка установлены',
    'Проверены USB, аудио, Ethernet/Wi-Fi и фронт-панель',
    'Стресс-тест CPU и GPU 30 минут, температуры в норме',
    'Шум и температуры соответствуют ожиданиям клиента',
    'Клиент получил отчёт, памятку и условия гарантии'
  ];

  let state = $state({ selection: {}, intentId: 'aaa_1440p_high', budget: 150000, measurements: {} });
  let ready = $state(false);
  let checked = $state(CHECKLIST.map(() => false));

  onMount(() => {
    state = decodeBuild(location.search);
    ready = true;
  });

  let result = $derived(assessBuild(state.selection, state.intentId, state.budget, state.measurements));
  let hasBuild = $derived(Object.keys(state.selection).length > 0);
  let unknownChecks = $derived(result.checks.filter((check) => check.status === 'unknown'));
  let riskChecks = $derived(result.checks.filter((check) => check.status === 'fail' || check.status === 'warn'));
  let colors = { PASS: 'var(--green)', WARN: 'var(--amber)', FAIL: 'var(--red)' };
</script>

<svelte:head>
  <title>Отчёт о сборке — PCBO KB</title>
  <meta name="description" content="Отчёт о совместимости и рисках PC-сборки." />
</svelte:head>

{#if !ready}
  <div class="empty">Загрузка отчёта…</div>
{:else if !hasBuild}
  <div class="page-head">
    <div>
      <div class="eyebrow">Build report</div>
      <h1 style="font-size:clamp(32px,4vw,48px)">Отчёт о сборке</h1>
      <p>Сначала соберите конфигурацию в конструкторе, затем откройте отчёт.</p>
    </div>
  </div>
  <a class="btn primary" href="{base}/build/">Перейти в конструктор</a>
{:else}
  <div class="page-head no-print">
    <div>
      <div class="eyebrow">Build report / {state.intentId}</div>
      <h1 style="font-size:clamp(32px,4vw,48px)">Отчёт о сборке</h1>
      <p>
        Проверка совместимости, риски, полнота данных и чек-лист приёмки.
        Это инженерный отчёт, а не юридическая гарантия.
      </p>
    </div>
    <div class="actions" style="margin:0">
      <a class="btn" href="{base}/build/?{encodeBuild(state.selection, state.intentId, state.budget, state.measurements)}">← в конструктор</a>
      <button class="btn primary" onclick={() => window.print()}>Печать / PDF</button>
    </div>
  </div>

  <section class="verdict" style="--status:{colors[result.status]}; position:static; margin-bottom:14px">
    <div class="verdict-label">итоговый вердикт</div>
    <div class="verdict-status">{STATUS_TEXT[result.status]}</div>
    <div class="verdict-summary">
      {#if result.status === 'PASS'}
        Все известные проверки пройдены. Ниже — данные, которых не хватает для полной гарантии.
      {:else if result.status === 'WARN'}
        Сборка возможна, но есть замечания или не хватает данных. Их нужно закрыть до выдачи клиенту.
      {:else}
        Есть несовместимость. Меняйте компоненты или интент.
      {/if}
    </div>
    <div class="verdict-stats" style="max-width:560px">
      <div class="verdict-stat">
        <div class="v">{formatPrice(result.total)}</div>
        <div class="l">известная сумма</div>
      </div>
      <div class="verdict-stat">
        <div class="v">{result.estimatedPower ? `${result.estimatedPower} W` : '—'}</div>
        <div class="l">оценка нагрузки</div>
      </div>
      <div class="verdict-stat">
        <div class="v">{result.completeness.score}%</div>
        <div class="l">полнота данных</div>
      </div>
      <div class="verdict-stat">
        <div class="v">{riskChecks.length}</div>
        <div class="l">замечаний</div>
      </div>
    </div>
  </section>

  <div class="detail-grid">
    <div class="panel">
      <div class="panel-title">
        <h2>Состав сборки</h2>
        <span class="panel-meta">{result.bom.length} / 8</span>
      </div>
      <table class="spec-table">
        <tbody>
          {#each result.bom as item}
            <tr>
              <td>{item.label}</td>
              <td>{item.component.title}</td>
              <td style="text-align:right;white-space:nowrap">{formatPrice(item.component.price)}</td>
            </tr>
          {/each}
          <tr>
            <td><strong>Итого</strong></td>
            <td></td>
            <td style="text-align:right;white-space:nowrap"><strong>{formatPrice(result.total)}</strong></td>
          </tr>
        </tbody>
      </table>
      <div class="panel-meta" style="margin-top:12px">
        Интент: {state.intentId}. Бюджет: {formatPrice(state.budget)}.
      </div>
    </div>

    <div class="panel">
      <div class="panel-title">
        <h2>Полнота данных</h2>
        <span class="panel-meta">{result.completeness.known} / {result.completeness.total}</span>
      </div>
      <div class="meter"><span style="width:{result.completeness.score}%"></span></div>
      <div style="margin-top:10px;color:var(--muted);font-size:12px">
        {#if result.completeness.score === 100}
          Все обязательные поля заполнены. Это всё ещё не заменяет проверку BIOS, QVL и фактических размеров.
        {:else}
          Для полной гарантии не хватает данных. Чем ниже процент, тем больше ручной проверки.
        {/if}
      </div>
      {#if result.completeness.missing.length}
        <ul class="missing-list">
          {#each result.completeness.missing.slice(0, 12) as item}
            <li>{item}</li>
          {/each}
        </ul>
        {#if result.completeness.missing.length > 12}
          <div class="panel-meta">и ещё {result.completeness.missing.length - 12}…</div>
        {/if}
      {/if}
    </div>
  </div>

  <div class="panel" style="margin-top:14px">
    <div class="panel-title">
      <h2>Проверки</h2>
      <span class="panel-meta">{result.checks.length} пунктов</span>
    </div>
    <table class="check-table">
      <thead>
        <tr><th>Проверка</th><th>Статус</th><th>Детали</th></tr>
      </thead>
      <tbody>
        {#each result.checks as check}
          <tr>
            <td>{check.label}</td>
            <td>
              <span class="pill {check.status === 'fail' ? 'fail' : check.status === 'warn' ? 'warn' : check.status === 'unknown' ? 'skip' : 'pass'}">
                {check.status === 'fail' ? 'блок' : check.status === 'warn' ? 'warn' : check.status === 'unknown' ? 'нет данных' : 'ok'}
              </span>
            </td>
            <td>{check.detail}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  {#if riskChecks.length}
    <div class="panel" style="margin-top:14px">
      <div class="panel-title">
        <h2>Риски и что проверить</h2>
        <span class="panel-meta">{riskChecks.length}</span>
      </div>
      {#each riskChecks as check}
        <div class="profile">
          <div class="profile-name" style="color:{check.status === 'fail' ? 'var(--red)' : 'var(--amber)'}">
            {check.status === 'fail' ? 'BLOCK' : 'WARN'} · {check.label}
          </div>
          <p>{check.detail}</p>
          <div class="profile-tags"><span class="tag">{check.component}</span></div>
        </div>
      {/each}
    </div>
  {/if}

  <div class="panel" style="margin-top:14px">
    <div class="panel-title">
      <h2>Чек-лист сборки и приёмки</h2>
      <span class="panel-meta no-print">отмечайте перед выдачей</span>
    </div>
    <div class="checklist">
      {#each CHECKLIST as item, index}
        <label>
          <input
            type="checkbox"
            checked={checked[index]}
            onchange={(event) => (checked[index] = event.currentTarget.checked)}
          />
          <span>{item}</span>
        </label>
      {/each}
    </div>
  </div>

  {#if unknownChecks.length}
    <div class="panel" style="margin-top:14px">
      <div class="panel-title">
        <h2>Чего не хватает для гарантии</h2>
        <span class="panel-meta">{unknownChecks.length}</span>
      </div>
      <ul class="missing-list">
        {#each unknownChecks as check}
          <li><strong>{check.label}:</strong> {check.detail}</li>
        {/each}
      </ul>
    </div>
  {/if}

  <div class="panel disclaimer" style="margin-top:14px">
    <div class="panel-title"><h2>Границы отчёта</h2></div>
    <p>
      Отчёт основан на данных карточек и введённых вручную измерениях. Он проверяет
      только те поля, которые есть в базе, и не является юридической гарантией.
      Перед сборкой проверьте BIOS, QVL памяти, ревизию платы, фактические размеры
      корпуса и видеокарты, а также условия гарантии производителей.
    </p>
  </div>
{/if}
