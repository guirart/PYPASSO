/**
 * Baús de peças: quanto mais fundo a zona, mais forte o baú e mais provável sair peça rara.
 *
 * - Baú normal (cai de elites): sua "força" cresce com a zona e varia um pouco de baú para baú, então nas zonas
 *   altas os baús raros aparecem muito mais.
 * - Baú de chefe (cai ao derrotar o chefe da zona): sempre um pouco melhor que o normal médio da mesma zona, mas com teto
 *   para nunca igualar os baús mais fortes das zonas finais. Ele evolui com a zona, então acompanha o herói.
 *
 * Este arquivo não depende de imagens nem do resto do app, para ser fácil de testar.
 */
export const RARIDADES = ['comum', 'incomum', 'raro', 'epico', 'lendario'] as const;
export type RaridadeBau = (typeof RARIDADES)[number];

export const ZONAS = 13; // zonas do curso principal (a última é a 12)
export const FORCA_MAX = 4; // força do melhor baú possível (só sai nas últimas zonas, com a variação sorteada)
export const FORCA_MEDIA_FINAL = 3.5; // força média do baú normal na última zona
export const FORCA_MAX_BOSS = 3.7; // o baú de chefe nunca passa daqui: fica abaixo dos baús mais fortes das zonas finais
export const VANTAGEM_BOSS = 0.5; // quanto o baú de chefe é mais forte que o normal médio da mesma zona

/** Chance (em pontos, soma 100) de cada raridade em cada força inteira de baú, de 0 a 4. Entre uma e outra, interpola. */
export const TABELA: number[][] = [
  [74, 22, 4, 0, 0],
  [45, 38, 14, 3, 0],
  [20, 36, 32, 10, 2],
  [7, 22, 38, 26, 7],
  [0, 8, 32, 40, 20],
];

export type ModeloBau = { id: string; nome: string; boss: boolean };
/** Baús normais, do mais simples ao mais raro (a arte é o Treasure Chests da Mana Seed). */
export const BAUS_NORMAIS: ModeloBau[] = [
  { id: 'n0', nome: 'Baú de Madeira', boss: false },
  { id: 'n1', nome: 'Baú Reforçado', boss: false },
  { id: 'n2', nome: 'Baú de Prata', boss: false },
  { id: 'n3', nome: 'Baú Ornado', boss: false },
  { id: 'n4', nome: 'Baú Místico', boss: false },
];
/** Baús de chefe (caveira): a cor muda conforme o herói avança. */
export const BAUS_BOSS: ModeloBau[] = [
  { id: 'b0', nome: 'Baú do Chefe', boss: true },
  { id: 'b1', nome: 'Baú do Chefe de Prata', boss: true },
  { id: 'b2', nome: 'Baú do Chefe Sombrio', boss: true },
];

const limita = (x: number, a: number, b: number) => Math.max(a, Math.min(b, x));

/** Força média de um baú normal na zona `zona` (0 a 12). */
export const forcaNormal = (zona: number) => (FORCA_MEDIA_FINAL * limita(zona, 0, ZONAS - 1)) / (ZONAS - 1);
/** Força do baú de chefe da zona: um pouco acima do normal, com teto. */
export const forcaBoss = (zona: number) => Math.min(FORCA_MAX_BOSS, forcaNormal(zona) + VANTAGEM_BOSS);

/** Chances de cada raridade para uma força qualquer (interpolando a tabela). */
export function pesosPorForca(forca: number): number[] {
  const f = limita(forca, 0, FORCA_MAX);
  const i = Math.min(FORCA_MAX - 1, Math.floor(f));
  const t = f - i;
  return TABELA[i].map((a, k) => a * (1 - t) + TABELA[i + 1][k] * t);
}

/** Sorteia a raridade pela força do baú. `sorte` (%) favorece as raras; `minimo` zera as raridades abaixo dele. */
export function raridadePorForca(r: () => number, forca: number, sorte = 0, minimo: RaridadeBau = 'comum'): RaridadeBau {
  const piso = RARIDADES.indexOf(minimo);
  const pesos = pesosPorForca(forca).map((p, i) => (i < piso ? 0 : p * (i >= 2 ? 1 + sorte / 100 : 1)));
  const total = pesos.reduce((s, p) => s + p, 0);
  if (total <= 0) return minimo;
  let x = r() * total;
  for (let i = 0; i < pesos.length; i++) { x -= pesos[i]; if (x < 0) return RARIDADES[i]; }
  return minimo;
}

/** Sorteia o baú que cai: o modelo (a aparência) e a força que vai decidir a raridade da peça. */
export function sortearBau(r: () => number, zona: number, tipo: 'normal' | 'boss'): { modelo: ModeloBau; forca: number } {
  if (tipo === 'boss') {
    const forca = forcaBoss(zona);
    return { modelo: BAUS_BOSS[forca < 1.5 ? 0 : forca < 2.8 ? 1 : 2], forca };
  }
  // cada baú normal varia ±0,6 em torno da força da zona: nas zonas altas os baús raros saem bem mais
  const forca = limita(forcaNormal(zona) + (r() - 0.5) * 1.2, 0, FORCA_MAX);
  return { modelo: BAUS_NORMAIS[Math.round(forca)], forca };
}
