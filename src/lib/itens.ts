import { OPCOES } from '@/components/mana-sprites';
import { raridadePorForca } from './baus';
import { valorMelhorado } from './melhoria';
import type { LookHeroi, Variante } from './heroi';

/**
 * Itens do herói. Cada item é uma "peça" sorteada: um visual (estilo + cor), uma raridade e de 0 a 3 habilidades com valores
 * sorteados. Chefes (e elites) deixam peças cair; o baú do herói vende uma peça sorteada. Peças de 5 raridades:
 * comum, incomum, raro, épico e lendário.
 */
export type Slot = 'arma' | 'escudo' | 'roupa' | 'chapeu';
export type Raridade = 'comum' | 'incomum' | 'raro' | 'epico' | 'lendario';
export type HabId = 'crit' | 'xp' | 'moedas' | 'dica' | 'protecao' | 'sorte' | 'vida' | 'tempo' | 'dano';
export type Hab = { id: HabId; v: number };
export type ItemInst = { id: string; slot: Slot; estilo: string; cor: string; raridade: Raridade; hab: Hab[]; novo?: boolean; mel?: number /* nível de melhoria, 0 a 5 */ };

export const SLOTS: { id: Slot; nome: string; opcional: boolean }[] = [
  { id: 'arma', nome: 'Arma', opcional: false },
  { id: 'escudo', nome: 'Escudo', opcional: true },
  { id: 'roupa', nome: 'Roupa', opcional: false },
  { id: 'chapeu', nome: 'Chapéu', opcional: true },
];
export const ORDEM_RARIDADE: Raridade[] = ['comum', 'incomum', 'raro', 'epico', 'lendario'];
export const RARIDADE: Record<Raridade, { nome: string; cor: string; nivel: number; habs: [number, number]; peso: number; venda: number }> = {
  comum: { nome: 'Comum', cor: '#8A94A3', nivel: 1, habs: [0, 0], peso: 50, venda: 4 },
  incomum: { nome: 'Incomum', cor: '#43B26B', nivel: 2, habs: [1, 1], peso: 28, venda: 10 },
  raro: { nome: 'Raro', cor: '#2E9BD0', nivel: 3, habs: [1, 2], peso: 14, venda: 25 },
  epico: { nome: 'Épico', cor: '#A24CF0', nivel: 4, habs: [2, 2], peso: 6, venda: 60 },
  lendario: { nome: 'Lendário', cor: '#E8960C', nivel: 5, habs: [3, 3], peso: 2, venda: 150 },
};

/** O que cada habilidade faz no jogo (os valores crescem com a raridade). `faixa` é por nível de raridade. */
export const HABS: Record<HabId, { nome: string; texto: (v: number) => string; faixa: [number, number]; sufixo: string; favorita: Slot }> = {
  crit: { nome: 'Precisão', texto: (v) => `+${v}% de chance de golpe crítico`, faixa: [3, 5], sufixo: 'da Precisão', favorita: 'arma' },
  xp: { nome: 'Sabedoria', texto: (v) => `+${v}% de XP nas lições`, faixa: [2, 4], sufixo: 'do Sábio', favorita: 'roupa' },
  moedas: { nome: 'Fortuna', texto: (v) => `+${v}% de moedas`, faixa: [3, 6], sufixo: 'do Mercador', favorita: 'roupa' },
  dica: { nome: 'Pipo', texto: (v) => `${v} ${v === 1 ? 'dica grátis' : 'dicas grátis'} por lição`, faixa: [1, 1], sufixo: 'do Pipo', favorita: 'chapeu' },
  protecao: { nome: 'Guarda', texto: (v) => `Ignora ${v} ${v === 1 ? 'erro' : 'erros'} por lição (sem perder vida)`, faixa: [1, 1], sufixo: 'do Guardião', favorita: 'escudo' },
  sorte: { nome: 'Sorte', texto: (v) => `+${v}% de sorte nos drops de chefe`, faixa: [3, 6], sufixo: 'da Sorte', favorita: 'chapeu' },
  vida: { nome: 'Vitalidade', texto: (v) => `Recupera 1 vida a cada ${v} acertos seguidos`, faixa: [4, 12], sufixo: 'da Vida', favorita: 'escudo' },
  tempo: { nome: 'Relógio', texto: (v) => `+${v}s por bug nas lutas de chefe`, faixa: [1, 5], sufixo: 'do Tempo', favorita: 'chapeu' },
  dano: { nome: 'Fúria', texto: (v) => `+${v}% de dano nos chefes`, faixa: [4, 7], sufixo: 'da Fúria', favorita: 'arma' },
};

