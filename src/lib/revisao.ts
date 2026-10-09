import { exercicioPorId } from '@/content';
import type { Exercise } from '@/content/types';
import type { CartaoRevisao } from './store';

export const MAX_REVISAO = 10;

/** Exercícios vencidos (os mais atrasados e mais errados primeiro). */
export function vencidos(revisao: Record<string, CartaoRevisao>, agora = Date.now()): string[] {
  return Object.entries(revisao ?? {})
    .filter(([id, c]) => c.due <= agora && exercicioPorId(id))
    .sort((a, b) => a[1].due - b[1].due || b[1].erros - a[1].erros)
    .map(([id]) => id);
}

export function filaDeRevisao(revisao: Record<string, CartaoRevisao>): Exercise[] {
  return vencidos(revisao).slice(0, MAX_REVISAO).map((id) => exercicioPorId(id)!.ex);
}

/** Quando vence o próximo (para mostrar "próxima revisão amanhã"). */
export function proximoVencimento(revisao: Record<string, CartaoRevisao>) {
  const ts = Object.values(revisao ?? {}).map((c) => c.due);
  return ts.length ? Math.min(...ts) : null;
}
