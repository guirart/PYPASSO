export type HostId = 'pipo' | 'ana' | 'caio' | 'bia' | 'teo';

type Base = { id: string; q: string; e: string; host: HostId };

export type ChoiceEx = Base & { k: 'mc' | 'out'; c?: string; o: string[]; mono?: boolean }; // o[0] é a correta
export type FillEx = Base & { k: 'fill'; c: string; b: string[]; a: string[] }; // ___ marca lacunas
export type OrderEx = Base & { k: 'order'; l: string[] }; // l na ordem correta
export type TypeEx = Base & { k: 'type'; c: string; a: string[] };
export type CodeEx = Base & { k: 'code'; starter: string; tests: string };
/** Cartão que ensina um conceito antes de cobrá-lo. q = título. */
export type LearnEx = Base & { k: 'learn'; body: string; c: string; out: string; rc?: string; ro?: string };

export type Exercise = ChoiceEx | FillEx | OrderEx | TypeEx | CodeEx | LearnEx;
export type Lesson = { id: string; title: string; exercises: Exercise[] };
export type Unit = { id: string; title: string; description: string; lessons: Lesson[]; group?: string };
export type Course = { units: Unit[] };
