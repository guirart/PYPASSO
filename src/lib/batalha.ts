/**
 * Equilíbrio das lutas: a vida dos inimigos e dos chefes acompanha o nível do herói e a zona, e nenhum golpe
 * sozinho pode tirar mais que uma fração da vida, então ninguém "termina a lição com um hit só".
 *
 * Arquivo puro (sem imagens nem telas) para ser fácil de testar.
 */
export type EstiloArma = 'sw01' | 'ax01' | 'mc01' | 'arco';

/** Dano que um acerto de peso 1 causa, por nível do herói (nível 1: 6; nível 10: 24; nível 20: 44). */
export const danoPorUnidade = (nivel: number) => 4 + 2 * Math.max(1, nivel);
/** Os inimigos das zonas mais fundas têm um pouco mais de vida (+3% por zona). */
export const multiplicadorZona = (zona: number) => 1 + 0.03 * Math.max(0, zona);

/** Nenhum golpe tira mais que isso da vida máxima: são sempre pelo menos 3 acertos. */
export const LIMITE_GOLPE = 0.34;
/** Quanto a mais de dano causa a arma a que o inimigo é fraco. */
export const BONUS_FRAQUEZA = 0.25;

/** Vida do inimigo da lição: o total de "unidades" dos exercícios, na escala do nível do herói (elite: +30%). */
export function vidaDoInimigo(unidades: number, nivel: number, zona: number, elite = false): number {
  return Math.max(3, Math.round(Math.max(1, unidades) * danoPorUnidade(nivel) * multiplicadorZona(zona) * (elite ? 1.3 : 1)));
}

/** Dano de um acerto: peso do exercício na escala do nível, vezes os bônus (crítico, arma, ponto fraco), com o teto por golpe. */
export function danoDoGolpe(o: { unidades: number; nivel: number; mult: number; vidaMax: number }): number {
  const bruto = Math.round(o.unidades * danoPorUnidade(o.nivel) * o.mult);
  return Math.max(1, Math.min(bruto, Math.floor(o.vidaMax * LIMITE_GOLPE)));
}

// ---- chefes das zonas
/** Escala do chefe: cresce com o nível do herói (+12% por nível) e com a zona (+4% por zona). */
export const escalaBoss = (nivel: number, zona: number) => (1 + 0.12 * (Math.max(1, nivel) - 1)) * (1 + 0.04 * Math.max(0, zona));
export const vidaBoss = (nivel: number, zona: number) => Math.round(100 * escalaBoss(nivel, zona));
export const LIMITE_GOLPE_BOSS = 0.3;
/** Dano de um acerto no chefe: o dano de antes (22 a ~50) na escala do chefe, com Fúria, ponto fraco e o teto por golpe (30%). */
export function danoNoBoss(o: { bruto: number; nivel: number; zona: number; furiaPct: number; fraco: boolean }): number {
  const hp = vidaBoss(o.nivel, o.zona);
  const d = Math.round(o.bruto * escalaBoss(o.nivel, o.zona) * (1 + o.furiaPct / 100) * (o.fraco ? 1 + BONUS_FRAQUEZA : 1));
  return Math.max(1, Math.min(d, Math.floor(hp * LIMITE_GOLPE_BOSS)));
}

// ---- pontos fracos: cada inimigo e chefe apanha mais de um tipo de arma
export const FRAQUEZA_INIMIGO: Record<string, EstiloArma> = {
  morcego: 'arco', fogofatuo: 'mc01', bruxo: 'sw01', olho: 'arco', cao: 'ax01', lodo: 'mc01', monstro: 'sw01', golem: 'ax01',
};
export const FRAQUEZA_CHEFE: Record<string, EstiloArma> = {
  aranha: 'arco', besouro: 'arco', escaravelho: 'ax01', centopeia: 'mc01', gosma: 'sw01',
  diabrete: 'arco', caveira: 'mc01', lodo: 'sw01', golem: 'ax01', dragao: 'ax01',
};
export const NOME_ARMA: Record<EstiloArma, string> = { sw01: 'Espada', ax01: 'Machado', mc01: 'Maça', arco: 'Arco' };
