import raw from './data/kb.json';

export const components = raw.components;
export const intents = raw.intents;
export const counts = raw.counts;
export const repoUrl = raw.repoUrl;
export const generatedAt = raw.generatedAt;

export const bySlug = new Map(components.map((component) => [component.slug, component]));

export const TYPE_LABELS = {
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

export const BUILD_CATEGORIES = [
  { key: 'cpu', label: 'Процессор', type: 'cpu', hint: 'Сокет и TDP' },
  { key: 'motherboard', label: 'Материнская плата', type: 'motherboard', hint: 'Сокет, память, форма-фактор' },
  { key: 'gpu', label: 'Видеокарта', type: 'gpu', hint: 'TBP и профиль' },
  { key: 'memory', label: 'Память', type: 'memory', hint: 'DDR4 / DDR5' },
  { key: 'storage', label: 'Накопитель', type: 'storage', hint: 'NVMe' },
  { key: 'psu', label: 'Блок питания', type: 'psu', hint: 'Мощность и ATX 3.x' },
  { key: 'cooling', label: 'Охлаждение', type: 'cooling', hint: 'Сокет и высота' },
  { key: 'case', label: 'Корпус', type: 'case', hint: 'Форма-фактор и клиренс' }
];

export function componentsOf(type) {
  return components.filter((component) => component.type === type);
}

export function formatPrice(value) {
  if (value === null || value === undefined) return '—';
  return new Intl.NumberFormat('ru-RU').format(value) + ' ₽';
}

export function statusLabel(status) {
  return { draft: 'draft', review: 'review', verified: 'verified' }[status] || status;
}

export function keyLine(component) {
  const norm = component.norm || {};
  const bits = [];
  if (norm.socket) bits.push(norm.socket);
  if (component.type === 'motherboard' && norm.formFactor) bits.push(norm.formFactor);
  if (norm.memoryType) bits.push(norm.memoryType);
  if (component.type === 'psu' && norm.psuW) bits.push(norm.psuW + ' W');
  else if (component.type === 'memory' && norm.ramCapacityGb) bits.push(norm.ramCapacityGb + ' GB');
  else if (component.type === 'case' && norm.caseForms.length) bits.push(norm.caseForms.join('/'));
  else if (norm.tdpW) bits.push(norm.tdpW + ' W');
  return bits.slice(0, 3).join(' · ');
}
