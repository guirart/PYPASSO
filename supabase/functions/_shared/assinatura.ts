// Regras da assinatura Plus, sem dependências do Deno (testadas em tools/testar_assinatura.mjs).
//
// A tabela public.assinaturas guarda uma linha por usuário. Quem escreve nela é só o servidor
// (webhooks do Stripe e do RevenueCat). O app só lê a própria linha.

export type Status = 'nenhuma' | 'teste' | 'ativa' | 'cancelada' | 'atrasada' | 'expirada';
export type Origem = 'stripe' | 'play_store' | 'app_store' | 'outra';
export type Linha = {
  user_id: string;
  origem: Origem;
  status: Status;
  ciclo: 'mensal' | 'anual' | null;
  expira_em: string | null;
  teste_usado?: boolean;
  stripe_customer_id?: string | null;
  stripe_subscription_id?: string | null;
};

export const PRECOS = {
  mensal: { centavos: 1490, texto: 'R$ 14,90/mês', pix: 'monthly' },
  anual: { centavos: 11990, texto: 'R$ 119,90/ano', pix: 'yearly' },
} as const;
export const DIAS_TESTE = 7;

/** Plus vale enquanto não expirou (cancelada = vale até o fim do período já pago). */
export const plusAtivo = (l: Pick<Linha, 'status' | 'expira_em'> | null | undefined, agora = Date.now()) =>
  !!l && ['teste', 'ativa', 'cancelada', 'atrasada'].includes(l.status) && (!l.expira_em || Date.parse(l.expira_em) > agora);

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const iso = (s: number | null | undefined) => (s ? new Date(s * 1000).toISOString() : null);

// ------------------------------------------------------------------ Stripe
/**
 * Confere o cabeçalho Stripe-Signature ("t=...,v1=...") com HMAC-SHA256 do segredo do webhook.
 * Recusa eventos com mais de `tolerancia` segundos (proteção contra reenvio).
 */