/** Como cada arma ataca na batalha: o `modo` muda a animação (ver InimigoBarra). */
export type ModoAtaque = 'corte' | 'pesado' | 'atordoa' | 'distancia';
export const ATAQUE: Record<string, { modo: ModoAtaque; nome: string; texto: string; passiva: string }> = {
  sw01: { modo: 'corte', nome: 'Espada', texto: 'Avança e corta rápido.', passiva: '+5% de chance de golpe crítico' },
  ax01: { modo: 'pesado', nome: 'Machado', texto: 'Golpe pesado: treme a tela e empurra o inimigo.', passiva: 'Golpes críticos causam +1 de dano' },
  mc01: { modo: 'atordoa', nome: 'Maça', texto: 'Atordoa o inimigo a cada pancada.', passiva: '20% de chance de atordoar: o próximo erro não custa vida' },
  arco: { modo: 'distancia', nome: 'Arco', texto: 'Ataca de longe, sem sair do lugar.', passiva: 'A partir de 3 acertos seguidos, cada flecha causa +1 de dano' },
};

type Base = { id: string; nome: string; cores: { id: string; nome: string; hex: string }[] };
const BASES: Record<Slot, Base[]> = {
  arma: [
    { id: 'sw01', nome: 'Espada', cores: [{ id: 'v01', nome: 'de Aço', hex: '#a7a498' }, { id: 'v03', nome: 'Gélida', hex: '#8d8782' }, { id: 'v05', nome: 'Dourada', hex: '#aa8b4a' }] },
    { id: 'ax01', nome: 'Machado', cores: [{ id: 'v01', nome: 'de Aço', hex: '#908c86' }, { id: 'v03', nome: 'Gélido', hex: '#88817b' }, { id: 'v05', nome: 'Dourado', hex: '#a48548' }] },
    { id: 'mc01', nome: 'Maça', cores: [{ id: 'v01', nome: 'de Aço', hex: '#8c9392' }, { id: 'v03', nome: 'Gélida', hex: '#7f7c7a' }, { id: 'v05', nome: 'Dourada', hex: '#b98934' }] },
    { id: 'arco', nome: 'Arco', cores: [{ id: 'v01', nome: 'de Madeira', hex: '#a8754a' }, { id: 'v03', nome: 'de Ébano', hex: '#4a3a33' }, { id: 'v05', nome: 'Dourado', hex: '#d6a93c' }] },
  ],
  escudo: [
    { id: 'sh01', nome: 'Escudo Redondo', cores: [{ id: 'v01', nome: 'de Madeira', hex: '#755c55' }, { id: 'v03', nome: 'de Pedra', hex: '#7a7774' }, { id: 'v05', nome: 'de Musgo', hex: '#525145' }] },
    { id: 'sh02', nome: 'Escudo Escuro', cores: [{ id: 'v01', nome: 'de Prata', hex: '#646870' }, { id: 'v03', nome: 'de Sombra', hex: '#5c5957' }, { id: 'v05', nome: 'de Bronze', hex: '#9e6316' }] },
    { id: 'sh03', nome: 'Escudo Pesado', cores: [{ id: 'v01', nome: 'Cinzento', hex: '#69696b' }, { id: 'v03', nome: 'Vinho', hex: '#584648' }, { id: 'v05', nome: 'Ferrugem', hex: '#8e4b3c' }] },
  ],
  roupa: [
    { id: 'fstr', nome: 'Traje da Floresta', cores: ['Marrom', 'Roxo', 'Cinza', 'Ocre', 'Verde'].map((n, i) => ({ id: `v0${i + 1}`, nome: n, hex: OPCOES.roupa.cores.fstr[i].cor })) },
    { id: 'pfpn', nome: 'Traje de Fazenda', cores: ['Cinza', 'Marrom', 'Lilás', 'Chumbo', 'Areia'].map((n, i) => ({ id: `v0${i + 1}`, nome: n, hex: OPCOES.roupa.cores.pfpn[i].cor })) },
  ],
  chapeu: [
    { id: 'pnty', nome: 'Chapéu de Mago', cores: ['Azul', 'Marrom', 'Verde', 'Cinza', 'Ouro'].map((n, i) => ({ id: `v0${i + 1}`, nome: n, hex: OPCOES.chapeu.cores.pnty[i].cor })) },
    { id: 'pfht', nome: 'Touca', cores: ['Vermelha', 'Creme', 'Cinza', 'Marrom', 'Verde'].map((n, i) => ({ id: `v0${i + 1}`, nome: n, hex: OPCOES.chapeu.cores.pfht[i].cor })) },
  ],
};

