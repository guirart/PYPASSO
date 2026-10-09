// Edge Function: recebe os eventos do Stripe e atualiza public.assinaturas.
// Cadastre no Stripe (Desenvolvedores > Webhooks) a URL
//   https://<projeto>.supabase.co/functions/v1/stripe-webhook
// com os eventos: checkout.session.completed, customer.subscription.created,
// customer.subscription.updated, customer.subscription.deleted.
// Implante sem exigir login do Supabase: npx supabase functions deploy stripe-webhook --no-verify-jwt
//
// Segredos: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
import { linhaDoStripe, verificarStripe } from '../_shared/assinatura.ts';
import { admin, env, json, stripe } from '../_shared/http.ts';

Deno.serve(async (req) => {
  const corpo = await req.text();
  if (!(await verificarStripe(corpo, req.headers.get('Stripe-Signature'), env('STRIPE_WEBHOOK_SECRET')))) {
    return json({ error: 'assinatura inválida' }, 400);
  }
  const evento = JSON.parse(corpo);
  const db = admin();
  // Cada evento só é processado uma vez (o Stripe reenvia em caso de falha).
  const { error: dup } = await db.from('webhook_eventos').insert({ id: evento.id, origem: 'stripe' });
  if (dup) return json({ ok: true, repetido: true });
  try {
    let sub = null;
    let userId: string | null = null;
    const o = evento.data.object;
    if (evento.type === 'checkout.session.completed' && o.mode === 'subscription' && o.subscription) {
      sub = await stripe(`subscriptions/${o.subscription}`);
      userId = o.client_reference_id ?? o.metadata?.user_id ?? null;
    } else if (evento.type.startsWith('customer.subscription.')) {
      sub = o;
      userId = o.metadata?.user_id ?? null;
    }
    if (!sub) return json({ ok: true, ignorado: evento.type });
    if (!userId) {
      const { data } = await db.from('assinaturas').select('user_id').eq('stripe_customer_id', sub.customer).maybeSingle();
      userId = data?.user_id ?? null;
    }
    if (!userId) return json({ ok: true, semUsuario: true });
    const linha = linhaDoStripe(sub, userId);
    if (linha) await db.from('assinaturas').upsert({ ...linha, atualizado_em: new Date().toISOString() });
    return json({ ok: true });
  } catch (e) {
    console.error(e);
    await db.from('webhook_eventos').delete().eq('id', evento.id); // deixa o Stripe tentar de novo
    return json({ error: 'falha ao processar' }, 500);
  }
});
