import type { BossId } from '@/components/boss-art';
import { ENEMY_IDS, type EnemyId } from '@/components/enemy-art';
import type { NomeIcone } from '@/components/icones-data';

/**
 * Mapa roguelite de uma zona (= unidade da trilha), no estilo dos mapas de Slay the Spire:
 * linhas de nós de cima para baixo, caminhos que só andam para a coluna vizinha e nunca se
 * cruzam, e um chefe no fim. A diferença: cada "linha de lição" é uma lição da unidade, então
 * QUALQUER caminho passa por todas as lições, na ordem. Entre elas há linhas de evento
 * (fogueira, mistério, tesouro), e antes do chefe sempre há uma linha de descanso.
 *
 * O mapa é gerado a partir de uma semente (zona + perfil + número da expedição): é sempre o
 * mesmo para a mesma expedição, e muda quando a pessoa começa uma expedição nova.
 */
export type TipoNo = 'entrada' | 'batalha' | 'elite' | 'cura' | 'misterio' | 'tesouro' | 'chefe';
export type No = { id: string; tipo: TipoNo; linha: number; col: number; licao?: string; liga: string[] };
export type Mapa = { unidade: string; colunas: number; linhas: No[][]; nos: Record<string, No>; entrada: No; chefe: No };

export const INFO_NO: Record<TipoNo, { nome: string; icone: NomeIcone; cor: [string, string]; texto: string }> = {
  entrada: { nome: 'Entrada', icone: 'entrada', cor: ['#2FB7C9', '#137A8C'], texto: 'Onde a expedição começa.' },
  batalha: { nome: 'Batalha', icone: 'batalha', cor: ['#FFA43A', '#E8620C'], texto: 'Uma lição da zona: conceitos novos e desafios de código.' },
  elite: { nome: 'Elite', icone: 'elite', cor: ['#F2545B', '#B3202A'], texto: 'A mesma lição no modo difícil: cada erro custa 2 vidas, mas rende o triplo de moedas, mais XP e uma relíquia.' },
  cura: { nome: 'Fogueira', icone: 'cura', cor: ['#5BD16E', '#21913A'], texto: 'Descanse para recuperar vidas ou treine o que você errou.' },
  misterio: { nome: 'Mistério', icone: 'misterio', cor: ['#8C6CF2', '#5536C4'], texto: 'Um evento surpresa: pode ser um desafio do Pipo, um mercador ou um baú suspeito.' },
  tesouro: { nome: 'Tesouro', icone: 'tesouro', cor: ['#FFD042', '#D99A0B'], texto: 'Um baú com moedas e uma relíquia.' },
  chefe: { nome: 'Chefe', icone: 'chefe', cor: ['#F2545B', '#8E1520'], texto: 'O chefe da zona. Cada bug que você acha tira vida dele. Derrote-o para liberar a próxima zona.' },
};

