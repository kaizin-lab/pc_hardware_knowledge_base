<script>
  import { base } from '$app/paths';
  import { formatPrice } from '$lib/kb.js';
  import PerformanceBars from '$lib/PerformanceBars.svelte';
  let { data } = $props();
  const component = data.component;
  const performance = data.performance;
  let tab = $state('overview');
  let hasPerformance = $derived(
    performance?.workloads.some((workload) =>
      workload.values.some((item) => item.slug === component.slug)
    )
  );
</script>

<svelte:head>
  <title>{component.title} — PCBO KB</title>
  <meta name="description" content={component.title + ' — спецификации и профили в базе PCBO.'} />
</svelte:head>

<div class="eyebrow">
  <a href="{base}/catalog/">← каталог</a> / {component.typeLabel}
</div>

<div class="detail-top">
  <div>
    <h1 style="font-size:clamp(30px,4vw,48px)">{component.title}</h1>
    <div class="detail-meta">
      <span class="status {component.status}">{component.status}</span>
      <span>{component.vendor}</span>
      <span>обновлено {component.lastUpdated || '—'}</span>
      {#if component.priceDate}<span>цена на {component.priceDate}</span>{/if}
    </div>
  </div>
  <div class="panel" style="text-align:right">
    <div class="panel-meta">median price</div>
    <div class="detail-price">{formatPrice(component.price)}</div>
    {#if component.priceSource}
      <div class="panel-meta" style="margin-top:6px">{component.priceSource}</div>
    {/if}
    <a class="btn ghost" style="margin-top:12px" href={component.sourceUrl} rel="noreferrer">исходник ↗</a>
  </div>
</div>

<div class="detail-tabs">
  <button class="tab" class:active={tab === 'overview'} onclick={() => (tab = 'overview')}>Обзор</button>
  {#if hasPerformance}
    <button class="tab" class:active={tab === 'performance'} onclick={() => (tab = 'performance')}>Производительность</button>
  {/if}
  <button class="tab" class:active={tab === 'profiles'} onclick={() => (tab = 'profiles')}>Профили</button>
</div>

{#if tab === 'overview'}
  <div class="detail-grid">
    <div class="panel">
      <div class="panel-title">
        <h2>Спецификации</h2>
        <span class="panel-meta">{component.specs.length} полей</span>
      </div>
      <table class="spec-table">
        <tbody>
          {#each component.specs as spec}
            <tr>
              <td>{spec.key.replaceAll('_', ' ')}</td>
              <td>{spec.value}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    {#if component.links.length}
      <div class="panel">
        <div class="panel-title">
          <h2>Связи</h2>
          <span class="panel-meta">{component.links.length}</span>
        </div>
        <div class="chips">
          {#each component.links as link}
            {#if link.slug}
              <a class="chip" href="{base}/catalog/{link.slug}/">{link.label}</a>
            {:else}
              <a class="chip" href={link.url} rel="noreferrer">{link.label} ↗</a>
            {/if}
          {/each}
        </div>
      </div>
    {/if}
  </div>

  <div class="panel" style="margin-top:14px">
    <div class="panel-title">
      <h2>Описание</h2>
      <span class="panel-meta">Markdown → HTML</span>
    </div>
    <div class="prose">{@html component.bodyHtml}</div>
  </div>
{:else if tab === 'performance'}
  <PerformanceBars {component} {performance} />
{:else}
  <div class="panel">
    <div class="panel-title">
      <h2>Профили</h2>
      <span class="panel-meta">{component.profiles.length}</span>
    </div>
    {#if component.profiles.length}
      {#each component.profiles as profile}
        <div class="profile">
          <div class="profile-name">{profile.name}</div>
          {#if profile.steel}<p>{profile.steel}</p>{/if}
          {#if profile.failureMode}<p style="color:var(--dim)">{profile.failureMode}</p>{/if}
          <div class="profile-tags">
            {#each profile.optimal as intent}
              <span class="tag" style="color:var(--green)">✓ {intent}</span>
            {/each}
            {#each profile.failure as intent}
              <span class="tag" style="color:var(--red)">✕ {intent}</span>
            {/each}
          </div>
        </div>
      {/each}
    {:else}
      <div class="panel-meta">Профилей пока нет — только спецификации.</div>
    {/if}
  </div>
{/if}
