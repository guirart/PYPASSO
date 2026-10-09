import data from './provas.json';

/** Bug da Prova de fogo. Gerado e conferido por tools/gerar_provas.py. */
export type Bug = {
  id: string; nivel: number; linhas: string[]; linha: number; correcao: string;
  explica: string; tipo: string; msg: string; u: string | null;
};
/** Bugs de Python (Prova de fogo, Detetive, Museu). */
export const BUGS = (data as { bugs: Bug[] }).bugs;

/** Prova que fecha a unidade: quantos bugs, e o tempo de cada um. */
export const FIRE_ROUND = 5;
const SECS: Record<number, number> = { 1: 20, 2: 18, 3: 15 };
export const unitBugs = (unitId: string) => BUGS.filter((b) => b.u === unitId);
export const fireSecs = (unitId: string) => SECS[unitBugs(unitId)[0]?.nivel ?? 2];
