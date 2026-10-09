// Edge Function: abre a área do Stripe para trocar o cartão/Pix ou cancelar o Plus (web).
// Assinaturas feitas pelo Google Play ou App Store são gerenciadas na própria loja.
//
// Segredos: STRIPE_SECRET_KEY, SITE_URL
import { admin, cors, env, json, stripe, usuario } from '../_shared/http.ts';

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ error: 'Use POST.' }, 405);
  try {
    const user = await usuario(req);
    if (!user) return json({ error: 'Entre na sua conta.' }, 401);
    const { data: linha } = await admin().from('assinaturas').select('origem, stripe_customer_id').eq('user_id', user.id).maybeSingle();
    if (linha && linha.origem !== 'stripe') return json({ loja: linha.origem });
    if (!linha?.stripe_customer_id) return json({ error: 'Você ainda não tem assinatura.' }, 404);
    const s = await stripe('billing_portal/sessions', new URLSearchParams({
      customer: linha.stripe_customer_id, return_url: `${env('SITE_URL').replace(/\/$/, '')}/plus`, locale: 'pt-BR',
    }));
    return json({ url: s.url });
  } catch (e) {
    console.error(e);
    return json({ error: 'Não foi possível abrir agora. Tente de novo.' }, 500);
  }
});