/** Todas as combinações de visual existentes (o "mostruário"): 12 armas, 9 escudos, 10 roupas e 10 chapéus. */
export const VISUAIS: { slot: Slot; estilo: string; cor: string; nome: string; hex: string }[] = (Object.keys(BASES) as Slot[]).flatMap((slot) =>
  BASES[slot].flatMap((b) => b.cores.map((c) => ({ slot, estilo: b.id, cor: c.id, nome: `${b.nome} ${c.nome}`, hex: c.hex }))));
export const visualDe = (slot: Slot, estilo: string, cor: string) => VISUAIS.find((v) => v.slot === slot && v.estilo === estilo && v.cor === cor);

/** Nome do item: o do visual, mais um sufixo pela habilidade principal (ex.: "Arco de Ébano da Precisão"). */
export function nomeDe(it: ItemInst): string {
  const v = visualDe(it.slot, it.estilo, it.cor);
  const base = v?.nome ?? it.estilo;
  const principal = it.hab[0];
  const nome = principal ? `${base} ${HABS[principal.id].sufixo}` : base;
  return it.mel ? `${nome} +${it.mel}` : nome;
}

/** Valor de uma habilidade da peça já com a melhoria aplicada. */
export const valorEfetivo = (it: ItemInst, h: Hab) => valorMelhorado(h.id, h.v, it.mel ?? 0);

// ---- itens básicos: o herói começa com eles e nunca os perde
export const BASICOS: ItemInst[] = [
  { id: 'basico-arma', slot: 'arma', estilo: 'sw01', cor: 'v01', raridade: 'comum', hab: [] },
  { id: 'basico-escudo', slot: 'escudo', estilo: 'sh01', cor: 'v01', raridade: 'comum', hab: [] },
  { id: 'basico-roupa', slot: 'roupa', estilo: 'fstr', cor: 'v01', raridade: 'comum', hab: [] },
];
export type Equip = Record<Slot, string | null>;
export const EQUIP_PADRAO: Equip = { arma: 'basico-arma', escudo: 'basico-escudo', roupa: 'basico-roupa', chapeu: null };
export const ehBasico = (it: ItemInst) => it.id.startsWith('basico-');

// ---- sorteio
type Rnd = () => number;
const entre = (r: Rnd, a: number, b: number) => a + Math.floor(r() * (b - a + 1));
const escolhe = <T,>(r: Rnd, l: T[]) => l[Math.floor(r() * l.length)];

/** Sorteia a raridade. `zona` (0 a 12) e `sorte` (%) deixam as raras mais prováveis; `minimo` garante o piso (chefes não soltam comum). */
export function sortearRaridade(r: Rnd, zona = 0, sorte = 0, minimo: Raridade = 'comum'): Raridade {
  const pisos = ORDEM_RARIDADE.indexOf(minimo);
  const pesos = ORDEM_RARIDADE.map((k, i) => (i < pisos ? 0 : RARIDADE[k].peso * (i >= 2 ? (1 + zona * 0.12) * (1 + sorte / 100) : 1)));
  let x = r() * pesos.reduce((s, p) => s + p, 0);
  for (let i = 0; i < pesos.length; i++) { x -= pesos[i]; if (x < 0) return ORDEM_RARIDADE[i]; }
  return minimo;
}

