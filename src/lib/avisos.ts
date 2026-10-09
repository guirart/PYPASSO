import { create } from 'zustand';
import type { NomeIcone } from '@/components/icones-data';

/** Avisos rápidos no topo da tela (nível novo, conquista, congelador usado...). */
export type Aviso = { id: number; icone: NomeIcone; titulo: string; texto?: string; tipo?: 'nivel' | 'conquista' | 'info' };

let seq = 0;
export const useAvisos = create<{ fila: Aviso[]; tirar: (id: number) => void }>()((set) => ({
  fila: [],
  tirar: (id) => set((s) => ({ fila: s.fila.filter((a) => a.id !== id) })),
}));

export function avisar(a: Omit<Aviso, 'id'>) {
  useAvisos.setState((s) => ({ fila: [...s.fila, { ...a, id: ++seq }].slice(-8) }));
}
