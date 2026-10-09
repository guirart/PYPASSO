import type { NomeIcone } from '@/components/icones-data';

/**
 * Gamificação do PyPasso: nível do jogador, moedas, missões diárias, baú, conquistas e loja.
 * Só regras e tabelas; o estado fica em src/lib/store.ts.
 */

// ------------------------------------------------------------------ nível
/** XP para passar do nível n para o n+1 (curva suave: 60, 80, 100, ...). */
export const xpDoNivel = (n: number) => 40 + 20 * n;

export type InfoNivel = { nivel: number; noNivel: number; precisa: number; pct: number; titulo: string; icone: NomeIcone };

const TITULOS: [number, string, NomeIcone][] = [
  [1, 'Ovo de Python', 'ovo'],
  [3, 'Filhote de cobra', 'cobra'],
  [6, 'Aprendiz do print', 'terminal'],
  [10, 'Domador de variáveis', 'cubo'],
  [15, 'Mestre dos laços', 'repetir'],
  [20, 'Feiticeiro das funções', 'varinha'],
  [25, 'Caçador de exceções', 'flechas'],
  [30, 'Arquiteto de classes', 'templo'],
  [40, 'Pythonista sênior', 'cobra'],
  [50, 'Lenda do PyPasso', 'coroa'],
];

export function nivelDe(xp: number): InfoNivel {
  let nivel = 1, resto = Math.max(0, xp);
  while (resto >= xpDoNivel(nivel)) { resto -= xpDoNivel(nivel); nivel++; }
  const [, titulo, icone] = TITULOS.filter(([n]) => nivel >= n).pop()!;
  const precisa = xpDoNivel(nivel);
  return { nivel, noNivel: resto, precisa, pct: resto / precisa, titulo, icone };
}

/** Moedas por subir de nível (cresce devagar). */
export const moedasDoNivel = (nivel: number) => 20 + 5 * Math.floor(nivel / 5);

// ------------------------------------------------------------------ contadores
/** Coisas que contam para missões e conquistas. */
export type Evento = 'xp' | 'licoes' | 'perfeitas' | 'revisoes' | 'provas' | 'especiais' | 'codigo' | 'passos' | 'projetos' | 'combo' | 'compras' | 'itens';
export type Contadores = Partial<Record<Evento, number>>;

// ------------------------------------------------------------------ missões diárias
export type Missao = { id: string; evento: Evento; meta: number; texto: string; moedas: number; icone: NomeIcone };

const MISSOES: Missao[] = [
  { id: 'xp30', evento: 'xp', meta: 30, texto: 'Ganhe 30 XP', moedas: 15, icone: 'raio' },
  { id: 'xp60', evento: 'xp', meta: 60, texto: 'Ganhe 60 XP', moedas: 25, icone: 'raio' },
  { id: 'lic2', evento: 'licoes', meta: 2, texto: 'Termine 2 lições', moedas: 15, icone: 'livro' },
  { id: 'lic3', evento: 'licoes', meta: 3, texto: 'Termine 3 lições', moedas: 25, icone: 'livro' },
  { id: 'perf1', evento: 'perfeitas', meta: 1, texto: 'Faça uma lição sem nenhum erro', moedas: 20, icone: 'alvo' },
  { id: 'rev1', evento: 'revisoes', meta: 1, texto: 'Faça uma Revisão', moedas: 15, icone: 'cerebro' },
  { id: 'combo8', evento: 'combo', meta: 8, texto: 'Acerte 8 seguidas numa lição', moedas: 20, icone: 'chama' },
  { id: 'prova1', evento: 'provas', meta: 1, texto: 'Termine uma Prova de fogo', moedas: 20, icone: 'labareda' },
  { id: 'esp1', evento: 'especiais', meta: 1, texto: 'Faça um exercício especial do Pipo', moedas: 15, icone: 'grimorio' },
  { id: 'cod3', evento: 'codigo', meta: 3, texto: 'Rode código 3 vezes na aba Código', moedas: 10, icone: 'play' },
  { id: 'passo1', evento: 'passos', meta: 1, texto: 'Avance um passo num Projeto', moedas: 20, icone: 'martelo' },
];

const hashDia = (dia: string) => [...dia].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);

/** Três missões por dia, sorteadas pela data (iguais o dia todo), sem repetir o tipo. */
export function missoesDoDia(dia: string): Missao[] {
  let h = hashDia(dia);
  const out: Missao[] = [];
  const pool = MISSOES.slice();
  while (out.length < 3 && pool.length) {
    h = (h * 1103515245 + 12345) >>> 0;
    const m = pool.splice(h % pool.length, 1)[0];
    if (!out.some((o) => o.evento === m.evento)) out.push(m);
  }
  return out;
}

/** Baú do dia: abre quando as 3 missões foram resgatadas. */
export const moedasDoBau = () => 30 + Math.floor(Math.random() * 6) * 10; // 30 a 80

// ------------------------------------------------------------------ conquistas
export type Fonte = Contadores & { nivel: number; streak: number; aprendidos: number; liga: number };
export type Conquista = { id: string; icone: NomeIcone; nome: string; texto: string; meta: number; valor: (f: Fonte) => number; moedas: number };

const c = (id: string, icone: NomeIcone, nome: string, texto: string, meta: number, valor: (f: Fonte) => number, moedas: number): Conquista =>
  ({ id, icone, nome, texto, meta, valor, moedas });
const n = (e: Evento) => (f: Fonte) => f[e] ?? 0;

