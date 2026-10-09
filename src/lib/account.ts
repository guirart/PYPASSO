import { useGame } from './store';
import { supabase } from './supabase';
import type { Review } from './assistant/types';

/** Exclui a conta na nuvem (Edge Function excluir-conta) e limpa o aparelho. */
export async function deleteAccount(): Promise<{ ok: boolean; message?: string }> {
  if (!supabase) return { ok: false, message: 'Login não configurado.' };
  const { data, error } = await supabase.functions.invoke('excluir-conta', { body: {} });
  if (error || !data?.ok) return { ok: false, message: data?.error ?? 'Não foi possível excluir agora. Tente de novo mais tarde.' };
  await supabase.auth.signOut().catch(() => {});
  useGame.getState().reset();
  return { ok: true };
}

/** Denuncia uma resposta da IA (guardada para revisão). Funciona mesmo sem login: nesse caso só confirma. */
export async function reportAIAnswer(review: Review, motivo: string): Promise<boolean> {
  if (!supabase) return true;
  const { data } = await supabase.auth.getUser();
  if (!data.user) return true;
  const { error } = await supabase.from('ai_reports').insert({
    user_id: data.user.id,
    motivo: motivo.slice(0, 300),
    resposta: { titulo: review.titulo, problemas: review.problemas, dicas: review.dicas, corrigido: review.corrigido, mudancas: review.mudancas },
  });
  return !error;
}
