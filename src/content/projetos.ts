import raw from './projetos.json';

/** Projetos guiados (gerados por tools/validar_projetos.py a partir de tools/projetos/). */
export type Passo = { titulo: string; explica: string; tarefa: string; starter: string; solucao: string; tests: string; dica: string };
export type Projeto = { id: string; titulo: string; emoji: string; resumo: string; requer: string; entrada: string; passos: Passo[] };
export const PROJETOS = (raw as { projetos: Projeto[] }).projetos;
export const projetoPorId = (id: string) => PROJETOS.find((p) => p.id === id);

/** Ícone e cor de cada projeto (sem emoji). */
export const ICONE_PROJ: Record<string, import('@/components/icones-data').NomeIcone> = { adivinha: 'dados', calculadora: 'calculadora', tarefas: 'lista', forca: 'forca', quiz: 'pergunta', rpg: 'batalha' };
export const COR_PROJ: Record<string, string> = { adivinha: '#7B5CE0', calculadora: '#2F6FD6', tarefas: '#3FA34D', forca: '#B07A3F', quiz: '#E0457B', rpg: '#E5383B' };
