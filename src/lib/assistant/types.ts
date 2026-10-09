export type Problem = {
  linha: number | null;
  codigo: string;
  titulo: string;
  explicacao: string;
  como_corrigir: string;
  arquivo?: string | null;
};
export type Tip = {
  linha: number | null;
  titulo: string;
  explicacao: string;
  antes?: string | null;
  depois?: string | null;
  bug?: boolean;
};
/** Resposta do Pipo local (analisador em Python). */
export type LocalAnalysis = {
  titulo: string;
  humor: 'sad' | 'think' | 'cheer';
  problemas: Problem[];
  dicas: Tip[];
  corrigido: string | null;
  mudancas: string[];
};
/** Formato normalizado mostrado no painel, venha do Pipo local ou da IA. */
export type Review = LocalAnalysis & { fonte: 'local' | 'ia'; aviso?: string };

export type ReviewInput = {
  files: Record<string, string>;
  entry: string;
  stdin: string;
  output: string;
  error: string;
  local?: LocalAnalysis | null;
};