// ------------------------------------------------------------------ aleatoriedade com semente
export function hash(s: string) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
export function rng(seed: number) {
  let a = seed || 1;
  return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

type Linha = { tipo: 'licao'; licao: string } | { tipo: 'evento'; final: boolean };

/** Lições e eventos intercalados. Unidades curtas: evento entre cada lição; longas: a cada 2. */
function plano(licoes: string[]): Linha[] {
  const out: Linha[] = [];
  licoes.forEach((l, i) => {
    out.push({ tipo: 'licao', licao: l });
    const ultima = i === licoes.length - 1;
    if (!ultima && (licoes.length <= 3 || i % 2 === 1)) out.push({ tipo: 'evento', final: false });
  });
  out.push({ tipo: 'evento', final: true });
  return out;
}

const COLS = 3;
const cruza = (a: number, b: number, c: number, d: number) => (a < c && b > d) || (a > c && b < d);

export function gerarMapa(unidade: string, licoes: string[], semente: string): Mapa {
  const r = rng(hash(`${unidade}|${semente}`));
  const linhas = plano(licoes);
  const R = linhas.length;
  // 1) Caminhos: 3 caminhos de cima para baixo; cada passo vai para a coluna -1, 0 ou +1 sem cruzar.
  const cel = new Set<string>();
  const arestas = new Map<number, [number, number][]>(); // linha -> [de, para]
  const inicios: number[] = [];
  for (let p = 0; p < 3; p++) {
    let c = p === 1 && inicios[0] !== undefined ? (inicios[0] + 1 + Math.floor(r() * 2)) % COLS : Math.floor(r() * COLS);
    inicios.push(c);
    cel.add(`0:${c}`);
    for (let l = 0; l < R - 1; l++) {
      const ops = [c - 1, c, c + 1].filter((x) => x >= 0 && x < COLS);
      let prox = ops[Math.floor(r() * ops.length)];
      const ex = arestas.get(l) ?? [];
      if (ex.some(([a, b]) => cruza(c, prox, a, b))) prox = c; // reto nunca cruza (passos de ±1)
      if (!ex.some(([a, b]) => a === c && b === prox)) ex.push([c, prox]);
      arestas.set(l, ex);
      c = prox;
      cel.add(`${l + 1}:${c}`);
    }
  }
  // 2) Nós e ligações
  const nos: Record<string, No> = {};
  const id = (l: number, c: number) => `${unidade}:${l}:${c}`;
  const grade: No[][] = [];
  for (let l = 0; l < R; l++) {
    const row: No[] = [];
    for (let c = 0; c < COLS; c++) {
      if (!cel.has(`${l}:${c}`)) continue;
      const lin = linhas[l];
      const n: No = { id: id(l, c), tipo: lin.tipo === 'licao' ? 'batalha' : 'cura', linha: l, col: c, liga: [], ...(lin.tipo === 'licao' ? { licao: lin.licao } : {}) };
      nos[n.id] = n; row.push(n);
    }
    grade.push(row);
  }
  arestas.forEach((ls, l) => ls.forEach(([a, b]) => nos[id(l, a)].liga.push(id(l + 1, b))));
  // 3) Tipos. Lição: batalha ou elite (nunca na 1ª lição; todo nó tem pelo menos uma batalha à frente).
  //    Evento: fogueira, mistério ou tesouro, com filhos do mesmo nó diferentes quando possível.
  for (let l = 1; l < R; l++) {
    const lin = linhas[l];
    for (const n of grade[l]) {
      if (lin.tipo === 'licao') n.tipo = r() < 0.32 ? 'elite' : 'batalha';
      else if (lin.final) n.tipo = r() < 0.75 ? 'cura' : 'tesouro';
      else { const x = r(); n.tipo = x < 0.4 ? 'misterio' : x < 0.75 ? 'cura' : 'tesouro'; }
    }
    for (const pai of grade[l - 1]) {
      const filhos = pai.liga.map((k) => nos[k]);
      if (lin.tipo === 'licao' && filhos.every((f) => f.tipo === 'elite')) filhos[0].tipo = 'batalha';
      if (lin.tipo === 'evento' && lin.final && !filhos.some((f) => f.tipo === 'cura')) filhos[0].tipo = 'cura';
      if (lin.tipo === 'evento' && !lin.final && filhos.length > 1 && filhos.every((f) => f.tipo === filhos[0].tipo)) {
        filhos[1].tipo = filhos[0].tipo === 'misterio' ? 'cura' : 'misterio';
      }
    }
  }
  // 4) Entrada (em cima) e chefe (embaixo)
  const entrada: No = { id: `${unidade}:entrada`, tipo: 'entrada', linha: -1, col: 1, liga: grade[0].map((n) => n.id) };
  const chefe: No = { id: `${unidade}:chefe`, tipo: 'chefe', linha: R, col: 1, liga: [] };
  grade[R - 1].forEach((n) => n.liga.push(chefe.id));
  nos[entrada.id] = entrada; nos[chefe.id] = chefe;
  return { unidade, colunas: COLS, linhas: grade, nos, entrada, chefe };
}

// ------------------------------------------------------------------ relíquias
export type Reliquia = { id: string; nome: string; icone: NomeIcone; texto: string };
export const RELIQUIAS: Reliquia[] = [
  { id: 'pato', nome: 'Pato de borracha', icone: 'pato', texto: 'O primeiro erro de cada lição não custa vida. (Explicar o código para um pato ajuda de verdade!)' },
  { id: 'cafe', nome: 'Café do programador', icone: 'cafe', texto: '+5 XP em cada batalha desta expedição.' },
  { id: 'teclado', nome: 'Teclado mecânico', icone: 'teclado', texto: 'Seus acertos tiram +10 de vida do chefe.' },
  { id: 'escudo', nome: 'Escudo try/except', icone: 'escudo', texto: 'Bloqueia o primeiro ataque do chefe.' },
  { id: 'lupa', nome: 'Lupa de depuração', icone: 'lupa', texto: '+5 segundos para achar cada bug no chefe.' },
];
export const reliquia = (id: string) => RELIQUIAS.find((x) => x.id === id);
export const MAX_RELIQUIAS = 3;

/** Uma relíquia que a pessoa ainda não tem (sorteada pela semente do nó). */
export function sortearReliquia(tem: string[], semente: string): string | null {
  const livres = RELIQUIAS.filter((x) => !tem.includes(x.id));
  if (!livres.length || tem.length >= MAX_RELIQUIAS) return null;
  return livres[hash(semente) % livres.length].id;
}

// ------------------------------------------------------------------ eventos de mistério
export type Misterio = 'pergaminho' | 'mercador' | 'bau-suspeito';
export const misterioDoNo = (noId: string): Misterio => (['pergaminho', 'mercador', 'bau-suspeito'] as const)[hash(noId) % 3];

// ------------------------------------------------------------------ chefes
export type Chefe = { id: BossId; nome: string; icone: NomeIcone; cor: [string, string]; fala: string };
const CHEFES: Chefe[] = [
  { nome: 'Diabrete do SyntaxError', id: 'aranha', icone: 'aranha', cor: ['#7A3FD1', '#3D1B78'], fala: 'Esqueceu os dois-pontos? Eu adoro.' },
  { nome: 'Demônio Alado do IndentationError', id: 'besouro', icone: 'besouro', cor: ['#2E9E5B', '#14552F'], fala: 'Um espaço a mais e seu código é meu.' },
  { nome: 'Minotauro do TypeError', id: 'escaravelho', icone: 'escaravelho', cor: ['#D99A0B', '#7A5300'], fala: 'Texto mais número? Que delícia.' },
  { nome: 'Lanceiro Negro do Loop Infinito', id: 'centopeia', icone: 'centopeia', cor: ['#E8620C', '#8A3200'], fala: 'Eu nunca termino... nunca termino...' },
  { nome: 'Demonesa do NameError', id: 'gosma', icone: 'gosma', cor: ['#3F8FD1', '#174A78'], fala: 'Essa variável? Nunca existiu.' },
  { nome: 'Martelador do IndexError', id: 'diabrete', icone: 'diabrete', cor: ['#D13F6A', '#731A36'], fala: 'Posição 10 numa lista de 3? Pode vir.' },
  { nome: 'Cavaleiro Sombrio do KeyError', id: 'caveira', icone: 'caveira', cor: ['#5B6B7A', '#262F38'], fala: 'Essa chave não está no dicionário.' },
  { nome: 'Ceifadora do ValueError', id: 'lodo', icone: 'lodo', cor: ['#4FB3A9', '#1C5E57'], fala: 'int("abc")? Manda mais!' },
  { nome: 'Cavaleiro Flamejante do AttributeError', id: 'golem', icone: 'golem', cor: ['#8C6CF2', '#3D2696'], fala: 'Esse método não existe neste objeto.' },
  { nome: 'Senhor Demônio do RecursionError', id: 'dragao', icone: 'dragao', cor: ['#B3202A', '#4D0A10'], fala: 'Chame a si mesmo de novo. E de novo...' },
];
/** O inimigo de uma batalha do mapa: fixo para cada nó, então o mesmo nó sempre tem o mesmo monstrinho. */
export const inimigoDoNo = (no: string): EnemyId => ENEMY_IDS[hash(no) % ENEMY_IDS.length];
export const chefeDaZona = (indice: number) => CHEFES[indice % CHEFES.length];

/** Cores de fundo de cada zona (claro, escuro). */
export const PALETAS: { claro: [string, string, string]; escuro: [string, string, string] }[] = [
  { claro: ['#FFE3C7', '#FFB38A', '#F2785C'], escuro: ['#2A1A22', '#40202A', '#5C2A2E'] },
  { claro: ['#D7F2F0', '#9EDCD6', '#5DB8B5'], escuro: ['#0E2226', '#123238', '#17454A'] },
  { claro: ['#E3F5D6', '#B7E39A', '#7CC46A'], escuro: ['#13221A', '#173022', '#1D402A'] },
  { claro: ['#EAE2FF', '#C9B8FF', '#9C86F2'], escuro: ['#1B1630', '#251C45', '#2F235A'] },
  { claro: ['#DCEBFF', '#A9CBFF', '#6FA2F2'], escuro: ['#0F1A2E', '#132443', '#183058'] },
];
