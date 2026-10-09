import { LESSONS, LESSONS_BY_TRACK } from '@/content';
import type { ChoiceEx, Exercise } from '@/content/types';
import { shuffle } from './grade';

/**
 * Duelo contra o elenco (offline): 5 perguntas de múltipla escolha, 15 segundos cada.
 * Quem acerta ganha 100 pontos mais 5 por segundo que sobrou; o adversário é simulado pelo app.
 */
export type AdversarioId = 'ana' | 'caio' | 'bia' | 'teo';
export const RODADAS = 5;
export const TEMPO_S = 15;

export type Adversario = {
  id: AdversarioId; nome: string; estilo: string;
  acerto: number; // chance de acertar uma pergunta
  tempo: [min: number, max: number]; // em quanto tempo ele costuma responder, em segundos
  ganhou: string[]; perdeu: string[];
  /** Falas enquanto ele pensa. Não dependem de ele acertar ou errar, para não entregar a resposta. */
  pensando: string[];
  /** Assunto favorito: se a pergunta for sobre isso, ele comenta. */
  tema: RegExp; favorito: string[];
};
export const ADVERSARIOS: Adversario[] = [
  { id: 'ana', nome: 'Ana', estilo: 'Calma e cuidadosa. Boa para começar.', acerto: 0.55, tempo: [6, 11], ganhou: ['Eu me dei bem dessa vez!', 'Pensei com calma.'], perdeu: ['Ah, você foi mais rápido.', 'Quase!'],
    pensando: ['Hmm, deixa eu ler com calma...', 'Vou com cuidado, sem pressa.', 'Será que é essa?'], tema: /string|texto|print|aspas|f"/i, favorito: ['Adoro textos e print!', 'Essa é do meu assunto favorito: textos.'] },
  { id: 'caio', nome: 'Caio', estilo: 'Rápido, mas erra por pressa.', acerto: 0.65, tempo: [3, 7], ganhou: ['Voei nessa!', 'Nem deu tempo de piscar.'], perdeu: ['Fui rápido demais...', 'Ops, errei de novo.'],
    pensando: ['Já sei, já sei!', 'Rapidinho, rapidinho...', 'Vou chutar rápido!'], tema: /input|int\(|float|type|len\(|número|numero/i, favorito: ['Números e input? É a minha praia!', 'Essa eu pego voando.'] },
  { id: 'bia', nome: 'Bia', estilo: 'Equilibrada. Um bom desafio.', acerto: 0.75, tempo: [5, 9], ganhou: ['Eu sabia essa!', 'Ponto meu.'], perdeu: ['Boa resposta!', 'Você me pegou.'],
    pensando: ['Vamos analisar as opções.', 'Eliminando as erradas...', 'Interessante essa.'], tema: /lista|list|for |while|range|laço|laco|append/i, favorito: ['Laços e listas são comigo!', 'Esse assunto eu domino.'] },
  { id: 'teo', nome: 'Téo', estilo: 'Sabe quase tudo. Só para quem já manda bem.', acerto: 0.88, tempo: [4, 8], ganhou: ['Moleza.', 'Fácil demais.'], perdeu: ['Hum, não esperava.', 'Você é bom mesmo.'],
    pensando: ['Isso eu já vi.', 'Hum, truque conhecido.', 'Fácil, mas vou conferir.'], tema: /def |return|class|try|except|dict|função|funcao/i, favorito: ['Funções e classes? Meu terreno.', 'Pergunta do meu nível, finalmente.'] },
];

/** O que o adversário diz ao começar a rodada: o assunto favorito, se a pergunta for sobre ele; senão, uma fala de quem está pensando. */
export function falaDaRodada(a: Adversario, p: Pergunta, rodada: number): string {
  const texto = `${p.ex.q} ${p.ex.c ?? ''}`;
  const lista = a.tema.test(texto) ? a.favorito : a.pensando;
  return lista[rodada % lista.length];
}
export const adversario = (id: string) => ADVERSARIOS.find((a) => a.id === id) ?? ADVERSARIOS[1];

export type Pergunta = { ex: ChoiceEx; opcoes: string[]; certa: string };
const ehEscolha = (e: Exercise): e is ChoiceEx => e.k === 'mc' || e.k === 'out';
const montar = (ex: ChoiceEx): Pergunta => ({ ex, certa: ex.o[0], opcoes: shuffle(ex.o) });

/** Perguntas sorteadas entre as lições já concluídas; se faltar, completa com as primeiras da trilha. */
export function sortearPerguntas(done: Record<string, number>): Pergunta[] {
  let pool = shuffle(LESSONS.filter((l) => l.id in done).flatMap((l) => l.exercises.filter(ehEscolha)));
  if (pool.length < RODADAS) {
    const extra = shuffle(LESSONS_BY_TRACK.main.slice(0, 8).flatMap((l) => l.exercises.filter(ehEscolha))).filter((e) => !pool.includes(e));
    pool = [...pool, ...extra];
  }
  return pool.slice(0, RODADAS).map(montar);
}

/** Pontos de uma resposta: errar ou ficar sem tempo vale zero. */
export const pontos = (certa: boolean, segRestantes: number) => (certa ? 100 + Math.ceil(Math.max(0, segRestantes)) * 5 : 0);

/** Como o adversário vai se sair nesta rodada: acerta ou não, e em quantos segundos. */
export function simularAdversario(a: Adversario): { acertou: boolean; segundos: number } {
  const [min, max] = a.tempo;
  return { acertou: Math.random() < a.acerto, segundos: min + Math.random() * (max - min) };
}

export type Resultado = 'v' | 'd' | 'e';
export const recompensa = (r: Resultado) => (r === 'v' ? { xp: 20, moedas: 25 } : r === 'e' ? { xp: 12, moedas: 12 } : { xp: 8, moedas: 5 });
export type Recorde = { v: number; d: number; e: number };
