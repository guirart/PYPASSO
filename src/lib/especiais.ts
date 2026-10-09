import type { Cena } from '@/components/scenes';
import { TRACKS } from '@/content';
import type { ChoiceEx, Exercise, TypeEx, Unit } from '@/content/types';

/**
 * Exercícios especiais das cenas do Pipo na trilha (um por unidade, opcionais):
 *  - Leitura de código (Pipo lendo): prever o que trechos da unidade mostram. Sem vidas.
 *  - Digitação de código (Pipo no computador): copiar trechos da unidade, valendo velocidade e precisão.
 * Os trechos vêm do próprio conteúdo da unidade (já conferido rodando Python).
 */
export const cenaDaUnidade = (unitIndex: number): Cena => (unitIndex % 2 === 0 ? 'lendo' : 'digitando');
export const especialId = (cena: Cena, unitId: string) => `${cena}-${unitId}`;
export const TITULOS: Record<Cena, string> = { lendo: 'Leitura de código', digitando: 'Digitação de código' };

export function lerId(id: string): { cena: Cena; unit: Unit; numero: number } | null {
  const m = /^(lendo|digitando)-(.+)$/.exec(id);
  if (!m) return null;
  for (const tr of TRACKS) {
    const i = tr.course.units.findIndex((u) => u.id === m[2]);
    if (i >= 0) return { cena: m[1] as Cena, unit: tr.course.units[i], numero: i + 1 };
  }
  return null;
}

/** Embaralhamento estável (a mesma unidade sempre começa igual; muda a cada tentativa). */
function embaralhar<T>(xs: T[], semente: number) {
  const a = xs.slice();
  let s = semente || 1;
  for (let i = a.length - 1; i > 0; i--) {
    s = (s * 1103515245 + 12345) % 2147483648;
    const j = s % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
const hash = (t: string) => [...t].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);

export const N_LEITURA = 5;
/** Leitura: só exercícios de prever a saída (é o "ler código" de verdade). */
export function questoesDeLeitura(unit: Unit, tentativa = 0): Exercise[] {
  const todas = unit.lessons.flatMap((l) => l.exercises).filter((e): e is ChoiceEx | TypeEx =>
    (e.k === 'out' || e.k === 'type') && !!e.c && !/input\(/.test(e.c));
  return embaralhar(todas, hash(unit.id) + tentativa * 7919).slice(0, N_LEITURA);
}

export const N_DIGITAR = 3;
/** Digitação: trechos curtos (1 a 4 linhas) da unidade, sem lacunas nem input(). */
export function trechosParaDigitar(unit: Unit, tentativa = 0): string[] {
  const fontes = unit.lessons.flatMap((l) => l.exercises).flatMap((e) => (e.k === 'learn' || e.k === 'out' || e.k === 'type') && e.c ? [e.c] : []);
  const trechos = new Set<string>();
  for (const f of fontes) {
    if (/___|input\(|breakpoint/.test(f)) continue;
    const linhas = f.split('\n').map((l) => l.replace(/\s+$/, '')).filter((l) => l.trim() && !l.trim().startsWith('#'));
    for (let i = 0; i < linhas.length; i += 3) {
      const t = linhas.slice(i, i + 3).join('\n');
      // começa sem recuo (para fazer sentido sozinho) e tem um tamanho bom para o celular
      if (!/^\s/.test(t) && t.length >= 18 && t.length <= 110) trechos.add(t);
    }
  }
  return embaralhar([...trechos], hash(unit.id) + tentativa * 104729).slice(0, N_DIGITAR);
}

/** Estrelas da leitura: 3 = tudo certo, 2 = um erro, 1 = mais da metade. */
export const estrelasLeitura = (acertos: number, total: number) =>
  acertos >= total ? 3 : acertos >= total - 1 ? 2 : acertos > total / 2 ? 1 : 0;

/** Estrelas da digitação: terminar = 1; rápido e quase sem erros = 2; muito rápido e preciso = 3. */
export const estrelasDigitacao = (cpm: number, precisao: number) =>
  cpm >= 90 && precisao >= 0.98 ? 3 : cpm >= 50 && precisao >= 0.94 ? 2 : 1;
