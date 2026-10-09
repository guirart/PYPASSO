// Edge Function: começa a assinatura Plus na versão web (Stripe Checkout com cartão e Pix Automático).
// No Android/iPhone a compra é pelas lojas (RevenueCat); esta função é só para a web.
//
// Segredos: STRIPE_SECRET_KEY, STRIPE_PRICE_MENSAL, STRIPE_PRICE_ANUAL, SITE_URL
// Implantação: npx supabase functions deploy plus-checkout
import { paramsCheckout, plusAtivo } from '../_shared/assinatura.ts';
import { admin, cors, env, json, stripe, usuario } from '../_shared/http.ts';

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ error: 'Use POST.' }, 405);
  try {
    const user = await usuario(req);
    if (!user) return json({ error: 'Entre na sua conta para assinar o Plus.' }, 401);
    const { ciclo } = await req.json().catch(() => ({}));
    if (ciclo !== 'mensal' && ciclo !== 'anual') return json({ error: 'Escolha o plano mensal ou anual.' }, 400);

    const db = admin();
    const { data: linha } = await db.from('assinaturas').select('*').eq('user_id', user.id).maybeSingle();
    if (plusAtivo(linha)) return json({ error: 'Você já é Plus.' }, 409);

    let customer = linha?.stripe_customer_id as string | undefined;
    if (!customer) {
      const c = await stripe('customers', new URLSearchParams({ email: user.email ?? '', 'metadata[user_id]': user.id }));
      customer = c.id as string;
      await db.from('assinaturas').upsert({
        user_id: user.id, origem: 'stripe', status: linha?.status ?? 'nenhuma', stripe_customer_id: customer, atualizado_em: new Date().toISOString(),
      });
    }
    const sessao = await stripe('checkout/sessions', paramsCheckout({
      ciclo, customer, userId: user.id, site: env('SITE_URL').replace(/\/$/, ''),
      priceId: env(ciclo === 'mensal' ? 'STRIPE_PRICE_MENSAL' : 'STRIPE_PRICE_ANUAL'),
      teste: !linha?.teste_usado,
    }));
    return json({ url: sessao.url });
  } catch (e) {
    console.error(e);
    return json({ error: 'Não foi possível abrir o pagamento agora. Tente de novo.' }, 500);
  }
});
