import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { loja } from './loja';
import { supabase } from './supabase';

/**
 * PyPasso Plus: vidas ilimitadas, para todos os perfis do aparelho.
 *
 * De onde vem a assinatura:
 * - Android/iPhone: Google Play ou App Store, via RevenueCat (src/lib/loja.native.ts).
 * - Web: Stripe Checkout com cartão ou Pix Automático (src/lib/loja.web.ts + Edge Functions).
 * - Com conta, o servidor também guarda a assinatura (tabela assinaturas), então quem assinou
 *   na web tem Plus no celular e vice-versa.
 * - Sem chaves configuradas, o app fica em MODO DEMONSTRAÇÃO: dá para ver e testar o Plus sem
 *   nenhum pagamento real.
 */
export type Ciclo = 'mensal' | 'anual';
export const PLANOS = {
  mensal: { preco: 'R$ 14,90', por: '/mês', detalhe: 'cobrado todo mês' },
  anual: { preco: 'R$ 119,90', por: '/ano', detalhe: 'equivale a R$ 9,99/mês', economia: 'Economize 33%' },
} as const;
export const DIAS_TESTE = 7;

type Fonte = 'loja' | 'servidor' | 'demo';
type State = {
  ativo: boolean;
  fonte: Fonte | null;
  ciclo: Ciclo | null;
  expiraEm: string | null;
  cancelada: boolean;
  demo: boolean; // Plus de demonstração ligado
};

export const usePlus = create<State>()(
  persist(() => ({ ativo: false, fonte: null, ciclo: null, expiraEm: null, cancelada: false, demo: false } as State), {
    name: 'pypasso-plus',
    storage: createJSONStorage(() => AsyncStorage),
  }),
);

/** Sem chaves de loja/Stripe, tudo vira demonstração (nenhuma cobrança). */
export const modoDemo = () => !loja.configurada();
export const nomeDaLoja = () => loja.nome;

const ativoNaLinha = (l: { status: string; expira_em: string | null } | null) =>
  !!l && ['teste', 'ativa', 'cancelada', 'atrasada'].includes(l.status) && (!l.expira_em || Date.parse(l.expira_em) > Date.now());

/** Junta o que a loja diz (no aparelho) com o que o servidor diz (pela conta). */
export async function atualizarPlus() {
  if (modoDemo()) {
    const d = usePlus.getState().demo;
    usePlus.setState({ ativo: d, fonte: d ? 'demo' : null });
    return usePlus.getState();
  }
  const [doAparelho, doServidor] = await Promise.all([
    loja.status().catch(() => null),
    (async () => {
      if (!supabase) return null;
      const { data: auth } = await supabase.auth.getUser();
      if (!auth.user) return null;
      const { data } = await supabase.from('assinaturas').select('status, ciclo, expira_em').eq('user_id', auth.user.id).maybeSingle();
      return data;
    })().catch(() => null),
  ]);
  if (doAparelho?.ativo) {
    usePlus.setState({ ativo: true, fonte: 'loja', ciclo: doAparelho.ciclo ?? null, expiraEm: doAparelho.expiraEm ?? null, cancelada: !!doAparelho.cancelada, demo: false });
  } else if (ativoNaLinha(doServidor)) {
    usePlus.setState({ ativo: true, fonte: 'servidor', ciclo: (doServidor!.ciclo as Ciclo) ?? null, expiraEm: doServidor!.expira_em, cancelada: doServidor!.status === 'cancelada', demo: false });
  } else {
    usePlus.setState({ ativo: false, fonte: null, ciclo: null, expiraEm: null, cancelada: false, demo: false });
  }
  return usePlus.getState();
}

export type Resultado = { ok: boolean; mensagem?: string; redirecionando?: boolean };

export async function assinar(ciclo: Ciclo): Promise<Resultado> {
  if (modoDemo()) {
    usePlus.setState({
      ativo: true, fonte: 'demo', demo: true, ciclo, cancelada: false,
      expiraEm: new Date(Date.now() + DIAS_TESTE * 864e5).toISOString(),
    });
    return { ok: true, mensagem: 'Plus de demonstração ativado. Nenhum pagamento foi feito.' };
  }
  const r = await loja.comprar(ciclo);
  if (r.ok && !r.redirecionando) await atualizarPlus();
  return r;
}

export async function restaurar(): Promise<Resultado> {
  if (modoDemo()) return { ok: false, mensagem: 'No modo demonstração não há compras para restaurar.' };
  const r = await loja.restaurar();
  const s = await atualizarPlus();
  return s.ativo ? { ok: true, mensagem: 'Assinatura restaurada!' } : r.ok ? { ok: false, mensagem: 'Nenhuma assinatura encontrada nesta conta da loja.' } : r;
}

export async function gerenciar(): Promise<Resultado> {
  if (modoDemo()) {
    usePlus.setState({ ativo: false, fonte: null, ciclo: null, expiraEm: null, demo: false });
    return { ok: true, mensagem: 'Plus de demonstração desligado.' };
  }
  return loja.gerenciar();
}

/** Liga a identidade da loja à conta (para o servidor saber de quem é a compra). */
export async function ligarContaNaLoja(userId: string | null) {
  await loja.identificar(userId).catch(() => {});
  await atualizarPlus().catch(() => {});
}

/** Preços reais da loja (obrigatório mostrar o preço da loja no Android/iPhone). */
export const precosDaLoja = () => loja.precos().catch(() => ({} as Partial<Record<Ciclo, string>>));
