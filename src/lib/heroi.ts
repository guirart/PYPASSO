import { OPCOES, type PaginaMana } from '@/components/mana-sprites';

/**
 * O herói das batalhas: um personagem em camadas (paper doll) do Mana Seed Character Base (demo gratuito de Seliel the Shaper).
 * O visual é guardado só como ids (pele, cabelo, roupa...), e as camadas são montadas na hora em HeroiMana.tsx.
 */
export type Variante = { estilo: string; cor: string };
export type LookHeroi = { pele: string; cabelo: Variante | null; roupa: Variante; chapeu: Variante | null; arma: Variante; escudo: Variante | null };

export const HEROI_PADRAO: LookHeroi = {
  pele: 'v01', cabelo: { estilo: 'dap1', cor: 'v11' }, roupa: { estilo: 'fstr', cor: 'v01' }, chapeu: null,
  arma: { estilo: 'sw01', cor: 'v01' }, escudo: { estilo: 'sh01', cor: 'v01' },
};

const pega = <T,>(lista: T[], i: number) => lista[Math.abs(i) % lista.length];
/** Sorteia um visual (o chapéu e o cabelo podem ficar de fora). */
export function heroiAleatorio(): LookHeroi {
  const r = (n: number) => Math.floor(Math.random() * n);
  const cabelo = r(5) ? { estilo: pega(OPCOES.cabelo.estilos, r(2)).id, cor: pega(OPCOES.cabelo.cores, r(8)).id } : null;
  const roupaE = pega(OPCOES.roupa.estilos, r(2)).id;
  const chapeuE = r(3) === 0 ? pega(OPCOES.chapeu.estilos, r(2)).id : null;
  const armaE = pega(OPCOES.arma.estilos, r(3)).id;
  const escudoE = r(6) ? pega(OPCOES.escudo.estilos, r(3)).id : null;
  return {
    pele: pega(OPCOES.pele, r(6)).id, cabelo,
    roupa: { estilo: roupaE, cor: pega(OPCOES.roupa.cores[roupaE], r(5)).id },
    chapeu: chapeuE ? { estilo: chapeuE, cor: pega(OPCOES.chapeu.cores[chapeuE], r(5)).id } : null,
    arma: { estilo: armaE, cor: pega(OPCOES.arma.cores[armaE], r(3)).id },
    escudo: escudoE ? { estilo: escudoE, cor: pega(OPCOES.escudo.cores[escudoE], r(3)).id } : null,
  };
}

/** Garante um visual válido, mesmo que o salvo no aparelho tenha ficado incompleto. */
export const normalizarHeroi = (l: Partial<LookHeroi> | undefined): LookHeroi => ({ ...HEROI_PADRAO, ...(l ?? {}) });

// ---- animações (sempre olhando para a direita, que é a linha 2 das páginas de combate e a linha 6 da de caminhada)
export type AnimHeroi = 'andar' | 'sacar' | 'idle' | 'golpe1' | 'golpe2' | 'dano';
export type Anim = { pg: PaginaMana; row: number; cols: number[]; ms: number[]; loop: boolean };
export const ANIMS: Record<AnimHeroi, Anim> = {
  andar: { pg: 'p1', row: 6, cols: [0, 1, 2, 3, 4, 5], ms: [135, 135, 135, 135, 135, 135], loop: true },
  sacar: { pg: 'pONE1', row: 2, cols: [0, 1, 2], ms: [120, 120, 120], loop: false },
  idle: { pg: 'pONE2', row: 2, cols: [0, 1, 2, 3], ms: [200, 200, 200, 200], loop: true },
  golpe1: { pg: 'pONE3', row: 2, cols: [0, 1, 2, 3], ms: [160, 65, 65, 200], loop: false },
  golpe2: { pg: 'pONE3', row: 2, cols: [4, 5, 6, 7], ms: [160, 65, 65, 200], loop: false },
  dano: { pg: 'pONE1', row: 2, cols: [5], ms: [450], loop: false },
};
export const duracao = (a: AnimHeroi) => ANIMS[a].ms.reduce((s, x) => s + x, 0);

/** Em cada quadro, a arma (sw) e o escudo (sh) ficam na frente (F) ou atrás (B) do corpo. Lido dos guias de camadas do pacote. */
export const FRENTE: Record<'pONE1' | 'pONE2' | 'pONE3', { sw: string[]; sh: string[] }> = {
  pONE1: { sw: ['BFBFFFBB', 'FBBBBBBB', 'BFFBFFBB', 'BFFBFFBB', 'BBBBBBBB', 'BBBBBBBB', 'BBBBBBBB', 'BBBBBBBB'], sh: ['BFBBFBBB', 'FBFFBFBB', 'BBBFFBBB', 'BBBFFBBB', 'BBBBBBBB', 'BBBBBBBB', 'BBBBBBBB', 'BBBBBBBB'] },
  pONE2: { sw: ['FFFFFFFF', 'BBBBBBBB', 'FFFFFFFF', 'FFFFFFFF', 'FFFBBBBB', 'BBBBBBBB', 'FFFBBBBB', 'FFFBBBBB'], sh: ['FFFFFFFF', 'BBBBBBBB', 'BBBBBBBB', 'BBBBBBBB', 'FFFBBBBB', 'BBBBBBBB', 'BBBBBBBB', 'BBBBBBBB'] },
  pONE3: { sw: ['BBBBBBBB', 'BBBBBBBB', 'BFBBBBBB', 'BFBBBBBB', 'FFBBBBBB', 'BBBBBBBB', 'FFBBFFFF', 'FFBBFFFF'], sh: ['FBBBBBFF', 'BBFFFFBB', 'BBBBBBBB', 'BBBBBBBB', 'FBBBFFBB', 'BBFFBFFF', 'BBBBFBFF', 'BBBBFBFF'] },
};

// Âncoras no quadro de 64x64: coluna do centro do corpo e linha dos pés.
export const CENTRO = 30;
export const PES = 43;
