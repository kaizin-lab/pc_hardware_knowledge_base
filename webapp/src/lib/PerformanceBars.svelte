<script>
  import { base } from '$app/paths';
  import { bySlug } from '$lib/kb.js';

  let { component, performance } = $props();

  let mode = $state('perf');
  let selectedId = $state('r23_multi');

  const fmt = (value) => new Intl.NumberFormat('ru-RU').format(Math.round(value));

  let workloads = $derived.by(() => {
    if (!performance?.workloads) return [];
    const list = [...performance.workloads];

    const multi = performance.workloads.find((workload) => workload.id === 'r23_multi');
    if (multi) {
      const values = multi.values
        .map((item) => {
          const target = bySlug.get(item.slug);
          const power = target?.norm?.tdpW;
          return power ? { slug: item.slug, value: item.value / power } : null;
        })
        .filter(Boolean);
      if (values.length) {
        list.push({
          id: 'efficiency',
          label: 'R23 multi / W',
          unit: 'pts/W',
          higherIsBetter: true,
          values,
          derived: true
        });
      }
    }
    return list;
  });

  let selected = $derived(workloads.find((workload) => workload.id === selectedId) || workloads[0]);
  let currentHasData = $derived(
    workloads.some((workload) => workload.values.some((item) => item.slug === component.slug))
  );

  let rows = $derived.by(() => {
    if (!selected) return [];
    const values = selected.values
      .map((item) => {
        const target = bySlug.get(item.slug);
        return target ? { ...item, target, price: target.price } : null;
      })
      .filter(Boolean);
    if (!values.length) return [];

    const best = selected.higherIsBetter
      ? Math.max(...values.map((item) => item.value))
      : Math.min(...values.map((item) => item.value));

    let scored = values.map((item) => ({
      ...item,
      score: selected.higherIsBetter ? (item.value / best) * 100 : (best / item.value) * 100,
      display: `${fmt(item.value)} ${selected.unit}`
    }));

    if (mode === 'value') {
      scored = scored
        .filter((item) => item.price)
        .map((item) => {
          const valueIndex = (item.score / item.price) * 1000;
          return {
            ...item,
            rawValueIndex: valueIndex,
            display: `${valueIndex.toFixed(2)} инд./1000 ₽`
          };
        });
      const max = Math.max(...scored.map((item) => item.rawValueIndex), 1);
      scored = scored.map((item) => ({ ...item, score: (item.rawValueIndex / max) * 100 }));
    }

    return scored.sort((a, b) => b.score - a.score);
  });

  let currentRow = $derived(rows.find((row) => row.slug === component.slug));

  let summary = $derived.by(() => {
    return workloads
      .map((workload) => {
        const current = workload.values.find((item) => item.slug === component.slug);
        if (!current) return null;
        const best = workload.higherIsBetter
          ? Math.max(...workload.values.map((item) => item.value))
          : Math.min(...workload.values.map((item) => item.value));
        const score = workload.higherIsBetter
          ? (current.value / best) * 100
          : (best / current.value) * 100;
        return { label: workload.label, score };
      })
      .filter(Boolean)
      .sort((a, b) => b.score - a.score);
  });
</script>

{#if !performance || !workloads.length || !currentHasData}
  <div class="empty">Для этого компонента пока нет сравнимых данных по производительности.</div>
{:else}
  <div class="panel">
    <div class="panel-title">
      <h2>Производительность</h2>
      <span class="panel-meta">100 = лучший в выборке</span>
    </div>

    {#if summary.length}
      <div class="perf-summary">
        {#if summary.length > 1}
          <span>Сильнее всего: <strong>{summary[0].label}</strong> — {summary[0].score.toFixed(0)}/100</span>
          <span>Слабее всего: <strong>{summary[summary.length - 1].label}</strong> — {summary[summary.length - 1].score.toFixed(0)}/100</span>
        {:else}
          <span>Данные есть только для одной нагрузки.</span>
        {/if}
        {#if currentRow}
          <span>Место: <strong>{rows.indexOf(currentRow) + 1}</strong> из {rows.length}</span>
        {/if}
      </div>
    {/if}

    <div class="perf-controls">
      <div class="chips">
        {#each workloads as workload}
          <button
            class="chip"
            class:active={selectedId === workload.id}
            onclick={() => (selectedId = workload.id)}
          >
            {workload.label}
          </button>
        {/each}
      </div>
      <div class="chips">
        <button class="chip" class:active={mode === 'perf'} onclick={() => (mode = 'perf')}>индекс</button>
        <button class="chip" class:active={mode === 'value'} onclick={() => (mode = 'value')}>
          цена / производительность
        </button>
      </div>
    </div>

    {#if !currentRow}
      <div class="empty" style="padding:18px;margin-bottom:12px">
        {mode === 'value'
          ? 'У этого компонента нет цены — сравнение по цене недоступно.'
          : 'У этого компонента нет данных для выбранной нагрузки.'}
      </div>
    {/if}

    <div class="bars">
      {#each rows as row}
        <a
          class="bar-row"
          class:current={row.slug === component.slug}
          href="{base}/catalog/{row.slug}/"
          title={row.target.title}
        >
          <span class="bar-name">{row.target.title}</span>
          <span class="bar-track">
            <span class="bar-fill" style="width:{Math.max(row.score, 1)}%"></span>
          </span>
          <span class="bar-value">{row.display}</span>
        </a>
      {/each}
    </div>

    <div class="panel-meta" style="margin-top:14px">
      {#if mode === 'value'}
        100 = лучшая отдача на 1000 ₽ в этой выборке.
      {:else}
        100 = лучший результат в этой выборке. Это относительный индекс, не абсолютный FPS.
      {/if}
      {#if selected?.derived}
        Эффективность считается как R23 multi / TDP из карточки.
      {/if}
      Источник: {performance.source}. Снимок: {performance.asOf}.
    </div>
  </div>
{/if}
