import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

/** Preferência de lembrete (vale para o aparelho). */
export const useLembretes = create<{ ativo: boolean; hora: number; minuto: number; set: (p: Partial<{ ativo: boolean; hora: number; minuto: number }>) => void }>()(
  persist((set) => ({ ativo: false, hora: 19, minuto: 0, set: (p) => set(p) }), { name: 'pypasso-lembretes', storage: createJSONStorage(() => AsyncStorage) }),
);

export const HORARIOS: [number, number][] = [[8, 0], [12, 30], [18, 0], [19, 0], [20, 30], [22, 0]];
export const fmtHora = (h: number, m: number) => `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;

/** Mensagens do Pipo (sorteadas). {n} = dias seguidos. */
const COM_SEQUENCIA = [
  ['{n} dias seguidos!', 'Não deixa a chama apagar: uma lição rapidinha e está garantido.'],
  ['O Pipo está te esperando', 'Sua sequência de {n} dias depende de 5 minutinhos hoje.'],
  ['Ainda dá tempo!', 'Faz uma lição e mantém seus {n} dias. O Pipo já separou os exercícios.'],
];
const SEM_SEQUENCIA = [
  ['Bora codar?', 'Uma lição de 5 minutos e você começa uma sequência nova.'],
  ['Pergunta do Pipo', 'O que print(len("Python")) mostra? Abre o PyPasso para descobrir!'],
  ['Missões do dia', 'Tem 3 missões novas e um baú de moedas esperando por você.'],
];
export function mensagem(streak: number, i: number) {
  const lista = streak > 0 ? COM_SEQUENCIA : SEM_SEQUENCIA;
  const [titulo, corpo] = lista[i % lista.length];
  return { titulo: titulo.replace('{n}', String(streak)), corpo: corpo.replace('{n}', String(streak)) };
}
