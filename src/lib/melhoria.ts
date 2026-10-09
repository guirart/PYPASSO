/**
 * Melhoria de peças com "pó de forja": desmontar uma peça dá pó, e o pó sobe o nível (+1 a +5) de uma peça que você ama,
 * reforçando as habilidades dela. Arquivo puro, sem imagens, para ser fácil de testar.
 */
export const MAX_MEL = 5;

/** Pó que sai ao desmontar uma peça, pelo nível da raridade (1 comum a 5 lendário). */
export const poeiraDeDesmontar = (nivelRaridade: number) => [1, 2, 4, 8, 15][Math.max(1, Math.min(5, nivelRaridade)) - 1];

/** Custo de subir a peça do nível `mel` para `mel + 1`: cresce com o nível da melhoria e com a raridade. */
export const custoMelhoria = (nivelRaridade: number, mel: number) => (mel + 1) * [2, 3, 5, 8, 12][Math.max(1, Math.min(5, nivelRaridade)) - 1];

/**
 * Valor de uma habilidade depois da melhoria. As porcentagens crescem 15% por nível; as habilidades "de contagem"
 * ganham em degraus: Relógio +1s a cada 2 níveis, Vitalidade cura 1 acerto antes a cada 2 níveis (mínimo 3),
 * Pipo +1 dica no nível 5 e Guarda +1 erro no nível 3 (máximo 3 de cada).
 */
export function valorMelhorado(id: string, v: number, mel: number): number {
  switch (id) {
    case 'crit': case 'xp': case 'moedas': case 'sorte': case 'dano': return Math.round(v * (1 + 0.15 * mel));
    case 'tempo': return v + Math.floor(mel / 2);
    case 'vida': return Math.max(3, v - Math.floor(mel / 2));
    case 'dica': return Math.min(3, v + (mel >= 5 ? 1 : 0));
    case 'protecao': return Math.min(3, v + (mel >= 3 ? 1 : 0));
    default: return v;
  }
}
