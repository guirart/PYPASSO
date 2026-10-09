import builtinsRaw from './builtins.json';
import libsRaw from './bibliotecas.json';
import logicaRaw from './logica.json';
import raw from './course.json';
import type { Course, Lesson } from './types';

/**
 * Duas trilhas: "Python do zero" (course.json) e "71 funções embutidas"
 * (builtins.json, gerada por tools/gerar_builtins.py). O progresso é um só.
 */
export const COURSE = raw as Course;
export const BUILTINS = builtinsRaw as unknown as Course;
/** Trilha "Bibliotecas": uma unidade por biblioteca (gerada por tools/gerar_bibliotecas.py). */
export const LIBS = libsRaw as unknown as Course;

/** Trilha "Lógica" (gerada por tools/gerar_logica.mjs). */
export const LOGICA = logicaRaw as unknown as Course;

export type TrackId = 'main' | 'builtins' | 'libs' | 'logica';
export const TRACKS: { id: TrackId; title: string; short: string; course: Course }[] = [
  { id: 'main', title: 'Python do zero', short: 'Python do zero', course: COURSE },
  { id: 'builtins', title: '71 funções embutidas', short: '71 built-ins', course: BUILTINS },
  { id: 'libs', title: 'Bibliotecas do Python', short: 'Bibliotecas', course: LIBS },
  { id: 'logica', title: 'Lógica e Prolog', short: 'Lógica', course: LOGICA },
];

export type FlatLesson = Lesson & { unitIndex: number; lessonIndex: number; order: number; track: TrackId };

const flatten = (course: Course, track: TrackId): FlatLesson[] =>
  course.units
    .flatMap((u, unitIndex) => u.lessons.map((l, lessonIndex) => ({ ...l, unitIndex, lessonIndex, order: 0, track })))
    .map((l, order) => ({ ...l, order }));

export const LESSONS_BY_TRACK: Record<TrackId, FlatLesson[]> = {
  main: flatten(COURSE, 'main'),
  builtins: flatten(BUILTINS, 'builtins'),
  libs: flatten(LIBS, 'libs'),
  logica: flatten(LOGICA, 'logica'),
};
/** Todas as lições, das duas trilhas (para buscar por id e para o treino). */
export const LESSONS: FlatLesson[] = [...LESSONS_BY_TRACK.main, ...LESSONS_BY_TRACK.builtins, ...LESSONS_BY_TRACK.libs, ...LESSONS_BY_TRACK.logica];
export const lessonById = (id: string) => LESSONS.find((l) => l.id === id);
export const courseOf = (track: TrackId) => TRACKS.find((t) => t.id === track)!.course;

/** Ids antigos da trilha de built-ins (b0l0…) → lição 1 da unidade da função. */
export const LEGACY_IDS: Record<string, string> = (builtinsRaw as { legacyIds?: Record<string, string> }).legacyIds ?? {};

/** Exercício por id (todas as trilhas), para a Revisão espaçada. */
let _ex: Map<string, { ex: import('./types').Exercise; lesson: FlatLesson }> | null = null;
export function exercicioPorId(id: string) {
  if (!_ex) {
    _ex = new Map();
    for (const l of LESSONS) for (const ex of l.exercises) _ex.set(ex.id, { ex, lesson: l });
  }
  return _ex.get(id);
}