export const CONQUISTAS: Conquista[] = [
  c('primeira', 'broto', 'Primeiro passo', 'Termine sua primeira lição', 1, n('licoes'), 10),
  c('lic10', 'livro', 'Estudante', 'Termine 10 lições', 10, n('licoes'), 30),
  c('lic50', 'pilha-livros', 'Rato de biblioteca', 'Termine 50 lições', 50, n('licoes'), 80),
  c('lic150', 'formatura', 'Formando', 'Termine 150 lições', 150, n('licoes'), 200),
  c('perf5', 'mosca', 'Mira certeira', '5 lições sem nenhum erro', 5, n('perfeitas'), 40),
  c('perf25', 'oculos', 'Mr. Perfeito', '25 lições sem nenhum erro', 25, n('perfeitas'), 120),
  c('seq3', 'chama', 'Esquentando', 'Sequência de 3 dias', 3, (f) => f.streak, 20),
  c('seq7', 'fogo', 'Semana em chamas', 'Sequência de 7 dias', 7, (f) => f.streak, 60),
  c('seq30', 'cometa', 'Imparável', 'Sequência de 30 dias', 30, (f) => f.streak, 250),
  c('niv5', 'estrela', 'Nível 5', 'Chegue ao nível 5', 5, (f) => f.nivel, 30),
  c('niv15', 'medalha-estrela', 'Nível 15', 'Chegue ao nível 15', 15, (f) => f.nivel, 100),
  c('niv30', 'louros', 'Nível 30', 'Chegue ao nível 30', 30, (f) => f.nivel, 250),
  c('combo15', 'raios', 'Combo x15', 'Acerte 15 seguidas numa lição', 15, n('combo'), 50),
  c('rev10', 'cerebro', 'Memória de elefante', 'Faça 10 Revisões', 10, n('revisoes'), 60),
  c('prova10', 'labareda', 'Bombeiro', 'Termine 10 Provas de fogo', 10, n('provas'), 60),
  c('esp10', 'grimorio', 'Leitor do Pipo', '10 exercícios especiais', 10, n('especiais'), 50),
  c('cod25', 'teclado-ui', 'Mão na massa', 'Rode código 25 vezes na aba Código', 25, n('codigo'), 40),
  c('proj1', 'martelo', 'Construtor', 'Termine um Projeto guiado', 1, n('projetos'), 60),
  c('proj6', 'engrenagem-martelo', 'Engenheiro', 'Termine todos os Projetos guiados', 6, n('projetos'), 300),
  c('bib25', 'livros', 'Colecionador de conceitos', '25 conceitos na sua Biblioteca', 25, (f) => f.aprendidos, 40),
  c('bib100', 'pergaminho', 'Bibliotecário', '100 conceitos na sua Biblioteca', 100, (f) => f.aprendidos, 150),
  c('liga3', 'taca', 'Caçador de Bugs', 'Chegue à liga Ouro', 3, (f) => f.liga, 60),
  c('compra1', 'sacola', 'Freguês', 'Compre algo na Loja', 1, n('compras'), 10),
  c('item1', 'sacola', 'Achado e perdido', 'Ganhe sua primeira peça de equipamento', 1, n('itens'), 20),
  c('item15', 'sacola', 'Colecionador de tesouros', 'Ganhe 15 peças de equipamento', 15, n('itens'), 80),
];

// ------------------------------------------------------------------ loja
export type ItemLoja = {
  id: string; icone: NomeIcone; nome: string; texto: string; preco: number;
  tipo: 'congelador' | 'vidas' | 'xp2' | 'moldura';
  max?: number; // quanto dá para ter guardado ao mesmo tempo
  cores?: [string, string]; // moldura: gradiente simples (cor de fora, de dentro)
};

export const LOJA: ItemLoja[] = [
  { id: 'congelador', icone: 'gelo', nome: 'Congelador de sequência', texto: 'Se você ficar um dia sem estudar, ele protege sua sequência. Guarde até 2.', preco: 120, tipo: 'congelador', max: 2 },
  { id: 'vidas', icone: 'pocao', nome: 'Recarga de vidas', texto: 'Enche suas 5 vidas na hora.', preco: 60, tipo: 'vidas' },
  { id: 'xp2', icone: 'raio', nome: 'XP em dobro (15 min)', texto: 'Tudo que você ganhar nos próximos 15 minutos vale o dobro.', preco: 100, tipo: 'xp2' },
  { id: 'mold-fogo', icone: 'fogo', nome: 'Moldura Fogo', texto: 'Um anel em chamas em volta do seu avatar.', preco: 150, tipo: 'moldura', cores: ['#FF6B1A', '#FFC83D'] },
  { id: 'mold-oceano', icone: 'gota', nome: 'Moldura Oceano', texto: 'Azul profundo, para quem mergulha no código.', preco: 150, tipo: 'moldura', cores: ['#1E6FD9', '#5BD1F5'] },
  { id: 'mold-floresta', icone: 'broto', nome: 'Moldura Floresta', texto: 'Verde de cobra, bem pythônica.', preco: 150, tipo: 'moldura', cores: ['#1F8A4C', '#7BD88F'] },
  { id: 'mold-ouro', icone: 'coroa', nome: 'Moldura Ouro', texto: 'Para quem já juntou muita moeda.', preco: 400, tipo: 'moldura', cores: ['#B98B3A', '#FFD86B'] },
  { id: 'mold-galaxia', icone: 'planeta', nome: 'Moldura Galáxia', texto: 'Roxa e brilhante. A mais rara da loja.', preco: 600, tipo: 'moldura', cores: ['#5B2BC4', '#E05BF5'] },
];

export const itemLoja = (id: string) => LOJA.find((i) => i.id === id);
export const XP2_MS = 15 * 60 * 1000;

// ------------------------------------------------------------------ recompensas das atividades
export const MOEDAS = { licao: 5, perfeita: 5, revisao: 8, passo: 5, projeto: 50, prova: 5, especial: 5 };
