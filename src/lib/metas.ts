export const META_PADRAO = 30;

const emMs = (k: string) => { const [y, m, d] = k.split('-').map(Number); return new Date(y, m - 1, d).getTime(); };

/**
 * Meta diária adaptativa: a média dos últimos dias em que a pessoa estudou, com um empurrãozinho de 15%,
 * arredondada de 5 em 5 e entre 20 e 80 XP. Com menos de 3 dias de histórico, fica nos 30 XP de sempre.
 */
export function metaDiaria(xpDias: Record<string, number> | undefined, hoje: string): number {
  const dias = Object.entries(xpDias ?? {})
    .filter(([d, xp]) => d !== hoje && xp > 0)
    .sort((a, b) => emMs(b[0]) - emMs(a[0]))
    .slice(0, 5);
  if (dias.length < 3) return META_PADRAO;
  const media = dias.reduce((s, [, xp]) => s + xp, 0) / dias.length;
  return Math.min(80, Math.max(20, Math.round((media * 1.15) / 5) * 5));
}

/** Guarda só os 14 dias mais recentes. */
export function podarDias(xpDias: Record<string, number>): Record<string, number> {
  return Object.fromEntries(Object.entries(xpDias).sort((a, b) => emMs(b[0]) - emMs(a[0])).slice(0, 14));
}
