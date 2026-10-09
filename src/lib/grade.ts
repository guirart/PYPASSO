import type { Exercise } from '@/content/types';
import { runPython } from './python/runner';

/** Resposta em andamento para cada tipo de exercício. */
export type Answer =
  | { k: 'choice'; selected: number | null; options: { v: string; ok: boolean }[] }
  | { k: 'fill'; bank: string[]; slots: (number | null)[] }
  | { k: 'order'; bank: number[]; seq: number[] }
  | { k: 'type'; text: string }
  | { k: 'code'; text: string }
  | { k: 'learn' };

export type Verdict = { ok: boolean; solution?: string; detail?: string; stdout?: string };

export const shuffle = <T,>(a: T[]): T[] => {
  const r = a.slice();
  for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; }
  return r;
};

export function initAnswer(ex: Exercise): Answer {
  switch (ex.k) {
    case 'mc': case 'out': return { k: 'choice', selected: null, options: shuffle(ex.o.map((v, i) => ({ v, ok: i === 0 }))) };
    case 'fill': return { k: 'fill', bank: shuffle(ex.b), slots: ex.a.map(() => null) };
    case 'order': {
      let bank: number[];
      do { bank = shuffle(ex.l.map((_, i) => i)); } while (ex.l.length > 1 && bank.every((v, i) => v === i));
      return { k: 'order', bank, seq: [] };
    }
    case 'type': return { k: 'type', text: '' };
    case 'code': return { k: 'code', text: ex.starter };
    case 'learn': return { k: 'learn' };
  }
}

export function isReady(a: Answer): boolean {
  switch (a.k) {
    case 'choice': return a.selected !== null;
    case 'fill': return !a.slots.includes(null);
    case 'order': return a.seq.length === a.bank.length;
    case 'type': return a.text.trim() !== '';
    case 'code': return a.text.trim() !== '';
    case 'learn': return true;
  }
}

export async function grade(ex: Exercise, a: Answer): Promise<Verdict> {
  if (a.k === 'choice' && (ex.k === 'mc' || ex.k === 'out')) return { ok: !!a.options[a.selected!]?.ok, solution: ex.o[0] };
  if (a.k === 'fill' && ex.k === 'fill') {
    const ok = a.slots.every((v, i) => v !== null && a.bank[v] === ex.a[i]);
    const parts = ex.c.split('___');
    return { ok, solution: parts.reduce((s, p, i) => s + (i ? ex.a[i - 1] : '') + p, '') };
  }
  if (a.k === 'order' && ex.k === 'order') return { ok: a.seq.every((li, p) => ex.l[li] === ex.l[p]), solution: ex.l.join('\n') };
  if (a.k === 'type' && ex.k === 'type') {
    const t = a.text.trim().replace(/^["']|["']$/g, '');
    return { ok: ex.a.includes(t), solution: ex.a[0] };
  }
  if (a.k === 'code' && ex.k === 'code') {
    const r = await runPython(a.text, ex.tests);
    return { ok: r.ok, detail: r.error ?? undefined, stdout: r.stdout };
  }
  return { ok: false };
}
