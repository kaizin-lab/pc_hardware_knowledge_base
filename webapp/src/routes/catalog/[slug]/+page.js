import kb from '$lib/data/kb.json';
import { error } from '@sveltejs/kit';

export function entries() {
  return kb.components.map((component) => ({ slug: component.slug }));
}

export function load({ params }) {
  const component = kb.components.find((item) => item.slug === params.slug);
  if (!component) throw error(404, 'Компонент не найден');
  return { component };
}
