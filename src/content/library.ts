import raw from './library.json';

export type LibParam = { nome: string; desc: string };
export type LibEntry = {
  id: string; nome: string; cat: string; sig: string; resumo: string; explica: string;
  params: LibParam[]; retorna: string; exemplo: string; saida: string; entrada: string;
  cuidado: string | null; rel: string[]; tags: string;
  licao: string | null; // lição correspondente (trilha das 71 built-ins)
  builtin: boolean;
};
export type LibCategory = { id: string; nome: string; desc: string };

const lib = raw as { categorias: LibCategory[]; funcoes: LibEntry[] };
export const LIB_CATS = lib.categorias;
export const LIB = lib.funcoes;
export const libById = (id: string) => LIB.find((f) => f.id === id);
export const catName = (id: string) => LIB_CATS.find((c) => c.id === id)?.nome ?? id;

/** Tira acentos e deixa minúsculo, para a busca achar "funcao" e "função". */
export const norm = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

const INDEX = LIB.map((f) => ({ f, text: norm(`${f.nome} ${f.id} ${f.resumo} ${f.tags} ${catName(f.cat)} ${f.sig}`) }));

/** Busca: todas as palavras digitadas precisam aparecer; nome que começa com o termo vem primeiro. */
export function searchLib(q: string): LibEntry[] {
  const words = norm(q).trim().split(/\s+/).filter(Boolean);
  if (!words.length) return LIB;
  return INDEX.filter((x) => words.every((w) => x.text.includes(w)))
    .map((x) => ({ f: x.f, score: norm(x.f.nome).replace(/^[.\s]+/, '').startsWith(words[0]) ? 0 : norm(x.f.nome).includes(words[0]) ? 1 : 2 }))
    .sort((a, b) => a.score - b.score)
    .map((x) => x.f);
}
