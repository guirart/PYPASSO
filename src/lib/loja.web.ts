import type { Ciclo, Resultado } from './plus';
import { supabase } from './supabase';

/**
 * Assinatura na versão web: Stripe Checkout com cartão e Pix Automático.
 * O app chama as Edge Functions plus-checkout / plus-portal; o webhook do Stripe atualiza a
 * tabela assinaturas, e o app lê de lá (src/lib/plus.ts).
 *
 * Ligue com EXPO_PUBLIC_PLUS_WEB=1 depois de configurar o Stripe (veja PAGAMENTOS.md).
 */
const LIGADO = process.env.EXPO_PUBLIC_PLUS_WEB === '1';

async function chamar(fn: string, body: object) {
  const { data, error } = await supabase!.functions.invoke(fn, { body });
  if (error) {
    const ctx = (error as { context?: Response }).context;
    const msg = ctx ? (await ctx.json().catch(() => null))?.error : null;
    throw new Error(msg ?? 'Não foi possível falar com o servidor agora.');
  }
  return data as { url?: string; loja?: string; error?: string };
}

export const loja = {
  nome: 'cartão ou Pix',
  configurada: () => LIGADO && !!supabase,

  async identificar() { /* na web a conta é a própria sessão do Supabase */ },

  async status() { return null; }, // na web, quem sabe da assinatura é o servidor

  async precos() { return {} as Partial<Record<Ciclo, string>>; },

  async comprar(ciclo: Ciclo): Promise<Resultado> {
    const { data } = await supabase!.auth.getUser();
    if (!data.user) return { ok: false, mensagem: 'Entre na sua conta para assinar: assim o Plus vale na web e no celular.' };
    try {
      const r = await chamar('plus-checkout', { ciclo });
      if (!r.url) return { ok: false, mensagem: r.error ?? 'Não foi possível abrir o pagamento.' };
      window.location.assign(r.url); // página segura do Stripe (cartão ou Pix)
      return { ok: true, redirecionando: true };
    } catch (e) {
      return { ok: false, mensagem: (e as Error).message };
    }
  },

  async restaurar(): Promise<Resultado> { return { ok: true }; },

  async gerenciar(): Promise<Resultado> {
    try {
      const r = await chamar('plus-portal', {});
      if (r.loja) return { ok: false, mensagem: `Sua assinatura é pela ${r.loja === 'app_store' ? 'App Store' : 'Google Play'}: gerencie pelo celular, na loja.` };
      if (r.url) { window.location.assign(r.url); return { ok: true, redirecionando: true }; }
      return { ok: false, mensagem: r.error };
    } catch (e) {
      return { ok: false, mensagem: (e as Error).message };
    }
  },
};
