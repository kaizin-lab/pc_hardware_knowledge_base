#!/usr/bin/env node
/**
 * Build the web app dataset from the Markdown/YAML knowledge base.
 * Run from webapp/: `node scripts/build-data.mjs`
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'js-yaml';
import { marked } from 'marked';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WEBAPP = path.resolve(__dirname, '..');
const ROOT = path.resolve(WEBAPP, '..');
const CATALOG = path.join(ROOT, 'catalog');
const OUT = path.join(WEBAPP, 'src', 'lib', 'data', 'kb.json');
const REPO_URL = 'https://github.com/kaizin-lab/pc_hardware_knowledge_base';
const EXCLUDED_SLUGS = new Set(['amd-ryzen-7000']);
const OVERVIEW_SLUGS = new Set(['ddr5']);

const COMPONENT_TYPES = new Set([
  'cpu',
  'gpu',
  'motherboard',
  'memory',
  'storage',
  'psu',
  'cooling',
  'case',
  'audio_interface'
]);

const TYPE_LABELS = {
  cpu: 'Процессор',
  gpu: 'Видеокарта',
  motherboard: 'Материнская плата',
  memory: 'Память',
  storage: 'Накопитель',
  psu: 'Блок питания',
  cooling: 'Охлаждение',
  case: 'Корпус',
  audio_interface: 'Аудиоинтерфейс'
};

const TYPE_ORDER = ['cpu', 'gpu', 'motherboard', 'memory', 'storage', 'psu', 'cooling', 'case', 'audio_interface'];

const INTENTS = [
  { id: 'esports_1080p_240hz', label: 'Киберспорт 1080p / 240 Hz', domain: 'Гейминг' },
  { id: 'esports_1080p_360hz', label: 'Киберспорт 1080p / 360 Hz', domain: 'Гейминг' },
  { id: 'aaa_1080p_ultra', label: 'AAA 1080p ultra', domain: 'Гейминг' },
  { id: 'aaa_1440p_high', label: 'AAA 1440p high', domain: 'Гейминг' },
  { id: 'aaa_4k_ultra', label: 'AAA 4K ultra', domain: 'Гейминг' },
  { id: 'aaa_4k_path_tracing', label: 'AAA 4K path tracing', domain: 'Гейминг' },
  { id: 'llm_inference_7b', label: 'Локальный LLM 7B', domain: 'AI / ML' },
  { id: 'llm_inference_13b', label: 'Локальный LLM 13B', domain: 'AI / ML' },
  { id: 'llm_inference_20b', label: 'Локальный LLM 20B+', domain: 'AI / ML' },
  { id: 'llm_training_lora', label: 'LoRA-файнтюнинг', domain: 'AI / ML' },
  { id: 'stable_diffusion', label: 'Stable Diffusion', domain: 'AI / ML' },
  { id: 'ai_upscaling', label: 'AI-апскейлинг', domain: 'AI / ML' },
  { id: 'heavy_compilation', label: 'Тяжёлая компиляция', domain: 'Продуктивность' },
  { id: '3d_rendering_cpu', label: '3D-рендер на CPU', domain: 'Продуктивность' },
  { id: '3d_rendering_gpu', label: '3D-рендер на GPU', domain: 'Продуктивность' },
  { id: 'video_editing_4k', label: 'Видеомонтаж 4K', domain: 'Продуктивность' },
  { id: 'video_editing_8k', label: 'Видеомонтаж 8K', domain: 'Продуктивность' },
  { id: 'scientific_computing', label: 'Научные расчёты', domain: 'Продуктивность' },
  { id: 'data_engineering', label: 'Data engineering', domain: 'Продуктивность' },
  { id: 'software_development', label: 'Разработка ПО', domain: 'Продуктивность' },
  { id: 'office_productivity', label: 'Офисные задачи', domain: 'Продуктивность' },
  { id: 'silent_build', label: 'Тихая сборка', domain: 'Операции' },
  { id: 'sff_build', label: 'Компактная SFF-сборка', domain: 'Операции' },
  { id: 'home_server_24_7', label: 'Домашний сервер 24/7', domain: 'Операции' },
  { id: 'streaming', label: 'Стриминг', domain: 'Операции' },
  { id: 'virtualization', label: 'Виртуализация', domain: 'Операции' }
];

const LINK_LABELS = {
  platform: 'Платформа',
  socket: 'Сокет',
  memory_type: 'Память',
  family: 'Семейство',
  concept_power: 'Питание',
  concept_pcie: 'PCIe',
  concept_vrm: 'VRM',
  concept_acoustic: 'Акустика',
  concept_memory: 'Тайминги',
  concepts: 'Концепты',
  competitor_intel: 'Конкурент Intel',
  competitor_amd: 'Конкурент AMD',
  competitor_nvidia: 'Конкурент NVIDIA',
  competitors: 'Конкуренты',
  chipset_spec: 'Чипсет',
  chipset_concept: 'Чипсет',
  up_variant: 'Старшая версия',
  down_variant: 'Младшая версия',
  next_gen: 'Следующее поколение',
  driver_taxonomy: 'Драйверы',
  dpc_concept: 'DPC latency'
};

function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else if (entry.name.endsWith('.md') && entry.name !== 'index.md') out.push(full);
  }
  return out;
}

function parseFrontmatter(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) return null;
  try {
    return { data: yaml.load(match[1]) || {}, body: text.slice(match[0].length) };
  } catch {
    return null;
  }
}

function firstNumber(value) {
  if (value === null || value === undefined) return null;
  const match = String(value).match(/(\d+(?:[.,]\d+)?)/);
  return match ? Number(match[1].replace(',', '.')) : null;
}

function watts(...values) {
  for (const value of values) {
    if (value === null || value === undefined) continue;
    const match = String(value).match(/(\d+(?:[.,]\d+)?)\s*(?:W|Вт)/i);
    if (match) return Number(match[1].replace(',', '.'));
    const n = Number(value);
    if (Number.isFinite(n) && n > 0) return n;
  }
  return null;
}

function list(value) {
  if (Array.isArray(value)) return value.map(String);
  if (typeof value === 'string') {
    return value
      .split(/[;,/]/)
      .map((x) => x.trim())
      .filter(Boolean);
  }
  return [];
}

function normSocket(value) {
  const text = String(value ?? '').toUpperCase();
  for (const socket of ['AM5', 'AM4', 'LGA1851', 'LGA1700', 'LGA1200', 'LGA1151']) {
    if (text.includes(socket)) return socket;
  }
  return null;
}

function normMemory(...values) {
  const text = values.flat().filter(Boolean).join(' ').toUpperCase();
  if (text.includes('DDR5')) return 'DDR5';
  if (text.includes('DDR4')) return 'DDR4';
  return null;
}

function normForm(value) {
  const text = String(value ?? '').toUpperCase();
  if (text.includes('E-ATX')) return 'E-ATX';
  if (text.includes('MICRO') || text.includes('M-ATX') || text.includes('MATX')) return 'mATX';
  if (text.includes('MINI') || text === 'ITX' || text.includes('MINI-ITX')) return 'ITX';
  if (text.includes('ATX')) return 'ATX';
  return null;
}

function parseConnectors(value) {
  const text = String(value ?? '').toLowerCase();
  const eight = Number((text.match(/(\d+)\s*[×x]\s*8[- ]?pin/) || [])[1] || (text.includes('8-pin') ? 1 : 0));
  const twelve = /12v|12vhpwr|16-pin/.test(text);
  const alternative = /или|aib|на ряде|опционально/.test(text);
  return { eight, twelve, alternative };
}

function numbersIn(value) {
  if (Array.isArray(value)) return value.flatMap(numbersIn);
  return [...String(value ?? '').matchAll(/(\d+)/g)].map((match) => Number(match[1]));
}

function formatValue(value) {
  if (value === null || value === undefined || value === '') return '—';
  if (Array.isArray(value)) return value.join(', ');
  if (typeof value === 'object') {
    return Object.entries(value)
      .map(([key, item]) => `${key}: ${formatValue(item)}`)
      .join(' · ');
  }
  return String(value);
}

function rewriteLinks(html, sourcePath) {
  return html.replace(/href="([^"]+)"/g, (full, href) => {
    if (/^(https?:|mailto:|#|\/)/.test(href)) return full;
    const [target, hash] = href.split('#');
    if (!/\.(md|ya?ml)$/i.test(target)) return full;
    const absolute = path.posix.normalize(path.posix.join(path.posix.dirname(sourcePath), target));
    return `href="${REPO_URL}/blob/main/${absolute}${hash ? `#${hash}` : ''}"`;
  });
}

function normalize(data) {
  const specs = data.specs || {};
  const type = data.type;

  const sockets = list(specs.sockets || specs.socket)
    .map(normSocket)
    .filter(Boolean);

  const memoryType =
    type === 'memory'
      ? normMemory(specs.type, specs.standard, specs.speed, data.title)
      : normMemory(specs.memory, specs.max_ram, specs.ram, data.title);

  const caseForms = list(specs.motherboard_support || specs.form_factors || specs.mb_support)
    .map(normForm)
    .filter(Boolean);

  return {
    socket: normSocket(specs.socket || specs.platform),
    sockets,
    memoryType,
    tdpW: watts(specs.tdp, specs.tdp_w, specs.tbp, specs.tgp, specs.ppt),
    psuW: watts(specs.wattage, specs.wattage_w, specs.power),
    psuAtx3: /ATX\s*3/i.test(String(specs.standard || specs.atx_version || '')),
    formFactor: normForm(specs.form_factor),
    caseForms,
    coolerHeightMm: firstNumber(specs.height_mm),
    caseCoolerMaxMm: firstNumber(specs.max_cooler_height_mm ?? specs.max_cooler_mm),
    gpuLengthMm: firstNumber(specs.length_mm ?? specs.length),
    caseGpuMaxMm: firstNumber(specs.max_gpu_length_mm ?? specs.max_gpu_mm),
    ramCapacityGb: firstNumber(specs.capacity_gb ?? specs.capacity),
    capacityGb: firstNumber(specs.capacity_gb ?? specs.capacity),
    ramSpeedMt: firstNumber(specs.speed_mt ?? specs.speed_mts ?? specs.speed),
    m2Slots: firstNumber(specs.m2_slots),
    layoutType: String(specs.layout_type || specs.type || '').toLowerCase(),
    connectors: parseConnectors(specs.power_connector),
    coolerTdp: watts(specs.tdp_rating_w),
    radiatorMm: firstNumber(specs.radiator_size),
    caseRadiatorMm: Math.max(0, ...numbersIn(specs.radiator_support)),
    psuLengthMm: firstNumber(specs.length_mm),
    casePsuMaxMm: firstNumber(specs.max_psu_length_mm),
    coolerRamClearanceMm: firstNumber(specs.ram_clearance_mm),
    ramHeightMm: firstNumber(specs.height),
    psu8pin: firstNumber(specs.pcie_8pin_count),
    psu12v: Boolean(specs['12v_2x6']),
    mbBifurcation: Boolean(specs.bifurcation_risk)
  };
}

function linkList(links, sourcePath, byPath) {
  const out = [];
  if (!links || typeof links !== 'object') return out;

  for (const [key, raw] of Object.entries(links)) {
    const values = Array.isArray(raw) ? raw : [raw];
    for (const value of values) {
      if (typeof value !== 'string') continue;
      if (/^(https?:|mailto:|pcbo:)/.test(value)) {
        out.push({ label: LINK_LABELS[key] || key, url: value });
        continue;
      }
      const target = path.posix.normalize(value.replace(/^\.\//, ''));
      const linked = byPath.get(target);
      if (linked) {
        out.push({ label: LINK_LABELS[key] || key, slug: linked.slug });
      } else {
        out.push({ label: LINK_LABELS[key] || key, url: `${REPO_URL}/blob/main/${target}` });
      }
    }
  }
  return out;
}

function main() {
  const files = walk(CATALOG);
  const components = [];
  const byPath = new Map();

  for (const file of files) {
    const sourcePath = path.relative(ROOT, file).split(path.sep).join('/');
    const parsed = parseFrontmatter(fs.readFileSync(file, 'utf8'));
    if (!parsed) continue;
    const { data, body } = parsed;
    if (!COMPONENT_TYPES.has(data.type)) continue;

    const slug = data.id || path.basename(file, '.md');
    if (EXCLUDED_SLUGS.has(slug)) continue;
    const profiles = Object.entries(data.profiles || {}).map(([name, profile]) => ({
      name,
      optimal: profile.optimal_for_intents || [],
      failure: profile.failure_for_intents || [],
      severity: profile.failure_severity || 'WARN',
      steel: profile.steel_man_desc || '',
      failureMode: profile.failure_mode_desc || '',
      capability: profile.capability_level ?? null
    }));

    const specs = Object.entries(data.specs || {})
      .filter(([key]) => !['engineering_notes'].includes(key))
      .map(([key, value]) => ({ key, value: formatValue(value) }));

    let html = marked.parse(body);
    html = rewriteLinks(html, sourcePath);
    html = html.replace(/<h1[^>]*>[\s\S]*?<\/h1>/, '');

    const component = {
      slug,
      selectable: !OVERVIEW_SLUGS.has(slug),
      id: data.id || slug,
      type: data.type,
      typeLabel: TYPE_LABELS[data.type] || data.type,
      title: data.title || slug,
      vendor: data.vendor || '—',
      status: data.status || 'draft',
      tags: data.tags || [],
      lastUpdated: data.last_updated || null,
      price: data.price_ru?.median ?? null,
      priceMin: data.price_ru?.min ?? null,
      priceMax: data.price_ru?.max ?? null,
      priceSource: data.price_ru?.source ?? null,
      priceDate: data.price_ru?.date ?? null,
      specs,
      profiles,
      norm: normalize(data),
      bodyHtml: html,
      sourcePath,
      sourceUrl: `${REPO_URL}/blob/main/${sourcePath}`,
      links: []
    };

    components.push(component);
    byPath.set(sourcePath, component);
  }

  for (const component of components) {
    const parsed = parseFrontmatter(fs.readFileSync(path.join(ROOT, component.sourcePath), 'utf8'));
    component.links = linkList(parsed?.data?.links, component.sourcePath, byPath);
  }

  components.sort((a, b) => {
    const order = TYPE_ORDER.indexOf(a.type) - TYPE_ORDER.indexOf(b.type);
    return order || a.title.localeCompare(b.title, 'ru');
  });

  const byType = {};
  const statuses = {};
  let withProfiles = 0;
  const profileNames = new Set();
  for (const component of components) {
    byType[component.type] = (byType[component.type] || 0) + 1;
    statuses[component.status] = (statuses[component.status] || 0) + 1;
    if (component.profiles.length) withProfiles += 1;
    for (const profile of component.profiles) profileNames.add(profile.name);
  }

  const data = {
    generatedAt: new Date().toISOString(),
    repoUrl: REPO_URL,
    counts: {
      components: components.length,
      byType,
      statuses,
      withProfiles,
      profiles: profileNames.size
    },
    intents: INTENTS,
    components
  };

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(data), 'utf8');
  console.log(`wrote ${path.relative(WEBAPP, OUT)} (${components.length} components, ${INTENTS.length} intents)`);
}

main();
