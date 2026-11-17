<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import { components, counts, formatPrice, keyLine, TYPE_LABELS } from '$lib/kb.js';

  const typeOrder = ['cpu', 'gpu', 'motherboard', 'memory', 'storage', 'psu', 'cooling', 'case', 'audio_interface'];

  let q = $state('');
  let type = $state('all');
  let status = $state('all');
  let vendor = $state('all');

  const vendors = [...new Set(components.map((component) => component.vendor))].sort((a, b) =>
    a.localeCompare(b, 'ru')
  );

  let filtered = $derived.by(() => {
    const query = q.trim().toLowerCase();
    return components.filter((component) => {
      if (type !== 'all' && component.type !== type) return false;
      if (status !== 'all' && component.status !== status) return false;
      if (vendor !== 'all' && component.vendor !== vendor) return false;
      if (!query) return true;
      const haystack = [component.title, component.vendor, component.type, ...(component.tags || [])]
        .join(' ')
        .toLowerCase();
      return haystack.includes(query);
    });
  });

  onMount(() => {
    const initial = new URLSearchParams(location.search).get('type');
    if (initial && initial !== 'all') type = initial;
  });
</script>

<svelte:head>
  <title>Каталог — PCBO KB</title>
</svelte:head>

<div class="page-head">
  <div>
    <div class="eyebrow">Catalog</div>
    <h1 style="font-size:clamp(32px,4vw,48px)">Каталог компонентов</h1>
    <p>Спецификации, профили и ограничения. Фильтруйте по типу, статусу и вендору.</p>
  </div>
  <span class="panel-meta">{filtered.length} / {components.length}</span>
</div>

<div class="toolbar">
  <div class="field">
    <label for="q">Поиск</label>
    <input id="q" class="input search" bind:value={q} placeholder="5070, AM5, DDR5…" />
  </div>
  <div class="field">
    <label for="status">Статус</label>
    <select id="status" class="select" bind:value={status}>
      <option value="all">Все</option>
      <option value="verified">verified</option>
      <option value="draft">draft</option>
    </select>
  </div>
  <div class="field">
    <label for="vendor">Вендор</label>
    <select id="vendor" class="select" bind:value={vendor}>
      <option value="all">Все</option>
      {#each vendors as item}
        <option value={item}>{item}</option>
      {/each}
    </select>
  </div>
</div>

<div class="chips" style="margin-bottom:18px">
  <button class="chip" class:active={type === 'all'} onclick={() => (type = 'all')}>все</button>
  {#each typeOrder as item}
    {#if counts.byType[item]}
      <button class="chip" class:active={type === item} onclick={() => (type = item)}>
        {TYPE_LABELS[item]} · {counts.byType[item]}
      </button>
    {/if}
  {/each}
</div>

{#if filtered.length}
  <div class="card-grid">
    {#each filtered as component}
      <a class="card" href="{base}/catalog/{component.slug}/">
        <div class="card-top">
          <span class="type">{component.typeLabel}</span>
          <span class="status {component.status}">{component.status}</span>
        </div>
        <h3>{component.title}</h3>
        {#if keyLine(component)}<div class="card-specs">{keyLine(component)}</div>{/if}
        <div class="card-tags">
          {#each component.tags.slice(0, 4) as tag}
            <span class="tag">{tag}</span>
          {/each}
        </div>
        <div class="card-meta">
          <span>{component.vendor}</span>
          <span class="card-price">{component.price ? formatPrice(component.price) : 'цена —'}</span>
        </div>
      </a>
    {/each}
  </div>
{:else}
  <div class="empty">Ничего не найдено. Попробуйте другой запрос или сбросьте фильтры.</div>
{/if}
