/**
 * "Explique com suas palavras": compara o texto da pessoa com as palavras-chave do conceito que ela acabou de ver.
 * Não é uma correção de IA: só confere se as ideias principais apareceram.
 */
const PARADA = new Set(('para com uma uns umas que por mais como mas ele ela eles elas isso essa esse esta este aqui onde quando entre sobre ' +
  'sempre depois antes ainda assim pode podem fazer faz fica ficam seja ser sao nao sim muito pouco cada todo toda todos todas outro outra dentro fora ' +
  'quer quiser voce vai vao tem tambem apenas so seus suas seu sua nosso nossa pelo pela pelos pelas numa nuns').split(' '));

export const normalizar = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
const palavras = (s: string) => normalizar(s).split(/[^a-z0-9_]+/).filter((w) => w.length >= 4 && !PARADA.has(w));
/** Raiz simples para "listas" casar com "lista" e "imprime" com "imprimir". */
const raiz = (w: string) => w.replace(/(mente|oes|ao|as|os|es|ar|er|ir|a|e|o|s)$/, '');

/** As palavras mais importantes do conceito: as do título e as mais repetidas no texto. */
export function palavrasChave(titulo: string, corpo: string, max = 6): string[] {
  const peso = new Map<string, number>();
  for (const w of palavras(titulo)) peso.set(w, (peso.get(w) ?? 0) + 3);
  for (const w of palavras(corpo)) peso.set(w, (peso.get(w) ?? 0) + 1);
  return [...peso.entries()].sort((a, b) => b[1] - a[1] || b[0].length - a[0].length).slice(0, max).map(([w]) => w);
}

export type Comparacao = { citadas: string[]; faltaram: string[]; ok: boolean; curto: boolean };
export function compararExplicacao(texto: string, titulo: string, corpo: string): Comparacao {
  const chaves = palavrasChave(titulo, corpo);
  const dele = new Set(palavras(texto).map(raiz));
  const citadas = chaves.filter((c) => dele.has(raiz(c)));
  const faltaram = chaves.filter((c) => !citadas.includes(c));
  const curto = texto.trim().length < 25;
  return { citadas, faltaram, curto, ok: !curto && citadas.length >= Math.max(2, Math.ceil(chaves.length * 0.4)) };
}
