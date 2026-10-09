import type { NomeIcone } from '@/components/icones-data';
import { courseOf, lessonById } from '@/content';
import { hash } from './mapa';

/**
 * Evento da semana: um tema novo a cada semana (o mesmo para todos, pela data). Lições do tema valem 2 pontos,
 * as outras 1. Ao juntar a meta, o baú do evento dá moedas.
 */
export type Evento = { id: string; nome: string; texto: string; palavras: string[]; cor: string; icone: NomeIcone };
export const EVENTOS: Evento[] = [
  { id: 'loop', nome: 'Semana do Loop', texto: 'Laços e repetições valem pontos em dobro.', palavras: ['laco', 'repeticao', 'repetir', 'while', 'for'], cor: '#E8620C', icone: 'repetir' },
  { id: 'texto', nome: 'Semana dos Textos', texto: 'Strings, print e input valem pontos em dobro.', palavras: ['string', 'texto', 'valores e textos', 'input', 'print'], cor: '#8C6CF2', icone: 'pergaminho' },
  { id: 'listas', nome: 'Semana das Listas', texto: 'Listas, dicionários e coleções valem pontos em dobro.', palavras: ['lista', 'colec', 'dicion', 'tupla', 'conjunto'], cor: '#24A85E', icone: 'livros' },
  { id: 'funcoes', nome: 'Semana das Funções', texto: 'Funções e classes valem pontos em dobro.', palavras: ['funcao', 'funcoes', 'classes', 'objeto'], cor: '#2F6FD6', icone: 'engrenagem-martelo' },
  { id: 'erros', nome: 'Semana dos Erros', texto: 'Erros e exceções valem pontos em dobro.', palavras: ['erro', 'excec'], cor: '#E1474C', icone: 'inseto' },
];
export const META_EVENTO = 10;
export const PREMIO_EVENTO = 100;

export const eventoDaSemana = (semana: string): Evento => EVENTOS[hash(`evento|${semana}`) % EVENTOS.length];

const limpo = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

/** Pontos que uma lição concluída rende no evento: 2 se for do tema, senão 1. */
export function pontosDaLicao(lessonId: string, ev: Evento): number {
  const l = lessonById(lessonId);
  if (!l) return 0;
  const unidade = courseOf(l.track).units[l.unitIndex]?.title ?? '';
  const alvo = limpo(`${unidade} ${l.title}`);
  return ev.palavras.some((p) => alvo.includes(p)) ? 2 : 1;
}

/** Nível em que os eventos semanais são liberados. Antes disso eles ficam escondidos. */
export const EVENTO_NIVEL = 3;