function sortearHabs(r: Rnd, slot: Slot, raridade: Raridade): Hab[] {
  const [min, max] = RARIDADE[raridade].habs;
  const n = entre(r, min, max);
  const lote = (Object.keys(HABS) as HabId[]).flatMap((id) => Array(HABS[id].favorita === slot ? 3 : 1).fill(id) as HabId[]);
  const usados = new Set<HabId>();
  const habs: Hab[] = [];
  while (habs.length < n) {
    const id = escolhe(r, lote);
    if (usados.has(id)) continue;
    usados.add(id);
    const nivel = RARIDADE[raridade].nivel;
    const [a, b] = HABS[id].faixa;
    const v = id === 'dica' ? Math.min(3, Math.ceil(nivel / 2))
      : id === 'protecao' ? (nivel >= 4 ? 2 : 1)
      : id === 'vida' ? Math.max(4, 14 - 2 * nivel) // quanto mais rara, menos acertos seguidos para curar
      : id === 'tempo' ? entre(r, Math.ceil(nivel / 2), nivel)
      : entre(r, a * nivel, b * nivel);
    habs.push({ id, v });
  }
  return habs.sort((x, y) => y.v - x.v);
}

let contador = 0;
/** Cria um item sorteado. `r` é o gerador de números (Math.random, ou um fixo nos testes). */
export function sortearItem(r: Rnd = Math.random, opc: { zona?: number; sorte?: number; minimo?: Raridade; slot?: Slot; forca?: number } = {}): ItemInst {
  // com `forca` (a do baú, de lib/baus.ts) a raridade vem da tabela do baú; sem ela, do cálculo simples por zona
  const raridade = opc.forca !== undefined ? raridadePorForca(r, opc.forca, opc.sorte ?? 0, opc.minimo ?? 'comum') : sortearRaridade(r, opc.zona ?? 0, opc.sorte ?? 0, opc.minimo ?? 'comum');
  const slot = opc.slot ?? escolhe(r, VISUAIS.map((v) => v.slot));
  const v = escolhe(r, VISUAIS.filter((x) => x.slot === slot));
  contador += 1;
  return { id: `i${Date.now().toString(36)}${contador}${Math.floor(r() * 1e4).toString(36)}`, slot, estilo: v.estilo, cor: v.cor, raridade, hab: sortearHabs(r, slot, raridade), novo: true };
}

// ---- efeitos
export type Bonus = Record<HabId, number>;
export const BONUS_ZERO: Bonus = { crit: 0, xp: 0, moedas: 0, dica: 0, protecao: 0, sorte: 0, vida: 0, tempo: 0, dano: 0 };
/** Soma das habilidades de tudo que está equipado. */
export function bonusDoEquipamento(inv: ItemInst[], equip: Equip): Bonus {
  const b = { ...BONUS_ZERO };
  for (const slot of SLOTS) {
    const it = inv.find((i) => i.id === equip[slot.id]);
    if (!it) continue;
    for (const h of it.hab) {
      // Vitalidade guarda o MENOR número de acertos (a melhor cura); as outras somam
      const v = valorEfetivo(it, h);
      if (h.id === 'vida') b.vida = b.vida ? Math.min(b.vida, v) : v; else b[h.id] += v;
    }
  }
  if (inv.find((i) => i.id === equip.arma)?.estilo === 'sw01') b.crit += 5; // passiva da espada
  return b;
}

/** O visual do herói com as peças equipadas (pele e cabelo vêm da aparência). */
export function vestirEquipamento(base: LookHeroi, inv: ItemInst[], equip: Equip): LookHeroi {
  const peca = (slot: Slot): Variante | null => {
    const it = inv.find((i) => i.id === equip[slot]);
    return it ? { estilo: it.estilo, cor: it.cor } : null;
  };
  return { ...base, arma: peca('arma') ?? base.arma, escudo: peca('escudo'), roupa: peca('roupa') ?? base.roupa, chapeu: peca('chapeu') };
}

/** Pontos de raridade das peças vestidas (máximo 20). */
export function poderDoEquipamento(inv: ItemInst[], equip: Equip): { pontos: number; max: number } {
  let pontos = 0;
  for (const s of SLOTS) { const it = inv.find((i) => i.id === equip[s.id]); if (it) pontos += RARIDADE[it.raridade].nivel; }
  return { pontos, max: SLOTS.length * 5 };
}

/** Estilo da arma vestida (para as passivas do machado, da maça e do arco). */
export const armaVestida = (inv: ItemInst[], equip: Equip) => inv.find((i) => i.id === equip.arma)?.estilo ?? 'sw01';
