import { LESSONS, LESSONS_BY_TRACK } from '@/content';
import type { CodeEx, Exercise } from '@/content/types';
import { hash } from './mapa';

/**
 * Desafio do dia: um exercício de código por dia, sorteado entre as lições que a pessoa já concluiu
 * (nunca cobra o que ela ainda não aprendeu). Quem ainda não concluiu nada recebe o primeiro de código da trilha.
 * Fica o mesmo o dia todo e só repete depois de passar por todos os outros do mesmo nível.
 */
export type Desafio = {
  dia: string; // dayKey do desafio sorteado
  exId: string; // exercício de hoje ('' = ainda sem sorteio)
  feito: boolean; // já resolveu o de hoje
  serie: number; // dias seguidos resolvendo o desafio
  melhor: number;
  ultimo: string; // dayKey do último desafio resolvido
  feitos: string[]; // exercícios que já foram desafio
};
export const desafioVazio = (): Desafio => ({ dia: '', exId: '', feito: false, serie: 0, melhor: 0, ultimo: '', feitos: [] });

const ehCodigo = (e: Exercise): e is CodeEx => e.k === 'code';

/** Sorteia o desafio de um dia. A semente do perfil mistura o resultado entre pessoas diferentes. */
export function exercicioDoDesafio(done: Record<string, number>, feitos: string[], dia: string, semente: string): CodeEx | null {
  let pool = LESSONS.filter((l) => l.id in done).flatMap((l) => l.exercises.filter(ehCodigo));
  if (!pool.length) pool = LESSONS_BY_TRACK.main.slice(0, 2).flatMap((l) => l.exercises.filter(ehCodigo));
  const novos = pool.filter((e) => !feitos.includes(e.id));
  const base = novos.length ? novos : pool;
  return base.length ? base[hash(`${dia}|${semente}`) % base.length] : null;
}

/** Sequência a mostrar: se passou mais de um dia sem resolver, a sequência já quebrou. */
export function serieAtual(d: Desafio | undefined, hoje: string, ontem: string): number {
  if (!d) return 0;
  return d.ultimo === hoje || d.ultimo === ontem ? d.serie : 0;
}