export async function verificarStripe(corpo: string, cabecalho: string | null, segredo: string, tolerancia = 300, agora = Date.now() / 1000) {
  if (!cabecalho || !segredo) return false;
  const partes = Object.fromEntries(cabecalho.split(',').map((p) => p.split('=', 2) as [string, string]));
  const t = Number(partes.t);
  const assinaturas = cabecalho.split(',').filter((p) => p.startsWith('v1=')).map((p) => p.slice(3));
  if (!t || !assinaturas.length || Math.abs(agora - t) > tolerancia) return false;
  const chave = await crypto.subtle.importKey('raw', new TextEncoder().encode(segredo), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const mac = new Uint8Array(await crypto.subtle.sign('HMAC', chave, new TextEncoder().encode(`${t}.${corpo}`)));
  const esperado = Array.from(mac, (b) => b.toString(16).padStart(2, '0')).join('');
  return assinaturas.some((a) => igual(a, esperado));
}
/** Comparação em tempo constante. */
function igual(a: string, b: string) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

type StripeSub = {
  id: string; customer: string; status: string; cancel_at_period_end?: boolean; trial_end?: number | null;
  current_period_end?: number; metadata?: Record<string, string>;
  items?: { data: { current_period_end?: number; price?: { recurring?: { interval?: string } } }[] };
};

/** Converte uma assinatura do Stripe na linha da tabela (ou null se ainda não vale nada). */
export function linhaDoStripe(sub: StripeSub, userId: string): Linha | null {
  const item = sub.items?.data?.[0];
  // Em versões novas da API o fim do período fica no item da assinatura.
  const fim = sub.current_period_end ?? item?.current_period_end ?? null;
  const mapa: Record<string, Status> = {
    trialing: 'teste', active: 'ativa', past_due: 'atrasada',
    canceled: 'expirada', unpaid: 'expirada', incomplete_expired: 'expirada', paused: 'expirada',
  };
  let status = mapa[sub.status];
  if (!status) return null; // "incomplete": esperando o Pix/cartão ser autorizado
  if (sub.cancel_at_period_end && (status === 'ativa' || status === 'teste')) status = 'cancelada';
  const intervalo = item?.price?.recurring?.interval;
  return {
    user_id: userId,
    origem: 'stripe',
    status,
    ciclo: intervalo === 'year' ? 'anual' : intervalo === 'month' ? 'mensal' : null,
    expira_em: iso(fim),
    teste_usado: true,
    stripe_customer_id: sub.customer,
    stripe_subscription_id: sub.id,
  };
}

/** Parâmetros do Checkout (assinatura com cartão e Pix Automático; 7 dias grátis na primeira vez). */
export function paramsCheckout(o: { ciclo: 'mensal' | 'anual'; priceId: string; customer: string; userId: string; site: string; teste: boolean }) {
  const p = new URLSearchParams({
    mode: 'subscription',
    customer: o.customer,
    client_reference_id: o.userId,
    locale: 'pt-BR',
    allow_promotion_codes: 'true',
    'line_items[0][price]': o.priceId,
    'line_items[0][quantity]': '1',
    success_url: `${o.site}/plus?status=ok`,
    cancel_url: `${o.site}/plus?status=cancelado`,
    'subscription_data[metadata][user_id]': o.userId,
    'metadata[user_id]': o.userId,
    // Pix Automático: a pessoa autoriza no app do banco; o banco avisa 3 dias antes de cada cobrança.
    'payment_method_options[pix][mandate_options][payment_schedule]': PRECOS[o.ciclo].pix,
    'payment_method_options[pix][mandate_options][amount_type]': 'maximum',
    // Teto com folga para reajuste de preço (o mandato não precisa ser refeito).
    'payment_method_options[pix][mandate_options][amount]': String(Math.ceil(PRECOS[o.ciclo].centavos * 1.5)),
    'payment_method_options[pix][mandate_options][reference]': 'PyPasso Plus',
  });
  if (o.teste) p.set('subscription_data[trial_period_days]', String(DIAS_TESTE));
  return p;
}

// ------------------------------------------------------------------ RevenueCat (Google Play / App Store)
type RCEvento = {
  type: string; app_user_id?: string; original_app_user_id?: string; aliases?: string[];
  expiration_at_ms?: number | null; period_type?: string; store?: string; product_id?: string;
  entitlement_ids?: string[] | null; environment?: string;
};

/** O app identifica o usuário no RevenueCat pelo id do Supabase (um UUID). */
export function usuarioDoEvento(e: RCEvento): string | null {
  const ids = [e.app_user_id, e.original_app_user_id, ...(e.aliases ?? [])];
  return ids.find((x): x is string => !!x && UUID.test(x)) ?? null;
}

export function linhaDoRevenueCat(e: RCEvento, entitlement = 'plus'): Linha | null {
  const userId = usuarioDoEvento(e);
  if (!userId) return null; // compra feita sem conta: vale no aparelho; vira linha quando a pessoa entrar
  if (e.entitlement_ids && !e.entitlement_ids.includes(entitlement)) return null;
  const origem: Origem = e.store === 'PLAY_STORE' ? 'play_store' : e.store === 'APP_STORE' || e.store === 'MAC_APP_STORE' ? 'app_store' : e.store === 'STRIPE' || e.store === 'RC_BILLING' ? 'stripe' : 'outra';
  const exp = e.expiration_at_ms ? new Date(e.expiration_at_ms).toISOString() : null;
  const teste = e.period_type === 'TRIAL';
  let status: Status;
  switch (e.type) {
    case 'INITIAL_PURCHASE': case 'RENEWAL': case 'UNCANCELLATION': case 'PRODUCT_CHANGE':
    case 'SUBSCRIPTION_EXTENDED': case 'TEMPORARY_ENTITLEMENT_GRANT': case 'NON_RENEWING_PURCHASE':
      status = teste ? 'teste' : 'ativa'; break;
    case 'CANCELLATION': status = 'cancelada'; break;
    case 'BILLING_ISSUE': status = 'atrasada'; break;
    case 'EXPIRATION': case 'SUBSCRIPTION_PAUSED': status = 'expirada'; break;
    default: return null; // TEST, TRANSFER etc.: nada a gravar
  }
  const pid = (e.product_id ?? '').toLowerCase();
  return {
    user_id: userId, origem, status,
    ciclo: /anual|annual|year|ano/.test(pid) ? 'anual' : /mensal|month|mes/.test(pid) ? 'mensal' : null,
    expira_em: exp, teste_usado: true,
  };
}
